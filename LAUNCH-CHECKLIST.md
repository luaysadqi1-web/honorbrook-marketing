# 🚀 Honorbrook Launch Checklist

Everything is built and verified locally. Here's how to put it live on **honorbrook-insurance.com** (hosted on Netlify).

Your whole site lives in: **`/Users/luaysadqi/honorbrook-marketing/site/`**
(plus `netlify.toml` and `netlify/functions/chat.js` one level up, for the chatbot).

---

## ⚠️ Before you start — keep these existing files
Your current live site has a few files I did NOT recreate (they're already on your server). When you upload, **keep these** alongside the new files:
- `privacy-policy.html`
- `favicon-64.png`, `apple-touch-icon.png`
- `assets/og-image.jpg`

If they're missing after launch, you'll see a broken favicon, broken link previews, and a dead "Privacy Policy" link — so don't delete them.

---

## OPTION A — Quickest: drag-and-drop (site live in ~10 min)
Gets all your **pages** live fast. The **chatbot won't work** this way and blog posts won't auto-publish (you'd upload those manually). Good for going live today.

1. Make one folder on your computer that contains **both**:
   - everything in `honorbrook-marketing/site/` (index.html, all the product/state/blog pages, `assets/`, `sitemap.xml`), **and**
   - your existing `privacy-policy.html`, `favicon-64.png`, `apple-touch-icon.png`, `assets/og-image.jpg`.
2. Log in to **app.netlify.com** → open your Honorbrook site → **Deploys** tab.
3. **Drag that folder** onto the "drag and drop your site output folder here" area.
4. Wait ~30 seconds. Live. Visit the site and click around.

---

## OPTION B — Recommended: connect a GitHub repo (everything works)
This is the only way the **chatbot** and **auto-publishing blog** work. A bit more setup once, then every future change deploys automatically.

1. **Put the project in GitHub.**
   - Create a free account at github.com if you don't have one.
   - Create a new repository (e.g. `honorbrook-site`).
   - Upload the **entire `honorbrook-marketing` folder** (including `netlify.toml` and the `netlify/` folder), plus your existing `privacy-policy.html` / favicons / `og-image.jpg` inside `site/`.
   - (If this is unfamiliar, the GitHub Desktop app makes this drag-and-drop simple — or ask me and I'll walk you through it.)
2. **Connect Netlify to the repo.**
   - In Netlify: **Add new site → Import an existing project → GitHub →** pick `honorbrook-site`.
   - Netlify reads `netlify.toml` automatically (publishes `site/`, deploys the chatbot function). Click **Deploy**.
3. **Point your domain.** If the site was already on Netlify, move the `honorbrook-insurance.com` custom domain to this new site (Site configuration → Domain management), or just keep deploying to the existing site from the repo.

---

## TURN ON THE CHATBOT (after Option B)
See `CHATBOT-SETUP.md` for detail. Short version:
1. Get an API key at **console.anthropic.com** (add ~$20 credit). Copy the `sk-ant-...` key.
2. Netlify → **Site configuration → Environment variables → Add variable**:
   `ANTHROPIC_API_KEY` = your key.
3. **Trigger deploy** (Deploys → Trigger deploy) so the key takes effect.
4. Open the live site, click **"Chat with us,"** and test.

---

## CONNECT YOUR LEADS (forms + chatbot → your inbox)
The forms and chatbot use a Formspree placeholder. To receive leads:
1. Create a free form at **formspree.io** pointed at `info@honorbrook-insurance.com`.
2. Copy your form ID (looks like `abcdwxyz`).
3. Replace every `xgobjlba` in these files with your real ID:
   - `site/index.html`, `site/reviews.html`, and `netlify/functions/chat.js` (the `LEAD_ENDPOINT`).
   (I can do this find-and-replace for you in seconds once you have the ID.)

---

## TELL GOOGLE (so the pages get found)
1. Go to **search.google.com/search-console** and add/verify `honorbrook-insurance.com`.
2. **Sitemaps → submit** `https://honorbrook-insurance.com/sitemap.xml`.
3. (Optional) Add Google Analytics: create a GA4 property, then uncomment the GA4 snippet in `index.html` and paste your Measurement ID.

---

## DRIVE THE "NEAR ME" CALLS (highest ROI this week)
Open **`LOCAL-SEO-PLAYBOOK.md`** and do the Google Business Profile section:
1. Claim/optimize your GBP (categories, the paste-ready description, services, photos, Q&A).
2. Paste your GBP "write a review" link into `site/reviews.html` (replace `REPLACE_WITH_YOUR_PLACE_ID`).
3. Start asking happy clients for reviews using the templates.

---

## QUICK PRE-FLIGHT (after going live, click these)
- [ ] Homepage loads with the gold crest + heritage look
- [ ] A product page (e.g. /medicare-advantage) and a state page (e.g. /virginia-medicare-insurance) load
- [ ] /reviews and /blog/ load
- [ ] Favicon shows, Privacy Policy link works
- [ ] (Option B) "Chat with us" answers a question
- [ ] A test form submission arrives at info@honorbrook-insurance.com
