#!/usr/bin/env python3
"""
Seed one week of drafts into queue/.

This exists to (a) prove the pipeline end to end and (b) show the generator the
exact house format. Ongoing weeks are written by the Claude routine described in
_daily-social-spec.md, which follows topic-calendar.md.

  python3 seed_week.py --start 2026-08-28
"""
import argparse, datetime, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
import compliance, store

PHONE = "(571) 354-0146"
SITE = "honorbrook-insurance.com"

# pillar, X content (disclaimer appended automatically), LinkedIn body
WEEK = {
0: ("medicare-foundations",
    "Turning 65? Your Medicare window opens 3 months before your birthday month "
    "and closes 3 months after. Miss it and the Part B penalty is permanent. "
    "We'll map your dates, free. " + PHONE,
    "Turning 65 is the one insurance deadline that never forgives you.\n\n"
    "Your Initial Enrollment Period runs seven months: the three months before "
    "your birthday month, that month, and the three after. Enroll late without "
    "qualifying coverage and the Part B late-enrollment penalty is permanent - "
    "it is added to your premium for as long as you have Part B.\n\n"
    "The part people miss: still working at 65 with employer coverage can change "
    "the math entirely, and whether it does depends on how many people your "
    "employer has.\n\n"
    "If you are approaching 65, map your dates before you do anything else. "
    "We do that at no cost, and there is no obligation to use us afterward.\n\n"
    "Honorbrook Insurance - independent, licensed in 11 states. " + SITE + "\n\n"
    + compliance.DISCLAIMER_LONG),
1: ("ichra-employer",
    "Small employers: ICHRA lets you give staff tax-free dollars to buy their own "
    "coverage instead of running a group plan. No participation minimums, no "
    "renewal roulette. Licensed in 11 states. " + SITE,
    "Most small employers we talk to think their only two options are \"offer a "
    "group plan\" or \"offer nothing.\"\n\n"
    "There is a third one: an ICHRA - an Individual Coverage Health Reimbursement "
    "Arrangement. Instead of buying a group policy, you set a monthly allowance "
    "and employees use it to buy their own individual coverage. The "
    "reimbursement is tax-free to them and deductible to you.\n\n"
    "Why owners of 5-50 person companies keep moving to it:\n\n"
    "- Your cost is a number you choose, not a renewal you receive\n"
    "- No participation minimums to hit\n"
    "- You can set different allowances by class - full-time, part-time, "
    "salaried, by location\n"
    "- Employees keep their plan if they leave\n\n"
    "It is not right for everyone. If your team is mostly older and your current "
    "group rates are good, staying put can win. That is a math question, and it "
    "is worth actually running.\n\n"
    "Happy to run it with you. Honorbrook Insurance, Tysons VA. " + SITE),
2: ("aca-under65",
    "Lost job coverage? You get a 60-day Special Enrollment Period on the ACA "
    "Marketplace - but the clock starts the day coverage ends, not the day you "
    "get around to it. " + SITE,
    "If you have just lost employer coverage, you have 60 days. Not 60 days from "
    "when you start looking - 60 days from the date the coverage ended.\n\n"
    "Two things worth knowing before you default to COBRA:\n\n"
    "1. COBRA is the same plan, but you now pay the full cost including the "
    "share your employer used to cover. For many households a Marketplace plan "
    "with a premium tax credit lands lower.\n\n"
    "2. Subsidy eligibility is based on your household income for the year, not "
    "your old salary. People who lost income mid-year often qualify for help "
    "they assume is not available to them.\n\n"
    "Run both before the 60 days closes. If COBRA wins, take COBRA - we will "
    "tell you when it does.\n\n"
    "Honorbrook Insurance - independent, no cost to you. " + SITE),
3: ("life-final-expense",
    "Final expense coverage isn't about leaving a fortune. It's about making sure "
    "the people you love aren't handed a bill during the worst week of their "
    "lives. Honest talk, no pressure. " + PHONE,
    "Final expense insurance is a small whole life policy meant to cover what a "
    "funeral and the loose ends actually cost.\n\n"
    "What we tell people to check before buying one:\n\n"
    "- Is it level benefit or graded? Graded policies pay a reduced amount if "
    "death occurs in the first two or three years. That difference matters and "
    "it is not always volunteered.\n"
    "- Does the premium ever increase? On a properly structured whole life "
    "policy it should not.\n"
    "- Would existing coverage already handle it? Sometimes a client already has "
    "what they need through work or an old policy, and the honest answer is to "
    "keep it.\n\n"
    "We have told people not to buy. That is part of the job.\n\n"
    "Honorbrook Insurance, Tysons VA. " + SITE),
4: ("local-nova",
    "Plan networks in Northern Virginia change county to county - Fairfax isn't "
    "Loudoun isn't Arlington. Check that your doctors are in-network before you "
    "enroll, not after. " + PHONE,
    "A pattern we see every year in Northern Virginia: someone compares plans on "
    "price, enrolls, and then finds out in February that their specialist at "
    "Inova or VHC Health is out of network.\n\n"
    "Networks here are genuinely local. A plan that is strong in Fairfax County "
    "can be thin in Loudoun. The provider directory is the document that "
    "matters, and it is the one almost nobody reads.\n\n"
    "Before you enroll anywhere, verify three things: your doctors, your "
    "hospital, and every prescription you actually take. All three, by name.\n\n"
    "We do that check for clients across Northern Virginia at no cost - Vienna, "
    "Tysons, McLean, Fairfax, Arlington, Falls Church, Reston, Herndon, Oakton "
    "and Alexandria.\n\n"
    "Honorbrook Insurance. " + PHONE + "\n\n" + compliance.DISCLAIMER_LONG),
5: ("you-asked",
    "You asked: does using an agent cost me anything? No. We're paid by the "
    "carrier, and your rate is the same whether you enroll with us or by "
    "yourself. You just get a person to call. " + PHONE,
    "\"What do you charge?\" is the question we get most, so here is the plain "
    "answer: nothing.\n\n"
    "Independent agents are compensated by the insurance carrier when a policy "
    "is placed. Your rate is set by the carrier and filed with the state - it "
    "does not go up because you used an agent, and it does not go down because "
    "you skipped one.\n\n"
    "What you get for it is a person who is accountable to you at claim time, "
    "at renewal, and when something changes. Not a call center queue.\n\n"
    "The fair follow-up question is: if the carrier pays you, whose side are you "
    "on? That is why independence matters. We represent many carriers rather "
    "than one, so we are not steering you toward a single company's shelf.\n\n"
    "Honorbrook Insurance - Luay Sadqi, NPN 21370662. " + SITE),
6: ("trust-brand",
    "We're an independent agency. We don't work for one carrier - we work for "
    "you, and we'll tell you when the plan you already have is the right one to "
    "keep. Honorbrook Insurance, Tysons VA. " + SITE,
    "The right coverage. The honest way.\n\n"
    "That line is on our door because of how often people arrive having been "
    "sold something rather than advised.\n\n"
    "What being independent actually changes, in practice:\n\n"
    "- We represent many carriers, so a comparison is a real comparison\n"
    "- We are allowed to tell you to keep what you have. We do, regularly\n"
    "- We are local. You can drive to our office in Tysons and sit across from "
    "the person who wrote your policy\n\n"
    "Health, life, and annuity, for individuals and small employers, licensed "
    "across 11 states.\n\n"
    "Luay Sadqi, NPN 21370662 - Honorbrook Insurance, 8609 Westwood Center "
    "Drive, Tysons VA. " + PHONE),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default=None, help="YYYY-MM-DD, default tomorrow")
    args = ap.parse_args()

    start = (datetime.date.fromisoformat(args.start) if args.start
             else datetime.date.today() + datetime.timedelta(days=1))

    made = 0
    for offset in range(7):
        day = start + datetime.timedelta(days=offset)
        pillar, x_body, li_body = WEEK[day.weekday()]

        x_text, fits = compliance.fit_x(x_body)
        if not fits:
            print("!! %s X draft is %d chars after the disclaimer - shorten it"
                  % (day, len(x_text)))

        data = {
            "date": day.isoformat(),
            "generated": datetime.datetime.now().isoformat(timespec="seconds"),
            "source": "seed_week.py",
            "items": [
                store.new_item("x", pillar, x_text),
                store.new_item("linkedin", pillar, li_body),
            ],
        }
        store.save_queue(day.isoformat(), data)
        made += 1
        print("wrote queue/%s.json  (%s)  X=%d chars  LI=%d chars"
              % (day, pillar, len(x_text), len(li_body)))
    print("\n%d day(s) queued." % made)


if __name__ == "__main__":
    main()
