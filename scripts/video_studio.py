#!/usr/bin/env python3
"""Honorbrook video studio: animated, hook-first explainers rendered locally on macOS (PIL + numpy + `say` + Swift/AVFoundation).

Each video is a list of scenes with bespoke animated graphics (counters, timelines, bar charts, checklists) driven by the
narration timing, with burned-in word-highlight captions, a quiet music bed and soft UI sounds. Renders a 16:9 file for the
website and a 9:16 master for Shorts / Reels / Facebook.

  python3 scripts/video_studio.py list
  python3 scripts/video_studio.py still part-d 3.0 land     # writes a PNG to the scratch dir for review
  python3 scripts/video_studio.py build part-d              # land -> site/assets/video, port -> social/video_masters
  python3 scripts/video_studio.py build part-d --only land

Facts on screen (all read on the official page this session, 2026-10-14):
  Part D: medicare.gov late enrollment penalty page (63 days after the Initial Enrollment Period; 1% x $38.99 base premium
          (2026) x full uncovered months, rounded to the nearest $.10; lasts as long as you have Medicare drug coverage;
          Extra Help = no penalty).
  ACA:    healthcare.gov dates-and-deadlines (Nov 1; Dec 15 for Jan 1 coverage) and plan categories (60/70/80/90 on average,
          categories say nothing about quality; extra savings only on Silver). Jan 15 / Virginia Jan 29 from scripts/aca_data.
No plan names, no benefits, no enroll-now language (CMS marketing rules): educational only.
"""
import os, sys, json, math, subprocess, tempfile, shutil, wave, hashlib, urllib.request, urllib.error
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = os.environ.get('VIDEO_SCRATCH', os.path.join(tempfile.gettempdir(), 'hbvideo'))
FPS = 30
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import video_scenes as VS
from video_scenes import Ctx, overlay, eio, VIDEOS



# ------------------------------------------------------------------ audio
SR = 44100
CONF = os.path.expanduser('~/.config/honorbrook')   # secrets live here, outside the repo
ENGINE = os.environ.get('VIDEO_VOICE_ENGINE', 'say')   # say | kokoro | elevenlabs | recorded


def _secret(env, fname):
    v = os.environ.get(env)
    if v: return v.strip()
    p = os.path.join(CONF, fname)
    return open(p).read().strip() if os.path.exists(p) else None


def _wav_to_array(path_wav):
    with wave.open(path_wav) as w: x = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(np.float32) / 32768
    return x


def _trim(x):
    f = int(SR * 0.006); x = x.copy(); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    nz = np.nonzero(np.abs(x) > 0.01)[0]
    return x[nz[0]:nz[-1] + 1] if len(nz) else x


def tts(text_, path_wav, tmp, voice=None, rate=178):
    voice = voice or os.environ.get('VIDEO_VOICE', 'Samantha')   # e.g. VIDEO_VOICE='Ava (Premium)' after downloading it in System Settings > Accessibility > Spoken Content
    aiff = path_wav.replace('.wav', '.aiff')
    subprocess.run(['say', '-v', voice, '-r', str(rate), '-o', aiff, text_], check=True)
    subprocess.run(['afconvert', '-f', 'WAVE', '-d', 'LEI16@%d' % SR, '-c', '1', aiff, path_wav], check=True)
    return _trim(_wav_to_array(path_wav))


