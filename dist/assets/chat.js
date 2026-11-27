/* ==========================================================================
   Honorbrook Insurance — "Brook" chat widget
   Drop-in: <script src="/assets/chat.js" defer></script> before </body>.
   Talks to /.netlify/functions/chat (Claude-powered, key stays server-side).
   ========================================================================== */
(function () {
  "use strict";
  if (window.__honorbrookChat) return;
  window.__honorbrookChat = true;

  var ENDPOINT = "/.netlify/functions/chat";
  var PHONE = "(301) 615-8289";
  var GREETING =
    "Hi, I'm Brook 👋 — Honorbrook's assistant. I can answer questions about Medicare, ICHRA, ACA, life insurance and more, or set up a free callback with a licensed agent. What brings you in today?";

  // conversation history sent to the function (role/content pairs)
  var history = [];
  var sending = false;

  /* ---------- styles ---------- */
  var css = `
  #hb-chat,#hb-launch{font-family:'Source Sans 3','Segoe UI',Arial,sans-serif;box-sizing:border-box}
  #hb-chat *,#hb-launch *{box-sizing:border-box}
  #hb-launch{position:fixed;right:22px;bottom:22px;z-index:2147483000;display:flex;align-items:center;gap:10px;
    background:#c9a227;color:#142339;border:1px solid #a8851a;border-radius:40px;padding:13px 20px;cursor:pointer;
    font-size:16px;font-weight:700;box-shadow:0 8px 26px rgba(20,35,57,.30);transition:transform .15s,background .15s}
  #hb-launch:hover{background:#e3c25c;transform:translateY(-2px)}
  #hb-launch svg{width:22px;height:22px;display:block}
  #hb-chat{position:fixed;right:22px;bottom:22px;z-index:2147483001;width:380px;max-width:calc(100vw - 32px);
    height:600px;max-height:calc(100vh - 90px);background:#faf7f0;border-radius:14px;overflow:hidden;display:none;
    flex-direction:column;box-shadow:0 24px 60px rgba(20,35,57,.40);border:1px solid #e7e0cf}
  #hb-chat.open{display:flex}
  .hb-head{background:linear-gradient(135deg,#142339,#2c486a);color:#eef1f6;padding:15px 16px;display:flex;align-items:center;gap:12px;border-bottom:3px solid #c9a227}
  .hb-head img{width:34px;height:38px;display:block}
  .hb-head .t{font-family:'Playfair Display',Georgia,serif;font-size:18px;font-weight:700;line-height:1.1}
  .hb-head .s{font-size:12px;color:#aebbd0;letter-spacing:.4px;margin-top:2px}
  .hb-head .x{margin-left:auto;background:none;border:none;color:#aebbd0;font-size:24px;cursor:pointer;line-height:1;padding:4px}
  .hb-head .x:hover{color:#e3c25c}
  .hb-body{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px;background:#faf7f0}
  .hb-msg{max-width:84%;padding:11px 14px;border-radius:14px;font-size:15px;line-height:1.5;white-space:pre-wrap;word-wrap:break-word}
  .hb-bot{background:#fff;border:1px solid #e7e0cf;color:#2a2a2a;align-self:flex-start;border-bottom-left-radius:4px}
  .hb-user{background:#1b2f4b;color:#eef1f6;align-self:flex-end;border-bottom-right-radius:4px}
  .hb-typing{align-self:flex-start;color:#5d6b7d;font-size:14px;font-style:italic;padding:4px 6px}
  .hb-foot{border-top:1px solid #e7e0cf;background:#fff;padding:10px;display:flex;gap:8px;align-items:flex-end}
  .hb-foot textarea{flex:1;resize:none;border:1.5px solid #c8d0db;border-radius:8px;padding:10px 12px;font-size:15px;
    font-family:inherit;max-height:90px;background:#fbfcfe;line-height:1.4}
  .hb-foot textarea:focus{outline:none;border-color:#c9a227}
  .hb-send{background:#c9a227;border:1px solid #a8851a;color:#142339;border-radius:8px;width:42px;height:42px;cursor:pointer;
    font-size:18px;flex-shrink:0;display:flex;align-items:center;justify-content:center}
  .hb-send:hover{background:#e3c25c}
  .hb-send:disabled{opacity:.5;cursor:default}
  .hb-disc{font-size:10.5px;color:#8195ad;text-align:center;padding:6px 10px 9px;background:#fff;line-height:1.3}
  .hb-disc a{color:#1b2f4b;font-weight:600}
  @media(max-width:560px){
    #hb-chat{right:0;bottom:0;width:100vw;max-width:100vw;height:100vh;max-height:100vh;border-radius:0;border:none}
    #hb-launch{right:14px;bottom:78px;padding:12px 18px;font-size:15px}
  }`;
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  var CREST = '<img src="/assets/hb-mark.png" alt="" width="34" height="29" style="display:block;width:34px;height:auto">';

  /* ---------- launcher ---------- */
  var launch = document.createElement("button");
  launch.id = "hb-launch";
  launch.setAttribute("aria-label", "Open chat with Honorbrook");
  launch.innerHTML =
    '<svg viewBox="0 0 24 24" fill="none" stroke="#142339" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-8.5 8.5 8.5 8.5 0 0 1-3.8-.9L3 21l1.9-5.7a8.5 8.5 0 0 1-.9-3.8A8.38 8.38 0 0 1 12.5 3 8.38 8.38 0 0 1 21 11.5z"/></svg><span>Chat with us</span>';
  document.body.appendChild(launch);

  /* ---------- panel ---------- */
  var panel = document.createElement("div");
  panel.id = "hb-chat";
  panel.setAttribute("role", "dialog");
  panel.setAttribute("aria-label", "Honorbrook chat");
  panel.innerHTML =
    '<div class="hb-head"><div style="width:34px">' + CREST + '</div>' +
    '<div><div class="t">Brook</div><div class="s">Honorbrook Insurance · replies in seconds</div></div>' +
    '<button class="x" aria-label="Close chat">&times;</button></div>' +
    '<div class="hb-body" id="hb-body"></div>' +
    '<div class="hb-foot"><textarea id="hb-input" rows="1" placeholder="Type your question…" aria-label="Message"></textarea>' +
    '<button class="hb-send" id="hb-send" aria-label="Send">▸</button></div>' +
    '<div class="hb-disc">Brook is an automated assistant, not a licensed agent, and can\'t give specific quotes or advice. For help now, call <a href="tel:+13016158289">' + PHONE + "</a>.</div>";
  document.body.appendChild(panel);

  var bodyEl = panel.querySelector("#hb-body");
  var inputEl = panel.querySelector("#hb-input");
  var sendEl = panel.querySelector("#hb-send");
  var opened = false;

  function addMsg(text, who) {
    var d = document.createElement("div");
    d.className = "hb-msg " + (who === "user" ? "hb-user" : "hb-bot");
    d.textContent = text;
    bodyEl.appendChild(d);
    bodyEl.scrollTop = bodyEl.scrollHeight;
    return d;
  }

  function typing(on) {
    var ex = bodyEl.querySelector(".hb-typing");
    if (on && !ex) {
      var d = document.createElement("div");
      d.className = "hb-typing";
      d.textContent = "Brook is typing…";
      bodyEl.appendChild(d);
      bodyEl.scrollTop = bodyEl.scrollHeight;
    } else if (!on && ex) {
      ex.remove();
    }
  }

  function openChat() {
    panel.classList.add("open");
    launch.style.display = "none";
    if (!opened) {
      opened = true;
      addMsg(GREETING, "bot");
    }
    setTimeout(function () { inputEl.focus(); }, 80);
  }
  function closeChat() {
    panel.classList.remove("open");
    launch.style.display = "flex";
  }

  launch.addEventListener("click", openChat);
  panel.querySelector(".x").addEventListener("click", closeChat);

  inputEl.addEventListener("input", function () {
    inputEl.style.height = "auto";
    inputEl.style.height = Math.min(inputEl.scrollHeight, 90) + "px";
  });
  inputEl.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  });
  sendEl.addEventListener("click", send);

  async function send() {
    var text = inputEl.value.trim();
    if (!text || sending) return;
    sending = true;
    sendEl.disabled = true;
    inputEl.value = "";
    inputEl.style.height = "auto";
    addMsg(text, "user");
    history.push({ role: "user", content: text });
    typing(true);

    try {
      var res = await fetch(ENDPOINT, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ messages: history }),
      });
      var data = {};
      try { data = await res.json(); } catch (_) {}
      typing(false);
      if (res.ok && data && data.leadCaptured && typeof window.gtag === "function") {
        // the chat saved a lead (netlify/functions/chat.js returns leadCaptured): count it like a form lead
        try { window.gtag("event", "generate_lead", { form: "chat", page: location.pathname, line: document.body.getAttribute("data-line") || "", transport_type: "beacon" }); } catch (_) {}
      }
      if (res.ok && data && data.reply) {
        addMsg(data.reply, "bot");
        history.push({ role: "assistant", content: data.reply });
      } else {
        addMsg(
          "Thanks for reaching out! For the fastest help, please call us at " + PHONE + " or use the contact form, and a licensed agent will get right back to you.",
          "bot"
        );
      }
    } catch (e) {
      typing(false);
      addMsg(
        "I'm having trouble connecting right now. Please call us at " + PHONE + " and a licensed agent will help you right away.",
        "bot"
      );
    } finally {
      sending = false;
      sendEl.disabled = false;
      inputEl.focus();
    }
  }
})();


