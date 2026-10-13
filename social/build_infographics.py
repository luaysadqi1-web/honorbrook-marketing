#!/usr/bin/env python3
"""
Render the day's infographic from infographic-specs/YYYY-MM-DD.json and attach
it to the queue items as "image" (path relative to social/). Only pending items
are touched. A spec that fails compliance is reported and NO image is attached,
so the day falls back to text-only.

  python3 build_infographics.py --from 2026-10-12 --days 7
"""
import argparse, datetime, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "lib"))
import infographic, store, shutil

SITE_DIR = os.path.join(HERE, "..", "site", "assets", "infographics")
SITE_URL = "https://honorbrook-insurance.com/assets/infographics/"

PLATFORMS = ("x", "gbp")  # LinkedIn stays text-only for now
# Images must be served from the live site before GBP can fetch image_url:
# deploy site/assets/infographics/ first.


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", required=True)
    ap.add_argument("--days", type=int, default=7)
    a = ap.parse_args()
    start = datetime.date.fromisoformat(a.start)
    bad = 0
    for n in range(a.days):
        d = (start + datetime.timedelta(days=n)).isoformat()
        sp = os.path.join(HERE, "infographic-specs", d + ".json")
        q = store.load_queue(d)
        if not q or not os.path.exists(sp):
            print("%s  no queue or spec, skipped" % d); continue
        specs = json.load(open(sp))
        specs = specs if isinstance(specs, list) else [specs]
        for spec in specs:
            try:
                path = infographic.render(spec)
            except infographic.Blocked as e:
                print("%s  %s BLOCKED: %s" % (d, spec.get("slug"), e)); bad += 1; continue
            os.makedirs(SITE_DIR, exist_ok=True)
            shutil.copy(path, SITE_DIR)
            rel = os.path.relpath(path, HERE)
            url = SITE_URL + os.path.basename(path)
            for it in q["items"]:
                if (it["platform"] in PLATFORMS and it["status"] == "pending"
                        and it["pillar"] == spec.get("pillar", it["pillar"])):
                    it["image"] = rel
                    it["image_url"] = url
            print("%s  %s -> %s" % (d, spec.get("pillar"), url))
        store.save_queue(d, q)
        print("%s  %s" % (d, rel))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
