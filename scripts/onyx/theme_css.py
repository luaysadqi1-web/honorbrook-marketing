"""Honorbrook Onyx: the hand-built design layer. Polished black surfaces, hairline silver edges, chrome type and buttons.
Loaded after the compiled palette overrides (palette.py), so these rules set the final look of the main components."""

# Fonts load from a <link> in each page head (scripts/onyx/build.py), not a CSS @import, so the browser finds them sooner.
# Weights in use (Nov 27 2026 scan of the built CSS): Sora 300-700 (headings, buttons), Manrope 400-700 (body; 800 was never used),
# Cinzel 500 and 600 (the logo wordmark; no other loaded face looks like it, so it stays).
FONT_URL = 'https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=Manrope:wght@400;500;600;700&family=Cinzel:wght@500;600&display=swap'
FONT_LINK = '<link rel="stylesheet" href="%s">' % FONT_URL.replace('&', '&amp;')
FONT_IMPORT = "@import url('%s');" % FONT_URL   # kept for reference; the build no longer writes it

ICON_PHONE = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z'/%3E%3C/svg%3E\")"
ICON_CAL = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='5' width='18' height='16' rx='2'/%3E%3Cpath d='M3 10h18M8 3v4M16 3v4'/%3E%3C/svg%3E\")"

