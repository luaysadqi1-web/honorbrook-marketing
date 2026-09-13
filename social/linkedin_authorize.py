#!/usr/bin/env python3
"""
One-time LinkedIn authorization helper.

Mirrors gbp_authorize.py: opens LinkedIn's consent screen, catches the redirect
on localhost, trades the code for an access token (and a refresh token if your
app is approved for them), verifies the token can actually administer the
company page, and writes the results straight into .env.

Prerequisite: LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET already in .env,
and the redirect URL this script prints must be registered on the app under
Auth -> Authorized redirect URLs.

    python3 linkedin_authorize.py

LinkedIn access tokens last 60 days. Refresh tokens last 365 and are only
issued to apps approved for programmatic refresh -- if you get one, the poster
will renew itself and this channel stops going dark.
"""

import json
import os
import socket
import sys
import urllib.parse
import urllib.request
import urllib.error
import uuid
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lib import store            # noqa: E402
from lib import linkedin_client  # noqa: E402

AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
ACLS_URL = ("https://api.linkedin.com/rest/organizationAcls"
            "?q=roleAssignee&role=ADMINISTRATOR&state=APPROVED")

# w_organization_social  -> post as the company page
# r_organization_social  -> read those posts back
# rw_organization_admin  -> confirm this member administers the page
SCOPE = "w_organization_social r_organization_social rw_organization_admin"

# LinkedIn matches the redirect URL exactly, including the port, so this is
# fixed rather than an ephemeral port like the Google helper uses.
PORT = 8723
REDIRECT = "http://localhost:%d/callback" % PORT

_result = {}


class Catcher(BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        _result["code"] = q.get("code", [None])[0]
        _result["state"] = q.get("state", [None])[0]
        _result["error"] = q.get("error_description", q.get("error", [None]))[0]
        ok = _result["code"] is not None
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            ("<html><body style='font-family:system-ui;padding:3rem'>"
             "<h2>%s</h2><p>%s</p></body></html>"
             % ("Authorized." if ok else "Authorization failed.",
                "You can close this tab and return to the terminal."
                if ok else "Error: %s" % _result.get("error"))).encode()
        )

    def log_message(self, *a):
        pass


def port_free(port):
    s = socket.socket()
    try:
        s.bind(("127.0.0.1", port))
        return True
    except OSError:
        return False
    finally:
        s.close()


def exchange(code, client_id, client_secret):
    body = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT,
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def admin_orgs(token):
    req = urllib.request.Request(ACLS_URL, method="GET")
    req.add_header("Authorization", "Bearer %s" % token)
    req.add_header("X-Restli-Protocol-Version", "2.0.0")
    req.add_header("LinkedIn-Version", linkedin_client.API_VERSION)
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())
    return [str(el.get("organization", "")).rsplit(":", 1)[-1]
            for el in data.get("elements", [])]


def main():
    store.load_dotenv()
    cid = os.environ.get("LINKEDIN_CLIENT_ID", "").strip()
    secret = os.environ.get("LINKEDIN_CLIENT_SECRET", "").strip()
    org = os.environ.get("LINKEDIN_ORG_ID", "").strip()

    if not cid or not secret:
        print("Missing LINKEDIN_CLIENT_ID / LINKEDIN_CLIENT_SECRET in .env.")
        print("Get them from your app at linkedin.com/developers/apps -> Auth.")
        return 1

    print("Redirect URL this script uses:\n    %s" % REDIRECT)
    print("It must be registered on the app under Auth -> Authorized redirect URLs,")
    print("character for character, or LinkedIn will reject the consent request.\n")

    if not port_free(PORT):
        print("Port %d is already in use. Free it and retry." % PORT)
        return 1

    state = uuid.uuid4().hex
    url = AUTH_URL + "?" + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": cid,
        "redirect_uri": REDIRECT,
        "state": state,
        "scope": SCOPE,
    })

    srv = HTTPServer(("127.0.0.1", PORT), Catcher)
    print("Opening LinkedIn consent in your browser...")
    print("If it does not open, paste this:\n    %s\n" % url)
    webbrowser.open(url)
    srv.handle_request()
    srv.server_close()

    if not _result.get("code"):
        print("No authorization code returned. Error: %s" % _result.get("error"))
        return 1
    if _result.get("state") != state:
        print("State mismatch -- aborting rather than trusting this response.")
        return 1

    try:
        tok = exchange(_result["code"], cid, secret)
    except urllib.error.HTTPError as e:
        print("Token exchange failed: HTTP %d %s"
              % (e.code, e.read().decode("utf-8", "replace")[:400]))
        return 1

    access = (tok.get("access_token") or "").strip()
    refresh = (tok.get("refresh_token") or "").strip()
    if not access:
        print("No access_token in response: %s" % tok)
        return 1

    linkedin_client._persist_env("LINKEDIN_ACCESS_TOKEN", access)
    print("\nWrote LINKEDIN_ACCESS_TOKEN to .env (expires in ~%s days)."
          % (int(tok.get("expires_in", 0)) // 86400 or "60"))

    if refresh:
        linkedin_client._persist_env("LINKEDIN_REFRESH_TOKEN", refresh)
        print("Wrote LINKEDIN_REFRESH_TOKEN to .env. The poster will now renew")
        print("itself, so this channel will not go dark after 60 days.")
    else:
        print("\nNo refresh token issued -- your app is not approved for")
        print("programmatic refresh. The access token dies in ~60 days and you")
        print("will need to run this script again. Request programmatic refresh")
        print("token access on the app to avoid that.")

    # Prove the token can actually administer the page before declaring success.
    try:
        orgs = admin_orgs(access)
    except urllib.error.HTTPError as e:
        print("\nToken saved, but the admin check failed: HTTP %d %s"
              % (e.code, e.read().decode("utf-8", "replace")[:300]))
        print("Run: python3 preflight.py --linkedin")
        return 1

    if org and org in orgs:
        print("\nVerified: this token administers org %s. LinkedIn is ready." % org)
    elif orgs:
        print("\nToken works, but LINKEDIN_ORG_ID=%s is not in its admin list %s."
              % (org or "(unset)", orgs))
        print("Set LINKEDIN_ORG_ID to one of those ids.")
        return 1
    else:
        print("\nToken works but administers no organizations. The signed-in")
        print("member must be an admin of the company page.")
        return 1

    print("\nNext: python3 preflight.py --linkedin")
    return 0


if __name__ == "__main__":
    sys.exit(main())
