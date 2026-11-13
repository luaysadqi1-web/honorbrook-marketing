/* Honorbrook Insurance: website lead -> IntegrityCONNECT (Leads Partner API).
   The credential never reaches the browser. It is read from the host's environment variables:
   INTEGRITY_CLIENT_ID, INTEGRITY_CLIENT_SECRET, optional INTEGRITY_AGENT_NPN and INTEGRITY_API_BASE.
   No SSN, Medicare number or health details are accepted or forwarded. */

const BASE = (process.env.INTEGRITY_API_BASE || "https://ae-api.integrity.com").replace(/\/$/, "");
const TOKEN_URL = BASE + "/ae-partner-auth-service/auth/token";
const LEADS_URL = BASE + "/ae-partner-gateway-service/partners/leads";
const ALLOWED_ORIGINS = ["https://honorbrook-insurance.com", "https://www.honorbrook-insurance.com"];

const clean = (v, max) => String(v == null ? "" : v).replace(/[\u0000-\u001f<>]/g, " ").trim().slice(0, max);

function reply(status, body, origin) {
  const allow = ALLOWED_ORIGINS.includes(origin) || /^http:\/\/localhost(:\d+)?$/.test(origin || "") ? origin : ALLOWED_ORIGINS[0];
  return {
    statusCode: status,
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": allow, "Access-Control-Allow-Headers": "Content-Type", "Vary": "Origin" },
    body: JSON.stringify(body),
  };
}

exports.handler = async (event) => {
  const origin = (event.headers && (event.headers.origin || event.headers.Origin)) || "";
  if (event.httpMethod === "OPTIONS") return reply(204, {}, origin);
  if (event.httpMethod !== "POST") return reply(405, { ok: false, error: "POST only" }, origin);

  const id = process.env.INTEGRITY_CLIENT_ID, secret = process.env.INTEGRITY_CLIENT_SECRET;
  if (!id || !secret) return reply(503, { ok: false, error: "not configured" }, origin);

  let d;
  try { d = JSON.parse(event.body || "{}"); } catch (e) { return reply(400, { ok: false, error: "bad json" }, origin); }
  if (d._gotcha) return reply(200, { ok: true }, origin);
  if (d.consent !== true) return reply(400, { ok: false, error: "consent required" }, origin);

  const name = clean(d.name, 80), phone = String(d.phone || "").replace(/\D/g, "").slice(-10), zip = clean(d.zip, 5);
  const email = clean(d.email, 120);
  if (!name || phone.length !== 10 || !/^\d{5}$/.test(zip)) return reply(400, { ok: false, error: "name, 10-digit phone and ZIP are required" }, origin);

  const parts = name.split(/\s+/), firstName = parts.shift(), lastName = parts.join(" ") || "(not given)";
  const notes = clean(
    "Website funnel lead. ZIP " + zip + ". Interests: " + clean(d.interests, 300) +
    ". Best time to call: " + clean(d.best, 40) +
    (d.answers ? ". Answers: " + clean(d.answers, 1200) : "") +
    ". Source: " + clean(d.source, 60) + ". Consent to contact: yes.", 1900);

  const lead = {
    agentNpn: process.env.INTEGRITY_AGENT_NPN || "21370662",
    firstName, lastName,
    primaryCommunication: "Phone",
    notes,
    phones: [{ phoneNumber: phone }],
    addresses: [{ postalCode: zip }],
  };
  if (/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) lead.emails = [{ email }];

  try {
    const t = await fetch(TOKEN_URL, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ client_id: id, client_secret: secret }) });
    if (!t.ok) return reply(502, { ok: false, error: "auth failed", status: t.status }, origin);
    const token = (await t.json()).access_token;
    const base = { agentNpn: lead.agentNpn, firstName, lastName, notes, phones: lead.phones };
    if (lead.emails) base.emails = lead.emails;
    const variants = [base, { firstName, lastName, notes, phones: lead.phones }];
    const tried = [];
    for (let i = 0; i < variants.length; i++) {
      const r = await fetch(LEADS_URL, {
        method: "POST",
        headers: { "Authorization": "Bearer " + token, "Content-Type": "application/json" },
        body: JSON.stringify({ options: { forceValidation: false }, lead: variants[i] }),
      });
      if (r.status === 409) return reply(200, { ok: true, duplicate: true }, origin);
      const body = r.ok ? "" : await r.text().catch(() => "");
      if (r.status === 422 && /duplicate/i.test(body)) return reply(200, { ok: true, duplicate: true }, origin);
      if (r.ok) { const out = await r.json().catch(() => ({})); return reply(200, { ok: true, leadId: out.leadId || out.leadsId || null, variant: i }, origin); }
      tried.push({ variant: i, status: r.status, detail: body.slice(0, 300) });
      if (r.status === 401 || r.status === 403) break;
    }
    return reply(502, { ok: false, error: "lead not created", tried }, origin);
  } catch (e) {
    return reply(502, { ok: false, error: "integrity unreachable" }, origin);
  }
};
