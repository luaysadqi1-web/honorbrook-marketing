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
