# BBB Listing — corrections to submit

**Live profile:** https://www.bbb.org/us/va/vienna/profile/insurance-agency/honorbrook-insurance-0241-236109068

**Current state (verified 2026-09-20):**

| Field | What BBB shows now |
|---|---|
| Name | Honorbrook Insurance |
| Address | 8609 Westwood Center Dr Ste 110, **Vienna**, VA 22182-7525 |
| Phone | (571) 354-0146 |
| Website | **missing** |
| Category | Insurance Agency |
| Owner | "Ms. Luay Sadqi" |
| Accreditation | Not accredited |
| Rating | A |
| Founded | November 6, 2024 |
| Reviews | 0 |
| Hours | none listed |

**The one that costs you the most: no website link.** A BBB profile with no URL is a
citation that passes zero link value and gives a searcher no way to reach you. This is
the single highest-value fix on the listing.

---

## Field-by-field values to submit

Log in at bbb.org, find "Update your business profile" on the profile page, and submit:

**Website**
```
https://honorbrook-insurance.com
```
(no `www.` — the www version 301-redirects, and the site's canonicals are all non-www)

**Business hours**
```
Monday      8:00 AM - 8:00 PM
Tuesday     8:00 AM - 8:00 PM
Wednesday   8:00 AM - 8:00 PM
Thursday    8:00 AM - 8:00 PM
Friday      8:00 AM - 8:00 PM
Saturday    9:00 AM - 2:30 PM
Sunday      9:00 AM - 2:30 PM
```
These match the `openingHoursSpecification` in the site's schema. Keep them identical —
mismatched hours between your site, GBP, and BBB is a real inconsistency signal.

**Primary category:** Insurance Agency (already correct — leave it)

**Additional categories** (add if BBB allows multiples):
```
Insurance Broker
Health Insurance
Life Insurance
Medicare Insurance
```

**Business description** (BBB usually allows ~250 words; this is written to match the
site's voice and the products you actually sell):
```
Honorbrook Insurance is an independent insurance agency helping families compare
Medicare, health, life, and retirement coverage from more than 90 carriers. We work
with people at every age — not only those on Medicare — including Medicare Advantage,
Medicare Supplement (Medigap), and Part D; final expense and life insurance; ICHRA and
small-group/SHOP coverage for employers; ACA health plans for people under 65; and
dental, vision, and hearing plans.

Our guidance is free. We are paid by the carriers, never by you, and we are not owned
by any one insurance company — so our job is finding the right fit and staying with you
after you enroll, through claims questions, card issues, and annual plan reviews.

Licensed in Virginia, Maryland, West Virginia, Georgia, North Carolina, South Carolina,
Texas, Louisiana, Alabama, Michigan, and Indiana. Office in Northern Virginia by
appointment; most clients prefer to handle everything by phone.

Agent: Luay Sadqi, NPN 21370662. Honorbrook Insurance is a DBA of Luay's Lifeline Inc.
```

**Service area:** list all 11 licensed states —
```
Virginia, Maryland, West Virginia, Georgia, North Carolina, South Carolina,
Texas, Louisiana, Alabama, Michigan, Indiana
```

**Social profiles** (if BBB offers the fields):
```
https://www.facebook.com/HonorbrookInsurance
https://www.instagram.com/honorbrookinsurance
https://www.linkedin.com/company/honorbrook-insurance
https://www.youtube.com/@luaysadqi5069
https://www.tiktok.com/@honorbrookinsurance
```

---

## Confirmed: the city is TYSONS

Verified on the Google Business Profile (2026-09-20), which shows:

```
8609 Westwood Center Dr #110, Tysons, VA 22182
```

GBP is the anchor, so **Tysons is correct and the website is already right**. BBB is the
outlier. Submit this address change along with everything above:

```
From:  8609 Westwood Center Dr Ste 110, Vienna, VA 22182
To:    8609 Westwood Center Dr, Suite 110, Tysons, VA 22182
```

One more thing to confirm yourself: BBB lists the owner as **"Ms. Luay Sadqi."** The agent
name should read identically across BBB, GBP, and NIPR — correct it in the same submission
if it should be different.

---

## Also worth doing on BBB

- **Accreditation is optional and paid.** The free listing is what provides the citation;
  accreditation mainly buys the seal and higher placement in BBB's own directory. For a
  Medicare/senior audience the trust seal has some real value, but it is not an SEO
  requirement. Your rating is already A.
- **You have 0 customer reviews.** BBB reviews are a separate pool from Google reviews.
  Once the Google review funnel at `/reviews` is producing, it's reasonable to ask a
  handful of clients for a BBB review as well. Same rule applies — ask everyone, never
  incentivize, never gate.

---

## Yelp — found it, and it needs the same fixes

**Live profile:** https://www.yelp.com/biz/honorbrook-insurance-vienna
(status: **Claimed**, last updated ~3 months ago, 6 photos, no reviews yet)

| Field | What Yelp shows | Should be |
|---|---|---|
| Address | 8609 Westwood Center Dr, **Vienna**, VA 22182 | 8609 Westwood Center Dr, **Suite 110, Tysons**, VA 22182 |
| Categories | Life Insurance, Health Insurance Offices | add **Insurance** / Insurance Agency — you are currently invisible in the category most Medicare searchers browse |
| Website | https://honorbrook-insurance.com | correct (note Yelp wraps outbound links in a redirect, so treat this as a citation, not a link) |
| Hours | Mon-Fri 8-8, Sat-Sun 9-2:30 | correct — matches GBP and the site |

Two fixes: **the city and the missing suite number**, and **the categories**. The URL slug
will keep saying "vienna" even after you change the address — Yelp does not regenerate
slugs, and that is fine. It is cosmetic and does not affect the citation.

---

## Three more things found on the Google Business Profile

**1. Your GBP website link uses `http://`, not `https://`.**
It currently points at `http://honorbrook-insurance.com/`, which forces an extra redirect
hop before the visitor reaches the site. Change it in GBP to:
```
https://honorbrook-insurance.com
```

**2. There's a Calendly booking link on GBP that does not exist anywhere on the website.**
```
https://calendly.com/luaysadqi1/30min
```
Someone finding you on Google can book a 30-minute slot directly; someone landing on the
website cannot. Every CTA on the site is "call" or "request a callback." Adding this as a
third option — "Book a time that suits you" — is likely the single easiest conversion win
available, especially for working-age ICHRA/ACA buyers who will not call during the day.

**3. You have 26 reviews at a 5.0 average, and the website shows none of it.**
That is a substantial trust asset sitting entirely on Google. The site has no testimonials,
no rating, no review count anywhere — while every competitor page in the space leads with
social proof.

Worth adding a testimonials block (homepage plus the highest-intent product pages) pulling
a few real quotes with first name and last initial, as Google displays them.

**Important caveat:** do **not** add `AggregateRating` schema markup for these. Google's
structured-data policy disallows self-serving review markup for a business on its own
site, and it can trigger a manual action. Display the reviews as ordinary content — the
trust benefit is in the conversion rate, not in rich-result stars.
