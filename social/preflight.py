#!/usr/bin/env python3
"""
Credential doctor for the Honorbrook social poster.

Run this after filling in .env. It reports what is set, then makes ONE
read-only live call per channel to prove the credentials actually work --
before a scheduled run tries to publish with them.

It never prints a secret. Values are shown only as a length and a short
fingerprint, so the output is safe to paste into a chat or a ticket.

    python3 preflight.py            # check everything
    python3 preflight.py --x        # just X
    python3 preflight.py --linkedin # just LinkedIn
    python3 preflight.py --gbp      # just Google Business Profile

Exit code 0 = every enabled channel is ready. 1 = at least one is not.
Stdlib only, so it runs against system Python exactly like run_daily.py.
"""

import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import store  # noqa: E402
from lib import linkedin_client  # noqa: E402
from lib import x_client  # noqa: E402

GREEN, RED, YELLOW, DIM, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"
OK, BAD, WARN = GREEN + "OK  " + RESET, RED + "FAIL" + RESET, YELLOW + "WARN" + RESET

PLACEHOLDER_HINTS = ("your", "xxx", "replace", "paste", "here", "placeholder", "changeme")


def fingerprint(val):
    """Length plus a short hash. Enough to tell two values apart, useless to steal."""
    return "len=%d sha=%s" % (len(val), hashlib.sha256(val.encode()).hexdigest()[:8])


def check_vars(names):
    """Returns (all_present, list of (name, status, note))."""
    rows, ok = [], True
    for n in names:
        v = os.environ.get(n, "").strip()
        if not v:
            rows.append((n, "EMPTY", ""))
            ok = False
        elif any(h in v.lower() for h in PLACEHOLDER_HINTS):
            rows.append((n, "PLACEHOLDER", v[:12] + "..."))
            ok = False
        else:
            rows.append((n, "set", fingerprint(v)))
    return ok, rows


def render(title, ok, rows, verdict, advice=""):
    print("\n%s%s%s" % ("\033[1m", title, RESET))
    for name, status, note in rows:
        mark = OK if status == "set" else BAD
        print("  %s %-26s %s%s%s" % (mark, name, DIM, note or status, RESET))
    print("  %s %s" % (OK if ok else BAD, verdict))
    if advice:
        for line in advice.strip().splitlines():
            print("       %s%s%s" % (DIM, line.strip(), RESET))


# ----------------------------------------------------------------- X --------
def check_x():
    names = ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET")
    present, rows = check_vars(names)
    if not present:
        render("X (Twitter)", False, rows, "not configured -- nothing to test",
               """Create an app at developer.x.com. Set the app's User authentication
                  settings to Read and Write BEFORE generating the access token: a
                  token minted while the app was read-only stays read-only forever
                  and returns 403 on every post. Regenerate the token after the
                  permission change if you are unsure.""")
        return False

    # Read-only identity call, signed the same way a post would be. If this
    # passes, the signature and the credentials are both good.
    url = "https://api.x.com/2/users/me"
    req = urllib.request.Request(url, method="GET")
    try:
        req.add_header("Authorization", x_client._auth_header("GET", url))
    except x_client.NotConfigured as e:
        render("X (Twitter)", False, rows, "config error: %s" % e)
        return False
    req.add_header("User-Agent", "honorbrook-social/1.0")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        handle = data.get("data", {}).get("username", "?")
        render("X (Twitter)", True, rows, "authenticated as @%s" % handle,
               "Write permission is not proven by this read call. The first real "
               "post will confirm it; a 403 there means the token predates the "
               "Read+Write switch.")
        return True
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:300]
        advice = ""
        if e.code in (401, 403):
            advice = ("Credentials rejected. Most common cause: the access token was "
                      "generated while the app was still Read-only. Fix the app "
                      "permission, then REGENERATE the access token and secret.")
        elif e.code == 429:
            advice = "Rate limited. Credentials are probably fine; retry later."
        render("X (Twitter)", False, rows, "live check failed: HTTP %d %s" % (e.code, detail), advice)
        return False
    except urllib.error.URLError as e:
        render("X (Twitter)", False, rows, "network error: %s" % e)
        return False


