#!/usr/bin/env python3
"""Build a short narrated explainer video (mp4) from a scene list. macOS only: PIL slides + `say` voice + Swift/AVFoundation.

Usage: python3 scripts/make_video.py scripts/videos/<name>.json
Writes site/assets/video/<slug>.mp4 and <slug>.jpg (poster). No third-party tools needed.
"""
import json, os, subprocess, sys, textwrap, tempfile, shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1280, 720
NAVY, NAVY_D, GOLD, CREAM, WHITE = (27, 47, 75), (20, 35, 57), (201, 162, 39), (250, 247, 240), (255, 255, 255)
FONT_B = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
FONT_R = '/System/Library/Fonts/Supplemental/Arial.ttf'
LOGO = os.path.join(ROOT, 'site', 'assets', 'logo-static.png')


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


def slide(scene, idx, total, brand_line, disclaimer, path):
    img = Image.new('RGB', (W, H), NAVY_D)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 14, H], fill=GOLD)
    try:
        lg = Image.open(LOGO).convert('RGBA'); lg.thumbnail((70, 84)); img.paste(lg, (W - 110, 30), lg)
    except Exception:
        pass
    d.text((70, 44), brand_line, font=font(FONT_B, 26), fill=GOLD)
    kind = scene.get('kind', 'bullets')
    y = 150
    head = scene['head']
    hf = font(FONT_B, 58 if kind != 'title' else 66)
    for ln in wrap(d, head, hf, W - 160):
        d.text((70, y), ln, font=hf, fill=WHITE); y += 74
    y += 18
    bf = font(FONT_R, 38)
    for b in scene.get('bullets', []):
        lines = wrap(d, b, bf, W - 220)
        d.ellipse([74, y + 14, 90, y + 30], fill=GOLD)
        for ln in lines:
            d.text((112, y), ln, font=bf, fill=CREAM); y += 52
        y += 14
    if scene.get('big'):
        bigf = font(FONT_B, 54)
        for ln in wrap(d, scene['big'], bigf, W - 160):
            d.text((70, y), ln, font=bigf, fill=GOLD); y += 70
    d.text((70, H - 96), disclaimer, font=font(FONT_R, 20), fill=(170, 185, 205))
    d.text((70, H - 62), 'honorbrook-insurance.com  ·  (571) 354-0146', font=font(FONT_B, 26), fill=WHITE)
    d.text((W - 150, H - 62), f'{idx}/{total}', font=font(FONT_R, 24), fill=(170, 185, 205))
    img.save(path)


SWIFT = r'''
import AVFoundation
import AppKit
let a = CommandLine.arguments
let outPath = a[1]; let audioPath = a[2]; let n = Int(a[3])!
var durs: [Double] = []; var imgs: [String] = []
for i in 0..<n { imgs.append(a[4 + i]); durs.append(Double(a[4 + n + i])!) }
let silent = outPath + ".silent.mp4"
try? FileManager.default.removeItem(atPath: silent); try? FileManager.default.removeItem(atPath: outPath)
let w = try! AVAssetWriter(outputURL: URL(fileURLWithPath: silent), fileType: .mp4)
let settings: [String: Any] = [AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: 1280, AVVideoHeightKey: 720, AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: 1500000, AVVideoProfileLevelKey: AVVideoProfileLevelH264MainAutoLevel, AVVideoMaxKeyFrameIntervalKey: 25]]
let inp = AVAssetWriterInput(mediaType: .video, outputSettings: settings)
let adap = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: inp, sourcePixelBufferAttributes: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32ARGB, kCVPixelBufferWidthKey as String: 1280, kCVPixelBufferHeightKey as String: 720])
w.add(inp); w.startWriting(); w.startSession(atSourceTime: .zero)
func buf(_ path: String) -> CVPixelBuffer {
  let img = NSImage(contentsOfFile: path)!
  var pb: CVPixelBuffer?
  CVPixelBufferCreate(nil, 1280, 720, kCVPixelFormatType_32ARGB, nil, &pb)
  CVPixelBufferLockBaseAddress(pb!, [])
  let ctx = CGContext(data: CVPixelBufferGetBaseAddress(pb!), width: 1280, height: 720, bitsPerComponent: 8, bytesPerRow: CVPixelBufferGetBytesPerRow(pb!), space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue)!
  let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil)!
  ctx.draw(cg, in: CGRect(x: 0, y: 0, width: 1280, height: 720))
  CVPixelBufferUnlockBaseAddress(pb!, [])
  return pb!
}
var t = 0.0
for i in 0..<n {
  let b = buf(imgs[i])
  // one frame per scene (slideshow): hold until the next frame; keeps the encoder load tiny
  for rep in 0..<2 {
    while !inp.isReadyForMoreMediaData { Thread.sleep(forTimeInterval: 0.005) }
    let ok = adap.append(b, withPresentationTime: CMTime(seconds: t + Double(rep) * 0.5, preferredTimescale: 600))
    if !ok { print("append failed scene", i, w.status.rawValue, String(describing: w.error)); break }
  }
  t += durs[i]
}
w.endSession(atSourceTime: CMTime(seconds: t, preferredTimescale: 600))
inp.markAsFinished()
let sem = DispatchSemaphore(value: 0)
w.finishWriting { sem.signal() }; sem.wait()
print("writer", w.status.rawValue, String(describing: w.error))
let comp = AVMutableComposition()
let va = AVURLAsset(url: URL(fileURLWithPath: silent)); let aa = AVURLAsset(url: URL(fileURLWithPath: audioPath))
for asset in [va, aa] {
  let sm = DispatchSemaphore(value: 0)
  asset.loadValuesAsynchronously(forKeys: ["tracks", "duration"]) { sm.signal() }
  sm.wait()
}
let vt = comp.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid)!
try! vt.insertTimeRange(CMTimeRange(start: .zero, duration: va.duration), of: va.tracks(withMediaType: .video)[0], at: .zero)
let at = comp.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid)!
try! at.insertTimeRange(CMTimeRange(start: .zero, duration: aa.duration), of: aa.tracks(withMediaType: .audio)[0], at: .zero)
let ex = AVAssetExportSession(asset: comp, presetName: AVAssetExportPreset1280x720)!
ex.outputURL = URL(fileURLWithPath: outPath); ex.outputFileType = .mp4; ex.shouldOptimizeForNetworkUse = true
let s2 = DispatchSemaphore(value: 0)
ex.exportAsynchronously { s2.signal() }; s2.wait()
try? FileManager.default.removeItem(atPath: silent)
print(ex.status == .completed ? "OK" : "FAIL \(String(describing: ex.error))")
'''


