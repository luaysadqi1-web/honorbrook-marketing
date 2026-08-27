"""
Google Business Profile -- local post client. Stdlib only.

Publishes "What's new" posts to the Honorbrook location. For a local service
business this is the highest-value channel in the system: GBP posts feed the
local pack, which is where "medicare agent near me" actually converts.

Two things to know about this API:

  * Local posts still live on the legacy My Business v4 surface. The newer v1
    APIs (Business Information, Account Management) do not cover posts.
  * Access requires Google to approve an API access request against your Cloud
    project. Until that clears, calls return 403 PERMISSION_DENIED.

Auth is an OAuth2 refresh token, which -- unlike LinkedIn -- does not expire.
Set it up once and it keeps working until it is explicitly revoked.

Required environment variables:
    GBP_CLIENT_ID
    GBP_CLIENT_SECRET
    GBP_REFRESH_TOKEN
    GBP_ACCOUNT_ID     numeric, from accounts.list
    GBP_LOCATION_ID    numeric, from accounts.locations.list
"""

import json
import os
import urllib.parse
import urllib.request
import urllib.error
import uuid

TOKEN_URL = "https://oauth2.googleapis.com/token"
API_BASE = "https://mybusiness.googleapis.com/v4"

# Google truncates the post in the UI well before this, but the hard cap is
# 1500. Front-load the message -- roughly the first 150-250 characters are what
# people actually see before "Read more".
MAX_SUMMARY = 1500


class NotConfigured(Exception):
    pass


class PostError(Exception):
    pass


def _creds():
    keys = (
        "GBP_CLIENT_ID", "GBP_CLIENT_SECRET", "GBP_REFRESH_TOKEN",
        "GBP_ACCOUNT_ID", "GBP_LOCATION_ID",
    )
    vals = [os.environ.get(k, "").strip() for k in keys]
    missing = [k for k, v in zip(keys, vals) if not v]
    if missing:
        raise NotConfigured("missing env vars: %s" % ", ".join(missing))
    return vals


def _access_token(client_id, client_secret, refresh_token):
    """Trade the long-lived refresh token for a 1-hour access token."""
    body = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }).encode("utf-8")

    req = urllib.request.Request(TOKEN_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:400]
        raise PostError(
            "could not refresh the Google access token (HTTP %d). If this says "
            "invalid_grant, the refresh token was revoked or the OAuth consent "
            "screen is still in Testing mode (test-mode tokens expire after 7 "
            "days -- publish the app). Detail: %s" % (e.code, detail)
        )
    except urllib.error.URLError as e:
        raise PostError("network error refreshing Google token: %s" % e)

    token = data.get("access_token")
    if not token:
        raise PostError("no access_token in Google's response: %s" % data)
    return token


def post(text, cta="CALL", cta_url=None, dry_run=False):
    """Publish one local post. Returns the created post name."""
    client_id, client_secret, refresh_token, account, location = _creds()

    if len(text) > MAX_SUMMARY:
        raise PostError(
            "post is %d characters; Google allows %d" % (len(text), MAX_SUMMARY)
        )

    if dry_run:
        return "dry-run-localPost/%s" % uuid.uuid4().hex[:12]

    token = _access_token(client_id, client_secret, refresh_token)

    payload = {
        "languageCode": "en-US",
        "summary": text,
        "topicType": "STANDARD",
    }
    # CALL uses the phone number already on the profile and needs no URL.
    if cta == "CALL":
        payload["callToAction"] = {"actionType": "CALL"}
    elif cta:
        payload["callToAction"] = {
            "actionType": cta,
            "url": cta_url or "https://honorbrook-insurance.com",
        }

    url = "%s/accounts/%s/locations/%s/localPosts" % (API_BASE, account, location)
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), method="POST"
    )
    req.add_header("Authorization", "Bearer %s" % token)
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "honorbrook-social/1.0")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:600]
        if e.code == 403:
            raise PostError(
                "Google denied the post (403). Almost always one of: the "
                "Business Profile API access request has not been approved for "
                "this Cloud project yet, the My Business API is not enabled, or "
                "this Google account is not an owner/manager of the location. "
                "Detail: %s" % detail
            )
        if e.code == 404:
            raise PostError(
                "location not found (404). Check GBP_ACCOUNT_ID and "
                "GBP_LOCATION_ID are the bare numeric ids. Detail: %s" % detail
            )
        if e.code == 429:
            raise PostError("Google rate limited the request. Detail: %s" % detail)
        raise PostError("Google API HTTP %d: %s" % (e.code, detail))
    except urllib.error.URLError as e:
        raise PostError("network error talking to Google: %s" % e)

    return data.get("name", "posted")
