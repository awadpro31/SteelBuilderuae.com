"""Batch 4 (Oct 2026): workshop night loading — the one new clip in this upload."""
import os
from PIL import Image, ImageFilter
from brand import *
import posts, reels

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
OUT = os.path.join(os.path.dirname(HERE), "batch-04")
NIGHT = os.path.join(SRC, "v4-night-clean.mp4")      # deshaken + denoised copy of v4-night-loading.mov
WORKSHOP = os.path.join(SRC, "v2-workshop.mp4")
ABOVE = os.path.join(SRC, "v3-above-steel.mov")
reels.OUT = os.path.join(OUT, "reels")
posts.OUT = OUT
W, H = 1080, 1920


def seg(name, src, ss, dur, eb=None, lines=None, ar=None, size=104, landscape=False, title_in=0.35):
    ov = reels.layer(name, eb, lines, ar, size=size) if lines else reels.layer(name)
    return reels.segment(name, src, ss, dur, ov, landscape=landscape, title_in=title_in)


def frame(t, path):
    reels.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", NIGHT, "-frames:v", "1", "-q:v", "2", path])
    return path


def fit_card(src_jpg, eb, lines, ar, y_end):
    """Landscape frame over its own blurred copy — avoids blowing a 1024px frame up to 1080x1920."""
    fr = Image.open(src_jpg).convert("RGB")
    bg = cover(fr, (W, H)).filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new("RGB", (W, H), INK), 0.5).convert("RGBA")
    fg = grade(fr.resize((W, round(fr.height * W / fr.width)), Image.LANCZOS)).convert("RGBA")
    bg.alpha_composite(fg, (0, 560))
    bg.alpha_composite(gradient((W, H), bottom=0.9, start=0.55))
    posts.headline(bg, eb, lines, ar, y_end, size=116, ar_size=52)
    return bg


def build_reels():
    reels.concat("reel-14-night-shift-loading", [
        seg("n1", NIGHT, 0.0, 2.8, "MUSAFFAH WORKSHOP", ["NIGHT", "~SHIFT."], "وردية الليل", landscape=True, title_in=0.1),
        seg("n2", NIGHT, 8.4, 4.2, "LOADING", ["STEEL", "~ON THE TRUCK."], "تحميل الحديد على التريلا", landscape=True),
        seg("n4", NIGHT, 15.3, 3.6, "READY FOR SITE", ["LOADED.", "~READY FOR SITE."], "جاهز للموقع", landscape=True),
        reels.endcard()])
    reels.concat("reel-15-workshop-to-site", [
        seg("s1", WORKSHOP, 5.0, 4.5, "01 · WORKSHOP", ["FABRICATED", "~TO THE DRAWING."], "تصنيع مطابق للرسم", size=96, title_in=0.1),
        seg("s2", NIGHT, 8.4, 4.2, "02 · DISPATCH", ["LOADED", "~AT NIGHT."], "تحميل بالليل", landscape=True),
        seg("s3", ABOVE, 1.0, 6.0, "03 · SITE", ["ERECTED", "~FRAME BY FRAME."], "تركيب إطار تلو الإطار"),
        reels.endcard()])


def build_stills():
    f1 = frame(10.4, os.path.join(reels.TMP, "night-a.jpg"))
    f2 = frame(16.5, os.path.join(reels.TMP, "night-b.jpg"))
    for i, (f, eb, ln, ar) in enumerate([(f1, "MUSAFFAH WORKSHOP", ["NIGHT", "~SHIFT."], "وردية الليل"),
                                         (f2, "READY FOR SITE", ["LOADED", "~AT NIGHT."], "تحميل بالليل")], start=1):
        im = fit_card(f, eb, ln, ar, 1560)
        watermark(im, w=170, pos="tl", margin=64, y=210)
        save(im, os.path.join(OUT, "stories", f"0{i}-{'night-shift' if i == 1 else 'loaded'}.jpg"))
    for n, f, eb, ln, ar in [("reel-14", f1, "NIGHT SHIFT", ["LOADED FOR", "~SITE."], "تحميل الحديد للموقع"),
                             ("reel-15", f2, "WORKSHOP TO SITE", ["THREE STEPS.", "~ONE TEAM."], "من الورشة إلى الموقع")]:
        im = fit_card(f, eb, ln, ar, 1560)
        watermark(im, w=190, pos="tr", margin=64, y=310)
        save(im, os.path.join(OUT, "reels", "covers", n + "-cover.jpg"))


if __name__ == "__main__":
    build_reels()
    build_stills()
    print("batch4 done")
