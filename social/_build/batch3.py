"""Batch 3 (Oct 2026): only the media that is new versus batch 2 — 3 videos + the formwork photo."""
import os
from PIL import Image, ImageDraw
from brand import *
import posts, reels, cine

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
OUT = os.path.join(os.path.dirname(HERE), "batch-03")
V = {"top": os.path.join(SRC, "v3-top-view.mov"), "above": os.path.join(SRC, "v3-above-steel.mov"),
     "loader": os.path.join(SRC, "v3-loader.mp4")}
FORM = os.path.join(SRC, "12.jpg")
reels.OUT = os.path.join(OUT, "reels")
posts.OUT = OUT
cine.SHOTS = os.path.join(OUT, "cinematic-shots")
SHOT = ("b3-01-formwork-push", FORM, (0.50, 0.70, 1.04, 0), (0.50, 0.52, 1.30, 0), False, False)


def seg(name, src, ss, dur, eb=None, lines=None, ar=None, size=104, landscape=False, title_in=0.35):
    ov = reels.layer(name, eb, lines, ar, size=size) if lines else reels.layer(name)
    return reels.segment(name, src, ss, dur, ov, landscape=landscape, title_in=title_in)


def build_reels():
    reels.concat("reel-11-view-from-the-top", [
        seg("t1", V["top"], 0.0, 6.0, "FROM THE MANLIFT", ["THE VIEW", "~FROM THE TOP."], "المنظر من فوق", title_in=0.1),
        seg("t2", V["top"], 7.0, 5.5, "AT HEIGHT", ["SAFETY", "~FIRST."], "السلامة أولاً"),
        seg("t3", V["top"], 16.0, 8.0, "ROOF STRUCTURE", ["PURLINS", "~LINED UP."], "المدادات على خط واحد"),
        reels.endcard()])
    reels.concat("reel-12-above-the-steel", [
        seg("a1", V["above"], 0.0, 8.5, "ON SITE", ["ABOVE", "~THE STEEL."], "فوق الهيكل", title_in=0.1),
        seg("a2", V["above"], 15.5, 8.0, "STEEL STRUCTURES", ["SPAN", "~AFTER SPAN."], "هيكل بعد هيكل"),
        seg("a3", V["above"], 27.0, 7.3, "STEEL BUILDER", ["STRENGTH,", "~BUILT PRECISELY."], "نبني القوة بدقة."),
        reels.endcard()])
    reels.concat("reel-13-before-the-steel", [
        seg("b1", V["loader"], 0.0, 3.2, "STEP 01", ["LEVEL", "~THE SITE."], "تسوية الموقع", landscape=True, title_in=0.1),
        seg("b2", V["loader"], 6.5, 3.2, "CIVIL WORKS", ["GRADE", "~& COMPACT."], "تسوية ودك", landscape=True),
        reels.segment("b3", os.path.join(cine.SHOTS, SHOT[0] + ".mp4"), 0.25, 4.5,
                      reels.layer("b3", "STEP 02", ["FORM", "~THE PEDESTALS."], "شدّات القواعد", size=104), title_in=0.3),
        seg("b4", V["top"], 16.0, 5.0, "STEP 03", ["THEN", "~THE STEEL."], "ثم يبدأ الهيكل المعدني"),
        reels.endcard()])


def build_covers():
    reels.cover_image("reel-11", os.path.join(SRC, "v3-top-frame.jpg"), "VIEW FROM THE TOP", ["THE VIEW", "~FROM THE TOP."], "المنظر من فوق", (0.5, 0.5))
    reels.cover_image("reel-12", os.path.join(SRC, "v3-above-frame.jpg"), "ABOVE THE STEEL", ["SPAN", "~AFTER SPAN."], "هيكل بعد هيكل", (0.4, 0.5))
    reels.cover_image("reel-13", FORM, "BEFORE THE STEEL", ["LEVEL. FORM.", "~THEN STEEL."], "تسوية — شدّات — ثم الحديد", (0.5, 0.6))


def build_stills():
    posts.post("12-formwork.jpg", FORM, "FOUNDATIONS", ["FORMED", "~TO SIZE."], "شدّات القواعد بالمقاس", focus=(0.5, 0.62))
    # progress grid: four stages, one post — formwork → pedestals → columns → frames
    W, Hh = posts.FEED
    im = Image.new("RGBA", (W, Hh), INK + (255,))
    tiles = [(FORM, (0.5, 0.65), "01", "FORMWORK"), (os.path.join(SRC, "8.jpg"), (0.5, 0.62), "02", "PEDESTALS"),
             (os.path.join(SRC, "7.jpg"), (0.42, 0.5), "03", "COLUMNS"), (os.path.join(SRC, "11.jpg"), (0.4, 0.5), "04", "FRAMES")]
    g, top = 8, 330
    tw, th = (W - 64 * 2 - g) // 2, (Hh - top - 150 - g) // 2
    d = ImageDraw.Draw(im)
    for i, (p, fo, n, lab) in enumerate(tiles):
        x = 64 + (i % 2) * (tw + g); y = top + (i // 2) * (th + g)
        t = grade(cover(p, (tw, th), fo)).convert("RGBA")
        t.alpha_composite(gradient((tw, th), bottom=0.85, start=0.45))
        im.alpha_composite(t, (x, y))
        text(d, (x + 24, y + th - 70), n, font("bold", 26), fill=ORANGE)
        text(d, (x + 24, y + th - 40), lab, font("bold", 30), fill=WHITE, spacing=4)
    eyebrow(d, 64, 120, "SITE PROGRESS")
    d.text((60, 150), "FOUR STAGES.", font=font("xbold", 72), fill=WHITE)
    d.text((60, 225), "ONE TEAM.", font=font("xbold", 72), fill=ORANGE)
    text(d, (W - 64, 270), "أربع مراحل — فريق واحد", font("kufi", 38), fill=STEEL, anchor="rm", rtl=True)
    footer_bar(im)
    watermark(im, w=150, margin=48)
    save(im, os.path.join(OUT, "feed", "13-four-stages.jpg"))
    so = os.path.join(OUT, "stories")
    im = posts.base(FORM, posts.STORY, (0.5, 0.6), scrim=0.95, start=0.36, top=0.55)
    posts.headline(im, "SITE UPDATE", ["PEDESTALS", "~FORMED."], "شدّات القواعد جاهزة", posts.STORY[1] - 330, size=120)
    watermark(im, w=170, pos="tl", margin=64, y=210)
    save(im, os.path.join(so, "01-formwork.jpg"))


if __name__ == "__main__":
    import sys
    steps = sys.argv[1:] or ["stills", "shots", "reels", "covers"]
    if "stills" in steps: build_stills()
    if "shots" in steps: cine.render(SHOT)
    if "reels" in steps: build_reels()
    if "covers" in steps: build_covers()
    print("batch3 done")
