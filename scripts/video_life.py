#!/usr/bin/env python3
"""Honorbrook life-insurance video kit: the Onyx look (polished black, silver type, chrome highlights) on top of the video studio.

This file is the shared kit AND the driver for the videos in scripts/videos_life/<slug>.py. It does not edit
video_studio.py or video_scenes.py. It reuses their renderer, audio chain, encoder and low-level drawing code, and swaps
three things at import time (in memory only):
  1. the color constants in video_scenes (navy / gold / teal names now hold Onyx neutrals), so any studio primitive a
     scene calls comes out on-brand. Monkeypatching the constants is the cleanest way to restyle without touching that file.
  2. the studio's Ctx (canvas) -> an Onyx canvas: black background with slow silver light, the HB monogram, a black caption scrim.
  3. the studio's overlay (brand corner, footer strip, captions). The studio footer prints (571) 354-0146 as if it were the
     call number; here the footer reads "honorbrook-insurance.com  ·  Call (301) 615-8289". Captions also switch at the moment
     a new line starts (the studio holds the old line about half a second too long).

Commands (run from the repo root):
  python3 scripts/video_life.py list
  python3 scripts/video_life.py times  <slug>                      scene and phrase times (seconds), total length
  python3 scripts/video_life.py still  <slug> <seconds> land|port  [--out DIR]     one PNG frame
  python3 scripts/video_life.py sheet  <slug> [land|port]          [--out DIR]     contact sheet: one frame per scene
  python3 scripts/video_life.py check  <slug>                      wording, phone numbers, caption length, layout, duration
  python3 scripts/video_life.py build  <slug> [--only land|port]   16:9 mp4 + jpg poster -> site/assets/video/<slug>.mp4/.jpg
                                                                   9:16 master -> social/video_masters/<slug>-vertical.mp4
  python3 scripts/video_life.py notes  <slug>                      writes scripts/videos_life/<slug>.md (transcript, sources, files)
<slug> is the file name in scripts/videos_life/ without .py (a path to a .py file also works, for scratch tests).

A video file exports VIDEO = dict(...). Worked examples: scripts/videos_life/_sample.py (two scenes) and
scripts/videos_life/_gallery.py (every scene builder once).

    import video_life as K
    P = K.P
    VIDEO = dict(
        title='...', description='One or two sentences.', poster=2.5,
        sources=[dict(fact='What the screen says', url='https://...', date='page date or "read 2026-11-25"')],
        scenes=[
            K.scene(K.hook('Life insurance', ['Term or', 'permanent?']), [P('Caption words.', 'Spoken words.')]),
            K.scene(K.checklist('Step 1', 'Three questions', ['First', 'Second', 'Third']), [P('...'), P('...'), P('...')]),
            K.end_scene(),
        ])

Voice: the local Kokoro voice "af_heart" (the voice of the existing Honorbrook shorts) when it is installed, else macOS `say`.
Both run offline. Online or paid voice engines are refused here.
"""
import os, sys, re, glob, json, math, subprocess, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
if HERE not in sys.path: sys.path.insert(0, HERE)
_KOKORO_PY = os.path.expanduser('~/.cache/honorbrook-tts/venv/bin/python')
os.environ.setdefault('VIDEO_VOICE_ENGINE', 'kokoro' if os.path.exists(_KOKORO_PY) else 'say')
if os.environ['VIDEO_VOICE_ENGINE'] not in ('kokoro', 'say'):
    raise SystemExit('video_life.py only uses the local voices (VIDEO_VOICE_ENGINE=kokoro or say). Got: ' + os.environ['VIDEO_VOICE_ENGINE'])
os.environ['VIDEO_THEME'] = 'silver'

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import video_scenes as VS
import video_studio as ST
from video_scenes import F, clamp, prog, eo3, eio, eob, lerp, mix, wrap, text, text_shadow, shape, rrect, circle, ring_line, glow, zoom

VDIR = os.path.join(HERE, 'videos_life')

# ------------------------------------------------------------------ Onyx palette (from scripts/onyx/theme_css.py and palette.py)
OX0, OX1, OX2, OX3, OX4, OX5 = (3, 3, 4), (5, 5, 6), (8, 9, 11), (12, 13, 16), (18, 19, 24), (26, 27, 33)
S1, S2, S3, S4 = (244, 245, 247), (217, 220, 226), (170, 176, 186), (125, 131, 142)   # silver type, light to dim
WHITE, INK, MUTED = (255, 255, 255), (5, 5, 6), (154, 161, 172)
ICE = (208, 216, 234)          # the cool light the site uses for glows
GREEN, RED = (87, 217, 163), (255, 157, 148)   # the site's only two accents; use sparingly (a "yes" tick, a "no" cross)
SILVER = ((0.0, (255, 255, 255)), (0.58, (236, 238, 241)), (1.0, (188, 193, 201)))                                        # --silver: headings
CHROME = ((0.0, (255, 255, 255)), (0.36, (238, 240, 243)), (0.51, (164, 170, 180)), (0.61, (223, 226, 231)), (1.0, (196, 201, 209)))   # --chrome: big figures
BTN = ((0.0, (255, 255, 255)), (0.42, (241, 242, 245)), (0.56, (205, 209, 216)), (0.72, (223, 226, 231)), (1.0, (244, 245, 247)))      # --btn: the call button
PANEL = ((0.0, (32, 34, 41)), (0.46, (17, 18, 23)), (1.0, (10, 11, 14)))          # --panel, lifted a little so cards read on video
CHIP = ((0.0, (46, 48, 58)), (1.0, (18, 19, 24)))

CALL = '(301) 615-8289'        # the Honorbrook line: the only number shown or spoken as a call number
TEXT = '(571) 354-0146'        # shown only after the word "Text"
SITE = 'honorbrook-insurance.com'
DISCLAIMER = ('Honorbrook Insurance is an independent insurance agency, not connected with or endorsed by any government agency. '
              'General information, not insurance, tax or legal advice.')
END_QUESTION = 'Want to talk it through?'
END_PHR = [(END_QUESTION, END_QUESTION),
           ('Schedule a time at %s or call %s.' % (SITE, CALL),
            'Schedule a time at honorbrook insurance dot com, or call three zero one, six one five, eight two eight nine.')]

WARN = []                      # layout warnings collected while drawing (printed by check / sheet / still)
STATE = {'caps': None}


def warn(msg):
    if msg not in WARN: WARN.append(msg)


# ------------------------------------------------------------------ restyle the studio in memory (see the module docstring)
VS.BG0, VS.BG1 = OX0, OX2
VS.GOLD, VS.GOLDL = S3, S1
VS.SKY, VS.SKYD = (176, 186, 206), (96, 104, 120)
VS.TEAL, VS.INDIGO = GREEN, (96, 104, 120)
VS.CORAL, VS.CORALL = RED, (255, 185, 178)
VS.MUTED, VS.INK, VS.HILITE = MUTED, INK, WHITE
VS.BLOBS = [(0.84, 0.02, 0.62, (176, 186, 206), 0.17, 0.21, 0.16, 0.0), (0.06, 0.40, 0.60, (120, 128, 146), 0.10, 0.17, 0.23, 2.1),
            (0.50, 1.02, 0.60, (150, 156, 170), 0.09, 0.14, 0.19, 4.0), (0.30, 0.10, 0.40, (140, 146, 160), 0.06, 0.26, 0.20, 1.0)]


class Ctx(VS.Ctx):
    """The studio canvas with the Onyx background, the HB monogram and a black caption scrim.
    S(p, l): portrait pixels on 1080x1920, or landscape pixels on 1280x720. R(p, l): pick a ratio. land: True for 16:9."""

    def __init__(self, W, H):
        super().__init__(W, H)
        brand = os.path.join(ROOT, 'social', 'brand')
        mono = os.path.join(brand, 'hb-monogram.png')      # the mark the Onyx build ships as assets/hb-mark.png
        if os.path.exists(mono):
            self.mono = Image.open(mono).convert('RGBA'); hh = int(self.S(86, 44))
            self.logo = self.mono.resize((int(self.mono.width * hh / self.mono.height), hh), Image.LANCZOS)
        lock = os.path.join(brand, 'hb-logo-lockup.png')
        self.lockup = Image.open(lock).convert('RGBA') if os.path.exists(lock) else None
        sh = int(H * 0.34); grad = (np.linspace(0, 1, sh) ** 1.5 * 205).astype('uint8')
        self.scrim = Image.fromarray(np.repeat(grad[:, None], W, axis=1)); self.scrim_y = H - sh
        self.top, self.bot = self.S(560, 200), self.S(1385, 532)     # bottom of the scene area; captions live below it
        self.cap_y = self.S(1618, 614); self.strip_y = self.S(1852, 699)


