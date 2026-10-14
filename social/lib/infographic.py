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
    parts = [spec.get("eyebrow", ""), plain(spec["headline"])]
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
    return "Honorbrook Insurance graphic. %s. %s" % (plain(spec["headline"]), body)


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


GOLD_DIM, CREAM, CARD, CARD_LINE = "#8a7020", "#f7f3e8", "#26385a", "#6f6130"
SERIF_I = ["/System/Library/Fonts/Supplemental/Georgia Italic.ttf"] + SERIF_B
TAGLINE = "The right coverage. The honest way."


def plain(t):
    return t.replace("*", "")


def _gradient():
    img = Image.new("RGB", (W * SS, H * SS), NAVY)
    d = ImageDraw.Draw(img)
    top, bot = (0x1f, 0x35, 0x58), (0x12, 0x20, 0x36)
    for y in range(H * SS):
        t = y / (H * SS)
        d.line([(0, y), (W * SS, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return img


def _frame(d):
    for inset, col in ((24, GOLD_DIM), (32, "#4d4220")):
        d.rectangle([inset * SS, inset * SS, (W - inset) * SS, (H - inset) * SS], outline=col, width=2 * SS)


def _shield(d, x, y, size):
    s = size
    pts = [(x, y), (x + s, y), (x + s, y + s * 0.62), (x + s / 2, y + s * 1.12), (x, y + s * 0.62)]
    d.polygon([(px * SS, py * SS) for px, py in pts], fill="#17304f", outline=GOLD, width=3 * SS)
    d.text(((x + s / 2) * SS, (y + s * 0.42) * SS), "H", font=_font(SERIF_B, int(s * 0.62)), fill=GOLD, anchor="mm")
    for k in (0.68, 0.8):
        yy = y + s * k
        d.line([((x + s * 0.28) * SS, yy * SS), ((x + s * 0.72) * SS, yy * SS)], fill=GOLD, width=2 * SS)


def _spaced(d, x, y, text, font, fill, spacing=4):
    for ch in text:
        d.text((x * SS, y * SS), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) / SS + spacing
    return x


def _rich(d, x, y, text, font, width, lh, cream=CREAM):
    """Draw headline with *gold* highlights, wrapped. Returns y after the last line."""
    words, gold = [], False
    for tok in text.split(" "):
        flag = gold
        if tok.startswith("*"):
            gold = True; flag = True
        if tok.endswith("*"):
            gold = False
        words.append((tok.strip("*"), flag))
    line, cx = [], 0.0
    sp = d.textlength(" ", font=font) / SS
    rows = []
    for w, g in words:
        wl = d.textlength(w, font=font) / SS
        if line and cx + wl > width:
            rows.append(line); line, cx = [], 0.0
        line.append((w, g)); cx += wl + sp
    rows.append(line)
    for row in rows[:3]:
        cx = x
        for w, g in row:
            d.text((cx * SS, y * SS), w, font=font, fill=GOLD if g else cream)
            cx += d.textlength(w, font=font) / SS + sp
        y += lh
    return y


def _footer(d, disc):
    top = H - 118
    if disc:
        df = _font(SANS, 17)
        fy = top - 62
        for ln in _wrap(d, disc, df, W - 150):
            d.text((75 * SS, fy * SS), ln, font=df, fill=MUTED); fy += 22
    d.rectangle([33 * SS, top * SS, (W - 33) * SS, (H - 33) * SS], fill="#0b1626")
    d.line([33 * SS, top * SS, (W - 33) * SS, top * SS], fill=GOLD_DIM, width=2 * SS)
    _spaced(d, 75, top + 20, "HONORBROOK INSURANCE", _font(SANS_B, 22), "white", 4)
    d.text((75 * SS, (top + 52) * SS), TAGLINE, font=_font(SERIF_I, 28), fill=GOLD)
    d.text(((W - 75) * SS, (top + 40) * SS), PHONE, font=_font(SERIF_B, 38), fill="white", anchor="ra")
    return top


def _header(d, spec):
    _shield(d, 72, 70, 92)
    x = 200
    if spec.get("eyebrow"):
        _spaced(d, x, 64, spec["eyebrow"].upper(), _font(SANS_B, 21), GOLD, 5)
    y = _rich(d, x, 98, spec["headline"], _font(SERIF_B, 52), W - x - 70, 62)
    d.line([75 * SS, (y + 14) * SS, 275 * SS, (y + 14) * SS], fill=GOLD, width=3 * SS)
    return y + 44


def _badge(d, cx, cy, r, kind, label, nf):
    d.ellipse([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS], fill=GOLD)
    if kind == "check":
        pts = [(cx - 14, cy), (cx - 4, cy + 11), (cx + 15, cy - 12)]
        d.line([(x * SS, y * SS) for x, y in pts], fill=NAVY, width=7 * SS, joint="curve")
    else:
        d.text((cx * SS, cy * SS), label, font=nf, fill=NAVY, anchor="mm")


def _card(d, x0, y0, x1, y1, text, kind, label, pf, nf):
    d.rounded_rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], 18 * SS, fill=CARD, outline=CARD_LINE, width=2 * SS)
    r = 26
    cy = (y0 + y1) // 2
    _badge(d, x0 + 26 + r, cy, r, kind, label, nf)
    tx = x0 + 26 + 2 * r + 24
    lines = _wrap(d, text, pf, x1 - 24 - tx)
    lh = pf.size // SS + 8
    if len(lines) * lh > (y1 - y0) - 14:
        raise Blocked("text too long for its card: %r" % text)
    ty = cy - len(lines) * lh // 2
    for ln in lines:
        d.text((tx * SS, ty * SS), ln, font=pf, fill=CREAM); ty += lh


def build_image(spec, reveal=None):
    """Draw the graphic. reveal=N shows only the first N cards (rows for compare);
    None shows all. Used for the video frames."""
    disc = vet(spec)
    lay = spec.get("layout", "steps")
    img = _gradient()
    d = ImageDraw.Draw(img)
    _frame(d)
    y = _header(d, spec)
    foot_top = _footer(d, disc)
    M = 75
    avail = foot_top - (62 if disc else 0) - y - 26
    nf = _font(SERIF_B, 30)
    gap = 16

    if lay == "compare":
        colw = (W - 2 * M - 30) // 2
        n = max(len(c["points"]) for c in _columns(spec))
        th = 56
        card_h = min(190, (avail - th - gap * (n - 1)) // n)
        pf = _font(SANS_B, 26)
        for ci, col in enumerate(_columns(spec)):
            x0 = M + ci * (colw + 30)
            d.text((x0 * SS, y * SS), plain(col["title"]), font=_font(SERIF_B, 34), fill=GOLD)
            cy0 = y + th
            for ri, p in enumerate(col["points"]):
                if reveal is not None and ri >= reveal:
                    break
                _card(d, x0, cy0, x0 + colw, cy0 + card_h, p, "check", "", pf, nf)
                cy0 += card_h + gap
    else:
        n = len(spec["points"])
        card_h = min(140, (avail - gap * (n - 1)) // n)
        pf = _font(SANS_B, 29 if card_h >= 100 else 25)
        for i, p in enumerate(spec["points"], 1):
            if reveal is not None and i > reveal:
                break
            _card(d, M, y, W - M, y + card_h, p,
                  "check" if lay == "checklist" else "num", str(i), pf, nf)
            y += card_h + gap
    return img.resize((W, H), Image.LANCZOS)


def end_card(spec):
    """Closing frame for videos: big call to action, disclaimer when required."""
    disc = vet(spec)
    img = _gradient()
    d = ImageDraw.Draw(img)
    _frame(d)
    _shield(d, 72, 120, 92)
    y = _rich(d, 200, 130, spec["headline"], _font(SERIF_B, 52), W - 270, 62)
    y = max(y, 280) + 20
    d.line([75 * SS, y * SS, 275 * SS, y * SS], fill=GOLD, width=3 * SS)
    d.text((75 * SS, (y + 40) * SS), "Call us. No cost, no obligation.", font=_font(SANS_B, 32), fill=MUTED)
    d.text((75 * SS, (y + 100) * SS), PHONE, font=_font(SERIF_B, 84), fill=GOLD)
    d.text((75 * SS, (y + 215) * SS), SITE, font=_font(SANS_B, 34), fill="white")
    _footer(d, disc)
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
