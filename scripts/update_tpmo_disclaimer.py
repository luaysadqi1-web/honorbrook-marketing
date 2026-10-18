#!/usr/bin/env python3
"""Swap the old Medicare disclaimer for the current TPMO wording (42 CFR 422.2267(e)(41)).

The current required text names how many organizations and products you represent
in the area (CY2027 rule, eCFR as of 2026-10-15; the SHIP clause was removed). The site, the
social linter and the video scenes still carry the older sentence without counts.

Usage (repo root). Get the two numbers from Ritter / your carrier compliance team first:
  python3 scripts/update_tpmo_disclaimer.py --orgs 8 --products 54 --dry-run
  python3 scripts/update_tpmo_disclaimer.py --orgs 8 --products 54

If you sell for every MA organization and PDP sponsor in your service area, add --all-sponsors
(uses CMS Version 2 wording). Counts vary by area: confirm with compliance whether one
agency-wide figure is acceptable or whether pages need area-specific counts.
"""
import argparse, glob, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OLD = re.compile(
    r"We do not offer every plan available in your area\.\s+Any information we provide is limited to "
    r"(?:those|the) plans we do offer in your area\.\s+Please contact Medicare\.gov or 1-800-MEDICARE "
    r"to get information on all of your options\.")


def new_text(orgs, products, all_sponsors):
    if all_sponsors:
        return ("Currently we represent %d organizations which offer %d products in your area. "
                "You can always contact Medicare.gov or 1-800-MEDICARE for help with plan choices." % (orgs, products))
    return ("We do not offer every plan available in your area. Currently we represent %d organizations "
            "which offer %d products in your area. Please contact Medicare.gov or 1-800-MEDICARE "
            "to get information on all of your options."
            % (orgs, products))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--orgs', type=int, required=True)
    ap.add_argument('--products', type=int, required=True)
    ap.add_argument('--all-sponsors', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    rep = new_text(a.orgs, a.products, a.all_sponsors)
    targets = glob.glob(os.path.join(ROOT, 'site/**/*.html'), recursive=True)
    targets += [os.path.join(ROOT, p) for p in ('scripts/video_scenes.py',)]
    targets += glob.glob(os.path.join(ROOT, 'social/queue/*.json'))
    files = hits = 0
    for f in targets:
        t = open(f, encoding='utf-8').read()
        n = len(OLD.findall(t))
        if n:
            files += 1; hits += n
            if not a.dry_run:
                open(f, 'w', encoding='utf-8').write(OLD.sub(rep, t))
    # the social linter builds the disclaimer from a Python string split across lines
    comp = os.path.join(ROOT, 'social/lib/compliance.py')
    c = open(comp, encoding='utf-8').read()
    m = re.search(r'DISCLAIMER_LONG = \(\n(?:\s+".*"\n)+\)', c)
    if m:
        files += 1
        if not a.dry_run:
            open(comp, 'w', encoding='utf-8').write(c.replace(m.group(0), 'DISCLAIMER_LONG = (\n    %r\n)' % rep))
    print(('DRY RUN: would update' if a.dry_run else 'Updated'), hits, 'disclaimers in', files, 'files')
    print('New text:', rep)
    print('Note: queue posts near the 1500-char GBP limit get longer; run social/run_daily.py --dry-run for each queued date.')


if __name__ == '__main__':
    main()
