# Free plan: post daily on every channel

Goal: daily posts on X, LinkedIn, Google Business Profile, Facebook and Instagram
with no paid API. Reddit stays manual by policy. Items marked "verify" come from
third-party write-ups; confirm on the platform before relying on them.

| Channel | Free route | Effort | Status |
|---|---|---|---|
| X | Manual, 3 a day, from the daily packet page (X's API now bills per post, and link posts cost more) | ~3 min/day | Ready now |
| LinkedIn | Free API for posting to your company page (token refresh every 60 days); or manual from the packet | Setup once, then 0 | Needs a new token (`linkedin_authorize.py`) |
| Google Business Profile | Free API but Google must approve access (slow, verify). Until then, post by hand from the packet, or from Google Search on your own business name | ~1 min/day | Ready now (manual) |
| Facebook Page + Instagram | Free Graph API for your own Page and IG business account (already partly set up in `.env`, `META_APP_SECRET` is empty), or Metricool (already connected) | Setup once | Needs app secret |
| Reddit | Manual only, never automated | ~5 min, 2x/week | Reddit blocks search here; paste thread URLs |

## How it works day to day
1. The weekly generator writes the week's posts, infographics and videos (as now).
2. `python3 daily_packet.py --open` builds one page for today: each post's text with a
   Copy button, the image or video file to attach, and a link to that platform's
   composer. Paste, attach, post. Do the 09:15, 13:00 and 18:00 X posts when due.
3. Platforms with working free APIs post themselves. To stop the poster trying a
   platform, put `SOCIAL_MANUAL_PLATFORMS=x` (comma list) in `.env`.

## Keep the cost at zero
- X: do not use the paid API. Posting by hand is free.
- If you later pay for X, strip links from most posts and set a spend cap first.
- Free scheduler as a middle option: Buffer, Metricool or X's own composer can queue
  posts ahead. Free-plan limits change, so check before building around one (verify).

## Order of work
1. Today: use the packet for X and GBP.
2. This week: re-authorise LinkedIn so it posts itself.
3. Next: add `META_APP_SECRET`, check Facebook and Instagram posting works.
4. Apply for Google Business Profile API access; switch GBP to automatic once approved.

## Geography
Copy is no longer limited to Northern Virginia. See Geography in `topic-calendar.md`
(11 licensed states).
