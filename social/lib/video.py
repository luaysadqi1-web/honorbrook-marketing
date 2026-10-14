"""
Honorbrook short video renderer: the infographic builds up one card at a time.

Silent H.264 MP4, 1200x900, ~14-20s, so it works muted in a feed (the words are
the content). Text is vetted by infographic.vet() (compliance linter) before any
frame is drawn, and the Medicare disclaimer is on every frame when required.

ffmpeg comes from PATH, or from the imageio-ffmpeg package in social/.venv.
  python3 lib/video.py spec.json [--out DIR]
"""
import hashlib, json, os, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import infographic

HEAD_S, CARD_S, END_S = 2.0, 3.0, 3.5
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "..", "social-assets", "videos")


def ffmpeg_exe():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        pass
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for sp in (os.path.join(here, ".venv", "lib", "python3.9", "site-packages"),):
        if os.path.isdir(sp):
            sys.path.insert(0, sp)
            import imageio_ffmpeg
            return imageio_ffmpeg.get_ffmpeg_exe()
    raise RuntimeError("ffmpeg not found: install it or pip install imageio-ffmpeg")


def render_video(spec, out_dir=None):
    infographic.vet(spec)  # raises infographic.Blocked before any work is done
    n = infographic.n_cards(spec)
    out_dir = os.path.abspath(out_dir or OUT_DIR)
    os.makedirs(out_dir, exist_ok=True)
    digest = hashlib.sha256(("v2" + infographic.all_text(spec)
                             + spec.get("layout", "steps")).encode()).hexdigest()[:8]
    out = os.path.join(out_dir, "%s-%s.mp4" % (spec.get("slug", "video"), digest))

    from PIL import Image, ImageDraw
    FPS, XF = 30, 0.5  # frame rate, crossfade seconds

    def ease(t):
        return t * t * (3 - 2 * t)

    def bar(img, frac):
        im = img.copy()
        d = ImageDraw.Draw(im)
        d.rectangle([0, infographic.H - 8, int(infographic.W * frac), infographic.H], fill=infographic.GOLD)
        return im

    # stills: headline only, each card added, then the call-to-action end card
    stills = [infographic.build_image(spec, reveal=k) for k in range(n + 1)]
    stills.append(infographic.end_card(spec))
    holds = [HEAD_S] + [CARD_S] * n + [END_S]
    total = len(stills)

    with tempfile.TemporaryDirectory() as tmp:
        lines, idx = [], [0]

        def emit(img, dur):
            p = os.path.join(tmp, "f%04d.png" % idx[0]); idx[0] += 1
            img.save(p)
            lines.extend(["file '%s'" % p, "duration %.4f" % dur])

        for k, still in enumerate(stills):
            if k > 0:  # eased crossfade in from the previous still
                steps = int(XF * FPS)
                for j in range(1, steps + 1):
                    t = ease(j / steps)
                    fr = Image.blend(stills[k - 1], still, t)
                    emit(bar(fr, (k - 1 + t) / (total - 1)), 1.0 / FPS)
            emit(bar(still, k / (total - 1)), holds[k])
        lines.append(lines[-2])  # concat demuxer needs the last file repeated
        lst = os.path.join(tmp, "list.txt")
        open(lst, "w").write("\n".join(lines) + "\n")
        cmd = [ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
               "-i", lst, "-vf", "fps=%d,format=yuv420p" % FPS, "-c:v", "libx264",
               "-preset", "medium", "-crf", "20", "-movflags", "+faststart", out]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError("ffmpeg failed: " + r.stderr[-400:])
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    o = a[a.index("--out") + 1] if "--out" in a else None
    try:
        print(render_video(json.load(open(a[0])), o))
    except infographic.Blocked as e:
        print("BLOCKED:", e); sys.exit(1)
