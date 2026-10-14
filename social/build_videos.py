#!/usr/bin/env python3
"""
Render a short video from the day's infographic spec and attach it to the 13:00
X post as "video" (path relative to social/). Uses the same specs as
build_infographics.py; the spec must match the post's pillar. Compliance-vetted.

  python3 build_videos.py --from 2026-10-13 --days 6
"""
import argparse, datetime, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "lib"))
import infographic, store, video

SLOT = "13:00"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", required=True)
    ap.add_argument("--days", type=int, default=7)
    a = ap.parse_args()
    start = datetime.date.fromisoformat(a.start)
    for n in range(a.days):
        d = (start + datetime.timedelta(days=n)).isoformat()
        sp = os.path.join(HERE, "infographic-specs", d + ".json")
        q = store.load_queue(d)
        if not q or not os.path.exists(sp):
            print("%s  no queue or spec, skipped" % d); continue
        specs = json.load(open(sp))
        specs = specs if isinstance(specs, list) else [specs]
        targets = [i for i in q["items"] if i["platform"] == "x"
                   and i.get("slot") == SLOT and i["status"] == "pending"]
        for it in targets:
            spec = next((s for s in specs if s.get("pillar", it["pillar"]) == it["pillar"]), None)
            if not spec:
                continue
            try:
                path = video.render_video(spec)
            except infographic.Blocked as e:
                print("%s  BLOCKED: %s" % (d, e)); continue
            it["video"] = os.path.relpath(path, HERE)
            it["image_alt"] = infographic.alt_text(spec)
            print("%s  %s" % (d, it["video"]))
        store.save_queue(d, q)


if __name__ == "__main__":
    main()