def eleven_tts(text_, prev, nxt, path_wav):
    """ElevenLabs text-to-speech with the cloned voice. Key and voice id come from env or ~/.config/honorbrook/. Audio is cached so re-renders cost nothing."""
    key, vid = _secret('ELEVENLABS_API_KEY', 'elevenlabs.key'), _secret('ELEVENLABS_VOICE_ID', 'elevenlabs.voice')
    if not key or not vid:
        raise SystemExit('Missing ElevenLabs key or voice id. See VOICE-CLONE-SETUP.md (files ~/.config/honorbrook/elevenlabs.key and elevenlabs.voice).')
    model = os.environ.get('ELEVENLABS_MODEL', 'eleven_multilingual_v2')
    vs = {'stability': float(os.environ.get('EL_STABILITY', '0.5')), 'similarity_boost': float(os.environ.get('EL_SIMILARITY', '0.8')),
          'style': 0.0, 'speed': float(os.environ.get('EL_SPEED', '1.0')), 'use_speaker_boost': True}
    body = {'text': text_, 'model_id': model, 'voice_settings': vs}
    if prev: body['previous_text'] = prev
    if nxt: body['next_text'] = nxt
    ck = hashlib.sha1(json.dumps([vid, body], sort_keys=True).encode()).hexdigest()[:16]
    cdir = os.path.join(SCRATCH, 'eleven_cache'); os.makedirs(cdir, exist_ok=True)
    mp3 = os.path.join(cdir, ck + '.mp3')
    if not os.path.exists(mp3):
        req = urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/%s?output_format=mp3_44100_128' % vid, data=json.dumps(body).encode(),
                                     headers={'xi-api-key': key, 'Content-Type': 'application/json', 'Accept': 'audio/mpeg', 'User-Agent': 'honorbrook-video/1.0'})
        try:
            data = urllib.request.urlopen(req, timeout=120).read()
        except urllib.error.HTTPError as e:
            raise SystemExit('ElevenLabs error %s: %s' % (e.code, e.read().decode()[:400]))
        open(mp3, 'wb').write(data)
    subprocess.run(['afconvert', '-f', 'WAVE', '-d', 'LEI16@%d' % SR, '-c', '1', mp3, path_wav], check=True)
    return _trim(_wav_to_array(path_wav))


KOKORO_PY = os.path.expanduser('~/.cache/honorbrook-tts/venv/bin/python')
KOKORO_VOICE = os.environ.get('VIDEO_KOKORO_VOICE', 'af_heart')
KOKORO_SPEED = float(os.environ.get('VIDEO_KOKORO_SPEED', '0.96'))


def kokoro_batch(says, tmp, voice=None, speed=None):
    """Render every line with the free local Kokoro voice (one model load). Lines are cached, so re-renders are instant."""
    voice, speed = voice or KOKORO_VOICE, speed or KOKORO_SPEED
    if not os.path.exists(KOKORO_PY): raise SystemExit('Kokoro is not installed (expected %s).' % KOKORO_PY)
    cdir = os.path.join(SCRATCH, 'kokoro_cache'); os.makedirs(cdir, exist_ok=True)
    keys = [hashlib.sha1(json.dumps([voice, speed, t]).encode()).hexdigest()[:16] for t in says]
    jobs = [{'text': t, 'voice': voice, 'speed': speed, 'out': os.path.join(cdir, k + '.wav')} for t, k in zip(says, keys) if not os.path.exists(os.path.join(cdir, k + '.wav'))]
    if jobs:
        jf = os.path.join(tmp, 'kokoro_jobs.json'); json.dump(jobs, open(jf, 'w'))
        subprocess.run([KOKORO_PY, os.path.join(ROOT, 'scripts', 'kokoro_say.py'), jf], check=True, stdout=subprocess.DEVNULL)
    out = []
    for i, k in enumerate(keys):
        w44 = os.path.join(tmp, 'k%d.wav' % i)
        subprocess.run(['afconvert', '-f', 'WAVE', '-d', 'LEI16@%d' % SR, '-c', '1', os.path.join(cdir, k + '.wav'), w44], check=True)
        out.append(_trim(_wav_to_array(w44)))
    return out