ST.Ctx = Ctx


# ------------------------------------------------------------------ drawing: gradients, panels, marks
def _ramp(stops, g):
    pos = [p for p, _ in stops]
    return np.stack([np.interp(g, pos, [col[i] for _, col in stops]) for i in range(3)], axis=-1)


def gtext(img, x, y, s, f, stops=SILVER, a=1.0, anchor='la', span=None):
    """Text filled with a vertical gradient (SILVER for headings, CHROME for big figures). span=(y0, y1) pins the gradient to a line."""
    if a <= 0.004 or not s: return
    l, t_, r, b = f.getbbox(s, anchor=anchor); pad = 4; w, h = r - l + 2 * pad, b - t_ + 2 * pad
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).text((-l + pad, -t_ + pad), s, font=f, fill=255, anchor=anchor)
    top = y + t_ - pad
    g = np.clip((top + np.arange(h) - span[0]) / max(span[1] - span[0], 1), 0, 1) if span else np.linspace(0, 1, h)
    arr = np.repeat(_ramp(stops, g)[:, None, :], w, axis=1).astype('uint8')
    if a < 1: m = m.point(lambda v: int(v * a))
    img.paste(Image.fromarray(arr), (int(round(x + l - pad)), int(round(top))), m)


def _rr_mask(w, h, r, outline=0):
    m = Image.new('L', (w * 2, h * 2), 0); d = ImageDraw.Draw(m)
    if outline: d.rounded_rectangle([0, 0, w * 2 - 1, h * 2 - 1], radius=r * 2, outline=255, width=outline * 2)
    else: d.rounded_rectangle([0, 0, w * 2 - 1, h * 2 - 1], radius=r * 2, fill=255)
    return m.resize((w, h), Image.LANCZOS)


_PN, _GF = {}, {}


def panel(img, x0, y0, x1, y1, r, a=1.0, shadow=True, stops=PANEL, edge=1.0):
    """Onyx card: black lacquer gradient, a soft gloss from the top-left corner, a hairline silver edge that is brightest on top."""
    if a <= 0.01: return
    w, h = int(round(x1 - x0)), int(round(y1 - y0)); x0, y0 = int(round(x0)), int(round(y0))
    if w < 8 or h < 8: return
    r = int(max(2, min(r, w / 2, h / 2))); key = (w, h, r, stops, edge)
    if key not in _PN:
        m = _rr_mask(w, h, r)
        rgb = np.repeat(_ramp(stops, np.linspace(0, 1, h))[:, None, :], w, axis=1)
        yy, xx = np.mgrid[0:h, 0:w]; d = (xx * 0.47 + yy * 0.88) / (0.30 * (w * 0.47 + h * 0.88))
        rgb = rgb + (np.clip(1 - d, 0, 1) * 20)[..., None]                                     # gloss
        prof = np.interp(np.linspace(0, 1, h), [0, 0.36, 1], [0.50, 0.15, 0.22]) * edge       # edge light, top to bottom
        ba = (np.asarray(_rr_mask(w, h, r, outline=1), float) / 255) * prof[:, None]
        rgb = rgb * (1 - ba[..., None]) + 255 * ba[..., None]
        blur = 22; sm = Image.new('L', (w + 4 * blur, h + 4 * blur), 0)
        ImageDraw.Draw(sm).rounded_rectangle([2 * blur, 2 * blur, 2 * blur + w, 2 * blur + h], radius=r, fill=255)
        _PN[key] = (Image.fromarray(np.clip(rgb, 0, 255).astype('uint8')), m, sm.filter(ImageFilter.GaussianBlur(blur)), blur)
    im, m, sm, blur = _PN[key]
    if shadow: img.paste((0, 0, 0), (x0 - 2 * blur, y0 - 2 * blur + 16), sm.point(lambda v: int(v * 0.6 * a)))
    img.paste(im, (x0, y0), m if a >= 1 else m.point(lambda v: int(v * a)))


def gfill(img, x0, y0, x1, y1, r, stops=BTN, a=1.0):
    """Rounded shape filled with a vertical gradient (the chrome call button, the tick circle)."""
    if a <= 0.01: return
    w, h = int(round(x1 - x0)), int(round(y1 - y0))
    if w < 4 or h < 4: return
    r = int(max(1, min(r, w / 2, h / 2))); key = (w, h, r, stops)
    if key not in _GF:
        if len(_GF) > 400: _GF.clear()
        rgb = np.repeat(_ramp(stops, np.linspace(0, 1, h))[:, None, :], w, axis=1)
        _GF[key] = (Image.fromarray(rgb.astype('uint8')), _rr_mask(w, h, r))
    im, m = _GF[key]
    img.paste(im, (int(round(x0)), int(round(y0))), m if a >= 1 else m.point(lambda v: int(v * a)))


def _rect(img, x0, y0, x1, y1, color, a=1.0):
    shape(img, (x0, y0, x1, y1), color, a, lambda d, ss, w, h: d.rectangle([0, 0, w, h], fill=255))


def hair(img, x0, x1, y, a=1.0, color=WHITE, base=0.22):
    """Hairline rule (the thin silver line the site puts under headers)."""
    if a > 0.01 and x1 - x0 > 2: _rect(img, x0, y - 1, x1, y + 1, color, base * a)


def diamond(img, cx, cy, r, color=S2, a=1.0):
    """The site's list bullet: a small rotated square."""
    shape(img, (cx - r, cy - r, cx + r, cy + r), color, a, lambda d, ss, w, h: d.polygon([(w * ss / 2, 0), (w * ss, h * ss / 2), (w * ss / 2, h * ss), (0, h * ss / 2)], fill=255), ss=3)


def _stroke(d, pts, w, closed=False):
    pts = list(pts) + ([pts[0]] if closed else [])
    d.line(pts, fill=255, width=int(w), joint='curve')
    for p in pts: d.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=255)


STUDIO_GLYPHS = ('calendar', 'doc', 'shield', 'heart', 'cross', 'pill', 'pin', 'flag', 'clock', 'x')
KIT_GLYPHS = ('home', 'person', 'people', 'mail', 'umbrella', 'check', 'lock', 'scale', 'arrow', 'chat')
GLYPHS = STUDIO_GLYPHS + KIT_GLYPHS


