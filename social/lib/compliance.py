"""
Honorbrook Insurance - social post compliance linter.

Runs in-process before EVERY automated post. A draft that trips a BLOCK rule is
held in the queue and never published; WARN rules are logged but allowed.

Rule sources:
  - CMS Medicare Communications & Marketing Guidelines (MCMG). The key line the
    agency must not cross: generic *educational* content is a "communication";
    the moment a post names plan benefits, premiums, cost sharing, star ratings
    or a specific carrier plan, it becomes "marketing" -- which requires the
    standardized disclaimer and, for plan-specific material, HPMS submission.
    An unattended bot must therefore never produce the second category.
  - TCPA: no solicitation of contact without prior express consent; posts may
    invite an inbound call, never promise outbound contact.
  - FTC + state DOI advertising rules: no unsubstantiated superlatives, no
    fabricated testimonials, licensed entity must be identifiable.

Zero dependencies (stdlib only) so this can run from launchd without a venv.
"""

import re

# The standardized CMS disclaimer, current CY2024+ wording, and the short form
# used where a 280-character limit makes the long form impossible.
DISCLAIMER_LONG = (
    "We do not offer every plan available in your area. Any information we "
    "provide is limited to those plans we do offer in your area. Please "
    "contact Medicare.gov or 1-800-MEDICARE to get information on all of "
    "your options."
)
DISCLAIMER_SHORT = (
    "Not connected with or endorsed by the U.S. government or the federal "
    "Medicare program."
)

# Words that mark a post as Medicare-topic, which triggers the disclaimer
# requirement below.
MEDICARE_TERMS = re.compile(
    r"\b(medicare|medigap|medicare\s+advantage|part\s*[abcd]\b|pdp\b|"
    r"annual\s+enrollment|aep\b|open\s+enrollment|turning\s*65|"
    r"supplement\s+plan|dual\s+eligible|d-?snp)\b",
    re.I,
)

# --- BLOCK rules: these hold the post ---------------------------------------
# Each entry: (rule id, compiled pattern, human explanation)
BLOCK_RULES = [
    (
        "CMS-BENEFIT-CLAIM",
        re.compile(
            r"(\$\s?0\s*(premium|plan|cost|deductible)|zero[- ]premium|"
            r"free\s+(plan|coverage|insurance)\b|"
            r"\$\d[\d,.]*\s*(/|per\s+)?(mo\b|month|year|yr\b|premium|copay|"
            r"deductible))",
            re.I,
        ),
        "Names a premium, cost-sharing amount or $0/free benefit. Under CMS "
        "rules this converts the post from a communication into plan marketing, "
        "which requires the full disclaimer and HPMS filing.",
    ),
    (
        "CMS-GOV-AFFILIATION",
        re.compile(
            r"(official\s+medicare|medicare\s+official|"
            r"we\s+are\s+(with|from|part\s+of)\s+medicare|"
            r"government[- ]approved|"
            r"authorized\s+by\s+(medicare|cms|the\s+government)|"
            r"on\s+behalf\s+of\s+(medicare|cms))",
            re.I,
        ),
        "Implies government or CMS affiliation/endorsement. Prohibited outright "
        "by CMS; also a state DOI misrepresentation issue.",
    ),
    (
        "CARRIER-PLAN-SPECIFIC",
        re.compile(
            r"\b(aetna|humana|unitedhealthcare|uhc|anthem|elevance|cigna|"
            r"wellcare|kaiser|devoted|clover|alignment|blue\s+cross|bcbs|"
            r"mutual\s+of\s+omaha|silverscript)\b",
            re.I,
        ),
        "Names a specific carrier. Carrier/plan-specific social content is "
        "marketing material requiring carrier and CMS review before use.",
    ),
    (
        "SUPERLATIVE-CLAIM",
        re.compile(
            r"\b(best\s+(plan|coverage|policy|rate)|cheapest|lowest\s+price|"
            r"#\s?1\b|number\s+one\b|guaranteed?\s+(savings|approval|"
            r"acceptance|rate)|save\s+(you\s+)?thousands|"
            r"unbeatable|no\s+one\s+else)\b",
            re.I,
        ),
        "Unsubstantiated superlative or guarantee. FTC and state DOI "
        "advertising rules prohibit these without substantiation on file.",
    ),
    (
        "HIGH-PRESSURE",
        re.compile(
            r"(act\s+now|limited\s+time|don'?t\s+miss\s+out|last\s+chance|"
            r"hurry\b|only\s+\d+\s+(spots|days)\s+left|expires\s+(today|"
            r"tonight)|call\s+immediately)",
            re.I,
        ),
        "High-pressure sales language. CMS explicitly prohibits pressure "
        "tactics in Medicare marketing.",
    ),
    (
        "PHI-SOLICITATION",
        re.compile(
            r"(send\s+(us\s+)?your\s+(medicare|social\s+security|ssn|"
            r"member\s+id)|"
            r"\b(dm|message|comment)\s+(us\s+)?your\s+"
            r"(medicare\s+number|ssn|social|date\s+of\s+birth|dob)|"
            r"reply\s+with\s+your\s+(medicare|ssn|social))",
            re.I,
        ),
        "Solicits protected health information or identifiers over a public or "
        "unsecured channel. HIPAA/PII exposure.",
    ),
    (
        "FABRICATED-TESTIMONIAL",
        re.compile(
            r"[\"“][^\"”]{15,}[\"”]\s*[-—]\s*"
            r"[A-Z][a-z]+(\s+(&|and)\s+[A-Z][a-z]+)?\s*[A-Z]?[a-z]*\.?,?\s*"
            r"(VA|MD|GA|TX|MI|NC|SC|AL|LA|IN|WV)\b"
        ),
        "Looks like an attributed client testimonial. Only real, documented, "
        "consented client quotes may be published -- never generated ones.",
    ),
    (
        "OUTBOUND-CONTACT-PROMISE",
        re.compile(
            r"(we'?ll\s+call\s+you|we\s+will\s+call\s+you|"
            r"expect\s+a\s+call\s+from\s+us|our\s+agent\s+will\s+reach\s+out)",
            re.I,
        ),
        "Promises outbound contact. TCPA requires prior express written consent "
        "before an agency initiates contact; a public post cannot capture it.",
    ),
]