def split_takes(path, n, tmp):
    """Split one long recording into n phrase takes at the pauses between lines."""
    wav = os.path.join(tmp, 'recorded.wav')
    subprocess.run(['afconvert', '-f', 'WAVE', '-d', 'LEI16@%d' % SR, '-c', '1', path, wav], check=True)
    x = _wav_to_array(wav); hop = int(SR * 0.01); frames = len(x) // hop
    env = np.sqrt(np.mean(x[:frames * hop].reshape(frames, hop) ** 2, axis=1))
    noise, speech = np.percentile(env, 10), np.percentile(env, 90)
    thr = noise + 0.12 * (speech - noise); quiet = env < thr
    found = 0
    for min_sil in (0.8, 0.65, 0.5, 0.4, 0.3, 0.25, 0.2):
        need = int(min_sil / 0.01); segs, start, run = [], None, 0
        for i in range(frames + 1):
            q = quiet[i] if i < frames else True
            if not q:
                if start is None: start = i
                run = 0
            else:
                if start is not None:
                    run += 1
                    if run >= need:
                        segs.append((start, i - run + 1)); start = None; run = 0
        found = len(segs)
        if found == n:
            return [x[max(0, a * hop - int(SR * 0.04)):min(len(x), b * hop + int(SR * 0.06))] for a, b in segs]
    raise SystemExit('Found %d takes in %s but the script has %d lines. Leave a clear one-second pause between lines, or tell me and I will adjust.' % (found, path, n))


def sfx_wave(kind):
    n = int(SR * 0.6); t = np.arange(n) / SR
    if kind == 'ding': y = np.sin(2 * np.pi * 1318.5 * t) * np.exp(-t * 9) * 0.5 + np.sin(2 * np.pi * 1975.5 * t) * np.exp(-t * 14) * 0.25
    elif kind == 'tick': y = np.sin(2 * np.pi * 880 * t) * np.exp(-t * 38) * 0.45
    elif kind == 'thump': y = np.sin(2 * np.pi * (70 + 40 * np.exp(-t * 12)) * t) * np.exp(-t * 7) * 0.9
    else: y = t * 0
    return (y * 0.20).astype(np.float32)


def load_music(path, n, tmp):
    wav = os.path.join(tmp, 'music.wav')
    subprocess.run(['afconvert', '-f', 'WAVE', '-d', 'LEI16@%d' % SR, '-c', '1', path, wav], check=True)
    m = _wav_to_array(wav)
    reps = int(math.ceil(n / max(len(m), 1)))
    return np.tile(m, reps)[:n]


def _fft_filter(x, curve):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * curve(f), len(x)).astype(np.float32)


def _frame_env(x, hop_s=0.005):
    hop = int(SR * hop_s); n = len(x) // hop
    return np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, axis=1)) + 1e-9, hop


def _smooth_gain(target, hop_s, attack, release):
    a, r = 1 - math.exp(-hop_s / attack), 1 - math.exp(-hop_s / release)
    g = np.empty(len(target)); prev = 1.0
    for i, t in enumerate(target):
        prev += (a if t < prev else r) * (t - prev); g[i] = prev      # gain falls fast (attack), recovers slowly (release)
    return g


def polish_voice(x, strength=1.0):
    """Studio chain for a synthetic or phone-recorded voice: high-pass, warmth, presence, de-ess, gentle compression, short room tail."""
    L = lambda db: 10 ** (db * strength / 20)
    hp = lambda f: (f / 80.0) ** 2 / (1 + (f / 80.0) ** 2)
    warm = lambda f: 1 + (L(1.8) - 1) / (1 + (f / 220.0) ** 2)
    pres = lambda f: 1 + (L(2.6) - 1) * np.exp(-0.5 * (np.log2(np.maximum(f, 1) / 3200.0) / 0.55) ** 2)
    x = _fft_filter(x, lambda f: hp(f) * warm(f) * pres(f))
    # de-esser: duck the 5-9.5 kHz band when it spikes
    band = _fft_filter(x, lambda f: ((f > 5000) & (f < 9500)).astype(float) * np.minimum(1, (f - 4500) / 600) * np.minimum(1, (9800 - f) / 600))
    env, hop = _frame_env(band); thr = np.percentile(env, 88) * 0.9
    g = np.clip(thr / env, 0.35, 1.0) ** 0.8; g = _smooth_gain(g, 0.005, 0.002, 0.04)
    gi = np.interp(np.arange(len(x)), np.arange(len(g)) * hop, g).astype(np.float32)
    x = x - band * (1 - gi)
    # compressor: 2.4:1 above -26 dBFS, 8 ms attack, 140 ms release, then make-up
    env, hop = _frame_env(x, 0.01); db = 20 * np.log10(env); thr_db, ratio = -26.0, 2.4
    gain_db = np.where(db > thr_db, (thr_db - db) * (1 - 1 / ratio), 0.0) * strength
    g = _smooth_gain(10 ** (gain_db / 20), 0.01, 0.008, 0.14)
    x = x * np.interp(np.arange(len(x)), np.arange(len(g)) * hop, g).astype(np.float32)
    # room: a few early reflections and a short soft tail, about -23 dB wet
    rng = np.random.default_rng(7); n = int(SR * 0.32); t = np.arange(n) / SR
    ir = rng.normal(0, 1, n) * np.exp(-t / 0.075); ir = _fft_filter(ir.astype(np.float32), lambda f: 1 / (1 + (f / 4500.0) ** 2)) if False else ir.astype(np.float32)
    ir[: int(SR * 0.012)] = 0
    for ms, a in ((11, 0.35), (19, 0.25), (31, 0.18)): ir[int(SR * ms / 1000)] += a * np.abs(ir).max() * 4
    ir /= np.sqrt(np.sum(ir ** 2))
    wet = np.fft.irfft(np.fft.rfft(x, len(x) + n) * np.fft.rfft(ir, len(x) + n))[:len(x)].astype(np.float32)
    wet = _fft_filter(wet, lambda f: 1 / (1 + (f / 5000.0) ** 2))
    x = x + wet * L(-23) * 0.9 * (np.sqrt(np.mean(x ** 2)) / max(np.sqrt(np.mean(wet ** 2)), 1e-9))
    return x


