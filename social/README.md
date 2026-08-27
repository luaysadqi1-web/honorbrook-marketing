# Honorbrook social routine

Daily automated posting to **Google Business Profile**, **X** and **LinkedIn**,
plus drafted (never auto-posted) **Reddit** replies.

## How it's built

Two stages, deliberately separate:

**1. Generation — weekly, needs Claude.** A routine runs each Sunday, reads
`topic-calendar.md`, writes the next seven days of drafts into `queue/`, and
commits them. Batching weekly means one missed run never takes the accounts dark.

**2. Posting — daily, needs nothing.** `run_daily.py` runs from launchd at 9:15am,
picks up today's queue file, lints every draft, publishes what passes. Pure
stdlib Python — no Claude, no venv, no pip, no app open. It just runs.

```
queue/2026-08-31.json ──> run_daily.py ──> compliance.check() ──┬─> Google Business Profile
                                                                ├─> X API
                                                                ├─> LinkedIn API
                                                                └─> held (stays in queue)
```

## The compliance linter

Every post is linted in-process before it goes out. This is the thing that makes
unattended posting for a licensed agency survivable. A draft that trips a BLOCK
rule is **held, not published** — it stays in the queue with the reason attached.

Blocking rules: named premiums / copays / "$0" / "free plan" (converts a CMS
*communication* into regulated *marketing*) · implied government affiliation ·
named carriers · superlatives and guarantees · high-pressure language · PHI
solicitation · attributed testimonials · promises of outbound contact (TCPA) ·
Medicare posts missing the required disclaimer · over-length.

Test any text yourself:

```bash
echo "Get a \$0 premium plan, best rates guaranteed!" | python3 lib/compliance.py x
```

## Daily use

Nothing, on a normal day. To check on it:

```bash
python3 run_daily.py --dry-run
```

Shows what would go out today and what would be held, without posting or
changing anything.

```bash
tail -5 logs/posted-log.csv
```

Everything that has posted, held, or failed, with reasons.

## Setup — three things, in order

1. **Keys.** Follow `SETUP-API-KEYS.md`, then `cp .env.example .env` and fill it
   in. `.env` is gitignored and never leaves this machine.
2. **Scheduler.**
   ```bash
   cp /Users/luaysadqi/honorbrook-marketing/social/com.honorbrook.social.daily.plist ~/Library/LaunchAgents/ && launchctl load ~/Library/LaunchAgents/com.honorbrook.social.daily.plist
   ```
3. **Refill the queue** before the current week runs out (the Sunday routine does
   this, or run the generator manually).

To stop it at any time:

```bash
launchctl unload ~/Library/LaunchAgents/com.honorbrook.social.daily.plist
```

## Files

| Path | What it is |
|---|---|
| `run_daily.py` | The daily poster. The only thing launchd runs. |
| `lib/compliance.py` | The linter. Rules and the CMS disclaimers. |
| `lib/gbp_client.py` | Google Business Profile local posts, OAuth2 refresh. |
| `gbp_authorize.py` | One-time Google auth helper; prints your `.env` values. |
| `lib/x_client.py` | X API v2, OAuth 1.0a, stdlib only. |
| `lib/linkedin_client.py` | LinkedIn Posts API, stdlib only. |
| `lib/store.py` | Queue files, `.env` loading, CSV log. |
| `topic-calendar.md` | Day-of-week pillars, topic bank, hard rules. |
| `_daily-social-spec.md` | The spec the weekly Claude routine executes. |
| `seed_week.py` | Writes a week of drafts. Also the format reference. |
| `queue/*.json` | Drafts, one file per day. |
| `reddit-drafts/*.md` | Manual-post Reddit replies. |
| `logs/posted-log.csv` | Every post attempt, with outcome. |

## Known limits

- **X free tier** allows ~500 posts/month and 17 per 24h. One post/day fits with
  enormous room. A 429 is logged and the item stays queued.
- **LinkedIn tokens expire ~60 days.** When it lapses, LinkedIn items fail and
  stay queued; X is unaffected. Refresh per `SETUP-API-KEYS.md`.
- **The Mac must be awake at 9:15am** for launchd to fire. If it is asleep the
  job runs on wake. If it is off, that day is skipped — the queue is not
  consumed, so nothing is lost except the day.
- **Reddit is manual by design.** See `reddit-drafts/_FORMAT.md`.
- **GBP posting requires Google to approve an API access request** against your
  Cloud project. Until it clears, GBP items fail with a 403 and stay queued
  while X and LinkedIn continue. The Google refresh token itself does not
  expire — but only if you **Publish** the OAuth consent screen; left in
  Testing, it dies after 7 days.

Each platform is independent: a dead LinkedIn token or an unapproved GBP project
never blocks the others.
