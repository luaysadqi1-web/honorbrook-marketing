/* Honorbrook coverage funnel engine: 14 products, each with its own branching intake, routing to the right page, consent, lead submit.
   Posts to the site's existing Formspree form. Set H.DRY = true to test without sending anything.
   Privacy by design: no SSN, Medicare number, medication names or diagnoses are collected. An agent covers those on the call. */
(function () {
  var H = window.HB = {};
  H.PHONE = '(571) 354-0146'; H.TEL = '+15713540146';
  H.ENDPOINT = 'https://formspree.io/f/xgobjlba';
  /* second lead form: emails a copy of each lead to the owner's Gmail (added Nov 25, 2026) */
  H.ENDPOINT2 = 'https://formspree.io/f/xljbopja';
  H.DRY = false;
  H.YEAR = 2026;
  H.SITE = '/';
  /* Online enrollment links, one per product id. PASTE YOUR PLAN-ENROLL URLS HERE; a product with '' shows no enroll button. */
  var PE = 'https://www.planenroll.com/?purl=Luay-Sadqi';
  H.ENROLL = { advantage: PE, medigap: PE, partd: PE };
  /* life, final expense, annuity, mortgage protection and the add-on health lines are booked through the same PlanEnroll page */
  H.BOOK = { life: PE, final: PE, annuity: PE, mortgage: PE, dvh: PE, hospital: PE, cancer: PE };
  /* server function that writes the lead into IntegrityCONNECT (see netlify/functions/lead.js) */
  H.CRM = '/.netlify/functions/lead';
  H.CONSENT = "By submitting, I authorize Honorbrook Insurance to contact me by phone or text (including automated means) about insurance. Consent isn't a condition of purchase; reply STOP to opt out. See our <a href='/privacy-policy' target='_blank' rel='noopener'>Privacy Policy</a>.";
  H.FINE = "Free to you. We do not offer every plan available in your area; contact Medicare.gov or 1-800-MEDICARE for all of your options. Honorbrook Insurance is not connected with or endorsed by the U.S. government or the federal Medicare program.";

  var ico = function (d) { return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + '</svg>'; };
  H.icon = {
    health: ico('<path d="M20.8 5.6a5.2 5.2 0 0 0-7.4 0L12 7l-1.4-1.4a5.2 5.2 0 0 0-7.4 7.4L12 21.8l8.8-8.8a5.2 5.2 0 0 0 0-7.4z"/>'),
    advantage: ico('<path d="M12 3 3 8l9 5 9-5-9-5zM3 12l9 5 9-5M3 16l9 5 9-5"/>'),
    medigap: ico('<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3z"/><path d="M9 12l2 2 4-4"/>'),
    partd: ico('<path d="M10.5 20.5a5 5 0 0 1-7-7l10-10a5 5 0 0 1 7 7l-10 10z"/><path d="M8.5 8.5l7 7"/>'),
    dvh: ico('<circle cx="12" cy="12" r="9"/><path d="M8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01"/>'),
    life: ico('<path d="M12 3a9 9 0 0 0-9 9h18a9 9 0 0 0-9-9z"/><path d="M12 12v7a2 2 0 0 0 4 0"/>'),
    final: ico('<path d="M3 11l9-8 9 8v10H3V11z"/><path d="M9 21v-6h6v6"/>'),
    mortgage: ico('<path d="M3 11l9-8 9 8v10H3V11z"/><path d="M9 15.5l2.2 2.2 4-4.4"/>'),
    annuity: ico('<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>'),
    biz: ico('<path d="M3 8h18v12H3z"/><path d="M8 8V5h8v3M3 13h18"/>'),
    disability: ico('<path d="M9 4h6v3H9zM6 6h12v15H6zM9 12h6M9 16h4"/>'),
    ltc: ico('<path d="M3 18V8M3 14h18v4M21 14v-2a3 3 0 0 0-3-3h-7v5"/>'),
    hospital: ico('<path d="M9 3h6v6h6v6h-6v6H9v-6H3V9h6z"/>'),
    cancer: ico('<path d="M12 3a4 4 0 0 0-4 4c0 3 4 5 4 9 0-4 4-6 4-9a4 4 0 0 0-4-4zM9 21l3-5 3 5"/>'),
    homecare: ico('<path d="M3 11l9-8 9 8M5 10v10h14V10"/><path d="M12 17s-3-1.8-3-4a1.7 1.7 0 0 1 3-.8 1.7 1.7 0 0 1 3 .8c0 2.2-3 4-3 4z"/>'),
    arrow: ico('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    back: ico('<path d="M19 12H5M11 6l-6 6 6 6"/>'),
    check: ico('<path d="M5 12.5l4.5 4.5L19 7.5"/>'),
    plus: ico('<path d="M12 5v14M5 12h14"/>'),
    phone: ico('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>')
  };

  var Q = function (id, q, o, x) { x = x || {}; x.id = id; x.q = q; x.o = o; return x; };
  var IN = function (id, list) { return { id: id, in: list }; };     /* show when single answer is in list */
  var HAS = function (id, v) { return { id: id, has: v }; };         /* show when multi answer includes v */
  var AGE = ['Under 40', '40 to 49', '50 to 59', '60 to 69', '70 to 79', '80 or older'];
  var AGE2 = ['50 to 59', '60 to 69', '70 to 79', '80 or older'];
  var CARR = ['UnitedHealthcare', 'Humana', 'Aetna', 'Wellcare', 'Another carrier', 'Not sure'];
  var YN = ['Yes', 'No', 'Not sure'];

  H.groups = [
    { id: 'medicare', title: 'Medicare' },
    { id: 'u65', title: 'Health insurance under 65' },
    { id: 'life', title: 'Life insurance & retirement' },
    { id: 'protect', title: 'Protect your income and savings' }
  ];

  H.products = [
    /* ---------- Medicare ---------- */
    { id: 'advantage', page: 'medicare-advantage', track: 'medicare', icon: 'advantage', label: 'Medicare Advantage (Part C)', desc: 'All-in-one plans that can include drug, dental, vision and hearing.',
      route: function (a) { return a.dual === 'Yes' ? 'medicaid-dual-eligible' : 'medicare-advantage'; },
      qs: [
        Q('stage', 'Where are you with Medicare?', ['Turning 65 soon', 'I have Medicare A & B', 'I have an Advantage plan and want to switch', 'Losing employer coverage', 'Not sure yet']),
        Q('when', 'When does your Medicare start, or when do you turn 65?', ['Within 3 months', '3 to 6 months', 'More than 6 months', 'Not sure'], { if: IN('stage', ['Turning 65 soon', 'Losing employer coverage']) }),
        Q('cur', 'Who is your current plan with?', CARR, { if: IN('stage', ['I have an Advantage plan and want to switch']) }),
        Q('dual', 'Do you have Medicaid or get help paying Medicare costs?', YN),
        Q('want', 'What matters most to you?', ['Keeping my doctors', 'Prescription drugs', 'Dental, vision and hearing', 'Low monthly cost', 'Low yearly out-of-pocket', 'Over-the-counter and fitness extras', 'Travel coverage'], { multi: true }),
        Q('doc', 'Do you have doctors or hospitals you want to keep?', ['Yes, check them for me', 'No preference']),
        Q('rx', 'How many prescriptions do you take?', ['None', '1 to 3', '4 to 7', '8 or more']),
        Q('budget', 'What monthly plan premium feels right?', ['As low as possible', 'Up to $50', '$50 to $150', 'Not sure yet'])
      ] },
    { id: 'medigap', page: 'medicare-supplement-medigap', track: 'medicare', icon: 'medigap', label: 'Medicare Supplement (Medigap)', desc: 'Fill the gaps in Original Medicare and keep any doctor that accepts Medicare.',
      qs: [
        Q('b', 'When did your Part B start, or when will it?', ['Within the last 6 months', 'More than 6 months ago', 'Starting in the next 3 months', 'Not sure']),
        Q('cur', 'What coverage do you have today?', ['Original Medicare only', 'A Medigap plan (want to switch)', 'A Medicare Advantage plan', 'Employer or retiree coverage', 'Nothing yet']),
        Q('plan', 'Which Medigap plan do you have in mind?', ['Plan G', 'Plan N', 'High-deductible Plan G', 'Not sure, help me choose']),
        Q('tob', 'Have you used tobacco in the last 12 months?', ['No', 'Yes']),
        Q('d', 'Do you need a Part D drug plan too?', ['Yes', 'I already have one', 'No']),
        Q('prio', 'What matters most?', ['Lowest premium', 'Keep any doctor', 'Predictable costs', 'Travel coverage', 'Strong carrier ratings'], { multi: true })
      ] },
    { id: 'partd', page: 'medicare-part-d', track: 'medicare', icon: 'partd', label: 'Prescription Drug Plan (Part D)', desc: 'An agent checks your medications against the plans we offer, on the call.',
      qs: [
        Q('need', 'What do you need?', ['A plan for the first time', 'Compare my current plan', 'Help paying for drugs (Extra Help)', 'I just lost drug coverage']),
        Q('cur', 'Who is your current drug plan with?', CARR, { if: IN('need', ['Compare my current plan']) }),
        Q('base', 'What is your medical coverage?', ['Original Medicare', 'Original Medicare with Medigap', 'Medicare Advantage', 'Not sure']),
        Q('rx', 'How many prescriptions do you take?', ['None', '1 to 3', '4 to 7', '8 or more']),
        Q('ph', 'Where do you fill them?', ['A local pharmacy', 'Mail order', 'Either']),
        Q('xh', 'Do you get Extra Help or have Medicaid?', YN)
      ] },
    { id: 'dvh', page: 'dental-vision-hearing-insurance', track: 'medicare', icon: 'dvh', label: 'Dental, vision & hearing', desc: 'Add-on plans for the care Original Medicare usually does not cover.',
      qs: [
        Q('what', 'What would you like covered?', ['Dental', 'Vision', 'Hearing'], { multi: true }),
        Q('dn', 'What dental care do you expect?', ['Cleanings and exams', 'Fillings and crowns', 'Dentures or implants', 'Not sure'], { if: HAS('what', 'Dental') }),
        Q('hr', 'Hearing aids?', ['I need them now', 'I may in the future', 'I have them and want help with costs'], { if: HAS('what', 'Hearing') }),
        Q('vs', 'Vision needs?', ['Exams, glasses or contacts', 'Cataract or other eye care', 'Not sure'], { if: HAS('what', 'Vision') }),
        Q('base', 'Your medical coverage today', ['Original Medicare', 'Medicare Advantage', 'Employer or other plan', 'No coverage']),
        Q('who', 'Who needs coverage?', ['Just me', 'Me and my spouse']),
        Q('start', 'When would you like coverage to start?', ['As soon as possible', 'In the next few months', 'Just looking'])
      ] },
    /* ---------- Under 65 ---------- */
    { id: 'health', page: 'aca-health-insurance', track: 'u65', icon: 'health', label: 'Health insurance (under 65)', desc: 'ACA marketplace plans, with help finding the savings you qualify for.',
      route: function (a) { return a.kind === 'Lost job-based coverage' ? 'lost-health-coverage' : a.kind === 'Self-employed' ? 'self-employed-health-insurance' : 'aca-health-insurance'; },
      qs: [
        Q('kind', 'What best describes you?', ['Individual or family', 'Self-employed', 'Lost job-based coverage', 'Early retiree (not yet 65)']),
        Q('lost', 'When did you lose coverage, or when will you?', ['Within the last 60 days', 'In the next 60 days', 'Longer ago', 'Not sure'], { if: IN('kind', ['Lost job-based coverage']) }),
        Q('who', 'Who needs coverage?', ['Just me', 'Me and my spouse', 'My family with kids']),
        Q('size', 'How many people in your household?', ['1', '2', '3', '4', '5 or more']),
        Q('inc', 'About what is your household income per year?', ['Under $25,000', '$25,000 to $50,000', '$50,000 to $75,000', '$75,000 to $100,000', 'Over $100,000', 'Prefer not to say']),
        Q('now', 'What coverage do you have today?', ['None', 'Employer plan that costs too much', 'A marketplace plan', 'COBRA', 'Medicaid or CHIP']),
        Q('want', 'What matters most?', ['Lowest monthly premium', 'Keeping my doctors', 'Prescription coverage', 'Low deductible', 'HSA-eligible plan'], { multi: true }),
        Q('start', 'When do you need it to start?', ['As soon as possible', 'The 1st of next month', 'January 1', 'Not sure'])
      ] },
    { id: 'biz', page: 'group-health-insurance-shop', track: 'u65', icon: 'biz', label: 'Business & group coverage', desc: 'ICHRA, SHOP and group health for employers of any size.',
      route: function (a) { return a.want === 'ICHRA allowance' ? 'ichra' : 'group-health-insurance-shop'; },
      qs: [
        Q('size', 'How many employees?', ['Just me', '2 to 10', '11 to 50', '51 to 100', 'More than 100']),
        Q('now', 'Do you offer coverage today?', ['No', 'Yes, a group plan', 'Yes, but the cost is a problem']),
        Q('want', 'What are you looking for?', ['Group health', 'ICHRA allowance', 'SHOP tax credit', 'Dental and vision', 'Life or disability for employees', 'Not sure']),
        Q('ren', 'When does your current plan renew?', ['Within 60 days', '60 to 120 days', 'More than 4 months', 'We are brand new'], { if: IN('now', ['Yes, a group plan', 'Yes, but the cost is a problem']) }),
        Q('state', 'Where are your employees based?', ['All in my state', 'Spread across states', 'Not sure'])
      ] },
    /* ---------- Life and retirement ---------- */
    { id: 'life', page: 'life-insurance', track: 'life', icon: 'life', label: 'Life insurance', desc: 'Term, whole life and indexed universal life, compared side by side.',
      route: function (a) { return { 'Term': 'term-life-insurance', 'Whole life': 'whole-life-insurance', 'Indexed universal life': 'indexed-universal-life', 'Guaranteed universal life': 'guaranteed-universal-life' }[a.type] || 'life-insurance'; },
      qs: [
        Q('type', 'What type are you considering?', ['Term', 'Whole life', 'Indexed universal life', 'Guaranteed universal life', 'Not sure']),
        Q('yrs', 'How many years do you need it?', ['10 years', '20 years', '30 years', 'Not sure'], { if: IN('type', ['Term', 'Not sure']) }),
        Q('goal2', 'What do you want the policy to do besides protect?', ['Build cash value', 'Help with retirement income', 'Leave a legacy'], { if: IN('type', ['Indexed universal life', 'Whole life']) }),
        Q('why', 'What is it for?', ['Replace my income', 'Mortgage or debts', 'Leave a legacy', 'Cover final costs', 'Business needs'], { multi: true }),
        Q('amt', 'How much coverage?', ['Under $100,000', '$100,000 to $250,000', '$250,000 to $500,000', '$500,000 to $1 million', 'Over $1 million']),
        Q('age', 'Your age', AGE),
        Q('tob', 'Have you used tobacco in the last 12 months?', ['No', 'Yes']),
        Q('have', 'Do you have life insurance now?', ['None', 'Only through work', 'An individual policy'])
      ] },
    { id: 'final', page: 'final-expense-life-insurance', track: 'life', icon: 'final', label: 'Final expense (burial) insurance', desc: 'Whole life coverage sized for funeral and final costs.',
      qs: [
        Q('who', 'Who is the policy for?', ['Myself', 'My spouse', 'A parent or relative']),
        Q('age', 'Their age', AGE2),
        Q('amt', 'How much would you like?', ['$5,000 to $10,000', '$10,000 to $15,000', '$15,000 to $25,000', 'Not sure']),
        Q('have', 'Is anything set aside for it now?', ['No', 'A small life policy', 'A pre-paid funeral plan', 'Savings']),
        Q('tob', 'Tobacco use in the last 12 months?', ['No', 'Yes']),
        Q('bud', 'What monthly payment is comfortable?', ['Under $30', '$30 to $60', '$60 to $100', 'Not sure'])
      ] },
    { id: 'mortgage', page: 'mortgage-protection-insurance', track: 'life', icon: 'mortgage', label: 'Mortgage protection', desc: 'Life insurance sized to your home loan, paid to the person you choose.',
      qs: [
        Q('st', 'Where are you with the home?', ['I have a mortgage now', 'Buying or just bought', 'Refinancing', 'Just looking']),
        Q('bal', 'About how much is left on the loan?', ['Under $150,000', '$150,000 to $300,000', '$300,000 to $500,000', 'Over $500,000', 'Not sure']),
        Q('yrs', 'How many years are left?', ['Under 10', '10 to 20', '20 to 30', 'Not sure']),
        Q('age', 'Your age', AGE),
        Q('tob', 'Have you used tobacco in the last 12 months?', ['No', 'Yes']),
        Q('have', 'Do you have life insurance now?', ['None', 'Only through work', 'An individual policy'])
      ] },
    { id: 'annuity', page: 'annuities', track: 'life', icon: 'annuity', label: 'Annuities & retirement', desc: 'Fixed and indexed annuities, plus 401(k) and IRA rollovers.',
      route: function (a) { return a.goal === 'Roll over a 401(k) or IRA' ? 'retirement-rollover-annuity' : 'annuities'; },
      qs: [
        Q('goal', 'What is your goal?', ['Steady retirement income', 'Growth with less market risk', 'Roll over a 401(k) or IRA', 'Not sure']),
        Q('src', 'Where would the money come from?', ['401(k) or 403(b)', 'IRA', 'Savings or CDs', 'Inheritance or sale', 'Other'], { multi: true }),
        Q('left', 'Have you left that employer?', ['Yes', 'No, I still work there'], { if: IN('goal', ['Roll over a 401(k) or IRA']) }),
        Q('amt', 'About how much are you planning with?', ['Under $50,000', '$50,000 to $150,000', '$150,000 to $500,000', '$500,000 or more']),
        Q('when', 'When might you need income?', ['Within a year', '1 to 5 years', '5 to 10 years', 'More than 10 years']),
        Q('age', 'Your age', ['Under 50', '50 to 59', '60 to 69', '70 or older']),
        Q('style', 'What kind of growth fits you?', ['Fixed and predictable', 'Indexed with a protected floor', 'Not sure'])
      ] },
    /* ---------- Protection ---------- */
    { id: 'disability', page: 'disability-insurance', track: 'protect', icon: 'disability', label: 'Disability income insurance', desc: 'Replace part of your paycheck if illness or injury stops you from working.',
      qs: [
        Q('job', 'How do you work?', ['Employee', 'Self-employed', 'Business owner', 'Professional practice']),
        Q('inc', 'About what is your yearly income?', ['Under $50,000', '$50,000 to $100,000', '$100,000 to $200,000', 'Over $200,000']),
        Q('grp', 'Do you have disability through work?', ['No', 'Short-term only', 'Short and long-term']),
        Q('wait', 'How long could you wait for benefits?', ['30 days', '90 days', '180 days', 'Not sure']),
        Q('len', 'How long should benefits last?', ['2 years', '5 years', 'To age 65 or 67', 'Not sure'])
      ] },
    { id: 'ltc', page: 'long-term-care-insurance', track: 'protect', icon: 'ltc', label: 'Long-term care insurance', desc: 'Pay for in-home care, assisted living or a nursing facility without draining savings.',
      qs: [
        Q('age', 'Your age', ['Under 50', '50 to 59', '60 to 69', '70 or older']),
        Q('care', 'What are you planning for?', ['Care at home', 'Assisted living', 'Nursing facility', 'All of the above'], { multi: true }),
        Q('type', 'What style do you prefer?', ['Traditional long-term care', 'Life insurance with a care benefit', 'Not sure']),
        Q('have', 'Do you have long-term care coverage now?', ['No', 'Through work', 'An individual policy']),
        Q('bud', 'What yearly budget is comfortable?', ['Under $2,000', '$2,000 to $5,000', 'Over $5,000', 'Not sure'])
      ] },
    { id: 'hospital', page: 'hospital-indemnity-insurance', track: 'protect', icon: 'hospital', label: 'Hospital indemnity', desc: 'Cash paid straight to you for hospital stays, to use however you need.',
      qs: [
        Q('base', 'Your medical coverage today', ['Medicare Advantage', 'Original Medicare', 'Employer plan', 'Marketplace plan']),
        Q('worry', 'What worries you most?', ['Hospital copays', 'High deductible', 'Out-of-pocket maximum', 'Lost income'], { multi: true }),
        Q('who', 'Who needs coverage?', ['Just me', 'Me and my spouse', 'My family']),
        Q('start', 'When would you like coverage to start?', ['As soon as possible', 'In the next few months', 'Just looking'])
      ] },
    { id: 'cancer', page: 'cancer-critical-illness-insurance', track: 'protect', icon: 'cancer', label: 'Cancer & critical illness', desc: 'A lump-sum benefit paid to you on diagnosis, for any expense.',
      qs: [
        Q('kind', 'What interests you?', ['Cancer only', 'Cancer plus heart attack and stroke', 'Not sure']),
        Q('who', 'Who needs coverage?', ['Just me', 'Me and my spouse', 'My family']),
        Q('base', 'Your medical coverage today', ['Medicare', 'Employer plan', 'Marketplace plan', 'None']),
        Q('start', 'When would you like coverage to start?', ['As soon as possible', 'In the next few months', 'Just looking'])
      ] },
    { id: 'homecare', page: 'short-term-home-care-insurance', track: 'protect', icon: 'homecare', label: 'Short-term & home care', desc: 'Recovery care and in-home help that Medicare usually pays little for.',
      qs: [
        Q('who', 'Who is it for?', ['Me', 'My spouse', 'A parent or relative']),
        Q('need', 'What do you want covered?', ['Short-term recovery care', 'Home health care', 'Both']),
        Q('age', 'Their age', ['Under 60', '60 to 69', '70 to 79', '80 or older'])
      ] }
  ];
  /* order inside each group: the lines the owner rated High on Nov 17, 2026 come first */
  var ORDER = ['advantage', 'dvh', 'medigap', 'partd', 'health', 'biz', 'life', 'final', 'mortgage', 'annuity', 'hospital', 'cancer', 'disability', 'ltc', 'homecare'];
  H.products.sort(function (x, y) { return ORDER.indexOf(x.id) - ORDER.indexOf(y.id); });
  /* not shown in grids: used when someone just wants a call back */
  H.extra = [{ id: 'general', page: 'contact', track: 'none', icon: 'plus', label: 'A general coverage review', desc: '', qs: [] }];
  H.track = function (n, p) { try { if (window.gtag) window.gtag('event', n, p || {}); } catch (e) {} };
  H.byId = function (id) { var all = H.products.concat(H.extra); for (var i = 0; i < all.length; i++) if (all[i].id === id) return all[i]; };

  /* ---------- branching engine: answers are {questionId: 'text'} per product ---------- */
  H.vis = function (p, a) {
    return p.qs.filter(function (q) {
      var c = q.if; if (!c) return true; var v = a[c.id]; if (v === undefined) return false;
      return c.in ? c.in.indexOf(v) > -1 : v.split(', ').indexOf(c.has) > -1;
    });
  };
  H.nextQ = function (p, a) { var v = H.vis(p, a); for (var i = 0; i < v.length; i++) if (a[v[i].id] === undefined) return v[i]; return null; };
  H.prog = function (p, a) { var v = H.vis(p, a), d = 0; v.forEach(function (q) { if (a[q.id] !== undefined) d++; }); return { n: Math.min(d + 1, v.length + 1), total: v.length + 1 }; };
  H.prune = function (p, a) { var ok = {}; H.vis(p, a).forEach(function (q) { ok[q.id] = 1; }); Object.keys(a).forEach(function (k) { if (!ok[k]) delete a[k]; }); };
  H.set = function (p, a, id, val) { a[id] = val; H.prune(p, a); };
  H.back = function (p, a) { var k = null; H.vis(p, a).forEach(function (q) { if (a[q.id] !== undefined) k = q.id; }); if (k === null) return false; delete a[k]; H.prune(p, a); return true; };
  H.demoFill = function (p, a, n) { for (var i = 0; i < n; i++) { var q = H.nextQ(p, a); if (!q) break; a[q.id] = q.o[0]; } };
  H.pageFor = function (id, a) { var p = H.byId(id); return p.route ? p.route(a || {}) : p.page; };

  H.trackFor = function (year) {
    var age = H.YEAR - year;
    if (!(year > 1900 && year <= H.YEAR)) return null;
    return { age: age, medicare: age >= 64 };
  };
  H.esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };

  /* Which meeting type to pick on PlanEnroll (it offers Annuities, Health or Life), so the booking lands on the right line in IntegrityCONNECT. */
  H.MEET = { life: 'Life', final: 'Life', mortgage: 'Life', annuity: 'Annuities' };
  H.meetType = function (ids) { var id = (ids || [])[0]; return H.MEET[id] || 'Health'; };
  H.meetHint = function (ids) {
    return 'When PlanEnroll asks what type of meeting you would like, choose ' + H.meetType(ids) + '. The first open time is at least 24 hours ahead. To talk sooner, call us.';
  };

  /* confirmation links: the page for what they chose, plus an enroll button when a link is set */
  H.doneLinks = function (ids, answers) {
    var h = '<div class="hbf-next">';
    ids.forEach(function (id) {
      var p = H.byId(id), e = H.ENROLL[id], pg = H.pageFor(id, (answers || {})[id]);
      h += '<div class="hbf-nx"><b>' + p.label + '</b>' +
        (e ? '<a class="hbf-enroll" href="' + e + '">Start enrollment online</a>' : '') +
        (H.BOOK[id] ? '<a class="hbf-enroll" href="' + H.BOOK[id] + '" target="_blank" rel="noopener">Schedule an appointment</a>' : '') +
        '<a class="hbf-learn" href="' + H.SITE + pg + '">Read about this coverage</a></div>';
    });
    return h + '</div>';
  };

  /* Priority note for the agent: which leads are ready to talk now. Internal only, shown in the lead email and CRM note. */
  H.priority = function (L) {
    var why = [], a = (L && L.answers) || {};
    ((L && L.products) || []).forEach(function (id) {
      var x = a[id] || {};
      if (id === 'annuity') {
        var hot = [];
        if (x.goal === 'Roll over a 401(k) or IRA' && x.left === 'Yes') hot.push('rollover, already left the employer');
        if (x.when === 'Within a year' || x.when === '1 to 5 years') hot.push('income needed ' + x.when.toLowerCase());
        if (hot.length) why.push('Annuity: ' + hot.join(', ') + (x.amt ? ', planning with ' + x.amt : ''));
      }
      if (id === 'final' && x.amt && x.amt !== 'Not sure' && x.bud && x.bud !== 'Not sure') why.push('Final expense: wants ' + x.amt + ', budget ' + x.bud);
      if (id === 'life' && x.type && x.type !== 'Not sure' && x.amt) why.push('Life: ' + x.type + ', ' + x.amt);
      if (id === 'advantage') {
        var m = [];
        if (x.when === 'Within 3 months') m.push('Medicare starts within 3 months');
        if (x.stage === 'Losing employer coverage') m.push('losing employer coverage');
        if (x.stage === 'I have an Advantage plan and want to switch') m.push('wants to switch plans' + (x.cur && x.cur !== 'Not sure' ? ', now with ' + x.cur : ''));
        if (m.length) why.push('Medicare Advantage: ' + m.join(', '));
      }
      if (id === 'dvh') {
        var d = [];
        if (x.start === 'As soon as possible') d.push('wants to start as soon as possible');
        if (x.hr === 'I need them now') d.push('needs hearing aids now');
        if (x.dn === 'Dentures or implants') d.push('expects dentures or implants');
        if (d.length) why.push('Dental, vision and hearing: ' + d.join(', '));
      }
      if (id === 'hospital' && x.start === 'As soon as possible') why.push('Hospital indemnity: wants to start as soon as possible' + (x.base ? ', has ' + x.base : ''));
      if (id === 'cancer' && x.start === 'As soon as possible') why.push('Cancer and critical illness: wants to start as soon as possible' + (x.kind && x.kind !== 'Not sure' ? ', ' + x.kind.toLowerCase() : ''));
      if (id === 'mortgage' && x.st && x.st !== 'Just looking' && x.bal && x.bal !== 'Not sure') why.push('Mortgage protection: ' + x.st.toLowerCase() + ', ' + x.bal + ' left on the loan');
    });
    return why.length ? 'HOT. ' + why.join('. ') : 'Standard';
  };

  H.contactHTML = function (btnLabel) {
    return '<form class="hbf-contact" novalidate>' +
      '<div class="hbf-grid">' +
      '<label>Full name<input name="name" autocomplete="name" placeholder="Jane Smith"></label>' +
      '<label>Phone number<input name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="(555) 555-5555"></label>' +
      '<label>ZIP code<input name="zip" autocomplete="postal-code" inputmode="numeric" maxlength="5" placeholder="22182"></label>' +
      '<label>Email <span class="hbf-opt">optional</span><input name="email" type="email" autocomplete="email" placeholder="you@email.com"></label>' +
      '</div>' +
      '<fieldset class="hbf-times"><legend>Best time to call</legend>' +
      ['Morning', 'Afternoon', 'Evening', 'Any time'].map(function (t, i) { return '<label class="hbf-chip"><input type="radio" name="best" value="' + t + '"' + (i === 3 ? ' checked' : '') + '><span>' + t + '</span></label>'; }).join('') +
      '</fieldset>' +
      '<input type="text" name="_gotcha" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">' +
      '<label class="hbf-consent"><input type="checkbox" name="consent"><span>' + H.CONSENT + '</span></label>' +
      '<p class="hbf-err" role="alert" aria-live="polite"></p>' +
      '<button class="hbf-submit" type="submit"><span>' + (btnLabel || 'Get my free review') + '</span>' + H.icon.arrow + '</button>' +
      '<p class="hbf-fine">' + H.FINE + '</p>' +
      '</form>';
  };

  /* validates, builds the lead and submits. getLead() returns {products:[ids], answers:{id:{qid:answer}}, source}. */
  H.bindContact = function (form, getLead, done) {
    var zipEl = form.elements.zip;
    if (zipEl && !zipEl.value && H.zip) zipEl.value = H.zip;
    /* first focus in the contact step counts as a form start, like the other lead forms (assets/chat.js) */
    form.addEventListener('focusin', function () {
      if (form._hbStarted) return; form._hbStarted = true;
      H.track('form_start', { form: 'funnel', page: location.pathname, line: (document.body && document.body.getAttribute('data-line')) || '', transport_type: 'beacon' });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = form.elements, err = form.querySelector('.hbf-err'), digits = f.phone.value.replace(/\D/g, '');
      var bad = !f.name.value.trim() ? 'Please add your name.' : digits.length < 10 ? 'Please add a phone number with area code.' :
        !/^\d{5}$/.test(f.zip.value.trim()) ? 'Please add your 5-digit ZIP code.' : !f.consent.checked ? 'Please check the box so we can contact you.' : '';
      if (bad) { err.textContent = bad; return; }
      err.textContent = '';
      if (f._gotcha.value) return done();
      var L = getLead(), fd = new FormData();
      var names = L.products.map(function (id) { return H.byId(id).label; });
      var prio = H.priority(L);
      fd.append('_subject', (prio.indexOf('HOT') === 0 ? 'HOT lead: ' : 'New funnel lead: ') + names.join(', ') + ' (Honorbrook website)');
      fd.append('Priority', prio);
      fd.append('Name', f.name.value.trim()); fd.append('Phone', f.phone.value.trim()); fd.append('ZIP', f.zip.value.trim());
      if (f.email.value) fd.append('Email', f.email.value.trim());
      fd.append('Best time to call', form.querySelector('input[name=best]:checked').value);
      fd.append('Interests', names.join(' | '));
      L.products.forEach(function (id) {
        var p = H.byId(id), a = (L.answers || {})[id] || {};
        var line = H.vis(p, a).filter(function (q) { return a[q.id] !== undefined; }).map(function (q) { return q.q + ' ' + a[q.id]; }).join(' / ');
        fd.append(p.label, line || '(no extra answers)');
        fd.append(p.label + ' page', H.SITE + H.pageFor(id, a));
      });
      fd.append('Consent', 'Yes'); fd.append('Funnel', L.source || '');
      /* lead source of this visit, kept by assets/chat.js for this browser tab; only fields that have a value */
      try { var at = JSON.parse(sessionStorage.getItem('hb_attr') || 'null');
        if (at && typeof at === 'object') ['landing_page', 'referrer', 'utm_source', 'utm_medium', 'utm_campaign', 'gclid'].forEach(function (k) { if (at[k]) fd.append(k, String(at[k]).slice(0, 300)); });
      } catch (x) {}
      /* the lead counts as sent when any one of the three posts is accepted (CRM function, xgobjlba, xljbopja) */
      var tries = [], ok = function (r) { return !!(r && r.ok); }, no = function () { return false; };
      /* also send the lead into IntegrityCONNECT through our own server function; never blocks the visitor */
      if (!H.DRY && H.CRM) { try {
        var ans = L.products.map(function (id) { var p = H.byId(id), x = (L.answers || {})[id] || {}; return p.label + ': ' + H.vis(p, x).filter(function (q) { return x[q.id] !== undefined; }).map(function (q) { return q.q + ' ' + x[q.id]; }).join(' / '); }).join(' || ');
        tries.push(fetch(H.CRM, { method: 'POST', keepalive: true, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name: f.name.value.trim(), phone: f.phone.value.trim(), zip: f.zip.value.trim(), email: f.email.value.trim(), best: form.querySelector('input[name=best]:checked').value, interests: names.join(', '), answers: 'Priority: ' + prio + ' || ' + ans, source: L.source || '', consent: true }) }).then(ok, no));
      } catch (x) {} }
      var btn = form.querySelector('.hbf-submit'); btn.disabled = true; btn.classList.add('busy');
      /* the copy is marked sent only when it is accepted, so a retry after a failure tries it again */
      if (!H.DRY && H.ENDPOINT2 && !form._hbCopied) { try { tries.push(fetch(H.ENDPOINT2, { method: 'POST', body: fd, headers: { Accept: 'application/json' }, keepalive: true }).then(function (r) { if (ok(r)) form._hbCopied = true; return ok(r); }, no)); } catch (x) {} }
      if (H.DRY) tries.push(Promise.resolve(true));
      else tries.push(fetch(H.ENDPOINT, { method: 'POST', body: fd, headers: { Accept: 'application/json' }, keepalive: true }).then(ok, no));
      /* true when any post is accepted; waits up to 3 s more for the others, and gives up after 15 s with no answer */
      var go = new Promise(function (res) { var left = tries.length, any = false, fin = false; function end(v) { if (!fin) { fin = true; res(v); } }
        setTimeout(function () { end(any); }, 15000);
        tries.forEach(function (p) { p.then(function (v) { if (v && !any) { any = true; setTimeout(function () { end(true); }, 3000); } if (--left === 0) end(any); }, function () { if (--left === 0) end(any); }); }); });
      go.then(function (sent) { if (sent) { H.track('generate_lead', { products: L.products.join(','), source: L.source || '', line: L.products.join(','), hot: String(prio).indexOf('HOT') === 0 }); done(); } else throw 0; }).catch(function () { btn.disabled = false; btn.classList.remove('busy'); err.innerHTML = 'Something went wrong. Please call us at <a href="tel:' + H.TEL + '">' + H.PHONE + '</a>.'; });
    });
  };
})();
