#!/usr/bin/env python3
"""Generate data-driven county/parish pages and state county directories.

Data (scripts/county_data/):
  county_stats.json  - Census 2023 (pop, 65+) + CMS MA State/County Penetration (Sept 2026)
  hospitals.json     - CMS Hospital General Information, matched to county FIPS
Skips the hand-built pilot pages (county-pilot.json) and NoVA counties that already have city pages.
Run from repo root: python3 scripts/county_gen.py
"""
import json, re, html, os, collections, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
DATA = os.path.join(ROOT, 'scripts', 'county_data')
BASE = 'https://honorbrook-insurance.com'
DATA_MONTH = 'September 2026'

STATES = {
 'Virginia': dict(ab='VA', slug='virginia', ship='VICAP', tel='1-800-552-3402', unit='counties'),
 'Maryland': dict(ab='MD', slug='maryland', ship='Maryland SHIP', tel='1-800-243-3425', unit='counties'),
 'North Carolina': dict(ab='NC', slug='north-carolina', ship='SHIIP', tel='1-855-408-1212', unit='counties'),
 'South Carolina': dict(ab='SC', slug='south-carolina', ship='I-CARE', tel='1-800-868-9095', unit='counties'),
 'Georgia': dict(ab='GA', slug='georgia', ship='GeorgiaCares', tel='1-866-552-4464', unit='counties'),
 'Alabama': dict(ab='AL', slug='alabama', ship='Alabama SHIP', tel='1-800-243-5463', unit='counties'),
 'Louisiana': dict(ab='LA', slug='louisiana', ship='SHIIP', tel='1-800-259-5301', unit='parishes'),
 'Texas': dict(ab='TX', slug='texas', ship='HICAP', tel='1-800-252-9240', unit='counties'),
 'Michigan': dict(ab='MI', slug='michigan', ship='MMAP', tel='1-800-803-7174', unit='counties'),
 'Indiana': dict(ab='IN', slug='indiana', ship='Indiana SHIP', tel='1-800-452-4800', unit='counties'),
 'West Virginia': dict(ab='WV', slug='west-virginia', ship='West Virginia SHIP', tel='1-877-987-4463', unit='counties'),
}
NOVA = {'51059': 'fairfax-medicare-insurance', '51013': 'arlington-medicare-insurance',
        '51510': 'alexandria-medicare-insurance', '51610': 'falls-church-medicare-insurance'}

DOI = {'Virginia': ('Virginia Bureau of Insurance', 'https://scc.virginia.gov/pages/Bureau-of-Insurance'),
       'Maryland': ('Maryland Insurance Administration', 'https://insurance.maryland.gov/'),
       'North Carolina': ('North Carolina Department of Insurance', 'https://www.ncdoi.gov/'),
       'South Carolina': ('South Carolina Department of Insurance', 'https://doi.sc.gov/'),
       'Georgia': ('Georgia Office of Insurance and Safety Fire Commissioner', 'https://oci.georgia.gov/'),
       'Alabama': ('Alabama Department of Insurance', 'https://aldoi.gov/'),
       'Louisiana': ('Louisiana Department of Insurance', 'https://ldi.la.gov/'),
       'Texas': ('Texas Department of Insurance', 'https://www.tdi.texas.gov/'),
       'Michigan': ('Michigan Department of Insurance and Financial Services', 'https://www.michigan.gov/difs'),
       'Indiana': ('Indiana Department of Insurance', 'https://www.in.gov/idoi/'),
       'West Virginia': ('West Virginia Offices of the Insurance Commissioner', 'https://www.wvinsurance.gov/')}
GUIDES = [
 ('/blog/when-can-you-switch-medicare-plans', 'When can you switch Medicare plans? Every enrollment window'),
 ('/blog/medicare-advantage-vs-medigap-2026', 'Medicare Advantage vs. Medigap: how to choose'),
 ('/blog/medicare-parts-a-b-c-d-explained', 'Medicare Parts A, B, C and D explained'),
 ('/blog/what-does-medicare-part-d-actually-cost', 'What Medicare Part D actually costs'),
 ('/blog/can-i-change-my-medicare-plan-after-december-7', 'Can I change my Medicare plan after December 7?'),
 ('/blog/how-to-read-medicare-annual-notice-of-change', 'How to read your Medicare Annual Notice of Change'),
 ('/blog/medigap-plan-g-vs-plan-n', 'Medigap Plan G vs. Plan N'),
 ('/blog/do-you-need-a-medicare-agent', 'Do you really need a Medicare agent?'),
 ('/blog/does-medicare-cover-dental-vision-hearing', 'Does Medicare cover dental, vision and hearing?'),
 ('/blog/what-happens-if-i-do-nothing-during-medicare-open-enrollment', 'What happens if you do nothing during open enrollment?'),
 ('/blog/medicare-101-what-every-family-should-know', 'Medicare 101 for families'),
 ('/blog/why-did-my-medicare-advantage-plan-drop-my-doctor-or-drug', 'Why a Medicare Advantage plan drops a doctor or drug'),
]
SBE = {'Georgia': ('Georgia Access', 'https://georgiaaccess.gov/'),
       'Virginia': ('Virginia&rsquo;s Insurance Marketplace', 'https://marketplace.virginia.gov/'),
       'Maryland': ('Maryland Health Connection', 'https://www.marylandhealthconnection.gov/')}
ACRONYMS = set('UAB UVA VCU MUSC HCA UNC WVU UPMC IU LSU UT UTMB OSF HSHS AHN SSM MD II III IV ICU LTAC ER ENT NC SC GA AL TX MI WV LA CHI TMC CMC UH UMC OU CHS VA USA AMG MCV NW SW NE SE HMA DCH CHRISTUS ARH BSA CAMC CJW DLP EAMC ECU FMOL JPS LPDS LV MCG NGMC PG RMH SGMC TRMC UMD UPHS USMD VHS HRMC CMC ECMC KVH MMC NMC SMC UHS'.split())
BRAND = {'MEDSTAR': 'MedStar', 'MCLEOD': 'McLeod', 'MCLAREN': 'McLaren', 'MUNSON': 'Munson'}
ABBR = {'HOSP': 'Hospital', 'CTR': 'Center', 'MED': 'Medical', 'ASSN': 'Association', 'CENT': 'Center', 'GEN': 'General', 'REG': 'Regional', 'MEM': 'Memorial', 'CMTY': 'Community', 'INST': 'Institute'}
LOWER = set('OF THE AND AT IN FOR DE LA ON TO A'.split())
TYPE = {'Acute Care Hospitals': 'acute care', 'Critical Access Hospitals': 'critical access',
        'Childrens': "children's", 'Rural Emergency Hospital': 'rural emergency'}


def esc(s):
    return html.escape(s, quote=False)


