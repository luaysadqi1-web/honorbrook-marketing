#!/usr/bin/env python3
"""
Honorbrook Insurance -- daily social poster.

Runs unattended from launchd. Reads the drafts for today out of queue/, runs
every one through the compliance linter, publishes what passes to X and
LinkedIn, and holds what does not. Reddit items are never auto-posted; they are
written out for manual posting.

  python3 run_daily.py                 post today's queue
  python3 run_daily.py --dry-run       lint and report, publish nothing
  python3 run_daily.py --date 2026-09-02
"""

import argparse
import datetime
import os
import sys
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))

import compliance
import store
import x_client
import linkedin_client
import gbp_client

AUTO_PLATFORMS = ("x", "linkedin", "gbp")


class NotConfiguredError(str):
    """Marks a failure where nothing was sent, so the item can be retried."""


def publish(item, dry_run):
    """Send one item. Returns (post_id, error_or_None)."""
    platform = item["platform"]
    try:
        if platform == "x":
            return x_client.post(item["text"], dry_run=dry_run), None
        if platform == "linkedin":
            return linkedin_client.post(item["text"], dry_run=dry_run), None
        if platform == "gbp":
            return gbp_client.post(
                item["text"],
                cta=item.get("cta", "CALL"),
                cta_url=item.get("cta_url"),
                dry_run=dry_run,
            ), None
        return None, "platform %r is not auto-posted" % platform
    except (x_client.NotConfigured, linkedin_client.NotConfigured,
            gbp_client.NotConfigured) as e:
        # Nothing was transmitted, so this stays retryable.
        return None, NotConfiguredError("not configured: %s" % e)
    except (x_client.PostError, linkedin_client.PostError,
            gbp_client.PostError) as e:
        return None, str(e)
    except Exception as e:
        return None, "unexpected error: %s" % e


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    store.load_dotenv()
    date_str = args.date or store.today_str()

    queue = store.load_queue(date_str)
    if queue is None:
        print("no queue file for %s -- nothing to post." % date_str)
        print("run the generator to refill queue/ (see _daily-social-spec.md)")
        return 0

    items = queue.get("items", [])
    pending = [i for i in items if i.get("status") == "pending"]
    if not pending:
        print("%s: nothing pending (%d item(s) already handled)."
              % (date_str, len(items)))
        return 0

    print("=" * 68)
    print("Honorbrook daily social -- %s%s"
          % (date_str, "  [DRY RUN]" if args.dry_run else ""))
    print("=" * 68)

    posted = held = failed = skipped = 0

    for item in pending:
        platform = item["platform"]
        text = item["text"]
        label = "%s / %s" % (platform, item.get("pillar", "-"))

        # Reddit is drafted only -- posting there from a bot gets the account
        # banned, so it is deliberately routed to a human.
        if platform not in AUTO_PLATFORMS:
            item["status"] = "manual"
            skipped += 1
            print("\n[MANUAL] %s -- left for you to post by hand" % label)
            continue

        result = compliance.check(text, platform)
        if not result.ok:
            item["status"] = "held"
            item["blocks"] = [r for r, _ in result.blocks]
            held += 1
            print("\n[HELD]   %s (%d chars)" % (label, len(text)))
            for rid, why in result.blocks:
                print("         BLOCK %s -- %s" % (rid, why))
            if args.dry_run:
                continue
            store.append_log({
                "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
                "date": date_str, "platform": platform,
                "pillar": item.get("pillar", ""), "status": "held",
                "post_id": "", "chars": len(text),
                "blocks": "|".join(item["blocks"]), "text": text,
            })
            continue

        for rid, why in result.warns:
            print("\n[warn]   %s -- %s" % (label, why))

        post_id, err = publish(item, args.dry_run)
        if err:
            # A credential gap means the post never left this machine, so keep
            # it pending and it will go out on the next run once .env is filled
            # in. A genuine API failure stays "failed" -- retrying blind risks
            # double-posting something that may actually have landed.
            retryable = isinstance(err, NotConfiguredError)
            item["status"] = "pending" if retryable else "failed"
            item["blocks"] = [str(err)]
            failed += 1
            print("\n[FAILED] %s -- %s%s"
                  % (label, err, "  (stays queued)" if retryable else ""))
            status = "failed"
        else:
            item["status"] = "dry-run" if args.dry_run else "posted"
            item["post_id"] = post_id
            posted += 1
            print("\n[POSTED] %s -> %s" % (label, post_id))
            print("         %s" % text[:100].replace("\n", " "))
            status = item["status"]

        if args.dry_run:
            continue
        store.append_log({
            "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
            "date": date_str, "platform": platform,
            "pillar": item.get("pillar", ""), "status": status,
            "post_id": post_id or "", "chars": len(text),
            "blocks": "|".join(item.get("blocks", [])), "text": text,
        })

    # A dry run must not mutate state -- it only reports.
    if not args.dry_run:
        store.save_queue(date_str, queue)

    print("\n" + "-" * 68)
    print("posted %d | held %d | failed %d | manual %d"
          % (posted, held, failed, skipped))
    if held:
        print("Held drafts stay in queue/%s.json with status \"held\"." % date_str)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(1)
