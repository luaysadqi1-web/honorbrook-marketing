#!/usr/bin/env python3
"""Bring the 44 hand-built pilot county pages to the current template without losing their hand-researched facts.
Replaces only the repeated sections (numbers, resources, coverage, guides, similar counties, callout, CTA) and adds the
profile and communities blocks. Idempotent. Run from repo root: python3 scripts/upgrade_pilot.py"""
import re, sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import county_gen as g

ROOT = g.ROOT
cen, pen, hosp = g.load(); agg = g.build_agg(cen, pen)
gv, rucc, idx = g.load_extra()
if idx is None:
    idx = set()
    for sn in g.STATES: idx.update(agg[sn]['order'][:14])
g.EXTRA.update(gv=gv, rucc=rucc, pen=pen, index=idx, sg={sn: g.state_gv([k for k, v in cen.items() if v['state'] == sn], gv) for sn in g.STATES})
slugmap = json.load(open(ROOT + '/scripts/county_data/slugmap.json'))
pilot = json.load(open(ROOT + '/scripts/county-pilot.json'))
pf = [x['fips'] for v in pilot.values() for x in v]
done = 0
for k in pf:
    c = cen[k]; st = g.STATES[c['state']]; ag = agg[c['state']]; sname = c['state']; D = g.display(c)
    f = f"{ROOT}/site/{slugmap[k]}.html"; h = open(f).read(); o = h
    rank = ag['order'].index(k) + 1
    nums = (f"    <h2>{g.V(k, 'nh', ['Medicare in ' + g.esc(D) + ' by the numbers', g.esc(D) + ' Medicare at a glance', 'The numbers behind Medicare in ' + g.esc(D)])}</h2>\n"
            f"{g.stats_table(c, pen.get(k), ag, sname)}    <p>{g.interp(c, pen.get(k), ag, sname, rank, len(ag['order']), st['unit'], k)}</p>\n"
            f"{g.profile_block(c, k, sname, g.EXTRA['sg'][sname])}{g.local_block(k, D, sname)}")
    h = re.sub(r'[ \t]*<h2>(?:Medicare in [^<]* by the numbers|[^<]* Medicare at a glance|The numbers behind Medicare in [^<]*)</h2>.*?(?=[ \t]*<h2>Free help available in)', lambda m: nums, h, flags=re.S)
    h = re.sub(r'[ \t]*<h2>(?:Medicare resources from official sources|Official Medicare resources)</h2>.*?</ul>\n', lambda m: g.external_block(sname, D, k), h, flags=re.S)
    h = re.sub(r'[ \t]*<h2>Coverage we offer [^<]*</h2>\s*(?:<ul>.*?</ul>|<p>.*?</p>)\n', lambda m: f"    <h2>Coverage we offer {g.esc(D)} residents</h2>\n    <p>{g.coverage_sentence(k, D)}</p>\n", h, flags=re.S)
    h = re.sub(r'[ \t]*<h2>(?:Medicare guides for [^<]*|Read next|Plain-English Medicare answers)</h2>.*?</ul>\n', lambda m: g.guides_block(c, k), h, flags=re.S)
    h = re.sub(r'[ \t]*<h2>Other [^<]* we serve</h2>.*?</p>\n', lambda m: g.similar_table(c, k, ag, cen, pen, slugmap, st, sname), h, flags=re.S)
    callout = g.V(k, 'callout', [f"<strong>Plans and networks differ within {g.esc(D)}.</strong> Availability can change by ZIP code and by doctor, so we check your ZIP and your doctors before recommending anything.", f"<strong>Your ZIP code matters in {g.esc(D)}.</strong> Some plans are offered in only part of a county, so we confirm that a plan serves your address and includes your doctors first.", f"<strong>Check before you enroll.</strong> Two neighbors in {g.esc(D)} can see different plan choices depending on ZIP code and doctors, so we verify both for you."])
    h = re.sub(r'(<div class="callout">\s*).*?(\s*</div>)', lambda m: m.group(1) + callout + m.group(2), h, count=1, flags=re.S)
    if h != o:
        open(f, 'w').write(h); done += 1
print('pilot pages upgraded', done)
