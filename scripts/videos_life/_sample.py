"""Worked example for the life-insurance video kit (scripts/video_life.py): two scenes, no facts.

Copy this file to scripts/videos_life/<your-slug>.py, keep the shape, replace the words.
  python3 scripts/video_life.py still _sample 2.0 land --out <dir>
  python3 scripts/video_life.py build _sample
"""
import video_life as K
P = K.P

VIDEO = dict(
    title='Video kit sample',
    description='A two-scene sample that shows the shape of a video file for the Honorbrook video kit.',
    poster=2.0,                      # seconds into the video for the 16:9 poster frame (pick a moment with the title fully shown)
    sources=[],                      # dict(fact=..., url=..., date=...) for every fact that appears on screen or in the narration
    scenes=[
        K.scene(K.hook('Video kit sample', ['A short title', 'goes here'], sub='One takeaway line'),
                [P('This is the opening scene of the sample video.'),
                 P('The takeaway line appears when this second phrase starts.')],
                pre=0.1, post=0.7),
        K.end_scene(),               # the standard end card: soft next step, site, Call (301) 615-8289, Text (571) 354-0146, disclaimer
    ])
