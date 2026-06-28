# Honorbrook Insurance — Lead Follow-Up ("Speed-to-Lead") Playbook

**Agency:** Honorbrook Insurance (trade name of Luay's Lifeline Inc.)
**Licensed agent:** Luay Sadqi · NPN 21370662 · Office: Vienna, VA
**Phone:** (571) 354-0146 · **Email:** info@honorbrook-insurance.com · **Site:** https://honorbrook-insurance.com
**CRM / ecosystem:** Integrity Connect (Integrity / MedicareCENTER) + dialer
**Lead sources:** Website forms (Formspree → info@), website chatbot ("Brook"), Google Business Profile, social
**Products:** Medicare (Advantage / Medigap / Part D), final expense, life, ICHRA, ACA, group/SHOP

> This is the operating manual for turning inbound, opted-in leads into enrollments. Copy-paste the templates. Follow the cadence. Log everything in Integrity Connect.

---

## 1. Why speed-to-lead matters

Inbound insurance leads have a short window of attention. The principle is simple and well-established:

- **The first agent to make real contact usually wins the relationship.** A lead who just filled out a form or chatted with "Brook" is thinking about coverage *right now*. Reach them while they're still in that mindset and you're the helpful expert. Reach them tomorrow and you're an interruption.
- **Interest fades fast.** Within hours, the lead has moved on with their day, may have submitted forms on competitor sites, or has cooled off entirely. Every hour of delay lowers the odds of a connect.
- **Speed signals competence.** A near-instant, human, personalized response tells the lead you're organized, responsive, and worth trusting with their Medicare or life coverage.
- **Persistence compounds speed.** One fast attempt isn't enough. A structured multi-touch cadence (call + text + email over two weeks) dramatically outperforms a single try. Most contacts happen after the first attempt.

**The rule of this playbook:** *Every opted-in lead gets an automated text + email within ~1–5 minutes, a live dial attempt the same hour, and a structured 14-day cadence until they connect or opt out.*

> We do **not** cite specific conversion statistics here on purpose — vendor stats vary wildly and age fast. The principles above are durable. Build the habit, not the headline.

---

## 2. The flow

```
                         ┌─────────────────────────────────────────────┐
                         │   LEAD CAPTURED (opted in)                  │
                         │   • Website form (Formspree → info@)        │
                         │   • Chatbot "Brook" (forwardLead())         │
                         │   • Google Business Profile / call / social │
                         └───────────────────────┬─────────────────────┘
                                                 │
                                                 ▼
                    ┌────────────────────────────────────────────────┐
                    │   WEBHOOK / AUTOMATION (Zapier or Make)         │
                    │   Parses lead → fans out to all systems         │
                    └───┬───────────────┬───────────────┬────────────┘
                        │               │               │
            ┌───────────▼──┐   ┌────────▼────────┐  ┌───▼──────────────┐
            │ Integrity    │   │ INSTANT SMS     │  │ INSTANT EMAIL    │
            │ Connect /    │   │ (within 1–5 min)│  │ (confirmation +  │
            │ LeadCENTER:  │   │ "Hi, it's Luay  │  │  expectations)   │
            │ create lead, │   │  from Honorbrook"│ └──────────────────┘
            │ tag "New",   │   └─────────────────┘
            │ load dialer  │
            └──────┬───────┘
                   │
                   ▼
        ┌──────────────────────┐      Connected?
        │  AGENT DIALS (dialer)│──────────────────► YES ──► SOA → needs → quote → enroll
        │  same hour            │                          (tag accordingly)
        └──────────┬───────────┘
                   │ NO answer
                   ▼
        ┌──────────────────────────────────────────────┐
        │  STRUCTURED CADENCE (call + SMS + email)      │
        │  Day 0 (2nd try) → Day 1 → Day 3 → Day 7      │
        │  → Day 14, then move to long-term nurture     │
        └──────────────────┬───────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────────────┐
        │  LOG + TAG every touch in Integrity Connect   │
        │  New → Contacted → SOA on file → Quoted →     │
        │  Enrolled → Annual review                     │
        └──────────────────────────────────────────────┘
```

**Same-hour standard:**
1. Lead hits the webhook.
2. Automated **SMS** fires within ~1–5 min.
3. Automated **confirmation email** fires within ~1–5 min.
4. Lead is created + tagged **New** in Integrity Connect and queued in the dialer.
5. Agent **dials** the same hour (ideally within minutes of the alert).
6. If no answer → cadence begins automatically; agent logs each touch.

---

## 3. TCPA-compliant SMS templates

**Ground rules for every text (do not skip):**
- These go **only** to leads who opted in (submitted a form, used the chatbot, or otherwise requested contact). No cold texting.
- Each message **identifies Honorbrook and Luay by name**.
- Each message **references that the lead reached out / requested info** (this anchors consent and keeps it conversational, not "telemarketing").
- Messages are **conversational and individually sent** by the agent (or a one-to-one texting tool) — not pre-recorded, not blasted as auto-dialed marketing.
- Each message includes **"Reply STOP to opt out."**
- Keep them **short and human**. No ALL CAPS, no spammy punctuation, no fake urgency.
- Texting hours: keep to reasonable local hours (roughly 8am–9pm recipient time).

### Day 0 — Instant first response (fires within 1–5 min of capture)
```
Hi {First}, this is Luay Sadqi with Honorbrook Insurance — thanks for
reaching out about coverage on our site. I'd love to help. Is now a
good time for a quick call, or should I try later today?
Reply STOP to opt out.
```

### Day 0 — Second attempt (a few hours later, if no answer to call/text)
```
Hi {First}, Luay with Honorbrook again. Tried giving you a call about
the info you requested. No rush — what time works best for you to
connect? You can also reach me at (571) 354-0146.
Reply STOP to opt out.
```

### Day 1 — Follow-up
```
Hi {First}, it's Luay from Honorbrook Insurance. Still happy to walk
you through your options whenever you're ready. Mornings or afternoons
better for a quick call?
Reply STOP to opt out.
```

### Day 3 — Value nudge
```
Hi {First}, Luay here with Honorbrook. There's no cost and no pressure —
just want to make sure you have the right info for the coverage you
asked about. Want me to send a quick summary by email, or call you?
Reply STOP to opt out.
```

### Day 7 — Check-in
```
Hi {First}, Luay with Honorbrook Insurance following up on the request
you sent. If now's not the right time, just let me know when is and
I'll reach back out then.
Reply STOP to opt out.
```

### Day 14 — Final attempt before long-term nurture
```
Hi {First}, Luay from Honorbrook one more time. I don't want to crowd
your inbox — if you're still interested I'm here at (571) 354-0146 or
info@honorbrook-insurance.com. Otherwise I'll close this out and you're
always welcome to reach back. Reply STOP to opt out.
```

> **Handling replies:** If someone replies STOP, opt them out immediately in your texting tool **and** tag it in Integrity Connect so no automation re-texts them. If they reply with a question, take over the conversation personally — never let automation respond to a real reply.

---

## 4. Email templates

> Send from **info@honorbrook-insurance.com** (or luay@…). Always include the agency name, agent name, phone, NPN, and an unsubscribe/opt-out line on non-transactional emails. Never imply government affiliation.

### (a) Instant confirmation / expectation-setting (fires within 1–5 min)
**Subject:** Thanks for reaching out, {First} — here's what happens next

```
Hi {First},

Thanks for contacting Honorbrook Insurance — I got your request and I'm
glad to help.

I'm Luay Sadqi, a licensed independent insurance agent (NPN 21370662)
based in Vienna, VA. Because I'm independent, I can compare options
across multiple carriers and help you find the plan that actually fits
your situation — not just one company's product.

Here's what happens next:
  1. I'll give you a quick call at the number you provided.
  2. We'll talk through what you're looking for — no cost, no pressure.
  3. If it makes sense, I'll put together clear options for you to compare.

If you'd rather pick a time, just reply to this email or call me
directly at (571) 354-0146.

Talk soon,
Luay Sadqi
Honorbrook Insurance
(571) 354-0146 · info@honorbrook-insurance.com
https://honorbrook-insurance.com
Licensed independent agent · NPN 21370662
```

### (b) Value follow-up (if no answer after first call attempts)
**Subject:** Still here to help with your coverage, {First}

```
Hi {First},

I tried reaching you about the coverage information you requested — no
worries, I know schedules get busy.

A few things I can help with whenever you're ready:
  • Medicare — Advantage, Medigap (Medicare Supplement), and Part D
  • Final expense and life insurance
  • ACA / individual health, ICHRA, and small-group (SHOP) coverage

There's never a cost to talk, and I'll only ever recommend what genuinely
fits your needs. When's a good time for a 10-minute call?

Reply here or call/text me at (571) 354-0146.

Best,
Luay Sadqi
Honorbrook Insurance · (571) 354-0146
info@honorbrook-insurance.com · NPN 21370662

To stop receiving these emails, reply "unsubscribe."
```

### (c) AEP reminder (Annual Enrollment Period, Oct 15 – Dec 7)
**Subject:** {First}, Medicare's annual window is open (Oct 15–Dec 7)

```
Hi {First},

Quick heads-up: the Medicare Annual Enrollment Period runs October 15
through December 7. This is the once-a-year window to review your
Medicare Advantage or Part D coverage and make changes for next year —
plans, drug lists, and costs can shift every year.

Even if you're happy with your current plan, a 15-minute review makes
sure you're not overpaying or missing a benefit. I'll do the comparison
for you — there's no cost.

Want me to run a review before the deadline? Reply here or call/text
(571) 354-0146 and we'll find a time.

Luay Sadqi
Honorbrook Insurance · (571) 354-0146
info@honorbrook-insurance.com · NPN 21370662

We do not offer every plan available in your area. Any information we
provide is limited to the plans we do offer. Please contact Medicare.gov,
1-800-MEDICARE, or your local State Health Insurance Program (SHIP) to
get information on all of your options.

To stop receiving these emails, reply "unsubscribe."
```

### (d) Long-term "annual review" nurture
**Subject:** Time for your yearly coverage check-in, {First}

```
Hi {First},

It's Luay with Honorbrook Insurance. We connected a while back, and I
like to check in once a year with everyone I work with — your needs and
the available plans both change over time.

It's a good moment to make sure:
  • Your current coverage still fits your situation and budget
  • You're aware of any new options that could save you money
  • Beneficiaries and details on any life/final-expense policies are current

No cost, no obligation — just a quick review so you stay covered the
right way. Want to grab 15 minutes?

Reply here or call/text me at (571) 354-0146.

Always here when you need me,
Luay Sadqi
Honorbrook Insurance · (571) 354-0146
info@honorbrook-insurance.com · NPN 21370662

To stop receiving these emails, reply "unsubscribe."
```

---

## 5. Medicare-specific compliance (CRITICAL — read before contacting anyone)

> These rules carry real regulatory and carrier consequences. When in doubt, slow down and stay compliant. This section is a working summary, **not legal advice** — confirm current CMS rules and your carriers'/Integrity's compliance requirements each plan year.

### 5.1 Only contact leads who opted in (TCPA)
- Call, text, or email **only** people who **requested contact** — submitted a form, used the "Brook" chatbot, called you, or otherwise gave permission. **No cold outreach.**
- Honor **STOP / unsubscribe / do-not-call** requests immediately and permanently. Tag it in Integrity Connect so no automation re-engages them.
- Keep proof of consent (the form submission, chatbot transcript, timestamp). Store it with the lead record.
- Texting/calling within reasonable local hours (roughly 8am–9pm recipient time).

### 5.2 Medicare sales calls must be recorded and retained
- CMS requires that **telephonic Medicare sales and enrollment calls be recorded in their entirety and retained** (per CMS guidance, generally **10 years**). This covers marketing/sales conversations about Medicare Advantage and Part D, not just the enrollment moment.
- Use the **dialer's / MedicareCENTER's call recording** so every Medicare sales call is captured and stored. Confirm recording is **on before** you discuss any specific plan.
- Tell the caller the call is recorded if your dialer doesn't already announce it (VA is a one-party-consent state, but CMS recording is the binding requirement here).

### 5.3 Scope of Appointment (SOA) is required before discussing specific Medicare plans
- For Medicare Advantage (MA/MAPD) and Part D (PDP), you must obtain a **Scope of Appointment** that documents which product type(s) the beneficiary agreed to discuss — **before** the sales appointment / before discussing those specific plans.
- The SOA must be **retained** (generally **10 years**).
- A SOA can be captured electronically (e.g., via MedicareCENTER/Integrity Connect's SOA tool or a signed/recorded SOA) and, for most appointments set in advance, should be on file **before** the meeting. There is a CMS-required waiting period between SOA and appointment in many cases (currently 48 hours, with limited exceptions) — confirm the current rule each year.
- The SOA **limits the conversation** to the agreed product types. To discuss a different product type, you need a new/expanded SOA.

### 5.4 Don't be misleading or imply government affiliation
- Never state or imply you're from Medicare, Social Security, CMS, or "the government." You're an **independent licensed agent**.
- Don't use words/logos that suggest government endorsement.
- Be accurate about plan benefits and costs; don't overstate.
- Include the **multi-plan disclaimer** on Medicare marketing where applicable: *"We do not offer every plan available in your area. Any information we provide is limited to the plans we do offer in your area. Please contact Medicare.gov or 1-800-MEDICARE to get information on all of your options."*
- Identify yourself and Honorbrook clearly at the start of every contact.

### 5.5 SOA explainer (plain-English, for your reference and to explain to clients)
> A **Scope of Appointment** is a short, CMS-required form that records which kinds of Medicare plans (e.g., Medicare Advantage, Part D drug plans, Medicare Supplement) a person agreed to talk about with you. It exists to protect the beneficiary — it makes sure they're only being shown what they asked to see, and that no one is steered into products they didn't agree to discuss. It's documentation, **not** an enrollment or commitment, and it doesn't obligate them to anything.

### 5.6 Sample "let's get your SOA on file" message
**SMS / verbal script:**
```
Hi {First}, before we go over any specific Medicare plans, CMS requires
a quick Scope of Appointment — it just confirms which types of plans
you'd like me to discuss (like Advantage, Part D, or Supplement). It's
free, takes 30 seconds, and doesn't commit you to anything. I'll send
a secure link now / can we knock it out at the start of our call?
Reply STOP to opt out.
```
**Email subject:** Quick 30-second step before we review your Medicare options

```
Hi {First},

Before we talk through any specific Medicare Advantage or drug plans,
Medicare's rules require a Scope of Appointment on file. It's a quick
form that just confirms which types of plans you'd like me to go over.

It protects you — it makes sure I only show you what you actually asked
about — and it doesn't obligate you to anything or cost a thing.

Here's the secure link: {SOA_LINK}

Once that's in, we can dive into your options. Questions? Call or text
me at (571) 354-0146.

Luay Sadqi
Honorbrook Insurance · NPN 21370662
```

> **Note:** SOA and recording requirements apply to **Medicare** (MA/MAPD/PDP) sales. Medicare Supplement (Medigap), final expense, life, ACA, ICHRA, and group have their own rules but are not subject to the MA/PD SOA requirement — keep a separate mental track so you don't either skip a required Medicare SOA or wrongly demand one where it doesn't apply.

---

## 6. Wiring it to Integrity Connect + the dialer

Goal: a lead from **any** source lands in Integrity Connect, triggers the instant SMS + email, and loads into the dialer — automatically. Three setup options, simplest to most powerful.

### Option A — Formspree email parsing (fastest to stand up, most manual)
- Formspree already emails each submission to **info@honorbrook-insurance.com**.
- Set up an inbox rule / parser (Gmail filter + a tool, or Zapier's **Email Parser by Zapier**) to read the name/phone/email out of those emails.
- Pipe the parsed fields into Integrity Connect (manual entry or import) and your texting tool.
- **Pros:** works today, no API needed. **Cons:** brittle (breaks if Formspree's email format changes), slower, more manual. Use as a stopgap.

### Option B — Formspree → Zapier/Make webhook → everything (recommended)
This is the real "speed-to-lead" engine. Step-by-step:

1. **Capture the lead as structured data.**
   - In **Formspree**, enable webhooks (Formspree → form settings → Integrations/Webhook) **or** add a custom webhook plugin so each submission POSTs JSON to your automation.
   - In **Zapier**: create a Zap with trigger **"Webhooks by Zapier → Catch Hook."** Copy the webhook URL Zapier generates.
   - In **Make (Integromat)**: create a scenario starting with a **"Webhooks → Custom webhook"** module; copy its URL.
   - Paste that URL into Formspree's webhook field. Submit a test lead to populate the field mapping.

2. **Create / update the lead in Integrity Connect / LeadCENTER.**
   - Add an action step that pushes the lead into Integrity. **Check Integrity Connect's available integration first** (see "Confirming the integration" below) — you'll use one of:
     - a **native Integrity/LeadCENTER connector** if Zapier/Make offers one,
     - Integrity's **API** via a "Webhooks → Custom Request (POST)" / HTTP module, or
     - **CSV import / LeadCENTER's own lead-ingestion** if no API is exposed.
   - Set the lead's tag/stage to **New** on creation.

3. **Fire the instant SMS (within 1–5 min).**
   - Add an SMS action: use **the dialer's built-in texting** if it exposes an API/Zapier action, or a one-to-one texting service like **Twilio** or **SimpleTexting**.
   - Map in the lead's first name + phone; use the **Day 0 instant-response** template from Section 3 (include "Reply STOP to opt out").

4. **Fire the instant confirmation email.**
   - Add an email action (Gmail/Google Workspace send, or your ESP) using template **(a)** from Section 4.

5. **Queue the dialer + alert the agent.**
   - Add the lead to the dialer's call list (via its connector/API) **and** send Luay a push/SMS/Slack alert: "New Honorbrook lead: {First} {Phone} — call now."

6. **Branch by product / source (optional but useful).**
   - Use a filter/router step so Medicare leads, final-expense leads, and ACA leads get slightly different first-touch copy and the right tag.

7. **Test end-to-end** with a real submission before going live. Verify: lead appears in Integrity, SMS arrives, email arrives, dialer shows it, alert fires.

### Option C — Point the chatbot's `forwardLead()` at the same webhook
- "Brook" already has a `forwardLead()` hook. Change it to **POST the captured lead JSON to the same Zapier/Make webhook URL** from Option B (instead of, or in addition to, emailing info@).
- Now chatbot leads flow through the identical pipeline — instant SMS, email, Integrity record, dialer queue — with no separate plumbing.
- Include a `source: "chatbot-brook"` field in the payload so tagging/branching can tell chatbot leads from form leads.
- Do the same for **Google Business Profile** leads (forward GBP message/lead notifications into the webhook or enter them through the same intake) so every source converges on one flow.

### Confirming the Integrity Connect integration
Before building step 2 above, verify **how** Integrity Connect/LeadCENTER accepts external leads. Check, in order:
- **Integrity Connect / MedicareCENTER settings** → look for "Integrations," "API," "Lead sources," or "Inbound leads."
- **Integrity's agent/partner support or your upline/FMO** — ask specifically: "Does Integrity Connect / LeadCENTER offer an API or webhook for inbound leads, and is there a Zapier/Make connector?"
- The **dialer's** docs for its API/Zapier action (for both lead-loading and texting).
- If no public API exists, fall back to **LeadCENTER's native lead import / CSV** or Option A email parsing as the Integrity-write step, while still using Zapier/Make to drive the instant SMS + email + alert (those don't depend on Integrity's API).

> **Security note:** keep webhook URLs and any API keys/tokens in the automation tool's secret storage — don't hardcode them in the chatbot's front-end code. The chatbot should POST to a URL that doesn't expose credentials client-side (proxy through a server/endpoint if needed).

---

## 7. Tagging & tracking

### Lead stages (use these as your pipeline in Integrity Connect)
| Stage | Means | Move it here when… |
|-------|-------|--------------------|
| **New** | Just captured, not yet worked | Lead hits the CRM from any source |
| **Contacted** | Reached out, no productive conversation yet | First call/text/email attempt made |
| **SOA on file** | (Medicare) Scope of Appointment captured & retained | SOA signed/recorded before plan discussion |
| **Quoted** | Options presented / quote delivered | You've shown specific plans or sent a quote |
| **Enrolled** | Application submitted / coverage bound | Enrollment completed |
| **Annual review** | Active client in yearly nurture | Post-enrollment; review at AEP / policy anniversary |

**Supporting tags to layer on:** `source: form / chatbot / GBP / social`, `product: medicare / final-expense / life / ACA / ICHRA / group`, `DNC / opted-out`, `AEP-2025`, `callback-scheduled`.

**Always log:** every call (recorded for Medicare), text, and email — with timestamp and outcome — on the lead record.

### Daily follow-up checklist
```
[ ] Work all NEW leads first — dial within the same hour they arrived
[ ] Confirm every new lead got the auto SMS + confirmation email (spot-check the automation)
[ ] Make today's scheduled cadence touches (Day 0/1/3/7/14 dues)
[ ] Return all missed calls, texts, and email replies from leads
[ ] For any Medicare appointment today: SOA on file + recording ON before plan talk
[ ] Update every lead's STAGE and log each contact in Integrity Connect
[ ] Honor any STOP/unsubscribe/DNC immediately and tag it
```

### Weekly checklist
```
[ ] Review pipeline by stage — no lead stuck in "New" or "Contacted" untouched
[ ] Re-engage Day 14 leads that didn't connect → move to long-term nurture
[ ] Verify the automation is healthy (send a test lead end-to-end)
[ ] Confirm Medicare call recordings + SOAs are being retained/stored
[ ] Check for missed leads across all sources (form, chatbot, GBP, social)
[ ] Schedule annual-review outreach for clients hitting their policy anniversary
[ ] (Seasonal) Prep AEP campaign Oct 15–Dec 7; send AEP reminder email to eligible clients
```

---

### Quick-reference: the non-negotiables
1. **Speed:** auto SMS + email in ~1–5 min; live dial same hour.
2. **Consent:** opted-in leads only; honor STOP instantly.
3. **Persistence:** run the full Day 0→14 cadence.
4. **Medicare compliance:** record sales calls, get/keep the SOA before plan talk, never imply government affiliation, use the multi-plan disclaimer.
5. **Log everything** and keep the pipeline stages current in Integrity Connect.

*Confirm current CMS rules, TCPA requirements, and your carriers'/Integrity's compliance policies each plan year. This playbook is operational guidance, not legal advice.*
