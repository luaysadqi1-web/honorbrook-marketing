"""Visual layer for the Honorbrook explainer videos: a modern motion-graphics look.

Animated gradient background, frosted-glass cards with soft shadows, SF Pro type with staggered headline reveals,
dial / column / ring graphics, gradient icon badges, and captions without a box. The audio, timeline and encoder live in
video_studio.py; this module only draws frames. Layouts are written for a 1080x1920 phone canvas and, for 16:9, in
1280x720 units that Ctx.S() scales up to 1920x1080.
"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(ROOT, 'site', 'assets', 'logo-static.png')

BG0, BG1 = (7, 13, 29), (16, 30, 58)
TEAL, INDIGO, GOLD, GOLDL = (52, 211, 182), (99, 102, 241), (245, 193, 75), (255, 224, 142)
CORAL, CORALL, SKY, SKYD = (255, 122, 102), (255, 170, 150), (136, 186, 255), (86, 128, 214)
WHITE, MUTED, INK = (255, 255, 255), (163, 178, 204), (10, 18, 36)
SFNS = '/System/Library/Fonts/SFNS.ttf'
_F = {}


def F(w, size):
    k = (w, int(size))
    if k not in _F:
        f = ImageFont.truetype(SFNS, int(size)); f.set_variation_by_name(w); _F[k] = f
    return _F[k]


# ------------------------------------------------------------------ easing
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, t0, d): return clamp((t - t0) / d) if d > 0 else (1.0 if t >= t0 else 0.0)
def eo3(x): return 1 - (1 - x) ** 3
def eio(x): return 3 * x * x - 2 * x ** 3
def eob(x):
    s = 1.70158; x -= 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2
def lerp(a, b, x): return a + (b - a) * x
def mix(c1, c2, x): return tuple(int(lerp(a, b, x)) for a, b in zip(c1, c2))


# ------------------------------------------------------------------ drawing primitives (alpha masks pasted onto the frame)
def _paste(img, color, x, y, mask, a):
    if a < 1: mask = mask.point(lambda v: int(v * a))
    img.paste(color, (int(round(x)), int(round(y))), mask)


def text(img, x, y, s, f, fill, a=1.0, anchor='la'):
    if a <= 0.004 or not s: return
    l, t, r, b = f.getbbox(s, anchor=anchor); pad = 3
    m = Image.new('L', (r - l + 2 * pad, b - t + 2 * pad), 0)
    ImageDraw.Draw(m).text((-l + pad, -t + pad), s, font=f, fill=255, anchor=anchor)
    _paste(img, fill, x + l - pad, y + t - pad, m, a)


def text_shadow(img, x, y, s, f, a=1.0, anchor='la', blur=7, dy=4, sa=0.6):
    if a <= 0.004 or not s: return
    l, t, r, b = f.getbbox(s, anchor=anchor); pad = blur * 3
    m = Image.new('L', (r - l + 2 * pad, b - t + 2 * pad), 0)
    ImageDraw.Draw(m).text((-l + pad, -t + pad), s, font=f, fill=255, anchor=anchor)
    _paste(img, (0, 0, 0), x + l - pad, y + t - pad + dy, m.filter(ImageFilter.GaussianBlur(blur)), a * sa)


def text_grad(img, x, y, s, f, c1, c2, a=1.0, anchor='la'):
    if a <= 0.004 or not s: return
    l, t, r, b = f.getbbox(s, anchor=anchor); pad = 4; w, h = r - l + 2 * pad, b - t + 2 * pad
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).text((-l + pad, -t + pad), s, font=f, fill=255, anchor=anchor)
    g = np.linspace(0, 1, h)[:, None, None]
    arr = np.repeat(np.array(c1, float)[None, None, :] * (1 - g) + np.array(c2, float)[None, None, :] * g, w, axis=1).astype('uint8')
    if a < 1: m = m.point(lambda v: int(v * a))
    img.paste(Image.fromarray(arr), (int(round(x + l - pad)), int(round(y + t - pad))), m)


def shape(img, box, color, a, drawer, ss=1):
    x0, y0, x1, y1 = [int(round(v)) for v in box]; w, h = x1 - x0, y1 - y0
    if w <= 0 or h <= 0 or a <= 0.004: return
    m = Image.new('L', (w * ss, h * ss), 0); drawer(ImageDraw.Draw(m), ss, w, h)
    if ss > 1: m = m.resize((w, h), Image.LANCZOS)
    _paste(img, color, x0, y0, m, a)


def rrect(img, x0, y0, x1, y1, r, color, a=1.0, outline=0):
    def d(dr, ss, w, h):
        if outline: dr.rounded_rectangle([0, 0, w * ss - 1, h * ss - 1], radius=r * ss, outline=255, width=outline * ss)
        else: dr.rounded_rectangle([0, 0, w * ss - 1, h * ss - 1], radius=r * ss, fill=255)
    shape(img, (x0, y0, x1, y1), color, a, d, ss=2 if r > 5 else 1)


def grect(img, x0, y0, x1, y1, r, c1, c2, a=1.0, shine=True):
    """Gradient (top to bottom) rounded bar with a soft top highlight."""
    w, h = int(x1 - x0), int(y1 - y0)
    if w <= 1 or h <= 1 or a <= 0.004: return
    m = Image.new('L', (w * 2, h * 2), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w * 2 - 1, h * 2 - 1], radius=min(r, w // 2, h // 2) * 2, fill=255)
    m = m.resize((w, h), Image.LANCZOS)
    g = np.linspace(0, 1, h)[:, None, None]
    arr = np.array(c1, float)[None, None, :] * (1 - g) + np.array(c2, float)[None, None, :] * g
    if shine: arr = arr + np.clip(1 - np.linspace(0, 1, h) * 5, 0, 1)[:, None, None] * 38
    img.paste(Image.fromarray(np.repeat(np.clip(arr, 0, 255), w, axis=1).astype('uint8')), (int(x0), int(y0)), m.point(lambda v: int(v * a)) if a < 1 else m)


def circle(img, cx, cy, r, color, a=1.0, outline=0):
    def d(dr, ss, w, h):
        if outline: dr.ellipse([0, 0, w * ss - 1, h * ss - 1], outline=255, width=outline * ss)
        else: dr.ellipse([0, 0, w * ss - 1, h * ss - 1], fill=255)
    shape(img, (cx - r, cy - r, cx + r, cy + r), color, a, d, ss=3)


def ring_line(img, cx, cy, r, w, color, a):
    """Thin ring for big radii (1x mask, light blur): cheap enough to animate."""
    r = int(r); pad = 4; m = Image.new('L', (2 * r + 2 * pad, 2 * r + 2 * pad), 0)
    ImageDraw.Draw(m).ellipse([pad, pad, 2 * r + pad, 2 * r + pad], outline=255, width=max(1, int(w)))
    _paste(img, color, cx - r - pad, cy - r - pad, m.filter(ImageFilter.GaussianBlur(0.8)), a)


_GL = {}


def glow(img, cx, cy, r, color, a=1.0, power=2.0):
    r = int(r)
    if a <= 0.01 or r < 6: return
    k = (r, power)
    if k not in _GL:
        yy, xx = np.mgrid[-r:r, -r:r]; d = np.sqrt(xx ** 2 + yy ** 2) / r
        _GL[k] = Image.fromarray((np.clip(1 - d, 0, 1) ** power * 255).astype('uint8'))
    _paste(img, color, cx - r, cy - r, _GL[k], a)


_SH = {}


def glass(img, x0, y0, x1, y1, r, a=1.0, fill_a=0.10, border_a=0.22, shadow=True, tint=WHITE):
    if a <= 0.01: return
    w, h = int(x1 - x0), int(y1 - y0); blur = 26
    if shadow:
        k = (w, h, int(r), round(a, 1))
        if k not in _SH:
            m = Image.new('L', (w + 4 * blur, h + 4 * blur), 0)
            ImageDraw.Draw(m).rounded_rectangle([2 * blur, 2 * blur, 2 * blur + w, 2 * blur + h], radius=int(r), fill=255)
            _SH[k] = m.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * 0.5 * round(a, 1)))
        img.paste((0, 0, 0), (int(x0 - 2 * blur), int(y0 - 2 * blur + 18)), _SH[k])
    rrect(img, x0, y0, x1, y1, r, tint, fill_a * a)
    rrect(img, x0, y0, x1, y1, r, WHITE, border_a * a, outline=2)


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
        text(img, cx, y, ln, f, fill, a, 'ma' if align == 'center' else 'la'); y += int(f.size * lh)
    return y


def overline(img, cx, y, s, f, color, a=1.0, track=0.2):
    s = s.upper(); adv = [f.getlength(ch) + f.size * track for ch in s]; x = cx - (sum(adv) - f.size * track) / 2
    for ch, w in zip(s, adv):
        text(img, x, y, ch, f, color, a, 'la'); x += w


def headline(img, cx, y, s, size, t, t0, maxw, color=WHITE, weight='Heavy'):
    """Words slide up and fade in one after another. Returns the bottom of the text block."""
    f = F(weight, size); lines = wrap(s, f, maxw); yy = y; n = 0
    for ln in lines:
        x = cx - f.getlength(ln) / 2
        for w in ln.split():
            p = eo3(prog(t, t0 + 0.07 * n, 0.5)); n += 1
            text(img, x, yy + (1 - p) * size * 0.45, w, f, color, p, 'la'); x += f.getlength(w + ' ')
        yy += int(size * 1.08)
    return yy


# ------------------------------------------------------------------ glyphs and badges
def _stroke(d, pts, w, closed=False):
    pts = list(pts) + ([pts[0]] if closed else [])
    d.line(pts, fill=255, width=int(w), joint='curve')
    for p in (pts if closed else (pts[0], pts[-1])): d.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=255)


def glyph(img, kind, cx, cy, s, color=WHITE, a=1.0):
    ss = 4; S = int(s)

    def draw(d, ss_, w, h):
        u = w * ss_ / 100.0; sw = 8 * u
        P = lambda *pts: [(x * u, y * u) for x, y in pts]
        if kind == 'calendar':
            d.rounded_rectangle([14 * u, 22 * u, 86 * u, 88 * u], radius=11 * u, outline=255, width=int(sw))
            _stroke(d, P((14, 42), (86, 42)), sw); _stroke(d, P((33, 11), (33, 29)), sw); _stroke(d, P((67, 11), (67, 29)), sw)
            _stroke(d, P((36, 66), (46, 76), (66, 55)), sw)
        elif kind == 'doc':
            _stroke(d, P((24, 10), (60, 10), (78, 28), (78, 90), (24, 90)), sw, True)
            for yy, x2 in ((52, 66), (66, 66), (78, 52)): _stroke(d, P((38, yy), (x2, yy)), sw * 0.8)
        elif kind == 'shield':
            _stroke(d, P((50, 8), (86, 22), (82, 58), (50, 92), (18, 58), (14, 22)), sw, True)
            _stroke(d, P((35, 50), (46, 61), (66, 38)), sw)
        elif kind == 'heart':
            tt = np.linspace(0, 2 * math.pi, 80)
            pts = [(50 + 2.55 * 16 * math.sin(t) ** 3, 44 - 2.55 * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) * 0.95 + 4) for t in tt]
            _stroke(d, [(x * u, y * u) for x, y in pts], sw, True)
        elif kind == 'cross':
            _stroke(d, P((50, 18), (50, 82)), sw * 1.25); _stroke(d, P((18, 50), (82, 50)), sw * 1.25)
        elif kind == 'pill':
            tmp = Image.new('L', (w * ss_, h * ss_), 0); td = ImageDraw.Draw(tmp)
            td.rounded_rectangle([8 * u, 32 * u, 92 * u, 68 * u], radius=18 * u, outline=255, width=int(sw)); _stroke(td, P((50, 32), (50, 68)), sw)
            tmp = tmp.rotate(40, resample=Image.BICUBIC); d._image.paste(255, (0, 0), tmp)
        elif kind == 'pin':
            d.ellipse([26 * u, 10 * u, 74 * u, 58 * u], outline=255, width=int(sw))
            _stroke(d, P((31, 50), (50, 90), (69, 50)), sw); d.ellipse([42 * u, 26 * u, 58 * u, 42 * u], fill=255)
        elif kind == 'flag':
            _stroke(d, P((28, 10), (28, 90)), sw); _stroke(d, P((28, 14), (80, 28), (28, 48)), sw, True)
        elif kind == 'clock':
            d.ellipse([12 * u, 12 * u, 88 * u, 88 * u], outline=255, width=int(sw)); _stroke(d, P((50, 28), (50, 50), (66, 60)), sw)
    shape(img, (cx - S / 2, cy - S / 2, cx + S / 2, cy + S / 2), color, a, draw, ss=ss)


def badge(img, cx, cy, r, kind, c1, c2, a=1.0):
    if a <= 0.01: return
    glow(img, cx, cy + r * 0.25, r * 2.0, c1, 0.22 * a, 2.5)
    size = int(2 * r); m = Image.new('L', (size * 3, size * 3), 0); ImageDraw.Draw(m).ellipse([0, 0, size * 3 - 1, size * 3 - 1], fill=255)
    m = m.resize((size, size), Image.LANCZOS)
    g = np.linspace(0, 1, size)[:, None, None] * 0.9 + np.linspace(0, 1, size)[None, :, None] * 0.1
    arr = np.array(c1, float)[None, None, :] * (1 - g) + np.array(c2, float)[None, None, :] * g
    img.paste(Image.fromarray(arr.astype('uint8')), (int(cx - r), int(cy - r)), m.point(lambda v: int(v * a)) if a < 1 else m)
    glyph(img, kind, cx, cy, size * 0.56, WHITE, a)


def check_badge(img, cx, cy, r, p):
    if p <= 0: return
    rr = r * (eob(clamp(p / 0.55)) if p < 0.55 else 1.0)
    glow(img, cx, cy, rr * 1.9, TEAL, 0.35, 2.5)
    circle(img, cx, cy, rr, TEAL, 1.0)
    q = clamp((p - 0.3) / 0.6)
    if q > 0:
        a_, b_, c_ = (cx - r * 0.42, cy + r * 0.02), (cx - r * 0.1, cy + r * 0.36), (cx + r * 0.46, cy - r * 0.3)
        seg = [a_, (lerp(a_[0], b_[0], q * 2), lerp(a_[1], b_[1], q * 2))] if q < 0.5 else [a_, b_, (lerp(b_[0], c_[0], (q - 0.5) * 2), lerp(b_[1], c_[1], (q - 0.5) * 2))]
        shape(img, (cx - r, cy - r, cx + r, cy + r), WHITE, 1.0,
              lambda d, ss, w, h: (d.line([((x - (cx - r)) * ss, (y - (cy - r)) * ss) for x, y in seg], fill=255, width=int(r * 0.2 * ss), joint='curve')), ss=3)


# ------------------------------------------------------------------ canvas
class Ctx:
    def __init__(self, W, H):
        self.W, self.H, self.land, self.cx = W, H, W > H, W // 2
        self.k = self.H / 720.0 if self.land else 1.0
        lw, lh = W // 6, H // 6; self.lw, self.lh = lw, lh
        yy, xx = np.mgrid[0:lh, 0:lw]; self.X, self.Y = xx / lw, yy / lh
        base = np.array(BG0, float)[None, None, :] * (1 - self.Y[..., None] * 0.9) + np.array(BG1, float)[None, None, :] * (self.Y[..., None] * 0.9)
        vig = np.clip(1 - 0.55 * (((self.X - 0.5) * 1.5) ** 2 + ((self.Y - 0.5) * 1.1) ** 2), 0.55, 1)
        self.base = base * vig[..., None]
        self.blobs = [(0.2, 0.18, 0.55, TEAL, 0.20, 0.23, 0.17, 0.0), (0.85, 0.42, 0.6, INDIGO, 0.24, 0.19, 0.27, 2.1),
                      (0.35, 0.92, 0.65, GOLD, 0.13, 0.15, 0.21, 4.0), (0.8, 0.05, 0.45, (60, 120, 255), 0.14, 0.31, 0.22, 1.0)]
        rng = np.random.default_rng(3); self.dither = Image.fromarray(rng.integers(0, 3, (H, W, 3)).astype('uint8'))
        self.logo = None
        try:
            lg = Image.open(LOGO).convert('RGBA'); px = np.asarray(lg).copy()
            px[..., 3] = np.clip((255 - px[..., :3].min(axis=2).astype(int)) * 3, 0, 255).astype('uint8'); lg = Image.fromarray(px)
            hh = int(self.S(84, 36)); self.logo = lg.resize((int(lg.width * hh / lg.height), hh), Image.LANCZOS)
        except Exception: pass
        sh = int(H * 0.30); grad = (np.linspace(0, 1, sh) ** 1.6 * 150).astype('uint8')
        self.scrim = Image.fromarray(np.repeat(grad[:, None], W, axis=1)); self.scrim_y = H - sh
        self.top, self.bot = self.S(560, 215), self.S(1370, 520)
        self.cap_y = self.S(1612, 614)
        self.strip_y = self.S(1848, 700)

    def S(self, p, l): return p if not self.land else l * self.k
    def R(self, p, l): return l if self.land else p      # unscaled ratio for width fractions
    def FS(self, p, l): return p if not self.land else max(l * self.k * 1.32, 23)   # font sizes: bigger on 16:9 (blog embeds it ~720 px wide)

    def frame(self, t):
        arr = self.base.copy()
        for cx, cy, rad, col, amp, fx, fy, ph in self.blobs:
            x = cx + 0.07 * math.sin(t * fx + ph); y = cy + 0.06 * math.cos(t * fy + ph * 1.3)
            d = np.sqrt(((self.X - x) / rad) ** 2 + ((self.Y - y) / rad) ** 2)
            arr += (np.clip(1 - d, 0, 1) ** 2)[..., None] * np.array(col, float)[None, None, :] * amp
        im = Image.fromarray(np.clip(arr, 0, 255).astype('uint8')).resize((self.W, self.H), Image.BICUBIC)
        return ImageChops.add(im, self.dither, 1.0, -1)


def zoom(img, s):
    if s <= 1.0005: return img
    W, H = img.size; w, h = W / s, H / s; x, y = (W - w) / 2, (H - h) / 2
    return img.resize((W, H), Image.BILINEAR, box=(x, y, x + w, y + h))


VOICE_NOTE = ''   # set by video_studio.prepare() when the narration is an AI voice


def overlay(c, img, t, total, cap):
    W = c.W
    shape(img, (0, 0, int(W * clamp(t / total)), int(c.S(7, 3))), GOLD, 1.0, lambda d, ss, w, h: d.rectangle([0, 0, w, h], fill=255))
    bx, by = c.S(54, 28), c.S(72, 24)
    if c.logo: img.paste(c.logo, (int(bx), int(by)), c.logo)
    text(img, bx + (c.logo.width if c.logo else 0) + c.S(20, 10), by + c.S(42, 18), 'Honorbrook Insurance', F('Bold', c.FS(42, 21)), WHITE, 1.0, 'lm')
    text(img, W / 2, c.strip_y, 'Honorbrook Insurance  ·  (571) 354-0146', F('Semibold', c.FS(32, 15)), MUTED, 1.0, 'mm')
    if cap:
        img.paste((6, 11, 24), (0, c.scrim_y), c.scrim)
        caption(c, img, t, cap)


def caption(c, img, t, cap):
    s, e, words = cap
    a = clamp((t - (s - 0.08)) / 0.16) * clamp(((e + 0.5) - t) / 0.25)
    if a <= 0: return
    f = F('Heavy', int(c.FS(60, 28))); maxw = int(c.W * c.R(0.88, 0.74))
    lines = wrap(' '.join(words), f, maxw); lh = int(f.size * 1.22)
    wts = [len(w) + 2 for w in words]; tot = sum(wts); p = clamp((t - s) / max(e - s, 0.2)) * 1.03
    y = c.cap_y - len(lines) * lh / 2; done = 0; idx = 0
    for ln in lines:
        lw = f.getlength(ln); x = c.cx - lw / 2
        text_shadow(img, c.cx, y, ln, f, a, 'ma', blur=int(c.S(9, 5)), dy=int(c.S(5, 3)), sa=0.7)
        for w in ln.split():
            ww = f.getlength(w); mid = done + wts[idx] / 2
            if done <= p * tot < done + wts[idx]:
                pop = 1 + 0.035 * math.sin(clamp((p * tot - done) / max(wts[idx], 1) * 3) * math.pi / 2 * 2)
                text(img, x + ww / 2, y + f.size * 0.55, w, F('Heavy', int(f.size * pop)), GOLDL, a, 'mm')
            else:
                text(img, x, y, w, f, WHITE if mid <= p * tot else (215, 224, 240), a * (1.0 if mid <= p * tot else 0.82), 'la')
            x += f.getlength(w + ' '); done += wts[idx]; idx += 1
        y += lh


def title_block(c, img, t, over, head=None, t0=0.0):
    overline(img, c.cx, c.S(300, 100), over, F('Bold', int(c.FS(32, 15))), GOLD, eo3(prog(t, t0, 0.4)), 0.22)
    if head: headline(img, c.cx, c.S(352, 124), head, c.S(92, 46), t, t0 + 0.08, int(c.W * c.R(0.9, 0.8)))


def row_card(c, img, t, x0, y0, w, h, p, kind, c1, c2, label, chk=0.0):
    gh = eo3(prog(t, 0.35, 0.6)) * (1 - eo3(p))
    if gh > 0.01: glass(img, x0, y0, x0 + w, y0 + h, c.S(40, 20), gh * 0.55, fill_a=0.05, border_a=0.14, shadow=False)
    p = eo3(p); sl = (1 - p) * c.S(70, 30)
    glass(img, x0 + sl, y0, x0 + w + sl, y0 + h, c.S(40, 20), p)
    badge(img, x0 + sl + h * 0.5, y0 + h / 2, h * 0.30, kind, c1, c2, p)
    f = F('Bold', int(c.FS(44, 21))); lines = wrap(label, f, w - h - c.S(150, 90))
    for j, ln in enumerate(lines): text(img, x0 + sl + h * 0.5 + h * 0.30 + c.S(40, 22), y0 + h / 2 + (j - (len(lines) - 1) / 2) * f.size * 1.2, ln, f, WHITE, p, 'lm')
    check_badge(img, x0 + sl + w - c.S(74, 36), y0 + h / 2, c.S(34, 16), chk)


def end_card(c, img, t, ph, lines):
    q, phone, web, disc = lines
    a = eo3(prog(t, 0.0, 0.5))
    if c.logo:
        lg = c.logo.resize((int(c.logo.width * 1.7), int(c.logo.height * 1.7)), Image.LANCZOS)
        lg.putalpha(lg.getchannel('A').point(lambda v: int(v * a)))
        img.paste(lg, (int(c.cx - lg.width / 2), int(c.S(300, 100))), lg)
    headline(img, c.cx, c.S(470, 190), q, c.S(84, 44), t, 0.1, int(c.W * c.R(0.88, 0.7)))
    b = eo3(prog(t, ph[0][0] + 0.2, 0.5)); y2 = c.S(790, 305); w2, h2 = c.S(840, 470), c.S(150, 74)
    glow(img, c.cx, y2 + h2 / 2, w2 * 0.7, GOLD, 0.25 * b * (0.85 + 0.15 * math.sin(t * 3)), 2.2)
    grect(img, c.cx - w2 / 2, y2, c.cx + w2 / 2, y2 + h2, c.S(75, 37), GOLDL, GOLD, b)
    text(img, c.cx, y2 + h2 / 2 + 2, phone, F('Black', c.FS(84, 40)), INK, b, 'mm')
    d = eo3(prog(t, ph[0][0] + 0.8, 0.5))
    text(img, c.cx, y2 + c.S(235, 112), 'or fill out the form at', F('Medium', c.FS(40, 19)), MUTED, d, 'mm')
    text(img, c.cx, y2 + c.S(305, 148), web, F('Bold', c.FS(58, 29)), WHITE, d, 'mm')
    e = eo3(prog(t, ph[-1][0], 0.5))
    yend = para(img, c.cx, c.S(1180, 478), disc, F('Regular', c.FS(29, 13)), MUTED, int(c.W * c.R(0.84, 0.7)), e * 0.95, 1.35)
    if VOICE_NOTE: para(img, c.cx, yend + c.S(22, 8), VOICE_NOTE, F('Medium', c.FS(28, 13)), GOLDL, int(c.W * c.R(0.84, 0.7)), e * 0.95, 1.3)


# ------------------------------------------------------------------ VIDEO 1: Part D late enrollment penalty
def d_hook(c, img, t, ph):
    title_block(c, img, t, 'Medicare Part D')
    cs, ce = ph[0][0] + 0.35, ph[0][0] + (ph[0][1] - ph[0][0]) * 0.82
    ncy = c.S(850, 282)
    pulse = 0.85 + 0.15 * math.sin(t * 2.2)
    glow(img, c.cx, ncy, c.S(560, 300), GOLD, 0.32 * pulse * eo3(prog(t, 0.1, 0.6)), 2.2)
    for k in range(3):
        ph_ = ((t * 0.38) + k / 3) % 1.0
        ring_line(img, c.cx, ncy, lerp(c.S(250, 130), c.S(560, 300), ph_), c.S(3, 2), GOLDL, (1 - ph_) * 0.30 * eo3(prog(t, 0.3, 0.6)))
    v = 9.40 * eo3(prog(t, cs, ce - cs))
    pop = 1 + (0.07 * math.sin(clamp((t - ce) / 0.5) * math.pi) if t > ce else 0)
    text_grad(img, c.cx, ncy, '$%.2f' % v, F('Black', int(c.S(285, 160) * pop)), GOLDL, GOLD, eo3(prog(t, 0.15, 0.3)), 'mm')
    text(img, c.cx, ncy + c.S(185, 90), 'more per month', F('Medium', c.FS(62, 30)), WHITE, eo3(prog(t, ce - 0.2, 0.5)), 'mm')
    p1 = eo3(prog(t, ph[1][0] + 0.05, 0.5)); cy = c.S(1215, 452); w, h = c.S(840, 540), c.S(120, 58)
    glass(img, c.cx - w / 2, cy - h / 2 + (1 - p1) * 30, c.cx + w / 2, cy + h / 2 + (1 - p1) * 30, h / 2, p1)
    circle(img, c.cx - w / 2 + c.S(52, 26), cy + (1 - p1) * 30, c.S(11, 6), TEAL, p1)
    text(img, c.cx + c.S(18, 8), cy + (1 - p1) * 30, 'for as long as you have drug coverage', F('Bold', c.FS(40, 20)), WHITE, p1, 'mm')
    text(img, c.cx, c.S(1330, 512), 'Example: 24 months without coverage  ·  2026 base premium $38.99', F('Regular', c.FS(28, 13)), MUTED, eo3(prog(t, ce + 0.3, 0.5)), 'mm')


def d_63(c, img, t, ph):
    title_block(c, img, t, 'The trigger', '63 days in a row')
    full = t >= ph[2][0]; flash = eio(prog(t, ph[2][0], 0.5))
    s_, e_ = ph[1][0] + 0.15, ph[1][1] - 0.1
    n = int(round(63 * clamp((t - s_) / (e_ - s_))))
    cx, cy = (c.cx, c.S(955, 0)) if not c.land else (c.S(0, 330), c.S(0, 375))
    R = c.S(318, 128); tl, tw = c.S(58, 25), c.S(11, 5)
    # dial of 63 ticks
    box = int(R * 2 + tl * 2 + 40); on = Image.new('L', (box * 2, box * 2), 0); off = Image.new('L', (box * 2, box * 2), 0)
    don, doff = ImageDraw.Draw(on), ImageDraw.Draw(off); m = box
    for i in range(63):
        ang = -math.pi / 2 + i * 2 * math.pi / 63; ca, sa = math.cos(ang), math.sin(ang)
        p0 = (m + (R - tl) * 2 * ca, m + (R - tl) * 2 * sa); p1 = (m + R * 2 * ca, m + R * 2 * sa)
        dr = don if i < n else doff
        dr.line([p0, p1], fill=255, width=int(tw * 2)); [dr.ellipse([p[0] - tw, p[1] - tw, p[0] + tw, p[1] + tw], fill=255) for p in (p0, p1)]
    on = on.resize((box, box), Image.LANCZOS); off = off.resize((box, box), Image.LANCZOS)
    pulse = 0.5 + 0.5 * math.sin(t * 5) if full else 0
    col = mix(GOLDL, CORAL, flash)
    glow(img, cx, cy, R * 1.5, mix(GOLD, CORAL, flash), (0.16 + 0.1 * pulse) * eo3(prog(t, 0.1, 0.5)), 2.2)
    _paste(img, (74, 96, 140), cx - box / 2, cy - box / 2, off, 0.9)
    _paste(img, mix(col, CORALL, pulse * 0.35), cx - box / 2, cy - box / 2, on, 1.0)
    text_grad(img, cx, cy - c.S(34, 0), str(n), F('Black', c.FS(210, 96)), mix(GOLDL, CORALL, flash), col, 1.0, 'mm')
    if not c.land:
        text(img, cx, cy + 84, 'days without', F('Medium', 34), MUTED, 1.0, 'mm'); text(img, cx, cy + 126, 'drug coverage', F('Medium', 34), MUTED, 1.0, 'mm')
    else: text(img, cx, cy + R + tl + 22 * c.k, 'days without drug coverage', F('Medium', c.FS(0, 17)), MUTED, 1.0, 'mm')
    a0 = eo3(prog(t, ph[0][0] + 0.1, 0.5))
    lx, ly = (c.cx, c.S(570, 0)) if not c.land else (c.S(0, 905), c.S(0, 300))
    w, h = c.S(780, 420), c.S(96, 48)
    glass(img, lx - w / 2, ly - h / 2 + (1 - a0) * 24, lx + w / 2, ly + h / 2 + (1 - a0) * 24, h / 2, a0)
    glyph(img, 'flag', lx - w / 2 + c.S(62, 30), ly + (1 - a0) * 24, c.S(54, 26), GOLDL, a0)
    text(img, lx + c.S(30, 14), ly + (1 - a0) * 24, 'Initial Enrollment Period ends', F('Bold', c.FS(36, 17)), WHITE, a0, 'mm')
    b = eob(prog(t, ph[2][0] + 0.25, 0.5))
    if b > 0:
        bx, by = (c.cx, cy + R + c.S(118, 0)) if not c.land else (c.S(0, 905), c.S(0, 430)); w2, h2 = c.S(700, 400), c.S(96, 52)
        glow(img, bx, by, w2 * 0.6, CORAL, 0.28 * clamp(b), 2.2)
        grect(img, bx - w2 / 2, by - h2 / 2, bx + w2 / 2, by + h2 / 2, h2 / 2, CORALL, CORAL, clamp(b))
        text(img, bx, by, 'The penalty can start', F('Heavy', c.FS(44, 21)), WHITE, clamp(b), 'mm')


def d_math(c, img, t, ph):
    title_block(c, img, t, 'The math', "How it's calculated")
    f1 = eo3(prog(t, ph[0][0] + 0.1, 0.5)); f2 = eo3(prog(t, ph[1][0] + 0.1, 0.5))
    fx, fy = (c.cx, c.S(640, 0)) if not c.land else (c.S(0, 335), c.S(0, 330))
    text_grad(img, fx, fy + (1 - f1) * 20, '1%  ×  $38.99', F('Black', c.FS(118, 60)), GOLDL, GOLD, f1, 'mm')
    text(img, fx, fy + c.S(120, 62) + (1 - f2) * 20, '×  each full month without coverage', F('Semibold', c.FS(44, 20)), WHITE, f2, 'mm')
    rows = [('6 mo', 2.30, 2), ('1 yr', 4.70, 3), ('2 yr', 9.40, 4), ('3 yr', 14.00, 5)]
    if not c.land: base, bw, gap, maxh, x0 = 1330, 176, 50, 440, c.cx - (4 * 176 + 3 * 50) / 2
    else: bw, gap = c.S(0, 92), c.S(0, 34); base, maxh = c.S(0, 510), c.S(0, 205); x0 = c.S(0, 905) - (4 * bw + 3 * gap) / 2
    shape(img, (x0 - 10, base, x0 + 4 * bw + 3 * gap + 10, base + 3), WHITE, 0.25, lambda d, ss, w, h: d.rectangle([0, 0, w, h], fill=255))
    for i, (lab, val, k) in enumerate(rows):
        x = x0 + i * (bw + gap); p = eob(prog(t, ph[k][0] + 0.05, 0.8)); hot = val == 9.40
        hh = maxh * val / 14.0 * clamp(p, 0, 1.06)
        if hh > bw * 0.4:
            if hot: glow(img, x + bw / 2, base - hh / 2, bw * 1.6, GOLD, 0.25 * clamp(p), 2.2)
            grect(img, x, base - hh, x + bw, base, c.S(26, 12), GOLDL if hot else SKY, GOLD if hot else SKYD, 1.0)
        text_grad(img, x + bw / 2, base - hh - c.S(40, 20), '$%.2f' % (val * clamp(p)), F('Heavy', c.FS(48, 24)), GOLDL if hot else WHITE, GOLD if hot else (200, 215, 240), clamp(p * 3), 'mm')
        text(img, x + bw / 2, base + c.S(44, 22), lab, F('Semibold', c.FS(38, 17)), MUTED, eo3(prog(t, 0.6 + 0.1 * i, 0.4)), 'mm')
    fnx, fny = (c.cx, c.S(1425, 0)) if not c.land else (c.S(0, 905), c.S(0, 556))
    text(img, fnx, fny, 'per month  ·  rounded to the nearest $0.10  ·  Medicare.gov', F('Regular', c.FS(27, 12)), MUTED, eo3(prog(t, ph[2][0], 0.6)), 'mm')


def d_follow(c, img, t, ph):
    title_block(c, img, t, 'It sticks', 'It follows you')
    if not c.land: cw, chh = 880, 260; xs = [c.cx - cw / 2] * 2; ys = [620, 980]
    else: cw, chh = c.S(0, 470), c.S(0, 170); xs = [c.S(0, 150), c.S(0, 660)]; ys = [c.S(0, 250)] * 2
    a = eo3(prog(t, 0.1, 0.5)); b = eo3(prog(t, ph[1][0] + 0.1, 0.5))
    inner = cw - c.S(90, 60); off = c.S(150, 82); bh = c.S(70, 34); pw = c.S(200, 108)
    fl = [3 * math.sin(t * 1.3), 3 * math.sin(t * 1.3 + 2)]
    for i, (lab, plen, sa) in enumerate((('Your plan premium', 0.46, a), ('A different plan', 0.62, b))):
        y = ys[i] + fl[i] * c.k
        glass(img, xs[i], y, xs[i] + cw, y + chh, c.S(44, 22), sa)
        text(img, xs[i] + c.S(46, 24), y + c.S(58, 28), lab, F('Bold', c.FS(42, 21)), WHITE, sa, 'lm')
        grect(img, xs[i] + c.S(46, 24), y + off, xs[i] + c.S(46, 24) + inner * plen, y + off + bh, bh / 2, SKY, SKYD, sa)
    appear = eo3(prog(t, ph[0][0] + 0.3, 0.5)); mv = eio(prog(t, ph[1][0] + 0.55, 1.1))
    x1, y1 = xs[0] + c.S(46, 24) + inner * 0.46, ys[0] + fl[0] * c.k + off; x2, y2 = xs[1] + c.S(46, 24) + inner * 0.62, ys[1] + fl[1] * c.k + off
    for g_ in range(5, -1, -1):
        mm = clamp(mv - g_ * 0.035); x = lerp(x1, x2, mm); y = lerp(y1, y2, mm) - math.sin(mm * math.pi) * c.S(80, 40)
        if g_ and 0 < mv < 1: grect(img, x, y, x + pw, y + bh, bh / 2, CORAL, CORAL, appear * (0.5 - g_ * 0.07), shine=False)
    x = lerp(x1, x2, mv); y = lerp(y1, y2, mv) - math.sin(mv * math.pi) * c.S(80, 40)
    glow(img, x + pw / 2, y + bh / 2, pw, CORAL, 0.35 * appear, 2.2)
    grect(img, x, y, x + pw, y + bh, bh / 2, CORALL, CORAL, appear)
    text(img, x + pw / 2, y + bh / 2, '+ penalty', F('Heavy', c.FS(32, 16)), WHITE, appear, 'mm')
    text(img, c.cx, c.S(1340, 525), 'It stays for as long as you have Medicare drug coverage', F('Medium', c.FS(34, 16)), MUTED, eo3(prog(t, ph[1][0] + 1.8, 0.6)), 'mm')


def d_avoid(c, img, t, ph):
    title_block(c, img, t, 'The penalty', 'How to avoid it')
    items = [('calendar', TEAL, (34, 150, 190), 'Enroll when you are first eligible'), ('doc', GOLD, (230, 140, 40), 'Keep your creditable coverage notices'),
             ('shield', SKY, INDIGO, 'Never let a gap reach 63 days'), ('heart', CORAL, (220, 70, 110), 'Ask about Extra Help: no penalty if you get it')]
    cw, chh, gap = c.S(940, 880), c.S(184, 70), c.S(28, 10); y0 = c.S(606, 206)
    for i, (kind, c1, c2, lab) in enumerate(items):
        row_card(c, img, t, c.cx - cw / 2, y0 + i * (chh + gap) + 4 * math.sin(t * 1.4 + i) * c.k, cw, chh, prog(t, ph[i][0] - 0.05, 0.45), kind, c1, c2, lab, prog(t, ph[i][1] - 0.4, 0.5))


# ------------------------------------------------------------------ video definitions (phrases, timing, sound cues)
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
    title_block(c, img, t, 'ACA open enrollment', "The premium isn't the whole cost")
    if not c.land: cw, chh = 900, 290; ys = [660, 1000]
    else: cw, chh = c.S(0, 800), c.S(0, 124); ys = [c.S(0, 226), c.S(0, 368)]
    segs = [('Plan X', 'Lower premium', 0.30, 0.62, 'Higher total', CORAL), ('Plan Y', 'Higher premium', 0.50, 0.28, 'Lower total', TEAL)]
    bw = cw - c.S(90, 60); bh = c.S(72, 34)
    for i, (nm, lab, pr, car, verdict, vcol) in enumerate(segs):
        a = eo3(prog(t, 0.15 + i * 0.2, 0.5)); y = ys[i] + 3 * math.sin(t * 1.3 + i * 2) * c.k; x0 = c.cx - cw / 2
        glass(img, x0, y, x0 + cw, y + chh, c.S(44, 22), a)
        text(img, x0 + c.S(46, 24), y + c.S(56, 26), nm + '  ·  ' + lab, F('Bold', c.FS(40, 18)), WHITE, a, 'lm')
        bx = x0 + c.S(46, 24); by = y + chh - c.S(46, 22) - bh
        rrect(img, bx, by, bx + bw, by + bh, bh / 2, (255, 255, 255), 0.08 * a)
        p1 = eo3(prog(t, ph[0][0] + 0.2 + i * 0.25, 0.8)); p2 = eo3(prog(t, ph[1][0] + 0.05 + i * 0.25, 0.9))
        L1, L2 = bw * pr * p1, bw * car * p2
        if L1 > bh * 0.5: grect(img, bx, by, bx + L1, by + bh, bh / 2, SKY, SKYD)
        if L2 > bh * 0.5: grect(img, bx + L1 - bh / 2, by, bx + L1 + L2, by + bh, bh / 2, CORALL, CORAL)
        v = eo3(prog(t, ph[1][1] - 0.6 + i * 0.2, 0.5))
        text(img, x0 + cw - c.S(46, 24), y + c.S(56, 26), verdict, F('Heavy', c.FS(36, 17)), vcol, v, 'rm')
    ly = (1330 if not c.land else c.S(0, 536))
    circle(img, c.cx - c.S(330, 290), ly, c.S(13, 6), SKY); text(img, c.cx - c.S(300, 262), ly, 'Premiums for the year', F('Medium', c.FS(33, 15)), WHITE, 1.0, 'lm')
    circle(img, c.cx + c.S(60, 24), ly, c.S(13, 6), CORAL); text(img, c.cx + c.S(90, 52), ly, 'What you pay for care', F('Medium', c.FS(33, 15)), WHITE, 1.0, 'lm')
    text(img, c.cx, ly + c.S(60, 22), 'Illustration only, not real prices', F('Regular', c.FS(28, 12)), MUTED, eo3(prog(t, ph[1][0] + 0.6, 0.5)), 'mm')


def a_cost(c, img, t, ph, over='Step 1'):
    title_block(c, img, t, over, 'Total yearly cost')
    w, h = c.S(780, 540), c.S(132, 60); x0 = c.cx - w / 2; yb = c.S(1270, 504); gp = c.S(16, 8)
    blocks = [('Monthly premium × 12', SKY, SKYD, INK), ('Deductible', GOLDL, GOLD, INK), ('Copays and coinsurance', CORALL, CORAL, INK)]
    ys = []
    for i, (lab, c1, c2, fg) in enumerate(blocks):
        y = yb - (i + 1) * (h + gp); ys.append(y)
        p = eo3(prog(t, ph[1][0] + 0.15 + i * (ph[1][1] - ph[1][0]) * 0.33, 0.5)); sl = (1 - p) * c.S(70, 36)
        gh = eo3(prog(t, 0.35 + 0.12 * i, 0.5)) * (1 - p)
        if gh > 0.01: rrect(img, x0, y, x0 + w, y + h, c.S(30, 14), WHITE, 0.16 * gh, outline=2)
        grect(img, x0, y - sl, x0 + w, y + h - sl, c.S(30, 14), c1, c2, p)
        text(img, x0 + w / 2, y + h / 2 - sl, lab, F('Heavy', c.FS(42, 20)), fg, p, 'mm')
    q = eo3(prog(t, ph[2][0] + 0.1, 0.6))
    if q > 0:
        ytop = ys[2] - c.S(26, 12)
        for xx in range(int(x0 - c.S(10, 6)), int(x0 + w), int(c.S(48, 24))): rrect(img, xx, ytop - 3, xx + c.S(28, 14), ytop + 3, 3, TEAL, q)
        bx = x0 - c.S(28, 14); shape(img, (bx - 3, int(ys[2]), bx + 3, int(ys[1] + h)), TEAL, q, lambda d, ss, ww, hh: d.rectangle([0, 0, ww, hh], fill=255))
        glow(img, c.cx, ytop - c.S(40, 20), c.S(380, 220), TEAL, 0.18 * q, 2.2)
        text(img, c.cx, ytop - c.S(42, 20), 'Out-of-pocket maximum', F('Heavy', c.FS(44, 21)), TEAL, q, 'mm')
        text(img, c.cx, ytop - c.S(96, 46), 'caps what you pay for covered, in-network care', F('Medium', c.FS(30, 14)), MUTED, q, 'mm')


def a_check(c, img, t, ph):
    title_block(c, img, t, 'Step 2', 'Doctors and drugs')
    items = [('cross', TEAL, (34, 150, 190), 'Are your doctors and hospitals in the plan network?'), ('pill', GOLD, (230, 140, 40), "Is each prescription on the plan's drug list?"),
             ('pin', SKY, INDIGO, 'And is your pharmacy covered?')]
    cw, chh, gap = c.S(940, 880), c.S(226, 92), c.S(32, 14); y0 = c.S(620, 220)
    for i, (kind, c1, c2, lab) in enumerate(items):
        row_card(c, img, t, c.cx - cw / 2, y0 + i * (chh + gap) + 4 * math.sin(t * 1.4 + i) * c.k, cw, chh, prog(t, ph[i][0] - 0.05, 0.45), kind, c1, c2, lab, prog(t, ph[i][1] - 0.35, 0.5))


METALS = [('Bronze', 60, (222, 160, 108), (150, 92, 52)), ('Silver', 70, (226, 232, 242), (150, 162, 180)), ('Gold', 80, GOLDL, (222, 160, 40)), ('Platinum', 90, (200, 228, 248), (120, 162, 204))]


def a_metal(c, img, t, ph):
    title_block(c, img, t, 'Step 3', 'Metal levels')
    if not c.land: bw, bh, x0, y0, gap = 880, 104, c.cx - 440, 610, 70
    else: bw, bh, x0, y0, gap = c.S(0, 560), c.S(0, 34), c.S(0, 90), c.S(0, 248), c.S(0, 48)
    for i, (nm, pays, c1, c2) in enumerate(METALS):
        y = y0 + i * (bh + gap); p = eo3(prog(t, ph[1][0] + 0.15 + i * 0.28, 0.7))
        early = eo3(prog(t, 0.35 + 0.1 * i, 0.5))
        text(img, x0, y - c.S(32, 15), nm, F('Heavy', c.FS(40, 18)), c1, max(early, clamp(p * 3)), 'lm')
        text(img, x0 + bw, y - c.S(32, 15), 'You pay %d%%' % (100 - pays), F('Semibold', c.FS(36, 16)), WHITE, clamp((p - 0.5) * 2), 'rm')
        rrect(img, x0, y, x0 + bw, y + bh, bh / 2, WHITE, 0.09 * max(early, clamp(p * 3)))
        Lp = bw * pays / 100 * p
        if Lp > bh * 0.6:
            grect(img, x0, y, x0 + Lp, y + bh, bh / 2, c1, c2)
            lo, hi = x0 + bh / 2, x0 + Lp - bh / 2; sx = lo + ((t * 0.35 + i * 0.2) % 1.6 - 0.3) * (hi - lo)
            if hi > lo: shape(img, (max(lo, sx), y + 2, min(hi, sx + bw * 0.1), y + bh - 2), WHITE, 0.15, lambda d, ss, w, h: d.rectangle([0, 0, w, h], fill=255))
        if p > 0.55: text(img, x0 + c.S(38, 18), y + bh / 2, 'Plan pays %d%%' % pays, F('Heavy', c.FS(40, 17)), INK, clamp((p - 0.55) / 0.45), 'lm')
    r = eob(prog(t, ph[2][0] + 0.1, 0.5))
    if r > 0:
        if not c.land: bx, by, w, h = c.cx, y0 + 4 * (bh + gap) - 6, 860, 104
        else: bx, by, w, h = c.S(0, 985), c.S(0, 320), c.S(0, 380), c.S(0, 104)
        glow(img, bx, by, w * 0.6, CORAL, 0.25 * clamp(r), 2.2)
        grect(img, bx - w / 2, by - h / 2, bx + w / 2, by + h / 2, c.S(52, 24), CORALL, CORAL, clamp(r))
        text(img, bx, by, 'Metal level ≠ quality of care' if c.land else 'Metal level  ≠  quality of care', F('Heavy', c.FS(44, 17)), WHITE, clamp(r), 'mm')
    fx, fy = (c.cx, y0 + 4 * (bh + gap) + 80) if not c.land else (c.S(0, 985), c.S(0, 395))
    para(img, fx, fy - (0 if c.land else 18), 'On average. Actual costs vary by plan. Source: HealthCare.gov', F('Regular', c.FS(28, 12)), MUTED, int(c.S(900, 360)), eo3(prog(t, ph[1][0] + 1.2, 0.5)), 1.25)


def a_save(c, img, t, ph):
    title_block(c, img, t, 'Step 4', 'Savings')
    cw, rh, gap = c.S(940, 800), c.S(134, 56), c.S(34, 12); x0 = c.cx - cw / 2; y0 = c.S(640, 230)
    g1 = eo3(prog(t, ph[1][0] + 0.2, 0.6)); g2 = eo3(prog(t, ph[2][0] + 0.15, 0.6))
    for i, (nm, pays, c1, c2) in enumerate(METALS):
        y = y0 + i * (rh + gap); p = eo3(prog(t, 0.15 + i * 0.12, 0.45))
        glass(img, x0, y, x0 + cw, y + rh, c.S(40, 18), p)
        circle(img, x0 + c.S(60, 28), y + rh / 2, c.S(24, 10), c1, p)
        text(img, x0 + c.S(104, 50), y + rh / 2, nm, F('Heavy', c.FS(44, 21)), WHITE, p, 'lm')
        chw1, chw2 = c.S(300, 232), c.S(280, 212); bx = x0 + cw - c.S(36, 16) - chw1 - c.S(18, 8) - chw2
        if g1 > 0:
            grect(img, bx, y + c.S(26, 11), bx + chw1, y + rh - c.S(26, 11), c.S(34, 14), (110, 230, 205), TEAL, g1); text(img, bx + chw1 / 2, y + rh / 2, 'Premium tax credit', F('Heavy', c.FS(30, 13)), INK, g1, 'mm')
        if nm == 'Silver' and g2 > 0:
            bx2 = bx + chw1 + c.S(18, 8)
            grect(img, bx2, y + c.S(26, 11), bx2 + chw2, y + rh - c.S(26, 11), c.S(34, 14), GOLDL, GOLD, g2); text(img, bx2 + chw2 / 2, y + rh / 2, 'Cost-sharing help', F('Heavy', c.FS(30, 13)), INK, g2, 'mm')
            rrect(img, x0 - 6, y - 6, x0 + cw + 6, y + rh + 6, c.S(46, 22), GOLDL, g2, outline=3)
    fy = y0 + 4 * (rh + gap) + c.S(50, 20)
    text(img, c.cx, fy, 'If you qualify. Cost-sharing reductions only come with Silver plans.', F('Medium', c.FS(31, 14)), MUTED, g2, 'mm')


def a_dates(c, img, t, ph):
    title_block(c, img, t, 'Mark the dates', 'Open Enrollment')
    pts = [('Nov 1', 'Open Enrollment starts', ph[1][0] + 0.1), ('Dec 15', 'Last day to enroll for Jan 1 coverage', ph[1][0] + 1.9), ('Jan 15', 'Open Enrollment ends', ph[1][0] + 4.1)]
    total = prog(t, pts[0][2], pts[2][2] - pts[0][2] + 0.4)
    if not c.land:
        lx, y0, step = 230, 640, 245
        shape(img, (lx - 4, y0, lx + 4, y0 + 2 * step), (80, 100, 150), 0.6, lambda d, ss, w, h: d.rectangle([0, 0, w, h], fill=255))
        shape(img, (lx - 4, y0, lx + 4, y0 + max(1, int(2 * step * total))), GOLD, 1.0, lambda d, ss, w, h: d.rectangle([0, 0, w, h], fill=255))
        for i, (d, lab, ts) in enumerate(pts):
            y = y0 + i * step; p = eob(prog(t, ts, 0.5)); col = GOLD if i != 1 else CORAL
            early = 0.28 * eo3(prog(t, 0.4 + 0.12 * i, 0.5))
            glow(img, lx, y, 90 * clamp(p), col, 0.35, 2.2); circle(img, lx, y, 28 * clamp(p) if p > 0.02 else 14 * early * 3.5, col, 1.0 if p > 0.02 else early * 2)
            text_grad(img, lx + 90, y - 30, d, F('Black', 84), GOLDL if i != 1 else CORALL, col, max(clamp(p), early), 'lm')
            para(img, lx + 90, y + 18, lab, F('Semibold', 38), WHITE, 640, clamp(p), 1.15, align='left')
            img  # keep
        v = eob(prog(t, ph[2][0] + 0.3, 0.5))
        if v > 0:
            glass(img, c.cx - 440, 1210, c.cx + 440, 1326, 58, clamp(v))
            text(img, c.cx, 1268, 'Virginia: through Jan 29', F('Heavy', 46), GOLDL, clamp(v), 'mm')
        text(img, c.cx, 1380, 'State exchanges can differ  ·  Source: HealthCare.gov', F('Regular', 28), MUTED, clamp(v), 'mm')
    else:
        y = c.S(0, 275); xs = [c.S(0, 210), c.S(0, 640), c.S(0, 1070)]
        shape(img, (xs[0], y - 3, xs[2], y + 3), (80, 100, 150), 0.6, lambda d, ss, w, h: d.rectangle([0, 0, w, h], fill=255))
        shape(img, (xs[0], y - 3, xs[0] + max(1, int((xs[2] - xs[0]) * total)), y + 3), GOLD, 1.0, lambda d, ss, w, h: d.rectangle([0, 0, w, h], fill=255))
        for i, (d, lab, ts) in enumerate(pts):
            p = eob(prog(t, ts, 0.5)); col = GOLD if i != 1 else CORAL
            early = 0.28 * eo3(prog(t, 0.4 + 0.12 * i, 0.5))
            glow(img, xs[i], y, c.S(0, 50) * clamp(p), col, 0.35, 2.2); circle(img, xs[i], y, c.S(0, 12) * clamp(p) if p > 0.02 else c.S(0, 8) * 3.5 * early, col, 1.0 if p > 0.02 else early * 2)
            text_grad(img, xs[i], y - c.S(0, 52), d, F('Black', c.FS(0, 46)), GOLDL if i != 1 else CORALL, col, max(clamp(p), early), 'mm')
            para(img, xs[i], y + c.S(0, 30), lab, F('Semibold', c.FS(0, 21)), WHITE, int(c.S(0, 330)), clamp(p), 1.15)
        v = eob(prog(t, ph[2][0] + 0.3, 0.5))
        if v > 0:
            glass(img, c.cx - c.S(0, 250), c.S(0, 400), c.cx + c.S(0, 250), c.S(0, 458), c.S(0, 29), clamp(v))
            text(img, c.cx, c.S(0, 429), 'Virginia: through Jan 29', F('Heavy', c.FS(0, 27)), GOLDL, clamp(v), 'mm')
        text(img, c.cx, c.S(0, 496), 'State exchanges can differ  ·  Source: HealthCare.gov', F('Regular', c.FS(0, 15)), MUTED, clamp(v), 'mm')


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


# ------------------------------------------------------------------ short cut-downs for Shorts / Reels / TikTok (vertical only; not embedded on the site)
_cost = dict(ACA['scenes'][1])
_cost['phr'] = [('First, estimate your total yearly cost.', 'First, estimate your total yearly cost.')] + list(_cost['phr'][1:])
_cost['draw'] = lambda c, img, t, ph: a_cost(c, img, t, ph, over='The key idea')
PART_D_SHORT = dict(slug='part-d-late-penalty-short', title='Part D late enrollment penalty in 45 seconds', poster=2.6, disclaimer=PART_D['disclaimer'],
                    scenes=[PART_D['scenes'][0], PART_D['scenes'][1], PART_D['scenes'][4], PART_D['scenes'][5]])
ACA_SHORT = dict(slug='aca-premium-vs-total-cost-short', title='ACA: the premium is not the whole cost', poster=3.2, disclaimer=ACA['disclaimer'],
                 scenes=[ACA['scenes'][0], _cost, ACA['scenes'][6]])
VIDEOS.update({'part-d-short': PART_D_SHORT, 'aca-short': ACA_SHORT})


# ------------------------------------------------------------------ VIDEO 3: Medicare Annual Enrollment Period (facts: Medicare.gov "Joining a plan" and CMS Medicare Open Enrollment page)
def fit_font(weight, s_, maxw, maxsize):
    size = int(maxsize)
    while size > 20 and F(weight, size).getlength(s_) > maxw: size -= 4
    return F(weight, size)


def m_hook(c, img, t, ph):
    title_block(c, img, t, 'Medicare annual enrollment')
    f = fit_font('Black', 'Oct 15 – Dec 7', c.W * c.R(0.86, 0.62), c.S(200, 140))
    ncy = c.S(720, 280); a = eo3(prog(t, 0.15, 0.4))
    glow(img, c.cx, ncy, c.S(520, 300), GOLD, 0.30 * a * (0.85 + 0.15 * math.sin(t * 2.2)), 2.2)
    for k in range(3):
        ph_ = ((t * 0.38) + k / 3) % 1.0
        ring_line(img, c.cx, ncy, lerp(c.S(240, 130), c.S(520, 290), ph_), c.S(3, 2), GOLDL, (1 - ph_) * 0.28 * a)
    text_grad(img, c.cx, ncy, 'Oct 15 – Dec 7', f, GOLDL, GOLD, a, 'mm')
    text(img, c.cx, ncy + f.size * 0.78, 'every year', F('Medium', c.FS(56, 24)), WHITE, eo3(prog(t, 0.6, 0.5)), 'mm')
    bw = c.S(860, 640); bh = c.S(86, 40); x0 = c.cx - bw / 2; y = c.S(1090, 438)
    glass(img, x0 - 18, y - 18, x0 + bw + 18, y + bh + 18, c.S(52, 24), eo3(prog(t, 0.3, 0.5)), shadow=False)
    days = [31, 30, 31]; tot = sum(days); xm = x0
    for i, (nm, d) in enumerate(zip(('Oct', 'Nov', 'Dec'), days)):
        w = bw * d / tot
        text(img, xm + w / 2, y + bh + c.S(44, 20), nm, F('Semibold', c.FS(38, 16)), MUTED, eo3(prog(t, 0.5 + 0.1 * i, 0.4)), 'mm')
        if i: shape(img, (xm - 1, y, xm + 1, y + bh), WHITE, 0.25, lambda d_, ss, w_, h_: d_.rectangle([0, 0, w_, h_], fill=255))
        xm += w
    xs, xe = x0 + bw * 14 / tot, x0 + bw * 68 / tot
    p0 = eio(prog(t, ph[0][0] + 0.7, max(ph[0][1] - ph[0][0] - 1.0, 1.0)))
    if p0 > 0.01:
        grect(img, xs, y, xs + (xe - xs) * p0, y + bh, bh / 2, GOLDL, GOLD)
        text(img, xs, y - c.S(40, 18), 'Oct 15', F('Heavy', c.FS(36, 16)), GOLDL, eo3(prog(t, ph[0][0] + 0.7, 0.4)), 'mm')
    if p0 > 0.97: text(img, xe, y - c.S(40, 18), 'Dec 7', F('Heavy', c.FS(36, 16)), GOLDL, eo3((p0 - 0.97) / 0.03), 'mm')
    q = eo3(prog(t, ph[1][0] + 0.1, 0.5))
    if q > 0:
        shape(img, (x0 + bw - 2, y - c.S(14, 6), x0 + bw + 2, y + bh + c.S(14, 6)), TEAL, q, lambda d_, ss, w_, h_: d_.rectangle([0, 0, w_, h_], fill=255))
        glyph(img, 'flag', x0 + bw - c.S(30, 14), y + bh + c.S(120, 54), c.S(60, 28), TEAL, q)
        text(img, x0 + bw - c.S(60, 28), y + bh + c.S(120, 54), 'Jan 1: changes start', F('Bold', c.FS(36, 16)), WHITE, q, 'rm')


def m_change(c, img, t, ph):
    title_block(c, img, t, 'Annual enrollment', 'What you can change')
    items = [('doc', GOLD, (230, 140, 40), 'Join, drop or switch a Medicare Advantage plan'),
             ('shield', TEAL, (34, 150, 190), 'Move between Original Medicare and Medicare Advantage'),
             ('pill', SKY, INDIGO, 'Join, drop or switch a Part D drug plan (with Original Medicare)')]
    cw, chh, gap = c.S(940, 880), c.S(230, 92), c.S(34, 14); y0 = c.S(640, 232)
    for i, (kind, c1, c2, lab) in enumerate(items):
        row_card(c, img, t, c.cx - cw / 2, y0 + i * (chh + gap) + 4 * math.sin(t * 1.4 + i) * c.k, cw, chh, prog(t, ph[i][0] - 0.05, 0.45), kind, c1, c2, lab, prog(t, ph[i][1] - 0.4, 0.5))


def m_review(c, img, t, ph):
    title_block(c, img, t, 'Before you decide', 'Your review checklist')
    items = [('doc', GOLD, (230, 140, 40), 'Read your Annual Notice of Change'), ('pill', SKY, INDIGO, 'Check your drugs, doctors and pharmacy'),
             ('calendar', TEAL, (34, 150, 190), 'Compare total yearly cost, not just the premium'), ('clock', CORAL, (220, 70, 110), 'Make sure your plan gets your request by Dec 7')]
    cw, chh, gap = c.S(940, 880), c.S(190, 78), c.S(28, 11); y0 = c.S(610, 220)
    for i, (kind, c1, c2, lab) in enumerate(items):
        row_card(c, img, t, c.cx - cw / 2, y0 + i * (chh + gap) + 4 * math.sin(t * 1.4 + i) * c.k, cw, chh, prog(t, ph[i][0] - 0.05, 0.45), kind, c1, c2, lab, prog(t, ph[i][1] - 0.4, 0.5))


def m_happy(c, img, t, ph):
    title_block(c, img, t, 'Happy with your plan?')
    a = eo3(prog(t, 0.2, 0.5)); cy = c.S(820, 330)
    check_badge(img, c.cx, cy, c.S(120, 58), prog(t, 0.5, 0.8))
    w, h = c.S(900, 760), c.S(220, 100); y = c.S(1040, 410)
    glass(img, c.cx - w / 2, y + (1 - a) * 30, c.cx + w / 2, y + h + (1 - a) * 30, c.S(46, 22), a)
    text_grad(img, c.cx, y + h / 2 + (1 - a) * 30, 'No action needed.', F('Black', c.FS(76, 34)), WHITE, (200, 215, 240), a, 'mm')


MEDICARE_AEP = dict(
    slug='medicare-annual-enrollment-short', title='Medicare Annual Enrollment: Oct 15 to Dec 7, what you can change and how to review', poster=3.5, disclaimer=PART_D['disclaimer'],
    scenes=[
        dict(phr=[("Every year, Medicare's Annual Enrollment Period runs October 15 to December 7.", "Every year, Medicare's Annual Enrollment Period runs October fifteenth to December seventh."),
                  ('Changes you make generally start January 1.', 'Changes you make generally start January first.')], draw=m_hook, sfx=lambda ph: [(ph[1][0] + 0.15, 'ding')], pre=0.1, post=0.7),
        dict(phr=[('During that window, you can join, drop or switch a Medicare Advantage plan.', 'During that window, you can join, drop or switch a Medicare Advantage plan.'),
                  ('Move between Original Medicare and Medicare Advantage, in either direction.', 'Move between Original Medicare and Medicare Advantage, in either direction.'),
                  ('Or join, drop or switch a Part D drug plan if you have Original Medicare.', 'Or join, drop or switch a Part D drug plan if you have Original Medicare.')],
             draw=m_change, sfx=lambda ph: [(ph[k][1] - 0.35, 'ding') for k in (0, 1, 2)], pre=0.15, post=0.6),
        dict(phr=[("Before you decide, read your plan's Annual Notice of Change.", "Before you decide, read your plan's Annual Notice of Change."),
                  ('Check that your drugs, doctors and pharmacy are still covered.', 'Check that your drugs, doctors and pharmacy are still covered.'),
                  ('Compare the total yearly cost, not just the premium.', 'Compare the total yearly cost, not just the premium.'),
                  ('And make sure your plan gets your request by December 7.', 'And make sure your plan gets your request by December seventh.')],
             draw=m_review, sfx=lambda ph: [(ph[k][1] - 0.35, 'ding') for k in (0, 1, 2, 3)], pre=0.15, post=0.6),
        dict(phr=[('If your plan still meets your needs and is still offered, you do not have to do anything.', 'If your plan still meets your needs and is still offered, you do not have to do anything.')],
             draw=m_happy, sfx=lambda ph: [(ph[0][0] + 1.0, 'ding')], pre=0.15, post=0.8),
        PART_D['scenes'][5],
    ])
MEDICARE_AEP['scenes'][-1] = dict(PART_D['scenes'][5])
VIDEOS['aep'] = MEDICARE_AEP

