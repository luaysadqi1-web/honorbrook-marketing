"""Is there a government final expense program? (for /final-expense-life-insurance)
Facts: scratchpad leads/content/government-final-expense-program.checked.json (checked November 25, 2026).
"""
import video_life as K
P = K.P

MN = 'https://www.ag.state.mn.us/consumer/publications/ProtectPersonalInformation.asp'
DC = 'https://disb.dc.gov/node/1464551'
USC = 'https://www.govinfo.gov/content/pkg/USCODE-2024-title15/html/USCODE-2024-title15-chap20-sec1012.htm'
NAIC_LIFE = 'https://content.naic.org/consumer/life-insurance.htm'
SSA = 'https://www.ssa.gov/personal-record/when-someone-dies/lump-sum-death-payment'
VA_BURIAL = 'https://www.va.gov/burials-memorials/veterans-burial-allowance/'
NAIC_AGENT = 'https://content.naic.org/article/consumer-insight-how-choose-insurance-agent'
NAIC_DEPTS = 'https://content.naic.org/state-insurance-departments'
NIPR = 'https://nipr.com/licensing-center/look-up-a-national-producer-number'
SSA_DATE = 'No date shown on the page (metadata: published September 3, 2025, modified April 16, 2026); read November 25, 2026'

VIDEO = dict(
    title='Is there a government final expense program?',
    description=('There is no federal final expense insurance program for the general public; the ads describe private life insurance. '
                 'This short video covers which public benefits do exist and how to check an agent before you share your information.'),
    poster=3.0,
    sources=[
        dict(fact='No federal final expense insurance program for the public. Ads and mailers describe private life insurance '
                  '(mailers "are not affiliated with the government" and are used to sell "life, burial, or supplemental" insurance)',
             url=MN, date='No date shown; read November 25, 2026'),
        dict(fact='DC insurance regulator: the mailed form "is not from District government" and was used by insurance companies to find clients',
             url=DC, date='No date shown (notice describes a 2020 form); read November 25, 2026'),
        dict(fact='Insurance is regulated mainly by the states ("shall be subject to the laws of the several States")',
             url=USC, date='United States Code, 2024 edition; read November 25, 2026'),
        dict(fact='"all insurance companies are regulated by the state, so a \'state-regulated\' plan is nothing new or special"',
             url=MN, date='No date shown; read November 25, 2026'),
        dict(fact='State insurance departments list the agents and companies licensed in the state',
             url=NAIC_LIFE, date='No date shown; read November 25, 2026'),
        dict(fact='Social Security lump-sum death payment: "A spouse might get a one-time death benefit payment of $255."',
             url=SSA, date=SSA_DATE),
        dict(fact='If there is no spouse, some children may be eligible', url=SSA, date=SSA_DATE),
        dict(fact='Apply within 2 years of the death', url=SSA, date=SSA_DATE),
        dict(fact='VA burial allowances help cover "some of the costs of the burial, funeral, and plot or interment"; "You may be eligible for Veterans burial allowances if you\'re paying for the burial and funeral costs" (VA lists who qualifies and current amounts)',
             url=VA_BURIAL, date='Last updated October 30, 2026'),
        dict(fact='"Make sure the agent and insurance company are licensed in your state."',
             url=NAIC_AGENT, date='February 1, 2019; read November 25, 2026'),
        dict(fact='NAIC Insurance Departments page: "Find an Insurance Agent" state selector leads to each state\'s agent search',
             url=NAIC_DEPTS, date='No date shown; read November 25, 2026'),
        dict(fact='An NPN is an ID assigned during licensing', url=NIPR, date='No date shown; read November 25, 2026'),
    ],
    scenes=[
        K.scene(K.hook('Final expense', ['A government', 'final expense', 'program?'], sub='Here is what is real', icon='doc'),
                [P('Saw an ad for a government final expense program?'),
                 P('Here is what is real.')], pre=0.1, post=0.6),
        K.scene(K.fact_card('The short answer', 'No', ['No federal final expense insurance program',
                                                      'The ads describe private life insurance'],
                            source='Sources: Minnesota Attorney General; DC insurance regulator (read Nov 25, 2026)'),
                [P('There is no federal final expense insurance program for the public.'),
                 P('The ads describe private life insurance that you pay for.')]),
        K.scene(K.fact_card('Ad wording', 'State-regulated', ['State insurance departments oversee insurers and agents',
                                                             'It does not mean the state runs or pays for the plan'],
                            source='Sources: 15 U.S.C. 1012; Minnesota Attorney General'),
                [P('State-regulated means your state oversees insurers and agents.'),
                 P('It does not mean the state runs or pays for the plan.')]),
        K.scene(K.fact_card('Social Security', '$255', ['A one-time payment a spouse might get',
                                                       'If no spouse, some children may be eligible',
                                                       'Apply within 2 years of the death'],
                            head='Lump-sum death payment',
                            source='Source: ssa.gov, Lump-sum death payment (read Nov 25, 2026)'),
                [P('Social Security has a lump-sum death payment.'),
                 P('A spouse might get a one-time payment of $255.',
                   'A spouse might get a one-time payment of two hundred fifty five dollars.'),
                 P('If there is no spouse, some children may be eligible.'),
                 P('You must apply within 2 years of the death.', 'You must apply within two years of the death.')]),
        K.scene(K.fact_card('For veterans', 'VA burial allowances', ['For the person who pays for an eligible veteran\'s burial',
                                                                     'Help cover some burial, funeral and plot costs'],
                            source='Source: va.gov, Veterans burial allowance (updated Oct 30, 2026)'),
                [P('If you pay for an eligible veteran\'s burial, VA burial allowances may help.',
                   'If you pay for an eligible veteran\'s burial, V A burial allowances may help.'),
                 P('They cover some burial and funeral costs.')]),
        K.scene(K.checklist('Before you share', 'Check the license',
                            ['Ask for name, agency and NPN', 'Open the NAIC Insurance Departments page',
                             'Confirm a license in your state'],
                            start=1, icons=['person', 'doc', 'check'], note='Sources: NAIC; NIPR (read Nov 25, 2026)'),
                [P('Check the agent\'s license.'),
                 P('Ask for the name, the agency, and the NPN.', 'Ask for the name, the agency, and the N P N.'),
                 P('Open the NAIC Insurance Departments page.', 'Open the N A I C insurance departments page.'),
                 P('Confirm the agent is licensed in your state.')]),
        K.scene(K.checklist('Ask any caller', 'Fair questions',
                            ['Are you licensed in my state?', 'Is this insurance I pay for?', 'Can I have it in writing first?'],
                            start=1, mark_kind=None, icons=['?', '?', '?']),
                [P('Fair questions for any caller, including us.'),
                 P('Are you licensed in my state?'),
                 P('Is this insurance I pay for?'),
                 P('Can I have it in writing first?')]),
        K.end_scene(),
    ])