def slugify(s):
    s = s.lower().replace("'", '').replace('.', '')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def tcword(w, first):
    if not w:
        return w
    core = re.sub(r'[^A-Z0-9]', '', w)
    if core in ACRONYMS and core != 'LA' and core != 'IN':
        return w
    if core == 'ST' and w.rstrip('.,') == 'ST':
        return 'St.' + w[2:].lstrip('.')
    if core in LOWER and not first:
        return w.lower()
    if '-' in w:
        return '-'.join(tcword(p, True) for p in w.split('-'))
    if w.startswith('MC') and len(core) > 3 and core.isalpha():
        return 'Mc' + w[2:].capitalize()
    return w.capitalize()


def clean_name(name):
    n = name.strip()
    if ' DBA ' in n:
        n = n.split(' DBA ')[-1]
    for _ in range(3):
        n = re.sub(r'[,\s]+(INC|LLC|LLP|LP|PLLC|CORP|DBA)\.?$', '', n)
    m = re.match(r'^(.*),\s*THE$', n)
    if m:
        n = 'THE ' + m.group(1)
    return n


def tc(name):
    ws = clean_name(name).split()
    out = []
    for i, w in enumerate(ws):
        key = re.sub(r'[^A-Z]', '', w)
        out.append(ABBR[key] if key in ABBR and w.rstrip('.') == key else BRAND.get(w, tcword(w, i == 0)))
    return ' '.join(out)


def V(k, key, options):
    import hashlib
    i = int(hashlib.md5(f'{k}:{key}'.encode()).hexdigest(), 16) % len(options)
    return options[i]


OWN = [('Voluntary non-profit', 'nonprofit'), ('Proprietary', 'for-profit'), ('Government', 'government-owned'), ('Physician', 'physician-owned')]


def own_label(o):
    for a, b in OWN:
        if o.startswith(a):
            return b
    return None


def ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1:'st',2:'nd',3:'rd'}.get(n % 10,'th')}"


def display(c):
    n = c['name']
    if n.endswith(' city'):
        base = n[:-5]
        if c['state'] == 'Virginia':
            return f'City of {base}'
        return f'{base} City'
    return n


def pct(a, b):
    return f'{100 * a / b:.1f}%' if b else None


def load():
    d = json.load(open(os.path.join(DATA, 'county_stats.json')))
    cen, pen = d['census'], d['pen']
    hosp = collections.defaultdict(list)
    for h in json.load(open(os.path.join(DATA, 'hospitals.json'))):
        hosp[h['fips']].append(h)
    return cen, pen, hosp


# ---------- shared page shell, taken from an existing county page so the site stays consistent ----------
def shell():
    t = open(os.path.join(SITE, 'harris-county-tx-medicare-insurance.html')).read()
    a = t.index('<body>')
    b = t.index('<section class="page-hero"')
    header = t[a:b]
    foot = t[t.index('<footer>'):]
    marker = '    <div class="svc-areas">\n      <strong>Popular guides:</strong>'
    assert marker in foot
    if 'Medicare by county:' in foot:
        return header, foot
    dirs = ' &middot; '.join(f'<a href="/{v["slug"]}-counties">{k}</a>' for k, v in STATES.items())
    foot = foot.replace(marker, f'    <div class="svc-areas">\n      <strong>Medicare by county:</strong> {dirs}\n    </div>\n' + marker, 1)
    return header, foot


HEAD_TOP = '''<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-J5YG8E3PYC"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-J5YG8E3PYC');
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
'''


def head(title, desc, canon, tw_desc, ldjson, index=True):
    t, d = esc(title), esc(desc)
    out = HEAD_TOP
    out += f'<title>{t}</title>\n<meta name="description" content="{d}">\n'
    out += '<link rel="icon" type="image/png" href="/favicon-64.png">\n<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
    out += f'<link rel="canonical" href="{canon}">\n<meta name="theme-color" content="#142339">\n'
    out += ('<meta name="robots" content="index, follow, max-image-preview:large">\n\n' if index else '<meta name="robots" content="noindex, follow">\n\n')
    out += f'<meta property="og:site_name" content="Honorbrook Insurance">\n<meta property="og:title" content="{t}">\n<meta property="og:description" content="{d}">\n'
    out += f'<meta property="og:url" content="{canon}">\n<meta property="og:type" content="website">\n<meta property="og:locale" content="en_US">\n'
    out += '<meta property="og:image" content="https://honorbrook-insurance.com/assets/og-image.jpg">\n<meta name="twitter:card" content="summary_large_image">\n'
    out += f'<meta name="twitter:title" content="{t}">\n<meta name="twitter:description" content="{esc(tw_desc)}">\n'
    out += '<meta name="twitter:image" content="https://honorbrook-insurance.com/assets/og-image.jpg">\n\n<link rel="stylesheet" href="/assets/style.css">\n\n'
    for j in ldjson:
        out += '<script type="application/ld+json">\n' + json.dumps(j, indent=2, ensure_ascii=False) + '\n</script>\n'
    out += '</head>\n'
    return out


def faq_html(qas):
    return '\n'.join(f'    <details><summary>{esc(q)}</summary><div class="a">{a}</div></details>' for q, a in qas)


# ---------- aggregates ----------
def build_agg(cen, pen):
    agg = {}
    for sname in STATES:
        ks = [k for k, v in cen.items() if v['state'] == sname]
        pop = sum(cen[k]['pop'] for k in ks)
        p65 = sum(cen[k]['p65'] for k in ks)
        elig = sum(pen[k]['elig'] for k in ks if k in pen)
        enr = sum(pen[k]['enr'] for k in ks if k in pen)
        order = sorted(ks, key=lambda k: -cen[k]['p65'])
        agg[sname] = dict(pop=pop, p65=p65, elig=elig, enr=enr, order=order,
                          sh65=100 * p65 / pop, ma=100 * enr / elig)
    return agg


def stats_table(c, p, ag, sname):
    D = display(c)
    rows = [
        ('Residents age 65 and older', f"{c['p65']:,}", f"{ag['p65']:,} statewide"),
        ('Share of residents age 65+', pct(c['p65'], c['pop']), f"{ag['sh65']:.1f}% statewide"),
    ]
    if p:
        rows += [('People with Medicare', f"{p['elig']:,}", f"{ag['elig']:,} statewide"),
                 ('Enrolled in Medicare Advantage', f"{p['enr']:,}", f"{ag['enr']:,} statewide"),
                 ('Medicare Advantage share', pct(p['enr'], p['elig']), f"{ag['ma']:.1f}% statewide")]
    body = '\n'.join(f'          <tr><td>{a}</td><td>{b}</td><td>{c_}</td></tr>' for a, b, c_ in rows)
    return f'''    <div class="table-wrap">
      <table class="compare">
        <thead>
          <tr><th>&nbsp;</th><th>{esc(D)}</th><th>{sname}</th></tr>
        </thead>
        <tbody>
{body}
        </tbody>
      </table>
    </div>
    {sources_line(c['fips'])}
'''




