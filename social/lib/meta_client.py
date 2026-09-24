"""
Meta (Facebook Page + Instagram) publishing client -- stdlib only.

Replaces Metricool for Facebook and Instagram. The Graph API is free and has
no monthly post cap, which is what stranded 13 posts in September.

Required environment variables:
    META_PAGE_ID        numeric Facebook Page id
    META_PAGE_TOKEN     Page access token with pages_manage_posts
                        and pages_read_engagement
    META_IG_USER_ID     Instagram Business account id linked to that Page
                        (only needed for Instagram)

The two networks do NOT work the same way, and the difference drives the design:

  Facebook schedules natively. POST /{page-id}/photos with the image `url`,
  `published=false` and `scheduled_publish_time` hands the post to Meta and we
  are done. Meta enforces 10 minutes to 30 days out.

  Instagram has no scheduling. There is no scheduled_publish_time on the
  Content Publishing API. Publishing is two calls -- create a container from an
  image_url, then publish that container -- and an unpublished container
  expires after 24 hours, so containers cannot be built days ahead. Every
  "schedule to Instagram" feature in every tool is really a job queue that
  fires at the minute. Here that queue is run_daily.py under launchd: the item
  sits in queue/YYYY-MM-DD.json until its day, then this module publishes it.

Images are passed by public URL, so the graphics already committed to
social-assets/2026-q4/ work directly with no upload step.
"""

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

GRAPH = "https://graph.facebook.com/v21.0"

# Meta's own bounds on scheduled_publish_time, enforced server-side.
MIN_LEAD_SECONDS = 10 * 60
MAX_LEAD_SECONDS = 30 * 24 * 3600

# Instagram container processing. Images finish in a second or two; this is
# generous so a slow fetch of our own CDN does not fail a post.
IG_POLL_ATTEMPTS = 20
IG_POLL_SECONDS = 3


class NotConfigured(Exception):
    pass


class PostError(Exception):
    pass


def _require(*names):
    vals = [os.environ.get(n, "").strip() for n in names]
    missing = [n for n, v in zip(names, vals) if not v]
    if missing:
        raise NotConfigured("missing env vars: %s" % ", ".join(missing))
    return vals


def can_post_facebook():
    return all(os.environ.get(n, "").strip() for n in ("META_PAGE_ID", "META_PAGE_TOKEN"))


def can_post_instagram():
    return all(os.environ.get(n, "").strip()
               for n in ("META_IG_USER_ID", "META_PAGE_TOKEN"))


def _call(path, params, method="POST"):
    url = "%s/%s" % (GRAPH, path.lstrip("/"))
    body = urllib.parse.urlencode(params).encode("utf-8")
    if method == "GET":
        url = "%s?%s" % (url, urllib.parse.urlencode(params))
        req = urllib.request.Request(url, method="GET")
    else:
        req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("User-Agent", "honorbrook-social/1.0")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            err = json.loads(raw).get("error", {})
        except ValueError:
            err = {}
        raise PostError(_explain(e.code, err, raw))
    except urllib.error.URLError as e:
        raise PostError("network error talking to Meta: %s" % e)


def _explain(http_code, err, raw):
    """Turn Meta's error codes into something actionable at 9am."""
    code = err.get("code")
    sub = err.get("error_subcode")
    msg = err.get("message", raw[:300])
    if code == 190 or http_code == 401:
        return ("Meta rejected the token (code 190). Page access tokens die when "
                "the password changes, the app permissions change, or a short-lived "
                "token was used. Re-issue a long-lived Page token. Detail: %s" % msg)
    if code == 200 or code == 10 or http_code == 403:
        return ("Meta denied the action (code %s). The token is usually missing "
                "pages_manage_posts, or for Instagram the account is not a "
                "Business/Creator account linked to this Page. Detail: %s" % (code, msg))
    if code == 4 or code == 17 or code == 32 or sub == 2207051:
        return ("Meta rate limit hit (code %s). Instagram allows 25 API-published "
                "posts per rolling 24 hours. The item stays queued and will retry. "
                "Detail: %s" % (code, msg))
    if code == 100:
        return ("Meta rejected a parameter (code 100). Most often the image URL is "
                "not publicly reachable, or scheduled_publish_time is outside the "
                "10-minute-to-30-day window. Detail: %s" % msg)
    if sub == 2207052 or "media" in str(msg).lower() and "fetch" in str(msg).lower():
        return ("Meta could not fetch the image. Confirm the URL returns 200 with an "
                "image content-type and no redirect to a login page. Detail: %s" % msg)
    return "Meta API HTTP %d (code %s): %s" % (http_code, code, msg)