CSS = r'''
:root{color-scheme:dark;
  --ox0:#030304;--ox1:#050506;--ox2:#08090b;--ox3:#0c0d10;--ox4:#121318;--ox5:#1a1b21;
  --s1:#dfe2e7;--s2:#d9dce2;--s3:#aab0ba;--s4:#7d838e;
  --hair:rgba(255,255,255,.10);--hair2:rgba(255,255,255,.18);
  --chrome:linear-gradient(180deg,#e9ebef 0%,#d3d7dd 36%,#8f96a1 51%,#c4c9d1 61%,#aab0ba 100%);
  --silver:linear-gradient(180deg,#e6e8ec 0%,#cfd3d9 55%,#aab0ba 100%);
  --btn:linear-gradient(180deg,#eceef1 0%,#cfd3d9 40%,#a3a9b3 56%,#bfc4cc 74%,#d9dce2 100%);
  --panel:linear-gradient(180deg,#15161b 0%,#0c0d10 46%,#08090b 100%);
  --edge:linear-gradient(180deg,rgba(255,255,255,.30),rgba(255,255,255,.05) 36%,rgba(255,255,255,.10));
  --gloss:linear-gradient(118deg,rgba(255,255,255,.075) 0%,rgba(255,255,255,0) 26%);
  --disp:'Sora','Avenir Next','Segoe UI',Helvetica,Arial,sans-serif;
  --body:'Manrope','Segoe UI',Helvetica,Arial,sans-serif;
  --r:20px;
}
html{background:#050506}
html body{background:#050506;color:var(--ink);font-size:18.5px;line-height:1.72;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
html body::before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;
  background:radial-gradient(1100px 560px at 84% -10%,rgba(176,186,206,.11),transparent 62%),radial-gradient(900px 620px at -12% 34%,rgba(120,128,146,.06),transparent 60%)}
html body ::selection{background:#dfe2e7;color:#050506}
html body *{font-family:var(--body)!important}
html body :is(h1,h2,h3,h4,summary,.kicker,.breadcrumb,nav.menu a,.btn-primary,.btn-ghost,.cta-btn,.find-btn,.calc-big-v,.phone,.badge,.fd-tag),
html body :is(h1,h2,h3,h4,summary,.btn-primary,.btn-ghost,.cta-btn,.find-btn) *{font-family:var(--disp)!important}
html body .logo-text,html body .logo-text *{font-family:'Cinzel',Georgia,serif!important}
html body a{color:var(--s1)}
html body :focus-visible{outline:2px solid #fff;outline-offset:3px;border-radius:6px}
html body input[type=checkbox],html body input[type=radio]{accent-color:#dfe2e7}

/* ---------- type ---------- */
html body h1,html body h2,html body h3,html body h4{color:var(--s1);font-weight:600;letter-spacing:-.024em;line-height:1.12}
html body :is(.page-hero h1,h2.section-title,.prose h2,.band h2,.cta-strip h3,.calc-cta h2,.hb-subscribe h2){background:var(--silver);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:#e4e7eb}
html body .kicker{color:var(--s3);font-size:12.5px;font-weight:600;letter-spacing:.24em;text-transform:uppercase;gap:14px;margin-bottom:16px}
html body .kicker::before{content:"";flex:0 0 30px;height:1px;background:linear-gradient(90deg,#fff,rgba(255,255,255,.15));display:block}
html body .kicker::after{display:none}
html body .kicker.center::before{flex:0 0 30px;background:linear-gradient(90deg,rgba(255,255,255,.15),#fff)}
html body .kicker.center::after{content:"";display:block;flex:0 0 30px;height:1px;background:linear-gradient(90deg,#fff,rgba(255,255,255,.15))}
html body .wrap{max-width:1180px}

/* ---------- top bar, header, nav ---------- */
html body .topbar{background:#000;color:#8d939e;font-size:12.5px;letter-spacing:.12em;text-transform:uppercase;padding:9px 0;border-bottom:1px solid rgba(255,255,255,.07)}
html body .topbar a{color:#f4f5f7;letter-spacing:.06em}
html body header{background:rgba(5,5,6,.74);-webkit-backdrop-filter:saturate(1.5) blur(20px);backdrop-filter:saturate(1.5) blur(20px);border-bottom:0;box-shadow:none}
html body header::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.38) 30%,rgba(255,255,255,.38) 70%,transparent)}
html body header .wrap{max-width:1320px}
html body .nav{padding:13px 0}
html body .logo{gap:14px}
html body .logo img{height:46px;width:auto;filter:drop-shadow(0 0 14px rgba(255,255,255,.16))}
html body .logo-text{font-size:17px;font-weight:600;letter-spacing:.34em;text-transform:uppercase;line-height:1.1;white-space:nowrap;
  background:var(--chrome);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:#e4e7eb}
html body .logo-text span{display:block;font-size:10px;font-weight:500;letter-spacing:.62em;margin-top:6px;-webkit-text-fill-color:#9aa1ac;color:#9aa1ac}
html body .logo-text small{display:none}
html body nav.menu{gap:2px}
html body nav.menu a{color:#c9cdd4;font-size:15px;font-weight:500;letter-spacing:.01em;padding:9px 13px;border-radius:10px;transition:color .2s,background .2s}
html body nav.menu a::after{display:none}
html body nav.menu a:hover{color:#e6e8ec;background:rgba(255,255,255,.07)}
html body nav.menu .dd{background:linear-gradient(180deg,#121318,#0a0b0d) padding-box,var(--edge) border-box;border:1px solid transparent;border-radius:16px;padding:8px;min-width:290px;box-shadow:0 40px 80px -20px #000,0 0 0 1px rgba(0,0,0,.6)}
html body nav.menu .dd a{color:#c9cdd4;font-size:15px;padding:10px 14px;border-radius:10px}
html body nav.menu .dd a:hover{background:rgba(255,255,255,.08);color:#e6e8ec}
html body .find-btn{background:rgba(255,255,255,.04);color:#e4e7eb;border:1px solid var(--hair2);border-radius:12px;padding:10px 15px;font-size:14.5px;font-weight:500;letter-spacing:.01em;transition:.2s}
html body .find-btn:hover{background:rgba(255,255,255,.10);color:#e6e8ec;border-color:rgba(255,255,255,.4)}
html body .aep-banner{background:#08090b;color:#aab0ba;font-size:14.5px;letter-spacing:.02em;padding:11px 16px;border-bottom:1px solid var(--hair)}
html body .aep-banner strong{color:#f4f5f7;font-weight:600}
html body .aep-banner strong::before{content:"";display:inline-block;width:7px;height:7px;border-radius:50%;background:#57d9a3;box-shadow:0 0 0 4px rgba(87,217,163,.16),0 0 12px #57d9a3;margin-right:12px;vertical-align:middle;position:relative;top:-1px}
html body .aep-banner a{color:#e6e8ec;text-decoration-color:rgba(255,255,255,.4);text-underline-offset:4px}

/* ---------- buttons: polished chrome ---------- */
html body :is(.btn-primary,.cta-btn,.fd-go,.hb-send,button.btn-primary,.hb-consent .ok){
  background:var(--btn);color:#050506;border:1px solid rgba(255,255,255,.7);border-radius:12px;font-weight:600;letter-spacing:.005em;text-shadow:0 1px 0 rgba(255,255,255,.55);
  box-shadow:inset 0 1px 0 #fff,inset 0 -1px 0 rgba(0,0,0,.22),0 14px 34px -14px rgba(255,255,255,.34),0 2px 12px rgba(0,0,0,.6);
  position:relative;overflow:hidden;transition:transform .2s,box-shadow .2s,filter .2s;text-decoration:none}
html body .btn-primary{padding:16px 30px;font-size:16.5px}
html body .cta-btn{padding:12px 22px;font-size:15px}
html body :is(.btn-primary,.cta-btn,.fd-go)::after{content:"";position:absolute;inset:0;background:linear-gradient(105deg,transparent 36%,rgba(255,255,255,.85) 50%,transparent 64%);transform:translateX(-130%);pointer-events:none}
html body :is(.btn-primary,.cta-btn,.fd-go):hover{background:var(--btn);color:#050506;transform:translateY(-2px);filter:brightness(1.06);box-shadow:inset 0 1px 0 #fff,inset 0 -1px 0 rgba(0,0,0,.22),0 22px 44px -14px rgba(255,255,255,.5),0 2px 12px rgba(0,0,0,.6)}
html body :is(.btn-primary,.cta-btn,.fd-go):hover::after{transform:translateX(130%);transition:transform .8s}
html body a.btn-primary[href^="tel:"]::before,html body .sticky-call a[href^="tel:"]::before,html body .sticky-call a.bk::before{content:"";display:inline-block;width:17px;height:17px;margin-right:10px;vertical-align:-3px;background:currentColor;-webkit-mask:ICON_PHONE center/contain no-repeat;mask:ICON_PHONE center/contain no-repeat}
html body .sticky-call a.bk::before{-webkit-mask-image:ICON_CAL;mask-image:ICON_CAL}
html body .btn-ghost{background:rgba(255,255,255,.03);color:#f4f5f7;border:1px solid var(--hair2);border-radius:12px;padding:15px 28px;font-size:16.5px;font-weight:500;letter-spacing:.005em;transition:.2s;text-decoration:none}
html body .btn-ghost:hover{background:rgba(255,255,255,.10);border-color:rgba(255,255,255,.5);color:#e6e8ec}

/* ---------- surfaces: black lacquer panels ---------- */
html body :is(.card,.rel-card,.quote-card,.bundle-card,.cta-strip,.calc-card,.calc-tile,.hero-card,.contact form,#findInline,.callout,.referral,.faq details,.hb-pop,.table-wrap,.fe-box,.area-grid a,.toc,.author-box,.stat,.note-box){
  background:var(--gloss),var(--panel);background-origin:border-box;border:1px solid var(--hair);border-top-color:rgba(255,255,255,.26);border-left-color:rgba(255,255,255,.13);
  border-radius:var(--r);box-shadow:inset 0 1px 0 rgba(255,255,255,.05),0 30px 60px -34px #000;color:var(--ink)}
html body :is(.card,.rel-card,.calc-tile,.area-grid a){transition:transform .25s,border-color .25s,box-shadow .25s}
html body :is(.card,.rel-card,.calc-tile,.area-grid a):hover{transform:translateY(-4px);border-color:rgba(255,255,255,.3);border-top-color:rgba(255,255,255,.6);box-shadow:inset 0 1px 0 rgba(255,255,255,.08),0 40px 70px -34px #000,0 0 44px -18px rgba(255,255,255,.24)}
html body :is(.card,.rel-card,.bundle-card,.quote-card) h3{font-size:21px;color:#f4f5f7;letter-spacing:-.018em}
html body :is(.card,.rel-card,.bundle-card,.calc-tile) p{color:var(--muted);font-size:16px;line-height:1.6}
html body .card{padding:30px}
html body .card .icon,html body .h-ic{display:inline-grid;place-items:center;width:52px;height:52px;border-radius:14px;background:linear-gradient(180deg,#1d1e25,#0c0d10);border:1px solid var(--hair2);border-top-color:rgba(255,255,255,.4);color:#e4e7eb;font-size:0;margin-bottom:18px;box-shadow:inset 0 1px 0 rgba(255,255,255,.08)}
html body .card .icon svg,html body .h-ic svg{width:24px;height:24px}
html body .h-ic{width:40px;height:40px;border-radius:11px;margin:0 12px 0 0;vertical-align:middle}
html body .h-ic svg{width:20px;height:20px}
html body :is(.card .learn,.bundle-card .learn,.calc-tile span){color:#f4f5f7;font-weight:600;font-size:14.5px;letter-spacing:.02em;text-decoration:none}
html body :is(.card .learn,.bundle-card .learn):hover,html body .rel-card:hover h3,html body .area-grid a:hover{color:#e6e8ec}
html body .badge,html body .badge.gold{align-self:flex-start;width:auto;background:rgba(255,255,255,.07);color:#d9dce2;border:1px solid var(--hair2);border-radius:999px;font-size:10.5px;font-weight:600;letter-spacing:.16em;padding:5px 12px}
html body .quote-card blockquote{color:#d9dce2;font-size:17px;line-height:1.65}
html body .quote-card figcaption{color:var(--s4);font-size:14px;letter-spacing:.02em}
html body :is(.quote-card .rv-stars,.rv-stars,.stars){background:var(--chrome);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:#dfe2e7;letter-spacing:4px}
html body .callout{padding:24px 28px;font-size:17.5px}
html body .callout strong{color:#e6e8ec}
html body .cta-strip{padding:38px 30px}
html body .cta-strip p{color:var(--muted)}

/* ---------- inner page hero ---------- */
html body .page-hero{position:relative;background:radial-gradient(900px 420px at 86% -30%,rgba(190,198,216,.20),transparent 68%),linear-gradient(180deg,#0b0c0f,#050506);color:var(--ink);padding:76px 0 68px;border-bottom:0;overflow:hidden}
html body .page-hero::before{content:"";position:absolute;inset:0;border:0;border-radius:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:64px 64px;-webkit-mask-image:radial-gradient(ellipse 70% 90% at 80% 0%,#000,transparent 72%);mask-image:radial-gradient(ellipse 70% 90% at 80% 0%,#000,transparent 72%)}
html body .page-hero::after{content:"";position:absolute;left:50%;bottom:-1596px;width:3400px;height:1640px;transform:translateX(-50%);border-radius:50%;pointer-events:none;background:radial-gradient(ellipse 44% 16% at 50% 0%,rgba(208,216,234,.16),transparent 72%),#050506;border-top:1px solid rgba(255,255,255,.55);box-shadow:0 -2px 22px rgba(220,228,244,.4),0 -30px 110px rgba(190,202,228,.14);-webkit-mask-image:linear-gradient(90deg,transparent 12%,#000 36%,#000 64%,transparent 88%);mask-image:linear-gradient(90deg,transparent 12%,#000 36%,#000 64%,transparent 88%)}
html body .page-hero{padding-bottom:104px}
html body .page-hero > .wrap{position:relative;z-index:1}
html body .page-hero h1{font-size:clamp(36px,4.6vw,60px);font-weight:600;letter-spacing:-.034em;line-height:1.05;max-width:20ch;margin:18px 0 22px}
html body .page-hero h1 em{font-style:normal;background:none;-webkit-text-fill-color:transparent}
html body .page-hero p.lead{color:#b9bec7;font-size:20px;line-height:1.6;max-width:720px}
html body .breadcrumb{color:var(--s4);font-size:12px;letter-spacing:.2em}
html body .breadcrumb a{color:#c9cdd4;text-decoration:none}
html body .page-hero [style*="aebbd0"]{color:var(--s4)!important;letter-spacing:.04em}

/* ---------- article / prose ---------- */
html body .article{padding:72px 0}
html body .prose{font-size:19px;line-height:1.78;color:#d5d8de}
html body .prose h2{font-size:clamp(28px,3vw,38px);margin:64px 0 16px;padding:0;line-height:1.14}
html body .prose h2::after{display:none}
html body .prose h3{font-size:23px;margin:36px 0 10px;color:#f4f5f7}
html body .prose strong{color:#e6e8ec;font-weight:700}
html body .prose a{color:#e6e8ec;font-weight:600;text-decoration:underline;text-decoration-color:rgba(255,255,255,.34);text-decoration-thickness:1px;text-underline-offset:5px;transition:text-decoration-color .2s}
html body .prose a:hover{text-decoration-color:#fff}
html body .prose a:is(.btn-primary,.cta-btn){color:#050506;text-decoration:none}
html body .prose a.btn-ghost{text-decoration:none}
html body .prose ul li::before{width:6px;height:6px;border-radius:1px;background:linear-gradient(135deg,#fff,#8d939e);top:.74em;transform:rotate(45deg)}
html body .prose ol li::before{background:linear-gradient(180deg,#1d1e25,#0c0d10);color:#f4f5f7;border:1px solid var(--hair2);font-family:var(--disp)!important;width:24px;height:24px;border-radius:8px;font-size:12.5px}
html body .prose ol li{padding-left:40px}
html body .prose img,html body .article img{border-radius:16px;border:1px solid var(--hair)}
html body .crest-divider{color:var(--s3)}
html body .crest-divider::before,html body .crest-divider::after{background:linear-gradient(90deg,transparent,rgba(255,255,255,.4))}
html body .crest-divider::after{background:linear-gradient(90deg,rgba(255,255,255,.4),transparent)}
html body .table-wrap{padding:0;overflow:hidden;overflow-x:auto}
html body table.compare{background:transparent;font-size:16.5px}
html body table.compare th,html body table.compare td{border-bottom:1px solid var(--hair);padding:16px 20px}
html body table.compare thead th{background:rgba(255,255,255,.05);color:var(--s3);font-size:11.5px;letter-spacing:.18em;font-weight:600}
html body table.compare tbody tr:nth-child(even){background:rgba(255,255,255,.018)}
html body table.compare td:first-child{color:#e6e8ec;font-family:var(--body)!important;font-weight:700}
html body table.compare td{color:#c9cdd4}

/* ---------- faq ---------- */
html body .faq{background:#08090b;border-top:1px solid var(--hair);border-bottom:1px solid var(--hair);padding:72px 0}
html body .faq details{margin-bottom:12px;border-radius:16px;transition:border-color .2s}
html body .faq details[open]{border-color:rgba(255,255,255,.3)}
html body .faq summary{color:#f4f5f7;font-size:18.5px;font-weight:500;letter-spacing:-.01em;padding:22px 60px 22px 26px}
html body .faq summary::after{color:var(--s3);font-family:var(--disp)!important;font-weight:300;font-size:28px}
html body .faq .a{color:#b9bec7;font-size:17px;line-height:1.7;padding:0 26px 24px}
html body .faq .a a{color:#e6e8ec}
html body .related{padding:72px 0 84px}

/* ---------- closing band ---------- */
html body .band{position:relative;background:radial-gradient(700px 340px at 50% -34%,rgba(200,208,224,.24),transparent 70%),#030304;border:0;padding:96px 0;overflow:hidden}
html body .band::before,html body .band::after{content:"";position:absolute;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.34) 30%,rgba(255,255,255,.34) 70%,transparent)}
html body .band::before{top:0}html body .band::after{bottom:0}
html body .band h2{font-size:clamp(32px,4.4vw,54px);letter-spacing:-.034em;margin-bottom:14px}
html body .band p{color:var(--s3);font-size:13.5px;letter-spacing:.22em;text-transform:uppercase;margin-bottom:28px}
html body .band .phone{font-size:clamp(34px,5vw,60px);font-weight:300;letter-spacing:-.02em;text-decoration:none;background:var(--chrome);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:#e4e7eb}

/* ---------- footer ---------- */
html body footer{position:relative;background:#030304;color:#8d939e;font-size:14.5px;padding:64px 0 96px}
html body footer::before{content:"";position:absolute;left:0;right:0;top:0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.26) 30%,rgba(255,255,255,.26) 70%,transparent)}
html body footer h3{color:#f4f5f7;font-size:11.5px;letter-spacing:.24em;font-weight:600;margin-bottom:18px}
html body footer a{color:#aab0ba;transition:color .2s}
html body footer a:hover,html body .social-row a:hover,html body .svc-areas a:hover{color:#e6e8ec;border-bottom-color:transparent}
html body :is(.social-row,.svc-areas,.disclaimer){border-top:1px solid rgba(255,255,255,.07)}
html body .social-row a,html body .svc-areas a{color:#aab0ba}
html body .svc-areas{color:#7d838e}html body .svc-areas strong{color:#d9dce2}
html body .disclaimer{color:#7d838e;font-size:12.5px}
html body .disclaimer a{color:#aab0ba}
html body .disclaimer strong{color:#aab0ba}

/* ---------- forms ---------- */
html body :is(input,select,textarea):not([type=checkbox]):not([type=radio]):not([type=submit]):not([type=button]){background:rgba(255,255,255,.04);border:1px solid var(--hair2);border-radius:12px;color:#f4f5f7;font-size:17px;padding:14px 16px;transition:border-color .2s,box-shadow .2s,background .2s}
html body :is(input,textarea)::placeholder{color:#636974}
html body :is(input,select,textarea):not([type=checkbox]):not([type=radio]):focus{outline:none;border-color:#fff;background:rgba(255,255,255,.07);box-shadow:0 0 0 4px rgba(255,255,255,.12)}
html body select option{background:#0c0d10;color:#f4f5f7}
html body :is(.hero-card label,.contact label,.cf label,.fd-label,.grp-label){color:#c9cdd4}
html body .consent,html body .consent span{color:#8d939e}
html body .consent a{color:#d9dce2}
html body .hb-form-msg.err{background:rgba(255,107,97,.10);border:1px solid rgba(255,107,97,.5);color:#ffb9b2;border-radius:12px}
html body .hb-field-err{border-color:#ff6b61!important;background:rgba(255,107,97,.08)}
html body .contact form{padding:36px}
html body .info-line{border-color:var(--hair)}
html body .info-line .ic{display:grid;place-items:center;width:44px;height:44px;border-radius:12px;background:linear-gradient(180deg,#1d1e25,#0c0d10);border:1px solid var(--hair2);color:#e4e7eb;font-size:0;flex:none}
html body .info-line .ic svg{width:20px;height:20px}
html body .info-line strong{color:#f4f5f7}
html body :is(.hb-map iframe,.map-embed iframe){filter:invert(.92) hue-rotate(180deg) grayscale(.7) contrast(.92) brightness(.95);border-radius:16px}
html body .map-embed{border:1px solid var(--hair);border-radius:16px}
html body .hb-map-link{color:#d9dce2}

/* ---------- dialogs, notices, popups ---------- */
html body dialog.fd-dlg{background:linear-gradient(180deg,#121318,#08090b);border:1px solid var(--hair2);border-radius:22px;color:var(--ink);box-shadow:0 60px 120px -20px #000}
html body dialog.fd-dlg::backdrop{background:rgba(0,0,0,.72);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px)}
html body .fd-head{background:transparent;border-bottom:1px solid var(--hair);color:#f4f5f7}
html body .fd-head h2{color:#f4f5f7;font-size:20px;-webkit-text-fill-color:#f4f5f7}
html body .fd-x{color:#aab0ba}
html body .fd-go{border-radius:12px;padding:0 22px}
html body .fd-out{color:#d5d8de}
html body .fd-yes{background:rgba(87,217,163,.08);border:1px solid rgba(87,217,163,.32);border-radius:12px;color:#d9dce2}
html body .fd-no{background:rgba(255,255,255,.05);border:1px solid var(--hair2);border-radius:12px;color:#d9dce2}
html body .fd-list li{border-color:var(--hair)}
html body .fd-tag{color:var(--s4);border-color:var(--hair2);font-size:10.5px;letter-spacing:.12em}
html body .fd-hint,html body .fd-foot{color:var(--muted)}
html body .hb-consent{background:rgba(12,13,16,.94);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border:1px solid var(--hair2);border-radius:16px;color:#c9cdd4;box-shadow:0 30px 60px -10px #000}
html body .hb-consent{left:0;right:0;bottom:0;transform:none;max-width:none;width:auto;border-radius:0;border-width:1px 0 0;font-size:13px;padding:9px 190px 9px 20px;display:flex;align-items:center;justify-content:center;gap:14px;flex-wrap:wrap;box-shadow:none}
html body .hb-consent p{margin:0}
html body .hb-consent button{padding:6px 14px;font-size:13px}
html body .hb-consent a{color:#e6e8ec}
html body .hb-consent button{border-radius:10px}
html body .hb-consent .no{background:transparent;color:#d9dce2;border:1px solid var(--hair2)}
html body .hb-subscribe{background:var(--gloss),var(--panel);border:1px solid var(--hair);border-top-color:rgba(255,255,255,.26);border-radius:var(--r);color:#c9cdd4;box-shadow:0 30px 60px -34px #000}
html body .hb-subscribe p,html body .hb-sub-consent{color:#aab0ba}
html body .hb-sub-kicker{color:var(--s3);letter-spacing:.2em;font-size:11.5px}
html body .hb-sub-consent a{color:#e6e8ec}
html body .hb-pop-ov{background:rgba(0,0,0,.74);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px)}
html body .hb-pop{color:var(--ink)}
html body .hb-pop h2{color:#f4f5f7}
html body .hb-pop-x{color:#aab0ba}
html body .hb-pop-call{color:#e6e8ec}
html body .hb-pop-sub{background:transparent;border:0;box-shadow:none}

/* ---------- calculators ---------- */
html body .calc-out{background:rgba(255,255,255,.035);border:1px solid var(--hair);border-radius:16px}
html body .calc-big-v{font-weight:300;letter-spacing:-.03em;background:var(--chrome);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:#e4e7eb}
html body .calc-big-l{color:var(--s3);letter-spacing:.18em;font-size:11.5px}
html body .calc-tbl th,html body .calc-tbl td{border-bottom:1px solid var(--hair);color:#c9cdd4}
html body .calc-tbl tr.tot th,html body .calc-tbl tr.tot td{color:#e6e8ec}
html body .calc-cta{background:var(--gloss),var(--panel);border:1px solid var(--hair);border-top-color:rgba(255,255,255,.26);border-radius:var(--r)}
html body .calc-cta p{color:#aab0ba}html body .calc-call{color:#e6e8ec}
html body .calc-strip{background:#08090b;border-top:1px solid var(--hair);border-bottom:1px solid var(--hair)}
html body .calc-tile h3{color:#f4f5f7;font-size:20px}
html body details:not(.faq details) summary{color:#f4f5f7}

/* ---------- sticky mobile bar + chat ---------- */
html body .sticky-call{background:rgba(5,5,6,.9);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);border-top:1px solid var(--hair2);box-shadow:0 -20px 40px rgba(0,0,0,.6);box-sizing:border-box;width:100%}
html body .sticky-call a{background:var(--btn);color:#050506;border-radius:12px;font-size:16px;font-weight:700;border:1px solid rgba(255,255,255,.7);box-shadow:inset 0 1px 0 #fff}
html body .sticky-call a.bk{background:rgba(255,255,255,.06);color:#f4f5f7;border:1px solid var(--hair2);box-shadow:none}
html body #hb-launch{background:var(--btn);color:#050506;border:1px solid rgba(255,255,255,.7);border-radius:14px;font-weight:700;box-shadow:inset 0 1px 0 #fff,0 16px 40px -10px rgba(0,0,0,.9),0 0 30px -8px rgba(255,255,255,.3)}
html body #hb-launch:hover{background:var(--btn);filter:brightness(1.06)}
html body #hb-launch svg{stroke:#050506}
html body #hb-chat{background:#08090b;border:1px solid var(--hair2);border-radius:22px;box-shadow:0 60px 120px -20px #000}
html body .hb-head{background:linear-gradient(180deg,#15161b,#0c0d10);border-bottom:1px solid var(--hair);color:#f4f5f7}
html body .hb-head .s,html body .hb-head .x{color:#8d939e}
html body .hb-head .x:hover{color:#e6e8ec}
html body .hb-body{background:#08090b}
html body .hb-bot{background:#15161b;border:1px solid var(--hair);color:#d9dce2}
html body .hb-user{background:var(--btn);color:#050506;font-weight:600}
html body .hb-typing{color:#8d939e}
html body .hb-foot{background:#0c0d10;border-top:1px solid var(--hair)}
html body .hb-foot textarea{background:rgba(255,255,255,.04);border:1px solid var(--hair2);color:#f4f5f7}
html body .hb-send{border-radius:10px}
html body .hb-disc{background:#0c0d10;color:#636974}
html body .hb-disc a{color:#aab0ba}
html body .skip-link{background:#fff;color:#050506}

/* ---------- homepage blocks that survive from the old layout ---------- */
html body section{position:relative}
html body .fe-spotlight,html body .steps,html body .bundle,html body .areas,html body .reviews-block,html body .contact{background:transparent;border-color:var(--hair)}
html body .bundle,html body .reviews-block{background:#08090b;border-top:1px solid var(--hair);border-bottom:1px solid var(--hair)}
html body h2.section-title{font-size:clamp(30px,3.7vw,46px);letter-spacing:-.034em;line-height:1.08;margin-bottom:16px}
html body p.section-sub{color:#aab0ba;font-size:19px;max-width:700px}
html body .fe-box{padding:38px;color:#d9dce2}
html body .fe-box h3{color:#f4f5f7;font-size:22px}
html body .fe-box .row{border-bottom:1px solid var(--hair);color:#c9cdd4}
html body .fe-box .row strong{color:#e6e8ec;font-family:var(--disp)!important;font-weight:500}
html body .fe-box p.note{color:#7d838e}
html body .fe-spotlight li::before{width:6px;height:6px;border-radius:1px;background:linear-gradient(135deg,#fff,#8d939e)}
html body .step .num{background:linear-gradient(180deg,#1d1e25,#0c0d10);color:#f4f5f7;border:1px solid var(--hair2);border-top-color:rgba(255,255,255,.45);font-family:var(--disp)!important;font-weight:300;border-radius:16px;width:58px;height:58px;font-size:24px}
html body .step h3{color:#f4f5f7}html body .step p{color:var(--muted)}
html body .referral{padding:38px}
html body .referral p{color:var(--muted)}
html body .rv-sub,html body .rv-note{color:var(--muted)}
html body .rv-sub a{color:#e6e8ec}
html body .area-grid a{border-radius:14px;color:#e4e7eb;font-size:15.5px}

@media(max-width:1400px){
  html body .find-btn .fb-t{display:none}
  html body .find-btn{padding:10px 11px}
}
@media(max-width:1368px){
  html body header .wrap{padding-left:24px;padding-right:24px}
}
@media(max-width:1180px){
  html body header .wrap{padding-left:20px;padding-right:20px}
  html body header .cta-btn{padding:10px 14px;font-size:13.5px;white-space:nowrap}
  html body nav.menu a{padding:8px 6px;font-size:13.5px}
}
@media(max-width:1260px){
  html body nav.menu a{padding:9px 9px;font-size:14.5px}
  html body .logo-text{font-size:15px;letter-spacing:.28em}
}
@media(max-width:900px){
  html body .hb-consent{bottom:0;padding:8px 14px;font-size:12px;gap:8px;justify-content:flex-start}
  html body .hb-consent button{padding:5px 11px;font-size:12px}
  html body:has(.hb-consent:not([hidden])) #hb-launch{bottom:112px}
  html body{font-size:17.5px}
  html body .topbar{font-size:11px;letter-spacing:.08em}
  html body .logo img{height:40px}
  html body .logo-text{font-size:14px;letter-spacing:.26em}
  html body .logo-text span{font-size:9px}
  html body .page-hero{padding:52px 0 84px}
  html body .prose{font-size:18px}
  html body .article{padding:52px 0}
  html body .band{padding:68px 0}
}
@media(max-width:640px){
  html body header .cta-btn{display:none}
}
@media(max-width:520px){
  html body header .wrap{padding-left:12px;padding-right:12px}
  html body .logo{gap:9px}
  html body .logo img{height:34px}
  html body .logo-text{font-size:11.5px;letter-spacing:.18em}
  html body .logo-text span{font-size:8px;letter-spacing:.42em;margin-top:4px}
  html body .cta-btn{padding:10px 13px;font-size:14px}
  html body .find-btn{padding:10px 11px;margin-right:8px}
  html body .card{padding:24px}
  html body .contact form{padding:24px}
}
html body .steps-more{display:flex;flex-wrap:wrap;gap:12px;margin-top:38px}
html body .fx-how{display:inline-block;margin-top:14px;color:#c9cdd4;font-size:15px;text-decoration:underline;text-decoration-color:rgba(255,255,255,.35);text-underline-offset:4px}
html body .fx-how:hover{color:#e6e8ec}
/* -- silver surfaces and 3D (Nov 17) -- */
html body .band{background:
    repeating-linear-gradient(90deg,rgba(255,255,255,.18) 0 1px,rgba(0,0,0,.025) 1px 2px,transparent 2px 4px),
    linear-gradient(112deg,#e4e6ea 0%,#bcc1c9 24%,#dcdfe4 46%,#a6acb6 70%,#d3d6dc 100%);
  border-top:1px solid #fff;border-bottom:1px solid #8d939e;box-shadow:inset 0 18px 30px -22px rgba(255,255,255,.9),inset 0 -22px 34px -24px rgba(0,0,0,.35)}
html body .band::before,html body .band::after{display:none}
html body .band h2{background:none;-webkit-text-fill-color:currentColor;color:#0b0c0f;text-shadow:0 1px 0 rgba(255,255,255,.7)}
html body .band p{color:#3a3d45}
html body .band .phone{background:none;-webkit-text-fill-color:currentColor;color:#0b0c0f;font-weight:400;text-shadow:0 1px 0 rgba(255,255,255,.7)}
html body .band a:not(.phone){color:#0b0c0f}
html body .step .num{background:var(--btn);color:#050506;border:1px solid #fff;font-weight:500;
  box-shadow:inset 0 1px 0 #fff,0 2px 0 #a4aab3,0 4px 0 #858b95,0 6px 0 #6c727c,0 16px 22px -8px rgba(0,0,0,.85),0 0 30px -8px rgba(255,255,255,.35)}
html body :is(.btn-primary,.cta-btn,.fd-go){box-shadow:inset 0 1px 0 #fff,inset 0 -1px 0 rgba(0,0,0,.22),0 3px 0 #8d939e,0 14px 26px -12px rgba(0,0,0,.9),0 0 26px -10px rgba(255,255,255,.35)}
html body :is(.btn-primary,.cta-btn,.fd-go):hover{box-shadow:inset 0 1px 0 #fff,inset 0 -1px 0 rgba(0,0,0,.22),0 5px 0 #8d939e,0 22px 36px -14px rgba(0,0,0,.9),0 0 34px -8px rgba(255,255,255,.5)}
html body :is(.btn-primary,.cta-btn,.fd-go):active{transform:translateY(2px);box-shadow:inset 0 1px 0 #fff,inset 0 -1px 0 rgba(0,0,0,.22),0 1px 0 #8d939e,0 8px 14px -10px rgba(0,0,0,.9)}
html body .hb-glare{position:absolute;inset:0;border-radius:inherit;pointer-events:none;opacity:0;transition:opacity .25s;
  background:radial-gradient(300px circle at var(--gx,50%) var(--gy,0%),rgba(255,255,255,.17),rgba(255,255,255,.04) 42%,transparent 66%)}
html body .hb-tilting > .hb-glare{opacity:1}
html body .hb-tilting{z-index:2;box-shadow:0 40px 70px -30px #000,0 0 0 1px rgba(255,255,255,.22)}
/* -- booking block on life, final expense and annuity pages -- */
html body .hb-book{margin:40px 0;padding:30px 32px;border-radius:20px;background:var(--gloss),var(--panel);background-origin:border-box;border:1px solid var(--hair);border-top-color:rgba(255,255,255,.26)}
html body .hb-book h3{margin:0 0 10px;font-size:23px;letter-spacing:-.02em;color:#f4f5f7}
html body .hb-book p{margin:0 0 12px;font-size:16.5px;color:#aab0ba}
html body .hb-book ul{margin:0 0 22px;padding-left:20px;font-size:16.5px;color:#d9dce2}
html body .hb-book li{margin:7px 0}
html body .hb-book .hb-book-type{margin:0 0 20px;padding:12px 16px;border-left:2px solid rgba(255,255,255,.45);background:rgba(255,255,255,.04);border-radius:0 10px 10px 0;font-size:15.5px;color:#d9dce2}
html body .hb-book .hb-book-type strong{color:#e6e8ec}
html body .hb-book .hb-book-type a{color:#e6e8ec;text-decoration:underline;text-underline-offset:3px}
html body .hb-book-cta{display:flex;flex-wrap:wrap;align-items:center;gap:14px 18px}
html body .hb-book-how{font-size:15px;color:#c9cdd4;text-decoration:underline;text-decoration-color:rgba(255,255,255,.35);text-underline-offset:4px}
@media(max-width:640px){html body .hb-book{padding:24px 20px;margin:32px 0}}
/* -- life insurance in every county and state (Nov 20): county link list on the state life pages -- */
html body .prose ul.hb-cols{columns:3 190px;column-gap:30px;margin:18px 0 34px;padding:0}
html body .prose ul.hb-cols li{padding-left:0;margin:0 0 9px;break-inside:avoid;font-size:15.5px}
html body .prose ul.hb-cols li::before{display:none}
html body .prose h2#life{scroll-margin-top:96px}
/* -- on-page forms (Nov 25 review): the sticky header must not cover the form heading; optional email field -- */
html body #quote{scroll-margin-top:96px}
html body .hb-quote input[type=email]{width:100%;box-sizing:border-box}
html body .prose p.hb-life-cta{display:flex;flex-wrap:wrap;align-items:center;gap:14px 20px;margin:22px 0 14px}
html body .prose p.hb-life-cta span{font-size:15.5px;color:#c9cdd4}
html body .prose p.hb-life-cta span strong{color:#e6e8ec}
@media(max-width:640px){html body .prose p.hb-life-cta .btn-primary{padding:15px 16px;font-size:15.5px;white-space:nowrap}}
html body .prose .hb-places details{margin:18px 0 34px;border:1px solid var(--hair);border-radius:16px;background:rgba(255,255,255,.03)}
html body .prose .hb-places details summary{cursor:pointer;padding:18px 22px;font-size:16.5px;font-weight:600;color:#f4f5f7;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:16px}
html body .prose .hb-places details summary::-webkit-details-marker{display:none}
html body .prose .hb-places details summary::after{content:"+";font-size:22px;font-weight:300;color:#c9cdd4;line-height:1}
html body .prose .hb-places details[open] summary::after{content:"−"}
html body .prose .hb-places details summary:focus-visible{outline:2px solid #fff;outline-offset:2px;border-radius:14px}
html body .prose .hb-places details ul.hb-cols{margin:0;padding:6px 22px 20px}
@media(max-width:640px){html body .prose ul.hb-cols{columns:2;column-gap:18px}html body .prose ul.hb-cols li{font-size:14.5px}html body .prose .hb-places details ul.hb-cols{padding:4px 16px 16px}}
/* -- booking on the mid-page call to action and the closing band (Nov 19) -- */
footer .hb-langs{color:#8d939e;font-size:13.5px;line-height:1.45;margin:2px 0 8px}
html body .hb-strip-cta{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:14px 22px}
html body .band .band-book{margin-top:30px}
html body .band .band-book a{display:inline-block;padding:16px 32px;border-radius:12px;background:#0b0c0f;color:#f4f5f7;font-family:var(--disp);font-size:16.5px;font-weight:600;text-decoration:none;
  border:1px solid #000;box-shadow:inset 0 1px 0 rgba(255,255,255,.2),0 3px 0 #555a63,0 18px 28px -14px rgba(0,0,0,.75);transition:transform .2s,box-shadow .2s}
html body .band .band-book a:hover{transform:translateY(-2px);box-shadow:inset 0 1px 0 rgba(255,255,255,.2),0 5px 0 #555a63,0 24px 34px -14px rgba(0,0,0,.75)}
html body .band .band-book a:focus-visible{outline:2px solid #0b0c0f;outline-offset:3px}
html body .band .band-text{display:block;width:max-content;max-width:100%;margin:14px auto 0;font-size:17px;font-weight:500;color:#0b0c0f;text-decoration:underline;text-decoration-color:rgba(11,12,15,.4);text-underline-offset:4px}
html body .band .band-text:hover{text-decoration-color:#0b0c0f}
@media(max-width:640px){html body .hb-strip-cta .btn-primary{padding:15px 18px;white-space:nowrap}html body .band .band-book{margin-top:24px}}
/* -- phone and tablet: menu button, full-width menu panel, compact tables, slim bottom bar -- */
html body .hb-burger{display:none}
html body nav.menu .hb-ml b{font-weight:inherit}
html body nav.menu .hb-ml small{display:none}
html body nav.menu .hb-menu-cta{display:none}
@media(max-width:1100px){
  html body nav.menu{display:none}
  html body .hb-burger{display:inline-flex;flex-direction:column;justify-content:center;gap:5px;box-sizing:border-box;width:46px;height:44px;padding:0 13px;margin-left:8px;border-radius:12px;border:1px solid var(--hair2);background:rgba(255,255,255,.04);cursor:pointer;-webkit-tap-highlight-color:transparent}
  html body .hb-burger span{display:block;height:1.5px;background:#f4f5f7;border-radius:2px;transition:transform .25s,opacity .2s}
  html body .hb-burger:focus-visible{outline:2px solid #fff;outline-offset:2px}
  html body.hb-menu-open .hb-burger span:nth-child(1){transform:translateY(6.5px) rotate(45deg)}
  html body.hb-menu-open .hb-burger span:nth-child(2){opacity:0}
  html body.hb-menu-open .hb-burger span:nth-child(3){transform:translateY(-6.5px) rotate(-45deg)}
  html body.hb-menu-open{overflow:hidden}
  html body.hb-menu-open header{background:#050506}
  html body.hb-menu-open nav.menu{display:flex;flex-direction:column;gap:0;position:absolute;left:0;right:0;top:100%;height:100vh;box-sizing:border-box;background:#050506;border-top:1px solid var(--hair);padding:6px 18px 120px;overflow-y:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;z-index:60}
  html body.hb-menu-open nav.menu .has-dd{display:block;position:static}
  html body.hb-menu-open nav.menu > a,html body.hb-menu-open nav.menu .has-dd > a{display:flex;justify-content:space-between;align-items:center;padding:17px 6px;font-size:18px;font-weight:500;color:#f4f5f7;border-bottom:1px solid var(--hair);border-radius:0;background:none}
  html body.hb-menu-open nav.menu .has-dd > a::after{content:"";display:block;position:static;flex:none;width:8px;height:8px;margin-right:8px;background:none;border-right:1.5px solid #8d939e;border-bottom:1.5px solid #8d939e;transform:rotate(45deg);transition:transform .2s}
  html body.hb-menu-open nav.menu .has-dd.open > a::after{transform:rotate(-135deg)}
  html body.hb-menu-open nav.menu .has-dd .dd{display:none;position:static;min-width:0;background:none;border:0;border-radius:0;box-shadow:none;padding:6px 0 10px 12px;border-bottom:1px solid var(--hair)}
  html body.hb-menu-open nav.menu .has-dd.open .dd{display:block}
  html body.hb-menu-open nav.menu .dd a{display:block;white-space:normal;padding:12px 10px;font-size:16px;font-weight:400;color:#aab0ba;border-radius:10px}
  html body.hb-menu-open nav.menu{padding-bottom:0}
  html body.hb-menu-open nav.menu .hb-ml{display:flex;flex-direction:column;gap:4px;text-align:left}
  html body.hb-menu-open nav.menu .hb-ml b{font-size:19px;font-weight:600;letter-spacing:-.01em;color:#f4f5f7}
  html body.hb-menu-open nav.menu .hb-ml small{display:block;font-size:13.5px;font-weight:400;color:#8d939e;letter-spacing:0}
  html body.hb-menu-open nav.menu .has-dd.open > a{border-bottom-color:transparent}
  html body.hb-menu-open nav.menu .has-dd.open .dd{margin:0 0 14px 8px;padding:2px 0 2px 14px;border-left:1px solid var(--hair2);border-bottom:0}
  html body.hb-menu-open nav.menu .hb-menu-cta{display:grid;grid-template-columns:1.7fr 1fr;gap:10px;margin-top:auto;position:sticky;bottom:0;padding:30px 0 calc(16px + env(safe-area-inset-bottom));background:linear-gradient(180deg,rgba(5,5,6,0),#050506 30px)}
  html body.hb-menu-open nav.menu .hb-menu-cta a.hb-mc-how{grid-column:1 / -1}
  html body.hb-menu-open nav.menu .hb-menu-cta a:not(.hb-mc-how){font-size:15px;padding:15px 6px;white-space:nowrap}
  html body.hb-menu-open nav.menu .hb-menu-cta{grid-template-columns:2.2fr 1fr}
  html body.hb-menu-open nav.menu .hb-menu-cta a{display:block;text-align:center;padding:15px 12px;border-radius:12px;font-size:16.5px;font-weight:700;border:1px solid var(--hair2);color:#f4f5f7;background:rgba(255,255,255,.05)}
  html body.hb-menu-open nav.menu .hb-menu-cta a.hb-mc-how{border:0;background:none;padding:8px;font-size:15px;font-weight:500;color:#aab0ba;text-decoration:underline;text-underline-offset:4px}
  html body.hb-menu-open nav.menu .hb-menu-cta a.hb-mc-book{background:var(--btn);color:#050506;border-color:rgba(255,255,255,.7);box-shadow:inset 0 1px 0 #fff}
  html body.hb-menu-open :is(.sticky-call,#hb-launch,.hb-consent){display:none!important}
}
@media(max-width:640px){
  html body table.compare{font-size:15px}
  html body table.compare th,html body table.compare td{padding:12px 11px}
  html body table.compare thead th{font-size:10.5px;letter-spacing:.1em}
  html body .sticky-call{gap:8px;padding:9px 10px calc(9px + env(safe-area-inset-bottom))}
  html body .sticky-call a{font-size:14.5px;padding:13px 4px;white-space:nowrap;letter-spacing:0}
  html body .sticky-call a[href^="tel:"]{flex:0 0 35%}
  html body .sticky-call a::before{margin-right:7px!important;width:15px!important;height:15px!important}
  html body #hb-launch{padding:13px;border-radius:50%;bottom:76px}
  html body #hb-launch span{display:none}
}
@media(max-width:350px){
  html body .sticky-call a{font-size:13px}
  html body .hb-burger{margin-left:6px;width:42px;padding:0 11px}
}
@media (prefers-reduced-motion:no-preference){
  @keyframes oxSheen{0%{background-position:130% 0}55%,100%{background-position:-130% 0}}
  html body .logo img{transition:filter .4s}
  html body .logo:hover img{filter:drop-shadow(0 0 22px rgba(255,255,255,.4))}
}
/* Nov 27 2026 conversion pass (scripts/onyx/lifeleads.py convert): small Text and Schedule links under the hero buttons,
   a phone-only "Get a call back" link under the hero, a three-part bottom bar, and the cookie notice kept above the bar. */
html body .hb-hero-alt{margin:16px 0 0;font-size:15.5px;color:#aab0ba}
html body .hb-hero-alt a{color:#e6e8ec;text-decoration:underline;text-underline-offset:4px}
html body .hb-hero-alt a:hover{color:#fff}
html body .hb-callback-m{display:none}
html body .sticky-call a.tx{background:rgba(255,255,255,.06);color:#f4f5f7;border:1px solid var(--hair2);box-shadow:none}
@media(max-width:900px){
  html body .hb-consent{bottom:calc(66px + env(safe-area-inset-bottom))}
  html body:has(.hb-consent:not([hidden])) #hb-launch{bottom:calc(160px + env(safe-area-inset-bottom))}
}
@media(max-width:640px){
  html body .hb-callback-m{display:block;margin:0;padding:14px 20px;text-align:center;font-size:16px;border-bottom:1px solid var(--hair)}
  html body .hb-callback-m a{color:#f4f5f7;font-weight:600;text-decoration:underline;text-underline-offset:4px}
  html body .sticky-call a[href^="tel:"]{flex:0 0 27%}
  html body .sticky-call a.tx{flex:0 0 21%}
}
/* Nov 27 2026 trust block (scripts/onyx/seo.py verify_block): "Verify our license" on the about and contact pages. */
html body .hb-verify{margin:28px 0;padding:22px 24px;border:1px solid var(--hair2);border-radius:var(--r);background:var(--panel)}
html body .hb-verify h3{margin:0 0 8px;font-size:21px}
html body .hb-verify p{margin:0 0 10px;font-size:16.5px;color:#cfd3d9}
html body .hb-verify ul{margin:0;padding-left:20px;font-size:16.5px}
html body .hb-verify li{margin:4px 0}
html body .hb-verify a{color:#f4f5f7;text-decoration:underline;text-underline-offset:4px}
'''.replace('ICON_PHONE', ICON_PHONE).replace('ICON_CAL', ICON_CAL)
