"""
LinkedIn Posts API client -- stdlib only.

Posts to the Honorbrook Insurance COMPANY PAGE (not a personal profile), which
requires an app approved for the Community Management API with the
w_organization_social scope.

Required environment variables:
    LINKEDIN_ACCESS_TOKEN   OAuth2 access token. LinkedIn expires these after
                            60 days, which is how this channel went dark before.
    LINKEDIN_ORG_ID         numeric company page id, e.g. 12345678

Optional but strongly recommended -- without these the channel dies every
60 days and someone has to notice and re-auth by hand:
    LINKEDIN_REFRESH_TOKEN  valid 365 days, not extended by use
    LINKEDIN_CLIENT_ID      app client id
    LINKEDIN_CLIENT_SECRET  app client secret

When all three are present, a 401 triggers one automatic refresh, the new
access token is written back to .env, and the post is retried. Programmatic
refresh tokens are only issued to apps approved for them; if yours is not,
refresh returns a clear error instead of failing silently.
"""

import json
import os
import urllib.parse
import urllib.request
import urllib.error
import uuid

ENDPOINT = "https://api.linkedin.com/rest/posts"
OAUTH_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"

# LinkedIn requires an explicit API version header in YYYYMM form. Marketing
# API versions are supported for a minimum of one year and then sunset, so a
# stale value here fails every call. 202508 lapsed in Aug 2026; keep this
# within a year of today and bump it on the sunset schedule.
API_VERSION = "202608"

ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")


class NotConfigured(Exception):
    pass


class PostError(Exception):
    pass


def _creds():
    token = os.environ.get("LINKEDIN_ACCESS_TOKEN", "").strip()
    org = os.environ.get("LINKEDIN_ORG_ID", "").strip()
    missing = []
    if not token:
        missing.append("LINKEDIN_ACCESS_TOKEN")
    if not org:
        missing.append("LINKEDIN_ORG_ID")
    if missing:
        raise NotConfigured("missing env vars: %s" % ", ".join(missing))
    return token, org


def _refresh_creds():
    return (
        os.environ.get("LINKEDIN_REFRESH_TOKEN", "").strip(),
        os.environ.get("LINKEDIN_CLIENT_ID", "").strip(),
        os.environ.get("LINKEDIN_CLIENT_SECRET", "").strip(),
    )


def can_refresh():
    """True when the three refresh credentials are all present."""
    return all(_refresh_creds())


def _persist_env(key, value, path=None):
    """Rewrite one key in .env in place, preserving the file's 0600 mode.

    Written atomically so a crash mid-write cannot leave a truncated .env
    that would take every channel down, not just LinkedIn.
    """
    path = path or ENV_PATH
    if not os.path.exists(path):
        return False
    with open(path) as fh:
        lines = fh.readlines()
    out, found = [], False
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            k = stripped.partition("=")[0].strip()
            if k == key:
                out.append("%s=%s\n" % (key, value))
                found = True
                continue
        out.append(line)
    if not found:
        out.append("%s=%s\n" % (key, value))
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        fh.write("".join(out))
    os.chmod(tmp, 0o600)
    os.replace(tmp, path)
    return True


def refresh_access_token(persist=True):
    """Exchange the refresh token for a fresh 60-day access token."""
    refresh_token, client_id, client_secret = _refresh_creds()
    missing = [
        name
        for name, val in (
            ("LINKEDIN_REFRESH_TOKEN", refresh_token),
            ("LINKEDIN_CLIENT_ID", client_id),
            ("LINKEDIN_CLIENT_SECRET", client_secret),
        )
        if not val
    ]
    if missing:
        raise NotConfigured(
            "cannot refresh, missing: %s" % ", ".join(missing)
        )

    body = urllib.parse.urlencode(
        {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
        }
    ).encode("utf-8")
    req = urllib.request.Request(OAUTH_TOKEN_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("User-Agent", "honorbrook-social/1.0")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:600]
        raise PostError(
            "LinkedIn refresh failed (HTTP %d). Programmatic refresh tokens "
            "are only issued to approved apps; if yours is not approved you "
            "must re-run the consent flow by hand every 60 days. Detail: %s"
            % (e.code, detail)
        )
    except urllib.error.URLError as e:
        raise PostError("network error refreshing LinkedIn token: %s" % e)

    token = (data.get("access_token") or "").strip()
    if not token:
        raise PostError("LinkedIn refresh returned no access_token: %s" % data)

    os.environ["LINKEDIN_ACCESS_TOKEN"] = token
    # A rotated refresh token is returned only on some flows; keep it if so.
    new_refresh = (data.get("refresh_token") or "").strip()
    if persist:
        _persist_env("LINKEDIN_ACCESS_TOKEN", token)
        if new_refresh and new_refresh != refresh_token:
            os.environ["LINKEDIN_REFRESH_TOKEN"] = new_refresh
            _persist_env("LINKEDIN_REFRESH_TOKEN", new_refresh)
    return token


def _build_request(text, token, org):
    payload = {
        "author": "urn:li:organization:%s" % org,
        "commentary": text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    req = urllib.request.Request(
        ENDPOINT, data=json.dumps(payload).encode("utf-8"), method="POST"
    )
    req.add_header("Authorization", "Bearer %s" % token)
    req.add_header("Content-Type", "application/json")
    req.add_header("X-Restli-Protocol-Version", "2.0.0")
    req.add_header("LinkedIn-Version", API_VERSION)
    req.add_header("User-Agent", "honorbrook-social/1.0")
    return req


def post(text, dry_run=False, _retried=False):
    """Publish one company-page post. Returns the post URN."""
    token, org = _creds()

    if dry_run:
        return "dry-run-urn:li:share:%s" % uuid.uuid4().hex[:12]

    try:
        with urllib.request.urlopen(_build_request(text, token, org), timeout=30) as resp:
            # The created post URN comes back in a header, not the body.
            urn = resp.headers.get("x-restli-id") or resp.headers.get("X-RestLi-Id")
            return urn or "posted"
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:600]
        if e.code == 401:
            # Expired 60-day token. Refresh once and retry rather than going
            # dark until a human notices.
            if not _retried and can_refresh():
                refresh_access_token()
                return post(text, dry_run=False, _retried=True)
            raise PostError(
                "LinkedIn token rejected (401) and no refresh credentials are "
                "set. Access tokens expire after 60 days. Add "
                "LINKEDIN_REFRESH_TOKEN, LINKEDIN_CLIENT_ID and "
                "LINKEDIN_CLIENT_SECRET so this self-heals. Detail: %s" % detail
            )
        if e.code == 403:
            raise PostError(
                "LinkedIn denied the post (403). The app usually lacks "
                "w_organization_social, or this token's member is not an admin "
                "of org %s. Detail: %s" % (org, detail)
            )
        if e.code == 426 or "version" in detail.lower():
            raise PostError(
                "LinkedIn rejected API version %s (HTTP %d). Versions sunset "
                "about a year after release. Bump API_VERSION in "
                "lib/linkedin_client.py. Detail: %s"
                % (API_VERSION, e.code, detail)
            )
        raise PostError("LinkedIn API HTTP %d: %s" % (e.code, detail))
    except urllib.error.URLError as e:
        raise PostError("network error talking to LinkedIn: %s" % e)
