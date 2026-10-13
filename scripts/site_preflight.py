#!/usr/bin/env python3
"""Preflight for Honorbrook site batches. Read-only: it never edits or commits anything.

Usage (from repo root):
  python3 scripts/site_preflight.py            # files changed vs origin/main plus untracked files under site/
  python3 scripts/site_preflight.py --all      # every page under site/
  python3 scripts/site_preflight.py site/blog/x.html site/y.html

Prints ERROR (must fix), WARN (look at it) per file, then cross-site duplicate-topic warnings.
Exit code 1 if any ERROR.
"""
import re, os, sys, json, glob, subprocess, difflib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SITE = os.path.join(ROOT, 'site')
STATE_AB = {'va', 'md', 'nc', 'sc', 'ga', 'al', 'la', 'tx', 'mi', 'in', 'wv'}

BANNED = [  # (pattern, label, severity)
    (r'free plan', 'says "free plan"', 'ERROR'),
    (r'(?<![\w])\$0(?![\d,.])', 'says "$0"', 'ERROR'),
    (r'guaranteed (income|returns?|growth)', 'promises guaranteed income/returns/growth', 'ERROR'),
    (r'tax[- ]free retirement', 'says "tax-free retirement"', 'ERROR'),
    (r'(no|zero) risk|risk[- ]free', 'says no risk', 'ERROR'),
    (r'act now|limited time|don.t wait|hurry', 'urgency wording', 'ERROR'),
    (r'#1\b|number one|top[- ]rated|best[- ]in', 'superlative', 'ERROR'),
    (r'official medicare(?! (information|resources|website|site|plan finder|sources))|government[- ]approved', 'implies government affiliation', 'ERROR'),
    (r'best (plan|policy|option|way|rates?)\b', 'says "best plan/policy/option"', 'WARN'),
    (r'\bnever lose\b|\bcannot lose\b|beat the market', 'investment promise', 'ERROR'),
]
LIFE_KEYS = ('iul', 'fixed-indexed', 'annuit', 'cash-value', 'policy-loan', 'high-income', 'universal-life')
KIDS_KEYS = ('kids', '529', 'gerber', 'juvenile', 'college')


def files_to_check(argv):
    if '--all' in argv:
        return sorted(glob.glob(SITE + '/**/*.html', recursive=True))
    paths = [a for a in argv if not a.startswith('--')]
    if paths:
        return [os.path.abspath(p) for p in paths]
    out = set()
    for cmd in (['git', 'diff', '--name-only', 'origin/main', '--', 'site'],
                ['git', 'ls-files', '--others', '--exclude-standard', 'site'],
                ['git', 'diff', '--name-only', '--', 'site']):
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        out.update(l for l in r.stdout.split('\n') if l.endswith('.html'))
    return sorted(os.path.join(ROOT, p) for p in out if os.path.exists(os.path.join(ROOT, p)))


def redirects():
    p = os.path.join(SITE, '_redirects')
    if not os.path.exists(p):
        return set()
    return {l.split()[0] for l in open(p) if l.strip() and not l.startswith('#')}


def link_ok(l, red):
    l = l.split('#')[0].split('?')[0]
    if l in ('', '/'):
        return True
    p = l[1:]
    return (os.path.exists(os.path.join(SITE, p)) or os.path.exists(os.path.join(SITE, p + '.html'))
            or os.path.exists(os.path.join(SITE, p.rstrip('/'), 'index.html')) or l in red)


