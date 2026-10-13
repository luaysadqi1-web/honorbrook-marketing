# Honorbrook — High-Converting Plan (SEO + GEO → calls → appointments)
Oct 12, 2026. Companion to `SEO-GEO-MASTER-PLAN.md` (architecture) and `_growth-plan-2026.md`. Built locally; nothing here is deployed until you say so (Netlify credits are low).

## 0. Deploy discipline (Netlify credits)
How deploys work here: every push to `main` that changes published files triggers a Netlify deploy. To spend as few as possible:
1. **Staging.** Unpublished posts live in `staging/blog/` (outside the publish folder). Currently 16 are staged, listed in `staging/manifest.json`.
2. **One command publishes a batch:** `python3 scripts/publish_staged.py --n 6` (or `--all`, or slugs). It moves the posts into `site/blog/`, stamps today's date, adds blog-index cards and sitemap entries, checks off the backlog, and refuses if a post links to a post that is not live. It does not run git.
3. **Then ONE push:** `git add site _blog-topics.md && git commit -m "blog: batch" && git push`, then `./scripts/indexnow.sh /blog/<slug> ... /blog/`.
4. **Ignore rule added to `netlify.toml`:** pushes that only touch `social/`, docs, `staging/` or `scripts/` no longer trigger a build (takes effect after the next push that includes `netlify.toml`).
5. **In the Netlify dashboard (you):** turn off Deploy Previews and Branch Deploys, and keep only `main` as the production branch. Check Billing to see what a deploy costs on your plan; I could not see your account.
6. **Cadence:** two batches a week (Mon, Thu), about 6 posts each = about 8 deploys a month for ~48 posts.
7. Rebuild a post after editing its source: `python3 scripts/blogbuild/build.py posts_5.py` (writes to `staging/blog/`). Post sources are in `scripts/blogbuild/`.

## 1. The funnel (what turns a reader into an appointment)
| Stage | What the visitor sees | Goal |
|---|---|---|
| Answer | Question-style post, direct answer in first 2 sentences | Earn the click and the AI citation |
| Proof | Founder byline with NPN, 11-state license line, reviews block | Trust |
| Offer | ONE offer per page type (below), not a generic "contact us" | Specific reason to call |
| Capture | Click-to-call (tracked), short form (name, phone, state, best time), chat | Lead |
| Follow-up | Call back within 5 minutes during business hours; text + email within the hour | Appointment |

**Offers by page type**
- Medicare / AEP posts → "Free plan check: we run your doctors and drugs" (call now during AEP).
- Under-65 / ACA / small business → "Free quote with your subsidy" / "Free group-vs-ICHRA cost comparison".
- Rollover / annuity / IUL → "Retirement Income Review" (educational, no pressure).
- Final expense → "Find out what you qualify for in 5 minutes".
- Kids / college → "Free needs check" (see compliance).

## 2. Conversion fixes (site, small edits)
1. Every post ends with the right offer (already: `.cta-strip` + closing `.band` with phone).
2. Form: add a "State" field and a "What do you need help with?" select so leads are routed by line and state. (Form posts to Formspree; confirm emails arrive.)
3. Tracking already exists in `assets/chat.js` (`phone_call_click`, `generate_lead`). Verify in GA4 DebugView that both fire, and mark them as key events.
4. Add the visible reviews block (26 Google reviews) to the homepage and state hubs. Do not add AggregateRating schema.
5. Speed to lead: set Formspree/Gmail notification to your phone; auto-reply email with your direct number.

## 3. Geo plan
- Done: 11 state hubs with areaServed schema, local SHIP section, restored titles.
- Next (needs your input): county pages for top 5 counties per state (Census data); state x line hubs (ACA first, Nov 1) only after verifying each state's facts and your appointments.
- Rule: no footer link-stuffing; counties link from the state hub only.

## 4. GEO (AI answers) checklist
Answer-first writing; FAQPage + BlogPosting schema (done on every post); citations to CMS/IRS/state DOI; `llms.txt` (written by the other session, uncommitted); identical entity facts everywhere; log AI citations monthly.

## 5. Content engine
- Published: 26 older + 20 new posts (live).
- Staged (this batch): 21 posts = 3 per day for 7 days, covering under-65/small business (5), high-income life/FIA (6), seniors/final expense (5), kids/college (5). Backlog is then empty; refill from People-Also-Ask, Reddit, and your own call/chat questions.
- **Dates are honest.** Posts carry the real publish date. Backdating is not used: Google can detect it, it is misleading, and it risks the whole site's trust.
- Release schedule once staged: 3/day through AEP is too heavy for one deploy each day. Instead release in two deploys per week (about 6 posts each) so Google still sees steady fresh content and credits last.

## 6. Weekly operating rhythm
Mon: deploy staged batch + GBP post. Daily: 15 min of call-backs and review requests. Thu: second deploy. Fri: check Search Console (queries, pages by state), GA4 key events, and the AI-citation log.

## 7. Scorecard
Calls, forms, chats, appointments set/held/closed by line and state; GSC impressions/clicks for question queries; GBP calls; reviews added.

## 8. Needs from you
Search Console export; confirm GA4 property for `G-J5YG8E3PYC`; Census API key (or OK to download ACS) for counties; which lines you are appointed for in each state (for state x line hubs); compliance sign-off on rollover/IUL/FIA copy.
