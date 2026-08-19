# Daily Prospecting Bot — Run Spec
### The instructions the scheduled bot follows once every weekday

Read `PROSPECTING-BOT-PLAYBOOK.md` (strategy + compliance) and `PROSPECTING-OUTREACH-SCRIPTS.md` (copy) before running. Do the steps below, then STOP. This bot **drafts**; a human reviews and sends.

## Files it uses
- `prospecting/prospects-inbox.csv` — new leads to work (columns: `first_name,company,title,city,email,phone,segment,linkedin,hook`). You (or Apollo/Clay/a list export) drop rows here.
- `prospecting/suppression-list.csv` — do-not-contact (opt-outs, existing clients, DNC). One `email`/`phone`/`company` per row.
- `prospecting/outbox/YYYY-MM-DD.md` — where the bot writes the day's ready-to-send drafts.
- `prospecting/sent-log.csv` — appended after a human sends (for follow-up scheduling).

## Steps
1. **Determine today's segment** from the weekday: Mon=ICHRA owners · Tue=Pharmacies · Wed=Verticals · Thu=New agents · Fri=Captive agents. (Weekend = skip.)
2. **Select up to 25 prospects** from `prospects-inbox.csv` whose `segment` matches today (or are unlabeled and fit). If the inbox has fewer than 25 for today's segment, work what's there and note the shortfall.
3. **Scrub:** drop any prospect whose email/phone/company appears in `suppression-list.csv`. Never draft for them.
4. **Personalize:** for each remaining prospect, using that segment's scripts:
   - Draft **Email 1** (fill `{{FirstName}}`, `{{Company}}`, `{{City}}`, and a specific `{{Hook}}` from their row — if no hook given, write one neutral, truthful line; never invent facts).
   - Draft a **LinkedIn connection note** (≤300 chars) if a `linkedin` URL exists.
   - Include the **CAN-SPAM footer** on every email.
5. **Queue follow-ups:** read `sent-log.csv`; for anyone sent 3/7/14 days ago with no reply logged, draft the matching follow-up email from the scripts.
6. **Write the outbox file** `prospecting/outbox/YYYY-MM-DD.md`:
   - A "NEW TOUCHES" section: one block per prospect (name/company + the email + the LinkedIn note), copy-paste ready.
   - A "FOLLOW-UPS" section: same, for the follow-up drafts.
   - A short header: today's segment, # drafted, # suppressed, # shortfall.
7. **Compliance self-check before finishing:** confirm every email has the footer + opt-out, no Medicare *consumer* was targeted, and no suppressed contact slipped through. Note the check result at the top of the outbox.
8. **STOP.** Do not send anything. Reply with the outbox path and the day's counts.

## Rules
- **Never** cold-target Medicare beneficiaries/consumers — business & agent segments only.
- **Never** invent facts about a prospect (revenue, employee count, personal details). Personalize only from real fields provided.
- Keep emails short (under ~120 words), human, one ask.
- If `prospects-inbox.csv` is empty for today's segment, still draft any pending follow-ups and note that the inbox needs new leads.
