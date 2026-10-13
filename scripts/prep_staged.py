#!/usr/bin/env python3
"""Compliance + GEO pass over staging/blog/*.html before publish_staged.py. Idempotent."""
import re, json, glob, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import county_gen as g
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/'
cen, pen, hosp = g.load(); agg = g.build_agg(cen, pen)
ST = g.STATES

def end_of_prose(h):
    m = re.search(r'\s*</div>\s*</article>', h); assert m
    return m.start()

def ship_block():
    lis = '\n'.join(f'      <li><a href="/{v["slug"]}-medicare-insurance">{k}</a> · <a href="/{v["slug"]}-counties">County pages</a></li>' for k, v in ST.items())
    return f'''
    <h2>Medicare help in your state</h2>
    <p>Honorbrook is licensed in all 11 states below. Plan availability, costs and some rules vary by state and county, so call us at <a href="tel:+15713540146">(571) 354-0146</a> or fill out <a href="/#contact">our short form</a> for what applies where you live.</p>
    <ul>
{lis}
    </ul>
'''

def life_state_block():
    lis = '\n'.join(f'      <li><strong><a href="/{v["slug"]}-medicare-insurance">{k}</a>:</strong> <a href="{g.DOI[k][1]}" rel="noopener" target="_blank">{g.esc(g.DOI[k][0])}</a></li>' for k, v in ST.items())
    return f'''
    <h2>Availability and rules vary by state</h2>
    <p>Life insurance and annuity products, rates, riders and consumer protections differ by state, and a given product may not be available in every state. Honorbrook is licensed in the 11 states below; which products we can offer you depends on what carriers sell in your state. Each state&rsquo;s insurance regulator can verify an agent&rsquo;s license and answer consumer questions.</p>
    <ul>
{lis}
    </ul>
'''

NOTES = {
 'annuity': "This article is general education, not tax, legal, investment or insurance advice. A fixed indexed annuity is an insurance contract, not a direct market investment. Credited interest depends on the insurer&rsquo;s caps, participation rates and spreads, which can change; surrender charges, fees and tax rules may apply, and guarantees depend on the issuing insurer&rsquo;s claims-paying ability. Whether any product is suitable depends on your age, goals, other assets and time horizon. Talk with a licensed agent and a qualified tax professional before acting.",
 'cashvalue': "This article is general education, not tax, legal, investment or insurance advice. Indexed and cash value life insurance is not a direct market investment. Credited interest depends on the insurer&rsquo;s caps, participation rates and spreads, which can change; policy charges, fees and surrender charges apply, loans and withdrawals can reduce the death benefit and may be taxable, and guarantees depend on the issuing insurer&rsquo;s claims-paying ability. Suitability depends on your situation; consult a qualified tax professional before acting.",
 'kids': "This article is general education, not tax, legal, investment or insurance advice. We do not suggest that life insurance is better or worse than a 529 plan or other savings; each has different purposes, costs and tax treatment. Cash value grows slowly in the early years, fees and surrender charges may apply, and guarantees depend on the issuing insurer&rsquo;s claims-paying ability. Suitability depends on your family&rsquo;s situation.",
 'general': "This article is general education, not tax, legal or insurance advice. Policy availability, pricing, waiting periods and benefits vary by insurer, age, health and state, and guarantees depend on the issuing insurer&rsquo;s claims-paying ability. A licensed agent can explain what applies to you.",
}
def note_kind(slug):
    if 'fixed-indexed' in slug: return 'annuity'
    if any(x in slug for x in ('iul', 'cash-value', 'policy-loan', 'high-income')): return 'cashvalue'
    if any(x in slug for x in ('kids', '529', 'gerber', 'guaranteed-insurability', 'protect-kids')): return 'kids'
    return 'general'

def state_table(sname):
    ag = agg[sname]; st = ST[sname]
    slug = json.load(open(R + 'scripts/county_data/slugmap.json'))
    rows = []
    for k in ag['order'][:10]:
        c, p = cen[k], pen.get(k)
        ma = g.pct(p['enr'], p['elig']) if p else 'n/a'
        rows.append(f'          <tr><td><a href="/{slug[k]}">{g.esc(g.display(c))}</a></td><td>{c["p65"]:,}</td><td>{ma}</td></tr>')
    unit = 'Parish' if st['unit'] == 'parishes' else 'County'
    return f'''
    <h2>Medicare Advantage by {unit.lower()} in {sname}</h2>
    <p>Medicare plan choices are set {unit.lower()} by {unit.lower()}. Statewide, about {ag['ma']:.1f}% of people with Medicare in {sname} are enrolled in a Medicare Advantage plan (CMS, September 2026). Here are the 10 largest {st['unit']} by residents age 65 and older:</p>
    <div class="table-wrap">
      <table class="compare">
        <thead>
          <tr><th>{unit}</th><th>Residents 65+</th><th>Medicare Advantage share</th></tr>
        </thead>
        <tbody>
{chr(10).join(rows)}
        </tbody>
      </table>
    </div>
    <p>Free help in {sname}: <strong>{g.esc(st['ship'])}</strong> offers free Medicare counseling at <a href="tel:+1{st['tel'].replace('-', '')[1:]}">{st['tel']}</a>. See every {unit.lower()} on our <a href="/{st['slug']}-counties">{sname} {unit.lower()} directory</a> or our <a href="/{st['slug']}-medicare-insurance">{sname} Medicare hub</a>. Sources: U.S. Census Bureau 2023 estimates; CMS Medicare Advantage State/County Penetration.</p>
'''

ct = [{"@type": "State", "name": k} for k in ST]
done = 0
for f in sorted(glob.glob(R + 'staging/blog/*.html')):
    slug = os.path.basename(f)[:-5]
    h = open(f).read(); o = h
    for a, b in (('Get my free plan review', 'Get my plan review'), ('free plan review', 'plan review'), ('Free plan review', 'Plan review'), ('free plan comparison', 'plan comparison')):
        h = h.replace(a, b)
    medicare = 'do not offer every plan available in your area' in h
    state_post = re.search(r'when-can-i-change-my-medicare-plan-in-(.+)$', slug)
    add = ''
    if 'Medicare help in your state' not in h and 'Availability and rules vary by state' not in h and 'Medicare Advantage by ' not in h:
        if state_post:
            sname = {v['slug']: k for k, v in ST.items()}[state_post.group(1)]
            add += state_table(sname)
        elif medicare:
            add += ship_block()
        else:
            add += life_state_block()
            k = note_kind(slug)
            n = NOTES[k]
            if 'gerber' in slug:
                n += ' Gerber is a trademark of its owner; this article is not affiliated with or sponsored by Gerber Life Insurance Company.'
            add += f'\n    <p style="font-size:15.5px;color:var(--muted)"><em>{n}</em></p>\n'
    if add:
        i = end_of_prose(h); h = h[:i] + '\n' + add.rstrip('\n') + h[i:]
    def fix(m):
        try: j = json.loads(m.group(1))
        except Exception: return m.group(0)
        if j.get('@type') == 'BlogPosting':
            j['contentLocation'] = ct
            return '<script type="application/ld+json">\n' + json.dumps(j, ensure_ascii=False) + '\n</script>'
        return m.group(0)
    h = re.sub(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', fix, h, flags=re.S)
    if h != o:
        open(f, 'w').write(h); done += 1
print('prepared', done)
