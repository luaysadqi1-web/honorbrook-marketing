#!/usr/bin/env python3
"""Honorbrook video studio: animated, hook-first explainers rendered locally on macOS (PIL + numpy + `say` + Swift/AVFoundation).

Each video is a list of scenes with bespoke animated graphics (counters, timelines, bar charts, checklists) driven by the
narration timing, with burned-in word-highlight captions, a quiet music bed and soft UI sounds. Renders a 16:9 file for the
website and a 9:16 master for Shorts / Reels / Facebook.

  python3 scripts/video_studio.py list
  python3 scripts/video_studio.py still part-d 3.0 land     # writes a PNG to the scratch dir for review
  python3 scripts/video_studio.py build part-d              # land -> site/assets/video, port -> social/video_masters
  python3 scripts/video_studio.py build part-d --only land

Facts on screen (all read on the official page this session, 2026-10-14):
  Part D: medicare.gov late enrollment penalty page (63 days after the Initial Enrollment Period; 1% x $38.99 base premium
          (2026) x full uncovered months, rounded to the nearest $.10; lasts as long as you have Medicare drug coverage;
          Extra Help = no penalty).
  ACA:    healthcare.gov dates-and-deadlines (Nov 1; Dec 15 for Jan 1 coverage) and plan categories (60/70/80/90 on average,
          categories say nothing about quality; extra savings only on Silver). Jan 15 / Virginia Jan 29 from scripts/aca_data.
No plan names, no benefits, no enroll-now language (CMS marketing rules): educational only.
"""
import os, sys, json, math, subprocess, tempfile, shutil, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = os.environ.get('VIDEO_SCRATCH', os.path.join(tempfile.gettempdir(), 'hbvideo'))
FPS = 30
NAVY, NAVY2, GOLD, GOLDL = (20, 35, 57), (30, 52, 82), (201, 162, 39), (236, 205, 105)
CREAM, WHITE, SOFT = (250, 247, 240), (255, 255, 255), (166, 182, 204)
CORAL, GREEN, PANEL = (232, 116, 86), (108, 196, 150), (38, 62, 96)
SERIF, AVENIR = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf', '/System/Library/Fonts/Avenir Next.ttc'
LOGO = os.path.join(ROOT, 'site', 'assets', 'logo-static.png')
_F = {}


def F(kind, size):
    k = (kind, int(size))
    if k not in _F:
        idx = {'bold': 2, 'reg': 7, 'med': 5, 'heavy': 8}.get(kind)
        _F[k] = ImageFont.truetype(SERIF, int(size)) if kind == 'serif' else ImageFont.truetype(AVENIR, int(size), index=idx)
    return _F[k]


# ------------------------------------------------------------------ easing and drawing helpers
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, t0, d): return clamp((t - t0) / d) if d > 0 else (1.0 if t >= t0 else 0.0)
def eo3(x): return 1 - (1 - x) ** 3
def eio(x): return 3 * x * x - 2 * x ** 3
def eob(x):
    s = 1.70158; x -= 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2
def lerp(a, b, x): return a + (b - a) * x
def mix(c1, c2, x): return tuple(int(lerp(a, b, x)) for a, b in zip(c1, c2))


def text(img, x, y, s, f, fill, a=1.0, anchor='la'):
    if a <= 0.004 or not s: return
    l, t, r, b = f.getbbox(s, anchor=anchor)
    pad = 3
    m = Image.new('L', (r - l + 2 * pad, b - t + 2 * pad), 0)
    ImageDraw.Draw(m).text((-l + pad, -t + pad), s, font=f, fill=255, anchor=anchor)
    if a < 1: m = m.point(lambda v: int(v * a))
    img.paste(fill, (int(round(x + l - pad)), int(round(y + t - pad))), m)


def shape(img, box, color, a, drawer, ss=1):
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    w, h = x1 - x0, y1 - y0
    if w <= 0 or h <= 0 or a <= 0.004: return
    m = Image.new('L', (w * ss, h * ss), 0)
    drawer(ImageDraw.Draw(m), ss, w, h)
    if ss > 1: m = m.resize((w, h), Image.LANCZOS)
    if a < 1: m = m.point(lambda v: int(v * a))
    img.paste(color, (x0, y0), m)


def rrect(img, x0, y0, x1, y1, r, color, a=1.0, outline=0):
    def d(dr, ss, w, h):
        if outline: dr.rounded_rectangle([0, 0, w * ss - 1, h * ss - 1], radius=r * ss, outline=255, width=outline * ss)
        else: dr.rounded_rectangle([0, 0, w * ss - 1, h * ss - 1], radius=r * ss, fill=255)
    shape(img, (x0, y0, x1, y1), color, a, d, ss=2 if r > 5 else 1)


def circle(img, cx, cy, r, color, a=1.0, outline=0):
    def d(dr, ss, w, h):
        if outline: dr.ellipse([0, 0, w * ss - 1, h * ss - 1], outline=255, width=outline * ss)
        else: dr.ellipse([0, 0, w * ss - 1, h * ss - 1], fill=255)
    shape(img, (cx - r, cy - r, cx + r, cy + r), color, a, d, ss=3)


def wrap(s, f, maxw):
    lines, cur = [], ''
    for w in s.split():
        t = (cur + ' ' + w).strip()
        if f.getlength(t) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


def para(img, cx, y, s, f, fill, maxw, a=1.0, lh=1.25, align='center'):
    for ln in wrap(s, f, maxw):
        if align == 'center': text(img, cx, y, ln, f, fill, a, 'ma')
        else: text(img, cx, y, ln, f, fill, a, 'la')
        y += int(f.size * lh)
    return y


def check(img, cx, cy, r, p, color=GREEN):
    """Circle that pops in, with a check mark that draws itself."""
    if p <= 0: return
    rr = r * eob(clamp(p / 0.5)) if p < 0.5 else r
    circle(img, cx, cy, rr, color, 1.0)
    q = clamp((p - 0.35) / 0.5)
    if q > 0:
        pts = [(cx - r * 0.42, cy + r * 0.02), (cx - r * 0.1, cy + r * 0.36), (cx + r * 0.46, cy - r * 0.3)]
        seg = [pts[0], pts[1]] if q < 0.5 else [pts[0], pts[1], (lerp(pts[1][0], pts[2][0], (q - 0.5) / 0.5), lerp(pts[1][1], pts[2][1], (q - 0.5) / 0.5))]
        if q < 0.5: seg = [pts[0], (lerp(pts[0][0], pts[1][0], q / 0.5), lerp(pts[0][1], pts[1][1], q / 0.5))]
        shape(img, (cx - r, cy - r, cx + r, cy + r), NAVY, 1.0,
              lambda d, ss, w, h: d.line([((x - (cx - r)) * ss, (y - (cy - r)) * ss) for x, y in seg], fill=255, width=int(r * 0.2 * ss), joint='curve'), ss=3)