def loudness_lufs(x):
    """Approximate BS.1770 integrated loudness (K-weighting by frequency-domain curves, 400 ms blocks, two gates)."""
    k = _fft_filter(x, lambda f: (1 + (10 ** (4 / 20) - 1) * f ** 2 / (f ** 2 + 1700.0 ** 2)) * f ** 2 / (f ** 2 + 38.0 ** 2))
    b, st = int(SR * 0.4), int(SR * 0.1)
    ms = np.array([np.mean(k[i:i + b] ** 2) for i in range(0, max(len(k) - b, 1), st)]) + 1e-12
    lu = -0.691 + 10 * np.log10(ms); ms = ms[lu > -70]
    if not len(ms): return -70.0
    rel = -0.691 + 10 * np.log10(np.mean(ms)) - 10; ms = ms[(-0.691 + 10 * np.log10(ms)) > rel]
    return -0.691 + 10 * np.log10(np.mean(ms))


def finish_mix(mix, target=-14.0):
    """Level to about -14 LUFS (what YouTube plays back at), then soft-limit peaks to about -1 dBFS."""
    cur = loudness_lufs(mix); y = mix * 10 ** ((target - cur) / 20)
    y = np.tanh(y / 0.95) * 0.95 if np.abs(y).max() > 0.9 else y
    return np.clip(y, -0.891, 0.891).astype(np.float32), cur


DEFAULT_MUSIC = os.path.join(ROOT, 'social', 'music', 'mixkit-serene-view-443.mp3')   # Mixkit Stock Music Free License, see README there


def _carve_voice_band(bed):
    """Make room for speech: roll off rumble and dip 1.5-4 kHz about 3 dB in the music."""
    dip = lambda f: 1 - (1 - 10 ** (-3 / 20)) * np.exp(-0.5 * (np.log2(np.maximum(f, 1) / 2500.0) / 0.8) ** 2)
    return _fft_filter(bed, lambda f: (f ** 2 / (f ** 2 + 60.0 ** 2)) * dip(f))


