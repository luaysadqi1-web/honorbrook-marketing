# Honorbrook SEO + GEO Master Plan (11 states, all lines)

Revised 2026-10-12 (v2). States: VA, MD, NC, SC, GA, AL, LA, TX, MI, IN, WV.

## STATUS (v2)
| Item | State |
|---|---|
| llms.txt, explicit AI-bot robots.txt | LIVE |
| 7 AEP answer posts (after Dec 7, do nothing, ANOC, plan dropped doctor, MA back to Original, Parts A-D, dental/vision/hearing) | LIVE |
| 11-state SHIP block + `contentLocation` schema on all 7 AEP posts | LIVE |
| Under-65 posts (cost without a job, OE deadline, subsidy changes, deductible vs OOP, HMO/PPO/EPO, 2-10 employees, self-employed deduction, health sharing, short-term) | LIVE (committed by the content engine) |
| 44 county/parish pages (4 per state x 11 states) + "Counties we serve" on every state hub + sitemap | LIVE |
| "Free plan" wording removed site-wide (150 files) | LIVE |
| Content engine cadence 4x/week (Mon/Tue/Thu/Fri 8am) | ON |
| Reviews/testimonials block on homepage | NOT DONE (needs real review text from GBP) |
| Person schema for Luay (NPN, 11 licensed states, sameAs) | NOT DONE |
| ACA state hubs for Nov 1 open enrollment | NEXT |
| State x life / IUL / FIA / final expense hubs | BLOCKED on license + appointment confirmation per state |

## What we learned (changes the strategy)
1. **Counties are the real geographic unit for Medicare.** MA and Part D are sold by county; Medigap and ACA price by area. 1,077 counties/parishes exist in the 11 states (Census 2023). County pages are justified, but only with real local facts: thin template pages are doorway-spam risk.
2. **We are remote outside Northern Virginia.** Every out-of-state page must say phone/video; never claim a local office. Local-pack ranking will not come from these pages (GBP is Tysons), so they compete on organic and AI-citation, not map pack.
3. **State SHIP/AAA data is a reusable trust asset.** Each state has a SHIP helpline and local Area Agency on Aging; citing them gives pages a verifiable, non-templated core. Several county facts could not be verified (county seats, some hospitals, some AAA phones). Those were left out, not guessed.
4. **Parallel agents collide.** They share a scratchpad and a repo, and a background job commits with `git add -A`. Rules from now on: one writer per file, agents write only their own files, orchestrator registers sitemap/index, verify what is on disk after every batch.
5. **Compliance wording is a site-wide issue, not per page.** Fixed "free plan"; keep the linter (`social/lib/compliance.py`) and page scans in the loop.

## Architecture (revised): Line x State x County x Intent
| Layer | Status | Next |
|---|---|---|
| Pillar (national) product pages (~20) | live | add FAQ/answer blocks |
| State hubs (11), Medicare | live + county lists | add ACA, life, ICHRA/SHOP sections |
| **County/parish pages** | 44 live (top 4 by 65+ pop per state) | Wave 2: next 4 per state (44 more) once Wave 1 shows indexing |
| State x line hubs (ACA, ICHRA, life, IUL/FIA, final expense, kids) | none | build ACA first (Nov 1); others gated by licensing |
| Answer posts (national, 11-state block) | ~60 live | 4/week; every post carries the 11-state block |
| NoVA city pages | 10 live | keep |

### County rollout rules
- Wave 1 (done): 44 pages. Gate to Wave 2: >=60% of pages indexed in Search Console within 4 weeks AND impressions on county-named queries.
- Wave 2 (Nov-Dec): next 4 per state by 65+ population. Wave 3: top ~15 per state where verified AAA/hospital data exists. Do NOT mass-publish all 1,077.
- A county page ships only if it has: verified hospitals/health systems, verified local AAA or state aging bureau, SHIP number, Census figure, county-specific FAQ. Otherwise hold.
- Add real, checkable county differentiators over time: CMS Medicare Advantage landscape (plan counts by county, if retrievable), ACA rating area and insurers participating (healthcare.gov/state exchange), county ZIP list.
- Expansion option: "Medicare by ZIP" lookup tool/FAQ rather than 1,000 pages.

## Content pillars (unchanged order)
1. Under 65: individuals, families, small business. 2. Medicare, every part. 3. High-income: IUL, FIA, term vs permanent. 4. Seniors: final expense. 5. Parents: juvenile whole life (Gerber-style), college funding.

## GEO checklist (revised)
- [x] llms.txt, explicit AI-bot robots.txt
- [x] Answer block + "In your state" (11 states) on AEP posts
- [x] State-level schema (`contentLocation`) on posts, `areaServed` on county pages
- [ ] Person schema for Luay (NPN, licensed states, sameAs) + author page
- [ ] Add 11-state block to the older ~30 posts (same script)
- [ ] Primary-source citations inline on every post
- [ ] Visible testimonials (real GBP reviews; no AggregateRating on own site)
- [ ] AI-citation tracker: monthly, same 30 questions in ChatGPT, Perplexity, Gemini, Google AI Overviews; log whether Honorbrook is cited and which page
- [ ] Off-site entity: consistent NAP/NPN on BBB, Yelp (both still say Vienna), LinkedIn; helpful Reddit answers (no solicitation)

## Calendar
- **Now - Oct 31:** AEP posts push (4/week); reviews block; Person schema; 11-state block backfill on older posts; request indexing for county pages in Search Console; fix Yelp/BBB address.
- **Nov 1 - Dec 7 (AEP + ACA OE):** ACA state hubs x11; county Wave 2; ICHRA/SHOP state hubs; keep Medicare AEP posts first.
- **Dec 8 - Jan 15:** high-income cluster (IUL x5, FIA x4), seniors cluster, parents cluster; state x life hubs for states where licensed.
- **Jan - Mar:** MA Open Enrollment posts (Jan 1 - Mar 31); county Wave 3; Spanish /es/ mirror (priority metros TX, GA, NC).

## KPIs
Indexed pages and index rate for the 44 county pages; impressions on question and county queries; AI-citation log; GBP calls/directions; leads by state, line and county (GA4 events already installed); review count.

## Compliance guardrails (unchanged, plus)
- No "free plan"/"$0"/superlatives; Medicare disclaimer on Medicare pages; independent-agency disclaimer elsewhere.
- IUL/FIA: no projected returns, no "tax-free retirement"; explain caps, participation rates, surrender charges.
- Kids/college: tradeoffs only vs 529.
- Any local fact must be verified from an official source or omitted.
- Confirm lines of authority and carrier appointments per state before publishing a state x line page.

## Decisions needed from Luay
1. For each of the 11 states: which lines are you licensed AND appointed for (esp. annuities/FIA, IUL, health outside VA)? Blocks all state x life/IUL/FIA hubs.
2. Permission to read your real Google reviews from GBP for the testimonials block.
3. Approve county Wave 2 once Wave 1 shows indexing.