/* ---- GA4 conversion tracking (fires only if gtag is present on the page) ---- */
(function(){
  function track(name,params){ if(typeof window.gtag==='function'){ try{ var p=params||{}; p.transport_type='beacon'; window.gtag('event',name,p); }catch(e){} } }
  document.addEventListener('click',function(e){
    var a=e.target&&e.target.closest?e.target.closest('a[href^="tel:"]'):null;
    if(a){ track('phone_call_click',{phone:a.getAttribute('href').replace('tel:',''),line:(document.body.getAttribute('data-line')||'')}); }
  },true);
  document.addEventListener('submit',function(e){
    if(e.target&&e.target.tagName==='FORM'&&!e.target.classList.contains('hbf-contact')&&e.target.checkValidity()){ if(!/formspree\.io/.test(e.target.getAttribute('action')||'')){ track(e.target.getAttribute('data-event')||'generate_lead',{form:(e.target.getAttribute('action')||'form')}); } }
  },true);
})();

/* ---- Header button: it keeps the link written in the page (the on-page form, #quote, or the home page form).
   Until Nov 27 2026 this script sent it to the booking site instead; booking asks for a profile first, so it was removed. ---- */


/* ---- Lead forms: inline loading + error states, then /thank-you ---- */
(function(){
  function msg(form,text){
    var m=form.querySelector('.hb-form-msg');
    if(!m){ m=document.createElement('div'); m.className='hb-form-msg err'; m.setAttribute('role','alert'); m.setAttribute('aria-live','assertive'); form.appendChild(m); }
    m.textContent=text; m.hidden=!text; if(text){ m.scrollIntoView({block:'nearest'}); }
  }
  function hbLead(f){ try{ if(typeof window.gtag==='function'){ window.gtag('event',f.getAttribute('data-event')||'generate_lead',{transport_type:'beacon',page:location.pathname,form:f.getAttribute('action')||'form',line:f.getAttribute('data-line')||'',hot:!!f.querySelector('option[data-hot]:checked')}); } }catch(x){} }
  function hbAnswers(f,fd){ var skip={Name:1,Phone:1,Email:1,ZIP:1,Consent:1,Topic:1,Interests:1,_subject:1,_gotcha:1,'Best time to call':1,landing_page:1,referrer:1,utm_source:1,utm_medium:1,utm_campaign:1,gclid:1}, out=[]; fd.forEach(function(v,k){ if(!skip[k]&&v){ out.push(k+': '+v); } }); return out.join(' / '); }
  function hbBody(f){ var d=new FormData(f); try{ if(d.has('Email')&&!d.get('Email')){ d['delete']('Email'); } HB_SRC.forEach(function(k){ if(d.has(k)&&!d.get(k)){ d['delete'](k); } }); }catch(x){} return d; }
  var HB_SRC=['landing_page','referrer','utm_source','utm_medium','utm_campaign','gclid'];
  function hbOk(r){ return !!(r&&r.ok); }
  function hbNo(){ return false; }
  function hbAny(ps){ return new Promise(function(res){ var left=ps.length, any=false, done=false; function end(v){ if(!done){ done=true; res(v); } } if(!left){ end(false); return; } setTimeout(function(){ end(any); },15000); ps.forEach(function(p){ Promise.resolve(p).then(function(v){ if(v&&!any){ any=true; setTimeout(function(){ end(true); },3000); } if(--left===0){ end(any); } },function(){ if(--left===0){ end(any); } }); }); }); }
  function prep(){ document.querySelectorAll('form[action*="formspree.io"]').forEach(function(f){ f.noValidate=true; f.addEventListener('input',function(ev){ ev.target.classList&&ev.target.classList.remove('hb-field-err'); }); }); }
  if(document.readyState==='loading'){ document.addEventListener('DOMContentLoaded',prep); } else { prep(); }
  document.addEventListener('submit',function(e){
    var f=e.target;
    if(!f||f.tagName!=='FORM'||!/formspree\.io/.test(f.getAttribute('action')||'')||!window.fetch||!window.FormData) return;
    e.preventDefault();
    var how=f.querySelector('select[name="Contact preference"]'), em=f.querySelector('input[name="Email"]');
    if(how&&em&&how.value==='Email me'&&!em.value.replace(/\s/g,'')){ em.classList.add('hb-field-err'); msg(f,'Please add your email, or choose text or call.'); em.focus(); return; }
    if(!f.checkValidity()){
      var bad=f.querySelectorAll(':invalid'); bad.forEach(function(el){ el.classList.add('hb-field-err'); });
      msg(f,'Please complete the highlighted fields (and tick the consent box) so we can reach you.'); bad[0].focus(); return;
    }
    f.querySelectorAll('.hb-field-err').forEach(function(el){ el.classList.remove('hb-field-err'); });
    var sj=f.querySelector('input[name=_subject]'); if(sj){ if(!sj.hasAttribute('data-base')){ sj.setAttribute('data-base',sj.value); } var sb=sj.getAttribute('data-base'); sj.value=f.querySelector('option[data-hot]:checked')?'HOT lead: '+sb.replace(/^Quote request: /,''):sb; }
    var btn=f.querySelector('button[type=submit]'), label=btn&&btn.textContent;
    if(btn){ btn.disabled=true; btn.textContent='Sending…'; }
    msg(f,'');
    var hbTries=[];
    /* also send the lead into IntegrityCONNECT through our own server function; any one accepted post counts as sent */
    try{ var fd0=new FormData(f), nm=fd0.get('Name'), ph=fd0.get('Phone'); if(nm&&ph&&!f.hasAttribute('data-inline')){ hbTries.push(fetch('/.netlify/functions/lead',{method:'POST',keepalive:true,headers:{'Content-Type':'application/json'},body:JSON.stringify({name:nm,phone:ph,email:fd0.get('Email')||'',zip:fd0.get('ZIP')||'',best:fd0.get('Best time to call')||'',interests:fd0.getAll('Interests').join(', ')||fd0.get('Topic')||'',answers:hbAnswers(f,fd0),source:'website-form '+location.pathname,consent:!!fd0.get('Consent'),_gotcha:fd0.get('_gotcha')||''})}).then(hbOk,hbNo)); } }catch(x){}
    if(!f.hasAttribute('data-inline')&&!f.hasAttribute('data-nocopy')&&!f._hbCopied){ try{ hbTries.push(fetch('https://formspree.io/f/xljbopja',{method:'POST',body:hbBody(f),headers:{Accept:'application/json'},keepalive:true}).then(function(r){ var k=hbOk(r); if(k){ f._hbCopied=true; } return k; },hbNo)); }catch(x){} }
    hbTries.push(fetch(f.action,{method:'POST',body:hbBody(f),headers:{Accept:'application/json'},keepalive:true}).then(hbOk,hbNo));
    hbAny(hbTries)
      .then(function(ok){ if(ok){ hbLead(f); if(f.hasAttribute('data-inline')){ f.innerHTML='<p class="hb-sub-ok" role="status">Thank you &mdash; you&rsquo;re subscribed. We&rsquo;ll only email when we publish something worth your time.</p>'; try{localStorage.setItem('hb_subscribed','1');}catch(x){} } else { location.href=f.getAttribute('data-thanks')||'/thank-you'; } } else { throw new Error('bad'); } })
      .catch(function(){
        try{ if(typeof window.gtag==='function'){ window.gtag('event','lead_error',{transport_type:'beacon',line:f.getAttribute('data-line')||'',page:location.pathname}); } }catch(x){}
        if(btn){ btn.disabled=false; btn.textContent=label; }
        msg(f,'Sorry, that did not go through. Please try again, or call us at (301) 615-8289 and we will help right away.');
      });
  });
})();