def hospital_block(c, hs, k=''):
    D = display(c)
    if hs:
        hs = sorted(hs, key=lambda h: h['name'])
        items = []
        for h in hs[:12]:
            bits = [TYPE.get(h['type'], h['type'].lower())]
            ol = own_label(h.get('own', ''))
            if ol:
                bits.append(ol)
            bits.append('emergency services' if h.get('emerg') == 'Yes' else 'no emergency department')
            if h.get('rating', '').isdigit():
                bits.append(f"CMS overall rating {h['rating']} of 5")
            items.append(f"      <li>{esc(tc(h['name']))} &mdash; {esc(tc(h['city']))} ({esc('; '.join(bits))})</li>")
        more = f"<p>CMS lists {len(hs) - 12} more {'hospital' if len(hs) - 12 == 1 else 'hospitals'} located in {esc(D)} that {'is' if len(hs) - 12 == 1 else 'are'} not shown here.</p>\n    " if len(hs) > 12 else ''
        tail = V(k, 'hosp', [
            "A hospital being in the county does not mean every plan covers it. Medicare Advantage networks differ by plan, so we check the hospitals and doctors you actually use before you enroll.",
            "Being located in the county is not the same as being in your plan&rsquo;s network. Each Medicare Advantage plan builds its own network, so we confirm that your hospital and your doctors are included before you choose.",
            "Network rules, not geography, decide whether a plan covers a hospital. We look up the hospitals and doctors you use and check them against each plan before you enroll."])
        return f'''    <h2>Hospitals located in {esc(D)}</h2>
    <p>The Centers for Medicare &amp; Medicaid Services (CMS) lists {'this hospital' if len(hs) == 1 else 'these hospitals'} in {esc(D)}:</p>
    <ul>
{chr(10).join(items)}
    </ul>
    {more}<p>{tail} Ratings are CMS Care Compare overall hospital star ratings; they describe the hospital, not whether a plan covers it. Source: CMS Hospital General Information.</p>
'''
    return f'''    <h2>Hospitals and doctors near {esc(D)}</h2>
    <p>CMS Hospital General Information lists no acute care, critical access or children&rsquo;s hospital located inside {esc(D)}. Residents often use hospitals in neighboring counties, which matters for Medicare Advantage because a plan&rsquo;s network may include or leave out the hospital you use. We check your hospitals and doctors before you enroll.</p>
'''










EXTRA = {}




























def others_block(c, ag, cen, slugmap, st, sname):
    order = ag['order']; i = order.index(c['fips'])
    idxs = [j for j in (i-1, i+1, i-2, i+2, i-3, i+3, i-4, i+4) if 0 <= j < len(order)][:8]
    items = '\n'.join(f'      <li><a href="/{slugmap[order[j]]}">{esc(display(cen[order[j]]))}</a></li>' for j in idxs)
    unit = 'parishes' if st['unit'] == 'parishes' else 'counties'
    return f"""    <h2>Other {sname} {unit} we serve</h2>
    <ul>
{items}
    </ul>
    <p>See every {sname} {'parish' if unit == 'parishes' else 'county'} on our <a href="/{st['slug']}-counties">{sname} county directory</a>, or go to our <a href="/{st['slug']}-medicare-insurance">{sname} Medicare hub</a>.</p>
"""


def external_block(sname, D, k=''):
    doi_n, doi_u = DOI[sname]
    items = [
      '<li><a href="https://www.medicare.gov/care-compare/" rel="noopener" target="_blank">Medicare Care Compare</a> for hospitals and doctors.</li>',
      '<li><a href="https://www.ssa.gov/medicare" rel="noopener" target="_blank">Social Security: Medicare</a> to enroll or check status.</li>',
      '<li><a href="https://www.medicare.gov/health-drug-plans/medigap" rel="noopener" target="_blank">Medicare.gov: Medigap</a> on how Medicare Supplement works.</li>',
      ('<li><a href="' + SBE[sname][1] + '" rel="noopener" target="_blank">' + SBE[sname][0] + '</a>, ' + sname + '&rsquo;s own health insurance exchange, if you are not yet on Medicare.</li>') if sname in SBE else '<li><a href="https://www.healthcare.gov/" rel="noopener" target="_blank">HealthCare.gov</a> if you are not yet on Medicare.</li>',
    ]
    off = int(k) % len(items) if str(k).isdigit() else 0
    pick = [items[(off + i) % len(items)] for i in range(3)]
    base = ['<li><a href="https://www.medicare.gov/plan-compare/" rel="noopener" target="_blank">Medicare Plan Finder</a> on Medicare.gov, searchable by ZIP code.</li>',
            f'<li><a href="{doi_u}" rel="noopener" target="_blank">{esc(doi_n)}</a>: {sname}&rsquo;s insurance regulator, including agent license lookup.</li>']
    rows = '\n      '.join([base[0]] + pick + [base[1]])
    return f"""    <h2>Medicare resources from official sources</h2>
    <ul>
      {rows}
    </ul>
"""


def coverage_sentence(k, D):
    L = [('/medicare-advantage', 'Medicare Advantage'), ('/medicare-supplement-medigap', 'Medicare Supplement (Medigap)'), ('/medicare-part-d', 'Part D drug plans'),
         ('/aca-health-insurance', 'ACA health insurance'), ('/ichra', 'ICHRA'), ('/group-health-insurance-shop', 'group health insurance'),
         ('/life-insurance', 'life insurance'), ('/final-expense-life-insurance', 'final expense insurance'), ('/annuities', 'annuities')]
    off = int(k) % len(L)
    L = L[off:] + L[:off]
    links = [f'<a href="{h}">{t}</a>' for h, t in L]
    lead = V(k, 'cov2', [f"As an independent agency we are not tied to one insurer, so for {esc(D)} residents we can compare ",
                         f"We work with many carriers, which lets us compare more than one option for {esc(D)} households, including ",
                         f"Here is what we can help {esc(D)} residents with, drawing on plans from many insurers: "])
    return lead + ', '.join(links[:-1]) + ' and ' + links[-1] + '.'



def load_extra():
    gv = json.load(open(os.path.join(DATA, 'gv.json')))
    rucc = json.load(open(os.path.join(DATA, 'rucc.json')))
    ip = os.path.join(DATA, 'indexable.json')
    idx = set(json.load(open(ip))) if os.path.exists(ip) else None
    EXTRA['places'], EXTRA['zips'] = local_data()
    return gv, rucc, idx


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def wavg(keys, gv, field, w='BENES_TOTAL_CNT'):
    tot = sw = 0.0
    for k in keys:
        x, ww = num(gv.get(k, {}).get(field)), num(gv.get(k, {}).get(w))
        if x is not None and ww:
            tot += x * ww; sw += ww
    return tot / sw if sw else None


