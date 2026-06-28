# Honorbrook "Brook" Chatbot — Setup Guide

Your site now has a 24/7 AI chat assistant ("Brook") on every page. It answers questions
about Medicare, ICHRA, ACA, life insurance, etc., and captures leads (name + phone) straight
to your inbox — all with TCPA consent and compliance guardrails built in.

The chat widget is already live on the site. It just needs an **Anthropic API key** to start
thinking. Until then, it shows a friendly "please call us" fallback (so you never lose a lead).

---

## What's in this project

```
honorbrook-marketing/
├── netlify.toml                      ← tells Netlify where the site + function live
├── site/                             ← your website (deploy this folder's contents)
│   ├── index.html, *.html            ← all your pages (chat widget already embedded)
│   └── assets/
│       ├── style.css, logo.svg       ← design
│       └── chat.js                   ← the chat widget (front end)
└── netlify/functions/
    └── chat.js                       ← the secure "brain" (calls Claude; key stays here)
```

---

## One-time setup (about 10 minutes)

### 1. Get an Anthropic API key
1. Go to **https://console.anthropic.com** and sign in (or create an account).
2. Add a small amount of billing credit (Settings → Billing). $20 goes a very long way (see costs below).
3. Go to **API Keys → Create Key**, name it "Honorbrook Website", and copy the key
   (it starts with `sk-ant-...`). You won't be able to see it again, so paste it somewhere safe.

### 2. Deploy this project to Netlify with the function
The chatbot needs the serverless function, so deploy the **whole project folder** (the one
containing `netlify.toml`), not just the `site` folder.

**Easiest: connect a GitHub repo (recommended for the chatbot)**
1. Put this `honorbrook-marketing` folder in a GitHub repository.
2. In Netlify: **Add new site → Import an existing project → pick the repo.**
3. Netlify reads `netlify.toml` automatically (publishes `site/`, deploys the function). Done.

**Or: drag-and-drop**
- Drag the entire `honorbrook-marketing` folder (with `netlify.toml` inside) onto the Netlify
  **Deploys** area. Netlify will publish `site/` and pick up the function.

### 3. Add your API key to Netlify (this is what keeps it secret)
1. In your Netlify site: **Site configuration → Environment variables → Add a variable.**
2. Add:  **Key:** `ANTHROPIC_API_KEY`   **Value:** your `sk-ant-...` key
3. (Optional) `LEAD_ENDPOINT` — defaults to your existing Formspree form so chat leads email you.
   Replace the placeholder Formspree ID (`xgobjlba`) in the function/forms with your real one first.
4. **Redeploy** the site (Deploys → Trigger deploy) so the key takes effect.

### 4. Test it
Open your live site, click **"Chat with us"**, and ask "I'm turning 65, can you help?"
Brook should answer in seconds. Try giving a name + phone and saying yes to a callback —
you should get a "🔵 New CHATBOT lead" email.

---

## What it costs

Brook runs on **Claude Haiku 4.5** — fast and inexpensive ($1 per million input tokens,
$5 per million output tokens). A typical full back-and-forth conversation costs roughly
**2–5 cents**. So $20 of credit covers **hundreds of conversations**. You only pay for
actual chats; an idle widget costs nothing.

To use a smarter (pricier) model, set a Netlify env var `CHAT_MODEL` to `claude-sonnet-4-6`.
Haiku 4.5 is the right default for a website chatbot.

---

## Compliance — what's already built in
- Brook is clearly labeled an **automated assistant, not a licensed agent**, and won't give
  quotes, specific plan advice, or enroll anyone — it hands those to you.
- It shows **TCPA consent language** before capturing a phone number and only saves a lead
  after the visitor agrees (reply STOP to opt out).
- It will **not** collect SSNs, Medicare ID numbers, full DOBs, or health histories in chat.
- It states Honorbrook is **not connected with Medicare/government**.

You can tune Brook's personality, knowledge, and rules by editing the `SYSTEM_PROMPT` text
near the top of `netlify/functions/chat.js`, then redeploying.

---

## Next step (optional): pipe leads into Integrity Connect
Right now chat leads email you via Formspree (same as your forms). When you're ready, we can
wire `forwardLead()` in `netlify/functions/chat.js` to push leads straight into Integrity
Connect / your dialer via its API or a Zapier/Make webhook — just let me know which integration
Integrity Connect supports and I'll set it up.
