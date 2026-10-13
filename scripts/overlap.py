#!/usr/bin/env python3
"""Measure how much county-page article text overlaps other county pages (6-word shingles).
Usage: python3 scripts/overlap.py [--sample N] [--per-page]   Prints mean/median/max pairwise overlap and, per page, its mean overlap with 40 random peers."""
import re, json, os, sys, random, glob, statistics as st
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')); SITE = ROOT + '/site'
sl = json.load(open(ROOT + '/scripts/county_data/slugmap.json'))
def sh(f):
    h = open(f).read(); m = re.search(r'<article.*?</article>', h, re.S)
    w = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(0))).split() if m else []
    return {' '.join(w[i:i+6]) for i in range(len(w) - 5)}
files = {k: f"{SITE}/{v}.html" for k, v in sl.items() if os.path.exists(f"{SITE}/{v}.html")}
S = {k: sh(f) for k, f in files.items()}
random.seed(7)
keys = list(S)
N = 40
per = {}
for k in keys:
    peers = random.sample([x for x in keys if x != k], N)
    per[k] = sum(len(S[k] & S[p]) / max(1, len(S[k])) for p in peers) / N
vals = sorted(per.values())
print(f"pages {len(keys)} | per-page mean overlap with {N} random peers: mean {st.mean(vals):.2f} median {st.median(vals):.2f} p90 {vals[int(len(vals)*.9)]:.2f} max {vals[-1]:.2f}")
if '--json' in sys.argv: json.dump(per, open(ROOT + '/scripts/county_data/overlap.json', 'w'))
