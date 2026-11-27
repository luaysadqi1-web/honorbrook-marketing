"""About Honorbrook Insurance: the home page video (for /index.html).
Facts only from the built pages staging/site-onyx/index.html, about.html and schedule-an-appointment.html (read Nov 27, 2026),
in their wording. No reviews, no ratings, no client names, no prices, no carrier names, no plan details.
Custom scenes in this file (built from the kit primitives): the opening with the HB mark, the line tiles, the tile map of
the 16 states and DC (same grid as the home page map), the 4 steps, and an end card that also carries the Medicare
disclaimer from the site footer, word for word.
"""
import math
from PIL import Image, ImageDraw
import video_life as K
from video_life import F, clamp, prog, eo3, eob, lerp, wrap, text, rrect, circle, glow, ring_line
P = K.P

HOME = 'https://honorbrook-insurance.com/'
ABOUT = 'https://honorbrook-insurance.com/about'
SCHED = 'https://honorbrook-insurance.com/schedule-an-appointment'
D_HOME = 'built page staging/site-onyx/index.html, read Nov 27, 2026'
D_ABOUT = 'built page staging/site-onyx/about.html, read Nov 27, 2026'
D_SCHED = 'page updated November 2026; read Nov 27, 2026'

# The Medicare disclaimer, copied word for word from the footer of index.html.
MEDICARE_DISCLAIMER = ('We do not offer every plan available in your area. Any information we provide is limited to those plans '
                       'we do offer in your area. Please contact Medicare.gov or 1-800-MEDICARE to get information on all of your options.')

# The home page tile map: (abbreviation, column, row), and the 17 licensed markets in the order the home page lists them.
GRID = [('AK', 1, 1), ('ME', 12, 1), ('WI', 7, 2), ('VT', 11, 2), ('NH', 12, 2), ('WA', 2, 3), ('ID', 3, 3), ('MT', 4, 3), ('ND', 5, 3),
        ('MN', 6, 3), ('IL', 7, 3), ('MI', 8, 3), ('NY', 10, 3), ('MA', 11, 3), ('OR', 2, 4), ('NV', 3, 4), ('WY', 4, 4), ('SD', 5, 4),
        ('IA', 6, 4), ('IN', 7, 4), ('OH', 8, 4), ('PA', 9, 4), ('NJ', 10, 4), ('CT', 11, 4), ('RI', 12, 4), ('CA', 2, 5), ('UT', 3, 5),
        ('CO', 4, 5), ('NE', 5, 5), ('MO', 6, 5), ('KY', 7, 5), ('WV', 8, 5), ('VA', 9, 5), ('MD', 10, 5), ('DE', 11, 5), ('AZ', 3, 6),
        ('NM', 4, 6), ('KS', 5, 6), ('AR', 6, 6), ('TN', 7, 6), ('NC', 8, 6), ('SC', 9, 6), ('DC', 10, 6), ('OK', 5, 7), ('LA', 6, 7),
        ('MS', 7, 7), ('AL', 8, 7), ('GA', 9, 7), ('HI', 1, 8), ('TX', 5, 8), ('FL', 10, 8)]