def glyph(img, kind, cx, cy, s, color=S1, a=1.0):
    """Line icon in a box of side s. Names: GLYPHS."""
    if kind in STUDIO_GLYPHS: return VS.glyph(img, kind, cx, cy, s, color, a)
    S = int(s)

    def draw(d, ss, w, h):
        u = w * ss / 100.0; sw = 8 * u
        P_ = lambda *pts: [(x * u, y * u) for x, y in pts]
        if kind == 'home':
            _stroke(d, P_((12, 50), (50, 16), (88, 50)), sw); _stroke(d, P_((24, 46), (24, 86), (76, 86), (76, 46)), sw)
            _stroke(d, P_((43, 86), (43, 64), (57, 64), (57, 86)), sw * 0.8)
        elif kind == 'person':
            d.ellipse([34 * u, 12 * u, 66 * u, 44 * u], outline=255, width=int(sw))
            _stroke(d, P_((16, 90), (20, 72), (34, 60), (66, 60), (80, 72), (84, 90)), sw)
        elif kind == 'people':
            d.ellipse([22 * u, 18 * u, 48 * u, 44 * u], outline=255, width=int(sw * 0.9))
            _stroke(d, P_((8, 86), (12, 70), (24, 60), (46, 60), (58, 70), (62, 86)), sw * 0.9)
            d.ellipse([60 * u, 26 * u, 82 * u, 48 * u], outline=255, width=int(sw * 0.9))
            _stroke(d, P_((72, 62), (84, 66), (92, 86)), sw * 0.9)
        elif kind == 'mail':
            d.rounded_rectangle([10 * u, 24 * u, 90 * u, 78 * u], radius=8 * u, outline=255, width=int(sw))
            _stroke(d, P_((14, 30), (50, 56), (86, 30)), sw * 0.9)
        elif kind == 'umbrella':
            pts = [(50 + 38 * math.cos(math.pi * k / 16), 52 - 36 * math.sin(math.pi * k / 16)) for k in range(17)]
            _stroke(d, P_(*pts), sw, True); _stroke(d, P_((50, 52), (50, 80), (46, 88), (38, 88), (34, 80)), sw)
        elif kind == 'check':
            _stroke(d, P_((20, 52), (42, 74), (80, 28)), sw * 1.25)
        elif kind == 'lock':
            d.rounded_rectangle([20 * u, 46 * u, 80 * u, 90 * u], radius=9 * u, outline=255, width=int(sw))
            _stroke(d, P_((34, 46), (34, 32), (40, 20), (50, 16), (60, 20), (66, 32), (66, 46)), sw)
        elif kind == 'scale':
            _stroke(d, P_((16, 28), (84, 28)), sw); _stroke(d, P_((50, 16), (50, 86)), sw); _stroke(d, P_((32, 86), (68, 86)), sw)
            _stroke(d, P_((16, 28), (5, 58), (27, 58)), sw * 0.8, True); _stroke(d, P_((84, 28), (73, 58), (95, 58)), sw * 0.8, True)
        elif kind == 'arrow':
            _stroke(d, P_((16, 50), (84, 50)), sw * 1.1); _stroke(d, P_((60, 26), (84, 50), (60, 74)), sw * 1.1)
        elif kind == 'chat':
            _stroke(d, P_((14, 18), (86, 18), (86, 68), (48, 68), (30, 86), (30, 68), (14, 68)), sw, True)
            _stroke(d, P_((32, 36), (68, 36)), sw * 0.8); _stroke(d, P_((32, 51), (58, 51)), sw * 0.8)
    shape(img, (cx - S / 2, cy - S / 2, cx + S / 2, cy + S / 2), color, a, draw, ss=4)


def chip(img, cx, cy, size, what, a=1.0):
    """Onyx icon tile: dark rounded square with a bright top edge. `what` is a glyph name or a short text ('1', '$', '?')."""
    if a <= 0.01: return
    h = size / 2; panel(img, cx - h, cy - h, cx + h, cy + h, size * 0.27, a, shadow=False, stops=CHIP, edge=1.25)
    if what in GLYPHS: glyph(img, what, cx, cy, size * 0.54, S1, a)
    elif what: gtext(img, cx, cy, str(what), F('Heavy', size * (0.52 if len(str(what)) < 2 else 0.40)), SILVER, a, 'mm')


def mark(img, cx, cy, r, p, kind='check'):
    """The mark at the right end of a row: p runs 0 to 1. 'check' = chrome disc with a black tick; 'x' = dark disc with a soft red cross."""
    if p <= 0 or not kind: return
    rr = r * (eob(clamp(p / 0.55)) if p < 0.55 else 1.0)
    if kind == 'x':
        circle(img, cx, cy, rr, OX5, 1.0); circle(img, cx, cy, rr, RED, 0.75, outline=max(2, int(r * 0.12)))
        q = clamp((p - 0.3) / 0.5)
        if q > 0: glyph(img, 'x', cx, cy, r * 1.05, RED, q)
        return
    glow(img, cx, cy, rr * 2.0, ICE, 0.30, 2.5)
    if p < 0.55: circle(img, cx, cy, rr, S1, 1.0)
    else: gfill(img, cx - r, cy - r, cx + r, cy + r, r, BTN, 1.0)
    q = clamp((p - 0.3) / 0.6)
    if q > 0:
        a_, b_, c_ = (cx - r * 0.42, cy + r * 0.02), (cx - r * 0.1, cy + r * 0.36), (cx + r * 0.46, cy - r * 0.3)
        seg = [a_, (lerp(a_[0], b_[0], q * 2), lerp(a_[1], b_[1], q * 2))] if q < 0.5 else [a_, b_, (lerp(b_[0], c_[0], (q - 0.5) * 2), lerp(b_[1], c_[1], (q - 0.5) * 2))]
        shape(img, (cx - r, cy - r, cx + r, cy + r), INK, 1.0,
              lambda d, ss, w, h: d.line([((x - (cx - r)) * ss, (y - (cy - r)) * ss) for x, y in seg], fill=255, width=int(r * 0.22 * ss), joint='curve'), ss=3)


# ------------------------------------------------------------------ type
def fit(labels, weight, maxw, maxh, hi, lo, lh=1.2, step=2, what='text'):
    """Largest font (hi down to lo) at which every label wraps inside maxw x maxh. Warns when even `lo` does not fit."""
    labels = [s for s in labels if s]
    for size in range(int(hi), int(lo) - 1, -step):
        f = F(weight, size)
        if all(len(wrap(s, f, maxw)) * size * lh <= maxh and max(f.getlength(w) for w in s.split()) <= maxw for s in labels): return f
    warn('%s does not fit, shorten it: %s' % (what, max(labels, key=len)[:60]))
    return F(weight, lo)


def kicker(img, cx, y, s, f, a=1.0, track=0.24, color=S3):
    """Small tracked caps with a hairline on each side (the site's .kicker)."""
    if a <= 0.004 or not s: return
    s = s.upper(); adv = [f.getlength(ch) + f.size * track for ch in s]; tw = sum(adv) - f.size * track; x = cx - tw / 2
    for ch, w in zip(s, adv):
        text(img, x, y, ch, f, color, a, 'la'); x += w
    ym = y + f.size * 0.62; L = f.size * 1.7; g = f.size * 0.8
    hair(img, cx - tw / 2 - g - L, cx - tw / 2 - g, ym, a, base=0.45); hair(img, cx + tw / 2 + g, cx + tw / 2 + g + L, ym, a, base=0.45)


def headline(img, cx, y, lines, size, t, t0=0.0, stops=SILVER, weight='Heavy', lh=1.1):
    """Centred lines; words slide up and fade in one after another. Returns the y under the block."""
    f = F(weight, size); yy = y; n = 0
    for ln in lines:
        x = cx - f.getlength(ln) / 2
        for w in ln.split():
            p = eo3(prog(t, t0 + 0.07 * n, 0.5)); n += 1; oy = (1 - p) * size * 0.4
            gtext(img, x, yy + oy, w, f, stops, p, 'la', span=(yy + oy + size * 0.12, yy + oy + size * 1.02))
            x += f.getlength(w + ' ')
        yy += int(size * lh)
    return yy


def lines_block(img, x, y, s, f, fill, maxw, a=1.0, lh=1.25, align='center'):
    """Wrapped paragraph. x is the centre (align='center') or the left edge. Returns the y under the block."""
    for ln in wrap(s, f, maxw):
        text(img, x, y, ln, f, fill, a, 'ma' if align == 'center' else 'la'); y += int(f.size * lh)
    return y


def title(c, img, t, over=None, head=None, t0=0.0):
    """Kicker + headline at the top of a scene. Returns the y where the scene's own content may start."""
    y = c.S(292, 90)
    if over: kicker(img, c.cx, y, over, F('Bold', c.S(31, 19)), eo3(prog(t, t0, 0.4)))
    y += c.S(58, 31)
    if not head: return y + c.S(24, 8)
    maxw = c.W * c.R(0.90, 0.86); size = int(c.S(86, 50)); maxl = c.R(3, 2)
    while True:
        f = F('Heavy', size); L = []
        for part in ([head] if isinstance(head, str) else head): L += wrap(part, f, maxw)
        if len(L) <= maxl or size <= c.S(60, 38): break
        size -= 4
    if len(L) > maxl: warn('headline is too long, shorten it: %s' % (head if isinstance(head, str) else ' '.join(head))[:60])
    return headline(img, c.cx, y, L, size, t, t0 + 0.08) + c.S(34, 18)


def note_line(c, img, t, s, y=None, t0=0.5):
    """Small muted line at the bottom of the scene area (a source, a qualifier). Returns the height it uses."""
    if not s: return 0
    f = F('Medium', c.S(30, 21)); maxw = c.W * c.R(0.86, 0.84); L = wrap(s, f, maxw)
    if len(L) > 2: warn('note is too long, shorten it: %s' % s[:60])
    hgt = len(L) * int(f.size * 1.3); y = (c.bot - hgt) if y is None else y
    lines_block(img, c.cx, y, s, f, S3, maxw, eo3(prog(t, t0, 0.5)), 1.3)
    return hgt + c.S(22, 12)