/* ---- Analytics notice (opt-out stored in this browser; honored by the tag on every page) ---- */
(function(){
  var K='hb_analytics', v=null;
  try{ v=localStorage.getItem(K); }catch(e){}
  if(v) return;
  var d=document.createElement('div'); d.className='hb-consent'; d.setAttribute('role','region'); d.setAttribute('aria-label','Analytics notice');
  d.innerHTML='<p>We use cookies for analytics to improve this site. We do not sell your data. See our <a href="/privacy-policy#cookies">Privacy Policy</a>.</p><button class="ok" type="button">Accept</button><button class="no" type="button">Decline</button>';
  function set(val){ try{ localStorage.setItem(K,val); }catch(e){} if(val==='off'){ window['ga-disable-G-J5YG8E3PYC']=true; } d.remove(); }
  d.querySelector('.ok').onclick=function(){ set('on'); };
  d.querySelector('.no').onclick=function(){ set('off'); };
  document.body.appendChild(d);
})();


/* ---- Blog subscribe (inline box on blog pages + scroll popup) and consultation popup ---- */
(function(){
  var path=location.pathname.replace(/\.html$/,'').replace(/\/$/,'')||'/';
  var isBlogPost=/^\/blog\/[^\/]+/.test(path), isBlogIndex=(path==='/blog');
  var skip=/^\/(thank-you|thank-you-life|privacy-policy|terms|404|contact)$/.test(path);
  function get(k){ try{return localStorage.getItem(k);}catch(e){return null;} }
  function put(k,v){ try{localStorage.setItem(k,v);}catch(e){} }
  var CAL='https://www.planenroll.com/?purl=Luay-Sadqi';
  var SUB='<form class="hb-sub-form" action="https://formspree.io/f/xgobjlba" method="POST" data-inline data-event="blog_subscribe">'+
    '<input type="hidden" name="_subject" value="New blog subscriber — Honorbrook website">'+
    '<input type="hidden" name="Form" value="Blog subscribe">'+
    '<input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">'+
    '<label class="hb-sr" for="HBID">Email address</label>'+
    '<div class="hb-sub-row"><input id="HBID" type="email" name="Email" placeholder="Your email address" autocomplete="email" required>'+
    '<button class="btn-primary sans" type="submit">Subscribe</button></div>'+
    '<label class="hb-sub-consent"><input type="checkbox" name="Consent" value="Yes" required> <span>I agree to receive email updates from Honorbrook Insurance. Unsubscribe anytime. See our <a href="/privacy-policy">Privacy Policy</a>.</span></label></form>';
  function subBox(id,cls){
    var d=document.createElement('aside'); d.className='hb-subscribe '+(cls||''); d.setAttribute('aria-label','Subscribe to the Honorbrook blog');
    d.innerHTML='<div class="hb-sub-kicker">The Honorbrook Blog</div><h2>Plain-English Medicare &amp; insurance updates, in your inbox</h2><p>One short email when we publish something worth your time &mdash; enrollment dates, rule changes and honest explainers. No spam, no sales pressure.</p>'+SUB.replace(/HBID/g,id);
    return d;
  }
  function mountInline(){
    if(get('hb_subscribed')) return;
    if(isBlogPost){ var w=document.querySelector('article .wrap.prose')||document.querySelector('article'); if(w) w.appendChild(subBox('hb-sub-in')); }
    else if(isBlogIndex){ var h=document.querySelector('.page-hero'); if(h&&h.parentNode) h.parentNode.insertBefore(subBox('hb-sub-top','hb-sub-wide'),h.nextSibling); }
  }
  /* popup shell */
  var open=null;
  function show(html,key,days,cls){
    if(open||document.querySelector('.hb-consent')) return false;
    var ov=document.createElement('div'); ov.className='hb-pop-ov';
    ov.innerHTML='<div class="hb-pop '+(cls||'')+'" role="dialog" aria-modal="true" aria-labelledby="hbPopT"><button class="hb-pop-x" type="button" aria-label="Close">&times;</button>'+html+'</div>';
    var prev=document.activeElement;
    function close(){ ov.remove(); open=null; document.removeEventListener('keydown',esc); if(prev&&prev.focus) try{prev.focus();}catch(e){} }
    function esc(e){ if(e.key==='Escape') close(); }
    ov.addEventListener('click',function(e){ if(e.target===ov) close(); });
    ov.querySelector('.hb-pop-x').onclick=close;
    document.addEventListener('keydown',esc);
    document.body.appendChild(ov); open=ov;
    put(key,String(Date.now()+days*864e5));
    var f=ov.querySelector('input,a,button'); if(f) try{f.focus();}catch(e){}
    if(typeof window.gtag==='function'){ try{window.gtag('event','popup_shown',{popup:key});}catch(e){} }
    return true;
  }
  function due(key){ var t=parseInt(get(key)||'0',10); return !t||Date.now()>t; }
  var desktop=window.matchMedia&&window.matchMedia('(min-width:901px) and (hover:hover)').matches;
  function subPopup(){
    if(get('hb_subscribed')||!due('hb_pop_sub')) return;
    var d=document.createElement('div'); d.appendChild(subBox('hb-sub-pop','hb-sub-pop-box'));
    show(d.innerHTML.replace('<h2>','<h2 id="hbPopT">'),'hb_pop_sub',14,'hb-pop-sub');
  }
  function consultPopup(){
    if(!due('hb_pop_consult')) return;
    show('<div class="hb-sub-kicker">Free &middot; No obligation</div><h2 id="hbPopT">Not sure which plan fits? Talk to a licensed agent.</h2><p>Book a free 15&ndash;30 minute review. We&rsquo;re independent, compare 90+ carriers and our help costs you nothing.</p><p class="hb-pop-cta"><a class="btn-primary sans" href="'+CAL+'" target="_blank" rel="noopener">Book a free call</a> <a class="hb-pop-call sans" href="tel:+13016158289">or call (301) 615-8289</a></p><p class="hb-pop-fine">We do not offer every plan available in your area. For all Medicare options, visit Medicare.gov or call 1-800-MEDICARE.</p>','hb_pop_consult',7);
  }
  function arm(){
    if(skip||!desktop) return;
    var t0=Date.now(), fired=false;
    if(isBlogPost){
      window.addEventListener('scroll',function(){
        if(fired) return; var h=document.documentElement; var p=(h.scrollTop+innerHeight)/h.scrollHeight;
        if(p>0.6 && Date.now()-t0>20000){ fired=true; subPopup(); }
      },{passive:true});
    } else {
      document.addEventListener('mouseout',function(e){
        if(fired||e.relatedTarget||e.clientY>0||Date.now()-t0<15000) return; fired=true; consultPopup();
      });
    }
  }
  function init(){ mountInline(); arm(); }
  if(document.readyState==='loading'){ document.addEventListener('DOMContentLoaded',init); } else { init(); }
})();


