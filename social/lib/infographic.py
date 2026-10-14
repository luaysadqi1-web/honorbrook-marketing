"""
Honorbrook infographic renderer (Pillow). 1200x900 PNG, brand colours,
drawn at 2x and downsampled so edges are smooth.

Every word on the image is run through compliance.check() BEFORE drawing; a
spec that trips a BLOCK rule raises Blocked and no file is written. Medicare-topic
specs get the full CMS disclaimer printed in the footer automatically.

Layouts (spec["layout"], default "steps"):
  steps      numbered cards, 2-5 points           {"points": [...]}
  checklist  tick-mark cards, 2-5 points          {"points": [...]}
  compare    two columns, 2-4 points each         {"left": {"title","points"}, "right": {...}}

Common keys: slug, eyebrow, headline, footer (optional override).
render() returns the PNG path; alt_text(spec) returns screen-reader text.

CLI:  python3 lib/infographic.py spec.json [--out DIR]
"""
import json, os, sys, hashlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compliance
from PIL import Image, ImageDraw, ImageFont

W, H, SS = 1200, 900, 2
NAVY, NAVY2, GOLD, LIGHT, INK, MUTED = "#142339", "#1c3250", "#c9a227", "#eef1f6", "#142339", "#aebbd0"
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
            return ImageFont.truetype(p, size * SS)
    return ImageFont.load_default()


def _wrap(d, text, font, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width * SS:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + ([cur] if cur else [])


def _columns(spec):
    return [spec["left"], spec["right"]]


def _points(spec):
    if spec.get("layout") == "compare":
        return [p for c in _columns(spec) for p in c["points"]]
    return list(spec["points"])


def all_text(spec):
    parts = [spec.get("eyebrow", ""), spec["headline"]]
    if spec.get("layout") == "compare":
        parts += [c["title"] for c in _columns(spec)]
    parts += _points(spec)
    parts.append(spec.get("footer", "Honorbrook Insurance " + PHONE + " " + SITE))
    return "\n".join(p for p in parts if p)


def alt_text(spec):
    if spec.get("layout") == "compare":
        body = " ".join("%s: %s." % (c["title"], "; ".join(c["points"])) for c in _columns(spec))
    else:
        body = "; ".join(spec["points"]) + "."
    return "Honorbrook Insurance graphic. %s. %s" % (spec["headline"], body)


def vet(spec):
    """Lint the on-image text. Returns the disclaimer to print ('' if none)."""
    lay = spec.get("layout", "steps")
    if lay not in ("steps", "checklist", "compare"):
        raise Blocked("unknown layout %r" % lay)
    if lay == "compare":
        if not all(2 <= len(c["points"]) <= 4 for c in _columns(spec)):
            raise Blocked("compare columns need 2-4 points each")
    elif not 2 <= len(spec["points"]) <= 5:
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


def _badge(d, cx, cy, r, kind, label, nf):
    d.ellipse([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS], fill=GOLD)
    if kind == "check":
        pts = [(cx - 14, cy), (cx - 4, cy + 11), (cx + 15, cy - 12)]
        d.line([(x * SS, y * SS) for x, y in pts], fill=NAVY, width=7 * SS, joint="curve")
    else:
        d.text((cx * SS, cy * SS), label, font=nf, fill=NAVY, anchor="mm")


def _card(d, x0, y0, x1, y1, text, kind, label, pf, nf):
    d.rounded_rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], 16 * SS, fill=LIGHT)
    r = 28
    cy = (y0 + y1) // 2
    _badge(d, x0 + 24 + r, cy, r, kind, label, nf)
    tx = x0 + 24 + 2 * r + 24
    lines = _wrap(d, text, pf, x1 - 24 - tx)
    lh = pf.size // SS + 8
    if len(lines) * lh > (y1 - y0) - 16:
        raise Blocked("text too long for its card: %r" % text)
    ty = cy - len(lines) * lh // 2
    for ln in lines:
        d.text((tx * SS, ty * SS), ln, font=pf, fill=INK); ty += lh


def build_image(spec, reveal=None):
    """Draw the graphic. reveal=N shows only the first N cards (rows for compare);
    None shows all. Used for the video frames."""
    disc = vet(spec)
    lay = spec.get("layout", "steps")
    img = Image.new("RGB", (W * SS, H * SS), NAVY)
    d = ImageDraw.Draw(img)
    # quiet decorative arc, top right
    d.ellipse([(W - 260) * SS, -200 * SS, (W + 200) * SS, 260 * SS], fill=NAVY2)
    d.rectangle([0, 0, W * SS, 14 * SS], fill=GOLD)
    M = 70

    y = 56
    if spec.get("eyebrow"):
        d.text((M * SS, y * SS), spec["eyebrow"].upper(), font=_font(SANS_B, 24), fill=GOLD)
        y += 50
    hf = _font(SERIF_B, 56)
    for ln in _wrap(d, spec["headline"], hf, W - 2 * M - 60)[:3]:
        d.text((M * SS, y * SS), ln, font=hf, fill="white"); y += 68
    y += 18

    foot_h = 85 + (110 if disc else 0)
    avail = H - foot_h - y - 30
    nf = _font(SANS_B, 32)
    gap = 18

    if lay == "compare":
        colw = (W - 2 * M - 30) // 2
        n = max(len(c["points"]) for c in _columns(spec))
        th = 60
        card_h = min(200, (avail - th - gap * (n - 1)) // n)
        pf = _font(SANS_B, 26)
        for ci, col in enumerate(_columns(spec)):
            x0 = M + ci * (colw + 30)
            d.text((x0 * SS, y * SS), col["title"], font=_font(SERIF_B, 34), fill=GOLD)
            cy0 = y + th
            for ri, p in enumerate(col["points"]):
                if reveal is not None and ri >= reveal:
                    break
                _card(d, x0, cy0, x0 + colw, cy0 + card_h, p, "check", "", pf, nf)
                cy0 += card_h + gap
    else:
        n = len(spec["points"])
        card_h = min(150, (avail - gap * (n - 1)) // n)
        pf = _font(SANS_B, 30 if card_h >= 110 else 26)
        for i, p in enumerate(spec["points"], 1):
            if reveal is not None and i > reveal:
                break
            _card(d, M, y, W - M, y + card_h, p,
                  "check" if lay == "checklist" else "num", str(i), pf, nf)
            y += card_h + gap

    fy = H - foot_h + 10
    if disc:
        df = _font(SANS, 18)
        for ln in _wrap(d, disc, df, W - 2 * M):
            d.text((M * SS, fy * SS), ln, font=df, fill=MUTED); fy += 24
        fy += 8
    d.line([M * SS, fy * SS, (W - M) * SS, fy * SS], fill=GOLD, width=2 * SS)
    d.text((M * SS, (fy + 14) * SS), "Honorbrook Insurance", font=_font(SANS_B, 26), fill="white")
    d.text(((W - M) * SS, (fy + 16) * SS), spec.get("footer", PHONE + "  |  " + SITE),
           font=_font(SANS, 24), fill=MUTED, anchor="ra")

    return img.resize((W, H), Image.LANCZOS)


def n_cards(spec):
    if spec.get("layout") == "compare":
        return max(len(c["points"]) for c in _columns(spec))
    return len(spec["points"])


def render(spec, out_dir=None):
    img = build_image(spec)
    lay = spec.get("layout", "steps")
    out_dir = out_dir or os.path.abspath(OUT_DIR)
    os.makedirs(out_dir, exist_ok=True)
    digest = hashlib.sha256((lay + all_text(spec)).encode()).hexdigest()[:8]
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