def pill(c, img, cy, s, a=1.0, size=None, dot=True, maxw=None):
    """Capsule panel with a centred line of text (a short takeaway). Returns its height."""
    f = F('Bold', size or c.S(42, 29)); maxw = maxw or (c.W * c.R(0.86, 0.80) - c.S(150, 90))
    L = wrap(s, f, maxw); lw = max(f.getlength(l) for l in L)
    w = lw + c.S(150, 90); h = len(L) * f.size * 1.22 + c.S(54, 30)
    if a <= 0.01: return h
    oy = (1 - a) * c.S(30, 16); x0 = c.cx - w / 2
    panel(img, x0, cy - h / 2 + oy, x0 + w, cy + h / 2 + oy, min(h / 2, c.S(60, 34)), a)
    if dot: diamond(img, x0 + c.S(54, 32), cy + oy, c.S(10, 6), S1, a)
    for j, ln in enumerate(L): text(img, c.cx + (c.S(20, 12) if dot else 0), cy + oy + (j - (len(L) - 1) / 2) * f.size * 1.22, ln, f, S1, a, 'mm')
    return h


def cues(ph, n, start=0, at=None):
    """When each of n items shows and when it is 'done', from the phrase times. Item i rides phrase start+i (or at[i]).
    Items that land on the same phrase are spread across it. Returns [(show, done)] in scene seconds."""
    idx = [min(max(int(k), 0), len(ph) - 1) for k in (at if at is not None else [start + i for i in range(n)])]
    out = []
    for i, k in enumerate(idx):
        same = [j for j in range(n) if idx[j] == k]; a, b = ph[k]; d = (b - a) / len(same); j = same.index(i)
        out.append((a + j * d, a + (j + 1) * d))
    return out


# ------------------------------------------------------------------ scene builders (each returns draw(c, img, t, ph))
def _texts(draw, *parts):
    out = []
    for p in parts:
        if isinstance(p, str): out.append(p)
        elif isinstance(p, (list, tuple)): out += [x for x in _flatten(p) if isinstance(x, str)]
    draw.texts = out
    return draw


def _flatten(x):
    for y in x:
        if isinstance(y, (list, tuple)): yield from _flatten(y)
        else: yield y


def hook(over, title_lines, sub=None, sub_at=1, icon=None):
    """Opening scene: a kicker and a very large headline, with an optional takeaway capsule.
    over: small caps line above (e.g. 'Life insurance'). title_lines: a string (auto-wrapped) or a list of lines (your own breaks).
    sub: short line in a capsule under the headline; it appears when phrase `sub_at` starts (default the 2nd phrase;
    with one phrase it appears two thirds of the way through). icon: optional glyph name shown above the headline."""
    given = [title_lines] if isinstance(title_lines, str) else list(title_lines)

    def draw(c, img, t, ph):
        y0 = title(c, img, t, over); y1 = c.bot
        subh = (pill(c, img, 0, sub, 0) + c.S(40, 22)) if sub else 0
        ich = c.S(150, 84) if icon else 0
        maxw = c.W * c.R(0.88, 0.84); room = y1 - y0 - subh - ich
        for size in range(int(c.S(132, 92)), int(c.S(64, 44)) - 1, -4):
            f = F('Black', size); L = []
            for ln in given: L += wrap(ln, f, maxw)
            if len(L) * int(size * 1.12) <= room and len(L) <= max(len(given), c.R(4, 2)) and all(f.getlength(w) <= maxw for ln in L for w in ln.split()): break
        else: warn('hook headline is too long, shorten it: %s' % ' '.join(given)[:60])
        bh = len(L) * int(size * 1.12); y = y0 + (room - bh) / 2 + ich; cy = y + bh / 2
        a = eo3(prog(t, 0.1, 0.6)); pulse = 0.85 + 0.15 * math.sin(t * 2.0)
        glow(img, c.cx, cy, c.S(620, 420), ICE, 0.16 * a * pulse, 2.2)
        for k in range(2):
            q = ((t * 0.22) + k / 2) % 1.0
            ring_line(img, c.cx, cy, lerp(c.S(300, 190), c.S(640, 430), q), c.S(3, 2), S2, (1 - q) * 0.16 * a)
        if icon: chip(img, c.cx, y - ich / 2 - c.S(6, 2), c.S(112, 62), icon, eo3(prog(t, 0.05, 0.4)))
        headline(img, c.cx, y, L, size, t, 0.12, SILVER, 'Black', 1.12)
        if sub:
            ts = ph[min(sub_at, len(ph) - 1)][0] if len(ph) > sub_at else ph[0][0] + (ph[0][1] - ph[0][0]) * 0.66
            pill(c, img, y + bh + c.S(40, 22) + (subh - c.S(40, 22)) / 2, sub, eo3(prog(t, ts, 0.5)))
    return _texts(draw, over, given, sub)


def checklist(over, head, items, start=0, at=None, mark_kind='check', icons=None, note=None):
    """Rows that slide in one per phrase, each with a mark that lands as its phrase ends.
    items: 2 to 5 short labels (aim for under 45 characters). start: index of the phrase that brings in the first row
    (use 1 when the scene opens with an intro phrase). at: explicit phrase index per row instead of start.
    icons: list of glyph names or short texts for the left tile (default 1, 2, 3 ...). mark_kind: 'check', 'x', None,
    or a list with one of those per row. note: small line under the rows (a source or a qualifier)."""
    items = list(items); n = len(items)
    icons = list(icons) if icons else [str(i + 1) for i in range(n)]
    kinds = list(mark_kind) if isinstance(mark_kind, (list, tuple)) else [mark_kind] * n

    def draw(c, img, t, ph):
        y0 = title(c, img, t, over, head); y1 = c.bot - note_line(c, img, t, note)
        gap = c.S(26, 11); cw = c.W * c.R(0.88, 0.84); x0 = c.cx - cw / 2
        h = min(c.S(196, 84), (y1 - y0 - (n - 1) * gap) / n); cs = min(h * 0.62, c.S(100, 52)); pad = c.S(34, 18)
        tx = pad + cs + c.S(30, 20); tw = cw - tx - (c.S(128, 78) if any(kinds) else pad)
        f = fit(items, 'Bold', tw, h - c.S(26, 12), c.S(46, 33), c.S(32, 23), what='checklist row')
        top = y0 + (y1 - y0 - (n * h + (n - 1) * gap)) / 2; cu = cues(ph, n, start, at)
        for i, lab in enumerate(items):
            y = top + i * (h + gap) + 3 * math.sin(t * 1.3 + i) * c.k
            p = eo3(prog(t, cu[i][0] - 0.05, 0.45)); gh = eo3(prog(t, 0.3 + 0.08 * i, 0.5)) * (1 - p)
            if gh > 0.01: rrect(img, x0, y, x0 + cw, y + h, c.S(34, 18), WHITE, 0.10 * gh, outline=2)
            if p <= 0.004: continue
            sl = (1 - p) * c.S(70, 36)
            panel(img, x0 + sl, y, x0 + cw + sl, y + h, c.S(34, 18), p)
            chip(img, x0 + sl + pad + cs / 2, y + h / 2, cs, icons[i % len(icons)], p)
            L = wrap(lab, f, tw)
            for j, ln in enumerate(L): text(img, x0 + sl + tx, y + h / 2 + (j - (len(L) - 1) / 2) * f.size * 1.2, ln, f, S1, p, 'lm')
            mark(img, x0 + sl + cw - c.S(72, 42), y + h / 2, min(c.S(34, 19), h * 0.3), prog(t, cu[i][1] - 0.4, 0.5), kinds[i])
    draw.sfx = lambda ph: [(max(b - 0.35, 0), 'ding' if kinds[i] != 'x' else 'tick') for i, (a, b) in enumerate(cues(ph, n, start, at)) if kinds[i]]
    return _texts(draw, over, head, items, note)