# icons: drawn in a square box of size s
def icon(img, kind, x, y, s, color, a=1.0):
    def d(dr, ss, w, h):
        u = w * ss / 100.0
        if kind == 'calendar':
            dr.rounded_rectangle([10 * u, 18 * u, 90 * u, 90 * u], radius=9 * u, outline=255, width=int(6 * u))
            dr.rectangle([10 * u, 18 * u, 90 * u, 38 * u], fill=255)
            dr.rounded_rectangle([28 * u, 6 * u, 36 * u, 28 * u], radius=3 * u, fill=255); dr.rounded_rectangle([64 * u, 6 * u, 72 * u, 28 * u], radius=3 * u, fill=255)
            for i in range(3):
                for j in range(2): dr.rectangle([(24 + i * 22) * u, (50 + j * 18) * u, (34 + i * 22) * u, (58 + j * 18) * u], fill=255)
        elif kind == 'doc':
            dr.polygon([(22 * u, 8 * u), (62 * u, 8 * u), (80 * u, 26 * u), (80 * u, 92 * u), (22 * u, 92 * u)], outline=255, width=int(6 * u))
            for i in range(3): dr.rounded_rectangle([34 * u, (44 + i * 15) * u, 68 * u, (50 + i * 15) * u], radius=3 * u, fill=255)
        elif kind == 'shield':
            dr.polygon([(50 * u, 6 * u), (88 * u, 20 * u), (84 * u, 58 * u), (50 * u, 94 * u), (16 * u, 58 * u), (12 * u, 20 * u)], outline=255, width=int(6 * u))
        elif kind == 'heart':
            dr.ellipse([12 * u, 16 * u, 52 * u, 56 * u], fill=255); dr.ellipse([48 * u, 16 * u, 88 * u, 56 * u], fill=255)
            dr.polygon([(15 * u, 46 * u), (85 * u, 46 * u), (50 * u, 88 * u)], fill=255)
        elif kind == 'cross':
            dr.rounded_rectangle([38 * u, 10 * u, 62 * u, 90 * u], radius=5 * u, fill=255); dr.rounded_rectangle([10 * u, 38 * u, 90 * u, 62 * u], radius=5 * u, fill=255)
        elif kind == 'pill':
            dr.rounded_rectangle([8 * u, 30 * u, 92 * u, 70 * u], radius=20 * u, outline=255, width=int(6 * u))
            dr.line([(50 * u, 30 * u), (50 * u, 70 * u)], fill=255, width=int(6 * u))
            dr.rounded_rectangle([14 * u, 36 * u, 48 * u, 64 * u], radius=14 * u, fill=255)
        elif kind == 'pin':
            dr.ellipse([22 * u, 8 * u, 78 * u, 64 * u], outline=255, width=int(7 * u))
            dr.polygon([(30 * u, 56 * u), (70 * u, 56 * u), (50 * u, 92 * u)], fill=255)
            dr.ellipse([40 * u, 26 * u, 60 * u, 46 * u], fill=255)
        elif kind == 'flag':
            dr.line([(26 * u, 10 * u), (26 * u, 92 * u)], fill=255, width=int(7 * u))
            dr.polygon([(26 * u, 12 * u), (84 * u, 24 * u), (26 * u, 46 * u)], fill=255)
    shape(img, (x, y, x + s, y + s), color, a, d, ss=3)


# ------------------------------------------------------------------ canvas and persistent overlay
class Ctx:
    def __init__(self, W, H):
        self.W, self.H, self.land, self.cx = W, H, W > H, W // 2
        yy = np.linspace(0, 1, H)[:, None]; xx = np.linspace(-1, 1, W)[None, :]
        glow = np.clip(1 - np.sqrt(xx ** 2 * 0.8 + (yy - 0.28) ** 2 * 1.6), 0, 1) ** 2
        top, bot = np.array(NAVY2, float), np.array(NAVY, float)
        arr = top[None, None, :] * (1 - yy[..., None]) + bot[None, None, :] * yy[..., None] + glow[..., None] * np.array([16, 24, 34], float)
        self.bg = Image.fromarray(np.clip(arr, 0, 255).astype('uint8'), 'RGB')
        self.logo = None
        try:
            lg = Image.open(LOGO).convert('RGBA')
            px = np.asarray(lg).copy(); px[..., 3] = np.clip((255 - px[..., :3].min(axis=2).astype(int)) * 3, 0, 255).astype('uint8'); lg = Image.fromarray(px, 'RGBA')
            hh = self.S(88, 56); self.logo = lg.resize((int(lg.width * hh / lg.height), hh), Image.LANCZOS)
        except Exception: pass
        # layout (portrait is a phone, with platform UI at the very top and bottom)
        self.top, self.bot = self.S(330, 118), self.S(1330, 545)
        self.cap_y = self.S(1610, 612)
        self.strip_y = self.S(1842, 698)

    def S(self, p, l): return l if self.land else p
    def frame(self): return self.bg.copy()


def pill(c, img, cx, y, label, a=1.0, fill=GOLD, fg=NAVY, size=None):
    f = F('heavy', size or c.S(34, 21))
    w = f.getlength(label) + c.S(58, 36); h = c.S(66, 40)
    rrect(img, cx - w / 2, y, cx + w / 2, y + h, h / 2, fill, a)
    text(img, cx, y + h / 2 + 1, label, f, fg, a, 'mm')


def overlay(c, img, t, total, cap):
    W, H = c.W, c.H
    shape(img, (0, 0, int(W * clamp(t / total)), c.S(8, 5)), GOLD, 1.0, lambda d, ss, w, h: d.rectangle([0, 0, w, h], fill=255))
    bx, by = c.S(56, 40), c.S(70, 26)
    if c.logo: img.paste(c.logo, (bx, by), c.logo)
    lw = c.logo.width if c.logo else 0
    text(img, bx + lw + c.S(20, 12), by + c.S(44, 28), 'Honorbrook Insurance', F('serif', c.S(44, 27)), GOLDL, 1.0, 'lm')
    text(img, W / 2, c.strip_y, 'Honorbrook Insurance  ·  (571) 354-0146', F('bold', c.S(34, 21)), SOFT, 1.0, 'mm')
    if cap: caption(c, img, t, cap)


def caption(c, img, t, cap):
    s, e, words = cap
    a = clamp((t - (s - 0.08)) / 0.18) * clamp(((e + 0.45) - t) / 0.25)
    if a <= 0: return
    f = F('bold', c.S(52, 31)); maxw = int(c.W * c.S(0.88, 0.78))
    lines = wrap(' '.join(words), f, maxw)
    lh = int(f.size * 1.3); hbox = len(lines) * lh + c.S(40, 22)
    wmax = max(f.getlength(l) for l in lines) + c.S(64, 40)
    y0 = c.cap_y - hbox / 2
    rrect(img, c.cx - wmax / 2, y0, c.cx + wmax / 2, y0 + hbox, c.S(30, 18), (10, 20, 36), 0.72 * a)
    wts = [len(w) + 2 for w in words]; tot = sum(wts); p = clamp((t - s) / max(e - s, 0.2)) * 1.04
    done, idx = 0, 0
    y = y0 + c.S(20, 11)
    for ln in lines:
        n = len(ln.split()); xs = c.cx - f.getlength(ln) / 2
        for w in ln.split():
            col = WHITE if done + wts[idx] / 2 <= p * tot else (GOLDL if done <= p * tot else (200, 210, 226))
            text(img, xs, y, w, f, col, a, 'la'); xs += f.getlength(w + ' '); done += wts[idx]; idx += 1
        y += lh


# ------------------------------------------------------------------ shared scenes
def end_card(c, img, t, ph, lines):
    """lines = (question, phone, web, disclaimer)"""
    q, phone, web, disc = lines
    a = eo3(prog(t, 0.0, 0.5))
    y = c.S(360, 140)
    text(img, c.cx, y, q, F('serif', c.S(76, 44)), CREAM, a, 'mm') if f_fits(c, q) else para(img, c.cx, y - c.S(60, 20), q, F('serif', c.S(76, 44)), CREAM, int(c.W * 0.86), a, 1.15)
    b = eo3(prog(t, ph[0][0] + 0.2, 0.5))
    y2 = c.S(640, 215)
    rrect(img, c.cx - c.S(430, 260), y2, c.cx + c.S(430, 260), y2 + c.S(150, 78), c.S(30, 16), GOLD, b)
    text(img, c.cx, y2 + c.S(75, 39), phone, F('heavy', c.S(84, 48)), NAVY, b, 'mm')
    d = eo3(prog(t, ph[0][0] + 0.8, 0.5))
    text(img, c.cx, y2 + c.S(250, 118), 'or fill out the form at', F('med', c.S(40, 22)), SOFT, d, 'mm')
    text(img, c.cx, y2 + c.S(320, 160), web, F('bold', c.S(56, 32)), WHITE, d, 'mm')
    e = eo3(prog(t, ph[-1][0], 0.5))
    para(img, c.cx, c.S(1090, 425), disc, F('reg', c.S(30, 17)), SOFT, int(c.W * c.S(0.84, 0.74)), e * 0.95, 1.35)


