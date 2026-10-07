"""Renders the 5 reels (Instagram Reels + TikTok, 1080x1920, 30fps, H.264/AAC)."""
import os, subprocess, shutil, tempfile
from PIL import Image, ImageDraw
from brand import *
import posts

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
OUT = os.path.join(os.path.dirname(HERE), "reels")
TMP = tempfile.mkdtemp(prefix="sb-reels-")
W, H = 1080, 1920
V = {k: os.path.join(SRC, f"v-{k}.mp4") for k in ["lift", "height", "wide", "excavation", "grading"]}
GRADE = "eq=contrast=1.07:saturation=0.86,unsharp=5:5:0.6"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(cmd)); print(r.stderr[-2500:]); raise SystemExit(1)


def layer(name, eb=None, lines=None, ar=None, size=104, wm=True, y_end=1500, hook=False):
    """Transparent full-frame overlay: scrim + title + logo watermark (safe zones respected)."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if lines:
        im.alpha_composite(gradient((W, H), bottom=0.9, start=0.40))
        posts.headline(im, eb, lines, ar, y_end, size=size, ar_size=50, x=72)
    if wm:
        watermark(im, w=170, pos="tl", margin=64, y=190)
    p = os.path.join(TMP, name + ".png")
    im.save(p)
    return p


def segment(name, src, ss, dur, overlay, landscape=False, fade_in=0.35, title_in=0.4):
    """Normalise a clip to 1080x1920 graded footage with its overlay faded in."""
    out = os.path.join(TMP, name + ".mp4")
    if landscape:
        vf = (f"[0:v]split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
              f"gblur=sigma=40,eq=brightness=-0.18:saturation=0.6[bg];"
              f"[b]scale={W}:-2:flags=lanczos,{GRADE}[fg];[bg][fg]overlay=0:(H-h)/2-140[v0]")
    else:
        vf = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,"
              f"crop={W}:{H},{GRADE}[v0]")
    vf += (f";[1:v]format=rgba,fade=in:st={title_in}:d=0.5:alpha=1[ov];"
           f"[v0][ov]overlay=0:0,fade=in:st=0:d={fade_in},setsar=1,fps=30,format=yuv420p[v]")
    run(["ffmpeg", "-y", "-v", "error", "-ss", str(ss), "-t", str(dur), "-i", src,
         "-loop", "1", "-t", str(dur), "-i", overlay,
         "-filter_complex", vf + ";[0:a]aresample=44100,volume=0.55,afade=in:d=0.3,"
         f"afade=out:st={dur - 0.3}:d=0.3[a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
         "-c:a", "aac", "-b:a", "160k", "-ac", "2", "-t", str(dur), out])
    return out


def still_segment(name, img_path, dur, zoom=True, overlay=None, title_in=0.5):
    """Ken-Burns push on a still (photo reel) or a static end card."""
    out = os.path.join(TMP, name + ".mp4")
    frames = int(dur * 30)
    if zoom:
        v = (f"[0:v]scale=2160:3840,zoompan=z='1+0.07*on/{frames}':x='iw/2-(iw/zoom/2)':"
             f"y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps=30[v0]")
    else:
        v = f"[0:v]scale={W}:{H},fps=30,trim=duration={dur}[v0]"
    inputs = ["-loop", "1", "-t", str(dur), "-i", img_path]
    if overlay:
        inputs += ["-loop", "1", "-t", str(dur), "-i", overlay]
        v += (f";[1:v]format=rgba,fade=in:st={title_in}:d=0.5:alpha=1[ov];[v0][ov]overlay=0:0[v1]")
    else:
        v += ";[v0]null[v1]"
    v += ";[v1]fade=in:st=0:d=0.35,setsar=1,format=yuv420p[v]"
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-f", "lavfi", "-t", str(dur),
         "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex", v,
         "-map", "[v]", "-map", f"{2 if overlay else 1}:a", "-c:v", "libx264", "-preset", "medium",
         "-crf", "19", "-c:a", "aac", "-b:a", "160k", "-t", str(dur), out])
    return out


def endcard(dur=3.5):
    p = os.path.join(TMP, "endcard.png")
    if not os.path.exists(p):
        posts.cta_card((W, H), story=True).convert("RGB").save(p)
    return still_segment(f"end{dur}", p, dur, zoom=False)


def concat(name, parts, cover_png=None):
    lst = os.path.join(TMP, name + ".txt")
    with open(lst, "w") as f:
        f.writelines(f"file '{p}'\n" for p in parts)
    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, name + ".mp4")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
         "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-maxrate", "8M", "-bufsize", "12M",
         "-c:a", "aac", "-b:a", "160k", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-movflags", "+faststart", out])
    return out


def cover_image(name, photo, eb, lines, ar, focus=(0.5, 0.5)):
    """Reel / TikTok cover (1080x1920; title kept inside the 1080x1350 grid crop)."""
    im = posts.base(photo, (W, H), focus, scrim=0.95, start=0.3, top=0.5)
    posts.headline(im, eb, lines, ar, 1560, size=120, ar_size=54)
    watermark(im, w=190, pos="tr", margin=64, y=310)
    return save(im, os.path.join(OUT, "covers", name + "-cover.jpg"))


def frame(src, t, size=None):
    p = os.path.join(TMP, f"f{abs(hash((src, t)))}.png")
    run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", src, "-frames:v", "1", p])
    return p


if __name__ == "__main__":
    # R1 — From Sand to Steel (hero reel, ~29s)
    p = [
        segment("r1a", V["grading"], 1.0, 3.6, layer("r1a", "DAY ONE", ["IT STARTS", "~WITH SAND."], "كل شيء يبدأ من الرمل", size=112), title_in=0.15),
        segment("r1b", V["excavation"], 1.0, 3.6, layer("r1b", "CIVIL WORKS", ["DIG. LEVEL.", "~COMPACT."], "حفر — تسوية — دك")),
        segment("r1c", V["lift"], 4.0, 6.0, layer("r1c", "STEEL ERECTION", ["THEN THE", "~STEEL ARRIVES."], "ثم يبدأ تركيب الهيكل المعدني")),
        segment("r1d", V["height"], 2.0, 5.5, layer("r1d", "ON SITE", ["PRECISION", "~AT HEIGHT."], "الدقة على ارتفاع")),
        segment("r1e", V["wide"], 0.0, 6.0, layer("r1e", "STEEL BUILDER", ["FROM SAND", "~TO STEEL."], "من الرمل إلى الهيكل المعدني", size=112), landscape=True),
        endcard(),
    ]
    concat("reel-01-from-sand-to-steel", p)
    cover_image("reel-01", posts.P["portal"], "PROJECT FILM", ["FROM SAND", "~TO STEEL."], "من الرمل إلى الهيكل المعدني", (0.55, 0.5))

    # R2 — The Lift (~20s)
    p = [segment("r2a", V["lift"], 0.0, 5.0, layer("r2a", "WATCH THIS", ["ONE LIFT.", "~ZERO GUESSWORK."], "رفعة واحدة — بلا تخمين", size=108), title_in=0.1),
         segment("r2b", V["lift"], 5.0, 11.0, layer("r2b", wm=True)),
         endcard()]
    concat("reel-02-the-lift", p)
    cover_image("reel-02", posts.P["crane"], "THE LIFT", ["ONE LIFT.", "~ZERO GUESSWORK."], "رفعة واحدة — بلا تخمين", (0.5, 0.45))

    # R3 — Precision at height (~22s)
    p = [segment("r3a", V["height"], 0.0, 6.0, layer("r3a", "ON SITE", ["THE DIFFERENCE", "~IS IN THE DETAIL."], "الفرق في التفاصيل", size=96), title_in=0.1),
         segment("r3b", V["height"], 6.0, 12.5, layer("r3b", wm=True)),
         endcard()]
    concat("reel-03-precision-at-height", p)
    cover_image("reel-03", posts.P["crew"], "THE DETAIL", ["PRECISION", "~AT HEIGHT."], "الدقة على ارتفاع", (0.5, 0.35))

    # R4 — Ground works (~19s)
    p = [segment("r4a", V["grading"], 0.5, 7.0, layer("r4a", "CIVIL WORKS", ["STRONG STEEL", "~NEEDS STRONG GROUND."], "الهيكل القوي يبدأ من أرض قوية", size=92), title_in=0.1),
         segment("r4b", V["excavation"], 0.5, 8.5, layer("r4b", "BEFORE THE STEEL", ["EXCAVATION,", "~LEVELS & COMPACTION."], "حفر ومناسيب ودك", size=88)),
         endcard()]
    concat("reel-04-ground-works", p)
    cover_image("reel-04", posts.P["frames"], "CIVIL WORKS", ["STRONG GROUND,", "~STRONG STEEL."], "أرض قوية — هيكل قوي", (0.5, 0.75))

    # R5 — Photo reel, Ken Burns (~16s; add a trending sound in-app)
    shots = [("portal", (0.55, 0.5), "STEEL BUILDER", ["STRENGTH,", "~BUILT PRECISELY."], "نبني القوة بدقة."),
             ("crane", (0.5, 0.45), "STEP 01", ["COLUMNS SET,", "~RAFTERS FLY."], "تثبيت الأعمدة ورفع الجمالونات"),
             ("crew", (0.5, 0.35), "STEP 02", ["EVERY BOLT,", "~BY HAND."], "كل وصلة تُنفَّذ بإتقان"),
             ("purlins", (0.6, 0.5), "STEP 03", ["PURLINS", "~LOCKED IN."], "تركيب المدادات المجلفنة"),
             ("frames", (0.5, 0.7), "STEP 04", ["FRAME", "~BY FRAME."], "إطار تلو الإطار")]
    p = []
    for i, (k, fo, eb, ln, ar) in enumerate(shots):
        bg = os.path.join(TMP, f"r5{i}.jpg")
        grade(cover(posts.P[k], (W, H), fo)).save(bg, quality=95)
        p.append(still_segment(f"r5{i}", bg, 2.6, overlay=layer(f"r5{i}", eb, ln, ar, size=104), title_in=0.2))
    p.append(endcard())
    concat("reel-05-frame-by-frame-photos", p)
    cover_image("reel-05", posts.P["purlins"], "PHOTO STORY", ["FRAME", "~BY FRAME."], "إطار تلو الإطار", (0.6, 0.5))

    shutil.rmtree(TMP)
    print("reels done")