def timeline(over, head, points, start=0, at=None, note=None):
    """A line with 2 to 4 stops that light up one per phrase (left to right on 16:9, top to bottom on 9:16).
    points: [(big, label), ...] e.g. [('Day 1', 'Coverage starts'), ('Year 2', '...')]. Keep `big` under 9 characters and
    `label` under 40. start / at: as in checklist. note: small line under the timeline."""
    pts = [tuple(p) for p in points]; n = len(pts)

    def draw(c, img, t, ph):
        y0 = title(c, img, t, over, head); y1 = c.bot - note_line(c, img, t, note); cu = cues(ph, n, start, at)
        prg = sum(prog(t, cu[i][0], max(cu[i + 1][0] - cu[i][0], 0.3)) for i in range(n - 1)) / max(n - 1, 1)
        if c.land:
            span = c.W * (0.50 if n == 2 else 0.66 if n == 3 else 0.74); step = span / (n - 1) if n > 1 else 0
            xs = [c.cx - span / 2 + i * step for i in range(n)]; colw = (step if n > 1 else c.W * 0.6) - c.S(0, 26)
            fb = fit([b for b, _ in pts], 'Black', colw, 200, c.S(0, 62), c.S(0, 38), lh=1.0, what='timeline stop')
            fl = fit([l for _, l in pts], 'Semibold', colw, c.S(0, 104), c.S(0, 29), c.S(0, 22), lh=1.22, what='timeline label')
            blockh = fb.size + c.S(0, 30) + c.S(0, 34) + 3 * fl.size * 1.22; yl = y0 + (y1 - y0 - blockh) / 2 + fb.size + c.S(0, 30)
            _rect(img, xs[0], yl - 2, xs[-1], yl + 2, S4, 0.55)
            if prg > 0.003: _rect(img, xs[0], yl - 2, xs[0] + (xs[-1] - xs[0]) * prg, yl + 2, S1, 1.0)
            for i, (big, lab) in enumerate(pts):
                p = eob(prog(t, cu[i][0], 0.5)); q = clamp(p); early = eo3(prog(t, 0.3 + 0.1 * i, 0.5))
                circle(img, xs[i], yl, c.S(0, 11), OX5, early); circle(img, xs[i], yl, c.S(0, 11), S3, early * 0.9, outline=2)
                if q > 0.02:
                    glow(img, xs[i], yl, c.S(0, 46) * q, ICE, 0.38, 2.2); circle(img, xs[i], yl, c.S(0, 13) * p, S1, 1.0)
                gtext(img, xs[i], yl - c.S(0, 26) - fb.size * 0.5, big, fb, CHROME if q > 0.5 else SILVER, max(q, early * 0.30), 'mm')
                lines_block(img, xs[i], yl + c.S(0, 30), lab, fl, S1, colw, q, 1.22)
        else:
            lx = c.S(150, 0); step = min(c.S(330, 0), (y1 - y0) / n); tw = c.W - lx - c.S(90, 0) - c.S(80, 0)
            fb = fit([b for b, _ in pts], 'Black', tw, 200, 84, 56, lh=1.0, what='timeline stop')
            fl = fit([l for _, l in pts], 'Semibold', tw, step - fb.size - 50, 42, 32, lh=1.22, what='timeline label')
            top = y0 + (y1 - y0 - n * step) / 2 + 56; ys = [top + i * step for i in range(n)]
            _rect(img, lx - 3, ys[0], lx + 3, ys[-1], S4, 0.55)
            if prg > 0.003: _rect(img, lx - 3, ys[0], lx + 3, ys[0] + (ys[-1] - ys[0]) * prg, S1, 1.0)
            for i, (big, lab) in enumerate(pts):
                p = eob(prog(t, cu[i][0], 0.5)); q = clamp(p); early = eo3(prog(t, 0.3 + 0.1 * i, 0.5))
                circle(img, lx, ys[i], 22, OX5, early); circle(img, lx, ys[i], 22, S3, early * 0.9, outline=3)
                if q > 0.02:
                    glow(img, lx, ys[i], 86 * q, ICE, 0.38, 2.2); circle(img, lx, ys[i], 26 * p, S1, 1.0)
                gtext(img, lx + 80, ys[i], big, fb, CHROME if q > 0.5 else SILVER, max(q, early * 0.30), 'lm')
                lines_block(img, lx + 80, ys[i] + fb.size * 0.62, lab, fl, S1, tw, q, 1.22, align='left')
    draw.sfx = lambda ph: [(a + 0.05, 'ding') for a, b in cues(ph, n, start, at)]
    return _texts(draw, over, head, pts, note)


def two_column(over, head, left, right, left_at=0, right_at=1, note=None, left_mark='dot', right_mark='dot'):
    """Two cards to compare (side by side on 16:9, stacked on 9:16). left / right: (title, [row, row, ...]) with 2 to 4 short rows each.
    left_at / right_at: the phrase that brings the card in; its rows then appear across that phrase. Pass a list of
    phrase indexes (one per row) to bring each row in with its own phrase; the card arrives with the first.
    left_mark / right_mark: 'dot' (bullet), 'check' or 'x' in front of each row. note: small line under the cards."""
    cols = [(left[0], list(left[1]), left_at, left_mark), (right[0], list(right[1]), right_at, right_mark)]

    def draw(c, img, t, ph):
        y0 = title(c, img, t, over, head); y1 = c.bot - note_line(c, img, t, note); gap = c.S(30, 28); m = c.W * c.R(0.06, 0.06)
        if c.land: w = (c.W - 2 * m - gap) / 2; boxes = [(m, y0, m + w, y1), (m + w + gap, y0, c.W - m, y1)]
        else: hh = (y1 - y0 - gap) / 2; boxes = [(m, y0, c.W - m, y0 + hh), (m, y0 + hh + gap, c.W - m, y1)]
        pad = c.S(44, 30); ft_hi = c.S(52, 34)
        for ci, ((ttl, rows, at_, mk), (bx0, by0, bx1, by1)) in enumerate(zip(cols, boxes)):
            nr = len(rows); rc = cues(ph, nr, 0, at_ if isinstance(at_, (list, tuple)) else [at_] * nr)
            t_in = rc[0][0]; p = eo3(prog(t, t_in - 0.05, 0.5)); gh = eo3(prog(t, 0.3 + 0.1 * ci, 0.5)) * (1 - p)
            if gh > 0.01: rrect(img, bx0, by0, bx1, by1, c.S(36, 20), WHITE, 0.10 * gh, outline=2)
            if p <= 0.004: continue
            dx = (1 - p) * c.S(0, 40) * (-1 if ci == 0 else 1); dy = (1 - p) * c.S(50, 0)
            panel(img, bx0 + dx, by0 + dy, bx1 + dx, by1 + dy, c.S(36, 20), p)
            iw = bx1 - bx0 - 2 * pad; ft = fit([ttl], 'Heavy', iw, ft_hi * 2.3, ft_hi, c.S(38, 26), lh=1.1, what='column title')
            tl_ = wrap(ttl, ft, iw); yy = by0 + dy + pad * 0.9
            for ln in tl_:
                gtext(img, bx0 + dx + pad, yy, ln, ft, SILVER, p, 'la'); yy += int(ft.size * 1.1)
            yy += c.S(14, 8); hair(img, bx0 + dx + pad, bx1 + dx - pad, yy, p); yy += c.S(26, 14)
            bw = c.S(46, 32); room = by1 + dy - pad * 0.8 - yy
            rg = c.S(20, 10); fr = None
            for size in range(int(c.S(42, 29)), int(c.S(30, 21)) - 1, -1):
                f_ = F('Semibold', size)
                if sum(len(wrap(r_, f_, iw - bw)) * int(size * 1.22) for r_ in rows) + (nr - 1) * rg <= room: fr = f_; break
            if fr is None:
                fr = F('Semibold', c.S(30, 21)); warn('column "%s" has too much text, shorten or drop a row' % ttl[:40])
            used = sum(len(wrap(r_, fr, iw - bw)) * int(fr.size * 1.22) for r_ in rows) + (nr - 1) * rg
            yy += max(0, (room - used) * 0.35)
            for j, r_ in enumerate(rows):
                ts = rc[j][0] + (0.25 if not isinstance(at_, (list, tuple)) else 0.0); q = eo3(prog(t, ts, 0.4)) * p; ox = (1 - q) * c.S(24, 14)
                L = wrap(r_, fr, iw - bw); bx = bx0 + dx + pad + c.S(14, 9); byc = yy + fr.size * 0.62
                if mk == 'check': glyph(img, 'check', bx, byc, c.S(34, 22), S1, q)
                elif mk == 'x': glyph(img, 'x', bx, byc, c.S(30, 20), RED, q)
                else: diamond(img, bx, byc, c.S(8, 5), S2, q)
                for ln in L:
                    text(img, bx0 + dx + pad + bw + ox, yy, ln, fr, S1, q, 'la'); yy += int(fr.size * 1.22)
                yy += rg
    return _texts(draw, over, head, left, right, note)


