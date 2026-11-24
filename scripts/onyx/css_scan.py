"""Shared CSS helpers for the Onyx build: collect every rule (style.css + unique inline <style> blocks) with its declarations."""
import glob, os, re

COMMENT = re.compile(r'/\*.*?\*/', re.S)

def split_rules(css, media=''):
    """Yield (media, selector, declarations) for a CSS string; handles one level of @media nesting."""
    css = COMMENT.sub('', css); i = 0; n = len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0: break
        sel = css[i:j].strip()
        depth = 1; k = j + 1
        while k < n and depth:
            if css[k] == '{': depth += 1
            elif css[k] == '}': depth -= 1
            k += 1
        body = css[j + 1:k - 1]
        if sel.startswith('@media') or sel.startswith('@supports'):
            yield from split_rules(body, sel)
        elif sel.startswith('@'):
            pass  # @keyframes, @font-face, @import
        else:
            yield media, re.sub(r'\s+', ' ', sel), body.strip()
        i = k

def decls(body):
    out = []
    for d in re.split(r';(?![^(]*\))', body):
        if ':' in d:
            p, v = d.split(':', 1); out.append((p.strip().lower(), v.strip()))
    return out

def site_css(site):
    """Return {(media, selector): {prop: value}} merged over style.css and every inline <style> block. Also conflicts."""
    rules = {}; conflicts = {}; src = {}
    def add(media, sel, body, origin):
        for s in [x.strip() for x in sel.split(',')]:
            key = (media, s); cur = rules.setdefault(key, {})
            for p, v in decls(body):
                if p in cur and cur[p] != v and origin != 'style.css' and src.get((key, p)) != origin:
                    conflicts.setdefault((key, p), set()).update([cur[p], v])
                cur[p] = v; src[(key, p)] = origin
    base = open(os.path.join(site, 'assets', 'style.css'), encoding='utf-8').read()
    for m, s, b in split_rules(base): add(m, s, b, 'style.css')
    seen = set()
    for f in sorted(glob.glob(os.path.join(site, '**', '*.html'), recursive=True)):
        t = open(f, encoding='utf-8', errors='ignore').read()
        for blk in re.findall(r'<style[^>]*>(.*?)</style>', t, re.S):
            h = hash(blk)
            if h in seen: continue
            seen.add(h)
            for m, s, b in split_rules(blk): add(m, s, b, os.path.relpath(f, site))
    return rules, conflicts