def duck_music(voice, bed, total):
    """Music sits about 18 dB under the voice while speaking and rises about 6 dB in pauses (attack 20 ms, release 350 ms)."""
    hop = int(SR * 0.01); frames = len(voice) // hop
    rms = np.sqrt(np.mean(voice[:frames * hop].reshape(frames, hop) ** 2, axis=1))
    active = rms > max(0.01, 0.12 * np.percentile(rms, 95))
    spk = np.sqrt(np.mean(rms[active] ** 2)) if active.any() else 0.1
    a, r = 1 - math.exp(-0.01 / 0.02), 1 - math.exp(-0.01 / 0.35)
    g = np.zeros(frames); prev = 0.0
    for i in range(frames):
        tgt = 1.0 if active[i] else 0.0
        prev += (a if tgt > prev else r) * (tgt - prev); g[i] = prev
    speak_lvl = spk * 10 ** (-18 / 20); pause_lvl = speak_lvl * 10 ** (6 / 20)
    lvl = pause_lvl - g * (pause_lvl - speak_lvl)
    env = np.interp(np.arange(len(bed)), np.arange(frames) * hop, lvl).astype(np.float32)
    bed = bed / max(np.sqrt(np.mean(bed ** 2)), 1e-6)
    tt = np.arange(len(bed)) / SR
    fade = np.minimum(1, tt / 1.5) * np.minimum(1, np.maximum(0, (total - tt)) / 1.5)
    return (bed * env * fade).astype(np.float32)


def build_audio(video, tmp):
    """Returns (mix, timeline, total) where timeline = per-scene dict(t0, t1, ph=[(s,e)...]) in global seconds."""
    pieces, tl, events = [], [], []
    says = [say for sc in video['scenes'] for _, say in sc['phr']]
    takes = None
    if ENGINE == 'recorded':
        src = os.environ.get('VIDEO_RECORDED_FILE')
        if not src: raise SystemExit('Set VIDEO_RECORDED_FILE to the voice recording (m4a/wav/mp3) for this video.')
        takes = split_takes(src, len(says), tmp)
    if ENGINE == 'kokoro': takes = kokoro_batch(says, tmp)
    t = 0.25; k = 0
    for si, sc in enumerate(video['scenes']):
        t0 = t; tp = t + sc.get('pre', 0.15); ph = []
        for pi, (cap, say) in enumerate(sc['phr']):
            path_wav = os.path.join(tmp, 's%d_%d.wav' % (si, pi))
            if ENGINE == 'elevenlabs': wav = eleven_tts(say, says[k - 1] if k else None, says[k + 1] if k + 1 < len(says) else None, path_wav)
            elif ENGINE in ('recorded', 'kokoro'): wav = _trim(takes[k])
            else: wav = tts(say, path_wav, tmp)
            k += 1
            d = len(wav) / SR
            pieces.append((tp, wav)); ph.append((tp, tp + d)); tp += d + (0.2 if ENGINE == 'say' else 0.3)
        t1 = ph[-1][1] + sc.get('post', 0.6)
        tl.append(dict(t0=t0, t1=t1, ph=ph)); t = t1
        if sc.get('sfx'): events += [(t0 + lt, kd) for lt, kd in sc['sfx']([(a - t0, b - t0) for a, b in ph])]
    total = t + 0.5
    n = int(SR * total) + SR
    voice = np.zeros(n, np.float32)
    for st, w in pieces:
        i = int(st * SR); voice[i:i + len(w)] += w
    if os.environ.get('VIDEO_POLISH', '1') != '0': voice = polish_voice(voice, 0.6 if ENGINE in ('elevenlabs', 'recorded') else 1.0)
    voice = voice / max(np.abs(voice).max(), 1e-6) * 0.86
    tt = np.arange(n) / SR
    mfile = os.environ.get('VIDEO_MUSIC_FILE', DEFAULT_MUSIC)
    if mfile and mfile != 'none' and os.path.exists(mfile): bed = _carve_voice_band(load_music(mfile, n, tmp))
    else: bed = sum(np.sin(2 * np.pi * f * tt + kk) * aa for kk, (f, aa) in enumerate([(110, 1.0), (164.81, 0.8), (220, 0.6), (246.94, 0.35), (277.18, 0.3)])) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.07 * tt))
    print('music:', os.path.basename(mfile) if (mfile and mfile != 'none' and os.path.exists(mfile)) else 'generated pad')
    mix = voice + duck_music(voice, np.asarray(bed, np.float32), total)
    for te, kd in events:
        w = sfx_wave(kd); i = int(te * SR); mix[i:i + len(w)] += w[:max(0, min(len(w), n - i))]
    mix, cur = finish_mix(mix)
    print('audio: %s voice, mix was %.1f LUFS before leveling, now about -14 LUFS' % (ENGINE, cur))
    return mix, tl, total


