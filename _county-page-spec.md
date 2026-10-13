# County Landing Page: Build Spec (Honorbrook Insurance)

ONE page per county/parish/independent city. Structure and classes identical to the site. Template: read `/Users/luaysadqi/honorbrook-marketing/site/tysons-medicare-insurance.html` IN FULL (head, JSON-LD, header, banner, footer, sticky call, chat.js) plus `/Users/luaysadqi/honorbrook-marketing/site/{state}-medicare-insurance.html` for the state hub. Use ONLY existing classes from /assets/style.css, no inline `<style>`.

## HARD RULES
- **Honorbrook is based in Tysons, VA and serves these counties by phone and video (and in person only in Northern Virginia). NEVER claim a local office, "nearby", "in your neighborhood", or in-person availability outside Northern Virginia.** Say: "an independent agency licensed in {STATE}, helping {COUNTY} residents by phone or video call."
- **Every local fact must be verified this run via WebSearch/WebFetch from an official or primary source** (county site, hospital/health-system site, state SHIP, state Area Agency on Aging, CMS, Census). If you cannot verify a fact, leave it out. A short accurate page beats a padded one. Do NOT invent plan counts, premiums, benefit amounts, star ratings, or statistics.
- Allowed numeric fact (already verified): the county's 65+ population from the Census Bureau 2023 estimate given in your task; cite "U.S. Census Bureau, 2023 population estimates".
- CMS rules: Medicare disclaimer block in footer (copy from template). No "free plan", "$0", "best", "guaranteed", superlatives. Not government-affiliated.
- Do not edit sitemap.xml, blog/index.html, footers, or any other page. Write ONLY your 4 county files.

## Page contents (600-800 words)
- Filename: `{county-slug}-{st}-medicare-insurance.html` e.g. `wake-county-nc-medicare-insurance.html`, `virginia-beach-va-medicare-insurance.html`. Canonical `https://honorbrook-insurance.com/{filename-without-.html}`.
- `<title>`: `{County}, {ST} Medicare & Insurance Agent | Honorbrook Insurance`; meta description ~155 chars.
- Breadcrumb: Home › {State} (link `/{state-slug}-medicare-insurance`) › {County}.
- H1: `Medicare &amp; insurance help in <em>{County}</em>, {State}`.
- ANSWER BLOCK (first paragraph, 40-60 words): who we are, that we help {County} residents choose Medicare, ACA, life and retirement coverage by phone/video, free to the client, independent, licensed in {State}.
- h2 "Medicare in {County}": county seat/major cities, the 65+ population fact with Census citation, the major hospitals/health systems that serve the county (verified), and the point that Medicare Advantage/Part D plan availability and networks are set county by county so we check yours.
- h2 "Free help available in {County}": the state SHIP name + phone (given in task), the local Area Agency on Aging for the county (verified name + phone/URL), 1-800-MEDICARE.
- h2 "Coverage we offer {County} residents": bullets linking /medicare-advantage, /medicare-supplement-medigap, /medicare-part-d, /aca-health-insurance, /ichra, /group-health-insurance-shop, /life-insurance, /final-expense-life-insurance, /annuities.
- ONE `.callout` (plans and networks differ within the county; we check by your ZIP and doctors) and ONE `.cta-strip` to /#contact.
- FAQ 4 Q&As, county-specific, mirrored in FAQPage JSON-LD (e.g. "Can I get help with Medicare in {County} by phone?", "Will my {County} doctors and {hospital} be covered?", "Do you charge {County} residents?", "When can I enroll or change plans?" AEP Oct 15-Dec 7).
- `.related` grid-3: the state hub + 2 other pages from the same state's county set (siblings in your task).
- Schema: BreadcrumbList, FAQPage, and an `InsuranceAgency` with `areaServed` = AdministrativeArea for the county (name "{County}, {State}") and the agency address 8609 Westwood Center Dr, Suite 110, Tysons, VA 22182, phone (571) 354-0146.
- Byline: "Luay Sadqi, Licensed Agent, NPN 21370662" (same as template).

Final reply: list the 4 filenames, and for each the facts you could NOT verify and left out (one line each).