def f_fits(c, s): return F('serif', c.S(76, 44)).getlength(s) < c.W * 0.9


# ------------------------------------------------------------------ VIDEO 1: Part D late enrollment penalty
def d_hook(c, img, t, ph):
    pill(c, img, c.cx, c.S(330, 118), 'MEDICARE PART D', eo3(prog(t, 0.05, 0.4)))
    cs, ce = ph[0][0] + 0.35, ph[0][0] + (ph[0][1] - ph[0][0]) * 0.82
    v = 9.40 * eo3(prog(t, cs, ce - cs))
    s = '$%.2f' % v
    pop = 1 + 0.06 * math.sin(clamp((t - ce) / 0.5) * math.pi) if t > ce else 1
    text(img, c.cx, c.S(720, 262), s, F('serif', int(c.S(300, 138) * pop)), GOLDL, eo3(prog(t, 0.15, 0.3)), 'mm')
    text(img, c.cx, c.S(930, 362), 'more per month', F('med', c.S(68, 34)), CREAM, eo3(prog(t, ce - 0.2, 0.5)), 'mm')
    p1 = eo3(prog(t, ph[1][0] + 0.05, 0.5))
    rrect(img, c.cx - c.S(440, 300), c.S(1010, 405), c.cx + c.S(440, 300), c.S(1150, 467), c.S(24, 14), PANEL, p1)
    text(img, c.cx, c.S(1080, 436), 'for as long as you have drug coverage', F('bold', c.S(44, 25)), WHITE, p1, 'mm')
    text(img, c.cx, c.S(1250, 505), 'Example: 24 months without coverage, using the 2026 base premium ($38.99)', F('reg', c.S(30, 17)), SOFT, eo3(prog(t, ce + 0.3, 0.5)), 'mm') if not c.land else \
        text(img, c.cx, 498, 'Example: 24 months uncovered, 2026 base premium $38.99', F('reg', 17), SOFT, eo3(prog(t, ce + 0.3, 0.5)), 'mm')


def d_63(c, img, t, ph):
    pill(c, img, c.cx, c.S(330, 118), 'THE TRIGGER', eo3(prog(t, 0.0, 0.4)))
    a0 = eo3(prog(t, ph[0][0] + 0.1, 0.5))
    icon(img, 'flag', c.cx - c.S(330, 235), c.S(420, 168), c.S(70, 38), GOLDL, a0)
    text(img, c.cx - c.S(250, 190), c.S(455, 187), 'Initial Enrollment Period ends', F('bold', c.S(44, 26)), CREAM, a0, 'lm')
    s, e = ph[1][0] + 0.15, ph[1][1] - 0.1
    n = int(round(63 * clamp((t - s) / (e - s))))
    full = t >= ph[2][0]
    flash = prog(t, ph[2][0], 0.5)
    col = mix(GOLDL, CORAL, eio(flash))
    text(img, c.cx, c.S(565, 262), ('%d' % n) if n else '0', F('serif', c.S(180, 96)), col, 1.0, 'mm')
    text(img, c.cx, c.S(680, 328), 'days without drug coverage', F('med', c.S(40, 23)), SOFT, 1.0, 'mm')
    cols, sq, gap = (9, c.S(70, 33), c.S(10, 8)) if not c.land else (21, 33, 8)
    if not c.land: cols = 7
    rows = math.ceil(63 / cols)
    gw = cols * sq + (cols - 1) * gap
    x0, y0 = c.cx - gw / 2, c.S(745, 360)
    for i in range(63):
        r, q = divmod(i, cols); x = x0 + q * (sq + gap); y = y0 + r * (sq + gap)
        on = i < n
        pulse = 0.5 + 0.5 * math.sin((t * 6) - i * 0.25) if full else 0
        rrect(img, x, y, x + sq, y + sq, c.S(12, 6), GOLDL if on and not full else (mix(CORAL, (255, 170, 140), pulse * 0.4) if full else PANEL), 1.0 if (on or full) else 0.9)
    b = eob(prog(t, ph[2][0] + 0.25, 0.5))
    if b > 0:
        wlab = c.S(700, 500); h = c.S(84, 56); yb = y0 + rows * (sq + gap) + c.S(22, 18)
        rrect(img, c.cx - wlab / 2, yb, c.cx + wlab / 2, yb + h, h / 2, CORAL, clamp(b))
        text(img, c.cx, yb + h / 2, 'The penalty can start', F('heavy', c.S(46, 28)), WHITE, clamp(b), 'mm')


def d_math(c, img, t, ph):
    pill(c, img, c.cx, c.S(330, 118), 'THE MATH', eo3(prog(t, 0.0, 0.4)))
    f1 = eo3(prog(t, ph[0][0] + 0.1, 0.5)); f2 = eo3(prog(t, ph[1][0] + 0.1, 0.5))
    if c.land:
        text(img, c.cx, 200, '1%  ×  $38.99', F('serif', 70), GOLDL, f1, 'mm')
        text(img, c.cx, 258, '×  each full month without coverage', F('bold', 34), CREAM, f2, 'mm')
    else:
        text(img, c.cx, 520, '1%  ×  $38.99', F('serif', 112), GOLDL, f1, 'mm')
        text(img, c.cx, 640, '×  each full month without coverage', F('bold', 44), CREAM, f2, 'mm')
    rows = [('6 months', 2.30, 2), ('1 year', 4.70, 3), ('2 years', 9.40, 4), ('3 years', 14.00, 5)]
    lx = c.S(100, 215); bx = c.S(330, 410); bw = c.S(520, 560); rh = c.S(92, 46); gap = c.S(40, 18); y0 = c.S(770, 305)
    for i, (lab, val, k) in enumerate(rows):
        y = y0 + i * (rh + gap); p = eo3(prog(t, ph[k][0] + 0.05, 0.7))
        hot = (val == 9.40)
        text(img, lx, y + rh / 2, lab, F('bold', c.S(44, 26)), WHITE if p > 0 else (0, 0, 0), clamp(p * 3), 'lm')
        rrect(img, bx, y, bx + bw, y + rh, rh / 2, PANEL, clamp(p * 3) * 0.5)
        L = max(bw * val / 14.0 * p, 0)
        if L > rh * 0.6: rrect(img, bx, y, bx + L, y + rh, rh / 2, GOLD if hot else (118, 150, 196), 1.0)
        text(img, bx + max(L, rh * 0.6) + c.S(18, 10), y + rh / 2, '$%.2f' % (val * p), F('heavy', c.S(48, 28)), GOLDL if hot else CREAM, clamp(p * 2), 'lm')
    text(img, c.cx, c.S(1275, 515), 'per month  ·  rounded to the nearest $0.10  ·  Medicare.gov', F('reg', c.S(30, 17)), SOFT, eo3(prog(t, ph[2][0], 0.6)), 'mm')


def d_follow(c, img, t, ph):
    pill(c, img, c.cx, c.S(330, 118), 'IT STICKS', eo3(prog(t, 0.0, 0.4)))
    cw, chh = c.S(860, 640), c.S(250, 120)
    ya = c.S(470, 190); yb = c.S(900, 350)
    a = eo3(prog(t, 0.1, 0.5)); b = eo3(prog(t, ph[1][0] + 0.1, 0.5))
    inner = cw - c.S(80, 48); px0 = c.cx - cw / 2 + c.S(40, 24); pw = c.S(190, 100); ph_ = c.S(80, 36); off = c.S(110, 56)
    for y, lab, plen, sa in ((ya, 'Your plan premium', 0.46, a), (yb, 'A different plan', 0.62, b)):
        rrect(img, c.cx - cw / 2, y, c.cx + cw / 2, y + chh, c.S(30, 16), PANEL, sa)
        text(img, c.cx - cw / 2 + c.S(40, 24), y + c.S(48, 24), lab, F('bold', c.S(40, 22)), CREAM, sa, 'lm')
        rrect(img, px0, y + off, px0 + inner * plen, y + off + ph_, c.S(20, 10), (118, 150, 196), sa)
    appear = eo3(prog(t, ph[0][0] + 0.3, 0.5)); move = eio(prog(t, ph[1][0] + 0.55, 1.0))
    x1, y1 = px0 + inner * 0.46, ya + off; x2, y2 = px0 + inner * 0.62, yb + off
    x = lerp(x1, x2, move); y = lerp(y1, y2, move) - math.sin(move * math.pi) * c.S(40, 18)
    rrect(img, x, y, x + pw, y + ph_, c.S(20, 10), CORAL, appear)
    text(img, x + pw / 2, y + ph_ / 2, '+ penalty', F('heavy', c.S(30, 16)), WHITE, appear, 'mm')
    text(img, c.cx, c.S(1230, 485), 'It stays for as long as you have Medicare drug coverage', F('med', c.S(36, 21)), SOFT, eo3(prog(t, ph[1][0] + 1.7, 0.6)), 'mm')


