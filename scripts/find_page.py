#!/usr/bin/env python3
"""Build site/find-your-area.html and add it to sitemap.xml. Run from repo root after county_gen.py."""
import json, os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
import county_gen as g
ROOT = g.ROOT; S = ROOT + '/site/'
cen = json.load(open(ROOT + '/scripts/county_data/county_stats.json'))['census']
n_by = {sn: sum(1 for v in cen.values() if v['state'] == sn) for sn in g.STATES}
header, foot = g.shell()
rows = '\n'.join(
    f'          <tr><td><strong>{sn}</strong></td><td><a href="/{st["slug"]}-medicare-insurance">Medicare</a></td><td><a href="/{st["slug"]}-aca-health-insurance">ACA health</a></td><td><a href="/{st["slug"]}-counties">All {n_by[sn]} {"parishes" if st["unit"] == "parishes" else "counties"}</a></td></tr>'
    for sn, st in g.STATES.items())
qas = [("Which states do you serve?", "We are licensed in Virginia, Maryland, North Carolina, South Carolina, Georgia, Alabama, Louisiana, Texas, Michigan, Indiana and West Virginia, and we help clients by phone or video call."),
       ("Do I need to live near your office?", "No. Our office is in Tysons, Virginia, but we help people in all 11 states by phone or video, and our help is free to you."),
       ("What if my state is not on the list?", "We cannot help with plans in states where we are not licensed. Call (571) 354-0146 if you are moving to one of our states or have a family member there.")]
ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": g.BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Find your area", "item": g.BASE + "/find-your-area"}]},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]}]
body = f'''<section class="page-hero" id="maincontent" role="main">
  <div class="wrap">
    <div class="breadcrumb"><a href="/">Home</a> &rsaquo; Find your area</div>
    <h1>Find help in <em>your area</em></h1>
    <p class="lead">Type your ZIP code, city, county or state to see whether Honorbrook can help, and go straight to local Medicare, ACA and coverage information for your area.</p>
  </div>
</section>

<article class="article">
  <div class="wrap prose">
    <div id="findInline"></div>
    <noscript><p>Search needs JavaScript. You can still browse by state below, or call <a href="tel:+15713540146">(571) 354-0146</a>.</p></noscript>

    <h2>Browse by state</h2>
    <p>Honorbrook is licensed in 11 states. Pick your state for Medicare help, ACA health insurance and a list of every {sum(n_by.values()):,} county and parish we cover.</p>
    <div class="table-wrap">
      <table class="compare">
        <thead>
          <tr><th>State</th><th>Medicare</th><th>ACA health</th><th>Local pages</th></tr>
        </thead>
        <tbody>
{rows}
        </tbody>
      </table>
    </div>
    <div class="cta-strip">
      <h3>Not sure where to start?</h3>
      <p class="sans">Call or request a callback and we will find the right plan for your area. Free to you, no pressure.</p>
      <a class="btn-primary sans" href="/#contact">Request a callback</a>
    </div>
  </div>
</article>

<section class="faq">
  <div class="wrap" style="max-width:880px">
    <div class="kicker">Common questions</div>
    <h2 class="section-title" style="font-size:30px;margin-bottom:24px">Where we help</h2>
{g.faq_html(qas)}
  </div>
</section>

'''
title = "Find Help in Your Area: ZIP, City, County or State | Honorbrook"
desc = "Search by ZIP code, city, county or state to see whether Honorbrook can help, and find local Medicare and ACA health insurance information. Licensed in 11 states."
page = g.head(title, desc, g.BASE + "/find-your-area", "Search by ZIP, city, county or state to find help from Honorbrook Insurance.", ld) + header + body + foot
open(S + 'find-your-area.html', 'w').write(page)
sm = open(S + 'sitemap.xml').read()
if '/find-your-area<' not in sm:
    sm = sm.replace('</urlset>', f'  <url>\n    <loc>{g.BASE}/find-your-area</loc>\n    <lastmod>2026-10-13</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n</urlset>')
    open(S + 'sitemap.xml', 'w').write(sm)
print('find-your-area built')
