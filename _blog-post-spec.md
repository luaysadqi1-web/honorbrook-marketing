# Blog Post — Build Spec (Honorbrook Insurance content engine)

Each run: produce ONE SEO blog post as a standalone HTML file, visually identical to the site, then register it in the blog index and sitemap.

## Step 1 — Template
Read `/Users/luaysadqi/honorbrook-marketing/site/medicare-advantage.html` for the exact head/header/footer/banner/sticky/chat structure and the CSS classes. The post links `/assets/style.css`. Use ONLY existing classes (page-hero, breadcrumb, prose, callout, table.compare, cta-strip, kicker, faq, band, related, rel-card). No invented classes, no inline `<style>`.

## Step 2 — Write the post
Path: `/Users/luaysadqi/honorbrook-marketing/site/blog/{slug}.html` (slug = kebab-case of the title).
- Same `.topbar`, `<header>` (img logo + tagline), `<footer>`, `.sticky-call`, and `<script src="/assets/chat.js" defer></script>` as the site.
- Header `<a class="logo" href="/">` and nav links use absolute paths (`/medicare-advantage`, etc.) so they work from `/blog/`.
- `<title>`: `{Post Title} | Honorbrook Insurance`
- meta description ~155 chars, canonical `https://honorbrook-insurance.com/blog/{slug}`.
- Breadcrumb: `Home › Blog › {short title}` (link Home=/ , Blog=/blog/).
- `.page-hero` with H1 = the post title (one `<em>` gold accent word), a one-line lead, and a small byline line: "By Luay Sadqi, Licensed Agent (NPN 21370662) · {Month Year}".
- `<article class="article"><div class="wrap prose">` body: 800–1100 words, clear h2/h3, at least one bullet list, one `.callout`, and one `.cta-strip` (CTA to `/#contact` or the relevant product page). Link to 2–4 relevant product/state pages in-body.
- A short FAQ (3 Q&As) + FAQPage JSON-LD, plus BreadcrumbList JSON-LD, plus a BlogPosting JSON-LD (`headline`, `datePublished`, `author` = Luay Sadqi, `publisher` = Honorbrook Insurance).
- `.related` grid-3 linking 3 relevant pages.
- `.band` closing CTA (same as template).

## Compliance (MANDATORY)
- If the post involves Medicare, the footer MUST include the Medicare disclaimer block (copy from the medicare-advantage template footer). For non-Medicare posts (ICHRA, ACA, group, life) use the independent-agency disclaimer (copy from `/ichra.html`).
- Never invent statistics, carrier-specific claims, or specific plan prices. Keep guidance general and truthful. No "official Medicare" implication.
- Educational tone, plain English, no pressure. Add a one-line note that it's general info, not advice, and a licensed agent will help.

## Step 3 — Register the post
1. In `/Users/luaysadqi/honorbrook-marketing/site/blog/index.html`, insert a new `<a class="rel-card">` card for this post **immediately after** the `<!-- POSTS:START -->` marker (newest first), with the post title, date, and a one-line summary, linking to `/blog/{slug}`.
2. In `/Users/luaysadqi/honorbrook-marketing/site/sitemap.xml`, add a `<url>` for `https://honorbrook-insurance.com/blog/{slug}` (priority 0.7, changefreq monthly) before the `</urlset>`.
3. In `/Users/luaysadqi/honorbrook-marketing/_blog-topics.md`, mark the chosen topic done by changing its leading `- [ ]` to `- [x]`.

## Step 4 — Publish (only if this is a git repo)
If `/Users/luaysadqi/honorbrook-marketing` is a git repository with a remote, `git add -A && git commit -m "blog: {title}" && git push`. If not a git repo, STOP after writing files — the post is a draft for the owner to review and upload. Never force-push; branch if not on the default branch.

Netlify auto-publishes from `main` and a build takes roughly 10 seconds.

## Step 5 — Ping IndexNow (only if Step 4 actually pushed)
Tell Bing, Yandex, Naver and Seznam the post exists instead of waiting for a crawl. From the repo root:

```
./scripts/indexnow.sh /blog/{slug} /blog/
```

Submit the new post **and** `/blog/` so the index page's updated links get recrawled too.

- The script waits for each URL to return 200 before submitting, so it is safe to run immediately after `git push` — it will poll for up to ~45 seconds while Netlify builds.
- It refuses to submit anything if the key file at `/{key}.txt` isn't live, and skips any URL that never comes up. A skipped URL means the deploy failed — check Netlify before assuming the post is published.
- Expected output: `OK (200) — accepted.`
- **Google does not use IndexNow.** For Google, the sitemap entry from Step 3 is what matters. If a post is time-sensitive, additionally request indexing manually in Search Console → URL Inspection.