def d_avoid(c, img, t, ph):
    pill(c, img, c.cx, c.S(330, 118), 'HOW TO AVOID IT', eo3(prog(t, 0.0, 0.4)))
    items = [('calendar', 'Enroll when you are first eligible', 0), ('doc', 'Keep your creditable coverage notices', 1),
             ('shield', 'Never let a gap reach 63 days', 2), ('heart', 'Ask about Extra Help (no penalty if you get it)', 3)]
    cw, chh, gap = c.S(920, 860), c.S(190, 76), c.S(30, 12); y0 = c.S(450, 180)
    for i, (ic, lab, k) in enumerate(items):
        y = y0 + i * (chh + gap)
        p = eo3(prog(t, ph[k][0] - 0.05, 0.45)); slide = (1 - p) * c.S(60, 40)
        rrect(img, c.cx - cw / 2 + slide, y, c.cx + cw / 2 + slide, y + chh, c.S(32, 18), PANEL, p)
        icon(img, ic, c.cx - cw / 2 + c.S(44, 26) + slide, y + (chh - c.S(100, 48)) / 2, c.S(100, 48), GOLDL, p)
        if ic == 'shield': text(img, c.cx - cw / 2 + c.S(94, 50) + slide, y + chh / 2 + c.S(6, 3), '63', F('heavy', c.S(26, 12)), GOLDL, p, 'mm')
        f = F('bold', c.S(41, 23)); lines = wrap(lab, f, cw - c.S(300, 170))
        for j, ln in enumerate(lines): text(img, c.cx - cw / 2 + c.S(190, 100) + slide, y + chh / 2 + (j - (len(lines) - 1) / 2) * f.size * 1.2, ln, f, WHITE, p, 'lm')
        check(img, c.cx + cw / 2 - c.S(68, 40) + slide, y + chh / 2, c.S(34, 17), prog(t, ph[k][1] - 0.4, 0.5))


PART_D = dict(
    slug='part-d-late-enrollment-penalty', title='The Medicare Part D late enrollment penalty: what it costs and how to avoid it', poster=2.6,
    disclaimer=('Honorbrook Insurance is an independent agency and is not connected with or endorsed by the U.S. government or the federal Medicare program. '
                'We do not offer every plan available in your area. Contact Medicare.gov or 1-800-MEDICARE for all of your options. General information, not advice.'),
    scenes=[
        dict(phr=[('Two years without Medicare drug coverage can add about $9.40 a month to your premium.', 'Two years without Medicare drug coverage can add about nine dollars and forty cents a month to your premium.'),
                  ('For as long as you have drug coverage.', 'For as long as you have drug coverage.')], draw=d_hook, pre=0.1, post=0.7),
        dict(phr=[('The clock starts when your Initial Enrollment Period ends.', 'The clock starts when your Initial Enrollment Period ends.'),
                  ('Go 63 days in a row without Part D, or other creditable drug coverage,', 'Go sixty three days in a row without Part D, or other creditable drug coverage,'),
                  ('and the late enrollment penalty can apply.', 'and the late enrollment penalty can apply.')], draw=d_63, sfx=lambda ph: [(ph[2][0] + 0.05, 'thump')], pre=0.15, post=0.8),
        dict(phr=[('One percent of the national base premium, $38.99 in 2026,', 'One percent of the national base premium, thirty eight ninety nine in twenty twenty six,'),
                  ('times each full month without coverage.', 'times each full month without coverage.'),
                  ('Six months: about $2.30 a month.', 'Six months, about two dollars and thirty cents a month.'),
                  ('A year: $4.70.', 'A year, four dollars and seventy cents.'),
                  ('Two years: $9.40.', 'Two years, nine dollars and forty cents.'),
                  ('Three years: $14.', 'Three years, fourteen dollars.')], draw=d_math,
             sfx=lambda ph: [(ph[k][0] + 0.1, 'tick') for k in (2, 3, 4, 5)], pre=0.15, post=0.6),
        dict(phr=[('It is added to your plan premium.', 'It is added to your plan premium.'),
                  ('And it follows you if you switch plans.', 'And it follows you if you switch plans.')], draw=d_follow, pre=0.15, post=1.1),
        dict(phr=[('Enroll when you are first eligible.', 'To avoid it, enroll when you are first eligible.'),
                  ('Keep your creditable coverage notices.', 'Keep your creditable coverage notices.'),
                  ('Do not let a gap reach 63 days.', 'Do not let a gap reach sixty three days.'),
                  ('And ask about Extra Help. If you get it, you do not pay the penalty.', 'And ask about Extra Help. If you get it, you do not pay the penalty.')],
             draw=d_avoid, sfx=lambda ph: [(ph[k][1] - 0.35, 'ding') for k in (0, 1, 2, 3)], pre=0.15, post=0.6),
        dict(phr=[('Questions about your situation? Call (571) 354-0146, or fill out the form at honorbrook-insurance.com.', 'Questions about your situation? Call five seven one, three five four, zero one four six, or fill out the form at honorbrook insurance dot com.'),
                  ('A licensed agent will reach out.', 'A licensed agent will reach out.')],
             draw=lambda c, img, t, ph: end_card(c, img, t, ph, ('Questions about your situation?', '(571) 354-0146', 'honorbrook-insurance.com',
                                                                  'Honorbrook Insurance is an independent agency and is not connected with or endorsed by the U.S. government or the federal Medicare program. We do not offer every plan available in your area. Contact Medicare.gov or 1-800-MEDICARE for all of your options.')),
             pre=0.1, post=1.2),
    ])


# ------------------------------------------------------------------ VIDEO 2: comparing ACA plans
def a_hook(c, img, t, ph):
    pill(c, img, c.cx, c.S(330, 118), 'ACA OPEN ENROLLMENT', eo3(prog(t, 0.0, 0.4)))
    y0, rh, bw, x0 = c.S(560, 215), c.S(150, 74), c.S(860, 620), c.cx - c.S(430, 310)
    segs = [('Plan X', 0.30, 0.62, 'Lower premium'), ('Plan Y', 0.50, 0.28, 'Higher premium')]
    for i, (nm, pr, car, lab) in enumerate(segs):
        y = y0 + i * (rh + c.S(110, 62))
        text(img, x0, y - c.S(34, 18), nm + '  ·  ' + lab, F('bold', c.S(38, 21)), CREAM, eo3(prog(t, 0.2 + i * 0.2, 0.4)), 'lm')
        rrect(img, x0, y, x0 + bw, y + rh, c.S(26, 14), PANEL, 0.55)
        p1 = eo3(prog(t, ph[0][0] + 0.2 + i * 0.25, 0.8)); p2 = eo3(prog(t, ph[1][0] + 0.05 + i * 0.25, 0.9))
        L1 = bw * pr * p1; L2 = bw * car * p2
        if L1 > 4: rrect(img, x0, y, x0 + L1, y + rh, c.S(26, 14), (118, 150, 196), 1.0)
        if L2 > 4: rrect(img, x0 + L1, y, x0 + L1 + L2, y + rh, c.S(26, 14), CORAL, 1.0)
    ly = y0 + 2 * (rh + c.S(110, 62)) - c.S(30, 10)
    circle(img, x0 + c.S(14, 9), ly + c.S(24, 12), c.S(14, 8), (118, 150, 196)); text(img, x0 + c.S(44, 26), ly + c.S(24, 12), 'Premiums for the year', F('med', c.S(34, 19)), CREAM, 1.0, 'lm')
    circle(img, x0 + c.S(14, 9) + c.S(430, 300), ly + c.S(24, 12), c.S(14, 8), CORAL); text(img, x0 + c.S(44, 26) + c.S(430, 300), ly + c.S(24, 12), 'What you pay for care', F('med', c.S(34, 19)), CREAM, 1.0, 'lm')
    v = eo3(prog(t, ph[1][1] - 0.6, 0.5))
    for i, (txt, col) in enumerate((('Higher total', CORAL), ('Lower total', GREEN))):
        y = y0 + i * (rh + c.S(110, 62))
        text(img, x0 + bw, y - c.S(34, 18), txt, F('heavy', c.S(34, 19)), col, v, 'rm')
    text(img, c.cx, c.S(1215, 492), 'Illustration only, not real prices', F('reg', c.S(30, 17)), SOFT, eo3(prog(t, ph[1][0] + 0.6, 0.5)), 'mm')