def write_wav(path, x):
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes())


# ------------------------------------------------------------------ encoder (Swift/AVFoundation, raw BGRA frames on stdin)
SWIFT = r'''
import AVFoundation
import Foundation
let a = CommandLine.arguments
let outPath = a[1], audioPath = a[2]
let W = Int(a[3])!, H = Int(a[4])!, fps = Int(a[5])!, n = Int(a[6])!, br = Int(a[7])!
let silent = outPath + ".v.mp4"
try? FileManager.default.removeItem(atPath: silent); try? FileManager.default.removeItem(atPath: outPath)
let w = try! AVAssetWriter(outputURL: URL(fileURLWithPath: silent), fileType: .mp4)
let settings: [String: Any] = [AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: W, AVVideoHeightKey: H,
  AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: br, AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
    AVVideoMaxKeyFrameIntervalKey: fps * 2, AVVideoExpectedSourceFrameRateKey: fps, AVVideoAllowFrameReorderingKey: false]]
let inp = AVAssetWriterInput(mediaType: .video, outputSettings: settings)
inp.expectsMediaDataInRealTime = false
let adap = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: inp, sourcePixelBufferAttributes: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA, kCVPixelBufferWidthKey as String: W, kCVPixelBufferHeightKey as String: H])
w.add(inp); w.startWriting(); w.startSession(atSourceTime: .zero)
let fsz = W * H * 4
let si = FileHandle.standardInput
var frame = 0
while frame < n {
  var data = Data(capacity: fsz)
  while data.count < fsz { let ch = si.readData(ofLength: fsz - data.count); if ch.isEmpty { break }; data.append(ch) }
  if data.count < fsz { print("short read at frame", frame); break }
  while !inp.isReadyForMoreMediaData { Thread.sleep(forTimeInterval: 0.002) }
  var pb: CVPixelBuffer?
  CVPixelBufferPoolCreatePixelBuffer(nil, adap.pixelBufferPool!, &pb)
  CVPixelBufferLockBaseAddress(pb!, [])
  let base = CVPixelBufferGetBaseAddress(pb!)!; let bpr = CVPixelBufferGetBytesPerRow(pb!)
  data.withUnsafeBytes { raw in for y in 0..<H { memcpy(base + y * bpr, raw.baseAddress! + y * W * 4, W * 4) } }
  CVPixelBufferUnlockBaseAddress(pb!, [])
  if !adap.append(pb!, withPresentationTime: CMTime(value: CMTimeValue(frame), timescale: CMTimeScale(fps))) { print("append failed", frame, String(describing: w.error)); break }
  frame += 1
}
inp.markAsFinished()
let sem = DispatchSemaphore(value: 0)
w.finishWriting { sem.signal() }; sem.wait()
print("writer", w.status.rawValue, String(describing: w.error))
let comp = AVMutableComposition()
let va = AVURLAsset(url: URL(fileURLWithPath: silent)); let aa = AVURLAsset(url: URL(fileURLWithPath: audioPath))
let sm = DispatchSemaphore(value: 0)
va.loadValuesAsynchronously(forKeys: ["tracks", "duration"]) { sm.signal() }; sm.wait()
aa.loadValuesAsynchronously(forKeys: ["tracks", "duration"]) { sm.signal() }; sm.wait()
let vt = comp.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid)!
try! vt.insertTimeRange(CMTimeRange(start: .zero, duration: va.duration), of: va.tracks(withMediaType: .video)[0], at: .zero)
let at = comp.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid)!
let adur = CMTimeMinimum(aa.duration, va.duration)
try! at.insertTimeRange(CMTimeRange(start: .zero, duration: adur), of: aa.tracks(withMediaType: .audio)[0], at: .zero)
let ex = AVAssetExportSession(asset: comp, presetName: AVAssetExportPresetPassthrough)!
ex.outputURL = URL(fileURLWithPath: outPath); ex.outputFileType = .mp4; ex.shouldOptimizeForNetworkUse = true
let s2 = DispatchSemaphore(value: 0)
ex.exportAsynchronously { s2.signal() }; s2.wait()
try? FileManager.default.removeItem(atPath: silent)
print(ex.status == .completed ? "OK" : "FAIL \(String(describing: ex.error))")
'''


