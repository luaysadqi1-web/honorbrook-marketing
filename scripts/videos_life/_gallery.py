"""Layout test for the life-insurance video kit: every scene builder once, with placeholder words and no facts.
Not a real video; use it to check stills and contact sheets after changing scripts/video_life.py.
  python3 scripts/video_life.py sheet _gallery --out <dir>
"""
import video_life as K
P = K.P

VIDEO = dict(
    title='Video kit gallery',
    description='Every scene builder once, for layout checks.',
    poster=2.0,
    sources=[dict(fact='Placeholder fact line', url='https://example.gov/page', date='read 2026-11-25')],
    scenes=[
        K.scene(K.hook('Life insurance', ['Two kinds of', 'coverage to compare'], sub='A short takeaway line', icon='umbrella'),
                [P('This is the hook scene with an icon.'), P('And this phrase brings in the takeaway line.')]),
        K.scene(K.checklist('Step one', 'Questions to ask yourself', ['Who depends on your income?', 'What debts would be left behind?',
                                                                    'How long would they need support?', 'What coverage do you have now?'],
                            start=1, icons=['people', 'home', 'clock', 'doc']),
                [P('Here is the checklist scene.'), P('First row.'), P('Second row.'), P('Third row.'), P('Fourth row.')]),
        K.scene(K.timeline('How it works', 'A simple timeline', [('Day 1', 'The policy starts'), ('Year 10', 'A middle point on the line'),
                                                                 ('Year 20', 'The end of the term')], note='Placeholder note: example only'),
                [P('The first stop.'), P('The second stop.'), P('The third stop.')]),
        K.scene(K.two_column('Compare', 'Two sides, side by side', ('Left card title', ['First short row', 'Second short row', 'A third row that is longer']),
                             ('Right card title', ['First short row', 'Second short row', 'A third row that is longer']), left_mark='check', right_mark='x'),
                [P('The left card comes in with this phrase.'), P('And the right card with this one.')]),
        K.scene(K.fact_card('Good to know', '20 years', ['A supporting line under the big line', 'A second supporting line'],
                            source='Source: example.gov, placeholder page (read 2026-11-25)'),
                [P('The fact card shows one big line.'), P('Then the first supporting line.'), P('Then the second.')]),
        K.end_scene(),
    ])
