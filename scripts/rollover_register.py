#!/usr/bin/env python3
"""Registers the pages made by rollover_gen.py: blog index cards, sitemap, llms.txt, and links from the existing annuity pages.
Idempotent: every step skips what is already there. Touches only the lines it adds (plus one "Related reading" sentence on the
older annuity-rollover post and one card on /annuities)."""
import os, re, sys, html
sys.path.insert(0, os.path.dirname(__file__))
import rollover_gen as G

ROOT, SITE = G.ROOT, G.SITE
posts = [p for p in G.pages if not p.get('pillar')]
pillar = [p for p in G.pages if p.get('pillar')][0]


def rw(path, fn):
    s = open(path, encoding='utf-8').read()
    n = fn(s)
    if n != s:
        open(path, 'w', encoding='utf-8').write(n)
        print('updated', os.path.relpath(path, ROOT))
    else:
        print('unchanged', os.path.relpath(path, ROOT))


def blog_index(s):
    cards = ''
    for p in posts:
        if 'href="%s"' % p['path'] in s:
            continue
        cards += ('      <a class="rel-card" href="%s">\n        <h3>%s</h3>\n        <p class="sans" style="font-size:13px;color:var(--gold-d);text-transform:uppercase;'
                  'letter-spacing:1.5px;margin-bottom:6px">October 2026</p>\n        <p>%s</p>\n      </a>\n' % (p['path'], G.plain(p['h1']), html.escape(p['desc'], quote=False)))
    return s.replace('<!-- POSTS:START -->\n', '<!-- POSTS:START -->\n' + cards, 1) if cards else s


def sitemap(s):
    add = ''
    for p, pri in [(pillar, '0.8')] + [(q, '0.7') for q in posts]:
        loc = G.BASE + p['path']
        if '<loc>%s</loc>' % loc not in s:
            add += '  <url>\n    <loc>%s</loc>\n    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>\n' % (loc, pri)
    return s.replace('</urlset>', add + '</urlset>') if add else s


def llms(s):
    line = '- [Retirement rollover to an annuity: every account type](%s%s): which accounts can be rolled over, with the IRS rule and the trap for each\n' % (G.BASE, pillar['path'])
    if pillar['path'] in s:
        return s
    anchor = '- [Annuities (fixed and fixed indexed)](https://honorbrook-insurance.com/annuities)\n'
    return s.replace(anchor, anchor + line, 1)


def old_post(s):
    if pillar['path'] in s:
        return s
    old = 'and how a <a href="/blog/what-is-a-fixed-indexed-annuity-fia">fixed indexed annuity</a> works.</p>'
    new = 'and how a <a href="/blog/what-is-a-fixed-indexed-annuity-fia">fixed indexed annuity</a> works. For each account type, see <a href="%s">every rollover account and its traps</a>.</p>' % pillar['path']
    return s.replace(old, new, 1)


def annuities(s):
    if pillar['path'] in s:
        return s
    old = "We'll tell you honestly which side of that ledger matters most for your situation.</p>"
    new = old[:-4] + ' If the money would come from a retirement account, see <a href="%s">which accounts can be rolled into an annuity, and the trap for each</a>.</p>' % pillar['path']
    return s.replace(old, new, 1)


rw(os.path.join(SITE, 'blog', 'index.html'), blog_index)
rw(os.path.join(SITE, 'sitemap.xml'), sitemap)
rw(os.path.join(SITE, 'llms.txt'), llms)
rw(os.path.join(SITE, 'blog', 'ira-rollover-into-an-annuity-what-to-ask-first.html'), old_post)
rw(os.path.join(SITE, 'annuities.html'), annuities)
