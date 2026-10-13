#!/usr/bin/env python3
"""Worst-case overlap: for each county page, the highest 6-word-shingle overlap with any other page in the same state.
Writes scripts/county_data/pair_overlap.json and prints the distribution."""
import re, json, os, collections, statistics as st
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')); SITE = ROOT + '/site'
sl = json.load(open(ROOT + '/scripts/county_data/slugmap.json'))
cen = json.load(open(ROOT + '/scripts/county_data/county_stats.json'))['census']
def sh(f):
    h = open(f).read(); m = re.search(r'<article.*?</article>', h, re.S)
    w = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(0))).split() if m else []
    return {' '.join(w[i:i+6]) for i in range(len(w) - 5)}
S = {k: sh(f"{SITE}/{v}.html") for k, v in sl.items() if os.path.exists(f"{SITE}/{v}.html")}
by = collections.defaultdict(list)
for k in S: by[cen[k]['state']].append(k)
worst = {}
for sn, ks in by.items():
    for i, a in enumerate(ks):
        for b in ks[i+1:]:
            o = len(S[a] & S[b]) / max(1, min(len(S[a]), len(S[b])))
            if o > worst.get(a, (0, None))[0]: worst[a] = (o, b)
            if o > worst.get(b, (0, None))[0]: worst[b] = (o, a)
vals = sorted(v[0] for v in worst.values())
print(f"pages {len(vals)} | worst same-state overlap per page: median {st.median(vals):.2f} p90 {vals[int(len(vals)*.9)]:.2f} p99 {vals[int(len(vals)*.99)]:.2f} max {vals[-1]:.2f}")
json.dump({k: round(v[0], 3) for k, v in worst.items()}, open(ROOT + '/scripts/county_data/pair_overlap.json', 'w'))