def state_gv(keys, gv):
    return {f: wavg(keys, gv, f) for f in ('BENE_AVG_AGE', 'BENE_DUAL_PCT', 'ER_VISITS_PER_1000_BENES', 'IP_CVRD_STAYS_PER_1000_BENES', 'BENES_HH_PCT')}


def rel(x, ref, hi=1.12, lo=0.88, words=('higher than', 'lower than', 'close to')):
    if x is None or not ref:
        return None
    return words[0] if x >= ref * hi else words[1] if x <= ref * lo else words[2]


def bucket(rucc):
    return 'metro' if rucc <= 3 else 'town' if rucc <= 7 else 'rural'


def profile_block(c, k, sname, sg):
    D = display(c)
    g_ = EXTRA['gv'].get(k, {})
    ru = EXTRA['rucc'].get(k)
    out = []
    if ru:
        b = bucket(ru['rucc'])
        desc = ru['desc'].split(' - ', 1)[-1] if ' - ' in ru['desc'] else ru['desc']
        if b == 'metro':
            t = V(k, 'ru', [f"{esc(D)} is a metro county; the U.S. Department of Agriculture describes it as: {esc(desc.lower())}. Metro counties usually have more hospitals and more insurers competing for Medicare members, so there can be more plans to compare.",
                            f"The U.S. Department of Agriculture classifies {esc(D)} as a metro county ({esc(desc.lower())}). Counties like this tend to have a wider choice of hospitals and Medicare plans than rural ones, though networks still differ plan by plan.",
                            f"{esc(D)} sits in a metro area, which the USDA defines as {esc(desc.lower())}. That usually means more doctors, more hospitals and more plan choices in the area."])
        elif b == 'town':
            t = V(k, 'ru', [f"{esc(D)} is a smaller-city and town county; the U.S. Department of Agriculture describes it as: {esc(desc.lower())}. Counties like this often sit between a metro area and rural communities, so some residents use hospitals and specialists in a neighboring county and a plan&rsquo;s network across the county line matters.",
                            f"The USDA classifies {esc(D)} as: {esc(desc.lower())}. In counties of this type, people often travel to a larger neighboring county for specialists, so we check whether your plan&rsquo;s network reaches there.",
                            f"{esc(D)} is a non-metro county with towns and small cities (USDA: {esc(desc.lower())}). Care is often split between local providers and a bigger hospital elsewhere, which is worth testing against each plan&rsquo;s network."])
        else:
            t = V(k, 'ru', [f"{esc(D)} is a rural county; the U.S. Department of Agriculture describes it as: {esc(desc.lower())}. Rural counties tend to have fewer local hospitals and doctors, so a plan&rsquo;s network and the distance to care matter a great deal.",
                            f"The USDA classifies {esc(D)} as: {esc(desc.lower())}. With fewer hospitals and clinics close by, the right Medicare plan here is often the one whose network includes the providers you can really reach.",
                            f"{esc(D)} is a rural county (USDA: {esc(desc.lower())}). Plan choices can be narrower than in a city, and we focus on networks that include the doctors and hospital you actually use."])
        out.append(t)
    n = num(g_.get('BENES_TOTAL_CNT'))
    age, dual = num(g_.get('BENE_AVG_AGE')), num(g_.get('BENE_DUAL_PCT'))
    parts = []
    if n:
        parts.append(f"CMS counts {int(n):,} Medicare beneficiaries in {esc(D)} (2023).")
    if age is not None and sg['BENE_AVG_AGE']:
        r = rel(age, sg['BENE_AVG_AGE'], 1.02, 0.98, ('older than', 'younger than', 'about the same as'))
        parts.append(f"Their average age is {age:.0f}, {r} the {sname} average of {sg['BENE_AVG_AGE']:.0f}.")
    if dual is not None:
        d100 = dual * 100
        r = rel(dual, sg['BENE_DUAL_PCT'], 1.2, 0.8, ('higher than', 'lower than', 'close to'))
        parts.append(f"About {d100:.0f}% are &ldquo;dual eligible,&rdquo; meaning they have both Medicare and Medicaid, {r} the state figure of {sg['BENE_DUAL_PCT'] * 100:.0f}%." if r else f"About {d100:.0f}% are dual eligible.")
        if r == 'higher than':
            parts.append("Where many people have both, special plans for dual-eligible members can matter; see our <a href=\"/medicaid-dual-eligible\">Medicaid and dual eligible guide</a>, since availability varies by plan and area.")
    if parts:
        out.append(' '.join(parts))
    er, ip_, hh = num(g_.get('ER_VISITS_PER_1000_BENES')), num(g_.get('IP_CVRD_STAYS_PER_1000_BENES')), num(g_.get('BENES_HH_PCT'))
    care = []
    if er is not None and ip_ is not None and sg['ER_VISITS_PER_1000_BENES']:
        r1 = rel(er, sg['ER_VISITS_PER_1000_BENES'])
        r2 = rel(ip_, sg['IP_CVRD_STAYS_PER_1000_BENES'])
        care.append(f"Among people in Original Medicare in {esc(D)}, CMS reported about {er:.0f} emergency room visits and {ip_:.0f} inpatient hospital stays per 1,000 beneficiaries in 2023, which is {r1} the state average for emergency visits ({sg['ER_VISITS_PER_1000_BENES']:.0f}) and {r2} it for hospital stays ({sg['IP_CVRD_STAYS_PER_1000_BENES']:.0f}).")
    if hh is not None:
        care.append(f"About {hh * 100:.0f}% received home health care.")
    if care:
        care.append("These figures describe how people use care under Original Medicare; they do not show what any plan covers or costs.")
        out.append(' '.join(care))
    if not out:
        return ''
    return f"    <h2>Who has Medicare in {esc(D)}</h2>\n" + '\n'.join(f'    <p>{x}</p>' for x in out) + '\n    <p class="sans" style="font-size:14px;color:var(--muted)">Sources: <a href="https://data.cms.gov/summary-statistics-on-beneficiary-enrollment/medicare-and-medicaid-reports/medicare-geographic-variation-by-national-state-county" rel="noopener" target="_blank">CMS Medicare Geographic Variation, 2023</a>; <a href="https://www.ers.usda.gov/data-products/rural-urban-continuum-codes" rel="noopener" target="_blank">USDA Rural-Urban Continuum Codes, 2023</a>.</p>\n\n'


