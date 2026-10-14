"""
X (Twitter) API v2 posting client -- stdlib only.

Uses OAuth 1.0a user-context signing, which is what POST /2/tweets requires.
No third-party packages, so this runs from launchd against system Python.

Required environment variables (see .env.example):
    X_API_KEY             consumer key
    X_API_SECRET          consumer secret
    X_ACCESS_TOKEN        user access token (must be for the Honorbrook account)
    X_ACCESS_TOKEN_SECRET user access token secret
"""

import base64
import hashlib
import hmac
import json
import os
import time
import urllib.parse
import urllib.request
import urllib.error
import uuid

ENDPOINT = "https://api.x.com/2/tweets"
# Media upload. Sources disagree on whether the v2 endpoint is live for every app,
# so try v2 first and fall back to the v1.1 host. Both take multipart bodies,
# which OAuth 1.0a does not sign, so the same header builder works for both.
MEDIA_V2 = "https://api.x.com/2/media/upload"
MEDIA_V11 = "https://upload.twitter.com/1.1/media/upload.json"
ALT_V11 = "https://upload.twitter.com/1.1/media/metadata/create.json"
MAX_IMAGE_BYTES = 5 * 1024 * 1024


class NotConfigured(Exception):
    pass


class PostError(Exception):
    pass


def _creds():
    keys = ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET")
    vals = [os.environ.get(k, "").strip() for k in keys]
    missing = [k for k, v in zip(keys, vals) if not v]
    if missing:
        raise NotConfigured("missing env vars: %s" % ", ".join(missing))
    return vals


def _quote(s):
    # OAuth percent-encoding: unreserved set is ALPHA / DIGIT / '-' / '.' / '_' / '~'
    return urllib.parse.quote(str(s), safe="~-._")


def _sign(method, url, oauth_params, consumer_secret, token_secret):
    """Build the OAuth 1.0a HMAC-SHA1 signature.

    The JSON request body is deliberately excluded from the signature base
    string: OAuth 1.0a only signs form-encoded bodies, and this endpoint takes
    application/json.
    """
    normalized = "&".join(
        "%s=%s" % (_quote(k), _quote(v))
        for k, v in sorted(oauth_params.items())
    )
    base = "&".join([method.upper(), _quote(url), _quote(normalized)])
    signing_key = "%s&%s" % (_quote(consumer_secret), _quote(token_secret))
    digest = hmac.new(
        signing_key.encode("utf-8"), base.encode("utf-8"), hashlib.sha1
    ).digest()
    return base64.b64encode(digest).decode("ascii")


def _auth_header(method, url, extra=None):
    api_key, api_secret, token, token_secret = _creds()
    params = {
        "oauth_consumer_key": api_key,
        "oauth_nonce": uuid.uuid4().hex,
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_token": token,
        "oauth_version": "1.0",
    }
    # Form-encoded bodies and query strings ARE part of an OAuth 1.0a signature
    # (JSON and multipart bodies are not); sign them but don't send them in the header.
    signed = dict(params)
    signed.update(extra or {})
    params["oauth_signature"] = _sign(
        method, url, signed, api_secret, token_secret
    )
    return "OAuth " + ", ".join(
        '%s="%s"' % (_quote(k), _quote(v)) for k, v in sorted(params.items())
    )


def _multipart(fields, filename, data):
    boundary = uuid.uuid4().hex
    parts = []
    for k, v in fields.items():
        parts.append(("--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n"
                      % (boundary, k, v)).encode())
    parts.append(("--%s\r\nContent-Disposition: form-data; name=\"media\"; filename=\"%s\"\r\n"
                  "Content-Type: image/png\r\n\r\n" % (boundary, filename)).encode())
    parts.append(data)
    parts.append(("\r\n--%s--\r\n" % boundary).encode())
    return b"".join(parts), "multipart/form-data; boundary=%s" % boundary


def _send(url, body, ctype):
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", _auth_header("POST", url))
    req.add_header("Content-Type", ctype)
    req.add_header("User-Agent", "honorbrook-social/1.0")
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw) if raw.strip() else {}


