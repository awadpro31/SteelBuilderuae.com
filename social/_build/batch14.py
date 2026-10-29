"""Batch 14: Dubai Industrial City site reel — rebar & formwork, pad pour, steel erection at sunset.
v14-dic-site.mp4 has burnt-in "Dubai Industrial City / موقع دبي الصناعية" captions: the opening shot (title mid-frame)
is dropped and every other shot is cropped to y<448, above the lower caption (measured at y≈455-550).
The pour clip is vidstab-stabilised and starts after the supplier's truck/plate leaves frame."""
import os, subprocess
from brand import *
import reels, music2

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
OUT = os.path.join(os.path.dirname(HERE), "batch-14")
reels.OUT = os.path.join(OUT, "reels")
S = lambda f: os.path.join(SRC, f)
B = music2.BEAT
GRADE = "eq=contrast=1.06:saturation=1.06,unsharp=5:5:0.6"


def prep():
    run = lambda *a: subprocess.run(["ffmpeg", "-y", "-v", "error", *a], check=True)
    # caption-free crop of the site clip (full width, top 448 rows)
    run("-i", S("v14-dic-site.mp4"), "-vf", f"crop=1024:448:0:0,{GRADE}", "-c:v", "libx264", "-crf", "14",
        "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", S("v14-dic-site-clean.mp4"))
    # stabilise the handheld pour clip (two-pass vidstab + safety crop)
    trf = os.path.join(reels.TMP, "pour.trf")
    run("-i", S("v14-dic-pour.mov"), "-vf", f"vidstabdetect=shakiness=8:accuracy=15:result={trf}", "-f", "null", "-")
    run("-i", S("v14-dic-pour.mov"), "-vf",
        f"vidstabtransform=input={trf}:smoothing=45:optzoom=1:interpol=bicubic,"
        f"crop=trunc(iw*0.9/2)*2:trunc(ih*0.9/2)*2,scale=848:478:flags=lanczos,{GRADE}",
        "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", S("v14-dic-pour-stab.mp4"))
    # sunset erection photo -> slow push-in clip, framed on the structure (above the clutter in the foreground)
    run("-i", S("20.jpg"), "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex",
        "[0:v]crop=1200:810:0:20,scale=2400:1620,zoompan=z='1+0.10*on/210':x='iw/2-(iw/zoom/2)':"
        "y='ih*0.45-(ih/zoom*0.45)':d=210:s=1080x730:fps=30,eq=contrast=1.05:saturation=1.08[v]",
        "-map", "[v]", "-map", "1:a", "-t", "7", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p",
        "-c:a", "aac", S("v14-sunset-push.mp4"))


def make_cover():
    """Sunset frame cropped above the foreground clutter, floated on its own blur; title on the ink below."""
    from PIL import Image, ImageFilter
    import posts
    W, H = 1080, 1920
    ph = Image.open(S("20.jpg")).convert("RGB").crop((0, 20, 1200, 1000))
    bg = cover(ph, (W, H)).filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new("RGB", (W, H), INK), 0.55).convert("RGBA")
    fg = grade(ph.resize((W, round(980 * W / 1200)), Image.LANCZOS), sat=1.0).convert("RGBA")
    fg.alpha_composite(gradient(fg.size, bottom=0.9, start=0.6))
    bg.alpha_composite(fg, (0, 250))
    bg.alpha_composite(gradient((W, H), bottom=0.92, start=0.55))
    posts.headline(bg, "DUBAI INDUSTRIAL CITY", ["STEEL", "~RISING."], "تركيب الهيكل المعدني", 1560, size=120, ar_size=54)
    watermark(bg, w=190, pos="tr", margin=64, y=310)
    save(bg, os.path.join(reels.OUT, "covers", "reel-23-cover.jpg"))


PLAN = [  # name, src, start, beats, eyebrow, lines, arabic
    ("s1", "v14-dic-site-clean.mp4", 5.2, 4, "DUBAI INDUSTRIAL CITY", ["GROUND", "~WORK."], "أعمال الأساسات — دبي الصناعية"),
    ("s2", "v14-dic-site-clean.mp4", 2.6, 4, None, None, None),
    ("s3", "v14-dic-site-clean.mp4", 7.6, 4, None, None, None),
    ("s4", "v14-dic-pour-stab.mp4", 1.3, 8, "CONCRETE", ["PADS", "~POURED."], "صبّ القواعد"),
    ("s5", "v14-sunset-push.mp4", 0.2, 12, "STEEL BUILDER", ["STEEL", "~RISING."], "تركيب الهيكل المعدني"),
]


def build():
    segs, t, cuts, starts = [], 0.0, [], {}
    for name, src, ss, beats, eb, lines, ar in PLAN:
        dur = beats * B
        ov = reels.layer(name, eb, lines, ar, size=116) if lines else reels.layer(name)
        segs.append(reels.segment(name, S(src), ss, dur, ov, landscape=True, fade_in=0.08, title_in=0.1))
        if t > 0: cuts.append(t)
        starts[name] = t; t += dur
    end = t
    segs.append(reels.endcard(8 * B))
    silent = reels.concat("_dic-silent", segs)
    total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", silent]))
    sec = {"groove": starts["s2"], "layer2": starts["s4"], "peak": starts["s5"], "final": starts["s5"] + 4, "end": end}
    wav = os.path.join(reels.TMP, "score.wav")
    music2.track(wav, total, sec, cuts)
    out = os.path.join(reels.OUT, "reel-23-dic-site.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", wav, "-filter_complex",
                    "[1:a]atrim=0:%.3f,volume=1.6,alimiter=limit=0.89:attack=5:release=80:level=false[a]" % total,
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    os.remove(silent)
    make_cover()
    print("sections", sec, "cuts", cuts, "total", round(total, 2))


if __name__ == "__main__":
    import sys
    steps = sys.argv[1:] or ["prep", "reel"]
    if steps == ["cover"]: make_cover()
    if "prep" in steps: prep()
    if "reel" in steps: build()