def similar_table(c, k, ag, cen, pen, slugmap, st, sname):
    unit = 'parishes' if st['unit'] == 'parishes' else 'counties'
    me = EXTRA['rucc'].get(k, {}).get('rucc')
    mb = bucket(me) if me else None
    order = ag['order']
    cand = [x for x in order if x != k]
    same = [x for x in cand if mb and EXTRA['rucc'].get(x) and bucket(EXTRA['rucc'][x]['rucc']) == mb]
    pool = same if len(same) >= 6 else cand
    pool = sorted(pool, key=lambda x: abs(cen[x]['p65'] - c['p65']))[:6]
    label = {'metro': 'Metro', 'town': 'Smaller city/town', 'rural': 'Rural'}
    rows = []
    for x in pool:
        p = pen.get(x); g_ = EXTRA['gv'].get(x, {})
        ma = pct(p['enr'], p['elig']) if p else 'n/a'
        dl = num(g_.get('BENE_DUAL_PCT'))
        ru = EXTRA['rucc'].get(x)
        rows.append(f'          <tr><td><a href="/{slugmap[x]}">{esc(display(cen[x]))}</a></td><td>{cen[x]["p65"]:,}</td><td>{ma}</td><td>{f"{dl * 100:.0f}%" if dl is not None else "n/a"}</td><td>{label[bucket(ru["rucc"])] if ru else "n/a"}</td></tr>')
    return f"""    <h2>{esc(display(c))} compared with similar {sname} {unit}</h2>
    <div class="table-wrap">
      <table class="compare">
        <thead>
          <tr><th>{'Parish' if unit == 'parishes' else 'County'}</th><th>Residents 65+</th><th>Medicare Advantage share</th><th>Dual eligible share</th><th>Area type</th></tr>
        </thead>
        <tbody>
{chr(10).join(rows)}
        </tbody>
      </table>
    </div>
    <p>See every {sname} {'parish' if unit == 'parishes' else 'county'} in our <a href="/{st['slug']}-counties">{sname} directory</a> or go to our <a href="/{st['slug']}-medicare-insurance">{sname} Medicare hub</a>.</p>
"""


def local_data():
    pl = json.load(open(os.path.join(DATA, 'places.json')))
    zp = json.load(open(os.path.join(DATA, 'zips.json')))
    return pl, zp


def local_block(k, D, sname):
    pl, zp = EXTRA['places'], EXTRA['zips']
    places = [(n, p_) for n, p_, raw in pl.get(k, []) if not n.lower().startswith('balance of')][:6]
    zips = zp.get(k, [])
    out = []
    if places:
        items = ', '.join(f"{esc(n)} ({p_:,})" for n, p_ in places)
        out.append(V(k, 'pl', [f"The largest communities in {esc(D)} by 2023 Census population estimates are {items}. Each figure counts only the people living inside the county.",
                               f"Census Bureau 2023 estimates put the biggest communities in {esc(D)} at {items}, counting only the part of each community inside the county.",
                               f"People in {esc(D)} live in communities such as {items} (2023 population estimates, counting only the part of each community that lies inside the county)."]))
    if zips:
        shown = ', '.join(zips[:14]) + (f" and {len(zips) - 14} more" if len(zips) > 14 else '')
        out.append(V(k, 'zp', [f"ZIP codes that fall mostly inside {esc(D)} include {shown}. Plan availability can change by ZIP code, so have yours ready when we compare plans.",
                               f"We look up plans by ZIP code. In {esc(D)}, that means areas such as {shown}, based on Census ZIP Code Tabulation Areas that lie mostly in the county.",
                               f"Census ZIP Code Tabulation Areas mostly within {esc(D)} number {len(zips)}: {shown}. Your exact ZIP code is what decides which plans you can join."]))
    if not out:
        return ''
    return V(k, 'plh', [f"    <h2>Communities and ZIP codes in {esc(D)}</h2>", f"    <h2>Where people live in {esc(D)}</h2>", f"    <h2>{esc(D)}: communities and ZIP codes</h2>"]) + '\n' + '\n'.join(f'    <p>{x}</p>' for x in out) + '\n\n'


def sources_line(k):
    return V(k, 'src', [
        '<p class="sans" style="font-size:14px;color:var(--muted)">Sources: <a href="https://www.census.gov/data/datasets/time-series/demo/popest/2020s-counties-detail.html" rel="noopener" target="_blank">Census Bureau 2023 estimates</a> and <a href="https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-advantagepart-d-contract-and-enrollment-data/ma-state/county-penetration" rel="noopener" target="_blank">CMS Medicare Advantage penetration, ' + DATA_MONTH + '</a>.</p>',
        '<p class="sans" style="font-size:14px;color:var(--muted)">Data: U.S. Census Bureau (2023 population estimates); <a href="https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-advantagepart-d-contract-and-enrollment-data/ma-state/county-penetration" rel="noopener" target="_blank">CMS, ' + DATA_MONTH + '</a>. Medicare Advantage share is enrollees divided by people with Medicare.</p>',
        '<p class="sans" style="font-size:14px;color:var(--muted)">Figures come from the <a href="https://www.census.gov/data/datasets/time-series/demo/popest/2020s-counties-detail.html" rel="noopener" target="_blank">Census Bureau</a> and <a href="https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-advantagepart-d-contract-and-enrollment-data/ma-state/county-penetration" rel="noopener" target="_blank">CMS</a> (' + DATA_MONTH + ').</p>'])


def free_help(k, D, sname, st):
    # Only our own number plus the federal 1-800-MEDICARE helpline; no SHIP/Eldercare/third-party numbers.
    return f"""    <h2>Questions about Medicare in {esc(D)}?</h2>
    <p>Reach out to us: <a href="/#contact">fill out our short form</a> or call <a href="tel:+15713540146">(571) 354-0146</a>, and a licensed agent will compare the plans available to you, check your doctors and drugs, and stay with you each year at renewal. For general Medicare information, the federal helpline is <strong>1-800-MEDICARE</strong> (<a href="tel:+18006334227">1-800-633-4227</a>).</p>

"""


def guides_block(c, k):
    D = display(c)
    n = len(GUIDES)
    off = int(k) % n
    step = V(k, 'gs', [1, 3, 5, 7])
    pick, seen = [], set()
    i = off
    while len(pick) < 4:
        g_ = GUIDES[i % n]
        if g_[0] not in seen:
            seen.add(g_[0]); pick.append(g_)
        i += step
    items = '\n'.join(f'      <li><a href="{h}">{esc(t)}</a></li>' for h, t in pick)
    head = V(k, 'gh', [f"Medicare guides for {esc(D)} residents", "Read next", f"Plain-English Medicare answers"])
    return f"""    <h2>{head}</h2>
    <ul>
{items}
    </ul>
"""


