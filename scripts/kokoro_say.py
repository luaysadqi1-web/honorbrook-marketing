#!/usr/bin/env python3
"""Free local neural voice (Kokoro-82M, Apache 2.0) for the video studio. Runs inside the private venv at ~/.cache/honorbrook-tts.

  ~/.cache/honorbrook-tts/venv/bin/python scripts/kokoro_say.py jobs.json

jobs.json = [{"text": "...", "voice": "af_heart", "speed": 1.0, "out": "/path/line.wav"}, ...]; writes 24 kHz mono 16-bit WAVs.
Voices graded by the model author: af_heart A, af_bella A-, af_nicole B-; best male voices (am_michael, am_fenrir, am_puck) are C+.
"""
import json, os, sys, wave
import numpy as np
from kokoro_onnx import Kokoro

HOME = os.path.expanduser('~/.cache/honorbrook-tts/dl')
k = Kokoro(os.path.join(HOME, 'kokoro-v1.0.onnx'), os.path.join(HOME, 'voices-v1.0.bin'))
for job in json.load(open(sys.argv[1])):
    voice = job.get('voice', 'af_heart')
    if '+' in voice:   # blend, e.g. "af_heart+af_bella"
        names = voice.split('+'); style = sum(k.get_voice_style(n) for n in names) / len(names)
    else:
        style = voice
    samples, sr = k.create(job['text'], voice=style, speed=float(job.get('speed', 1.0)), lang='en-us')
    pcm = (np.clip(samples, -1, 1) * 32767).astype('<i2')
    with wave.open(job['out'], 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
    print(job['out'], round(len(samples) / sr, 2), 's')
