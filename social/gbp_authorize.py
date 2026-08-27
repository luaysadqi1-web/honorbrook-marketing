#!/usr/bin/env python3
"""
One-time Google Business Profile authorization helper.

Does the whole fiddly part for you: opens Google's consent screen, catches the
redirect on localhost, trades the code for a REFRESH TOKEN (which does not
expire), then looks up your account and location ids and prints the exact lines
to paste into .env.

Prerequisite: GBP_CLIENT_ID and GBP_CLIENT_SECRET already in .env.

    python3 gbp_authorize.py
"""

import json
import os
import socket
import sys
import urllib.parse
import urllib.request
import urllib.error
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
import store

SCOPE = "https://www.googleapis.com/auth/business.manage"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
ACCOUNTS_URL = "https://mybusinessaccountmanagement.googleapis.com/v1/accounts"
LOCATIONS_URL = (
    "https://mybusinessbusinessinformation.googleapis.com/v1/"
    "%s/locations?readMask=name,title,storefrontAddress"
)

_code = {}


class Catcher(BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        _code["code"] = q.get("code", [None])[0]
        _code["error"] = q.get("error", [None])[0]
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        ok = _code["code"] is not None
        self.wfile.write(
            ("<html><body style='font-family:system-ui;padding:3rem'>"
             "<h2>%s</h2><p>%s</p></body></html>"
             % ("Authorized." if ok else "Authorization failed.",
                "You can close this tab and return to the terminal."
                if ok else "Error: %s" % _code.get("error"))).encode()
        )

    def log_message(self, *a):
        pass


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def api_get(url, token):
    req = urllib.request.Request(url)
    req.add_header("Authorization", "Bearer %s" % token)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:400]
        print("\n  ! %s returned HTTP %d" % (url.split("?")[0], e.code))
        print("    %s" % detail)
        if e.code == 403:
            print("\n    A 403 here usually means the Business Profile API")
            print("    access request has not been approved yet, or the API is")
            print("    not enabled on this Cloud project. The refresh token")
            print("    above is still valid - save it and re-run this script")
            print("    later to fetch the ids.")
        return None


def main():
    store.load_dotenv()
    cid = os.environ.get("GBP_CLIENT_ID", "").strip()
    secret = os.environ.get("GBP_CLIENT_SECRET", "").strip()
    if not cid or not secret:
        print("Put GBP_CLIENT_ID and GBP_CLIENT_SECRET in .env first.")
        print("See SETUP-API-KEYS.md.")
        return 1

    port = free_port()
    redirect = "http://127.0.0.1:%d" % port
    params = {
        "client_id": cid,
        "redirect_uri": redirect,
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent",  # forces a refresh_token every time
    }
    url = AUTH_URL + "?" + urllib.parse.urlencode(params)

    print("\nAdd this EXACT redirect URI to your OAuth client in Google Cloud")
    print("Console (APIs & Services > Credentials > your client > Authorized")
    print("redirect URIs), then press Return:\n")
    print("    %s\n" % redirect)
    input("  [Return when added] ")

    print("\nOpening Google's consent screen in your browser...")
    webbrowser.open(url)
    print("If it did not open, paste this:\n\n%s\n" % url)

    srv = HTTPServer(("127.0.0.1", port), Catcher)
    srv.timeout = 300
    while "code" not in _code and "error" not in _code:
        srv.handle_request()

    if not _code.get("code"):
        print("\nAuthorization failed: %s" % _code.get("error"))
        return 1

    body = urllib.parse.urlencode({
        "code": _code["code"], "client_id": cid, "client_secret": secret,
        "redirect_uri": redirect, "grant_type": "authorization_code",
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            tok = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print("token exchange failed: %s" % e.read().decode("utf-8", "replace"))
        return 1

    refresh = tok.get("refresh_token")
    access = tok.get("access_token")
    if not refresh:
        print("\nGoogle did not return a refresh token. Revoke this app's access")
        print("at myaccount.google.com/permissions and run this again.")
        return 1

    print("\n" + "=" * 66)
    print("Paste these into .env:")
    print("=" * 66)
    print("GBP_REFRESH_TOKEN=%s" % refresh)

    accts = api_get(ACCOUNTS_URL, access)
    if accts:
        for a in accts.get("accounts", []):
            name = a.get("name", "")           # "accounts/1234567890"
            acct_id = name.split("/")[-1]
            print("GBP_ACCOUNT_ID=%s" % acct_id)
            print("#   account: %s (%s)"
                  % (a.get("accountName", "?"), a.get("type", "?")))
            locs = api_get(LOCATIONS_URL % name, access)
            for l in (locs or {}).get("locations", []):
                loc_id = l.get("name", "").split("/")[-1]
                print("GBP_LOCATION_ID=%s" % loc_id)
                print("#   location: %s" % l.get("title", "?"))
    print("=" * 66)
    print("\nThen verify:  python3 run_daily.py --date <queued date> --dry-run")
    return 0


if __name__ == "__main__":
    sys.exit(main())