# ------------------------------------------------------------------ rendering
def scene_at(c, video, tl, si, t):
    img = c.frame(t); sc = video['scenes'][si]; s = tl[si]
    ph = [(a - s['t0'], b - s['t0']) for a, b in s['ph']]
    sc['draw'](c, img, t - s['t0'], ph)
    return VS.zoom(img, 1 + 0.03 * clamp01((t - s['t0']) / max(s['t1'] - s['t0'], 1.0)))   # slow push-in


def clamp01(x): return max(0.0, min(1.0, x))


def render_frame(c, video, tl, total, t, caps):
    si = max(i for i, s in enumerate(tl) if s['t0'] <= t + 1e-9) if t >= tl[0]['t0'] else 0
    img = scene_at(c, video, tl, si, t)
    if si > 0 and t - tl[si]['t0'] < 0.35:
        x = eio((t - tl[si]['t0']) / 0.35)
        img = Image.blend(VS.zoom(scene_at(c, video, tl, si - 1, t), 1 + 0.05 * x), VS.zoom(img, 1 + 0.05 * (1 - x)), x)
    cap = next(((s, e, w) for s, e, w in caps if s - 0.08 <= t <= e + 0.7), None)
    overlay(c, img, t, total, cap)
    return img


def prepare(name):
    VS.VOICE_NOTE = 'Narration: AI voice cloned from Luay Sadqi\'s own voice, with his permission.' if ENGINE == 'elevenlabs' else ''
    video = VIDEOS[name]
    tmp = os.path.join(SCRATCH, name); os.makedirs(tmp, exist_ok=True)
    mix, tl, total = build_audio(video, tmp)
    caps = []
    for sc, s in zip(video['scenes'], tl):
        for (cap, _), (a, b) in zip(sc['phr'], s['ph']): caps.append((a, b, cap.split()))
    return video, tmp, mix, tl, total, caps


def fmt_size(f): return (1280, 720) if f == 'land' else (1080, 1920)


def still(name, t, f):
    video, tmp, mix, tl, total, caps = prepare(name)
    c = Ctx(*fmt_size(f)); out = os.path.join(SCRATCH, '%s-%s-%.1f.png' % (name, f, t))
    render_frame(c, video, tl, total, t, caps).save(out); print(out, 'total', round(total, 1))