def check(path, red):
    rel = os.path.relpath(path, SITE)
    h = open(path, encoding='utf-8').read()
    msgs = []
    art = re.search(r'<article.*?</article>', h, re.S)
    body = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', art.group(0) if art else h))
    title = (re.search(r'<title>(.*?)</title>', h, re.S) or [None, ''])[1]
    desc = (re.search(r'name="description" content="([^"]*)"', h) or [None, ''])[1]
    slug = os.path.basename(path)[:-5]

    for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            j = json.loads(x)
            if j.get('@type') in ('AggregateRating', 'Review'):
                msgs.append(('ERROR', 'review markup on own site (Google can penalize)'))
            if j.get('@type') == 'BlogPosting':
                if 'dateModified' not in j: msgs.append(('WARN', 'BlogPosting has no dateModified'))
                if not isinstance(j.get('author'), dict) or '@id' not in j['author']: msgs.append(('WARN', 'author is not linked to the Luay Sadqi profile'))
        except Exception:
            msgs.append(('ERROR', 'invalid JSON-LD'))
    if h.count('<details>') != h.count('</details>'):
        msgs.append(('ERROR', 'unbalanced <details>'))
    for pat, label, sev in BANNED:
        if re.search(pat, body + ' ' + title + ' ' + desc, re.I):
            if label.startswith('promises guaranteed') and 'claims-paying' in body.lower():
                sev = 'WARN'  # contractual guarantee (e.g. SPIA income) with the carrier-ability caveat present: a human should still read it
            msgs.append((sev, label))
    canon = re.search(r'rel="canonical" href="([^"]+)"', h)
    if not canon:
        msgs.append(('ERROR', 'no canonical'))
    elif not (canon.group(1).rstrip('/').endswith(slug) or slug == 'index'):
        msgs.append(('WARN', 'canonical does not match filename'))
    if len(title) > 75: msgs.append(('WARN', f'title is {len(title)} characters (Google shows about 60)'))
    if len(desc) > 170: msgs.append(('WARN', f'meta description is {len(desc)} characters'))
    bad = sorted({l for l in re.findall(r'href="(/[^"]*)"', h) if not link_ok(l, red)})
    if bad:
        msgs.append(('ERROR', 'broken internal links: ' + ', '.join(bad[:6])))

    medicare = len(re.findall(r'Medicare Advantage|Part D|Medigap|Medicare Supplement', body)) >= 2
    aca_or_life = not medicare
    if medicare and 'do not offer every plan available in your area' not in h:
        msgs.append(('ERROR', 'Medicare content without the CMS disclaimer'))
    if not medicare and not ('independent' in h.lower() and 'not connected with' in h.lower()) and rel not in ('index.html',):
        msgs.append(('WARN', 'no independent-agency disclaimer in footer'))
    m = re.search(r'-(%s)-(medicare-insurance|aca-health-insurance)$' % '|'.join(STATE_AB), slug)
    if m and m.group(1) != 'va' and re.search(r'our office|local office|nearby|come to you|in-person|in person(?! (county|parish))', body, re.I):
        msgs.append(('ERROR', 'implies a local office or in-person service outside Northern Virginia'))
    if rel.startswith('blog/') and slug != 'index':
        low = body.lower()
        if any(k in slug for k in LIFE_KEYS):
            for need, label in (('claims-paying', 'claims-paying ability'), ('surrender', 'surrender charges'), ('not (tax|legal|investment|financial)|not insurance advice', 'not-advice note')):
                if not re.search(need, low): msgs.append(('ERROR', f'indexed/cash-value/annuity post missing {label}'))
        if any(k in slug for k in KIDS_KEYS) and re.search(r'better than (a )?529|beats? a 529', low):
            msgs.append(('ERROR', 'compares life insurance as better than a 529'))
        if not any(k in h for k in ('Medicare help in your state', 'Availability and rules vary by state', 'Medicare Advantage by ', 'Changing Medicare plans in other states')):
            msgs.append(('WARN', 'no all-11-states block'))
    if 'noindex' in h:
        msgs.append(('INFO', 'noindex'))
    return rel, msgs


def duplicates():
    T = {}
    for f in glob.glob(SITE + '/blog/*.html'):
        s = os.path.basename(f)[:-5]
        if s == 'index' or s.startswith('when-can-i-change-my-medicare-plan-in-'):
            continue
        m = re.search(r'<h1[^>]*>(.*?)</h1>', open(f).read(), re.S)
        T[s] = re.sub(r'<[^>]+>', '', m.group(1)).strip().lower() if m else s
    out, ks = [], sorted(T)
    for i, a in enumerate(ks):
        for b in ks[i + 1:]:
            r = difflib.SequenceMatcher(None, T[a], T[b]).ratio()
            sa, sb = set(re.findall(r'[a-z]{4,}', a)), set(re.findall(r'[a-z]{4,}', b))
            j = len(sa & sb) / max(1, len(sa | sb))
            if (r > 0.75 and j > 0.6) or j > 0.8:
                out.append((a, b, round(r, 2), round(j, 2)))
    return out


def main():
    argv = sys.argv[1:]
    red = redirects()
    files = files_to_check(argv)
    errors = warns = 0
    for f in files:
        rel, msgs = check(f, red)
        for sev, m in msgs:
            if sev == 'INFO':
                continue
            print(f'{sev:5} {rel}: {m}')
            errors += sev == 'ERROR'; warns += sev == 'WARN'
    d = duplicates()
    for a, b, r, j in d:
        print(f'WARN  duplicate topic? blog/{a}  <->  blog/{b}  (title match {r}, word overlap {j})')
    print(f'\nchecked {len(files)} files: {errors} errors, {warns} warnings, {len(d)} possible duplicate topics')
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
