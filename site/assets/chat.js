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
  var PHONE = "(571) 354-0146";
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

  var CREST =
    '<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><defs><linearGradient id="hbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e3c25c"/><stop offset="1" stop-color="#c9a227"/></linearGradient></defs><path d="M100 14 L182 44 L182 118 C182 186 148 214 100 232 C52 214 18 186 18 118 L18 44 Z" fill="#1b2f4b"/><g fill="url(#hbg)"><rect x="71" y="80" width="14" height="70"/><rect x="64" y="80" width="28" height="7"/><rect x="64" y="143" width="28" height="7"/><rect x="115" y="80" width="14" height="70"/><rect x="108" y="80" width="28" height="7"/><rect x="108" y="143" width="28" height="7"/><rect x="83" y="108" width="34" height="13"/></g></svg>';

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
    '<div class="hb-disc">Brook is an automated assistant, not a licensed agent, and can\'t give specific quotes or advice. For help now, call <a href="tel:+15713540146">' + PHONE + "</a>.</div>";
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
  function track(name,params){ if(typeof window.gtag==='function'){ try{ window.gtag('event',name,params||{}); }catch(e){} } }
  document.addEventListener('click',function(e){
    var a=e.target&&e.target.closest?e.target.closest('a[href^="tel:"]'):null;
    if(a){ track('phone_call_click',{phone:a.getAttribute('href').replace('tel:','')}); }
  },true);
  document.addEventListener('submit',function(e){
    if(e.target&&e.target.tagName==='FORM'){ track('generate_lead',{form:(e.target.getAttribute('action')||'form')}); }
  },true);
})();