# --- WARN rules: logged, post still goes out --------------------------------
WARN_RULES = [
    (
        "NO-CTA",
        lambda t: not re.search(r"(571\)?\s*354-0146|honorbrook-insurance\.com)", t, re.I),
        "No phone number or website in the post -- weaker conversion path.",
    ),
    (
        "HASHTAG-STUFFING",
        lambda t: len(re.findall(r"#\w+", t)) > 6,
        "More than 6 hashtags; most platforms downweight hashtag stuffing.",
    ),
    (
        "ALL-CAPS-SHOUT",
        lambda t: len(re.findall(r"\b[A-Z]{5,}\b", t)) > 2,
        "Several all-caps words; reads as shouty and can trip spam filters.",
    ),
]

PLATFORM_LIMITS = {"x": 280, "linkedin": 3000, "reddit": 40000}

# On X the short disclaimer costs 96 characters, so a Medicare-topic post has
# only this much room left for actual content. The generator writes to this
# budget; fit_x() below assembles the final string.
X_CONTENT_BUDGET = PLATFORM_LIMITS["x"] - len(DISCLAIMER_SHORT) - 1


def fit_x(content):
    """Append the short disclaimer to X content when the topic requires it.

    Returns (text, ok). ok is False when the result cannot fit in 280 chars,
    which means the content needs to be shortened before it can be published.
    """
    content = content.strip()
    if not is_medicare_topic(content) or has_disclaimer(content):
        return content, len(content) <= PLATFORM_LIMITS["x"]
    text = content + " " + DISCLAIMER_SHORT
    return text, len(text) <= PLATFORM_LIMITS["x"]


class Result:
    """Outcome of linting one draft."""

    def __init__(self, ok, blocks, warns):
        self.ok = ok
        self.blocks = blocks
        self.warns = warns

    def summary(self):
        if self.ok:
            base = "PASS"
        else:
            base = "HOLD"
        parts = [base]
        for rid, why in self.blocks:
            parts.append("  BLOCK %s: %s" % (rid, why))
        for rid, why in self.warns:
            parts.append("  warn  %s: %s" % (rid, why))
        return "\n".join(parts)

    def as_dict(self):
        return {
            "ok": self.ok,
            "blocks": [{"rule": r, "why": w} for r, w in self.blocks],
            "warns": [{"rule": r, "why": w} for r, w in self.warns],
        }


def is_medicare_topic(text):
    return bool(MEDICARE_TERMS.search(text))


def has_disclaimer(text):
    """True if either the long or an acceptable short disclaimer is present."""
    norm = re.sub(r"\s+", " ", text).lower()
    if "we do not offer every plan available in your area" in norm:
        return True
    if "not connected with or endorsed by the u.s. government" in norm:
        return True
    if "not affiliated with or endorsed by the u.s. government" in norm:
        return True
    return False


def check(text, platform):
    """Lint one draft. Returns a Result; .ok False means do not publish."""
    blocks = []
    warns = []

    if not text or not text.strip():
        blocks.append(("EMPTY", "Draft is empty."))
        return Result(False, blocks, warns)

    limit = PLATFORM_LIMITS.get(platform)
    if limit and len(text) > limit:
        blocks.append(
            (
                "LENGTH",
                "Post is %d characters; %s allows %d."
                % (len(text), platform, limit),
            )
        )

    for rule_id, pattern, why in BLOCK_RULES:
        if pattern.search(text):
            blocks.append((rule_id, why))

    # Medicare-topic posts must carry a disclaimer. On X the long form will not
    # fit alongside real content, so the short form is accepted there.
    if is_medicare_topic(text) and not has_disclaimer(text):
        blocks.append(
            (
                "CMS-MISSING-DISCLAIMER",
                "Medicare-topic post with no disclaimer. Append: \"%s\""
                % (DISCLAIMER_SHORT if platform == "x" else DISCLAIMER_LONG),
            )
        )

    for rule_id, fn, why in WARN_RULES:
        try:
            if fn(text):
                warns.append((rule_id, why))
        except Exception:
            pass

    return Result(len(blocks) == 0, blocks, warns)


if __name__ == "__main__":
    import sys

    platform = sys.argv[1] if len(sys.argv) > 1 else "x"
    body = sys.stdin.read()
    res = check(body, platform)
    print(res.summary())
    sys.exit(0 if res.ok else 1)
