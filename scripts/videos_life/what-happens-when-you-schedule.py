"""What happens when you schedule a call with Honorbrook (for /schedule-an-appointment).
Facts only from the built pages staging/site-onyx/schedule-an-appointment.html and the "Four steps" section of
staging/site-onyx/index.html (read Nov 27, 2026). No plan or product details, no prices, no company names.
"""
import video_life as K
P = K.P

PAGE = 'https://honorbrook-insurance.com/schedule-an-appointment'
HOME = 'https://honorbrook-insurance.com/'
D_PAGE = 'page updated November 2026; read Nov 27, 2026'
D_HOME = 'home page "Four steps" section; read Nov 27, 2026'

VIDEO = dict(
    title='What happens when you schedule a call with Honorbrook',
    description=('The four steps to schedule a call with Honorbrook Insurance: open the scheduling page, create a profile, '
                 'add your details and ask for your meeting. Plus what to have next to you and how to reach us sooner.'),
    poster=14.0,
    sources=[
        dict(fact='Four steps: open Luay\'s page (select Schedule an appointment; look for Luay Sadqi, NPN 21370662, at the top), '
                  'create your profile with your email address and a password, add your doctors, prescriptions, pharmacy and '
                  'current coverage, then ask for your meeting.', url=HOME, date=D_HOME),
        dict(fact='You choose how to meet: over the phone, at our office in Tysons or at your home '
                  '(office and home visits are in Northern Virginia).', url=PAGE, date=D_PAGE),
        dict(fact='Pick Life, Health or Annuities, and 30 or 60 minutes.', url=PAGE, date=D_PAGE),
        dict(fact='You see our open times. The first one offered is at least 24 hours ahead. '
                  'To talk sooner, call (301) 615-8289 or text (571) 354-0146.', url=PAGE, date=D_PAGE),
        dict(fact='What to have next to you: your prescriptions, with the dose and how often you take each one; the names of the '
                  'doctors and specialists you want to keep; the pharmacy you use; your current insurance cards.',
             url=PAGE, date=D_PAGE),
        dict(fact='We read it before we talk, so the conversation starts from your information.', url=PAGE, date=D_PAGE),
        dict(fact='Creating a profile does not enroll you in anything. You do not need to choose a plan before you schedule. '
                  'That is what the meeting is for.', url=PAGE, date=D_PAGE),
    ],
    scenes=[
        # 1. Hook
        K.scene(K.hook('Honorbrook Insurance', 'What happens when you schedule a call with Honorbrook',
                       sub='4 steps', icon='calendar'),
                [P('What happens when you schedule a call with Honorbrook?'),
                 P('Here are the 4 steps.', 'Here are the four steps.')], pre=0.1, post=0.5),
        # 2. Four steps (centerpiece)
        K.scene(K.checklist('How scheduling works', 'Four steps',
                            ["Open Luay's page", 'Create your profile', 'Add your details', 'Ask for your meeting'],
                            start=0, at=[0, 2, 3, 4]),
                [P('Select Schedule an appointment.'),
                 P('Look for Luay Sadqi at the top.', 'Look for Loo-eye Sodkee at the top.'),
                 P('Create your profile with your email address and a password.'),
                 P('Add your doctors, prescriptions, pharmacy and current coverage.'),
                 P('Then ask for your meeting.')]),
        # 3. The meeting choices
        K.scene(K.checklist('Your meeting', 'You choose',
                            ['Phone, Tysons office or your home', 'Life, Health or Annuities', '30 or 60 minutes'],
                            start=0, mark_kind=None, icons=['chat', 'doc', 'clock'],
                            note='Office and home visits are in Northern Virginia.'),
                [P('Choose how to meet: by phone, at our office in Tysons, or at your home.'),
                 P('Pick Life, Health or Annuities,'),
                 P('and 30 or 60 minutes.', 'and thirty or sixty minutes.'),
                 P('Office and home visits are in Northern Virginia.')]),
        # 4. First open time
        K.scene(K.fact_card('Pick a day and time', '24 hours',
                            ['The first open time is at least 24 hours ahead',
                             'To talk sooner: call (301) 615-8289', 'or text (571) 354-0146'],
                            head='First open time', at=[0, 1, 1]),
                [P('The first open time is at least 24 hours ahead.',
                   'The first open time is at least twenty four hours ahead.'),
                 P('To talk sooner, call or text us.')]),
        # 5. What to have ready
        K.scene(K.checklist('Before you start', 'What to have next to you',
                            ['Prescriptions: dose and how often', 'Doctors and specialists to keep', 'The pharmacy you use',
                             'Your current insurance cards'],
                            start=0, icons=['pill', 'person', 'pin', 'doc']),
                [P('Your prescriptions, with the dose and how often you take each one.'),
                 P('The doctors and specialists you want to keep.'),
                 P('The pharmacy you use.'),
                 P('And your current insurance cards.')]),
        # 6. What the call covers / no enrollment
        K.scene(K.fact_card('Good to know', 'We read it before we talk',
                            ['The conversation starts from your information',
                             'Creating a profile does not enroll you in anything',
                             'You do not need to choose a plan before you schedule'],
                            at=[0, 1, 2]),
                [P('We read it before we talk, so the conversation starts from your information.'),
                 P('Creating a profile does not enroll you in anything.'),
                 P('You do not need to choose a plan before you schedule.')]),
        K.end_scene(),
    ])
