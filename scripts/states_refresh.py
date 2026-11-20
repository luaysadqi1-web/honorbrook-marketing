#!/usr/bin/env python3
"""Bring every page in line with the current license list (15 states + DC) without hardcoding a count.

What it does, sitewide and idempotently:
  - footer, top bar and body copy that said "11 states" / "10 more states"
  - explicit state lists in prose, the footer "licensed" line, blog state blocks, homepage tiles
  - JSON-LD areaServed / contentLocation arrays
  - Georgia pages: licence is not active, so the licensing sentences become information-only wording
  - nav and footer links to the newer product pages
  - llms.txt, sitemap.xml, find.js (ZIP finder), the chatbot prompt, duplicate-post redirects

Edit LICENSED below when a licence is added or dropped, then run from the repo root:
    python3 scripts/states_refresh.py
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
BASE = 'https://honorbrook-insurance.com'
TODAY = '2026-11-20'

# (display name, prose name, slug, abbreviation, has county directory, regulator name, regulator url)
LICENSED = [
    ('Virginia', 'Virginia', 'virginia', 'VA', True, None, None),
    ('Maryland', 'Maryland', 'maryland', 'MD', True, None, None),
    ('Washington, DC', 'the District of Columbia', 'washington-dc', 'DC', False,
     'DC Department of Insurance, Securities and Banking', 'https://disb.dc.gov/'),
    ('Delaware', 'Delaware', 'delaware', 'DE', False, 'Delaware Department of Insurance', 'https://insurance.delaware.gov/'),
    ('Pennsylvania', 'Pennsylvania', 'pennsylvania', 'PA', False, 'Pennsylvania Insurance Department', 'https://www.insurance.pa.gov/'),
    ('West Virginia', 'West Virginia', 'west-virginia', 'WV', True, None, None),
    ('Kentucky', 'Kentucky', 'kentucky', 'KY', False, 'Kentucky Department of Insurance', 'https://insurance.ky.gov/'),
    ('Tennessee', 'Tennessee', 'tennessee', 'TN', False, 'Tennessee Department of Commerce and Insurance', 'https://www.tn.gov/commerce/insurance.html'),
    ('North Carolina', 'North Carolina', 'north-carolina', 'NC', True, None, None),
    ('South Carolina', 'South Carolina', 'south-carolina', 'SC', True, None, None),
    ('Florida', 'Florida', 'florida', 'FL', False, 'Florida Department of Financial Services', 'https://www.myfloridacfo.com/'),
    ('Alabama', 'Alabama', 'alabama', 'AL', True, None, None),
    ('Louisiana', 'Louisiana', 'louisiana', 'LA', True, None, None),
    ('Texas', 'Texas', 'texas', 'TX', True, None, None),
    ('Michigan', 'Michigan', 'michigan', 'MI', True, None, None),
    ('Indiana', 'Indiana', 'indiana', 'IN', True, None, None),
]
NOT_LICENSED_WITH_PAGES = ['georgia']          # pages stay live as information only
PROSE = [s[1] for s in LICENSED]
LIST_PROSE = ', '.join(PROSE[:-1]) + ' and ' + PROSE[-1]
LIST_ABBR = ', '.join(s[3] for s in LICENSED[:-1]) + ' and ' + LICENSED[-1][3]
SCHEMA_NAMES = ['District of Columbia' if s[3] == 'DC' else s[0] for s in LICENSED]
SHORT = 'Virginia, Maryland, DC and more than a dozen other states'

NEW_TITLE = 'Honorbrook Insurance | Medicare, Health, Life &amp; Annuities'
NEW_DESC = ('Independent agency comparing Medicare, ACA and group health, life insurance and annuities '
            'from 90+ carriers. Help by phone, text or video. (571) 354-0146.')

GA_NOTICE = ('<div class="callout"><strong>Georgia residents:</strong> Honorbrook is not currently licensed in Georgia. '
             'This page is general information only. We cannot advise on or enroll Georgia residents in a plan until our '
             'Georgia license is active again.</div>')

OLD_LISTS = [
    r"Virginia, Maryland, Georgia, Texas, Michigan, North Carolina, South Carolina, Alabama, Louisiana, Indiana,? (?:and )?West Virginia(?:, and (?:beyond|growing))?",
    r"Virginia, Maryland, North Carolina, South Carolina, Georgia, Alabama, Louisiana, Texas, Michigan, Indiana and West Virginia",
    r"Virginia, Maryland, West Virginia, North Carolina, South Carolina, Georgia, Alabama, Louisiana, Texas, Michigan,? and Indiana",
]

TEXT_RULES = [
    (r"serving Virginia and 10 additional states", "serving Virginia, Maryland, DC and states across the Mid-Atlantic, South and Midwest"),
    (r"Serving Virginia (&amp;|&) 10 more states", r"Serving Virginia, Maryland, DC \1 more"),
    (r"licensed in the 11 states below", "licensed in the states below"),
    (r"11 states (?:—|&mdash;|-) (?=Virginia)", ""),
    (r"11 states, including (?=Virginia)", ""),
    (r"11 states: (?=Virginia)", ""),
    (r" (?:—|&mdash;) 11 states in all (?:—|&mdash;) ", " — "),
    (r"Honorbrook Insurance \| Health, Medicare (&amp;|&) Life in 11 States", NEW_TITLE),
    (r"Licensed across 11 states (—|&mdash;) local help, by phone", r"Licensed across the Mid-Atlantic, South and Midwest \1 local help, by phone"),
    (r"across all 11 licensed states", "across every state where we're licensed"),
    (r"(across|in) all 11 states", r"\1 every state where we're licensed"),
    (r"(licensed|Growing) across 11 states", r"\1 across the Mid-Atlantic, South and Midwest"),
    (r"in the 11 states we serve", "in the states we serve"),
    (r"Each of Our 11 States", "Every State We Serve"),
    (r"and 10 other states", "and more than a dozen other states"),
    (r"✓ Licensed in 11 states", "✓ Licensed in VA, MD, DC &amp; more"),
    (r"Licensed in 11 states, all by phone", "Licensed in VA, MD, DC and more, all by phone"),
    (r"by phone in 11 states", "by phone in every state where we're licensed"),
    (r"([Ll])icensed in 11 states", r"\1icensed in " + SHORT),
]

GA_RULES = [
    (r"licensed in Georgia and (?:10 other states|more than a dozen other states)", "licensed in more than a dozen states, though not currently in Georgia"),
    (r"Independent Medicare and insurance agency licensed in Georgia, serving residents by phone\.", "Independent Medicare and insurance agency. Not currently licensed in Georgia; this page is general information."),
    (r"is an independent agency licensed in Georgia, helping", "is an independent agency that, once its Georgia license is active again, will be helping"),
    (r"independent agency licensed in Georgia, and we help", "independent agency that is not currently licensed in Georgia; once our license is active again we will help"),
    (r"we are licensed in Georgia and help", "once our Georgia license is active again we will help"),
    (r"is an independent agency licensed in Georgia that compares plans and checks", "is an independent agency that is not currently licensed in Georgia. Once our license is active again, we will compare plans and check"),
    (r"We are an independent agency licensed in Georgia\.", "We are an independent agency. We are not currently licensed in Georgia, so this page is general information."),
    (r"Honorbrook Insurance is licensed in Georgia and helps residents of all 159 counties compare", "Honorbrook Insurance is not currently licensed in Georgia. These pages are general information to help residents of all 159 counties understand"),
    (r"Licensed in GA\.", "Information only; not currently licensed in GA."),
    (r"Independent, Georgia-licensed agency helping ([^\"<]*?) residents with", r"Not currently licensed in Georgia. General information for \1 residents on"),
]

NAV_ADDS = [
    ('<a href="/final-expense-life-insurance">Final expense</a>',
     ['<a href="/mortgage-protection-insurance">Mortgage protection</a>',
      '<a href="/veterans-life-insurance">Life insurance for veterans</a>',
      '<a href="/high-net-worth-life-insurance">High-net-worth planning</a>']),
    ('<a href="/self-employed-health-insurance">Self-employed health</a>',
     ['<a href="/private-health-insurance">Private health insurance</a>',
      '<a href="/hsa-health-plans">HSA-eligible plans</a>']),
    ('<a href="/retirement-rollover-annuity">401(k) &amp; IRA rollovers</a>',
     ['<a href="/single-premium-annuities">Single-premium annuities</a>']),
    ('<a href="/final-expense-life-insurance">Final Expense Life</a>',
     ['<a href="/mortgage-protection-insurance">Mortgage Protection</a>',
      '<a href="/veterans-life-insurance">Veterans Life Insurance</a>',
      '<a href="/high-net-worth-life-insurance">High-Net-Worth Life</a>',
      '<a href="/childrens-life-insurance">Children\'s Life Insurance</a>',
      '<a href="/accident-insurance">Accident &amp; AD&amp;D</a>']),
    ('<a href="/self-employed-health-insurance">Self-Employed Health</a>',
     ['<a href="/private-health-insurance">Private Health Insurance</a>',
      '<a href="/hsa-health-plans">HSA-Eligible Plans</a>']),
    ('<a href="/long-term-care-insurance">Long-Term Care</a>',
     ['<a href="/annuities">Annuities</a>',
      '<a href="/single-premium-annuities">Single-Premium Annuities</a>']),
]

DUP_POSTS = {  # old slug -> kept slug
    'does-medicare-cover-dental-vision-and-hearing': 'does-medicare-cover-dental-vision-hearing',
    'medigap-plan-g-vs-plan-n': 'medigap-plan-g-vs-plan-n-2027',
    'why-did-my-medicare-advantage-plan-drop-my-doctor': 'why-did-my-medicare-advantage-plan-drop-my-doctor-or-drug',
}
NEW_URLS = [s[2] + '-medicare-insurance' for s in LICENSED if not s[4]] + [
    'mortgage-protection-insurance', 'veterans-life-insurance', 'high-net-worth-life-insurance',
    'childrens-life-insurance', 'private-health-insurance', 'hsa-health-plans', 'accident-insurance',
    'single-premium-annuities']


def is_ga(rel):
    b = os.path.basename(rel)
    return b.startswith('georgia-') or '-ga-medicare-insurance' in b or b == 'when-can-i-change-my-medicare-plan-in-georgia.html'


def licensed_line():
    return "<strong>Where we're licensed:</strong> " + ' · '.join(
        f'<a href="/{s[2]}-medicare-insurance">{s[0]}</a>' for s in LICENSED)


def fix_lists(t):
    """Rebuild the two kinds of state <ul> used in blog posts and guides."""
    def regulators(ul):
        indent = re.search(r'\n(\s*)<li', ul).group(1)
        have = {k: (n, u) for k, u, n in re.findall(
            r'<a href="/([a-z-]+)-medicare-insurance">[^<]+</a>:</strong> <a href="([^"]+)"[^>]*>([^<]+)</a>', ul)}
        rows = []
        for disp, _, slug, _, _, rn, ru in LICENSED:
            n, u = have.get(slug, (rn, ru))
            rows.append(f'{indent}<li><strong><a href="/{slug}-medicare-insurance">{disp}</a>:</strong> '
                        f'<a href="{u}" rel="noopener" target="_blank">{n}</a></li>')
        close = re.search(r'\n(\s*)</ul>', ul).group(1)
        return '<ul>\n' + '\n'.join(rows) + '\n' + close + '</ul>'

    def hubs(ul):
        indent = re.search(r'\n(\s*)<li', ul).group(1)
        rows = []
        for disp, _, slug, _, counties, _, _ in LICENSED:
            row = f'<a href="/{slug}-medicare-insurance">{disp}</a>'
            if counties:
                row += f' · <a href="/{slug}-counties">county pages</a>'
            rows.append(f'{indent}<li>{row}</li>')
        close = re.search(r'\n(\s*)</ul>', ul).group(1)
        return '<ul>\n' + '\n'.join(rows) + '\n' + close + '</ul>'

    def rebuild(m):
        ul = m.group(0)
        if 'scc.virginia.gov' in ul:
            return regulators(ul)
        if '-counties">county pages</a>' in ul:
            return hubs(ul)
        return ul

    if '/virginia-medicare-insurance' in t:
        t = re.sub(r'<ul>(?:(?!</ul>).)*?/virginia-medicare-insurance(?:(?!</ul>).)*?</ul>', rebuild, t, flags=re.S)
    return t


def fix_jsonld(t, rel):
    changed = [False]

    def walk(o):
        if isinstance(o, dict):
            for k, v in list(o.items()):
                if k in ('areaServed', 'contentLocation') and isinstance(v, list) and len(v) >= 8:
                    names = [x if isinstance(x, str) else x.get('name') for x in v]
                    if names != SCHEMA_NAMES:
                        o[k] = list(SCHEMA_NAMES) if isinstance(v[0], str) else [{"@type": "State", "name": n} for n in SCHEMA_NAMES]
                        changed[0] = True
                elif k == 'knowsAbout' and isinstance(v, list) and rel == 'index.html':
                    extra = ["Term Life Insurance", "Whole Life Insurance", "Indexed Universal Life Insurance",
                             "Mortgage Protection Insurance", "Life Insurance for Veterans",
                             "Fixed and Fixed Indexed Annuities", "Retirement Account Rollovers",
                             "Long-Term Care Insurance", "HSA-Eligible Health Plans", "Accident and AD&D Insurance"]
                    add = [x for x in extra if x not in v]
                    if add:
                        v.extend(add); changed[0] = True
                else:
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    def one(m):
        try:
            j = json.loads(m.group(2))
        except Exception:
            return m.group(0)
        changed[0] = False
        walk(j)
        if not changed[0]:
            return m.group(0)
        return m.group(1) + '\n' + json.dumps(j, indent=2, ensure_ascii=False) + '\n' + m.group(3)

    return re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', one, t, flags=re.S)


def fix_page(t, rel):
    for pat in OLD_LISTS:
        t = re.sub(pat, LIST_PROSE, t)
    for pat, rep in TEXT_RULES:
        t = re.sub(pat, rep, t)
    t = re.sub(r"<strong>Licensed in 11 states:</strong>[^\n]*", lambda m: licensed_line(), t)
    t = re.sub(r"<strong>Licensed in " + re.escape(SHORT) + r":</strong>[^\n]*", lambda m: licensed_line(), t)
    t = fix_lists(t)
    for old, new in DUP_POSTS.items():
        t = re.sub(r'(/blog/%s)(?=["#?])' % re.escape(old), '/blog/' + new, t)
    for anchor, adds in NAV_ADDS:
        if anchor in t and adds[0] not in t:
            def ins(m, adds=adds):
                return m.group(0) + ''.join('\n' + m.group(1) + a for a in adds)
            t = re.sub(r'(?m)^([ \t]*)' + re.escape(anchor), ins, t)
    if is_ga(rel):
        for pat, rep in GA_RULES:
            t = re.sub(pat, rep, t)
        if GA_NOTICE not in t:
            t = re.sub(r'(<div class="wrap prose">)', lambda m: m.group(1) + '\n    ' + GA_NOTICE, t, count=1)
    t = fix_jsonld(t, rel)
    return t


def fix_index(t):
    t = re.sub(r'(<meta name="description" content=")[^"]*"', lambda m: m.group(1) + NEW_DESC + '"', t, count=1)
    t = re.sub(r'(<meta property="og:description" content=")[^"]*"', lambda m: m.group(1) + NEW_DESC + '"', t, count=1)
    tiles = ''.join(f'\n        <a href="/{s[2]}-medicare-insurance">📍 {s[0]}</a>' for s in LICENSED)
    t = re.sub(r'(<div class="area-grid">).*?(\n\s*<a href="/#contact">＋ Your area\?</a>)',
               lambda m: m.group(1) + tiles + m.group(2), t, count=1, flags=re.S)
    return t


def fix_find_js(t):
    for ab, nm in (('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('KY', 'Kentucky'),
                   ('PA', 'Pennsylvania'), ('TN', 'Tennessee')):
        t = t.replace("%s:'%s'," % (ab, nm), '')
    if 'var NEWST' not in t:
        newst = ("\n  /* licensed, hub page live, county pages not built yet: [name, hub slug, other names] */\n"
                 "  var NEWST = {DE:['Delaware','delaware'],DC:['Washington, DC','washington-dc','district of columbia','washington dc','washington d c'],"
                 "FL:['Florida','florida'],KY:['Kentucky','kentucky'],PA:['Pennsylvania','pennsylvania'],TN:['Tennessee','tennessee']};\n"
                 "  function newState(q) {\n"
                 "    var n = norm(q).replace(/,/g, ''), up = q.trim().toUpperCase();\n"
                 "    if (NEWST[up]) return NEWST[up];\n"
                 "    for (var k in NEWST) { for (var i = 0; i < NEWST[k].length; i++) { if (i !== 1 && norm(NEWST[k][i]).replace(/,/g, '') === n) return NEWST[k]; } }\n"
                 "    return null;\n  }\n"
                 "  var GA_NOTE = '<p class=\"fd-no\">Honorbrook is not currently licensed in Georgia. Our Georgia pages are general information only until that license is active again.</p>';\n")
        t = t.replace("\n  function load() {", newst + "\n  function load() {", 1)
        t = t.replace("    var os = otherState(q);",
                      "    var ns = newState(q);\n"
                      "    if (ns) return { html: cta + '<ul class=\"fd-list\"><li><a href=\"/' + ns[1] + '-medicare-insurance\"><strong>' + esc(ns[0]) + '</strong> Medicare and insurance help</a></li></ul><p class=\"fd-hint\">County pages for ' + esc(ns[0]) + ' are on the way. We can help you now by phone, text or video.</p>', type: 'state' };\n"
                      "    var os = otherState(q);", 1)
        t = t.replace("return { html: cta + '<ul class=\"fd-list\"><li>ZIP ' + esc(q)",
                      "return { html: (c[1] === 'GA' ? GA_NOTE : cta) + '<ul class=\"fd-list\"><li>ZIP ' + esc(q)", 1)
        t = t.replace("      var u = '/' + st[2];\n      return { html: cta + ",
                      "      var u = '/' + st[2];\n      return { html: (st[1] === 'GA' ? GA_NOTE : cta) + ", 1)
    t = re.sub(r"We did not find ZIP ' \+ esc\(q\) \+ ' in the (?:11 )?states we serve\. If you are moving to one of them, search by county or state, or",
               "We do not have a local page for ZIP ' + esc(q) + ' yet. We are licensed in " + LIST_ABBR + ". If you live in one of them,", t)
    t = re.sub(r"We serve Virginia, Maryland, North Carolina, South Carolina, Georgia, Alabama, Louisiana, Texas, Michigan, Indiana and West Virginia\.",
               "We serve " + LIST_PROSE + ".", t)
    t = re.sub(r"We serve 11 states: VA, MD, NC, SC, GA, AL, LA, TX, MI, IN and WV\.", "We serve " + LIST_ABBR + ".", t)
    t = t.replace("These matches are in the 11 states we serve:", "These matches are in states we serve:")
    return t


def fix_llms(t):
    t = re.sub(r"licensed in (?:11 states: )?Virginia, Maryland, North Carolina[^.]*?West Virginia\.", "licensed in " + LIST_PROSE + ".", t)
    t = re.sub(r"## State pages\n(?:- .*\n)+", "## State pages\n" + ''.join(
        f"- [{s[0]}]({BASE}/{s[2]}-medicare-insurance)\n" for s in LICENSED), t)
    adds = [
        ("- [Self-employed health insurance]", [
            f"- [Private health insurance under 65]({BASE}/private-health-insurance): Marketplace, off-exchange, short-term and employer-funded options compared",
            f"- [HSA-eligible health plans]({BASE}/hsa-health-plans): which plans work with a health savings account, including bronze and catastrophic plans since 2026"]),
        ("- [Final expense]", [
            f"- [Mortgage protection insurance]({BASE}/mortgage-protection-insurance): term life sized to a home loan, paid to the family",
            f"- [Life insurance for veterans]({BASE}/veterans-life-insurance): VGLI and VALife compared with private coverage",
            f"- [High-net-worth life insurance planning]({BASE}/high-net-worth-life-insurance): estate liquidity, business succession, IUL trade-offs",
            f"- [Children's life insurance]({BASE}/childrens-life-insurance): standalone policies vs. child riders"]),
        ("- [Annuities (fixed and fixed indexed)]", [
            f"- [Single-premium annuities]({BASE}/single-premium-annuities): MYGA and SPIA explained, with surrender and tax rules"]),
        ("- [Cancer and critical illness]", [
            f"- [Accident and AD&D insurance]({BASE}/accident-insurance): cash benefits after a covered injury"]),
    ]
    for anchor, lines in adds:
        if lines[0] not in t:
            t = re.sub(r"(?m)^(%s.*)$" % re.escape(anchor), lambda m: m.group(1) + '\n' + '\n'.join(lines), t, count=1)
    return t


def fix_sitemap(t):
    for old in DUP_POSTS:
        t = re.sub(r"\s*<url>\s*<loc>%s/blog/%s</loc>.*?</url>" % (re.escape(BASE), re.escape(old)), '', t, flags=re.S)
    add = ''
    for u in NEW_URLS:
        if f'<loc>{BASE}/{u}</loc>' not in t:
            add += (f"  <url>\n    <loc>{BASE}/{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
                    f"    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n")
    return t.replace('</urlset>', add + '</urlset>') if add else t


def main():
    n = 0
    for f in sorted(glob.glob(SITE + '/**/*.html', recursive=True)):
        rel = os.path.relpath(f, SITE)
        if rel.startswith('blog/') and os.path.basename(f)[:-5] in DUP_POSTS:
            os.remove(f); print('removed duplicate post', rel); continue
        t = open(f, encoding='utf-8').read()
        new = fix_page(t, rel)
        if rel == 'index.html':
            new = fix_index(new)
        if new != t:
            open(f, 'w', encoding='utf-8').write(new); n += 1
    print('html files updated:', n)

    def rewrite(path, fn):
        t = open(path, encoding='utf-8').read(); new = fn(t)
        if new != t:
            open(path, 'w', encoding='utf-8').write(new); print('updated', os.path.relpath(path, ROOT))

    rewrite(os.path.join(SITE, 'assets', 'find.js'), fix_find_js)
    rewrite(os.path.join(SITE, 'llms.txt'), fix_llms)
    rewrite(os.path.join(SITE, 'sitemap.xml'), fix_sitemap)
    rewrite(os.path.join(ROOT, 'netlify', 'functions', 'chat.js'), lambda t: re.sub(
        r"Licensed in \d+ states: Virginia, Maryland, Georgia[^.]*\.",
        "Licensed in: " + LIST_PROSE + ". Not currently licensed in Georgia or any state not listed.", t))

    def redirects(t):
        for old, new in DUP_POSTS.items():
            line = f'/blog/{old} /blog/{new} 301'
            if line not in t:
                t = t.replace('/favicon.ico', line + '\n/favicon.ico', 1) if '/favicon.ico' in t else t.rstrip('\n') + '\n' + line + '\n'
        return t
    rewrite(os.path.join(SITE, '_redirects'), redirects)

    def toml(t):
        for old, new in DUP_POSTS.items():
            if f'from = "/blog/{old}"' not in t:
                t = t.rstrip('\n') + f'\n\n[[redirects]]\n  from = "/blog/{old}"\n  to = "/blog/{new}"\n  status = 301\n'
        return t
    rewrite(os.path.join(ROOT, 'netlify.toml'), toml)

    # keep the generators from writing the old wording back
    for f in sorted(glob.glob(os.path.join(ROOT, 'scripts', '*.py'))):
        if os.path.basename(f) == 'states_refresh.py':
            continue
        def gen(t):
            for pat, rep in TEXT_RULES:
                t = re.sub(pat, rep, t)
            return t
        rewrite(f, gen)


if __name__ == '__main__':
    main()
