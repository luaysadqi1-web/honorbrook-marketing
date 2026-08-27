# Honorbrook social — pillar calendar

The generator picks the pillar by day of week, then writes one X post and one
LinkedIn post against it. Reddit drafts are produced separately (see the spec).

| Day | Pillar | Angle | Primary platform |
|---|---|---|---|
| Mon | `medicare-foundations` | Enrollment windows, penalties, how the parts fit | X |
| Tue | `ichra-employer` | ICHRA, SHOP, small-group — the biggest content gap | **LinkedIn** |
| Wed | `aca-under65` | Marketplace, subsidies, SEPs, self-employed | X |
| Thu | `life-final-expense` | Final expense, term/whole, annuities. Calm, never morbid | X |
| Fri | `local-nova` | Fairfax/Arlington/Tysons, networks, Inova & VHC, local facts | X |
| Sat | `you-asked` | One real question we actually get, answered plainly | X |
| Sun | `trust-brand` | Independence, how we're paid, why we say "keep what you have" | LinkedIn |

Every day also gets a **Google Business Profile** post on the same pillar. GBP is
a different job from X or LinkedIn: the reader is looking at your profile with
intent *right now*. Front-load the offer, keep it concrete and local, and let the
CALL button be the action. Only the first ~200 characters show before "Read
more", so the first sentence has to carry it. 300–450 characters of content is
the sweet spot; the cap is 1500 including the disclaimer.

## Seasonal override

**Oct 15 – Dec 7 (Medicare AEP):** override Mon/Wed/Fri to AEP topics — what can
change, drug-list review, network re-checks, the Dec 7 deadline. This is the
agency's highest-intent window of the year. Tue and Sun keep their pillars so the
employer and brand lines do not go dark.

**Nov 1 – Jan 15 (ACA Open Enrollment):** Wed shifts to Marketplace deadlines.

**Jan 1 – Mar 31 (Medicare Advantage Open Enrollment):** Mon covers the
MA-to-MA / MA-to-Original switch window.

## Topic bank

Draw from these, and never repeat a topic within 60 days (check `logs/posted-log.csv`).

**medicare-foundations** — IEP vs GEP vs SEP · Part B late penalty math · working
past 65 and employer size · Medigap open enrollment and the medical-underwriting
cliff after it · what Original Medicare does not cover · Part D and the drug
list changing every year · SEPs for moving.

**ichra-employer** — what an ICHRA is · ICHRA vs group cost logic · employee
classes · setting an allowance · SHOP and the small-business tax credit · what
happens to coverage when an employee leaves · why participation minimums matter.

**aca-under65** — the 60-day SEP after losing coverage · COBRA vs Marketplace ·
how subsidies key off household income · metal tiers and total cost vs premium ·
self-employed coverage · income changes mid-year.

**life-final-expense** — level vs graded benefit · whether premiums can rise ·
how much coverage is actually needed · no-exam policies · term vs whole ·
annuities and what they are not.

**local-nova** — county-by-county network differences · Inova, VHC Health,
Reston Hospital Center · pharmacy networks · the ten NoVA city pages ·
seasonal local events.

**you-asked** — does an agent cost anything · whose side are you on · can I keep
my doctor · what if I already have a plan I like · do I have to switch every year.

**trust-brand** — independence · NPN 21370662 · licensed in 11 states · the
Tysons office · why we tell people to keep what they have.

## Hard rules for every draft

1. Medicare-topic posts on X have a **193-character content budget** — the
   86-character disclaimer is appended automatically. Write to the budget.
   On LinkedIn and GBP the *full* disclaimer is appended instead; there is room.
2. Never name a carrier. Never name a premium, copay, deductible, or "$0".
3. No superlatives, no guarantees, no urgency language.
4. No invented statistics. If a number cannot be cited, do not use it.
5. No testimonials unless they are real, documented, and consented.
6. Invite an inbound call; never promise an outbound one.