def a_cost(c, img, t, ph):
    pill(c, img, c.cx, c.S(330, 118), 'STEP 1  ·  TOTAL YEARLY COST', eo3(prog(t, 0.0, 0.4)))
    w, h = c.S(780, 560), c.S(150, 62); x0 = c.cx - w / 2; yb = c.S(1130, 480); gp = c.S(18, 8)
    blocks = [('Monthly premium × 12', (118, 150, 196), 1), ('Deductible', GOLD, 1), ('Copays and coinsurance', CORAL, 1)]
    ys = []
    for i, (lab, col, k) in enumerate(blocks):
        y = yb - (i + 1) * (h + gp); ys.append(y)
        p = eo3(prog(t, ph[k][0] + 0.15 + i * (ph[k][1] - ph[k][0]) * 0.33, 0.5)); slide = (1 - p) * c.S(70, 40)
        rrect(img, x0, y - slide, x0 + w, y + h - slide, c.S(24, 12), col, p)
        text(img, x0 + w / 2, y + h / 2 - slide, lab, F('heavy', c.S(42, 24)), NAVY if col != CORAL else WHITE, p, 'mm')
    q = eo3(prog(t, ph[2][0] + 0.1, 0.6))
    if q > 0:
        ytop = ys[2] - c.S(26, 12)
        for xx in range(int(x0 - c.S(10, 6)), int(x0 + w), int(c.S(46, 26))):
            rrect(img, xx, ytop - 3, xx + c.S(26, 14), ytop + 3, 3, GREEN, q)
        bx = x0 - c.S(26, 16)
        shape(img, (bx - 3, int(ys[2]), bx + 3, int(ys[1] + h)), GREEN, q, lambda d, ss, ww, hh: d.rectangle([0, 0, ww, hh], fill=255))
        text(img, x0 + w / 2, ytop - c.S(40, 20), 'Out-of-pocket maximum', F('heavy', c.S(42, 24)), GREEN, q, 'mm')
        text(img, x0 + w / 2, ytop - c.S(94, 46), 'caps what you pay for covered, in-network care', F('med', c.S(30, 17)), SOFT, q, 'mm')


def a_check(c, img, t, ph):
    pill(c, img, c.cx, c.S(330, 118), 'STEP 2  ·  DOCTORS AND DRUGS', eo3(prog(t, 0.0, 0.4)))
    items = [('cross', 'Are your doctors and hospitals in the plan network?', 0), ('pill', 'Is each prescription on the plan\'s drug list?', 1), ('pin', 'And is your pharmacy covered?', 2)]
    cw, chh, gap = c.S(920, 860), c.S(230, 100), c.S(36, 16); y0 = c.S(470, 200)
    for i, (ic, lab, k) in enumerate(items):
        y = y0 + i * (chh + gap)
        p = eo3(prog(t, ph[k][0] - 0.05, 0.45)); slide = (1 - p) * c.S(60, 40)
        rrect(img, c.cx - cw / 2 + slide, y, c.cx + cw / 2 + slide, y + chh, c.S(32, 18), PANEL, p)
        icon(img, ic, c.cx - cw / 2 + c.S(48, 26) + slide, y + (chh - c.S(110, 52)) / 2, c.S(110, 52), GOLDL, p)
        f = F('bold', c.S(44, 25)); lines = wrap(lab, f, cw - c.S(340, 200))
        for j, ln in enumerate(lines): text(img, c.cx - cw / 2 + c.S(210, 110) + slide, y + chh / 2 + (j - (len(lines) - 1) / 2) * f.size * 1.2, ln, f, WHITE, p, 'lm')
        check(img, c.cx + cw / 2 - c.S(70, 40) + slide, y + chh / 2, c.S(36, 18), prog(t, ph[k][1] - 0.35, 0.5))


METALS = [('Bronze', 60, (205, 140, 90)), ('Silver', 70, (200, 208, 220)), ('Gold', 80, GOLDL), ('Platinum', 90, (170, 205, 230))]


def a_metal(c, img, t, ph):
    pill(c, img, c.cx, c.S(330, 118), 'STEP 3  ·  METAL LEVELS', eo3(prog(t, 0.0, 0.4)))
    bw, bh = c.S(860, 700), c.S(100, 48); x0 = c.cx - bw / 2; y0 = c.S(510, 205); gap = c.S(76, 34)
    for i, (nm, pays, col) in enumerate(METALS):
        y = y0 + i * (bh + gap); p = eo3(prog(t, ph[1][0] + 0.15 + i * 0.28, 0.7))
        text(img, x0, y - c.S(30, 14), nm, F('heavy', c.S(38, 21)), col, clamp(p * 3), 'lm')
        text(img, x0 + bw, y - c.S(30, 14), 'You pay %d%%' % (100 - pays), F('bold', c.S(36, 20)), CREAM, clamp((p - 0.5) * 2), 'rm')
        rrect(img, x0, y, x0 + bw, y + bh, c.S(26, 14), PANEL, clamp(p * 3))
        Lp = bw * pays / 100 * p
        if Lp > 6: rrect(img, x0, y, x0 + Lp, y + bh, c.S(26, 14), col, 1.0)
        if p > 0.55: text(img, x0 + c.S(36, 20), y + bh / 2, 'Plan pays %d%%' % pays, F('heavy', c.S(40, 23)), NAVY, clamp((p - 0.55) / 0.45), 'lm')
    yb = y0 + 4 * (bh + gap) - c.S(20, 8); r = eob(prog(t, ph[2][0] + 0.1, 0.5))
    if r > 0:
        w = c.S(840, 560)
        rrect(img, c.cx - w / 2, yb, c.cx + w / 2, yb + c.S(100, 50), c.S(50, 25), CORAL, clamp(r))
        text(img, c.cx, yb + c.S(50, 25), 'Metal level  ≠  quality of care', F('heavy', c.S(42, 24)), WHITE, clamp(r), 'mm')
    text(img, c.cx, yb + c.S(150, 78), 'On average. Actual costs vary by plan. Source: HealthCare.gov', F('reg', c.S(29, 16)), SOFT, eo3(prog(t, ph[1][0] + 1.2, 0.5)), 'mm')


