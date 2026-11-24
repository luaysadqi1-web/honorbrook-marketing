"""Onyx brand assets: silver HB mark, favicons, share image, portrait crops, chat avatar."""
import base64, io, os
import phone
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRAND = os.path.join(ROOT, 'social', 'brand')


def mono(): return Image.open(os.path.join(BRAND, 'hb-monogram.png')).convert('RGBA')


def tile(w, h, mono_h, bg=(5, 5, 6)):
    im = Image.new('RGBA', (w, h), bg + (255,)); m = mono()
    m = m.resize((int(m.width * mono_h / m.height), mono_h), Image.LANCZOS)
    im.alpha_composite(m, ((w - m.width) // 2, (h - m.height) // 2)); return im


def _font(path, size, var=None):
    f = ImageFont.truetype(path, size)
    if var:
        try: f.set_variation_by_name(var)
        except Exception: pass
    return f


def _spaced(d, xy, s, f, fill, track):
    x, y = xy
    for ch in s: d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + track


def og(out):
    W, H = 1200, 630; g = Image.new('RGB', (W, H), (5, 5, 6)); d = ImageDraw.Draw(g); d.ellipse((620, -260, 1320, 300), fill=(44, 47, 56))
    im = g.filter(ImageFilter.GaussianBlur(150))
    lock = Image.open(os.path.join(BRAND, 'hb-logo-lockup.png')).convert('RGBA'); lh = 420
    lock = lock.resize((int(lock.width * lh / lock.height), lh), Image.LANCZOS)
    im.paste(lock, (36, (H - lh) // 2), lock)
    d = ImageDraw.Draw(im); X, RW = 748, 410
    sans = '/System/Library/Fonts/SFNS.ttf'; ser = '/System/Library/Fonts/Supplemental/Georgia Italic.ttf'
    ov = 'INDEPENDENT INSURANCE AGENCY'; f = _font(sans, 17, 'Semibold')
    track = (RW - sum(d.textlength(c, font=f) for c in ov)) / (len(ov) - 1)
    _spaced(d, (X, 178), ov, f, (170, 176, 186), track)
    d.line((X, 216, X + RW, 216), fill=(96, 101, 112), width=1)
    d.text((X, 250), 'The right coverage.', font=_font(ser, 44), fill=(244, 245, 247))
    d.text((X, 310), 'The honest way.', font=_font(ser, 44), fill=(244, 245, 247))
    _spaced(d, (X, 398), 'LICENSED IN 15 STATES + DC', _font(sans, 16, 'Semibold'), (170, 176, 186), 3.4)
    _spaced(d, (X, 436), phone.DISPLAY, _font(sans, 30, 'Medium'), (217, 220, 226), 5)
    im.save(out, quality=92)


def apply(site):
    A = os.path.join(site, 'assets')
    m = mono(); m.save(os.path.join(A, 'hb-mark.png'), optimize=True)
    s = m.resize((300, round(300 * m.height / m.width)), Image.LANCZOS); b = io.BytesIO(); s.save(b, 'PNG', optimize=True)
    open(os.path.join(A, 'logo.svg'), 'w').write('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 %d %d" role="img" aria-label="Honorbrook Insurance"><rect width="100%%" height="100%%" fill="#050506"/><image width="%d" height="%d" xlink:href="data:image/png;base64,%s"/></svg>' % (s.width, s.height, s.width, s.height, base64.b64encode(b.getvalue()).decode()))
    for n in (16, 32, 64): tile(n, n, int(n * .62)).convert('RGB').save(os.path.join(site, 'favicon-%d.png' % n))
    tile(256, 256, 160).convert('RGB').save(os.path.join(site, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    tile(180, 180, 112).convert('RGB').save(os.path.join(site, 'apple-touch-icon.png'))
    tile(240, 288, 150).convert('RGB').save(os.path.join(A, 'logo-static.png'))
    og(os.path.join(A, 'og-image.jpg'))
    p = Image.open(os.path.join(ROOT, 'site', 'assets', 'luay-sadqi.jpg')).convert('RGB')
    p.crop((105, 150, 555, 780)).save(os.path.join(A, 'luay.jpg'), quality=92)
    p.crop((215, 200, 445, 430)).resize((340, 340), Image.LANCZOS).save(os.path.join(A, 'luay-face.jpg'), quality=92)
    # chat panel avatar: the silver mark instead of the old shield
    c = os.path.join(A, 'chat.js'); L = open(c, encoding='utf-8').read().split('\n')
    for i, ln in enumerate(L):
        if ln.lstrip().startswith('var CREST ='):
            j = i + 1
            while not L[j].rstrip().endswith(';'): j += 1
            L[i:j + 1] = ["  var CREST = '<img src=\"/assets/hb-mark.png\" alt=\"\" width=\"34\" height=\"29\" style=\"display:block;width:34px;height:auto\">';"]
            break
    open(c, 'w', encoding='utf-8').write('\n'.join(L))
