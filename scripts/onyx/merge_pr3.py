"""Honorbrook Onyx: fold the useful parts of pull request #3 into the new site.

Pull request #3 (branch on GitHub, not merged) was made by another session on Nov 20, 2026. It was read through
raw.githubusercontent.com on Nov 21. What is taken, and why:
- Seven new product pages (veterans, high net worth, children's life, private health under 65, HSA plans, accident and AD&D,
  single-premium annuities), kept as written except two fixes: the guaranty-association sentence is removed from the annuity page
  (most states bar agents from using the association to sell, e.g. Virginia Code 38.2-1715), and the HSA sentence gets the
  condition IRS Notice 2026-5 Q&A-6 sets for plans bought off the Marketplace. Their VA and IRS figures were checked against
  va.gov (Oct 13 and Nov 19, 2026) and IRS Notice 2026-5.
- Its quote form, on the seven life and annuity product pages (the new pages already carry it).
- Its merge of three duplicate posts into the stronger one, with permanent redirects.
What is not taken: its Georgia "not licensed" wording (the owner said on Nov 21 "include georgia"), its state-count wording (the
owner wants the count shown), its Florida page (built here instead from verified facts, see footprint.py) and its copies of the
five state pages and the mortgage protection page that this build already has.
The page body comes from the pull request; the header and footer come from the current site so every page shares them.
"""
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRA = os.path.join(HERE, 'extra')
PAGES = ['veterans-life-insurance', 'high-net-worth-life-insurance', 'childrens-life-insurance', 'private-health-insurance',
         'hsa-health-plans', 'accident-insurance', 'single-premium-annuities']
QUOTE_ON = ['final-expense-life-insurance', 'life-insurance', 'term-life-insurance', 'whole-life-insurance', 'indexed-universal-life',
            'guaranteed-universal-life', 'annuities']
# (old post, the stronger post it is merged into)
DUPES = [('does-medicare-cover-dental-vision-and-hearing', 'does-medicare-cover-dental-vision-hearing'),
         ('medigap-plan-g-vs-plan-n', 'medigap-plan-g-vs-plan-n-2027'),
         ('why-did-my-medicare-advantage-plan-drop-my-doctor', 'why-did-my-medicare-advantage-plan-drop-my-doctor-or-drug')]
# menu entries for the new pages: (after this link in the dropdown, insert these)
NAV = [('<a href="/self-employed-health-insurance">Self-employed health</a>',
        ' <a href="/private-health-insurance">Private health under 65</a> <a href="/hsa-health-plans">HSA-eligible plans</a>'
        ' <a href="/accident-insurance">Accident &amp; AD&amp;D</a>'),
       ('<a href="/final-expense-life-insurance">Final expense</a>',
        ' <a href="/childrens-life-insurance">Children&rsquo;s life</a> <a href="/veterans-life-insurance">Life insurance for veterans</a>'
        ' <a href="/high-net-worth-life-insurance">High-net-worth planning</a>'),
       ('<a href="/retirement-rollover-annuity">401(k) &amp; IRA rollovers</a>',
        ' <a href="/single-premium-annuities">Single-premium annuities</a>')]
LLMS = [('Life insurance for veterans', 'veterans-life-insurance'), ('High-net-worth life insurance planning', 'high-net-worth-life-insurance'),
        ("Children's life insurance", 'childrens-life-insurance'), ('Private health insurance under 65', 'private-health-insurance'),
        ('HSA-eligible health plans', 'hsa-health-plans'), ('Accident and AD&D insurance', 'accident-insurance'),
        ('Single-premium annuities (MYGA, SPIA)', 'single-premium-annuities')]
DATE = '2026-11-21'


def _fix(slug, s):
    if slug == 'single-premium-annuities':
        s = re.sub(r',\s*with (?:a further layer of protection from your |)state guaranty association[^.<"]*', '', s)
        assert 'guaranty' not in s.lower(), 'guaranty wording left on ' + slug
    if slug == 'hsa-health-plans':
        a = 'whether bought through the Marketplace or directly from a carrier.'
        assert a in s, slug
        s = s.replace(a, 'whether bought through the Marketplace or directly from a carrier, as long as the same plan is offered on the Marketplace.')
    return s


def _area_served(names):
    return '"areaServed": ' + json.dumps([{"@type": "AdministrativeArea" if n == 'District of Columbia' else "State", "name": n} for n in names])