# --------------------------------------------------------------- Facebook ---
def post_facebook(text, image_url, when_epoch=None, dry_run=False):
    """Publish or schedule one Facebook Page photo post.

    when_epoch: unix seconds to schedule for, or None to publish now.
    Returns the post/photo id.
    """
    page_id, token = _require("META_PAGE_ID", "META_PAGE_TOKEN")
    if not image_url:
        raise PostError("Facebook photo post requires an image URL.")

    params = {"access_token": token, "url": image_url, "caption": text}
    if when_epoch is not None:
        lead = int(when_epoch) - int(time.time())
        if lead < MIN_LEAD_SECONDS:
            raise PostError(
                "scheduled_publish_time is only %d seconds out; Meta requires at "
                "least 10 minutes. Publish now instead, or pick a later slot." % lead)
        if lead > MAX_LEAD_SECONDS:
            raise PostError(
                "scheduled_publish_time is %d days out; Meta allows at most 30. "
                "Hold it in the queue and schedule closer to the date." % (lead // 86400))
        params["published"] = "false"
        params["scheduled_publish_time"] = str(int(when_epoch))

    if dry_run:
        return "dry-run-fb-%s" % (int(when_epoch) if when_epoch else "now")
    data = _call("%s/photos" % page_id, params)
    return data.get("post_id") or data.get("id", "unknown")


# -------------------------------------------------------------- Instagram ---
def post_instagram(text, image_url, dry_run=False):
    """Publish one Instagram image post, now.

    There is no scheduling on this API. Call this at the moment the post should
    go out -- run_daily.py under launchd is what provides that timing.
    """
    ig_id, token = _require("META_IG_USER_ID", "META_PAGE_TOKEN")
    if not image_url:
        raise PostError("Instagram requires an image; text-only posts are not possible.")

    if dry_run:
        return "dry-run-ig"

    created = _call("%s/media" % ig_id,
                    {"access_token": token, "image_url": image_url, "caption": text})
    container = created.get("id")
    if not container:
        raise PostError("Meta returned no container id: %s" % created)

    # The container is built asynchronously. Publishing before it reports
    # FINISHED fails, so poll rather than sleeping a fixed amount.
    for _ in range(IG_POLL_ATTEMPTS):
        st = _call(container, {"access_token": token, "fields": "status_code,status"},
                   method="GET")
        code = st.get("status_code")
        if code == "FINISHED":
            break
        if code == "ERROR":
            raise PostError("Instagram container failed to process: %s"
                            % st.get("status", st))
        time.sleep(IG_POLL_SECONDS)
    else:
        raise PostError(
            "Instagram container still processing after %d seconds. It stays valid "
            "for 24h, so the item is left queued to retry rather than lost."
            % (IG_POLL_ATTEMPTS * IG_POLL_SECONDS))

    published = _call("%s/media_publish" % ig_id,
                      {"access_token": token, "creation_id": container})
    return published.get("id", "unknown")


def verify():
    """Read-only check that the credentials actually work. Returns a dict."""
    out = {}
    if can_post_facebook():
        page_id, token = _require("META_PAGE_ID", "META_PAGE_TOKEN")
        d = _call(page_id, {"access_token": token, "fields": "name,username"}, method="GET")
        out["facebook"] = d.get("name", "?")
    if can_post_instagram():
        ig_id, token = _require("META_IG_USER_ID", "META_PAGE_TOKEN")
        # account_type is not a field on an IG Business node; username and
        # followers_count are, and they prove the link works.
        d = _call(ig_id, {"access_token": token,
                          "fields": "username,followers_count,media_count"}, method="GET")
        out["instagram"] = "@%s (%s followers, %s posts)" % (
            d.get("username", "?"), d.get("followers_count", "?"), d.get("media_count", "?"))
    return out
