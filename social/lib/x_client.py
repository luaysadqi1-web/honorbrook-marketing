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


def _auth_header(method, url):
    api_key, api_secret, token, token_secret = _creds()
    params = {
        "oauth_consumer_key": api_key,
        "oauth_nonce": uuid.uuid4().hex,
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_token": token,
        "oauth_version": "1.0",
    }
    params["oauth_signature"] = _sign(
        method, url, params, api_secret, token_secret
    )
    return "OAuth " + ", ".join(
        '%s="%s"' % (_quote(k), _quote(v)) for k, v in sorted(params.items())
    )


def post(text, reply_to=None, dry_run=False):
    """Publish one post. Returns the new post id, or a fake id on dry_run."""
    payload = {"text": text}
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