def add_pages(out, site, names):
    """Write the seven pages into the build: head and body from the pull request, header and footer from the current site."""
    shell = open(os.path.join(site, 'disability-insurance.html'), encoding='utf-8').read()
    top = shell[shell.index('</head>'):shell.index('<section class="page-hero"')]
    bottom = shell[shell.index('<footer'):]
    for slug in PAGES:
        p = open(os.path.join(EXTRA, slug + '.html'), encoding='utf-8').read()
        head = re.sub(r'"areaServed":\s*\[[^\]]*\]', _area_served(names), p[:p.index('</head>')])
        main = p[p.index('<section class="page-hero"'):p.index('<footer')]
        open(os.path.join(out, slug + '.html'), 'w', encoding='utf-8').write(_fix(slug, head + top + main + bottom))
    return len(PAGES)


def page_pass(slug, s):
    """Per page, inside the build's page pass: menu links, and the quote form on the life and annuity product pages."""
    i = s.find('<nav class="menu'); j = s.find('</nav>', i)
    if i >= 0 and j > i and '/hsa-health-plans"' not in s[i:j]:
        nav = s[i:j]
        for a, b in NAV:
            nav = nav.replace(a, a + b, 1)
        s = s[:i] + nav + s[j:]
    if slug in QUOTE_ON and 'class="hb-quote' not in s and '<section class="faq">' in s:
        blk = open(os.path.join(EXTRA, 'quote', slug + '.html'), encoding='utf-8').read()
        blk = blk.replace('No exam on most plans. ', 'Many plans ask health questions instead of an exam. ')
        s = s.replace('<section class="faq">', blk.strip() + '\n\n<section class="faq">', 1)
    return s


def finish(out, root):
    """After the page pass: merge the duplicate posts, list the new pages in the sitemap and llms.txt."""
    for old, new in DUPES:
        p = os.path.join(out, 'blog', old + '.html')
        if os.path.exists(p): os.remove(p)
    n = 0
    for f in glob.glob(os.path.join(out, '**', '*.html'), recursive=True):
        if '/assets/video' in f: continue
        s = open(f, encoding='utf-8', errors='ignore').read(); o = s
        for old, new in DUPES:
            s = re.sub(r'\s*<a class="rel-card" href="/blog/%s">.*?</a>' % re.escape(old), '', s, flags=re.S) if '/blog/%s"' % new in s else s
            s = s.replace('href="/blog/%s"' % old, 'href="/blog/%s"' % new).replace('honorbrook-insurance.com/blog/%s"' % old, 'honorbrook-insurance.com/blog/%s"' % new)
        seen = set()
        def dedupe(m):
            k = m.group(1)
            if k in seen: return ''
            seen.add(k); return m.group(0)
        s = re.sub(r'\s*<a class="rel-card" href="([^"]+)">.*?</a>', dedupe, s, flags=re.S)
        if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
    sm = os.path.join(out, 'sitemap.xml'); s = open(sm, encoding='utf-8').read()
    for old, new in DUPES:
        s = re.sub(r'\s*<url>\s*<loc>https://honorbrook-insurance\.com/blog/%s</loc>.*?</url>' % re.escape(old), '', s, flags=re.S)
    add = ''.join('  <url><loc>https://honorbrook-insurance.com/%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n' % (p, DATE)
                  for p in PAGES if '/%s</loc>' % p not in s)
    open(sm, 'w', encoding='utf-8').write(s.replace('</urlset>', add + '</urlset>'))
    lp = os.path.join(out, 'llms.txt')
    if os.path.exists(lp):
        s = open(lp, encoding='utf-8').read()
        for old, new in DUPES:
            s = '\n'.join(l for l in s.split('\n') if '/blog/%s)' % old not in l)
        if '/hsa-health-plans)' not in s:
            s = s.rstrip('\n') + '\n\n## More coverage\n' + ''.join('- [%s](https://honorbrook-insurance.com/%s)\n' % (t, p) for t, p in LLMS)
        open(lp, 'w', encoding='utf-8').write(s)
    rp = os.path.join(out, '_redirects')
    if os.path.exists(rp):
        s = open(rp, encoding='utf-8').read()
        add = ''.join('/blog/%s /blog/%s 301!\n' % d for d in DUPES if '/blog/%s ' % d[0] not in s)
        open(rp, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n' + add)
    toml = os.path.join(root, 'netlify.toml'); s = open(toml, encoding='utf-8').read()
    add = ''.join('\n[[redirects]]\n  from = "/blog/%s"\n  to = "/blog/%s"\n  status = 301\n  force = true\n' % d for d in DUPES if 'from = "/blog/%s"' % d[0] not in s)
    if add: open(toml, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n' + add)
    return n