def interp(c, p, ag, sname, order_rank, n_in_state, unit, k=None):
    k = k or c['fips']
    D = display(c)
    sh_c, sh_s = pct(c['p65'], c['pop']), f"{ag['sh65']:.1f}%"
    parts = [V(k, 'rk', [
        f"{D} ranks {ordinal(order_rank)} of {n_in_state} {sname} {unit} by number of residents age 65 and older, with about {c['p65']:,} people in that age group, or {sh_c} of residents (statewide: {sh_s}).",
        f"With roughly {c['p65']:,} residents age 65 and older, {D} is {ordinal(order_rank)} among {n_in_state} {sname} {unit} for older residents. That group is {sh_c} of its population, compared with {sh_s} across {sname}.",
        f"Among {sname}&rsquo;s {n_in_state} {unit}, {D} comes in {ordinal(order_rank)} for residents age 65 and up ({c['p65']:,}). Older adults make up {sh_c} of the population here; the state figure is {sh_s}."])]
    b = c.get('bands')
    if b:
        t65 = b['AGE6569_TOT'] + b['AGE7074_TOT'] + b['AGE7579_TOT'] + b['AGE8084_TOT'] + b['AGE85PLUS_TOT']
        if b['AGE6064_TOT']:
            parts.append(V(k, 'a60', [f"Another {b['AGE6064_TOT']:,} residents are age 60 to 64 and will reach Medicare eligibility within about five years (see our <a href=\"/turning-65\">turning 65 guide</a>).",
                                      f"About {b['AGE6064_TOT']:,} more people are 60 to 64 and are heading toward Medicare; our <a href=\"/turning-65\">turning 65 guide</a> explains their first steps.",
                                      f"The {b['AGE6064_TOT']:,} residents now between 60 and 64 will become Medicare-eligible soon, and our <a href=\"/turning-65\">turning 65 guide</a> walks through it."]))
        if t65:
            a1, a2, a3 = 100 * (b['AGE6569_TOT'] + b['AGE7074_TOT']) / t65, 100 * (b['AGE7579_TOT'] + b['AGE8084_TOT']) / t65, 100 * b['AGE85PLUS_TOT'] / t65
            parts.append(V(k, 'amx', [f"Among residents 65 and older, {a1:.0f}% are 65 to 74, {a2:.0f}% are 75 to 84 and {a3:.0f}% are 85 or older (Census 2023 estimates).",
                                      f"By age, the 65-and-older group splits {a1:.0f}% ages 65 to 74, {a2:.0f}% ages 75 to 84 and {a3:.0f}% age 85 and up (Census 2023).",
                                      f"Census 2023 estimates show {a1:.0f}% of the 65-plus population is under 75, {a2:.0f}% is 75 to 84 and {a3:.0f}% is 85 or older."]))
    if p:
        cp = 100 * p['enr'] / p['elig']
        diff = cp - ag['ma']
        cmp_ = 'higher than' if diff >= 5 else 'lower than' if diff <= -5 else 'close to'
        parts.append(V(k, 'mx', [f"About {cp:.1f}% of people with Medicare in {D} are enrolled in a Medicare Advantage plan. That is {cmp_} the {sname} average of {ag['ma']:.1f}%.",
                                 f"Medicare Advantage enrollment in {D} is {cp:.1f}% of people with Medicare, {cmp_} the {sname} average of {ag['ma']:.1f}%.",
                                 f"CMS data show {cp:.1f}% of {D} residents with Medicare chose Medicare Advantage, which is {cmp_} the {ag['ma']:.1f}% average across {sname}."]))
        parts.append(V(k, 'cl', ["A county average does not tell you which kind of plan fits you. Whether Medicare Advantage or Original Medicare with a Medigap plan is the better fit depends on your doctors, your prescriptions and how you want to handle costs, so we compare both for your ZIP code.",
                                 "Averages cannot choose a plan for you. Medicare Advantage and Original Medicare with a Medigap plan each suit different people, depending on doctors, medicines and how you prefer to handle costs, and we compare both at your ZIP code.",
                                 "What most people do in a county is less important than what fits you. We weigh Medicare Advantage against Original Medicare with Medigap using your doctors, your drugs and your budget."]))
    else:
        parts.append("CMS does not publish Medicare Advantage enrollment for counties with very few beneficiaries, so no county figure is shown here. We can still compare the plans available at your ZIP code.")
    return ' '.join(parts)


def related_card(href, name, blurb):
    return f'<a class="rel-card" href="{href}"><h3>{esc(name)}</h3><p>{esc(blurb)}</p></a>'


