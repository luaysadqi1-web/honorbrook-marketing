# State Landing Page — Build Spec (Honorbrook Insurance)

You are building ONE production HTML page that is visually and structurally IDENTICAL to the existing site.

## Step 1 — Read the template
Read `/Users/luaysadqi/honorbrook-marketing/site/medicare-advantage.html` IN FULL. Copy its EXACT structure and CSS classes:
- `<head>`: same meta / OG / Twitter pattern, the two JSON-LD `<script type="application/ld+json">` blocks, and `<link rel="stylesheet" href="/assets/style.css">`.
- Body order: `.topbar` → `<header>` (with `<img src="/assets/logo.svg">` + `.logo-text` containing the `<small>` tagline) → `.aep-banner` → `.page-hero` (breadcrumb + h1 + lead + hero-ctas) → `<article class="article"><div class="wrap prose">` → `<section class="faq">` → `.band` → `<section class="related">` (grid-3 of `.rel-card`) → `<footer>` → `.sticky-call` → the AEP `<script>`.
- Use ONLY classes that already exist (page-hero, breadcrumb, prose, callout, table-wrap, table.compare, cta-strip, kicker, faq, band, related, rel-card, btn-primary, btn-ghost). Do NOT invent classes or add inline `<style>`.
- KEEP the Medicare AEP banner and its `<script>` exactly as in the template (these are Medicare-relevant pages, so the `#aepMsg` span + script stay).

## Step 2 — Write the file to the path given in your task.

## Content rules
- This is a **{STATE} location hub** page. Tone: warm, plain-English, honest, no pressure.
- ~700–800 words in the article. **Do NOT invent statistics or specific numbers** — keep claims general and truthful.
- `<title>`: `{STATE} Medicare & Insurance Broker — Free Local Help | Honorbrook Insurance`
- meta description (~155 chars): Independent Medicare & insurance help for {STATE} residents — compare Medicare Advantage, Medigap, Part D, ICHRA, ACA & life from 90+ carriers, free & no-pressure. Serving {CITY1}, {CITY2} & all of {STATE}. Call (571) 354-0146.
- canonical + OG url: `https://honorbrook-insurance.com/{SLUG}`
- Breadcrumb: `Home › {STATE}`
- H1 with one `<em>` gold word, e.g. `Medicare &amp; insurance help across <em>{STATE}</em>`
- Lead paragraph: Honorbrook is an independent agency licensed in {STATE}, helping residents compare and choose Medicare, health, and life coverage with free, no-pressure guidance — handled by phone.

### Article sections (h2's)
1. **"Insurance help for {STATE} residents"** — who we help; free because carriers pay us, not you.
2. **"Coverage we offer in {STATE}"** — a bullet list, each linking to the real product page:
   `<a href="/medicare-advantage">Medicare Advantage</a>`, `<a href="/medicare-supplement-medigap">Medicare Supplement (Medigap)</a>`, `<a href="/medicare-part-d">Part D drug plans</a>`, `<a href="/final-expense-life-insurance">final expense</a>`, `<a href="/life-insurance">life insurance</a>`, `<a href="/ichra">ICHRA</a>`, `<a href="/aca-health-insurance">ACA plans (under 65)</a>`, `<a href="/group-health-insurance-shop">group / SHOP coverage</a>`.
3. **"Serving communities across {STATE}"** — a short paragraph plus a sentence naming these cities/metros: {CITIES}. State that everything is handled by phone — no office visit needed.
4. Include ONE `.callout` (plan availability varies by county in {STATE} — we check what's available at your exact address) and ONE `.cta-strip` (CTA button to `/#contact`).
5. **"Why {STATE} families choose Honorbrook"** — independent, 90+ carriers, always free, year-round service (claims help, annual reviews).

### FAQ — 4 Q&As, {STATE}-flavored, and MIRRORED in the FAQPage JSON-LD:
- "Do you charge {STATE} residents for help?" — No, it's free; carriers pay a commission and your premium is identical either way.
- "Which {STATE} cities do you serve?" — All of {STATE}, by phone — name a few from {CITIES}.
- "What plans can I get in {STATE}?" — Availability varies by county; we compare what's offered at your address.
- "Can you help if I'm new to {STATE} or moving?" — Yes; a move can open a Special Enrollment Period.

### Schema
- BreadcrumbList: Home → {STATE} (canonical URL).
- FAQPage: the 4 Q&As above.
- Any schema address must use: 8609 Westwood Center Drive, Vienna, VA 22182 (the office).

### Related (grid-3) — link to the 3 other state pages named in your task (slugs like `/maryland-medicare-insurance`).

### Footer
Copy the template footer EXACTLY — it already has the correct Medicare disclaimer, the Vienna VA service-areas line, the 4 columns, phone (571) 354-0146, email, and `/#contact`. Keep the `.band` section identical too.

When done, reply with ONLY the file path and a one-line confirmation.