def a_save(c, img, t, ph):
    pill(c, img, c.cx, c.S(330, 118), 'STEP 4  ·  SAVINGS', eo3(prog(t, 0.0, 0.4)))
    bw, bh = c.S(900, 720), c.S(130, 62); x0 = c.cx - bw / 2; y0 = c.S(470, 190); gap = c.S(40, 16)
    g1 = eo3(prog(t, ph[1][0] + 0.2, 0.6)); g2 = eo3(prog(t, ph[2][0] + 0.15, 0.6))
    for i, (nm, pays, col) in enumerate(METALS):
        y = y0 + i * (bh + gap); p = eo3(prog(t, 0.15 + i * 0.12, 0.45))
        rrect(img, x0, y, x0 + bw, y + bh, c.S(28, 14), PANEL, p)
        circle(img, x0 + c.S(52, 28), y + bh / 2, c.S(24, 12), col, p)
        text(img, x0 + c.S(96, 52), y + bh / 2, nm, F('heavy', c.S(44, 26)), WHITE, p, 'lm')
        bx = x0 + bw - c.S(570, 352)
        if g1 > 0: rrect(img, bx, y + c.S(24, 10), bx + c.S(270, 172), y + bh - c.S(24, 10), c.S(24, 14), GREEN, g1); text(img, bx + c.S(135, 86), y + bh / 2, 'Premium tax credit', F('heavy', c.S(29, 15)), NAVY, g1, 'mm')
        if nm == 'Silver' and g2 > 0:
            rrect(img, bx + c.S(288, 184), y + c.S(24, 10), bx + c.S(288, 184) + c.S(250, 158), y + bh - c.S(24, 10), c.S(24, 14), GOLD, g2)
            text(img, bx + c.S(288, 184) + c.S(125, 79), y + bh / 2, 'Cost-sharing help', F('heavy', c.S(29, 15)), NAVY, g2, 'mm')
            rrect(img, x0 - 8, y - 8, x0 + bw + 8, y + bh + 8, c.S(34, 18), GOLDL, g2, outline=4)
    text(img, c.cx, c.S(1190, 522), 'If you qualify. Cost-sharing reductions only come with Silver plans.', F('med', c.S(32, 18)), SOFT, g2, 'mm')


def a_dates(c, img, t, ph):
    pill(c, img, c.cx, c.S(330, 118), 'MARK THE DATES', eo3(prog(t, 0.0, 0.4)))
    pts = [('Nov 1', 'Open Enrollment starts', ph[1][0] + 0.1), ('Dec 15', 'Last day to enroll for Jan 1 coverage', ph[1][0] + 1.9), ('Jan 15', 'Open Enrollment ends', ph[1][0] + 4.1)]
    if not c.land:
        lx = c.S(250, 0); y0 = 510; step = 250
        total = prog(t, pts[0][2], pts[2][2] - pts[0][2] + 0.4)
        shape(img, (lx - 4, y0, lx + 4, y0 + 2 * step), (60, 90, 130), 1.0, lambda d, ss, w, h: d.rectangle([0, 0, w, h], fill=255))
        shape(img, (lx - 4, y0, lx + 4, y0 + int(2 * step * total)), GOLD, 1.0, lambda d, ss, w, h: d.rectangle([0, 0, w, h], fill=255))
        for i, (d, lab, ts) in enumerate(pts):
            y = y0 + i * step; p = eob(prog(t, ts, 0.5))
            circle(img, lx, y, 30 * clamp(p), GOLDL if i != 1 else CORAL)
            text(img, lx + 90, y - 34, d, F('serif', 76), GOLDL if i != 1 else (255, 170, 140), clamp(p), 'lm')
            para(img, lx + 90, y + 6, lab, F('bold', 38), CREAM, 600, clamp(p), 1.15, 'left')
        v = eob(prog(t, ph[2][0] + 0.3, 0.5))
        if v > 0:
            rrect(img, c.cx - 440, 1130, c.cx + 440, 1250, 60, PANEL, clamp(v))
            text(img, c.cx, 1190, 'Virginia: through Jan 29', F('heavy', 46), GOLDL, clamp(v), 'mm')
            text(img, c.cx, 1290, 'State exchanges can differ  ·  Source: HealthCare.gov', F('reg', 28), SOFT, clamp(v), 'mm')
    else:
        y = 255; xs = [210, 640, 1070]
        total = prog(t, pts[0][2], pts[2][2] - pts[0][2] + 0.4)
        shape(img, (xs[0], y - 3, xs[2], y + 3), (60, 90, 130), 1.0, lambda d, ss, w, h: d.rectangle([0, 0, w, h], fill=255))
        shape(img, (xs[0], y - 3, xs[0] + int((xs[2] - xs[0]) * total), y + 3), GOLD, 1.0, lambda d, ss, w, h: d.rectangle([0, 0, w, h], fill=255))
        for i, (d, lab, ts) in enumerate(pts):
            p = eob(prog(t, ts, 0.5))
            circle(img, xs[i], y, 14 * clamp(p), GOLDL if i != 1 else CORAL)
            text(img, xs[i], y - 50, d, F('serif', 44), GOLDL if i != 1 else (255, 170, 140), clamp(p), 'mm')
            para(img, xs[i], y + 32, lab, F('bold', 22), CREAM, 380, clamp(p), 1.15)
        v = eob(prog(t, ph[2][0] + 0.3, 0.5))
        if v > 0:
            rrect(img, c.cx - 270, 410, c.cx + 270, 468, 29, PANEL, clamp(v))
            text(img, c.cx, 439, 'Virginia: through Jan 29', F('heavy', 28), GOLDL, clamp(v), 'mm')
            text(img, c.cx, 502, 'State exchanges can differ  ·  Source: HealthCare.gov', F('reg', 17), SOFT, clamp(v), 'mm')


ACA = dict(
    slug='compare-aca-plans-open-enrollment', title='How to compare ACA health plans during Open Enrollment', poster=3.2,
    disclaimer='Honorbrook Insurance is an independent insurance agency and is not connected with or endorsed by any government agency. General information, not insurance, tax or legal advice.',
    scenes=[
        dict(phr=[('The cheapest premium is not always the cheapest year.', 'The cheapest premium is not always the cheapest year.'),
                  ('What you pay for care counts too.', 'What you pay for care counts too.')], draw=a_hook, pre=0.1, post=0.8),
        dict(phr=[('Step one: estimate your total yearly cost.', 'Step one. Estimate your total yearly cost.'),
                  ('Monthly premium times 12, plus the deductible, copays and coinsurance you expect to pay.', 'Monthly premium times twelve, plus the deductible, copays and coinsurance you expect to pay.'),
                  ('And know the out-of-pocket maximum, the most you pay for covered, in-network care in a year.', 'And know the out of pocket maximum, the most you pay for covered, in network care, in a year.')], draw=a_cost,
             sfx=lambda ph: [(ph[1][0] + 0.25, 'tick'), (ph[1][0] + 1.5, 'tick'), (ph[1][0] + 2.9, 'tick'), (ph[2][0] + 0.15, 'ding')], pre=0.15, post=0.8),
        dict(phr=[('Step two: are your doctors and hospitals in the plan network?', 'Step two. Are your doctors and hospitals in the plan network?'),
                  ('Is each prescription on the plan\'s drug list?', 'Is each prescription on the plan\'s drug list?'),
                  ('And your pharmacy?', 'And your pharmacy?')], draw=a_check,
             sfx=lambda ph: [(ph[k][1] - 0.3, 'ding') for k in (0, 1, 2)], pre=0.15, post=0.6),
        dict(phr=[('Step three: understand the metal levels.', 'Step three. Understand the metal levels.'),
                  ('Bronze, Silver, Gold and Platinum describe how costs are split, on average.', 'Bronze, Silver, Gold and Platinum describe how costs are split, on average.'),
                  ('They do not describe the quality of care.', 'They do not describe the quality of care.'),
                  ('Lower tiers usually mean lower premiums, but higher costs when you use care.', 'Lower tiers usually mean lower premiums, but higher costs when you use care.')], draw=a_metal,
             sfx=lambda ph: [(ph[1][0] + 0.3 + i * 0.28, 'tick') for i in range(4)], pre=0.15, post=0.8),
        dict(phr=[('Step four: check for savings.', 'Step four. Check for savings.'),
                  ('Premium tax credits can apply to any metal level, if you qualify.', 'Premium tax credits can apply to any metal level, if you qualify.'),
                  ('Cost-sharing reductions come only with Silver plans.', 'Cost sharing reductions come only with Silver plans.')], draw=a_save,
             sfx=lambda ph: [(ph[1][0] + 0.3, 'ding'), (ph[2][0] + 0.25, 'ding')], pre=0.15, post=0.8),
        dict(phr=[('Mark the dates.', 'Mark the dates.'),
                  ('On HealthCare.gov, enrollment starts November 1. Enroll by December 15 for coverage that starts January 1. It ends January 15.',
                   'On healthcare dot gov, enrollment starts November first. Enroll by December fifteenth for coverage that starts January first. It ends January fifteenth.'),
                  ('State exchanges can differ. Virginia\'s runs through January 29.', 'State exchanges can differ. Virginia\'s runs through January twenty ninth.')], draw=a_dates,
             sfx=lambda ph: [(ph[1][0] + 0.1, 'ding'), (ph[1][0] + 1.9, 'ding'), (ph[1][0] + 4.1, 'ding')], pre=0.15, post=0.8),
        dict(phr=[('Want a second set of eyes? Call (571) 354-0146, or fill out the form at honorbrook-insurance.com.', 'Want a second set of eyes? Call five seven one, three five four, zero one four six, or fill out the form at honorbrook insurance dot com.'),
                  ('A licensed agent will reach out.', 'A licensed agent will reach out.')],
             draw=lambda c, img, t, ph: end_card(c, img, t, ph, ('Want a second set of eyes?', '(571) 354-0146', 'honorbrook-insurance.com',
                                                                  'Honorbrook Insurance is an independent insurance agency and is not connected with or endorsed by any government agency. General information, not insurance, tax or legal advice.')),
             pre=0.1, post=1.2),
    ])