def upload_image(path, alt=None):
    """Upload a PNG/JPEG and return its media id string. Raises PostError."""
    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_IMAGE_BYTES:
        raise PostError("image is %d bytes; X images must be under 5MB" % len(data))
    name = os.path.basename(path)
    errors = []
    media_id = None
    for url, fields in ((MEDIA_V2, {"media_category": "tweet_image"}),
                        (MEDIA_V11, {"media_category": "tweet_image"})):
        body, ctype = _multipart(fields, name, data)
        try:
            resp = _send(url, body, ctype)
        except urllib.error.HTTPError as e:
            errors.append("%s HTTP %d %s" % (url, e.code, e.read().decode("utf-8", "replace")[:200]))
            continue
        except urllib.error.URLError as e:
            raise PostError("network error uploading image to X: %s" % e)
        mid = resp.get("media_id_string") or resp.get("data", {}).get("id") or resp.get("id")
        if mid:
            media_id = str(mid)
            break
        errors.append("%s returned no media id: %s" % (url, str(resp)[:200]))
    if not media_id:
        raise PostError("X image upload failed: " + " | ".join(errors))
    if alt:
        try:  # best effort: a missing alt text must never block the post
            _send(ALT_V11, json.dumps({"media_id": media_id,
                                       "alt_text": {"text": alt[:1000]}}).encode(),
                  "application/json")
        except Exception:
            pass
    return media_id


def _form(url, fields):
    body = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", _auth_header("POST", url, fields))
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("User-Agent", "honorbrook-social/1.0")
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw) if raw.strip() else {}


def upload_video(path, timeout_s=180):
    """Chunked v1.1 upload (INIT/APPEND/FINALIZE + STATUS). Returns the media id."""
    size = os.path.getsize(path)
    if size > 512 * 1024 * 1024:
        raise PostError("video too large for X")
    try:
        mid = str(_form(MEDIA_V11, {"command": "INIT", "total_bytes": size,
                                    "media_type": "video/mp4",
                                    "media_category": "tweet_video"})["media_id_string"])
        with open(path, "rb") as fh:
            seg = 0
            while True:
                chunk = fh.read(4 * 1024 * 1024)
                if not chunk:
                    break
                body, ctype = _multipart({"command": "APPEND", "media_id": mid,
                                          "segment_index": seg}, os.path.basename(path), chunk)
                _send(MEDIA_V11, body, ctype)
                seg += 1
        info = _form(MEDIA_V11, {"command": "FINALIZE", "media_id": mid}).get("processing_info")
        waited = 0
        while info and info.get("state") in ("pending", "in_progress"):
            wait = int(info.get("check_after_secs", 2))
            time.sleep(wait); waited += wait
            if waited > timeout_s:
                raise PostError("X video processing timed out")
            q = {"command": "STATUS", "media_id": mid}
            url = MEDIA_V11 + "?" + urllib.parse.urlencode(q)
            req = urllib.request.Request(url, method="GET")
            req.add_header("Authorization", _auth_header("GET", MEDIA_V11, q))
            with urllib.request.urlopen(req, timeout=30) as resp:
                info = json.loads(resp.read().decode()).get("processing_info")
        if info and info.get("state") == "failed":
            raise PostError("X rejected the video: %s" % info.get("error", info))
        return mid
    except urllib.error.HTTPError as e:
        raise PostError("X video upload HTTP %d: %s"
                        % (e.code, e.read().decode("utf-8", "replace")[:300]))
    except (KeyError, urllib.error.URLError) as e:
        raise PostError("X video upload failed: %s" % e)


def post(text, reply_to=None, image_path=None, image_alt=None, video_path=None, dry_run=False):
    """Publish one post. Returns the new post id, or a fake id on dry_run."""
    payload = {"text": text}
    if video_path and not dry_run:
        try:
            payload["media"] = {"media_ids": [upload_video(video_path)]}
        except (PostError, OSError) as e:
            print("         [warn] X video skipped, posting text only: %s" % e)
    elif image_path and not dry_run:
        # An image problem must not cost the day its post: fall back to text only.
        try:
            payload["media"] = {"media_ids": [upload_image(image_path, image_alt)]}
        except (PostError, OSError) as e:
            print("         [warn] X image skipped, posting text only: %s" % e)
    if reply_to:
        payload["reply"] = {"in_reply_to_tweet_id": str(reply_to)}

    if dry_run:
        _creds()  # still validate configuration in a dry run
        return "dry-run-%s" % uuid.uuid4().hex[:12]

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=body, method="POST")
    req.add_header("Authorization", _auth_header("POST", ENDPOINT))
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "honorbrook-social/1.0")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:600]
        if e.code == 429:
            raise PostError(
                "rate limited by X (HTTP 429). The free tier allows roughly "
                "500 posts/month and 17 per 24h. Detail: %s" % detail
            )
        if e.code in (401, 403):
            raise PostError(
                "X rejected the credentials (HTTP %d). Check that the app has "
                "Read and Write permission and that the access token was "
                "regenerated AFTER enabling write. Detail: %s" % (e.code, detail)
            )
        raise PostError("X API HTTP %d: %s" % (e.code, detail))
    except urllib.error.URLError as e:
        raise PostError("network error talking to X: %s" % e)

    return data.get("data", {}).get("id", "unknown")
