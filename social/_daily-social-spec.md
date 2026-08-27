# Weekly social generation spec

This is the prompt-spec the Claude routine runs. It generates **one week at a
time** so that a single missed run never takes the account dark — the poster
keeps working from the queue either way.

Cadence: **Sundays.** Generates the following Mon–Sun.

## Steps

1. Read `topic-calendar.md` for this week's pillars and the hard rules.
2. Read `logs/posted-log.csv` and the last 8 files in `queue/`. Do not repeat a
   topic used in the last 60 days.
3. For each of the seven days, write:
   - **one X post.** If the topic is Medicare, the content body must be
     **≤ 193 characters** — the disclaimer is appended automatically by
     `compliance.fit_x()`. Otherwise ≤ 280.
   - **one LinkedIn post**, 600–1200 characters. Real substance, short
     paragraphs, no hashtag spam, no "🚀". Medicare topics carry the full
     disclaimer at the end.
   - **one Google Business Profile post**, 300–450 characters of content. The
     reader is on the profile with intent, so front-load the offer — only the
     first ~200 characters show before "Read more". Concrete and local. Set
     `"cta": "CALL"`, which uses the phone number already on the profile.
     Build the text with `compliance.append_disclaimer(body, "gbp")`, which
     appends the full CMS disclaimer when the topic is Medicare.
4. Write each day to `queue/YYYY-MM-DD.json` using the schema below.
5. Generate 3 Reddit drafts into `reddit-drafts/YYYY-MM-DD.md` (see below).
6. Run `python3 run_daily.py --date <each day> --dry-run` for all seven days.
   **Every item must report `held 0`.** Rewrite anything held and re-check.
7. `git add social/queue social/reddit-drafts && git commit`.

## Queue schema

```json
{
  "date": "2026-08-31",
  "generated": "2026-08-30T09:00:00",
  "source": "weekly-generator",
  "items": [
    {
      "id": "a1b2c3d4e5",
      "platform": "x",
      "pillar": "medicare-foundations",
      "text": "…full post text, disclaimer already appended…",
      "note": "",
      "status": "pending",
      "post_id": null,
      "blocks": []
    }
  ]
}
```

`status` must be `pending`. The poster owns every other value. GBP items carry
one extra key, `"cta": "CALL"`.

Use `compliance.append_disclaimer(body, platform)` for LinkedIn and GBP, and
`compliance.fit_x(body)` for X, rather than typing disclaimers by hand.

## Voice

Match the site: plain English, calm, specific, no hype. "The right coverage.
The honest way." Short sentences. Lead with the thing the reader did not know.
Never open with "Did you know" or "In today's world". Never use an em dash where
a period works.

Say "we" for the agency. Luay signs nothing on social unless the post is
explicitly first-person about him.

## Reddit drafts — read this part carefully

Reddit is **never auto-posted**. r/Medicare, r/HealthInsurance and r/AskALawyer
style subs ban agent solicitation, and a promotional bot account gets banned and
can taint the brand name in search.

What the generator produces instead: **three drafted replies to real, current
threads**, for Luay to post manually from his personal account.

Rules for these drafts:
- Find genuine recent questions via web search (`site:reddit.com` + the topic).
- The reply must fully answer the question **with no link and no pitch.** If the
  answer is complete without mentioning Honorbrook, that is the correct answer.
- Disclose the role once, plainly, at the end: "I'm an independent agent, happy
  to answer follow-ups either way." No phone number. No URL.
- If the sub's rules ban agent participation, do not draft for it. Say so.
- Never draft a reply that argues with someone or corrects them harshly.

Value first, for months, is the only Reddit strategy that survives.
