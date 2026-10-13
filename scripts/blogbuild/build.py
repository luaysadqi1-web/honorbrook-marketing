import re,json,glob,importlib.util,sys,html,os
import os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE)
R=os.path.abspath(os.path.join(HERE,'..','..'))+'/'
OUT=os.environ.get('BLOG_OUT',R+'staging/blog/')
src=open(R+'site/blog/lost-your-job-coverage-your-health-insurance-options.html').read()
tpl=open(R+'site/medicare-advantage.html').read()
head=src[:src.index('<title>')]
nav=src[src.index('<body>'):src.index('<section class="page-hero"')]
foot=src[src.index('<footer>'):src.index('<div class="disclaimer">')]
tail=tpl[tpl.index('</footer>'):]
MED=tpl[tpl.index('<div class="disclaimer">'):tpl.index('</footer>')]
OTHER_TXT={'life':"This article is for general educational purposes only and is not insurance, tax, investment, or legal advice, an offer of coverage, or a contract. Product availability, features, riders, underwriting, surrender charges, and pricing vary by state, carrier, and individual circumstances. Guarantees are backed by the claims-paying ability of the issuing insurance company. Insurance and annuity products are not bank deposits, are not FDIC-insured, and are not investments. Consult a qualified tax or financial professional about your situation.",
'health':"This article is for general educational purposes only and is not insurance, tax, or legal advice, an offer of coverage, or a contract. Plan availability, eligibility, subsidies, and pricing vary by state, carrier, and individual circumstances, and rules change — confirm current details before you decide."}
def disc(kind):
    if kind=='med': return MED
    return f'''<div class="disclaimer">
      <p><strong>Disclaimer:</strong> Honorbrook Insurance is an independent insurance agency. {OTHER_TXT[kind]}</p>
      <p style="margin-top:10px">Honorbrook Insurance is not connected with or endorsed by any government agency or program.</p>
      <p style="margin-top:10px">© 2026 Luay's Lifeline Inc. dba Honorbrook Insurance · Licensed agent: Luay Sadqi, NPN 21370662 · <a href="/privacy-policy">Privacy Policy</a> · All rights reserved.</p>
    </div>
  </div>
'''
def inline(t):
    t=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',t)
    t=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',t)
    return t.replace(' & ',' &amp; ')
def body_html(md):
    out=[];lst=None;tbl=False;hdr=False
    def close():
        nonlocal lst
        if lst: out.append(f'</{lst}>'); lst=None
    for ln in md.strip().split('\n'):
        ln=ln.rstrip()
        if tbl and not ln.startswith('|'):
            out.append('</tbody>\n</table>\n</div>'); tbl=False
        if not ln: close(); continue
        if ln.startswith('## '): close(); out.append(f'<h2>{inline(ln[3:])}</h2>')
        elif ln.startswith('- '):
            if lst!='ul': close(); out.append('<ul>'); lst='ul'
            out.append(f'  <li>{inline(ln[2:])}</li>')
        elif re.match(r'\d+\. ',ln):
            if lst!='ol': close(); out.append('<ol>'); lst='ol'
            txt=re.sub(r'^\d+\. ','',ln); out.append('  <li>'+inline(txt)+'</li>')
        elif ln.startswith('|'):
            close()
            cells=[c.strip() for c in ln.strip('|').split('|')]
            if set(''.join(cells))<=set('-: '): continue
            if not tbl: out.append('<div class="table-wrap">\n<table class="compare">\n<thead>'); tbl=True; hdr=True
            else: hdr=False
            tag='th' if hdr else 'td'
            out.append('<tr>'+''.join('<'+tag+'>'+inline(c)+'</'+tag+'>' for c in cells)+'</tr>')
            if hdr: out.append('</thead>\n<tbody>')
            continue
        elif ln.startswith('!callout '): close(); out.append(f'<div class="callout">\n  {inline(ln[9:])}\n</div>')
        elif ln.startswith('!cta '):
            close(); a,b,c,d=[x.strip() for x in ln[5:].split('|')]
            out.append(f'<div class="cta-strip">\n  <h3>{inline(a)}</h3>\n  <p class="sans">{inline(b)}</p>\n  <a class="btn-primary sans" href="{d}">{c}</a>\n</div>')
        else: close(); out.append(f'<p>{inline(ln)}</p>')
    close()
    if tbl: out.append('</tbody>\n</table>\n</div>')
    return '\n    '.join(out)
