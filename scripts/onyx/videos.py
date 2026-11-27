"""Explainer videos on the pages they explain (Nov 25, 2026; the owner asked for more videos on the site).

One JSON file per video in scripts/onyx/data/videos/<slug>.json:
  slug         file name of the video: site/assets/video/<slug>.mp4 and <slug>.jpg (the poster)
  page         the page that carries the video and its VideoObject schema, relative to the build, e.g. "blog/x.html"
  also         optional list of other pages that show the same video (no schema there: one watch page per video)
  heading      the visible heading, shown as "Watch: <heading>"
  name         schema name
  description  schema description (one or two plain sentences)
  upload       ISO date the video was made
  seconds      duration in whole seconds
  transcript   the full narration, exactly as spoken
  before       optional dict page -> exact text the block is placed in front of (default: the second <h2 of the article)

A video is embedded only when both files exist in site/assets/video, so a video that is not finished never
leaves a broken player on a page. The mp4 and jpg are tracked in git under site/assets/video; Netlify copies
them into the published folder (see netlify.toml).
"""
import os, re, json, glob, html, datetime, zoneinfo, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(HERE, 'data', 'videos')
SRC = os.path.join(ROOT, 'site', 'assets', 'video')
BASE = 'https://honorbrook-insurance.com'


def _iso(sec):
    m, s = divmod(int(round(sec)), 60)
    return 'PT%dM%dS' % (m, s) if m else 'PT%dS' % s


def _when(d):
    """A date-only value becomes noon Eastern with its UTC offset (Google asks for a full date-time with a time zone)."""
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', d): return d
    t = datetime.datetime(int(d[:4]), int(d[5:7]), int(d[8:]), 12, tzinfo=zoneinfo.ZoneInfo('America/New_York'))
    return t.isoformat()


def _block(v):
    e = html.escape
    return ('    <h2>Watch: %s</h2>\n'
            '    <video controls preload="none" playsinline poster="/assets/video/%s.jpg" style="width:100%%;max-width:720px;border-radius:10px;display:block;margin:0 0 12px">\n'
            '      <source src="/assets/video/%s.mp4" type="video/mp4">\n'
            '      Your browser does not support video. A transcript is below.\n'
            '    </video>\n'
            '    <details><summary>Video transcript</summary><div class="a">%s</div></details>\n\n'
            % (e(v['heading'], quote=False), v['slug'], v['slug'], e(v['transcript'], quote=False)))


def _schema(v):
    d = {"@context": "https://schema.org", "@type": "VideoObject", "name": v['name'], "description": v['description'],
         "thumbnailUrl": "%s/assets/video/%s.jpg" % (BASE, v['slug']), "uploadDate": _when(v['upload']), "duration": _iso(v['seconds']),
         "contentUrl": "%s/assets/video/%s.mp4" % (BASE, v['slug']), "publisher": {"@type": "Organization", "name": "Honorbrook Insurance"},
         "transcript": v['transcript']}
    return '<script type="application/ld+json">\n%s\n</script>\n' % json.dumps(d, indent=1, ensure_ascii=False).replace('</', '<\\/')


def _spot(s, anchor):
    """Index where the block goes: in front of the given text, else in front of the second <h2 of the article."""
    if anchor:
        if s.count(anchor) != 1: raise SystemExit('videos: anchor found %d times: %r' % (s.count(anchor), anchor[:70]))
        i = s.index(anchor)
        return s.rfind('\n', 0, i) + 1 if s[s.rfind('\n', 0, i) + 1:i].strip() == '' else i
    a = s.find('<article'); b = s.find('</article>', a)
    if a < 0 or b < 0: raise SystemExit('videos: no article on the page')
    hs = [m.start() for m in re.finditer(r'<h2[ >]', s[a:b])]
    if len(hs) < 2: raise SystemExit('videos: fewer than two headings in the article')
    i = a + hs[1]
    return s.rfind('\n', 0, i) + 1 if s[s.rfind('\n', 0, i) + 1:i].strip() == '' else i


def apply(out):
    done, skipped = [], []
    for jf in sorted(glob.glob(os.path.join(DATA, '*.json'))):
        v = json.load(open(jf, encoding='utf-8'))
        for k in ('slug', 'page', 'heading', 'name', 'description', 'upload', 'seconds', 'transcript'):
            if not v.get(k): raise SystemExit('videos: %s has no %s' % (os.path.basename(jf), k))
        if not (os.path.isfile(os.path.join(SRC, v['slug'] + '.mp4')) and os.path.isfile(os.path.join(SRC, v['slug'] + '.jpg'))):
            skipped.append(v['slug']); continue
        for n, page in enumerate([v['page']] + list(v.get('also') or [])):
            p = os.path.join(out, page)
            if not os.path.isfile(p): raise SystemExit('videos: page not in the build: ' + page)
            s = open(p, encoding='utf-8').read()
            if '/assets/video/%s.mp4' % v['slug'] in s: continue
            i = _spot(s, (v.get('before') or {}).get(page))
            s = s[:i] + _block(v) + s[i:]
            if n == 0:
                if s.count('</head>') != 1: raise SystemExit('videos: head not found on ' + page)
                s = s.replace('</head>', _schema(v) + '</head>', 1)
            open(p, 'w', encoding='utf-8').write(s)
            done.append(page)
    dated = 0   # the older videos, whose schema is written in the page itself
    for p in glob.glob(os.path.join(out, '**', '*.html'), recursive=True):
        if '/assets/video' in p: continue
        s = open(p, encoding='utf-8', errors='ignore').read()
        if '"uploadDate"' not in s: continue
        t = re.sub(r'("uploadDate":\s*")(\d{4}-\d{2}-\d{2})(")', lambda m: m.group(1) + _when(m.group(2)) + m.group(3), s)
        if t != s: open(p, 'w', encoding='utf-8').write(t); dated += 1
    # every video file a page uses has to be in git under site/assets/video, or the live page shows a dead player (read-only check)
    used = set()
    for p in glob.glob(os.path.join(out, '**', '*.html'), recursive=True):
        if '/assets/video' in p: continue
        used.update(re.findall(r'/assets/video/([A-Za-z0-9_.-]+\.(?:mp4|jpg|vtt|webm))', open(p, encoding='utf-8', errors='ignore').read()))
    untracked = []
    for f in sorted(used):
        if not os.path.isfile(os.path.join(SRC, f)): raise SystemExit('videos: a page uses a video file that does not exist: ' + f)
        try:
            if subprocess.call(['git', '-C', ROOT, 'ls-files', '--error-unmatch', 'site/assets/video/' + f], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0: untracked.append(f)
        except OSError: pass
    return {'embedded on': done, 'waiting for files': skipped, 'dates given a time zone': dated, 'NOT IN GIT YET (stage by name when publishing)': untracked}
