#!/usr/bin/env python3
"""Move staged blog posts into site/, register them (blog index, sitemap, topic backlog).
Usage: python3 scripts/publish_staged.py --all | --n 6 | slug1 slug2 ...  [--dry-run]
Does NOT run git. Commit and push once afterwards so only ONE Netlify deploy is used.
Refuses to publish a post whose internal /blog/ links point at a post that is neither live nor in this batch."""
import json,os,re,shutil,sys,datetime
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))+'/'
args=[a for a in sys.argv[1:] if not a.startswith('--')]; dry='--dry-run' in sys.argv
man=json.load(open(R+'staging/manifest.json')); by={m['slug']:m for m in man}
staged=[m['slug'] for m in man if os.path.exists(R+f'staging/blog/{m["slug"]}.html')]
if '--all' in sys.argv: pick=staged
elif '--n' in sys.argv: pick=staged[:int(sys.argv[sys.argv.index('--n')+1])]
else: pick=[a for a in args if a in staged]
if not pick: sys.exit('nothing to publish (staged: %d)'%len(staged))
live={f[:-5] for f in os.listdir(R+'site/blog') if f.endswith('.html')}
ok=live|set(pick); bad=False
for sl in pick:
    s=open(R+f'staging/blog/{sl}.html').read()
    for h in set(re.findall(r'href="/blog/([^"#?/]+)"',s)):
        if h not in ok: print('BROKEN LINK',sl,'->',h); bad=True
if bad: sys.exit('Fix or include the linked posts in this batch (use --all).')
today=datetime.date.today()
month=today.strftime('%B %Y'); iso=today.isoformat()
def esc(a): return a.replace('&','&amp;')
cards=''.join(f'''
      <a class="rel-card" href="/blog/{sl}">
        <h3>{esc(by[sl]['title'])}</h3>
        <p class="sans" style="font-size:13px;color:var(--gold-d);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px">{month}</p>
        <p>{esc(by[sl]['desc'])}</p>
      </a>''' for sl in reversed(pick))
if dry: sys.exit('dry run OK: would publish %d posts: %s'%(len(pick),', '.join(pick)))
for sl in pick:
    p=R+f'staging/blog/{sl}.html'; s=open(p).read()
    s=s.replace('"datePublished":"2026-10-12"',f'"datePublished":"{iso}"').replace('"dateModified":"2026-10-12"',f'"dateModified":"{iso}"')
    s=re.sub(r'(<p class="byline sans">By Luay Sadqi, Licensed Agent \(NPN 21370662\) · )[A-Za-z]+ \d{4}',lambda m:m.group(1)+month,s)
    open(R+f'site/blog/{sl}.html','w').write(s); os.remove(p)
i=R+'site/blog/index.html'; s=open(i).read(); s=s.replace('<!-- POSTS:START -->','<!-- POSTS:START -->'+cards,1); open(i,'w').write(s)
m=R+'site/sitemap.xml'; s=open(m).read()
s=s.replace('</urlset>',''.join(f'  <url><loc>https://honorbrook-insurance.com/blog/{sl}</loc><lastmod>{iso}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n' for sl in pick)+'</urlset>'); open(m,'w').write(s)
k=open(R+'_blog-topics.md').read()
import difflib
lines=k.split('\n')
for sl in pick:
    t=by[sl]['title']; cand=[(difflib.SequenceMatcher(None,l[6:].lower(),t.lower()).ratio(),n) for n,l in enumerate(lines) if l.startswith('- [ ] ')]
    if cand:
        r,n=max(cand)
        if r>0.6: lines[n]='- [x] '+lines[n][6:]
k='\n'.join(lines)
open(R+'_blog-topics.md','w').write(k)
rest=[x for x in man if x['slug'] not in pick and os.path.exists(R+f'staging/blog/{x["slug"]}.html')]
json.dump(rest,open(R+'staging/manifest.json','w'),indent=1)
print('published',len(pick),'posts. Next: git add site _blog-topics.md && git commit && git push (ONE push), then ./scripts/indexnow.sh',' '.join('/blog/'+s for s in pick),'/blog/')