/* ---- Lead source and conversion events (Nov 27 2026) ----
   Every lead form (Formspree) gets hidden fields: landing_page, referrer, utm_source, utm_medium, utm_campaign, gclid.
   The first page of the visit and its referrer are kept for this browser tab only (sessionStorage); campaign tags in the
   current address replace the stored ones. Empty fields are left out of the posts.
   Events (sent with transport_type beacon, so they are not lost when the page changes): form_start (first focus in a
   lead form), phone_click (tel: links), text_click (sms: links), schedule_click (scheduling page or booking site). */
(function(){
  var KEYS=['landing_page','referrer','utm_source','utm_medium','utm_campaign','gclid'], SK='hb_attr';
  function qs(k){ var m=new RegExp('[?&]'+k+'=([^&#]*)').exec(location.search); if(!m) return ''; try{ return decodeURIComponent(m[1].replace(/\+/g,' ')); }catch(x){ return m[1]; } }
  function cut(v){ return String(v||'').slice(0,300); }
  var a=null;
  try{ a=JSON.parse(sessionStorage.getItem(SK)||'null'); }catch(x){ a=null; }
  if(!a||typeof a!=='object'){ a={landing_page:cut(location.href.split('#')[0]),referrer:cut(document.referrer)}; }
  var tagged=false; ['utm_source','utm_medium','utm_campaign','gclid'].forEach(function(k){ if(qs(k)){ tagged=true; } });
  if(tagged){ ['utm_source','utm_medium','utm_campaign','gclid'].forEach(function(k){ a[k]=cut(qs(k)); }); }
  try{ sessionStorage.setItem(SK,JSON.stringify(a)); }catch(x){}
  /* newsletter sign-ups (data-inline) are not lead forms: no source fields, no form_start */
  function lead(f){ return !!(f&&f.tagName==='FORM'&&/formspree\.io/.test(f.getAttribute('action')||'')&&!f.hasAttribute('data-inline')); }
  function fill(f){
    if(!lead(f)) return;
    KEYS.forEach(function(k){
      var el=f.querySelector('input[name="'+k+'"]');
      if(!el){ el=document.createElement('input'); el.type='hidden'; el.name=k; f.appendChild(el); }
      el.value=a[k]||'';
    });
  }
  function fillAll(){ [].forEach.call(document.querySelectorAll('form[action*="formspree.io"]'),fill); }
  if(document.readyState==='loading'){ document.addEventListener('DOMContentLoaded',fillAll); } else { fillAll(); }
  /* capture phase: runs before the lead form handler reads the form */
  document.addEventListener('submit',function(e){ fill(e.target); },true);

  function ev(name,p){
    if(typeof window.gtag!=='function') return;
    p=p||{}; p.page=location.pathname; p.line=(document.body&&document.body.getAttribute('data-line'))||''; p.transport_type='beacon';
    try{ window.gtag('event',name,p); }catch(x){}
  }
  document.addEventListener('focusin',function(e){
    var f=e.target&&e.target.form;
    if(!lead(f)||f._hbStarted) return;
    f._hbStarted=true;
    ev('form_start',{form:f.getAttribute('data-line')||f.getAttribute('data-event')||'form'});
  },true);
  function place(el){ return el.closest('.sticky-call')?'bottom bar':el.closest('.hero-ctas,.hb-hero-alt,.hb-callback-m')?'hero':el.closest('nav.menu')?'menu':el.closest('header')?'header':el.closest('footer')?'footer':el.closest('.hb-next')?'post next step':el.closest('#hb-chat')?'chat':'page'; }
  document.addEventListener('click',function(e){
    var el=e.target&&e.target.closest?e.target.closest('a[href]'):null;
    if(!el) return;
    var h=el.getAttribute('href')||'';
    if(/^tel:/i.test(h)){ ev('phone_click',{place:place(el)}); }
    else if(/^sms:/i.test(h)){ ev('text_click',{place:place(el)}); }
    else if(/^\/schedule-an-appointment(\.html)?([?#]|$)/.test(h)||/planenroll\.com/.test(h)){ ev('schedule_click',{place:place(el),to:/planenroll\.com/.test(h)?'booking site':'scheduling page'}); }
  },true);
})();

/* ---- /thank-you-life: show the meeting type and the "have this ready" line for the form that was sent ---- */
(function(){
  if(!/^\/thank-you-life/.test(location.pathname)) return;
  function go(){
    var t=(location.search.match(/[?&]t=([a-z_]+)/)||[])[1]||'', m=document.getElementById('hbMeet'), l=document.getElementById('hbReady');
    if(m&&t==='annuity'){ m.textContent='Annuities'; }
    if(l&&t){ var hit=l.querySelector('[data-t="'+t+'"]'); if(hit){ [].forEach.call(l.children,function(li){ if(li!==hit){ li.hidden=true; } }); } }
    if(t){ document.body.setAttribute('data-line',t); }
  }
  if(document.readyState==='loading'){ document.addEventListener('DOMContentLoaded',go); } else { go(); }
})();
