"""Onyx palette compiler: turn every color in the site's CSS (style.css + all inline <style> rules) into its Onyx equivalent.

The design layer (theme_css.py) sets the crafted look for the main components. This compiler is the safety net under it:
it guarantees no page type keeps a white card, navy text or gold accent, because it rewrites every rule that carries a color.
"""
import colorsys, re

HEX = re.compile(r'#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b')
RGBA = re.compile(r'rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)')
VAR = re.compile(r'var\(\s*(--[a-z-]+)\s*(?:,[^)]*)?\)')

# legacy variable names keep working, pointed at Onyx values (majority use); the minority use is fixed per rule below
VARS = {
    '--navy': '#eceef2', '--navy-d': '#050506', '--gold': '#c5cad2', '--gold-l': '#f2f4f7', '--gold-d': '#aab0ba',
    '--cream': '#050506', '--cream-d': '#08090b', '--ink': '#d9dce2', '--muted': '#9aa1ac', '--white': '#0c0d10',
    '--line': 'rgba(255,255,255,.10)', '--green': '#57d9a3',
}
# variable used in the "wrong" role for its new value: (context, var) -> explicit color
VAR_FIX = {
    ('text', '--white'): '#ffffff', ('text', '--cream'): '#f2f4f7', ('text', '--cream-d'): '#f2f4f7',
    ('bg', '--navy'): '#15161b', ('bg', '--ink'): '#15161b', ('bg', '--muted'): '#2a2c33',
    ('border', '--navy'): 'rgba(255,255,255,.30)', ('border', '--white'): 'rgba(255,255,255,.14)', ('border', '--navy-d'): 'rgba(255,255,255,.14)',
    ('border', '--cream'): 'rgba(255,255,255,.10)', ('border', '--cream-d'): 'rgba(255,255,255,.10)',
}


def _hsl(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r, g, b); return h * 360, s, l


def _fmt(r, g, b, a=1.0):
    r, g, b = [max(0, min(255, round(x))) for x in (r, g, b)]
    return '#%02x%02x%02x' % (r, g, b) if a >= 1 else 'rgba(%d,%d,%d,%s)' % (r, g, b, ('%.2f' % a).rstrip('0').rstrip('.'))


def _silver(l):
    """A cool neutral at lightness l (0-1)."""
    r, g, b = colorsys.hls_to_rgb(220 / 360, l, 0.07); return _fmt(r * 255, g * 255, b * 255)


def remap(r, g, b, a, ctx):
    h, s, l = _hsl(r, g, b)
    red = (h <= 20 or h >= 340) and s > .35
    green = 85 <= h <= 175 and s > .2
    gold = 28 <= h <= 62 and s > .3
    if ctx == 'text':
        if a < 1: return _fmt(255, 255, 255, max(a, .55))
        if red: return '#ff9d94' if l < .6 else '#ffb9b2'
        if green: return '#6fe0ae'
        if gold and l < .5: return '#c5cad2'
        if l < .30: return '#eceef2'
        if l < .56: return '#a7adb7'
        return _silver(max(l, .66))
    if ctx == 'bg':
        if a < 1:
            if gold: return _fmt(255, 255, 255, round(a * .6, 2))
            if l > .6: return _fmt(255, 255, 255, a)
            return _fmt(0, 0, 0, min(.82, a * 1.35))
        if red: return 'rgba(255,107,97,.12)' if l > .8 else '#e5484d'
        if green: return 'rgba(87,217,163,.10)' if l > .8 else '#1f8a5f'
        if gold and l < .8: return '#f2f4f7' if l > .58 else '#c5cad2' if l > .4 else '#aab0ba'
        if l >= .93: return '#0c0d10'
        if l >= .5: return '#111216'
        if l < .15: return '#050506'
        if l < .27: return '#0b0c0f'
        return '#15161b'
    if ctx == 'border':
        if a < 1:
            if l > .6 and not gold: return _fmt(255, 255, 255, a)
            return _fmt(255, 255, 255, round(min(.4, a * .7), 2))
        if red: return '#ff6b61'
        if green: return 'rgba(87,217,163,.35)'
        if gold: return 'rgba(255,255,255,.26)'
        if l >= .75: return 'rgba(255,255,255,.14)'
        if l >= .5: return 'rgba(255,255,255,.22)'
        return 'rgba(255,255,255,.09)'
    # shadow
    if gold: return _fmt(255, 255, 255, round(min(.12, a * .3), 2))
    return _fmt(0, 0, 0, min(.8, a * 3 + .25))


def context(prop):
    if prop.startswith('background'): return 'bg'
    if 'shadow' in prop or prop == 'filter': return 'shadow'
    if prop.startswith('border') or prop.startswith('outline') or prop.startswith('column-rule'): return 'border'
    if prop in ('color', 'fill', 'stroke', '-webkit-text-fill-color', 'caret-color', 'text-decoration-color', 'text-decoration'): return 'text'
    return None


def _hexparse(h):
    if len(h) in (3, 4): h = ''.join(c * 2 for c in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
    return r / 255, g / 255, b / 255, a


def convert(prop, value):
    """Return the Onyx value for a declaration, or None when nothing needs to change."""
    ctx = context(prop)
    if not ctx or 'url(' in value: return None
    v = value
    v = HEX.sub(lambda m: remap(*_hexparse(m.group(1)), ctx), v)
    v = RGBA.sub(lambda m: remap(float(m.group(1)) / 255, float(m.group(2)) / 255, float(m.group(3)) / 255, float(m.group(4)) if m.group(4) else 1.0, ctx), v)
    v = VAR.sub(lambda m: VAR_FIX.get((ctx, m.group(1)), m.group(0)), v)
    if ctx == 'bg': v = re.sub(r'(?<![-\w#])white(?![-\w])', '#0c0d10', v)
    return v if v != value else None


def prefixed(sel):
    """Raise a selector above any page-level rule: html body <selector>."""
    s = sel.strip()
    if s.startswith('html body'): return s
    if s in (':root', 'html', '*'): return None
    if s == 'body': return 'html body'
    if s.startswith('body.') or s.startswith('body '): return 'html ' + s
    if s.startswith('html'): return s
    return 'html body ' + s


def compile_rules(rules):
    """rules: {(media, selector): {prop: value}} -> CSS text of Onyx overrides."""
    by_media = {}
    for (media, sel), d in rules.items():
        ps = prefixed(sel)
        if not ps: continue
        out = []
        for p, v in d.items():
            imp = ''
            if v.endswith('!important'): v, imp = v[:-len('!important')].strip(), '!important'
            nv = convert(p, v)
            if nv: out.append('%s:%s%s' % (p, nv, imp))
        if out: by_media.setdefault(media, []).append('%s{%s}' % (ps, ';'.join(out)))
    parts = by_media.pop('', [])
    css = '\n'.join(parts)
    for media, rs in by_media.items(): css += '\n%s{\n%s\n}' % (media, '\n'.join(rs))
    return css


def root_vars():
    return ':root{' + ';'.join('%s:%s' % kv for kv in VARS.items()) + '}'
