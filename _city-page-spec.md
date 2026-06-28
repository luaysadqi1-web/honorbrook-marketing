# City Landing Page — Build Spec (Honorbrook Insurance)

You are building ONE hyper-local city page, visually/structurally IDENTICAL to the existing site. These target "Medicare agent / insurance near me in {CITY}" searches. Honorbrook's office is at 8609 Westwood Center Drive, Vienna, VA — so these Northern Virginia cities are the real local market.

## Step 1 — Template
Read `/Users/luaysadqi/honorbrook-marketing/site/medicare-advantage.html` IN FULL for exact structure/classes: head meta/OG/Twitter, two JSON-LD scripts, `<link rel=stylesheet href=/assets/style.css>`, body order: `.topbar` → header (`<img src="/assets/logo.svg">` + `.logo-text` with `<small>` tagline) → `.aep-banner` → `.page-hero` (breadcrumb + h1 + lead + a reviewer byline line + hero-ctas) → `article.article>.wrap.prose` → `section.faq` → `.band` → `section.related` (grid-3 `.rel-card`) → footer → `.sticky-call` → AEP `<script>`. Use ONLY existing classes. No invented classes, no inline `<style>`. KEEP the Medicare AEP banner + its `<script>`. The header nav is: About /about · Medicare /medicare-advantage · Final Expense /final-expense-life-insurance · Annuities /annuities · Blog /blog/ · Contact /contact. The topbar reads "Independent agency · Serving Virginia &amp; 10 more states". Footer: copy the standard Medicare-disclaimer footer from the template EXACTLY (it already says "11 licensed states" and has the correct CMS disclaimer). Add `<script src="/assets/chat.js" defer></script>` before `</body>`.

## Step 2 — Write the file to the path given in your task.

## Content rules
- ~600–750 words, warm/plain-English/no-pressure tone. **Use ONLY the real local facts provided in your task — do NOT invent statistics, plan counts, or details you weren't given.**
- `<title>`: `{CITY}, VA Medicare & Insurance Agent — Free Local Help | Honorbrook Insurance`
- meta description (~155): Local, independent Medicare & insurance help for {CITY}, Virginia residents — compare Medicare Advantage, Medigap, Part D, life & more, free & no-pressure, in person or by phone. Call (571) 354-0146.
- canonical + og:url: `https://honorbrook-insurance.com/{SLUG}`
- Breadcrumb: `Home › Virginia › {CITY}` (link Home=/ and Virginia=/virginia-medicare-insurance)
- H1 with one `<em>` gold word, e.g. `Medicare &amp; insurance help in <em>{CITY}</em>, Virginia`
- Reviewer byline line right after the lead (before hero-ctas): `<p class="sans" style="font-size:14px;color:#aebbd0;letter-spacing:.3px;margin-top:4px">Local independent agency · Luay Sadqi, Licensed Agent · NPN 21370662</p>`
- Lead: local and personal — independent agency based nearby in Vienna, helping {CITY} residents choose coverage with free, no-pressure guidance, in person by appointment or by phone.

### Article sections (h2's)
1. **"Local Medicare & insurance help for {CITY}"** — we're an independent agency based right nearby in Vienna; we help {CITY} neighbors in person (by appointment) or by phone; free because carriers pay us.
2. **"Coverage we offer {CITY} residents"** — bullet list linking each product page: `<a href="/medicare-advantage">Medicare Advantage</a>`, `<a href="/medicare-supplement-medigap">Medicare Supplement (Medigap)</a>`, `<a href="/medicare-part-d">Part D drug plans</a>`, `<a href="/final-expense-life-insurance">final expense</a>`, `<a href="/life-insurance">life insurance</a>`, `<a href="/annuities">annuities</a>`, `<a href="/aca-health-insurance">ACA (under 65)</a>`, `<a href="/ichra">ICHRA</a>`.
3. **"Knowing {CITY}'s doctors and hospitals"** — THE local-relevance section. Use the LOCAL FACTS provided (county, nearby hospitals/health systems, neighborhoods, landmarks) to show we know the area. Make the point that with Medicare Advantage, the local provider network matters — and we verify your {CITY}-area doctors and hospitals are covered before you enroll. Weave the real local facts in naturally.
4. ONE `.callout` (Medicare Advantage networks and plan availability differ even within {COUNTY} — we check what's available and in-network at your {CITY} address) and ONE `.cta-strip` (CTA to /#contact).
5. **"Why {CITY} families choose Honorbrook"** — independent, 90+ carriers, free, year-round local service.

### FAQ — 4 Q&As, {CITY}-specific, MIRRORED in FAQPage JSON-LD:
- "Can I meet with a {CITY} Medicare agent in person?" — Yes; by appointment — the office is nearby in Vienna, or we come to you / handle it by phone.
- "Will my {CITY}-area doctors and hospitals be covered?" — On Medicare Advantage it depends on the plan's network; we verify your specific providers (reference a real local hospital from the facts) before you enroll. Medigap lets you see any doctor that accepts Medicare.
- "Do you charge {CITY} residents for help?" — No, it's free; carriers pay us and your premium is the same.
- "When can I enroll or change plans?" — IEP at 65, AEP Oct 15–Dec 7, or a Special Enrollment Period (e.g. moving to/within {CITY}).

### Schema
- BreadcrumbList: Home → Virginia (https://honorbrook-insurance.com/virginia-medicare-insurance) → {CITY} (canonical).
- FAQPage: the 4 Q&As.
- Any address in schema = 8609 Westwood Center Drive, Vienna, VA 22182.

### Related (grid-3): link to the 3 nearby city/area pages named in your task.

When done, reply with ONLY the file path and a one-line confirmation.