def build(name, only=None):
    video, tmp, mix, tl, total, caps = prepare(name)
    wav = os.path.join(tmp, 'mix.wav'); m4a = os.path.join(tmp, 'mix.m4a'); write_wav(wav, mix)
    subprocess.run(['afconvert', '-f', 'm4af', '-d', 'aac', '-b', '128000', wav, m4a], check=True)
    swift = os.path.join(tmp, 'enc.swift'); open(swift, 'w').write(SWIFT)
    exe = os.path.join(SCRATCH, 'enc')
    if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(__file__):
        r = subprocess.run(['swiftc', '-O', swift, '-o', exe], capture_output=True, text=True)
        if r.returncode: print(r.stderr[-1500:]); raise SystemExit('swiftc failed')
    n = int(total * FPS)
    for f in ([only] if only else ['land', 'port']):
        c = Ctx(*fmt_size(f))
        outdir = os.path.join(ROOT, 'site', 'assets', 'video') if f == 'land' else os.path.join(ROOT, 'social', 'video_masters')
        os.makedirs(outdir, exist_ok=True)
        final = os.path.join(outdir, video['slug'] + ('.mp4' if f == 'land' else '-vertical.mp4'))
        out = os.path.join(SCRATCH, 'out_' + os.path.basename(final))
        br = 1_500_000 if f == 'land' else 2_600_000
        p = subprocess.Popen([exe, out, m4a, str(c.W), str(c.H), str(FPS), str(n), str(br)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=False)
        for i in range(n):
            img = render_frame(c, video, tl, total, i / FPS, caps)
            p.stdin.write(img.tobytes('raw', 'BGRX'))
            if i % 150 == 0: print(f, i, '/', n, flush=True)
        p.stdin.close(); res = p.stdout.read().decode(); p.wait(); print(res.strip())
        if f == 'land':
            render_frame(c, video, tl, total, video['poster'], caps).convert('RGB').save(os.path.join(outdir, video['slug'] + '.jpg'), quality=86)
        if os.path.exists(out) and os.path.getsize(out) > 100_000: shutil.move(out, final)
        else: raise SystemExit('encode failed for ' + final)
        print(f, 'wrote', final, os.path.getsize(final) // 1024, 'KB', round(total, 1), 's')
    json.dump(dict(slug=video['slug'], title=video['title'], duration=round(total, 1), transcript=[cap for sc in video['scenes'] for cap, _ in sc['phr']]),
              open(os.path.join(tmp, 'meta.json'), 'w'), indent=1)


def sample(name, voices, nscenes=2):
    """Audio-only voice shootout: first scenes of a video in each Kokoro voice, with polish, music bed and loudness leveling. Writes m4a files."""
    global ENGINE, KOKORO_VOICE
    ENGINE = 'kokoro'
    video = dict(VIDEOS[name]); video['scenes'] = video['scenes'][:nscenes]
    outdir = os.path.join(ROOT, 'social', 'voice_samples'); os.makedirs(outdir, exist_ok=True)
    for v in voices:
        KOKORO_VOICE = v; tmp = os.path.join(SCRATCH, 'sample_' + v.replace('+', '_')); os.makedirs(tmp, exist_ok=True)
        mix, tl, total = build_audio(video, tmp)
        wav = os.path.join(tmp, 'mix.wav'); write_wav(wav, mix)
        out = os.path.join(outdir, '%s-%s.m4a' % (name, v.replace('+', '-')))
        subprocess.run(['afconvert', '-f', 'm4af', '-d', 'aac', '-b', '128000', wav, out], check=True)
        print(v, '->', out, round(total, 1), 's')


def embed(name):
    """Update the blog page that embeds this video: heading, VideoObject duration/description/transcript, transcript text."""
    import re, html as H
    video = VIDEOS[name]; meta = json.load(open(os.path.join(SCRATCH, name, 'meta.json')))
    path = os.path.join(ROOT, 'site', 'blog', video['page'] + '.html'); h = open(path, encoding='utf-8').read()
    secs = int(round(meta['duration'])); iso = 'PT%dM%dS' % divmod(secs, 60)
    words = round(secs / 5) * 5
    title = '%s in about %d seconds' % (video['watch'], words)
    h = re.sub(r'<h2>Watch: .*?</h2>', '<h2>Watch: %s</h2>' % title, h, count=1)
    transcript = ' '.join(meta['transcript'])
    m = re.search(r'<script type="application/ld\+json">\s*(\{[^<]*?"@type": "VideoObject".*?\})\s*</script>', h, re.S)
    j = json.loads(m.group(1)); j.update(name=title, description=video['vdesc'], duration=iso, transcript=transcript)
    h = h[:m.start(1)] + json.dumps(j, indent=1, ensure_ascii=False) + h[m.end(1):]
    h = re.sub(r'(<details><summary>Video transcript</summary><div class="a">).*?(</div></details>)', lambda mm: mm.group(1) + H.escape(transcript, quote=False) + mm.group(2), h, count=1, flags=re.S)
    open(path, 'w', encoding='utf-8').write(h); print('patched', os.path.relpath(path, ROOT), iso, title)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] == 'list': print(list(VIDEOS))
    elif a[0] == 'still': still(a[1], float(a[2]), a[3] if len(a) > 3 else 'land')
    elif a[0] == 'build': build(a[1], a[a.index('--only') + 1] if '--only' in a else None)
    elif a[0] == 'embed': embed(a[1])
    elif a[0] == 'sample': sample(a[1], a[2].split(','), int(a[3]) if len(a) > 3 else 2)
