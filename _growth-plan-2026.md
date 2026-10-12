# Honorbrook Growth Plan — Geo-Targeted SEO + GEO → Calls & Qualified Appointments
Written Oct 12, 2026. Goal: calls and form fills that become appointments, in two lines of business.

## Business model (from Luay)
- **Volume engine:** Medicare Supplement + Medicare Advantage (seasonal; AEP Oct 15–Dec 7, MA-OEP Jan 1–Mar 31).
- **Profit engine:** life, IUL, large 401(k)/IRA rollovers into annuities, single-premium annuities for affluent clients.
- **Key insight:** Medicare clients and people turning 65 are the best pool for retirement-asset and life/IUL conversations. Every Medicare lead gets a "Retirement Income Review" offer. Medicare pays the bills now; wealth is the margin.
- Licensing: 11 states, multiple carrier appointments (confirmed by Luay). Assume insurance-only license: educational content only, no personalized investment advice, no guaranteed-return language.

## Phase 1 — Oct 12 → Dec 7 (AEP): get calls NOW
1. **Content:** 1 high-intent post/day (not 3: thin mass content risks a spam demotion and the site already lost traffic). Mix ≈ 2 Medicare : 1 wealth. Medicare posts answer AEP questions and end with a call CTA.
2. **Google Business Profile (biggest local lever):** 1 post/day-ish (reuse the blog), ask every client for a review, correct categories, Q&A, services. Tysons address is canonical.
3. **Conversion path:** phone number prominent, click-to-call tracked as a GA4 event, form-submit tracked, test the Formspree form lands in email, and confirm the chat widget captures phone numbers. A lead nobody measures can't be improved.
4. **Warm outreach (fastest cash):** every past client and open lead gets an AEP review call/text/email; ask for referrals. Use the existing prospecting bot/targets.
5. **Don't touch titles for 4–6 weeks** (state/homepage titles were restored Oct 12; let Google re-evaluate).

## Phase 2 — Geo architecture (hub and spoke)
- **Layer 1: state hubs** (done: 11 pages, areaServed schema, local SHIP section).
- **Layer 2: county pages**, target = top counties by median household income per state (need Census ACS data; pending). Launch **top 5 per state first** (55 pages), watch Search Console, then expand. Each page needs real data (county income and 65+ population, cited), own FAQ, state counseling program, links up to the state hub and across to the wealth pages. Two intents per county: "Medicare agent in {county}" and "retirement rollover / annuity help in {county}".
- Likely first-wave counties (seed list from general knowledge, MUST be confirmed against ACS before building): VA Loudoun, Fairfax, Arlington, Falls Church city, Alexandria; MD Howard, Montgomery, Anne Arundel, Calvert, Frederick; TX Collin, Fort Bend, Williamson, Denton, Montgomery; GA Forsyth, Fayette, Cobb, Oconee, Cherokee; NC Wake, Union, Cabarrus, Mecklenburg, Orange; SC York, Beaufort, Charleston, Lexington, Greenville; AL Shelby, Madison, Baldwin, Limestone, Jefferson; LA St. Tammany, Ascension, Lafayette, Livingston, East Baton Rouge; MI Oakland, Livingston, Washtenaw, Macomb, Kent; IN Hamilton, Boone, Hendricks, Johnson, Hancock; WV Putnam, Jefferson, Berkeley, Monongalia, Kanawha.
- No county links in the sitewide footer; link only from the state hub (avoids doorway-page pattern).

## Phase 3 — Wealth funnel (build in parallel, this month)
- New landing pages, each answering a real question and ending in a "Retirement Income Review" form: (1) What to do with a 401(k) when you retire/leave a job, (2) single-premium annuity / SPIA explained, (3) fixed indexed annuity explained, (4) IUL for high earners, (5) Medicare + retirement checkup for people turning 65.
- Lead magnet: "Retirement Rollover Checklist" (PDF) in exchange for name/email/phone → email follow-up + call.
- Referral partners (zero cost): CPAs, estate-planning attorneys, financial planners, HR managers in affluent counties. Outreach drafts live in OUTREACH-SEQUENCES.md.
- Compliance: no guarantees or returns, show caps/participation rates/surrender charges/fees, "not investment or tax advice", carrier-review of final copy.

## GEO (generative-engine) layer — applies to every page
- **Answer first:** direct answer in the first 2 sentences, then detail. Question as H1/H2.
- **Entity consistency:** same name, address (Tysons), phone, NPN, and bio on site, GBP, Bing Places, Apple Business Connect, LinkedIn, Yelp/BBB; `sameAs` links in schema.
- **Structured data:** FAQPage + BlogPosting + InsuranceAgency/areaServed on every geo page.
- **Citeable facts:** cite Census/CMS/SSA sources inline; no invented stats.
- Reviews and a real founder bio are the trust signals AI answers lean on.

## Cadence
| Window | Posts | Focus |
|---|---|---|
| Oct 12–Dec 7 | 1/day | 2:1 Medicare AEP : wealth |
| Dec 8–Dec 31 | 4/week | Wealth + year-end retirement/IUL, ACA open enrollment |
| Jan 1–Mar 31 | 4/week | MA-OEP, wealth, county pages roll out |
| Apr onward | 3/week | wealth + county pages, refresh older posts |

## Scorecard (check weekly; needs GA4 + Search Console access)
Calls, form fills, appointments set, appointments held, applications; GSC clicks/impressions by state and county; GBP calls/direction requests; reviews added.

## Open dependencies
Census API key or OK to download ACS (county ranking); Search Console export; confirm GA4 property continuity (G-RTWTB09G4R → G-J5YG8E3PYC); compliance sign-off on wealth pages.
