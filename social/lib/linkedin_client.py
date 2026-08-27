"""
LinkedIn Posts API client -- stdlib only.

Posts to the Honorbrook Insurance COMPANY PAGE (not a personal profile), which
requires an app approved for the Community Management API with the
w_organization_social scope.

Required environment variables:
    LINKEDIN_ACCESS_TOKEN   OAuth2 access token (expires ~60 days -- see
                            SETUP-API-KEYS.md for the refresh routine)
    LINKEDIN_ORG_ID         numeric company page id, e.g. 12345678
"""

import json
import os
import urllib.request
import urllib.error
import uuid

ENDPOINT = "https://api.linkedin.com/rest/posts"
# LinkedIn requires an explicit API version header in YYYYMM form.
API_VERSION = "202508"


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


def post(text, dry_run=False):
    """Publish one company-page post. Returns the post URN."""
    token, org = _creds()

    if dry_run:
        return "dry-run-urn:li:share:%s" % uuid.uuid4().hex[:12]

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

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            # The created post URN comes back in a header, not the body.
            urn = resp.headers.get("x-restli-id") or resp.headers.get("X-RestLi-Id")
            return urn or "posted"
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:600]
        if e.code == 401:
            raise PostError(
                "LinkedIn token rejected (401). Access tokens expire after "
                "about 60 days -- refresh it. Detail: %s" % detail
            )
        if e.code == 403:
            raise PostError(
                "LinkedIn denied the post (403). The app usually lacks "
                "w_organization_social, or this token's member is not an admin "
                "of org %s. Detail: %s" % (org, detail)
            )
        raise PostError("LinkedIn API HTTP %d: %s" % (e.code, detail))
    except urllib.error.URLError as e:
        raise PostError("network error talking to LinkedIn: %s" % e)