def esc(a): return a.replace('&','&amp;')
def build(p):
    slug=p['slug'];t=p['title'];url='https://honorbrook-insurance.com/blog/'+slug
    desc=p['desc'];short=p['short'];faqs=p['faqs']
    j=lambda s:s.replace('\\','\\\\').replace('"','\\"')
    metas=f'''<title>{esc(p['ttl'])} | Honorbrook</title>
<meta name="description" content="{esc(desc)}">
<link rel="icon" type="image/png" href="/favicon-64.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#142339">
<meta name="robots" content="index, follow, max-image-preview:large">

<meta property="og:site_name" content="Honorbrook Insurance">
<meta property="og:title" content="{esc(p['ttl'])} | Honorbrook">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="article">
<meta property="og:locale" content="en_US">
<meta property="og:image" content="https://honorbrook-insurance.com/assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(p['ttl'])} | Honorbrook">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="https://honorbrook-insurance.com/assets/og-image.jpg">

<link rel="stylesheet" href="/assets/style.css">

<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{{"@type":"ListItem","position":1,"name":"Home","item":"https://honorbrook-insurance.com/"}},
{{"@type":"ListItem","position":2,"name":"Blog","item":"https://honorbrook-insurance.com/blog/"}},
{{"@type":"ListItem","position":3,"name":"{j(short)}","item":"{url}"}}]}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BlogPosting","headline":"{j(t)}","description":"{j(desc)}","datePublished":"2026-10-12","dateModified":"2026-10-12","author":{{"@type":"Person","name":"Luay Sadqi"}},"publisher":{{"@type":"Organization","name":"Honorbrook Insurance"}},"mainEntityOfPage":{{"@type":"WebPage","@id":"{url}"}}}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
''' + ",\n".join(f'{{"@type":"Question","name":"{j(q)}","acceptedAnswer":{{"@type":"Answer","text":"{j(a)}"}}}}' for q,a in faqs) + '''
]}
</script>
</head>
'''
    h1=esc(t).replace(p['em'],'<em>'+p['em']+'</em>',1) if p['em'] in t else esc(t)
    hero=f'''<section class="page-hero" id="maincontent" role="main">
  <div class="wrap">
    <div class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/blog/">Blog</a> &rsaquo; {esc(short)}</div>
    <h1>{h1}</h1>
    <p class="lead">{inline(p['lead'])}</p>
    <p class="byline sans">By Luay Sadqi, Licensed Agent (NPN 21370662) · October 2026</p>
  </div>
</section>

'''
    body=p['body']
    ex=''
    for mn in ('extras1','extras2','extras3','extras4','extras5','extras6'):
        try:
            m=__import__(mn); ex+=m.EX.get(p['slug'],'')+'\n'
        except Exception: pass
    if ex:
        i=body.rfind('## How ')
        body=body[:i]+ex+'\n'+body[i:]
    bh=body_html(body)
    words=len(re.sub(r'<[^>]+>',' ',bh).split())
    rel=''.join(f'      <a class="rel-card" href="{h}"><h3>{esc(a)}</h3><p>{esc(b)}</p></a>\n' for a,b,h in p['rel'])
    page=f'''<article class="article">
  <div class="wrap prose">
    {bh}
  </div>
</article>

<section class="faq">
  <div class="wrap" style="max-width:880px">
    <div class="kicker">Common questions</div>
    <h2 class="section-title" style="font-size:30px;margin-bottom:24px">{esc(p['faqh'])}</h2>
''' + "\n".join(f'    <details><summary>{esc(q)}</summary><div class="a">{esc(a)}</div></details>' for q,a in faqs) + f'''
    <p class="sans" style="margin-top:20px;font-style:italic">This article is general information, not insurance, tax, investment, or legal advice &mdash; a licensed agent will help you weigh your specific situation.</p>
  </div>
</section>

<div class="band">
  <div class="wrap">
    <h2>One honest call can make all the difference.</h2>
    <p>Free consultation · No obligation · No pressure</p>
    <a class="phone" href="tel:+15713540146">(571) 354-0146</a>
  </div>
</div>

<section class="related">
  <div class="wrap">
    <div class="kicker" style="text-align:center;margin-bottom:20px">Keep exploring</div>
    <div class="grid-3">
{rel}    </div>
  </div>
</section>

'''
    out=head+metas+nav+hero+page+foot+disc(p['kind'])+"</footer>\n"+tail[len('</footer>'):]
    os.makedirs(OUT,exist_ok=True); open(OUT+slug+'.html','w').write(out)
    return words
def load(f):
    pass
def _unused(): pass
def load(f):
    sp=importlib.util.spec_from_file_location('m',f);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m.POSTS
if __name__=='__main__':
    files=sys.argv[1:] or sorted(glob.glob(HERE+'/posts_*.py'))
    man=[]
    for f in files:
        if not os.path.isabs(f): f=os.path.join(HERE,f)
        for p in load(f):
            w=build(p); print(p['slug'],w,'OK' if 800<=w<=1150 else '<<<LEN')
            man.append(dict(slug=p['slug'],title=p['title'],desc=p['desc']))
    if os.environ.get('BLOG_OUT') is None:
        import json
        old=[]
        try: old=json.load(open(R+'staging/manifest.json'))
        except Exception: pass
        keep={m['slug']:m for m in old if os.path.exists(R+'staging/blog/'+m['slug']+'.html')}
        keep.update({m['slug']:m for m in man})
        json.dump(list(keep.values()),open(R+'staging/manifest.json','w'),indent=1)