def build_page(c, p, ag, st, hs, rank, n_in, slugmap, cen):
    sname = c['state']
    D = display(c)
    k0 = c['fips']
    slug = slugmap[c['fips']]
    canon = f'{BASE}/{slug}'
    hub = f"/{st['slug']}-medicare-insurance"
    unit_word = 'Parish' if sname == 'Louisiana' else 'County'
    title = f"{D}, {st['ab']} Medicare & Insurance Agent | Honorbrook Insurance"
    if len(title) > 70:
        title = f"{D}, {st['ab']} Medicare Agent | Honorbrook Insurance"
    if p:
        cp = 100 * p['enr'] / p['elig']
        desc = f"{cp:.0f}% of people with Medicare in {D} use Medicare Advantage. Compare plans with an independent {sname} agency by phone or video. (571) 354-0146."
        lead_stat = f"About {cp:.1f}% of people with Medicare in {D} are enrolled in a Medicare Advantage plan, compared with {ag['ma']:.1f}% statewide (CMS, {DATA_MONTH}). "
    else:
        desc = f"Independent, licensed {sname} agency helping {D} residents with Medicare, ACA, life and retirement coverage by phone or video. (571) 354-0146."
        lead_stat = ''
    if len(desc) > 160:
        desc = desc[:157].rsplit(' ', 1)[0] + '...'
    lead = (f"Honorbrook Insurance is an independent agency licensed in {sname}, helping {esc(D)} residents compare Medicare, ACA, life and retirement coverage by phone or video call. "
            f"{lead_stat}Our help is free to you.")
    # FAQ
    hs_names = [tc(h['name']) for h in sorted(hs, key=lambda h: h['name'])[:3]]
    if hs_names:
        doc_a = (f"On a Medicare Advantage plan it depends on that plan&rsquo;s network, so before you enroll we check whether your doctors and the hospitals you use, such as {esc(', '.join(hs_names))}, are in network. "
                 "With a Medicare Supplement (Medigap) plan you can see any doctor who accepts Medicare.")
    else:
        doc_a = ("On a Medicare Advantage plan it depends on that plan&rsquo;s network, so before you enroll we check whether your doctors and the hospitals you use are in network, including hospitals in neighboring counties. "
                 "With a Medicare Supplement (Medigap) plan you can see any doctor who accepts Medicare.")
    qas = [
        (f"Can I get help with Medicare in {D} by phone?",
         V(k0, 'faq1', [f"Yes. We are an independent agency licensed in {sname}, and we help {esc(D)} residents by phone or video call, so you can compare plans from home. There is no pressure to enroll.", f"Yes. Phone and video appointments are how we serve {esc(D)}. We hold a {sname} license, compare plans from many carriers and walk you through them from home, with no pressure to enroll.", f"Yes. You do not need to travel: we are licensed in {sname} and help {esc(D)} residents by phone or video, comparing plans from many insurers at no cost to you."])),
        (f"Will my {D} doctors and hospitals be covered?", doc_a),
    ]
    if p:
        qas.append((f"How many people in {D} have Medicare Advantage?",
                    f"CMS reported {p['enr']:,} people enrolled in a Medicare Advantage plan out of {p['elig']:,} people with Medicare in {esc(D)} in {DATA_MONTH}, or {pct(p['enr'], p['elig'])}. The {sname} average was {ag['ma']:.1f}%."))
    qas += [
        (f"Do you charge {D} residents for help?",
         V(k0, 'faq3', ["No. Our help is free to you. Carriers pay us a commission when we place a policy, and your premium is the same whether you use an agent or enroll on your own.", "No, there is no fee. The insurance company pays us when you enroll, and your premium does not go up because you used an agent.", "No. You pay nothing to work with us. Carriers compensate us, and the price of your plan is the same as if you enrolled directly."])),
        ("When can I enroll or change plans?",
         "You can enroll during your Initial Enrollment Period around your 65th birthday, during the Annual Enrollment Period from October 15 to December 7, or during a Special Enrollment Period if you have a qualifying event such as moving into or within the county."),
    ]
    ld = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": sname, "item": BASE + hub},
            {"@type": "ListItem", "position": 3, "name": D, "item": canon}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', html.unescape(a))}} for q, a in qas]},
        {"@context": "https://schema.org", "@type": "InsuranceAgency", "name": "Honorbrook Insurance",
         "telephone": "+1-571-354-0146",
         "address": {"@type": "PostalAddress", "streetAddress": "8609 Westwood Center Dr, Suite 110", "addressLocality": "Tysons", "addressRegion": "VA", "postalCode": "22182", "addressCountry": "US"},
         "areaServed": {"@type": "AdministrativeArea", "name": f"{D}, {sname}"}, "url": canon},
    ]
    # related: hub + rank neighbours
    order = ag['order']
    i = order.index(c['fips'])
    nb = [order[j] for j in (i - 1, i + 1, i + 2, i - 2) if 0 <= j < len(order)][:2]
    cards = related_card(hub, sname, f"Our {sname} hub: Medicare and insurance help across the state.")
    for k in nb:
        n = display(cen[k])
        cards += related_card('/' + slugmap[k], n, f"Medicare &amp; insurance help for {n} residents, by phone or video.".replace('&amp;', '&'))
    cta_html = V(k0, 'cta', [f"<h3>Let&rsquo;s check your {esc(D)} options together</h3>\n      <p class=\"sans\">We confirm your doctors and prescriptions before you enroll, at no cost to you.</p>", f"<h3>Ready to compare plans in {esc(D)}?</h3>\n      <p class=\"sans\">Tell us your doctors and medicines and we will show you what fits. No cost, no pressure.</p>", f"<h3>Get a clear answer for {esc(D)}</h3>\n      <p class=\"sans\">A short call is enough to compare your options. Our help is free to you.</p>"])
    body = f'''<section class="page-hero" id="maincontent" role="main">
  <div class="wrap">
    <div class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="{hub}">{sname}</a> &rsaquo; {esc(D)}</div>
    <h1>Medicare &amp; insurance help in <em>{esc(D)}</em>, {sname}</h1>
    <p class="lead">{lead}</p>
    <p class="sans" style="font-size:14px;color:#aebbd0;letter-spacing:.3px;margin-top:4px">Independent agency &middot; Luay Sadqi, Licensed Agent, NPN 21370662</p>
    <div class="hero-ctas sans">
      <a class="btn-primary" href="tel:+15713540146">&#128222; Call (571) 354-0146</a>
      <a class="btn-ghost" href="/#contact">Request a free comparison</a>
    </div>
  </div>
</section>

<article class="article">
  <div class="wrap prose">
    <h2>{V(k0, 'nh', ['Medicare in ' + esc(D) + ' by the numbers', esc(D) + ' Medicare at a glance', 'The numbers behind Medicare in ' + esc(D)])}</h2>
{stats_table(c, p, ag, sname)}
    <p>{interp(c, p, ag, sname, rank, n_in, st['unit'], k0)}</p>
{profile_block(c, c['fips'], sname, EXTRA['sg'][sname])}    <p>{V(k0, 'avail', [f"Medicare Advantage and Part D plan availability and provider networks are set county by county, so the plans open to you in {esc(D)} may differ from those in a neighboring county.", f"Insurers choose which counties to serve each year, which means the Medicare Advantage and Part D plans you can pick in {esc(D)} can be different from the ones offered next door.", f"Where you live decides which Medicare Advantage and Part D plans you can join, and {esc(D)} may have a different set of plans than the counties around it."])} We are not based in {esc(D)}; we help {esc(D)} residents by phone or video call.</p>

{hospital_block(c, hs, c['fips'])}{local_block(k0, D, sname)}
{free_help(k0, D, sname, st)}
{external_block(sname, D, k0)}
    <h2>Coverage we offer {esc(D)} residents</h2>
    <p>{coverage_sentence(k0, D)}</p>

    <div class="callout">
      {V(k0, 'callout', [f"<strong>Plans and networks differ within {esc(D)}.</strong> Availability can change by ZIP code and by doctor, so we check your ZIP and your doctors before recommending anything.", f"<strong>Your ZIP code matters in {esc(D)}.</strong> Some plans are offered in only part of a county, so we confirm that a plan serves your address and includes your doctors first.", f"<strong>Check before you enroll.</strong> Two neighbors in {esc(D)} can see different plan choices depending on ZIP code and doctors, so we verify both for you."])}
    </div>

    <div class="cta-strip">
      {cta_html}
      <a class="btn-primary sans" href="/#contact">Get my plan comparison</a>
    </div>

{guides_block(c, c['fips'])}
{similar_table(c, c['fips'], ag, cen, EXTRA['pen'], slugmap, st, sname)}  </div>
</article>

<section class="faq">
  <div class="wrap" style="max-width:880px">
    <div class="kicker">Common questions</div>
    <h2 class="section-title" style="font-size:30px;margin-bottom:24px">{esc(D)} Medicare FAQ</h2>
{faq_html(qas)}
  </div>
</section>

<div class="band">
  <div class="wrap">
    <h2>One honest call can make all the difference.</h2>
    <p>Free consultation &middot; No obligation &middot; No pressure</p>
    <a class="phone" href="tel:+15713540146">(571) 354-0146</a>
  </div>
</div>

<section class="related">
  <div class="wrap">
    <div class="kicker" style="text-align:center;margin-bottom:20px">More {sname} coverage</div>
    <div class="grid-3">
      {cards}
    </div>
  </div>
</section>

'''
    return head(title, desc, canon, f"Independent Medicare & insurance help for {D}, {sname} residents, by phone or video.", ld, index=(c['fips'] in EXTRA['index'])), body