PART_D.update(page='what-is-the-medicare-part-d-late-enrollment-penalty', watch='The Part D late enrollment penalty',
              vdesc='An animated explainer: the 63-day trigger, the 1% formula with 2026 examples, how the penalty follows you, and four ways to avoid it.')
ACA.update(page='how-do-i-compare-aca-plans-during-open-enrollment', watch='How to compare ACA plans',
           vdesc='An animated explainer on comparing ACA Marketplace plans: total yearly cost, network and drugs, what metal levels mean, savings, and the key dates.')
VIDEOS = {'part-d': PART_D, 'aca': ACA}


# ------------------------------------------------------------------ audio
SR = 44100


def tts(text_, path_wav, tmp, voice=None, rate=178):
    voice = voice or os.environ.get('VIDEO_VOICE', 'Samantha')   # e.g. VIDEO_VOICE='Ava (Premium)' after downloading it in System Settings > Accessibility > Spoken Content
    aiff = path_wav.replace('.wav', '.aiff')
    subprocess.run(['say', '-v', voice, '-r', str(rate), '-o', aiff, text_], check=True)
    subprocess.run(['afconvert', '-f', 'WAVE', '-d', 'LEI16@%d' % SR, '-c', '1', aiff, path_wav], check=True)
    with wave.open(path_wav) as w: x = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(np.float32) / 32768
    f = int(SR * 0.006); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    nz = np.nonzero(np.abs(x) > 0.01)[0]
    return x[nz[0]:nz[-1] + 1] if len(nz) else x


def sfx_wave(kind):
    n = int(SR * 0.6); t = np.arange(n) / SR
    if kind == 'ding': y = np.sin(2 * np.pi * 1318.5 * t) * np.exp(-t * 9) * 0.5 + np.sin(2 * np.pi * 1975.5 * t) * np.exp(-t * 14) * 0.25
    elif kind == 'tick': y = np.sin(2 * np.pi * 880 * t) * np.exp(-t * 38) * 0.45
    elif kind == 'thump': y = np.sin(2 * np.pi * (70 + 40 * np.exp(-t * 12)) * t) * np.exp(-t * 7) * 0.9
    else: y = t * 0
    return (y * 0.20).astype(np.float32)


def build_audio(video, tmp):
    """Returns (mix, timeline) where timeline = per-scene dict(t0, t1, ph=[(s,e)...]) in global seconds."""
    pieces, t, tl, events = [], 0.0, [], []
    lead = 0.25
    t = lead
    for si, sc in enumerate(video['scenes']):
        t0 = t; tp = t + sc.get('pre', 0.15); ph = []
        for pi, (cap, say) in enumerate(sc['phr']):
            wav = tts(say, os.path.join(tmp, 's%d_%d.wav' % (si, pi)), tmp)
            d = len(wav) / SR
            pieces.append((tp, wav)); ph.append((tp, tp + d)); tp += d + 0.2
        t1 = ph[-1][1] + sc.get('post', 0.6)
        tl.append(dict(t0=t0, t1=t1, ph=ph)); t = t1
        if sc.get('sfx'): events += [(t0 + lt, k) for lt, k in sc['sfx']([(a - t0, b - t0) for a, b in ph])]
    total = t + 0.5
    n = int(SR * total) + SR
    voice = np.zeros(n, np.float32)
    for st, w in pieces:
        i = int(st * SR); voice[i:i + len(w)] += w
    voice = voice / max(np.abs(voice).max(), 1e-6) * 0.86
    tt = np.arange(n) / SR
    pad = sum(np.sin(2 * np.pi * f * tt + k) * a for k, (f, a) in enumerate([(110, 1.0), (164.81, 0.8), (220, 0.6), (246.94, 0.35), (277.18, 0.3)]))
    pad *= (0.8 + 0.2 * np.sin(2 * np.pi * 0.07 * tt)) * 0.030 * np.minimum(1, tt / 1.5) * np.minimum(1, np.maximum(0, (total - tt)) / 1.5)
    mix = voice + pad.astype(np.float32)
    for te, k in events:
        w = sfx_wave(k); i = int(te * SR); mix[i:i + len(w)] += w[:max(0, min(len(w), n - i))]
    mix = np.clip(mix, -0.98, 0.98)
    return mix, tl, total


def write_wav(path, x):
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes())


