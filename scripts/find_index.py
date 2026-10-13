#!/usr/bin/env python3
"""Build site/assets/find-index.json for the 'Find your area' search (counties, cities, ZIPs, states).
Run from repo root after county_gen.py: python3 scripts/find_index.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import county_gen as g
ROOT = g.ROOT; D = ROOT + '/scripts/county_data/'
cen = json.load(open(D + 'county_stats.json'))['census']
slug = json.load(open(D + 'slugmap.json'))
places = json.load(open(D + 'places_all.json'))
zips = json.load(open(D + 'zip_primary.json'))
keys = sorted(cen, key=lambda k: (cen[k]['state'], g.display(cen[k])))
ci = {k: i for i, k in enumerate(keys)}
idx = {
    's': [[sn, st['ab'], st['slug']] for sn, st in g.STATES.items()],
    'c': [[g.display(cen[k]), g.STATES[cen[k]['state']]['ab'], slug[k]] for k in keys],
    'p': sorted([[n, ci[k]] for k, v in places.items() if k in ci for n, pop in v], key=lambda x: x[0].lower()),
    'z': {z: ci[c] for z, c in sorted(zips.items()) if c in ci},
}
out = ROOT + '/site/assets/find-index.json'
json.dump(idx, open(out, 'w'), separators=(',', ':'), ensure_ascii=False)
print('counties', len(idx['c']), 'places', len(idx['p']), 'zips', len(idx['z']), 'bytes', os.path.getsize(out))