def build_directory(sname, st, cen, pen, ag, slugmap):
    slug = f"{st['slug']}-counties"
    canon = f'{BASE}/{slug}'
    hub = f"/{st['slug']}-medicare-insurance"
    unit = st['unit']
    ks = sorted(ag['order'], key=lambda k: display(cen[k]))
    rows = []
    for k in ks:
        c, p = cen[k], pen.get(k)
        ma = pct(p['enr'], p['elig']) if p else 'n/a'
        el = f"{p['elig']:,}" if p else 'n/a'
        rows.append(f"          <tr><td><a href=\"/{slugmap[k]}\">{esc(display(c))}</a></td><td>{c['p65']:,}</td><td>{el}</td><td>{ma}</td></tr>")
    title = f"{sname} Medicare by {'Parish' if unit == 'parishes' else 'County'} | Honorbrook Insurance"
    desc = f"Medicare Advantage enrollment, residents age 65+ and local Medicare help for all {len(ks)} {sname} {unit}. Independent agency, by phone or video."
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": sname, "item": BASE + hub},
        {"@type": "ListItem", "position": 3, "name": f"{sname} {unit}", "item": canon}]},
        {"@context": "https://schema.org", "@type": "ItemList", "name": f"{sname} {unit} served by Honorbrook Insurance",
         "numberOfItems": len(ks), "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "url": f"{BASE}/{slugmap[k]}", "name": display(cen[k])} for i, k in enumerate(ks)]}]
    body = f'''<section class="page-hero" id="maincontent" role="main">
  <div class="wrap">
    <div class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="{hub}">{sname}</a> &rsaquo; All {unit}</div>
    <h1>Medicare help in every <em>{sname}</em> {'parish' if unit == 'parishes' else 'county'}</h1>
    <p class="lead">Honorbrook Insurance is licensed in {sname} and helps residents of all {len(ks)} {unit} compare Medicare, ACA, life and retirement coverage by phone or video call. Statewide, about {ag['ma']:.1f}% of people with Medicare are enrolled in a Medicare Advantage plan ({'CMS, ' + DATA_MONTH}).</p>
    <div class="hero-ctas sans">
      <a class="btn-primary" href="tel:+15713540146">&#128222; Call (571) 354-0146</a>
      <a class="btn-ghost" href="/#contact">Request a free comparison</a>
    </div>
  </div>
</section>

<article class="article">
  <div class="wrap prose">
    <h2>{sname} Medicare numbers by {'parish' if unit == 'parishes' else 'county'}</h2>
    <p>Medicare Advantage and Part D plans are offered {'parish' if unit == 'parishes' else 'county'} by {'parish' if unit == 'parishes' else 'county'}, so the plans open to you depend on where you live. Pick your {'parish' if unit == 'parishes' else 'county'} to see local figures and free help in your area.</p>
    <div class="table-wrap">
      <table class="compare">
        <thead>
          <tr><th>{'Parish' if unit == 'parishes' else 'County'}</th><th>Residents 65+</th><th>People with Medicare</th><th>Medicare Advantage share</th></tr>
        </thead>
        <tbody>
{chr(10).join(rows)}
        </tbody>
      </table>
    </div>
    <p class="sans" style="font-size:14px;color:var(--muted)">Sources: U.S. Census Bureau 2023 population estimates; CMS Medicare Advantage State/County Penetration, {DATA_MONTH}. Medicare Advantage share = people enrolled in a Medicare Advantage plan divided by people with Medicare. &ldquo;n/a&rdquo; means CMS does not publish a figure for very small counties.</p>
    <div class="callout">
      Questions about your options? <a href="/#contact">Fill out our short form</a> and a licensed agent will reach out.
    </div>
    <div class="cta-strip">
      <h3>Let&rsquo;s check your options together</h3>
      <p class="sans">We confirm your doctors and prescriptions before you enroll, at no cost to you.</p>
      <a class="btn-primary sans" href="/#contact">Get my plan comparison</a>
    </div>
  </div>
</article>

<div class="band">
  <div class="wrap">
    <h2>One honest call can make all the difference.</h2>
    <p>Free consultation &middot; No obligation &middot; No pressure</p>
    <a class="phone" href="tel:+15713540146">(571) 354-0146</a>
  </div>
</div>

'''
    return slug, head(title, desc, canon, f"Medicare help for every {sname} {unit[:-3] if unit == 'parishes' else 'county'}, by phone or video.", ld), body


def main():
    cen, pen, hosp = load()
    agg = build_agg(cen, pen)
    gv, rucc, idx = load_extra()
    if idx is None:
        idx = set()
        for sn in STATES:
            idx.update(agg[sn]['order'][:14])
    EXTRA.update(gv=gv, rucc=rucc, pen=pen, index=idx,
                 sg={sn: state_gv([k for k, v in cen.items() if v['state'] == sn], gv) for sn in STATES})
    pilot = json.load(open(os.path.join(ROOT, 'scripts', 'county-pilot.json')))
    pilot_f = {x['fips'] for v in pilot.values() for x in v}
    header, foot = shell()
    # slug map for every county
    slugmap = {}
    for k, c in cen.items():
        ab = STATES[c['state']]['ab'].lower()
        if k in NOVA:
            slugmap[k] = NOVA[k]
        elif k in pilot_f:
            s = slugify(c['name'][:-5] if c['name'].endswith(' city') else c['name'])
            cand = f'{s}-{ab}-medicare-insurance'
            assert os.path.exists(os.path.join(SITE, cand + '.html')), cand
            slugmap[k] = cand
        else:
            slugmap[k] = f"{slugify(c['name'])}-{ab}-medicare-insurance"
    assert len(set(slugmap.values())) == len(slugmap)
    made, urls = 0, []
    for k, c in cen.items():
        if k in pilot_f or k in NOVA:
            continue
        st = STATES[c['state']]
        ag = agg[c['state']]
        rank = ag['order'].index(k) + 1
        hd, body = build_page(c, pen.get(k), ag, st, hosp.get(k, []), rank, len(ag['order']), slugmap, cen)
        open(os.path.join(SITE, slugmap[k] + '.html'), 'w').write(hd + header + body + foot)
        if k in idx:
            urls.append(slugmap[k])
        made += 1
    for sname, st in STATES.items():
        slug, hd, body = build_directory(sname, st, cen, pen, agg[sname], slugmap)
        open(os.path.join(SITE, slug + '.html'), 'w').write(hd + header + body + foot)
        urls.append(slug)
    # county sitemap
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in sorted(urls):
        sm += f'  <url>\n    <loc>{BASE}/{u}</loc>\n    <lastmod>2026-10-12</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.5</priority>\n  </url>\n'
    sm += '</urlset>\n'
    open(os.path.join(SITE, 'sitemap-counties.xml'), 'w').write(sm)
    json.dump(slugmap, open(os.path.join(DATA, 'slugmap.json'), 'w'))
    print('pages', made, 'directories', len(STATES), 'sitemap urls', len(urls))


if __name__ == '__main__':
    main()
