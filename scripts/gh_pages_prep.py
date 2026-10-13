#!/usr/bin/env python3
"""GitHub Pages cannot do server-side redirects, so write small redirect pages for the old URLs listed in site/_redirects,
plus a 404 page and favicon.ico. Idempotent. Run from repo root: python3 scripts/gh_pages_prep.py"""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(__file__))
import county_gen as g
S = g.ROOT + '/site/'
STUB = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Redirecting | Honorbrook Insurance</title>
<meta name="robots" content="noindex, follow"><link rel="canonical" href="{abs}">
<meta http-equiv="refresh" content="0; url={to}"></head>
<body><p>This page has moved. <a href="{to}">Continue to the new page</a>.</p>
<script>location.replace("{to}");</script></body></html>
'''
n = 0
for line in open(S + '_redirects'):
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    parts = line.split()
    frm, to = parts[0], parts[1]
    if '*' in frm or to.startswith('http') or parts[-1] != '301':
        continue
    path = S + frm.lstrip('/')
    if not path.endswith('.html'):
        path += '.html'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and 'Redirecting | Honorbrook' not in open(path).read():
        print('SKIP (real page exists):', frm); continue
    open(path, 'w').write(STUB.format(abs=g.BASE + to, to=to)); n += 1
# catch-all for the old /services/ section
os.makedirs(S + 'services', exist_ok=True)
open(S + 'services/index.html', 'w').write(STUB.format(abs=g.BASE + '/', to='/'))
# favicon.ico
if not os.path.exists(S + 'favicon.ico'):
    shutil.copy(S + 'favicon-64.png', S + 'favicon.ico')
# 404 page
header, foot = g.shell()
body = '''<section class="page-hero" id="maincontent" role="main">
  <div class="wrap">
    <h1>We could not find that <em>page</em></h1>
    <p class="lead">The page may have moved. Try searching for your area, or head to one of our main pages.</p>
    <div class="hero-ctas sans">
      <button type="button" class="btn-primary" data-find style="cursor:pointer">Find your area</button>
      <a class="btn-ghost" href="/">Go to the homepage</a>
      <a class="btn-ghost" href="tel:+15713540146">Call (571) 354-0146</a>
    </div>
  </div>
</section>

'''
page = g.head('Page Not Found | Honorbrook Insurance', 'The page you were looking for could not be found. Search for your area or call Honorbrook Insurance at (571) 354-0146.', g.BASE + '/404', 'Page not found.', [], index=False) + header + body + foot
open(S + '404.html', 'w').write(page)
print('redirect pages', n, '| 404 + favicon.ico + services/index.html written')
