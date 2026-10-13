# Honorbrook SEO + GEO Master Plan (11 states, all lines)

Written 2026-10-12. States: VA, MD, NC, SC, GA, AL, LA, TX, MI, IN, WV.

## Where we are
- 79 sitemap URLs: 8+ Medicare/health product pages, 11 state hubs, 26 blog posts, 10 NoVA city pages.
- Strength: schema (FAQPage, BlogPosting, BreadcrumbList), NAP clean, answer-style titles already adopted in the blog backlog.
- Gaps:
  1. **State hubs are Medicare-only** (`{state}-medicare-insurance.html`). Zero state-level surface for ACA, ICHRA/small business, life, IUL, FIA, final expense, kids. That is 11 states x 7 lines of unclaimed search surface.
  2. **No GEO layer**: no llms.txt (added today), no named-expert/entity signals on posts, no "quotable answer block" pattern.
  3. **Blog cadence is 1/week**. The backlog has ~35 open topics, so ~8 months at that rate. Too slow for AEP (Oct 15 - Dec 7) and ACA OE (Nov 1 - Jan 15).
  4. **High-income / life / FIA / kids topics have not started**, and the product pages for them exist but nothing links in from answer content.
  5. 26 real Google reviews appear nowhere on the site.

## Architecture: Line x State x Intent grid
Each cell is a page that answers one question for one audience.

| Layer | What | Count |
|---|---|---|
| Pillar (national) | Product pages that exist today | ~20 |
| State x line hubs (NEW) | e.g. `/texas/aca-health-insurance`, `/georgia/life-insurance`, `/north-carolina/ichra` | 11 states x 6 lines = 66 |
| Answer posts (national, state-aware) | Real-person questions; state specifics in a "In your state" block | 100+ |
| City pages | Keep NoVA; add 1 anchor metro per out-of-state market (Houston, Charlotte, Atlanta, Detroit, Indianapolis, Baltimore, Columbia, Birmingham, New Orleans, Charleston WV) only AFTER state-line hubs rank | later |

State x line hubs must contain real, checkable state facts (state Marketplace name, state Medicaid expansion status, state DOI, SHIP name and phone, state-run vs HealthCare.gov exchange, state premium-tax or guaranty-association limit). No templated filler: that is a thin-content risk. State facts get verified from the state DOI / exchange / SHIP site before publish.

## Content pillars (priority order, per your direction)
1. **Under 65: individuals, families, small business.** ACA, subsidies after the enhanced credits expired, ICHRA, SHOP/group, self-employed, job loss, kids on a plan.
2. **Medicare, every part.** A/B/C/D, Medigap, AEP, ANOC, switching, IRMAA, Medicaid/dual, turning 65.
3. **High income.** IUL, FIA, term vs permanent, cash value, policy loans, estate/legacy, how much coverage.
4. **Seniors.** Final expense, graded benefit, 80+ with health problems, funeral cost.
5. **Parents.** Juvenile whole life (Gerber-style), guaranteed insurability, college funding, life vs 529 tradeoffs.

## Question-first writing rule
- Title is the question a person types or says to an assistant.
- First 2 sentences answer it directly (the "answer block" AI engines lift).
- Then: steps/table, "In your state" block (VA, MD, NC, SC, GA, AL, LA, TX, MI, IN, WV, with only facts we verified), FAQ (3-5 related questions, FAQPage schema), reviewer byline (Luay, NPN), compliance footer.
- Mine real questions from: Google People Also Ask, Reddit r/Medicare r/healthinsurance r/personalfinance, Medicare.gov FAQs, SHIP helpline topics, your own call/chat logs (best source, add the Brook chatbot transcripts).

## GEO (Generative Engine Optimization) checklist
- [x] llms.txt published (site/llms.txt)
- [ ] robots.txt: explicitly Allow GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Bingbot (currently `Allow: /` for all, which already works; making it explicit documents intent)
- [ ] Answer-block pattern on every post and product page (direct answer in first 40-60 words)
- [ ] Person schema for Luay with NPN, licensed states, sameAs (LinkedIn, GBP). Expert + entity signals.
- [ ] Cite primary sources inline (CMS, Medicare.gov, KFF, state DOI) with links. AI engines prefer citable pages.
- [ ] Consistent entity facts everywhere (NAP, 11 states, NPNs, 90+ carriers). Same wording on site, GBP, BBB, Yelp, LinkedIn.
- [ ] Brand mentions off-site: Reddit helpful answers (no solicitation), Quora, HARO/Qwoted-style expert quotes, local news, chamber.
- [ ] Reviews on site as visible testimonials (NO AggregateRating schema on own site).
- [ ] Freshness: dateModified refreshed on seasonal posts every Oct/Nov/Jan.
- [ ] Track: monthly query a fixed list of 30 questions in ChatGPT, Perplexity, Gemini, Google AI Overviews and log whether Honorbrook is cited.

## Compliance guardrails (non-negotiable, already in backlog rules)
- Medicare content: CMS disclaimer; no plan premiums/benefits as marketing claims; no "free"/"$0" claims.
- IUL/FIA: no projected returns, no "tax-free retirement", explain caps, participation rates, surrender charges, fees, carrier-guarantee dependence; not investment/tax/legal advice.
- Kids/college: do not call a policy "better than a 529"; tradeoffs only.
- No invented statistics. Every number cites a source on the page.
- Per-state: confirm the agency's lines of authority in each state before publishing a state x line page for that line (e.g. life and health appointments). Your 11 licenses cover health and life per your signature; verify annuity/FIA appointments by state.

## Execution phases
**Phase 1 (this week, AEP-critical)**
- Publish llms.txt (done), explicit AI-bot robots, Person schema.
- Ship 7 AEP posts from the backlog (ANOC, "do nothing", after Dec 7, drops my doctor, MA back to Original, A/B/C/D, DVH coverage). Batch, not weekly.
- Add a visible reviews/testimonial block to homepage.

**Phase 2 (Oct 20 - Nov 15)**
- Build 11 x ACA state hubs (Nov 1 OE) and 11 x Medicare answer hubs refresh.
- 8 under-65 and small-business posts (cost without a job, OE deadline, subsidy changes, HMO/PPO/EPO, 2-10 employees, self-employed deduction).

**Phase 3 (Nov 15 - Jan 31)**
- State x life, final expense, IUL/FIA hubs (verify appointments first).
- High-income cluster (IUL x5, FIA x4), seniors cluster (x5), parents cluster (x5).

**Phase 4 (Feb onward)**
- ICHRA/SHOP state hubs, metro anchor pages, Spanish mirror (/es/ with hreflang), Medicare Advantage OEP posts (Jan 1 - Mar 31).

## Cadence to hit coverage
Move the content engine from 1/week to **4/week during AEP/OE**, 2/week after. Roughly 120 posts and 66 state-line pages by end of Q1 2027.

## KPIs
Indexed pages (Search Console), impressions on question queries, AI-citation log score, GBP calls/directions, form + chat leads by state and line, review count.

## Needs from you
1. Which lines are you licensed AND appointed to sell in each of the 11 states (esp. annuities/FIA, IUL, health in non-VA states)? Drives which state-line hubs I'm allowed to publish.
2. OK to raise cadence to 4 posts/week during AEP.
3. Approve the plan so I start Phase 1.