# ------------------------------------------------------------------ encoder (Swift/AVFoundation, raw BGRA frames on stdin)
SWIFT = r'''
import AVFoundation
import Foundation
let a = CommandLine.arguments
let outPath = a[1], audioPath = a[2]
let W = Int(a[3])!, H = Int(a[4])!, fps = Int(a[5])!, n = Int(a[6])!, br = Int(a[7])!
let silent = outPath + ".v.mp4"
try? FileManager.default.removeItem(atPath: silent); try? FileManager.default.removeItem(atPath: outPath)
let w = try! AVAssetWriter(outputURL: URL(fileURLWithPath: silent), fileType: .mp4)
let settings: [String: Any] = [AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: W, AVVideoHeightKey: H,
  AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: br, AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
    AVVideoMaxKeyFrameIntervalKey: fps * 2, AVVideoExpectedSourceFrameRateKey: fps, AVVideoAllowFrameReorderingKey: false]]
let inp = AVAssetWriterInput(mediaType: .video, outputSettings: settings)
inp.expectsMediaDataInRealTime = false
let adap = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: inp, sourcePixelBufferAttributes: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA, kCVPixelBufferWidthKey as String: W, kCVPixelBufferHeightKey as String: H])
w.add(inp); w.startWriting(); w.startSession(atSourceTime: .zero)
let fsz = W * H * 4
let si = FileHandle.standardInput
var frame = 0
while frame < n {
  var data = Data(capacity: fsz)
  while data.count < fsz { let ch = si.readData(ofLength: fsz - data.count); if ch.isEmpty { break }; data.append(ch) }
  if data.count < fsz { print("short read at frame", frame); break }
  while !inp.isReadyForMoreMediaData { Thread.sleep(forTimeInterval: 0.002) }
  var pb: CVPixelBuffer?
  CVPixelBufferPoolCreatePixelBuffer(nil, adap.pixelBufferPool!, &pb)
  CVPixelBufferLockBaseAddress(pb!, [])
  let base = CVPixelBufferGetBaseAddress(pb!)!; let bpr = CVPixelBufferGetBytesPerRow(pb!)
  data.withUnsafeBytes { raw in for y in 0..<H { memcpy(base + y * bpr, raw.baseAddress! + y * W * 4, W * 4) } }
  CVPixelBufferUnlockBaseAddress(pb!, [])
  if !adap.append(pb!, withPresentationTime: CMTime(value: CMTimeValue(frame), timescale: CMTimeScale(fps))) { print("append failed", frame, String(describing: w.error)); break }
  frame += 1
}
inp.markAsFinished()
let sem = DispatchSemaphore(value: 0)
w.finishWriting { sem.signal() }; sem.wait()
print("writer", w.status.rawValue, String(describing: w.error))
let comp = AVMutableComposition()
let va = AVURLAsset(url: URL(fileURLWithPath: silent)); let aa = AVURLAsset(url: URL(fileURLWithPath: audioPath))
let sm = DispatchSemaphore(value: 0)
va.loadValuesAsynchronously(forKeys: ["tracks", "duration"]) { sm.signal() }; sm.wait()
aa.loadValuesAsynchronously(forKeys: ["tracks", "duration"]) { sm.signal() }; sm.wait()
let vt = comp.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid)!
try! vt.insertTimeRange(CMTimeRange(start: .zero, duration: va.duration), of: va.tracks(withMediaType: .video)[0], at: .zero)
let at = comp.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid)!
let adur = CMTimeMinimum(aa.duration, va.duration)
try! at.insertTimeRange(CMTimeRange(start: .zero, duration: adur), of: aa.tracks(withMediaType: .audio)[0], at: .zero)
let ex = AVAssetExportSession(asset: comp, presetName: AVAssetExportPresetPassthrough)!
ex.outputURL = URL(fileURLWithPath: outPath); ex.outputFileType = .mp4; ex.shouldOptimizeForNetworkUse = true
let s2 = DispatchSemaphore(value: 0)
ex.exportAsynchronously { s2.signal() }; s2.wait()
try? FileManager.default.removeItem(atPath: silent)
print(ex.status == .completed ? "OK" : "FAIL \(String(describing: ex.error))")
'''


# ------------------------------------------------------------------ rendering
def scene_at(c, video, tl, si, t):
    img = c.frame(); sc = video['scenes'][si]; s = tl[si]
    ph = [(a - s['t0'], b - s['t0']) for a, b in s['ph']]
    sc['draw'](c, img, t - s['t0'], ph)
    return img


def render_frame(c, video, tl, total, t, caps):
    si = max(i for i, s in enumerate(tl) if s['t0'] <= t + 1e-9) if t >= tl[0]['t0'] else 0
    img = scene_at(c, video, tl, si, t)
    if si > 0 and t - tl[si]['t0'] < 0.33:
        x = eio((t - tl[si]['t0']) / 0.33)
        img = Image.blend(scene_at(c, video, tl, si - 1, t), img, x)
    cap = next(((s, e, w) for s, e, w in caps if s - 0.08 <= t <= e + 0.7), None)
    overlay(c, img, t, total, cap)
    return img


def prepare(name):
    video = VIDEOS[name]
    tmp = os.path.join(SCRATCH, name); os.makedirs(tmp, exist_ok=True)
    mix, tl, total = build_audio(video, tmp)
    caps = []
    for sc, s in zip(video['scenes'], tl):
        for (cap, _), (a, b) in zip(sc['phr'], s['ph']): caps.append((a, b, cap.split()))
    return video, tmp, mix, tl, total, caps


def fmt_size(f): return (1280, 720) if f == 'land' else (1080, 1920)


def still(name, t, f):
    video, tmp, mix, tl, total, caps = prepare(name)
    c = Ctx(*fmt_size(f)); out = os.path.join(SCRATCH, '%s-%s-%.1f.png' % (name, f, t))
    render_frame(c, video, tl, total, t, caps).save(out); print(out, 'total', round(total, 1))


def build(name, only=None):
    video, tmp, mix, tl, total, caps = prepare(name)
    wav = os.path.join(tmp, 'mix.wav'); m4a = os.path.join(tmp, 'mix.m4a'); write_wav(wav, mix)
    subprocess.run(['afconvert', '-f', 'm4af', '-d', 'aac', '-b', '128000', wav, m4a], check=True)
    swift = os.path.join(tmp, 'enc.swift'); open(swift, 'w').write(SWIFT)
    exe = os.path.join(SCRATCH, 'enc')
    if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(__file__):
        r = subprocess.run(['swiftc', '-O', swift, '-o', exe], capture_output=True, text=True)
        if r.returncode: print(r.stderr[-1500:]); raise SystemExit('swiftc failed')
    n = int(total * FPS)
    for f in ([only] if only else ['land', 'port']):
        c = Ctx(*fmt_size(f))
        outdir = os.path.join(ROOT, 'site', 'assets', 'video') if f == 'land' else os.path.join(ROOT, 'social', 'video_masters')
        os.makedirs(outdir, exist_ok=True)
        out = os.path.join(outdir, video['slug'] + ('.mp4' if f == 'land' else '-vertical.mp4'))
        br = 1_700_000 if f == 'land' else 2_600_000
        p = subprocess.Popen([exe, out, m4a, str(c.W), str(c.H), str(FPS), str(n), str(br)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=False)
        for i in range(n):
            img = render_frame(c, video, tl, total, i / FPS, caps)
            p.stdin.write(img.tobytes('raw', 'BGRX'))
            if i % 150 == 0: print(f, i, '/', n, flush=True)
        p.stdin.close(); res = p.stdout.read().decode(); p.wait(); print(res.strip())
        if f == 'land':
            render_frame(c, video, tl, total, video['poster'], caps).convert('RGB').save(os.path.join(outdir, video['slug'] + '.jpg'), quality=86)
        print(f, 'wrote', out, os.path.getsize(out) // 1024, 'KB', round(total, 1), 's')
    json.dump(dict(slug=video['slug'], title=video['title'], duration=round(total, 1), transcript=[cap for sc in video['scenes'] for cap, _ in sc['phr']]),
              open(os.path.join(tmp, 'meta.json'), 'w'), indent=1)


def embed(name):
    """Update the blog page that embeds this video: heading, VideoObject duration/description/transcript, transcript text."""
    import re, html as H
    video = VIDEOS[name]; meta = json.load(open(os.path.join(SCRATCH, name, 'meta.json')))
    path = os.path.join(ROOT, 'site', 'blog', video['page'] + '.html'); h = open(path, encoding='utf-8').read()
    secs = int(round(meta['duration'])); iso = 'PT%dM%dS' % divmod(secs, 60)
    words = round(secs / 5) * 5
    title = '%s in about %d seconds' % (video['watch'], words)
    h = re.sub(r'<h2>Watch: .*?</h2>', '<h2>Watch: %s</h2>' % title, h, count=1)
    transcript = ' '.join(meta['transcript'])
    m = re.search(r'<script type="application/ld\+json">\s*(\{[^<]*?"@type": "VideoObject".*?\})\s*</script>', h, re.S)
    j = json.loads(m.group(1)); j.update(name=title, description=video['vdesc'], duration=iso, transcript=transcript)
    h = h[:m.start(1)] + json.dumps(j, indent=1, ensure_ascii=False) + h[m.end(1):]
    h = re.sub(r'(<details><summary>Video transcript</summary><div class="a">).*?(</div></details>)', lambda mm: mm.group(1) + H.escape(transcript, quote=False) + mm.group(2), h, count=1, flags=re.S)
    open(path, 'w', encoding='utf-8').write(h); print('patched', os.path.relpath(path, ROOT), iso, title)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] == 'list': print(list(VIDEOS))
    elif a[0] == 'still': still(a[1], float(a[2]), a[3] if len(a) > 3 else 'land')
    elif a[0] == 'build': build(a[1], a[a.index('--only') + 1] if '--only' in a else None)
    elif a[0] == 'embed': embed(a[1])
