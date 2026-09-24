#!/usr/bin/env python3
"""
One-time Meta setup: short-lived token in, working .env out.

What this saves you from: the token the Graph API Explorer hands you is a
SHORT-LIVED USER token that dies in about an hour. What the poster needs is a
PAGE token, and a Page token derived from a long-lived user token does not
expire at all. Getting from one to the other is three chained API calls that
are easy to get subtly wrong, so this does them.

    1. exchange short-lived user token  ->  long-lived user token (60 days)
    2. GET /me/accounts                 ->  the Page and its Page token
                                            (never expires, from a long-lived user token)
    3. GET /{page}/instagram_business_account -> META_IG_USER_ID

then writes META_PAGE_TOKEN and META_IG_USER_ID into .env and verifies them.

Prerequisites in .env:
    META_APP_ID       1604097144602651  (already set)
    META_APP_SECRET   App settings > Basic > App secret > Show

Then, at developers.facebook.com/tools/explorer with the Honorbrook Social
Posting app selected and the four permissions listed, click Generate Access
Token, authorise, and copy the token. Run this and paste it when asked.

    python3 meta_setup.py

The token is read with getpass, so it is not echoed to your terminal and does
not land in your shell history.
"""

import getpass
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lib import store            # noqa: E402
from lib import meta_client      # noqa: E402
# Reuse the atomic .env writer already proven by the LinkedIn helper rather
# than writing a second one that could truncate the file on a crash.
from lib.linkedin_client import _persist_env  # noqa: E402

GRAPH = "https://graph.facebook.com/v21.0"
PAGE_ID_DEFAULT = "520470514472094"   # Honorbrook Insurance


def get(path, params):
    url = "%s/%s?%s" % (GRAPH, path.lstrip("/"), urllib.parse.urlencode(params))
    req = urllib.request.Request(url, method="GET")
    req.add_header("User-Agent", "honorbrook-social/1.0")
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            msg = json.loads(raw)["error"]["message"]
        except Exception:
            msg = raw[:300]
        raise SystemExit("  Meta said: %s" % msg)


def main():
    store.load_dotenv()
    app_id = os.environ.get("META_APP_ID", "").strip()
    secret = os.environ.get("META_APP_SECRET", "").strip()
    page_id = os.environ.get("META_PAGE_ID", "").strip() or PAGE_ID_DEFAULT

    if not app_id or not secret:
        print("Missing META_APP_ID / META_APP_SECRET in .env.")
        print("App secret: developers.facebook.com > your app >")
        print("            App settings > Basic > App secret > Show")
        return 1

    print("App %s, Page %s" % (app_id, page_id))
    print("Paste the token from the Graph API Explorer (input is hidden):")
    short = getpass.getpass("  token: ").strip()
    if not short:
        print("Nothing pasted.")
        return 1

    print("\n1/3  exchanging for a long-lived user token...")
    ex = get("oauth/access_token", {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": secret,
        "fb_exchange_token": short,
    })
    long_user = ex.get("access_token", "")
    if not long_user:
        print("     no access_token came back: %s" % ex)
        return 1
    days = int(ex.get("expires_in", 0)) // 86400
    print("     ok (user token good for ~%d days)" % days)

    print("2/3  finding the Page token...")
    accts = get("me/accounts", {"access_token": long_user, "limit": "100"})
    pages = accts.get("data", [])
    if not pages:
        print("     this account administers no Pages. Is the right profile signed in?")
        return 1
    match = next((p for p in pages if str(p.get("id")) == page_id), None)
    if not match:
        print("     Page %s is not in this account's list. Found:" % page_id)
        for p in pages:
            print("       %s  %s" % (p.get("id"), p.get("name")))
        return 1
    page_token = match.get("access_token", "")
    if not page_token:
        print("     no Page token returned. The token is probably missing "
              "pages_show_list or pages_read_engagement.")
        return 1
    print("     ok (%s)" % match.get("name"))

    print("3/3  looking up the Instagram Business account...")
    ig_id = ""
    ig = get(page_id, {"access_token": page_token,
                       "fields": "instagram_business_account{id,username}"})
    node = ig.get("instagram_business_account") or {}
    ig_id = str(node.get("id", "") or "")
    if ig_id:
        print("     ok (@%s, id %s)" % (node.get("username", "?"), ig_id))
    else:
        print("     none linked. Facebook will work; Instagram will not until the")
        print("     IG account is switched to Business/Creator and linked to the Page.")

    _persist_env("META_PAGE_TOKEN", page_token)
    if ig_id:
        _persist_env("META_IG_USER_ID", ig_id)
    print("\nwrote META_PAGE_TOKEN%s to .env"
          % (" and META_IG_USER_ID" if ig_id else ""))
    print("Page tokens derived from a long-lived user token do not expire, so this")
    print("is a one-time step unless the password or app permissions change.\n")

    os.environ["META_PAGE_TOKEN"] = page_token
    if ig_id:
        os.environ["META_IG_USER_ID"] = ig_id
    try:
        who = meta_client.verify()
        for k, v in who.items():
            print("  verified %-10s %s" % (k + ":", v))
    except Exception as e:
        print("  saved, but verification failed: %s" % str(e)[:200])
        return 1
    print("\nNext: python3 preflight.py --meta")
    return 0


if __name__ == "__main__":
    sys.exit(main())