def fact_card(over, big, lines=(), source=None, head=None, start=None, at=None):
    """One card with one large line and supporting lines under it, plus a source line.
    big: the large chrome line (a number, a date, two or three words). lines: 0 to 3 short supporting lines (under 60 characters).
    source: small line under the card, e.g. 'Source: irs.gov, Publication 525 (2025)'. head: optional headline above the card.
    Supporting line i appears with phrase start+i; start defaults to 1 when the scene has more phrases than lines, else 0."""
    lines = list(lines)

    def draw(c, img, t, ph):
        y0 = title(c, img, t, over, head); y1 = c.bot - note_line(c, img, t, source)
        pw = c.W * c.R(0.88, 0.84); pad = c.S(60, 40); iw = pw - 2 * pad
        fl = fit(lines, 'Semibold', iw, 400, c.S(44, 30), c.S(34, 23), lh=1.24, what='fact line') if lines else None
        lg = c.S(22, 10); lh_ = sum(len(wrap(s, fl, iw)) * int(fl.size * 1.24) for s in lines) + max(len(lines) - 1, 0) * lg if lines else 0
        sep = c.S(64, 34) if lines else 0
        for size in range(int(c.S(190, 112)), int(c.S(76, 50)) - 1, -4):
            fb = F('Black', size); B = wrap(big, fb, iw); bh = len(B) * int(size * 1.08)
            if len(B) <= c.R(3, 2) and all(fb.getlength(w) <= iw for w in big.split()) and 2 * pad * 0.8 + bh + sep + lh_ <= y1 - y0: break
        else: warn('fact card has too much text, shorten it: %s' % big[:50])
        H = 2 * pad * 0.8 + bh + sep + lh_; py = y0 + (y1 - y0 - H) / 2; a = eo3(prog(t, 0.1, 0.5)); oy = (1 - a) * c.S(30, 16)
        glow(img, c.cx, py + H * 0.4, pw * 0.62, ICE, 0.13 * a * (0.85 + 0.15 * math.sin(t * 2.0)), 2.2)
        panel(img, c.cx - pw / 2, py + oy, c.cx + pw / 2, py + H + oy, c.S(44, 26), a)
        yy = py + oy + pad * 0.8; pop = eo3(prog(t, 0.2, 0.5))
        for ln in B:
            gtext(img, c.cx, yy + (1 - pop) * size * 0.25, ln, fb, CHROME, pop, 'ma', span=(yy + size * 0.14, yy + size * 1.0)); yy += int(size * 1.08)
        if lines:
            b0 = eo3(prog(t, 0.5, 0.5)); hair(img, c.cx - iw * 0.5, c.cx + iw * 0.5, yy + sep * 0.42, a * b0); yy += sep
            st = start if start is not None else (1 if len(ph) > len(lines) else 0); cu = cues(ph, len(lines), st, at)
            for i, s in enumerate(lines):
                q = eo3(prog(t, cu[i][0], 0.45))
                yy = lines_block(img, c.cx, yy + (1 - q) * c.S(18, 10), s, fl, S1, iw, q, 1.24) - (1 - q) * c.S(18, 10) + lg
    return _texts(draw, over, big, lines, source, head)


def end(question=END_QUESTION):
    """Closing card: the HB lockup, the soft next step, the site, the chrome Call button, the Text line and the disclaimer.
    Use K.end_scene() rather than calling this directly, so the narration and captions are the standard ones."""
    def draw(c, img, t, ph):
        a = eo3(prog(t, 0.0, 0.5)); t1 = ph[min(1, len(ph) - 1)][0]; b = eo3(prog(t, t1 - 0.1, 0.5)); d = eo3(prog(t, t1 + 0.5, 0.5)); e = eo3(prog(t, 0.6, 0.6))

        def lock(cx, y, hgt):
            if not c.lockup: return
            lg = c.lockup.resize((int(c.lockup.width * hgt / c.lockup.height), int(hgt)), Image.LANCZOS)
            if a < 1: lg.putalpha(lg.getchannel('A').point(lambda v: int(v * a)))
            glow(img, cx, y + hgt * 0.42, hgt * 1.25, ICE, 0.12 * a, 2.2); img.paste(lg, (int(cx - lg.width / 2), int(y)), lg)

        def contact(cx, y, w):
            kicker(img, cx, y, 'Schedule a time', F('Bold', c.S(30, 19)), b); y += c.S(54, 32)
            fw = fit([SITE], 'Bold', w, 200, c.S(64, 42), c.S(44, 30), lh=1.0)
            gtext(img, cx, y, SITE, fw, SILVER, b, 'ma'); y += fw.size + c.S(44, 24)
            bh = c.S(150, 84); bw = min(w, c.S(880, 540)); pulse = 0.85 + 0.15 * math.sin(t * 3)
            glow(img, cx, y + bh / 2, bw * 0.72, ICE, 0.22 * d * pulse, 2.2)
            gfill(img, cx - bw / 2, y, cx + bw / 2, y + bh, c.S(36, 20), BTN, d)
            text(img, cx, y + bh / 2 + 1, 'Call ' + CALL, F('Heavy', c.S(74, 44)), INK, d, 'mm'); y += bh + c.S(34, 20)
            text(img, cx, y, 'Text ' + TEXT, F('Semibold', c.S(52, 33)), S1, d, 'ma')
            return y + c.S(62, 40)

        fd = F('Regular', c.S(29, 21)); dw = c.W * c.R(0.86, 0.84); dl = wrap(DISCLAIMER, fd, dw); dh = len(dl) * int(fd.size * 1.36)
        if c.land:
            lx, rx = c.W * 0.27, c.W * 0.70; top = c.S(0, 92); bot = c.bot - dh - c.S(0, 20)
            lock(lx, top + 6, c.S(0, 176))
            fq = fit([question], 'Heavy', c.W * 0.40, 130, c.S(0, 48), c.S(0, 34), lh=1.1)
            headline(img, lx, top + c.S(0, 206), wrap(question, fq, c.W * 0.40), fq.size, t, 0.1)
            _rect(img, c.W * 0.49 - 1, top + 20, c.W * 0.49 + 1, bot - 16, WHITE, 0.14 * a)
            contact(rx, top + c.S(0, 26), c.W * 0.40)
            hair(img, c.cx - dw / 2, c.cx + dw / 2, c.bot - dh - c.S(0, 12), e, base=0.16)
            lines_block(img, c.cx, c.bot - dh, DISCLAIMER, fd, S3, dw, e, 1.36)
        else:
            lock(c.cx, 232, 300)
            fq = fit([question], 'Heavy', c.W * 0.88, 200, 84, 60, lh=1.1)
            y = headline(img, c.cx, 580, wrap(question, fq, c.W * 0.88), fq.size, t, 0.1) + 60
            y = contact(c.cx, y, c.W * 0.86)
            hair(img, c.cx - dw / 2, c.cx + dw / 2, c.bot - dh - 22, e, base=0.16)
            lines_block(img, c.cx, c.bot - dh, DISCLAIMER, fd, S3, dw, e, 1.36)
    draw.is_end = True
    return _texts(draw, question, 'Call ' + CALL, 'Text ' + TEXT, SITE, DISCLAIMER)


# ------------------------------------------------------------------ scene and video helpers
def P(cap, say=None):
    """One narration phrase: (caption on screen, words to speak). Give `say` when the voice needs help: numbers as words,
    'honorbrook insurance dot com', a comma where it should breathe. The caption must carry the same words."""
    return (cap, say if say else cap)


def scene(draw, phr, sfx=None, pre=0.15, post=0.7):
    """A scene dict for VIDEO['scenes']. phr: list of P(...). sfx: None = the builder's own cue sounds (checklist and timeline
    have them), False = none, or a function ph -> [(seconds, 'ding'|'tick'|'thump')]. pre / post: silence before the first
    phrase and after the last (seconds)."""
    sc = dict(phr=[tuple(p) if not isinstance(p, str) else P(p) for p in phr], draw=draw, pre=pre, post=post)
    fx = getattr(draw, 'sfx', None) if sfx is None else sfx
    if fx: sc['sfx'] = fx
    return sc


