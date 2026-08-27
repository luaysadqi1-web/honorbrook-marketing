# Getting the API keys

You do this part — I never handle credentials. Both platforms take about
20 minutes each. Paste results into `social/.env` (copy `.env.example` first).

Nothing else in the system needs to change once these are filled in; the poster
picks them up on its next run automatically.

---

## X (Twitter) — required for daily posting

1. Go to **developer.x.com** and sign in as the Honorbrook account.
2. Sign up for the **Free** tier. It allows ~500 posts/month and 17 per 24h —
   the routine uses 1/day, so Free is genuinely enough.
3. Create a Project, then an App inside it.
4. **Before generating any token:** open the App → *User authentication settings*
   → set **App permissions: Read and Write** → App type: *Web App / Automated
   App or Bot* → save. Callback URL can be `https://honorbrook-insurance.com`.
   > This order matters. A token generated while the app was read-only will
   > return HTTP 403 forever until you regenerate it.
5. Go to *Keys and tokens* and copy four values into `.env`:
   - API Key → `X_API_KEY`
   - API Key Secret → `X_API_SECRET`
   - Access Token → `X_ACCESS_TOKEN`
   - Access Token Secret → `X_ACCESS_TOKEN_SECRET`
6. Verify: `python3 run_daily.py --date <a queued date> --dry-run`
   The "not configured" error should be gone.

---

## LinkedIn — harder, and honestly optional at first

LinkedIn company-page posting requires an app approved for the **Community
Management API**. Approval is a review process, not instant, and Microsoft
rejects vague use cases.

1. **linkedin.com/developers** → Create app. Associate it with the Honorbrook
   Insurance company page (you must be a page admin).
2. Verify the app via the page (LinkedIn generates a verification link).
3. Products tab → request **Community Management API**. In the use-case box,
   describe it concretely: *"Publishing our own licensed insurance agency's
   educational content to our own company page on a daily schedule."*
4. Once approved, run the OAuth2 authorization-code flow with scope
   `w_organization_social` and copy the access token to
   `LINKEDIN_ACCESS_TOKEN`.
5. `LINKEDIN_ORG_ID` is the number in `linkedin.com/company/<id>/admin/`.

**Token expiry:** LinkedIn access tokens last ~60 days. Set a calendar reminder,
or the LinkedIn half goes quiet. The X half is unaffected — the poster treats
each platform independently, so a dead LinkedIn token never blocks an X post.

**If approval stalls:** leave `LINKEDIN_*` blank. Those items stay `pending` in
the queue with a "not configured" note and cost you nothing. X keeps posting.

---

## Google Business Profile — the one worth doing first

Highest value of the three for a local agency: GBP posts feed the local pack,
which is where "medicare agent near me" actually converts. It is also the most
gated — Google reviews an access request before the posting API works.

The refresh token does **not** expire, so unlike LinkedIn this is set up once.

### 1. Cloud project

1. **console.cloud.google.com** → create a project, e.g. `honorbrook-social`.
2. Note the **project number** and **project ID** — the access request needs both.

### 2. Request API access (do this early, it is the long pole)

1. Go to the **Google Business Profile APIs access request form** (linked from
   `developers.google.com/my-business/content/prereqs`).
2. Fill it in as the business owner. Use the real agency details — NPN 21370662,
   the Tysons address, honorbrook-insurance.com.
3. Use case, stated concretely: *"Publishing our own licensed insurance agency's
   educational posts to our own verified Business Profile on a daily schedule."*
4. Approval typically takes days, sometimes longer. Continue with the steps
   below meanwhile — everything else can be ready and waiting.

### 3. OAuth consent screen

1. APIs & Services → **OAuth consent screen** → External.
2. Add the scope `https://www.googleapis.com/auth/business.manage`.
3. **Publish the app.** Leave it in *Testing* and your refresh token silently
   expires after 7 days, which will look like a random failure weeks later.

### 4. OAuth client

APIs & Services → Credentials → Create credentials → **OAuth client ID** →
*Web application*. Leave the redirect URIs empty for now; the helper script
prints the exact one to add.

Put the client id and secret into `.env` as `GBP_CLIENT_ID` / `GBP_CLIENT_SECRET`.

### 5. Authorize — the script does the rest

```bash
python3 gbp_authorize.py
```

It prints a redirect URI to paste into your OAuth client, opens Google's consent
screen, catches the response, and prints your `GBP_REFRESH_TOKEN`,
`GBP_ACCOUNT_ID` and `GBP_LOCATION_ID` ready to paste into `.env`.

If the account/location lookup returns 403, access is not approved yet. **Save
the refresh token anyway** and re-run the script once approval lands — it will
fetch the ids without re-authorizing.

### 6. Verify

```bash
python3 run_daily.py --date <a queued date> --dry-run
```

### Gotchas

- The Google account you authorize with must be an **owner or manager** of the
  Honorbrook location.
- Local posts live on the legacy My Business **v4** surface. The newer v1 APIs
  do not cover posts — that is expected, not a mistake.
- GBP posts use a **CALL** button by default, which uses the phone number
  already on the profile. No URL needed.