def main(cfg_path):
    cfg = json.load(open(cfg_path))
    slug = cfg['slug']
    tmp = tempfile.mkdtemp(prefix='hbvid_')
    scenes = cfg['scenes']
    pngs, durs, auds = [], [], []
    for i, sc in enumerate(scenes):
        p = os.path.join(tmp, f's{i}.png')
        slide(sc, i + 1, len(scenes), cfg.get('brand', 'HONORBROOK INSURANCE'), cfg['disclaimer'], p)
        aiff = os.path.join(tmp, f's{i}.aiff')
        subprocess.run(['say', '-v', cfg.get('voice', 'Samantha'), '-r', str(cfg.get('rate', 165)), '-o', aiff, sc['say']], check=True)
        info = subprocess.check_output(['afinfo', aiff], text=True)
        dur = float([l for l in info.splitlines() if 'estimated duration' in l][0].split()[2])
        pngs.append(p); durs.append(round(dur + 0.6, 2)); auds.append(aiff)
    # concatenate narration with small gaps into one wav
    import wave, struct
    merged = os.path.join(tmp, 'all.wav')
    outw = None
    for aiff, d in zip(auds, durs):
        wav = aiff.replace('.aiff', '.wav')
        subprocess.run(['afconvert', '-f', 'WAVE', '-d', 'LEI16@22050', '-c', '1', aiff, wav], check=True)
        with wave.open(wav) as r:
            frames = r.readframes(r.getnframes()); params = r.getparams()
        pad = int(params.framerate * (d - r.getnframes() / params.framerate)) * params.sampwidth
        if outw is None:
            outw = wave.open(merged, 'wb'); outw.setparams(params)
        outw.writeframes(frames); outw.writeframes(b'\x00' * max(pad, 0))
    outw.close()
    outdir = os.path.join(ROOT, 'site', 'assets', 'video'); os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, slug + '.mp4')
    swift = os.path.join(tmp, 'mk.swift'); open(swift, 'w').write(SWIFT)
    args = ['swiftc', '-O', swift, '-o', os.path.join(tmp, 'mk')]
    subprocess.run(args, check=True, capture_output=True)
    res = subprocess.run([os.path.join(tmp, 'mk'), out, merged, str(len(pngs))] + pngs + [str(d) for d in durs], capture_output=True, text=True)
    print(res.stdout.strip(), res.stderr.strip()[:300])
    shutil.copy(pngs[0], os.path.join(outdir, slug + '.jpg'))
    # jpg poster: convert from png
    Image.open(pngs[0]).convert('RGB').save(os.path.join(outdir, slug + '.jpg'), quality=85)
    print('duration_sec', round(sum(durs), 1), 'size_kb', os.path.getsize(out) // 1024 if os.path.exists(out) else 'MISSING')
    if os.path.exists(out): shutil.rmtree(tmp)
    else: print('kept', tmp)


if __name__ == '__main__':
    main(sys.argv[1])