def end_scene(question=END_QUESTION):
    """The standard last scene: end card + the standard two phrases (soft next step, site, call number)."""
    phr = [(question, question), END_PHR[1]]
    return scene(end(question), phr, sfx=lambda ph: [(ph[min(1, len(ph) - 1)][0] + 0.55, 'ding')], pre=0.1, post=1.6)


# ------------------------------------------------------------------ overlay: brand corner, footer strip, captions
def _tracked(img, x, y, s, f, color, a, track):
    for ch in s:
        text(img, x, y, ch, f, color, a, 'lm'); x += f.getlength(ch) + f.size * track
    return x


def caption(c, img, t, cap):
    s, e, words = cap
    a = clamp((t - (s - 0.08)) / 0.16) * clamp(((e + 0.5) - t) / 0.25)
    if a <= 0: return
    f = F('Heavy', int(c.S(60, 40))); maxw = int(c.W * c.R(0.88, 0.80))
    lines = wrap(' '.join(words), f, maxw); lh = int(f.size * 1.2)
    wts = [len(w) + 2 for w in words]; tot = sum(wts); p = clamp((t - s) / max(e - s, 0.2)) * 1.03
    y = c.cap_y - len(lines) * lh / 2; done = 0; idx = 0
    for ln in lines:
        x = c.cx - f.getlength(ln) / 2
        text_shadow(img, c.cx, y, ln, f, a, 'ma', blur=int(c.S(9, 6)), dy=int(c.S(5, 3)), sa=0.85)
        for w in ln.split():
            ww = f.getlength(w); mid = done + wts[idx] / 2
            if done <= p * tot < done + wts[idx]:
                pop = 1 + 0.03 * math.sin(clamp((p * tot - done) / max(wts[idx], 1) * 3) * math.pi)
                text(img, x + ww / 2, y + f.size * 0.55, w, F('Heavy', int(f.size * pop)), WHITE, a, 'mm')
            else:
                text(img, x, y, w, f, (236, 238, 242) if mid <= p * tot else (166, 172, 184), a, 'la')
            x += f.getlength(w + ' '); done += wts[idx]; idx += 1
        y += lh


def overlay(c, img, t, total, cap):
    W = c.W; bar = int(c.S(6, 4))
    _rect(img, 0, 0, W, bar, WHITE, 0.10); _rect(img, 0, 0, int(W * clamp(t / total)), bar, S2, 1.0)
    bx, by = c.S(54, 30), c.S(62, 22); lw = 0
    if c.logo:
        img.paste(c.logo, (int(bx), int(by)), c.logo); lw = c.logo.width
    tx = bx + lw + c.S(22, 14); cy = by + (c.logo.height if c.logo else c.S(86, 44)) / 2
    _tracked(img, tx, cy - c.S(15, 8), 'HONORBROOK', F('Semibold', c.S(34, 20)), S1, 1.0, 0.26)
    _tracked(img, tx + 2, cy + c.S(24, 13), 'INSURANCE', F('Medium', c.S(21, 13)), S3, 1.0, 0.52)
    text(img, W / 2, c.strip_y, '%s   ·   Call %s' % (SITE, CALL), F('Semibold', c.S(31, 20)), S3, 1.0, 'mm')
    caps = STATE.get('caps')
    if caps:      # the newest line that has started wins (the studio keeps the previous line up about half a second too long)
        live = [x for x in caps if x[0] - 0.08 <= t <= x[1] + 0.7]; cap = live[-1] if live else None
    if cap:
        img.paste((0, 0, 0), (0, c.scrim_y), c.scrim); caption(c, img, t, cap)
        text(img, W / 2, c.strip_y, '%s   ·   Call %s' % (SITE, CALL), F('Semibold', c.S(31, 20)), S3, 1.0, 'mm')


ST.overlay = overlay
_studio_prepare = ST.prepare


def _prepare(name):
    r = _studio_prepare(name); STATE['caps'] = r[5]; return r


if getattr(ST.prepare, '__name__', '') != '_prepare': ST.prepare = _prepare


# ------------------------------------------------------------------ driver
def slugs(): return sorted(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(VDIR, '*.py')))


def load(slug):
    """Load scripts/videos_life/<slug>.py (or a path to a .py file), fill the defaults and register it with the studio."""
    path = slug if slug.endswith('.py') else os.path.join(VDIR, slug + '.py')
    if not os.path.exists(path): raise SystemExit('No such video file: %s (have: %s)' % (path, ', '.join(slugs())))
    stem = os.path.basename(path)[:-3]
    spec = importlib.util.spec_from_file_location('videos_life_' + re.sub(r'\W', '_', stem), path); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    v = mod.VIDEO
    if v.setdefault('slug', stem) != stem: raise SystemExit("VIDEO['slug'] is %r but the file is %s.py; they must match." % (v['slug'], stem))
    v.setdefault('title', stem); v.setdefault('poster', 2.5); v.setdefault('disclaimer', DISCLAIMER); v.setdefault('description', '')
    v.setdefault('vdesc', v['description']); v.setdefault('sources', [])
    VS.VIDEOS[stem] = v
    return stem, v


def _out_dir(args):
    d = args[args.index('--out') + 1] if '--out' in args else os.environ.get('VIDEO_STILL_DIR', ST.SCRATCH)
    os.makedirs(d, exist_ok=True); return d


def _print_times(v, tl, total):
    for i, (sc, s) in enumerate(zip(v['scenes'], tl)):
        print('scene %d  %6.2f - %6.2f s' % (i + 1, s['t0'], s['t1']))
        for (cap, _), (a, b) in zip(sc['phr'], s['ph']): print('    %6.2f - %6.2f  %s' % (a, b, cap))
    print('total %.1f s' % total)


def _print_warn():
    for w in WARN: print('LAYOUT:', w)


def cmd_times(slug):
    name, v = load(slug); video, tmp, mix_, tl, total, caps = ST.prepare(name); _print_times(v, tl, total)


def cmd_still(slug, t, f, args):
    name, v = load(slug); video, tmp, mix_, tl, total, caps = ST.prepare(name)
    c = ST.Ctx(*ST.fmt_size(f)); out = os.path.join(_out_dir(args), '%s-%s-%.1f.png' % (name, f, t))
    ST.render_frame(c, video, tl, total, t, caps).save(out); _print_warn(); print(out, '(total %.1f s)' % total)


