# Honorbrook Daily Prospecting Bot — Master Playbook
### B2B client acquisition + agent recruiting, run once every weekday

This is the strategy + operating manual for a **daily automated outbound engine**. It targets **businesses and agents** — never cold Medicare consumers (that's illegal under TCPA + CMS; consumer leads come from the website/inbound only).

Companion files:
- `PROSPECTING-OUTREACH-SCRIPTS.md` — every email, LinkedIn, and call script, by segment.
- `_daily-prospecting-spec.md` — the machine instructions the bot follows each day.

---

## ⚖️ Compliance guardrails (read first — these shape everything)
- **No cold outreach to Medicare beneficiaries.** Ever. TCPA + CMS. Consumers reach us via the website.
- **B2B email (to businesses/agents) is legal under CAN-SPAM** if every email: uses a truthful from-name and subject, identifies Honorbrook, includes our **physical address** (8609 Westwood Center Dr #110, Tysons, VA 22182), and offers a **one-click opt-out** that we honor within 10 days. The bot enforces this on every send.
- **Calls:** business/office lines are fair game for B2B; **scrub against the DNC + our internal suppression list**; no autodialer/prerecorded messages to cell phones without consent.
- **No cold SMS** to prospects who haven't opted in.
- **Human-in-the-loop send.** The bot *drafts*; a person reviews and sends. This keeps us compliant and on-brand, and avoids spam-trap damage to our domain.
- **Suppression list is sacred.** Anyone who opts out, or is an existing client/DNC, never gets contacted again. The bot checks this list before every draft.
- **Recruiting captive agents:** poaching is legal, but do **not** induce anyone to breach a non-compete/non-solicit or misuse their current book/client data. Message the person, not their book.

---

## 🎯 The 5 segments (one per weekday)

| Day | Segment | Who | Core offer |
|---|---|---|---|
| **Mon** | ICHRA business owners | Owners/HR of 2–50 employee firms | Replace/skip group health with a tax-free ICHRA — predictable budget, no renewals |
| **Tue** | Independent pharmacies | Owner/PIC of independent pharmacies | (a) ICHRA for their staff + (b) **referral partnership** — we help their senior customers with Part D/Medicare that keeps them in-network |
| **Wed** | Business verticals | Dental/medical practices, gyms, salons, real-estate offices, franchises, nonprofits, churches | ICHRA/group + worksite/voluntary benefits |
| **Thu** | New / aspiring agents | Newly-licensed or studying for license; career-changers | Join Honorbrook: training, leads from our marketing engine, tech stack, real independent contracts |
| **Fri** | Captive agents | Agents at single-carrier/captive shops | Go independent: 90+ carriers, keep more commission, own your book, plug into our lead machine |

*(Rotate segments so no audience is over-contacted; each prospect enters a multi-touch sequence, not a one-off.)*

---

## 🧭 Ideal Customer Profiles (targeting criteria the bot filters on)

**1. ICHRA business owners**
- Size: 2–50 W-2 employees. Sweet spot 5–25.
- Signals: recently posted jobs (growing), no benefits listed, in a high-premium state, S-corp/LLC, industries with thin margins (restaurants, retail, trades, agencies, startups, nonprofits).
- Titles: Owner, Founder, CEO, President, Office Manager, HR.
- Where: Apollo/LinkedIn Sales Nav filters, Google Maps for local, state business registries, industry associations.

**2. Independent pharmacies**
- Independent (NOT CVS/Walgreens/Rite Aid chains). 1–5 locations.
- Titles: Owner, Pharmacist-in-Charge (PIC), Pharmacy Manager.
- Where: NCPA member directories, Google Maps "independent pharmacy near [city]", state pharmacy boards.
- Double value: they employ staff (ICHRA) AND see Medicare seniors daily (referral partner).

**3. Business verticals** — same as ICHRA but by vertical list: dental practices, chiropractors, med-spas, gyms/CrossFit, salons/barbershops, real-estate brokerages, home-service franchises, nonprofits, churches.

**4. New / aspiring agents**
- Recently earned or studying for a Life & Health license; career-changers (retail, sales, mortgage, real estate, teachers, veterans).
- Titles/signals: "Licensed Insurance Agent (new)", "Aspiring", bootcamp/exam-prep groups, Indeed applicants.
- Where: LinkedIn, Facebook licensing/exam groups, Indeed, local NAIFA chapters, exam-prep course communities.

**5. Captive agents**
- Agents at captive/single-carrier orgs (e.g., one-carrier field forces, bank/credit-union insurance desks, single-brand agencies).
- Titles: "Insurance Agent at [captive]", "Field Agent", "Financial Representative".
- Pain: limited product menu, low comp split, no ownership of book, quotas.
- Where: LinkedIn Sales Navigator (filter by current company = captive brands), industry events.

---

## 🔁 The daily loop (what the bot does every weekday)

```
1. PICK segment of the day (per the Mon–Fri table).
2. PULL ~20–30 fresh prospects matching that segment's ICP
   (from Apollo / a saved list / LinkedIn export).
3. SCRUB against the suppression list (opt-outs, clients, DNC).
4. ENRICH + PERSONALIZE: for each prospect, draft a compliant
   first-touch email + a LinkedIn connection note, using the
   segment's script + one specific personalization hook.
5. QUEUE follow-ups: draft the next-step message for anyone in
   a prior sequence who hasn't replied (Day 3 / 7 / 14 cadence).
6. OUTPUT everything to /outbox/YYYY-MM-DD.md for human review.
7. HUMAN sends the approved ones (email tool / LinkedIn / dialer),
   and logs replies to Integrity Connect.
8. LOG the batch + move responders into the CRM pipeline.
```

**Realistic daily volume:** 20–30 new touches + ~20 follow-ups = a steady ~250 fresh prospects/week without burning your domain or tripping spam filters. Quality personalization > blasting.

---

## 🛠️ Tools / automation stack (what to connect)
- **Lead source:** Apollo.io (best for B2B firmographics + emails/phones) — or Clay, or LinkedIn Sales Navigator exports, or manual Google-Maps lists to start.
- **The bot brain:** a scheduled Claude routine (like your blog engine) that reads `_daily-prospecting-spec.md`, drafts the day's outbox, and (optionally) commits it. Can be set up with the `/schedule` routine.
- **Email sending:** a cold-email platform with warmup + unsubscribe handling (Instantly, Smartlead, or Apollo sequences) on a **separate domain** (e.g. `honorbrookpartners.com`) so cold outreach never risks your main domain's deliverability.
- **LinkedIn:** manual or a compliant assistant tool (respect connection limits ~20/day).
- **Calls:** your existing dialer, DNC-scrubbed.
- **CRM:** Integrity Connect — track every prospect stage (New → Contacted → Replied → Meeting → Won/Recruited).

> ⚠️ **Deliverability:** send cold B2B email from a *secondary* domain with SPF/DKIM/DMARC + inbox warmup. Never blast cold mail from `honorbrook-insurance.com` — protect the domain your clients and Google trust.

---

## 📊 KPIs to watch (weekly)
- New prospects contacted, by segment
- Email open / reply / positive-reply rate (target 40%+ open, 5–10% reply on good B2B lists)
- Meetings booked (business demos + agent interviews)
- New group/ICHRA clients closed
- Agents recruited (new + captive)
- Cost per meeting / per recruit

---

## 🚦 Rollout order
1. **Week 1:** stand up the secondary sending domain + warmup; connect Apollo; load the suppression list.
2. **Week 1–2:** run the bot in **draft-only** mode — review its outbox daily, refine the scripts to your voice.
3. **Week 3+:** turn on daily sending for the segments that are converting; add follow-up automation.
4. **Ongoing:** feed replies back so the bot learns which hooks land; expand ICP lists.
