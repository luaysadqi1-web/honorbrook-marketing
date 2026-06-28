/* ==========================================================================
   Honorbrook Insurance — chatbot serverless function (Netlify)
   Runs Claude with a Honorbrook "brain" + lead-capture tool.
   Your Anthropic API key NEVER reaches the browser — it lives in the
   ANTHROPIC_API_KEY environment variable on Netlify.
   ========================================================================== */

const MODEL = process.env.CHAT_MODEL || "claude-haiku-4-5-20251001";
const LEAD_ENDPOINT = process.env.LEAD_ENDPOINT || "https://formspree.io/f/xgobjlba";
const MAX_TURNS = 24;          // hard cap on conversation length
const MAX_CHARS = 1500;        // hard cap per user message

const SYSTEM_PROMPT = `You are "Brook," the friendly virtual assistant for Honorbrook Insurance, an independent insurance agency (a trade name of Luay's Lifeline Inc.). Licensed agent: Luay Sadqi, NPN 21370662. Phone: (571) 354-0146. Email: info@honorbrook-insurance.com. Office: Vienna, VA. Hours: Mon–Fri 9am–6pm ET, evenings/weekends by appointment. Licensed in 12 states: Virginia, Maryland, Georgia, Texas, Michigan, North Carolina, South Carolina, Alabama, Louisiana, Indiana, and West Virginia.

WHAT HONORBROOK OFFERS:
- Medicare: Medicare Advantage (Part C), Medicare Supplement (Medigap, Plan G & N), Part D drug plans.
- Senior add-ons: hospital indemnity, cancer/critical illness, dental-vision-hearing, short-term/home care.
- Final expense / burial whole life (no exam, ages 45–85), and broader life insurance (term, whole).
- Under-65 & business: ICHRA, ACA marketplace plans (with subsidy checks), and group/SHOP small-business health (SHOP-certified).

YOUR JOB:
1. Answer questions in plain English — warm, patient, honest, never pushy. Keep replies SHORT (2–5 sentences; this is a chat window).
2. Help the visitor figure out which coverage fits, then offer a FREE, no-pressure callback from a licensed agent.
3. Capture a lead when the visitor wants help — but ONLY with their explicit consent (see rules).

HARD COMPLIANCE RULES (never break these):
- You are NOT a licensed agent and you do NOT give binding advice, quotes, specific plan recommendations, or enroll anyone. For anything specific, say a licensed agent will help and offer the callback.
- Honorbrook is NOT connected with or endorsed by Medicare or any government agency. If relevant, note "we don't offer every plan available in your area."
- NEVER collect or ask for sensitive data in chat: no Social Security numbers, Medicare/Medicaid ID numbers, full dates of birth, bank/financial info, or detailed health history. Just first name, phone, and what they need.
- Before capturing a phone number for follow-up, show this consent line and get a clear "yes": "Just to confirm — is it OK for a licensed Honorbrook agent to call or text you about insurance at this number? Standard message/data rates may apply; you can reply STOP anytime. (Consent isn't required to get information.)"
- Only call the capture_lead tool AFTER the visitor clearly consents (consent=true). Never set consent=true unless they actually said yes.
- If someone is in distress, confused, or it's an emergency, gently steer them to call (571) 354-0146 or, for emergencies, 911.

LEAD FLOW: When a visitor wants a callback or a quote, collect (a) first name, (b) best phone number, (c) what they're interested in, then show the consent line, and when they say yes, call capture_lead. After it succeeds, warmly confirm a licensed agent will reach out within one business day and give the phone number for anything urgent.

Always be the kind, trustworthy face of a small family agency. When unsure, offer the callback.`;

const TOOLS = [
  {
    name: "capture_lead",
    description:
      "Save a lead so a licensed Honorbrook agent can follow up. Only call this AFTER the visitor has explicitly consented to being contacted by phone/text.",
    input_schema: {
      type: "object",
      properties: {
        first_name: { type: "string", description: "Visitor's first name" },
        phone: { type: "string", description: "Best callback phone number" },
        interest: {
          type: "string",
          description:
            "What they want help with, e.g. 'Medicare Advantage', 'ICHRA for my business', 'final expense', 'ACA under 65'",
        },
        notes: {
          type: "string",
          description: "Short context from the conversation (no sensitive data)",
        },
        consent: {
          type: "boolean",
          description: "True only if the visitor explicitly agreed to be contacted by phone/text",
        },
      },
      required: ["first_name", "phone", "interest", "consent"],
    },
  },
];

async function callAnthropic(messages) {
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": process.env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: 700,
      system: SYSTEM_PROMPT,
      tools: TOOLS,
      messages,
    }),
  });
  if (!res.ok) {
    const t = await res.text();
    throw new Error(`Anthropic ${res.status}: ${t}`);
  }
  return res.json();
}

async function forwardLead(lead) {
  try {
    await fetch(LEAD_ENDPOINT, {
      method: "POST",
      headers: { "content-type": "application/json", accept: "application/json" },
      body: JSON.stringify({
        _subject: "🔵 New CHATBOT lead — Honorbrook website",
        Source: "Website chatbot (Brook)",
        Name: lead.first_name,
        Phone: lead.phone,
        Interest: lead.interest,
        Notes: lead.notes || "",
        Consent: lead.consent ? "Yes — agreed to phone/text" : "No",
      }),
    });
    return true;
  } catch (e) {
    return false;
  }
}

function textFrom(content) {
  return (content || [])
    .filter((b) => b.type === "text")
    .map((b) => b.text)
    .join("\n")
    .trim();
}

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }
  if (!process.env.ANTHROPIC_API_KEY) {
    return json(500, { error: "Server not configured. Please call (571) 354-0146." });
  }

  let body;
  try {
    body = JSON.parse(event.body || "{}");
  } catch {
    return json(400, { error: "Bad request." });
  }

  let messages = Array.isArray(body.messages) ? body.messages : [];
  // basic guards
  messages = messages.slice(-MAX_TURNS);
  for (const m of messages) {
    if (typeof m.content === "string" && m.content.length > MAX_CHARS) {
      m.content = m.content.slice(0, MAX_CHARS);
    }
  }

  try {
    let resp = await callAnthropic(messages);
    let leadCaptured = false;

    // handle one round of tool use (capture_lead)
    if (resp.stop_reason === "tool_use") {
      const toolUse = resp.content.find((b) => b.type === "tool_use" && b.name === "capture_lead");
      if (toolUse) {
        const ok = toolUse.input.consent ? await forwardLead(toolUse.input) : false;
        leadCaptured = ok;
        messages.push({ role: "assistant", content: resp.content });
        messages.push({
          role: "user",
          content: [
            {
              type: "tool_result",
              tool_use_id: toolUse.id,
              content: ok
                ? "Lead saved successfully. A licensed agent will follow up within one business day."
                : "Could not save the lead. Ask the visitor to call (571) 354-0146.",
            },
          ],
        });
        resp = await callAnthropic(messages);
      }
    }

    return json(200, { reply: textFrom(resp.content) || "Thanks! How else can I help?", leadCaptured });
  } catch (e) {
    return json(200, {
      reply:
        "I'm having a little trouble right now — please call us at (571) 354-0146 and a licensed agent will help you right away.",
      error: true,
    });
  }
};

function json(statusCode, obj) {
  return {
    statusCode,
    headers: { "content-type": "application/json" },
    body: JSON.stringify(obj),
  };
}