def cmd_sheet(slug, fmts, args):
    """One frame per scene, taken just before the scene ends (everything revealed), tiled into one PNG per format."""
    name, v = load(slug); video, tmp, mix_, tl, total, caps = ST.prepare(name); outd = _out_dir(args)
    for f in fmts:
        c = ST.Ctx(*ST.fmt_size(f)); tw, th = (640, 360) if f == 'land' else (405, 720); n = len(tl)
        cols = min(n, 3 if f == 'land' else 4); rows = int(math.ceil(n / cols))
        sheet = Image.new('RGB', (cols * tw + (cols + 1) * 8, rows * th + (rows + 1) * 8), (40, 42, 48))
        for i, s in enumerate(tl):
            tt = max(s['t0'] + 0.4, min(s['t1'] - 0.3, s['ph'][-1][1] + 0.25))
            im = ST.render_frame(c, video, tl, total, tt, caps).convert('RGB').resize((tw, th), Image.LANCZOS)
            ImageDraw.Draw(im).text((tw - 8, 8), '%d  %.1fs' % (i + 1, tt), font=F('Bold', 15), fill=(255, 255, 255), anchor='ra')
            sheet.paste(im, (8 + (i % cols) * (tw + 8), 8 + (i // cols) * (th + 8)))
        out = os.path.join(outd, '%s-%s-sheet.png' % (name, f)); sheet.save(out); print(out)
    _print_warn(); print('total %.1f s' % total)


RULES = [(r'\$\s?0\b', '"$0"'), (r'\bfree\b', '"free"'), (r'\b(best|lowest|cheapest|most|top|number one)\b|#1', 'superlative'),
         (r'\b(never|always|guarantee[ds]?)\b', 'guarantee word'), (r'\bscams?\b', '"scam"'), (r'\bmedicare\b', 'Medicare'),
         (r"\b(act now|hurry|limited time|don.?t wait|do not wait|last chance|too late|right away|today only|running out|before it)\b", 'urgency'),
         (r'\$\s?\d', 'dollar amount (only a dated figure from a government page)')]
PHONE = re.compile(r'\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b')


def cmd_check(slug):
    """Lint a video: wording rules, phone numbers, caption length, layout fit in both formats, end card, duration."""
    name, v = load(slug); probs = []; notes = []
    scenes = v['scenes']
    for i, sc in enumerate(scenes):
        texts = [('caption', cap) for cap, _ in sc['phr']] + [('spoken', say) for _, say in sc['phr']] + [('screen', s) for s in getattr(sc['draw'], 'texts', [])]
        for kind, s in texts:
            if getattr(sc['draw'], 'is_end', False) and kind == 'screen': continue
            for rx, label in RULES:
                for m in re.finditer(rx, s, re.I): notes.append('scene %d %s: %s "%s" in: %s' % (i + 1, kind, label, m.group(0), s[:70]))
            for m in PHONE.finditer(s):
                num = re.sub(r'\D', '', m.group(0)); before = s[:m.start()].rstrip().lower()
                if num == '3016158289': continue
                if num == '5713540146' and before.endswith('text'): continue
                probs.append('scene %d %s: phone number not allowed here: %s' % (i + 1, kind, s[:70]))
        for cap, say in sc['phr']:
            if len(cap) > 120: notes.append('scene %d: caption is long (%d characters); split the phrase: %s' % (i + 1, len(cap), cap[:50]))
    if not getattr(scenes[-1]['draw'], 'is_end', False): probs.append('last scene is not K.end_scene()')
    if not v.get('description'): notes.append("VIDEO['description'] is empty")
    if not v.get('sources'): notes.append("VIDEO['sources'] is empty (fine only when the screen states no facts)")
    video, tmp, mix_, tl, total, caps = ST.prepare(name)
    for f in ('land', 'port'):
        c = ST.Ctx(*ST.fmt_size(f)); cf = F('Heavy', int(c.S(60, 40))); cw = int(c.W * c.R(0.88, 0.80))
        for i, sc in enumerate(scenes):
            for cap, _ in sc['phr']:
                nl = len(wrap(cap, cf, cw))
                if nl > 3: probs.append('scene %d %s: caption wraps to %d lines (max 3); split the phrase: %s' % (i + 1, f, nl, cap[:50]))
        del WARN[:]
        for i, s in enumerate(tl):
            ST.render_frame(c, video, tl, total, max(s['t0'] + 0.4, s['t1'] - 0.3), caps)
            for w in WARN: probs.append('scene %d %s layout: %s' % (i + 1, f, w))
            del WARN[:]
    if not 45 <= total <= 75: probs.append('duration is %.1f s (target 45 to 75)' % total)
    _print_times(v, tl, total)
    words = sum(len(say.split()) for sc in scenes for _, say in sc['phr']); print('spoken words: %d' % words)
    for n_ in notes: print('REVIEW:', n_)
    for p_ in probs: print('PROBLEM:', p_)
    print('check: %d problem(s), %d line(s) to review' % (len(probs), len(notes)))
    return not probs


def _ensure_encoder():
    """Compile the studio's Swift encoder once, atomically, so parallel builds never see a half-written binary."""
    os.makedirs(ST.SCRATCH, exist_ok=True); exe = os.path.join(ST.SCRATCH, 'enc')
    if os.path.exists(exe) and os.path.getmtime(exe) >= os.path.getmtime(ST.__file__): return
    src = os.path.join(ST.SCRATCH, 'enc-%d.swift' % os.getpid()); tmp = os.path.join(ST.SCRATCH, 'enc-%d' % os.getpid())
    open(src, 'w').write(ST.SWIFT)
    r = subprocess.run(['swiftc', '-O', src, '-o', tmp], capture_output=True, text=True)
    if r.returncode: print(r.stderr[-1500:]); raise SystemExit('swiftc failed')
    os.replace(tmp, exe); os.remove(src)


def outputs(slug):
    h264 = os.environ.get('VIDEO_CODEC', 'h264') == 'h264'
    return dict(land=os.path.join(ROOT, 'site', 'assets', 'video', slug + '.mp4'), poster=os.path.join(ROOT, 'site', 'assets', 'video', slug + '.jpg'),
                port=os.path.join(ROOT, 'social', 'video_masters', slug + ('-vertical.mp4' if h264 else '-vertical-hevc.mp4')))


def cmd_build(slug, only=None):
    name, v = load(slug); _ensure_encoder()
    ST.build(name, only)          # the studio's own build: land -> site/assets/video, port -> social/video_masters
    o = outputs(name)
    for k in ([only] if only else ['land', 'port']):
        r = subprocess.run(['afinfo', o[k]], capture_output=True, text=True)
        info = [ln.strip() for ln in r.stdout.splitlines() if 'estimated duration' in ln or 'Data format' in ln]
        print(k, o[k], '|', ' | '.join(info) if info else 'NO AUDIO TRACK FOUND')
    _print_warn()


def cmd_notes(slug):
    """Write scripts/videos_life/<slug>.md: title, description, transcript, on-screen facts with sources, duration, files."""
    name, v = load(slug); video, tmp, mix_, tl, total, caps = ST.prepare(name); o = outputs(name)
    eng = 'Kokoro "af_heart" (local, AI-generated voice)' if ST.ENGINE == 'kokoro' else 'macOS say (local, synthetic voice)'
    L = ['Title: ' + v['title'], 'Slug: ' + name, 'Description: ' + v.get('description', ''), '',
         'Duration: %.1f seconds' % total, 'Narration voice: ' + eng, 'Music: ' + os.path.basename(os.environ.get('VIDEO_MUSIC_FILE', ST.DEFAULT_MUSIC)) + ' (see social/music/)', '',
         'Narration transcript (the burned-in captions carry the same words):']
    for i, (sc, s) in enumerate(zip(v['scenes'], tl)):
        L.append('  [%d] %.1f s  %s' % (i + 1, s['t0'], ' '.join(cap for cap, _ in sc['phr'])))
    L += ['', 'On-screen facts and sources:']
    for src in v.get('sources', []):
        if isinstance(src, dict): fact, url, date = src.get('fact', ''), src.get('url', ''), src.get('date', '')
        else: fact, url, date = (list(src) + ['', '', ''])[:3]
        L += ['  - ' + fact, '    Source: %s%s' % (url, ('  (page date: %s)' % date) if date else '')]
    if not v.get('sources'): L.append('  (none listed)')
    L += ['', 'On-screen text by scene:']
    for i, sc in enumerate(v['scenes']):
        L.append('  [%d] %s' % (i + 1, ' | '.join(getattr(sc['draw'], 'texts', []) or ['(custom scene)'])))
    L += ['', 'Footer on every frame: %s  ·  Call %s' % (SITE, CALL), 'End card disclaimer: ' + DISCLAIMER, '', 'Output files:',
          '  16:9 video: ' + os.path.relpath(o['land'], ROOT) + ('' if os.path.exists(o['land']) else '  (not built yet)'),
          '  16:9 poster: ' + os.path.relpath(o['poster'], ROOT) + ('' if os.path.exists(o['poster']) else '  (not built yet)'),
          '  9:16 master: ' + os.path.relpath(o['port'], ROOT) + ('' if os.path.exists(o['port']) else '  (not built yet)'), '']
    path = os.path.join(VDIR, name + '.md'); open(path, 'w', encoding='utf-8').write('\n'.join(L)); print('wrote', path)


def main(a):
    if not a or a[0] == 'list':
        for s in slugs():
            try: print('%-44s %s' % (s, load(s)[1]['title']))
            except Exception as ex: print('%-44s (does not load: %s)' % (s, ex))
    elif a[0] == 'times': cmd_times(a[1])
    elif a[0] == 'still': cmd_still(a[1], float(a[2]), a[3] if len(a) > 3 and a[3] in ('land', 'port') else 'land', a)
    elif a[0] == 'sheet': cmd_sheet(a[1], [a[2]] if len(a) > 2 and a[2] in ('land', 'port') else ['land', 'port'], a)
    elif a[0] == 'check': sys.exit(0 if cmd_check(a[1]) else 1)
    elif a[0] == 'build': cmd_build(a[1], a[a.index('--only') + 1] if '--only' in a else None)
    elif a[0] == 'notes': cmd_notes(a[1])
    else: print(__doc__)


if __name__ == '__main__':
    import video_life            # one shared copy of the kit: the video files import this same module
    video_life.main(sys.argv[1:])