# ---------------------------------------------------------- LinkedIn --------
def check_linkedin():
    names = ("LINKEDIN_ACCESS_TOKEN", "LINKEDIN_ORG_ID")
    present, rows = check_vars(names)
    _, refresh_rows = check_vars(
        ("LINKEDIN_REFRESH_TOKEN", "LINKEDIN_CLIENT_ID", "LINKEDIN_CLIENT_SECRET")
    )
    rows = rows + refresh_rows

    if not present:
        render("LinkedIn", False, rows, "not configured -- nothing to test",
               """Needs an app approved for the Community Management API with the
                  w_organization_social scope, and the signed-in member must be an
                  admin of the company page. LINKEDIN_ORG_ID is the numeric id in
                  your page's admin URL.""")
        return False

    org = os.environ["LINKEDIN_ORG_ID"].strip()
    token = os.environ["LINKEDIN_ACCESS_TOKEN"].strip()
    url = ("https://api.linkedin.com/rest/organizationAcls"
           "?q=roleAssignee&role=ADMINISTRATOR&state=APPROVED")
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", "Bearer %s" % token)
    req.add_header("X-Restli-Protocol-Version", "2.0.0")
    req.add_header("LinkedIn-Version", linkedin_client.API_VERSION)
    req.add_header("User-Agent", "honorbrook-social/1.0")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        admin_orgs = [
            str(el.get("organization", "")).rsplit(":", 1)[-1]
            for el in data.get("elements", [])
        ]
        if org in admin_orgs:
            note = "token valid, and it administers org %s" % org
            good = True
        else:
            note = ("token valid, but org %s is NOT in this member's admin list %s"
                    % (org, admin_orgs or "[]"))
            good = False
        extra = ""
        if not linkedin_client.can_refresh():
            extra = ("No refresh credentials set. LinkedIn access tokens expire after "
                     "60 days, so this channel will go dark again around then. Add "
                     "LINKEDIN_REFRESH_TOKEN, LINKEDIN_CLIENT_ID and "
                     "LINKEDIN_CLIENT_SECRET to make it self-heal.")
        render("LinkedIn", good, rows,
               "%s (API version %s)" % (note, linkedin_client.API_VERSION), extra)
        return good
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:300]
        advice = ""
        if e.code == 401:
            advice = ("Token expired or invalid. Tokens last 60 days. If refresh "
                      "credentials are set, run: python3 -c "
                      "\"import sys;sys.path.insert(0,'.');from lib import store,"
                      "linkedin_client as l;store.load_dotenv();"
                      "print(l.refresh_access_token()[:6]+'...')\"")
        elif e.code == 403:
            advice = "App lacks w_organization_social, or the member is not a page admin."
        elif e.code == 426:
            advice = ("API version %s has been sunset. Bump API_VERSION in "
                      "lib/linkedin_client.py." % linkedin_client.API_VERSION)
        render("LinkedIn", False, rows, "live check failed: HTTP %d %s" % (e.code, detail), advice)
        return False
    except urllib.error.URLError as e:
        render("LinkedIn", False, rows, "network error: %s" % e)
        return False


# --------------------------------------------------------------- GBP --------
def check_gbp():
    names = ("GBP_CLIENT_ID", "GBP_CLIENT_SECRET", "GBP_REFRESH_TOKEN",
             "GBP_ACCOUNT_ID", "GBP_LOCATION_ID")
    present, rows = check_vars(names)
    if not present:
        render("Google Business Profile", False, rows,
               "not configured -- nothing to test",
               """Run gbp_authorize.py for the refresh token. Posting also needs
                  Google to approve a Business Profile API request against the Cloud
                  project, and the OAuth consent screen must be PUBLISHED or the
                  refresh token dies after 7 days.""")
        return False
    render("Google Business Profile", True, rows,
           "credentials present (no live check -- posting is the only write path)")
    return True


def main():
    store.load_dotenv()
    args = [a for a in sys.argv[1:] if a.startswith("--")]
    want = {a.lstrip("-") for a in args} or {"x", "linkedin", "gbp"}

    print("\033[1mHonorbrook social -- credential preflight\033[0m")
    print("%s.env: %s%s" % (DIM, linkedin_client.ENV_PATH, RESET))
    print("%sNo secret values are printed. Fingerprints only.%s" % (DIM, RESET))

    results = {}
    if "x" in want:
        results["X"] = check_x()
    if "linkedin" in want:
        results["LinkedIn"] = check_linkedin()
    if "gbp" in want:
        results["GBP"] = check_gbp()

    ready = [k for k, v in results.items() if v]
    blocked = [k for k, v in results.items() if not v]
    print("\n\033[1mSummary\033[0m")
    print("  ready:   %s" % (", ".join(ready) or "none"))
    print("  blocked: %s" % (", ".join(blocked) or "none"))
    return 0 if not blocked else 1


if __name__ == "__main__":
    sys.exit(main())