LICENSED = [('AL', 'Alabama'), ('DE', 'Delaware'), ('DC', 'Washington, DC'), ('FL', 'Florida'), ('GA', 'Georgia'), ('IN', 'Indiana'),
            ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('MD', 'Maryland'), ('MI', 'Michigan'), ('NC', 'North Carolina'),
            ('PA', 'Pennsylvania'), ('SC', 'South Carolina'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('VA', 'Virginia'),
            ('WV', 'West Virginia')]
assert len(LICENSED) == 17 and all(any(g[0] == ab for g in GRID) for ab, _ in LICENSED)

_MONO, _ML = {}, {}


def _mono(c, img, cx, cy, h, a):
    """The HB monogram, centred on (cx, cy), h pixels tall."""
    if not getattr(c, 'mono', None) or a <= 0.01: return
    h = int(h)
    if h not in _MONO:
        if len(_MONO) > 80: _MONO.clear()
        _MONO[h] = c.mono.resize((int(c.mono.width * h / c.mono.height), h), Image.LANCZOS)
    lg = _MONO[h]
    if a < 1:
        lg = lg.copy(); lg.putalpha(lg.getchannel('A').point(lambda v: int(v * a)))
    img.paste(lg, (int(cx - lg.width / 2), int(cy - h / 2)), lg)


def _foot(c, img, s, a):
    """A takeaway capsule at the bottom of the scene area. Returns the height it reserves."""
    if not s: return 0
    size = c.S(38, 26); h = K.pill(c, img, 0, s, 0, size=size)
    if a > 0.01: K.pill(c, img, c.bot - h / 2 - c.S(8, 4), s, a, size=size)
    return h + c.S(40, 20)


# ------------------------------------------------------------------ 1. opening: the mark, the title, a takeaway capsule
def intro(over, lines_land, lines_port, sub, sub_at=1):
    def draw(c, img, t, ph):
        L = lines_land if c.land else lines_port
        y0 = c.S(292, 90); K.kicker(img, c.cx, y0, over, F('Bold', c.S(31, 19)), eo3(prog(t, 0.0, 0.4)))
        y0 += c.S(70, 36); maxw = c.W * c.R(0.88, 0.84)
        for size in range(int(c.S(128, 84)), int(c.S(80, 52)) - 1, -2):
            f = F('Black', size)
            if all(f.getlength(ln) <= maxw for ln in L): break
        else: K.warn('intro headline is too long: %s' % ' '.join(L))
        mh = c.S(300, 142); g1 = c.S(54, 20); g2 = c.S(56, 24); bh = len(L) * int(size * 1.1)
        subh = K.pill(c, img, 0, sub, 0)
        block = mh + g1 + bh + g2 + subh; y = y0 + max(0, (c.bot - y0 - block) / 2)
        a = eo3(prog(t, 0.05, 0.7)); pulse = 0.85 + 0.15 * math.sin(t * 2.0); my = y + mh / 2
        glow(img, c.cx, my, mh * 1.9, K.ICE, 0.26 * a * pulse, 2.2)
        for k in range(2):
            q = ((t * 0.20) + k / 2) % 1.0
            ring_line(img, c.cx, my, lerp(mh * 0.62, mh * 1.75, q), c.S(3, 2), K.S2, (1 - q) * 0.20 * a)
        _mono(c, img, c.cx, my + (1 - a) * c.S(16, 8), mh * (0.90 + 0.10 * a), a)
        w = eo3(prog(t, 0.35, 0.7)) * c.S(210, 130); K.hair(img, c.cx - w, c.cx + w, y + mh + g1 * 0.5, a, base=0.40)
        K.headline(img, c.cx, y + mh + g1, L, size, t, 0.35, K.SILVER, 'Black', 1.1)
        ts = ph[min(sub_at, len(ph) - 1)][0]
        K.pill(c, img, y + mh + g1 + bh + g2 + subh / 2, sub, eo3(prog(t, ts, 0.5)))
    draw.texts = [over, ' '.join(lines_land), sub]
    return draw


# ------------------------------------------------------------------ 2. tiles: one panel per item (a row on 16:9, a grid on 9:16)
def tiles(over, head, items, start=0, at=None, note=None, note_at=1):
    """items: [(icon, label)]. icon is a kit glyph name or a short text. One tile per phrase (start / at as in K.checklist)."""
    items = list(items); n = len(items)

    def draw(c, img, t, ph):
        y0 = K.title(c, img, t, over, head); cu = K.cues(ph, n, start, at)
        y1 = c.bot - _foot(c, img, note, eo3(prog(t, ph[min(note_at, len(ph) - 1)][0], 0.5)))
        cols = n if c.land else 2; rows = int(math.ceil(n / cols)); gap = c.S(28, 22); cw = c.W * c.R(0.88, 0.86); x0 = c.cx - cw / 2
        w = (cw - (cols - 1) * gap) / cols; h = min((y1 - y0 - (rows - 1) * gap) / rows, c.S(330, 250))
        top = y0 + (y1 - y0 - (rows * h + (rows - 1) * gap)) / 2
        f = K.fit([l for _, l in items], 'Heavy', w - c.S(40, 24), h * 0.34, c.S(56, 36), c.S(38, 26), lh=1.15, what='tile label')
        cs = min(h * 0.42, c.S(132, 96)); g = c.S(32, 20)
        for i, (ic, lab) in enumerate(items):
            r_, q_ = divmod(i, cols); x = x0 + q_ * (w + gap); y = top + r_ * (h + gap) + 3 * math.sin(t * 1.3 + i) * c.k
            p = eo3(prog(t, cu[i][0] - 0.05, 0.45)); gh = eo3(prog(t, 0.3 + 0.08 * i, 0.5)) * (1 - p)
            if gh > 0.01: rrect(img, x, y, x + w, y + h, c.S(34, 20), K.WHITE, 0.10 * gh, outline=2)
            if p <= 0.004: continue
            oy = (1 - p) * c.S(50, 28); fl = clamp(1 - (t - cu[i][0]) / 1.2) * p
            if fl > 0.02: glow(img, x + w / 2, y + h * 0.42, w * 0.8, K.ICE, 0.22 * fl, 2.2)
            K.panel(img, x, y + oy, x + w, y + h + oy, c.S(34, 20), p)
            L = wrap(lab, f, w - c.S(40, 24)); th = len(L) * int(f.size * 1.15); cy0 = y + oy + (h - (cs + g + th)) / 2
            K.chip(img, x + w / 2, cy0 + cs / 2, cs, ic, p)
            for j, ln in enumerate(L): K.gtext(img, x + w / 2, cy0 + cs + g + j * int(f.size * 1.15), ln, f, K.SILVER, p, 'ma')
    draw.sfx = lambda ph: [(a + 0.05, 'tick') for a, b in K.cues(ph, n, start, at)]
    draw.texts = [over, head] + [l for _, l in items] + ([note] if note else [])
    return draw


# ------------------------------------------------------------------ 3. the tile map of the 16 states and DC, with the list
def _maplayer(cell):
    key = round(cell, 2)
    if key not in _ML:
        ss = 3; W_, H_ = int(cell * 12 * ss), int(cell * 8 * ss)
        fill = Image.new('L', (W_, H_), 0); out = Image.new('L', (W_, H_), 0); df, do = ImageDraw.Draw(fill), ImageDraw.Draw(out)
        for ab, col, row in GRID:
            g = cell * 0.07; box = [((col - 1) * cell + g) * ss, ((row - 1) * cell + g) * ss, (col * cell - g) * ss, (row * cell - g) * ss]
            df.rounded_rectangle(box, radius=cell * 0.2 * ss, fill=255)
            do.rounded_rectangle(box, radius=cell * 0.2 * ss, outline=255, width=max(2, int(cell * 0.04 * ss)))
        size = (int(cell * 12), int(cell * 8))
        _ML[key] = (fill.resize(size, Image.LANCZOS), out.resize(size, Image.LANCZOS))
    return _ML[key]


def states(over, head, phrase=0):
    """The home page tile map: every state as a quiet tile, the 17 licensed markets light up outward from Virginia, and the
    names fill in next to it in the order the home page lists them."""
    pos = {ab: (col, row) for ab, col, row in GRID}; vc, vr = pos['VA']
    order = sorted([ab for ab, _ in LICENSED], key=lambda ab: ((pos[ab][0] - vc) ** 2 + (pos[ab][1] - vr) ** 2, ab))
    rank = {ab: i for i, ab in enumerate(order)}

    def draw(c, img, t, ph):
        y0 = K.title(c, img, t, over, head); y1 = c.bot; H = y1 - y0; cw = c.W * 0.88; x0 = c.cx - cw / 2
        a0, b0 = ph[min(phrase, len(ph) - 1)]; span = max(b0 - a0 - 0.5, 2.0)
        when = lambda ab: a0 + 0.25 + span * rank[ab] / (len(order) - 1)
        if c.land:
            cell = min(H / 8, 44.0); mx, my = x0, y0 + (H - cell * 8) / 2
            ncol, nrow = 2, 9; lx = x0 + cell * 12 + 44; lw = (x0 + cw - lx) / ncol; rh = min(H / nrow, 37.0); ly = y0 + (H - rh * nrow) / 2
            fn = F('Semibold', 24)
        else:
            ncol, nrow = 3, 6; rh = 54.0; gap = 44; cell = min((H - rh * nrow - gap) / 8, cw / 12)
            mx = c.cx - cell * 6; my = y0 + (H - (cell * 8 + gap + rh * nrow)) / 2
            lx = x0 + 8; lw = (cw - 8) / ncol; ly = my + cell * 8 + gap; fn = F('Semibold', 33)
        mx, my = int(round(mx)), int(round(my)); e = eo3(prog(t, 0.15, 0.7))
        fill, out = _maplayer(cell)
        glow(img, mx + cell * 8.6, my + cell * 5.3, cell * 7, K.ICE, 0.16 * e * (0.85 + 0.15 * math.sin(t * 2.0)), 2.2)
        img.paste(K.OX5, (mx, my), fill.point(lambda v: int(v * 0.80 * e)))
        img.paste(K.WHITE, (mx, my), out.point(lambda v: int(v * 0.17 * e)))
        fa = F('Heavy', cell * 0.43); g = cell * 0.07
        for ab, _ in LICENSED:
            col, row = pos[ab]; ts = when(ab); p = clamp(eob(prog(t, ts, 0.45)))
            if p <= 0.01: continue
            bx, by = mx + (col - 1) * cell, my + (row - 1) * cell; ccx, ccy = bx + cell / 2, by + cell / 2
            fl = clamp(1 - (t - ts) / 0.9)
            if fl > 0.02: glow(img, ccx, ccy, cell * 1.5, K.ICE, 0.45 * fl, 2.2)
            K.gfill(img, bx + g, by + g, bx + cell - g, by + cell - g, cell * 0.2, K.BTN, p)
            text(img, ccx, ccy + 1, ab, fa, K.INK, p, 'mm')
        for i, (ab, name) in enumerate(LICENSED):
            col, row = divmod(i, nrow); q = eo3(prog(t, a0 + 0.25 + span * i / (len(LICENSED) - 1), 0.4)); x = lx + col * lw + (1 - q) * c.S(18, 10); y = ly + row * rh + rh / 2
            K.diamond(img, x + c.S(9, 6), y, c.S(7, 5), K.S2, q)
            text(img, x + c.S(32, 22), y, name, fn, K.S1, q, 'lm')
    draw.sfx = lambda ph: [(ph[min(phrase, len(ph) - 1)][0] + 0.3, 'ding')]
    draw.texts = [over, head] + [name for _, name in LICENSED]
    return draw


# ------------------------------------------------------------------ 4. the 4 steps
def steps(over, head, items, start=1, at=None, note=None, note_at=None):
    """Numbered steps joined by a line that fills as each step arrives (a row of cards on 16:9, a column on 9:16)."""
    items = list(items); n = len(items)

    def disc(img, c, cx, cy, r, num, p, early):
        circle(img, cx, cy, r, K.OX5, early); circle(img, cx, cy, r, K.S3, early * 0.9, outline=max(2, int(r * 0.09)))
        text(img, cx, cy + 1, num, F('Heavy', r * 1.05), K.S3, early * (1 - p), 'mm')
        if p > 0.02:
            glow(img, cx, cy, r * 3.0, K.ICE, 0.34 * p, 2.2); K.gfill(img, cx - r, cy - r, cx + r, cy + r, r, K.BTN, p)
            text(img, cx, cy + 1, num, F('Heavy', r * 1.05), K.INK, p, 'mm')

    def draw(c, img, t, ph):
        y0 = K.title(c, img, t, over, head); cu = K.cues(ph, n, start, at)
        nt = ph[min(note_at if note_at is not None else len(ph) - 1, len(ph) - 1)][0]
        y1 = c.bot - _foot(c, img, note, eo3(prog(t, nt, 0.5))); cw = c.W * c.R(0.88, 0.88); x0 = c.cx - cw / 2
        prg = sum(prog(t, cu[i][0], max(cu[i + 1][0] - cu[i][0], 0.3)) for i in range(n - 1)) / max(n - 1, 1)
        if c.land:
            gap = 20; w = (cw - (n - 1) * gap) / n; r = 27; top = y0 + r + 2; h = min(y1 - top - 4, 230); top += (y1 - top - 4 - h) / 2
            xs = [x0 + i * (w + gap) + w / 2 for i in range(n)]
            f = K.fit(items, 'Bold', w - 36, h - r - 34, 32, 23, lh=1.2, what='step label')
            K._rect(img, xs[0], top - 2, xs[-1], top + 2, K.S4, 0.55)
            if prg > 0.003: K._rect(img, xs[0], top - 2, xs[0] + (xs[-1] - xs[0]) * prg, top + 2, K.S1, 1.0)
            for i, lab in enumerate(items):
                x = xs[i] - w / 2; p = eo3(prog(t, cu[i][0] - 0.05, 0.45)); early = eo3(prog(t, 0.3 + 0.08 * i, 0.5)); oy = (1 - p) * 26
                if early * (1 - p) > 0.01: rrect(img, x, top, x + w, top + h, 20, K.WHITE, 0.10 * early * (1 - p), outline=2)
                if p > 0.004:
                    K.panel(img, x, top + oy, x + w, top + h + oy, 20, p)
                    L = wrap(lab, f, w - 36); cy = top + oy + r + (h - r) / 2
                    for j, ln in enumerate(L): text(img, xs[i], cy + (j - (len(L) - 1) / 2) * f.size * 1.2, ln, f, K.S1, p, 'mm')
                disc(img, c, xs[i], top, r, str(i + 1), clamp(eob(prog(t, cu[i][0], 0.45))), early)
        else:
            gap = 30; h = min(190, (y1 - y0 - (n - 1) * gap) / n); r = 46; pad = 40; top = y0 + (y1 - y0 - (n * h + (n - 1) * gap)) / 2
            ys = [top + i * (h + gap) + h / 2 for i in range(n)]; dx = x0 + pad + r; tx = dx + r + 38; tw = x0 + cw - pad - tx
            f = K.fit(items, 'Bold', tw, h - 30, 50, 36, lh=1.2, what='step label')
            K._rect(img, dx - 3, ys[0], dx + 3, ys[-1], K.S4, 0.55)
            if prg > 0.003: K._rect(img, dx - 3, ys[0], dx + 3, ys[0] + (ys[-1] - ys[0]) * prg, K.S1, 1.0)
            for i, lab in enumerate(items):
                y = ys[i] - h / 2; p = eo3(prog(t, cu[i][0] - 0.05, 0.45)); early = eo3(prog(t, 0.3 + 0.08 * i, 0.5)); sl = (1 - p) * 60
                if early * (1 - p) > 0.01: rrect(img, x0, y, x0 + cw, y + h, 34, K.WHITE, 0.10 * early * (1 - p), outline=2)
                if p > 0.004:
                    K.panel(img, x0 + sl, y, x0 + cw + sl, y + h, 34, p)
                    L = wrap(lab, f, tw)
                    for j, ln in enumerate(L): text(img, tx + sl, ys[i] + (j - (len(L) - 1) / 2) * f.size * 1.2, ln, f, K.S1, p, 'lm')
                disc(img, c, dx + sl * min(p * 50, 1), ys[i], r, str(i + 1), clamp(eob(prog(t, cu[i][0], 0.45))), early)
    draw.sfx = lambda ph: [(a + 0.05, 'ding') for a, b in K.cues(ph, n, start, at)]
    draw.texts = [over, head] + items + ([note] if note else [])
    return draw


# ------------------------------------------------------------------ 5. end card: the kit end card plus the Medicare disclaimer
def end_medicare(question=K.END_QUESTION):
    """Same card as K.end (lockup, soft next step, site, chrome Call button, Text line, kit disclaimer), laid out a little
    tighter so the Medicare disclaimer from the site footer sits under the kit disclaimer for the whole scene."""
    def draw(c, img, t, ph):
        a = eo3(prog(t, 0.0, 0.5)); t1 = ph[min(1, len(ph) - 1)][0]; b = eo3(prog(t, t1 - 0.1, 0.5)); d = eo3(prog(t, t1 + 0.5, 0.5)); e = eo3(prog(t, 0.5, 0.6))

        def lock(cx, y, hgt):
            if not c.lockup: return
            lg = c.lockup.resize((int(c.lockup.width * hgt / c.lockup.height), int(hgt)), Image.LANCZOS)
            if a < 1: lg.putalpha(lg.getchannel('A').point(lambda v: int(v * a)))
            glow(img, cx, y + hgt * 0.42, hgt * 1.25, K.ICE, 0.12 * a, 2.2); img.paste(lg, (int(cx - lg.width / 2), int(y)), lg)

        def contact(cx, y, w):
            K.kicker(img, cx, y, 'Schedule a time', F('Bold', c.S(29, 18)), b); y += c.S(50, 29)
            fw = K.fit([K.SITE], 'Bold', w, 200, c.S(60, 40), c.S(44, 30), lh=1.0)
            K.gtext(img, cx, y, K.SITE, fw, K.SILVER, b, 'ma'); y += fw.size + c.S(38, 20)
            bh = c.S(134, 76); bw = min(w, c.S(860, 520)); pulse = 0.85 + 0.15 * math.sin(t * 3)
            glow(img, cx, y + bh / 2, bw * 0.72, K.ICE, 0.22 * d * pulse, 2.2)
            K.gfill(img, cx - bw / 2, y, cx + bw / 2, y + bh, c.S(34, 19), K.BTN, d)
            text(img, cx, y + bh / 2 + 1, 'Call ' + K.CALL, F('Heavy', c.S(70, 41)), K.INK, d, 'mm'); y += bh + c.S(28, 16)
            text(img, cx, y, 'Text ' + K.TEXT, F('Semibold', c.S(50, 31)), K.S1, d, 'ma')

        fd = F('Regular', c.S(32, 21)); dw = c.W * c.R(0.88, 0.88); lh = int(fd.size * 1.34); pg = c.S(14, 8)
        d1, d2 = wrap(K.DISCLAIMER, fd, dw), wrap(MEDICARE_DISCLAIMER, fd, dw); dh = (len(d1) + len(d2)) * lh + pg; dy = c.bot - dh
        if c.land:
            lx, rx = c.W * 0.27, c.W * 0.70; top = 84
            lock(lx, top + 2, 150)
            fq = K.fit([question], 'Heavy', c.W * 0.40, 130, 44, 32, lh=1.1)
            K.headline(img, lx, top + 166, wrap(question, fq, c.W * 0.40), fq.size, t, 0.1)
            K._rect(img, c.W * 0.49 - 1, top + 14, c.W * 0.49 + 1, dy - 26, K.WHITE, 0.14 * a)
            contact(rx, top + 12, c.W * 0.40)
        else:
            lock(c.cx, 200, 226)
            fq = K.fit([question], 'Heavy', c.W * 0.88, 200, 78, 56, lh=1.1)
            y = K.headline(img, c.cx, 452, wrap(question, fq, c.W * 0.88), fq.size, t, 0.1) + 40
            contact(c.cx, y, c.W * 0.86)
        K.hair(img, c.cx - dw / 2, c.cx + dw / 2, dy - c.S(18, 11), e, base=0.18)
        y = K.lines_block(img, c.cx, dy, K.DISCLAIMER, fd, K.S2, dw, e, 1.34)
        K.lines_block(img, c.cx, y + pg, MEDICARE_DISCLAIMER, fd, K.S2, dw, e, 1.34)
    draw.is_end = True
    draw.texts = [question, 'Call ' + K.CALL, 'Text ' + K.TEXT, K.SITE, K.DISCLAIMER, MEDICARE_DISCLAIMER]
    return draw


def end_scene_medicare():
    phr = [(K.END_QUESTION, K.END_QUESTION), K.END_PHR[1]]
    return K.scene(end_medicare(), phr, sfx=lambda ph: [(ph[min(1, len(ph) - 1)][0] + 0.55, 'ding')], pre=0.1, post=2.4)


VIDEO = dict(
    title='About Honorbrook Insurance',
    description=('Honorbrook Insurance is an independent, licensed agency in Virginia. Who we are, what independent means, '
                 'what we help with, where we are licensed, the languages we speak and how scheduling works in 4 steps.'),
    poster=3.2,
    disclaimer=K.DISCLAIMER + ' ' + MEDICARE_DISCLAIMER,
    sources=[
        dict(fact="We're an independent, licensed agency in Virginia. Our office is at 8609 Westwood Center Dr, Suite 110, Tysons, VA 22182. "
                  'Your licensed agent is Luay Sadqi, NPN 21370662.', url=ABOUT, date=D_ABOUT),
        dict(fact='Independent: we represent you, not one carrier. One independent agent who compares 90+ carriers and explains '
                  'your options in plain English.', url=HOME, date=D_HOME),
        dict(fact='Medicare, health, life and retirement. Honorbrook helps individuals, families, and employers.', url=HOME, date=D_HOME),
        dict(fact='Now licensed in 16 states and Washington, DC: Alabama, Delaware, Washington, DC, Florida, Georgia, Indiana, Kentucky, '
                  'Louisiana, Maryland, Michigan, North Carolina, Pennsylvania, South Carolina, Tennessee, Texas, Virginia, West Virginia. '
                  'Plans and rules differ by state and county, so we start with your ZIP code.', url=HOME, date=D_HOME),
        dict(fact='Help in English, Arabic, French and Spanish.', url=HOME, date=D_HOME),
        dict(fact='Four steps: select Schedule an appointment (open Luay\'s page), create your profile, add your details '
                  '(doctors, prescriptions, pharmacy and current coverage), ask for your meeting. We read everything before we talk.',
             url=HOME, date=D_HOME),
        dict(fact='Office visits are by appointment in Tysons, Virginia. Everywhere else, we work by phone or video.', url=HOME, date=D_HOME),
        dict(fact='Carriers pay us, and your premium is the same either way.', url=HOME, date=D_HOME),
        dict(fact='Creating a profile does not enroll you in anything. Choosing a plan is a separate step, and it is your decision.',
             url=SCHED, date=D_SCHED),
        dict(fact='End card, Medicare disclaimer copied word for word from the footer of the home page: ' + MEDICARE_DISCLAIMER,
             url=HOME, date=D_HOME),
    ],
    scenes=[
        # 1. Hook: the mark and the title
        K.scene(intro('Independent insurance agency', ['About Honorbrook Insurance'], ['About Honorbrook', 'Insurance'],
                      'Who we are, what we help with, and how we work with you'),
                [P('About Honorbrook Insurance.'),
                 P('Who we are, what we help with, and how we work with you.')], pre=0.1, post=0.6),
        # 2. Who we are
        K.scene(K.fact_card('Who we are', 'Independent, licensed agency',
                            ['Office in Tysons, Virginia', 'Licensed agent: Luay Sadqi', 'NPN 21370662'], at=[1, 2, 2]),
                [P('Honorbrook Insurance is an independent, licensed agency in Virginia.'),
                 P('Our office is in Tysons.'),
                 P('Your licensed agent is Luay Sadqi.', 'Your licensed agent is Loo-eye Sodkee.')]),
        # 3. What independent means
        K.scene(K.checklist('What independent means', 'We work for you',
                            ['We represent you, not one carrier', 'One agent compares 90+ carriers',
                             'Your options, explained in plain English'], start=0, icons=['person', 'scale', 'chat']),
                [P('Independent means we represent you, not one carrier.'),
                 P('One agent compares 90+ carriers,', 'One agent compares ninety plus carriers,'),
                 P('and explains your options in plain English.')]),
        # 4. What we help with
        K.scene(tiles('What we help with', 'Coverage we help with',
                      [('cross', 'Medicare'), ('heart', 'Health'), ('umbrella', 'Life'), ('clock', 'Retirement')], at=[0, 0, 0, 0],
                      note='For individuals, families and employers.'),
                [P('We help with Medicare, health, life and retirement,'),
                 P('for individuals, families and employers.')]),
        # 5. Where we are licensed
        K.scene(states('Where we are licensed', '16 states and Washington, DC'),
                [P('We are licensed in 16 states and Washington, DC.', 'We are licensed in sixteen states, and Washington, D C.'),
                 P('Plans and rules differ by state and county, so we start with your ZIP code.',
                   'Plans and rules differ by state and county, so we start with your zip code.')]),
        # 6. Languages
        K.scene(tiles('Languages', 'Help in 4 languages',
                      [('EN', 'English'), ('AR', 'Arabic'), ('FR', 'French'), ('ES', 'Spanish')], at=[0, 0, 0, 0]),
                [P('We help in English, Arabic, French and Spanish.')]),
        # 7. How scheduling works
        K.scene(steps('How scheduling works', 'Four steps',
                      ['Select Schedule an appointment', 'Create your profile', 'Add your details', 'Ask for your meeting'],
                      start=1, note='We read everything before we talk.', note_at=5),
                [P('Scheduling takes 4 steps.', 'Scheduling takes four steps.'),
                 P('Select Schedule an appointment.'),
                 P('Create your profile.'),
                 P('Add your doctors, prescriptions and current coverage.'),
                 P('Then ask for your meeting.'),
                 P('We read everything before we talk.')]),
        # 8. How we work with you
        K.scene(K.checklist('Working together', 'How we work with you',
                            ['Office visits by appointment in Tysons, Virginia', 'Everywhere else, by phone or video',
                             'Carriers pay us. Your premium is the same either way', 'Choosing a plan is your decision'],
                            start=0, mark_kind=None, icons=['pin', 'chat', 'doc', 'check']),
                [P('Office visits are by appointment in Tysons, Virginia.'),
                 P('Everywhere else, we work by phone or video.'),
                 P('Carriers pay us, and your premium is the same either way.'),
                 P('Choosing a plan is your decision.')]),
        end_scene_medicare(),
    ])
