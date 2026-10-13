"""
Honorbrook infographic renderer (Pillow). 1200x900 PNG, brand colours.

Every word on the image is run through compliance.check() BEFORE drawing; a
spec that trips a BLOCK rule raises Blocked and no file is written. Medicare-topic
specs get the full CMS disclaimer printed in the footer automatically.

Spec (dict / JSON):
    {"slug": "ichra-allowance", "eyebrow": "ICHRA FOR EMPLOYERS",
     "headline": "How to set an ICHRA allowance",
     "points": ["Start with what you spend today", "..."],   # 2-5 items
     "footer": "optional override"}

CLI:  python3 lib/infographic.py spec.json [--out DIR]
"""
import json, os, sys, hashlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compliance
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 900
NAVY, GOLD, LIGHT, INK, MUTED = "#142339", "#c9a227", "#eef1f6", "#142339", "#aebbd0"
PHONE, SITE = "(571) 354-0146", "honorbrook-insurance.com"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "..", "social-assets", "infographics")
SANS = ["/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Helvetica.ttc"]
SANS_B = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc"]
SERIF_B = ["/System/Library/Fonts/Supplemental/Georgia Bold.ttf"] + SANS_B


class Blocked(Exception):
    pass


def _font(paths, size):
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def _wrap(d, text, font, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + ([cur] if cur else [])


def all_text(spec):
    parts = [spec.get("eyebrow", ""), spec["headline"]] + list(spec["points"])
    parts.append(spec.get("footer", "Honorbrook Insurance " + PHONE + " " + SITE))
    return "\n".join(p for p in parts if p)


def vet(spec):
    """Lint the on-image text. Returns the disclaimer to print ('' if none)."""
    if not 2 <= len(spec["points"]) <= 5:
        raise Blocked("points must be 2-5 items")
    text = all_text(spec)
    disc = ""
    if compliance.is_medicare_topic(text):
        disc = compliance.DISCLAIMER_LONG
        text += "\n" + disc
    res = compliance.check(text, "linkedin")
    if not res.ok:
        raise Blocked("; ".join("%s: %s" % b for b in res.blocks))
    return disc


def render(spec, out_dir=None):
    disc = vet(spec)
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    M = 70
    d.rectangle([0, 0, W, 14], fill=GOLD)

    y = 56
    if spec.get("eyebrow"):
        d.text((M, y), spec["eyebrow"].upper(), font=_font(SANS_B, 24), fill=GOLD)
        y += 50
    hf = _font(SERIF_B, 56)
    for ln in _wrap(d, spec["headline"], hf, W - 2 * M)[:3]:
        d.text((M, y), ln, font=hf, fill="white"); y += 68
    y += 18

    foot_h = 85 + (110 if disc else 0)
    avail = H - foot_h - y - 30
    n = len(spec["points"])
    gap = 18
    card_h = min(150, (avail - gap * (n - 1)) // n)
    pf = _font(SANS_B, 30 if card_h >= 110 else 26)
    for i, p in enumerate(spec["points"], 1):
        d.rounded_rectangle([M, y, W - M, y + card_h], 16, fill=LIGHT)
        r = 28
        cy = y + card_h // 2
        d.ellipse([M + 24, cy - r, M + 24 + 2 * r, cy + r], fill=GOLD)
        nf = _font(SANS_B, 32)
        d.text((M + 24 + r, cy), str(i), font=nf, fill=NAVY, anchor="mm")
        tx = M + 24 + 2 * r + 28
        lines = _wrap(d, p, pf, W - M - 30 - tx)
        lh = pf.size + 8
        if len(lines) * lh > card_h - 16:
            raise Blocked("point %d too long for its card: %r" % (i, p))
        ty = cy - len(lines) * lh // 2
        for ln in lines:
            d.text((tx, ty), ln, font=pf, fill=INK); ty += lh
        y += card_h + gap

    fy = H - foot_h + 10
    if disc:
        df = _font(SANS, 18)
        for ln in _wrap(d, disc, df, W - 2 * M):
            d.text((M, fy), ln, font=df, fill=MUTED); fy += 24
        fy += 8
    d.line([M, fy, W - M, fy], fill=GOLD, width=2)
    d.text((M, fy + 14), "Honorbrook Insurance", font=_font(SANS_B, 26), fill="white")
    d.text((W - M, fy + 16), spec.get("footer", PHONE + "  |  " + SITE),
           font=_font(SANS, 24), fill=MUTED, anchor="ra")

    out_dir = out_dir or os.path.abspath(OUT_DIR)
    os.makedirs(out_dir, exist_ok=True)
    digest = hashlib.sha256(all_text(spec).encode()).hexdigest()[:8]
    path = os.path.join(out_dir, "%s-%s.png" % (spec.get("slug", "infographic"), digest))
    img.save(path, optimize=True)
    return path


if __name__ == "__main__":
    args = sys.argv[1:]
    out = args[args.index("--out") + 1] if "--out" in args else None
    try:
        print(render(json.load(open(args[0])), out))
    except Blocked as e:
        print("BLOCKED:", e); sys.exit(1)
