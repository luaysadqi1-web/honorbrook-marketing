#!/usr/bin/env python3
"""Luay Sadqi Person entity (E-E-A-T) + 11-state backfill on older posts. Idempotent."""
import re, json, glob, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import county_gen as g
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/'
S = R + 'site/'
BASE = 'https://honorbrook-insurance.com'
PID, OID = BASE + '/#luay-sadqi', BASE + '/#organization'
STATES = list(g.STATES)
PERSON = {
 "@type": "Person", "@id": PID, "name": "Luay Sadqi",
 "jobTitle": "Founder & Designated Responsible Licensed Producer",
 "description": "Licensed independent insurance agent helping individuals, families, small businesses and Medicare beneficiaries compare health, life and retirement coverage.",
 "url": BASE + "/about", "image": BASE + "/assets/luay-sadqi.jpg",
 "identifier": [{"@type": "PropertyValue", "propertyID": "National Producer Number (NPN)", "value": "21370662"}],
 "worksFor": {"@id": OID},
 "knowsAbout": ["Medicare Advantage", "Medicare Supplement (Medigap)", "Medicare Part D", "ACA Marketplace health insurance", "ICHRA", "Group health insurance and SHOP", "Term and whole life insurance", "Indexed universal life", "Fixed indexed annuities", "Final expense insurance"],
 "areaServed": [{"@type": "State", "name": s} for s in STATES],
}
AUTHOR_REF = {"@type": "Person", "@id": PID, "name": "Luay Sadqi", "jobTitle": PERSON["jobTitle"], "url": BASE + "/about", "identifier": "NPN 21370662", "worksFor": {"@id": OID}}

def rewrite_ld(h, fn):
    def sub(m):
        try: j = json.loads(m.group(1))
        except Exception: return m.group(0)
        j2 = fn(j)
        if j2 is None: return m.group(0)
        return '<script type="application/ld+json">\n' + json.dumps(j2, indent=2, ensure_ascii=False) + '\n</script>'
    return re.sub(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', sub, h, flags=re.S)

def about(j):
    if j.get('@type') == 'InsuranceAgency':
        j['founder'] = {"@id": PID}; return j
    if j.get('@type') == 'AboutPage':
        j['mainEntity'] = {"@id": PID}; return j
# about.html: person node as its own script
p = S + 'about.html'; h = open(p).read()
if PID not in h:
    h = rewrite_ld(h, about)
    pj = {"@context": "https://schema.org", **PERSON}
    h = h.replace('</head>', '<script type="application/ld+json">\n' + json.dumps(pj, indent=2, ensure_ascii=False) + '\n</script>\n</head>', 1)
    open(p, 'w').write(h); print('about ok')
# index founder
p = S + 'index.html'; h = open(p).read()
def idx(j):
    if j.get('@type') == 'InsuranceAgency' and 'founder' in j:
        j['founder'] = {"@id": PID}; return j
h2 = rewrite_ld(h, idx)
if h2 != h: open(p, 'w').write(h2); print('index founder ok')

# blog posts
def post(j):
    if j.get('@type') == 'BlogPosting':
        j['author'] = AUTHOR_REF
        j['contentLocation'] = [{"@type": "State", "name": s} for s in STATES]
        return j
ship = None
import prep_staged as ps
done = blk = 0
for f in sorted(glob.glob(S + 'blog/*.html')):
    if f.endswith('index.html'): continue
    h = open(f).read(); o = h
    h = rewrite_ld(h, post)
    has = any(k in h for k in ('Medicare help in your state', 'Availability and rules vary by state', 'Medicare Advantage by ', 'Changing Medicare plans in other states'))
    if not has:
        add = ps.ship_block() if 'do not offer every plan available in your area' in h else ps.life_state_block()
        m = re.search(r'\s*</div>\s*</article>', h)
        if m: h = h[:m.start()] + '\n' + add.rstrip('\n') + h[m.start():]; blk += 1
    if h != o: open(f, 'w').write(h); done += 1
print('posts changed', done, 'state blocks added', blk)
