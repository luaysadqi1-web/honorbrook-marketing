#!/usr/bin/env python3
"""
Free, no-API posting helper. Builds one HTML page for a day with every post's
text, a Copy button, the image or video to attach, and a link to open each
platform's composer. Posting by hand takes a few minutes and costs nothing.

  python3 daily_packet.py [--date YYYY-MM-DD] [--open]

Writes social/packets/YYYY-MM-DD.html. Includes items that are pending or
manual; posted items are shown as done.
"""
import argparse, html, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "lib"))
import store

COMPOSE = {
    "x": ("X", "https://x.com/compose/post"),
    "linkedin": ("LinkedIn", "https://www.linkedin.com/company/"),
    "gbp": ("Google Business Profile", "https://business.google.com/"),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None)
    ap.add_argument("--open", action="store_true")
    a = ap.parse_args()
    store.load_dotenv()
    d = a.date or store.today_str()
    q = store.load_queue(d)
    if not q:
        print("no queue for", d); return 1
    org = os.environ.get("LINKEDIN_ORG_ID", "").strip()
    cards = []
    for it in sorted(q["items"], key=lambda i: (i.get("slot", "00:00"), i["platform"])):
        name, url = COMPOSE.get(it["platform"], (it["platform"], "#"))
        if it["platform"] == "linkedin" and org:
            url = "https://www.linkedin.com/company/%s/admin/" % org
        media = ""
        for key, kind in (("video", "Video"), ("image", "Image")):
            if it.get(key):
                path = os.path.abspath(os.path.join(HERE, it[key]))
                media = '<p class="m">%s to attach: <code>%s</code></p>' % (kind, html.escape(path))
                break
        done = it["status"] == "posted"
        cards.append(
            '<section class="%s"><h2>%s <small>%s %s</small></h2>%s'
            '<textarea readonly rows="%d" id="t%s">%s</textarea>'
            '<p><button onclick="navigator.clipboard.writeText(document.getElementById(\'t%s\').value);this.textContent=\'Copied\'">Copy text</button> '
            '<a href="%s" target="_blank">Open %s</a>%s</p></section>'
            % ("done" if done else "", name, html.escape(it.get("slot", "")),
               "(posted)" if done else "", media,
               min(14, 3 + len(it["text"]) // 70), it["id"], html.escape(it["text"]),
               it["id"], url, name,
               ' &middot; GBP button: <b>Call</b>' if it.get("cta") == "CALL" else ""))
    page = ("<!doctype html><meta charset=utf-8><title>Honorbrook posts %s</title>"
            "<style>body{font:16px system-ui;max-width:760px;margin:24px auto;padding:0 16px;background:#eef1f6;color:#142339}"
            "section{background:#fff;border-radius:12px;padding:14px 18px;margin:14px 0}section.done{opacity:.5}"
            "h2{margin:0 0 6px;font-size:18px}small{color:#667}textarea{width:100%%;box-sizing:border-box;font:15px system-ui}"
            "button{background:#142339;color:#fff;border:0;border-radius:8px;padding:8px 14px;cursor:pointer}"
            "a{color:#8a6d00}.m{font-size:14px;margin:4px 0}code{word-break:break-all}</style>"
            "<h1>Posts for %s</h1>%s" % (d, d, "".join(cards)))
    os.makedirs(os.path.join(HERE, "packets"), exist_ok=True)
    out = os.path.join(HERE, "packets", d + ".html")
    open(out, "w").write(page)
    print(out)
    if a.open:
        subprocess.run(["open", out])
    return 0


if __name__ == "__main__":
    sys.exit(main())
