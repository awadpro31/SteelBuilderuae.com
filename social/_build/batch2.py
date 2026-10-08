"""Batch 2 (Oct 2026 site update): 5 reels, 5 cinematic shots, 5 posts, carousel, stories — same identity."""
import os, subprocess
from PIL import Image, ImageDraw
from brand import *
import posts, reels, cine

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
OUT = os.path.join(os.path.dirname(HERE), "batch-02")
V = {k: os.path.join(SRC, f"v2-{k}.mp4") for k in ["fill", "frames-walk", "excavator", "roof-sunset", "workshop"]}
P = {"cranes": os.path.join(SRC, "7.jpg"), "pedestals": os.path.join(SRC, "8.jpg"), "row": os.path.join(SRC, "9.jpg"),
     "bolts": os.path.join(SRC, "10.jpg"), "portals": os.path.join(SRC, "11.jpg")}
reels.OUT = os.path.join(OUT, "reels")
posts.OUT = OUT
cine.SHOTS = os.path.join(OUT, "cinematic-shots")


def pre_crop(src, out, crop):
    """Remove an edge artefact before the standard segment pipeline (e.g. cable across the lens)."""
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"crop={crop},scale=478:-2",
                    "-c:v", "libx264", "-crf", "16", "-c:a", "copy", out], check=True)
    return out


def seg(name, src, ss, dur, eb=None, lines=None, ar=None, size=104, landscape=False, title_in=0.35):
    ov = reels.layer(name, eb, lines, ar, size=size) if lines else reels.layer(name)
    return reels.segment(name, src, ss, dur, ov, landscape=landscape, title_in=title_in)


def cine_shot_seg(name, shot, eb, lines, ar):
    ov = reels.layer(name, eb, lines, ar, size=104)
    return reels.segment(name, os.path.join(cine.SHOTS, shot + ".mp4"), 0.25, 4.5, ov, title_in=0.3)


def top_title(size, photo, focus, eb, lines, ar, y_end, foot=None, wm_kw=None):
    """Headline over the sky (top) for photos whose steel sits in the lower half."""
    im = grade(cover(photo, size, focus)).convert("RGBA")
    im.alpha_composite(top_scrim(size, amount=0.92, end=0.55))
    im.alpha_composite(gradient(size, bottom=0.55, start=0.75))
    posts.headline(im, eb, lines, ar, y_end, size=110)
    if foot:
        foot(im)
    watermark(im, **(wm_kw or {"w": 170}))
    return im


SHOTS = [
    ("b2-01-cranes-push",   P["cranes"],    (0.42, 0.50, 1.05, 0), (0.40, 0.48, 1.30, 0), True),
    ("b2-02-pedestal-tilt", P["pedestals"], (0.50, 0.72, 1.20, 0), (0.50, 0.44, 1.20, 0), False),
    ("b2-03-row-slide",     P["row"],       (0.30, 0.55, 1.08, 0), (0.62, 0.55, 1.14, 0), False),
    ("b2-04-bolts-push",    P["bolts"],     (0.50, 0.55, 1.02, 0), (0.48, 0.72, 1.34, 0), False),
    ("b2-05-portals-push",  P["portals"],   (0.40, 0.50, 1.04, 0), (0.42, 0.48, 1.36, 0), True),
]


def render_shots():
    for name, photo, a, b, flare in SHOTS:
        cine.render((name, photo, a, b, flare, False))


def build_reels():
    fill = pre_crop(V["fill"], os.path.join(reels.TMP, "fill-crop.mp4"), "iw*0.80:ih*0.80:iw*0.20:ih*0.08")
    reels.concat("reel-06-the-full-process", [
        seg("p1", fill, 0.5, 3.4, "STEP 01", ["FILL", "~THE GROUND."], "ردم وتسوية", title_in=0.1),
        seg("p2", V["excavator"], 0.3, 3.4, "STEP 02", ["DIG", "~THE FOOTINGS."], "حفر القواعد", landscape=True),
        cine_shot_seg("p3", "b2-04-bolts-push", "STEP 03", ["ANCHOR BOLTS", "~SET TO LEVEL."], "تثبيت المسامير على المنسوب"),
        seg("p4", V["workshop"], 4.5, 4.0, "STEP 04", ["FABRICATE", "~IN OUR WORKSHOP."], "التصنيع في ورشتنا", size=96),
        seg("p5", V["frames-walk"], 4.0, 5.0, "STEP 05", ["ERECT", "~FRAME BY FRAME."], "التركيب إطار تلو الإطار"),
        reels.endcard()])
    reels.concat("reel-07-inside-our-workshop", [
        seg("w1", V["workshop"], 4.5, 6.5, "MUSAFFAH WORKSHOP", ["CUT. FIT.", "~WELD. CHECK."], "قص — تجميع — لحام — فحص", title_in=0.1),
        seg("w2", V["workshop"], 11.0, 4.6, "READY FOR SITE", ["EVERY PART", "~MARKED."], "كل قطعة مرقّمة وجاهزة"),
        reels.endcard()])
    reels.concat("reel-08-walk-the-frames", [
        seg("f1", V["frames-walk"], 0.0, 7.0, "ON SITE", ["WALK", "~THE FRAMES."], "جولة بين الإطارات", title_in=0.1),
        seg("f2", V["frames-walk"], 7.0, 7.0, "TWO CRANES", ["DOUBLE", "~THE PACE."], "رافعتان — ضعف الإنجاز"),
        seg("f3", V["frames-walk"], 20.5, 7.5, "STEEL BUILDER", ["STRENGTH,", "~BUILT PRECISELY."], "نبني القوة بدقة."),
        reels.endcard()])
    reels.concat("reel-09-golden-hour-roof", [
        seg("g1", V["roof-sunset"], 0.0, 6.4, "ROOF STRUCTURE", ["PURLINS", "~TO THE RIDGE."], "المدادات حتى قمة السقف", title_in=0.1),
        seg("g2", V["roof-sunset"], 6.4, 5.2, "GOLDEN HOUR", ["BUILT TO", "~LAST."], "نبني حلولاً تدوم"),
        reels.endcard()])
    reels.concat("reel-10-foundations-to-frames", [
        cine_shot_seg("c1", "b2-02-pedestal-tilt", "FOUNDATIONS", ["PEDESTALS", "~POURED."], "صب القواعد الخرسانية"),
        cine_shot_seg("c2", "b2-04-bolts-push", "PRECISION", ["BOLTS SET", "~TO THE DRAWING."], "مطابق للرسم"),
        cine_shot_seg("c3", "b2-01-cranes-push", "ERECTION", ["TWO CRANES.", "~ONE PLAN."], "رافعتان — خطة واحدة"),
        cine_shot_seg("c4", "b2-03-row-slide", "ON SITE", ["SPAN", "~AFTER SPAN."], "هيكل بعد هيكل"),
        cine_shot_seg("c5", "b2-05-portals-push", "STEEL BUILDER", ["FROM FOUNDATIONS", "~TO FRAMES."], "من القواعد إلى الهياكل"),
        reels.endcard()])


def build_covers():
    for n, p, fo, eb, ln, ar in [
        ("reel-06", P["bolts"], (0.5, 0.6), "THE FULL PROCESS", ["FIVE STEPS.", "~ONE TEAM."], "خمس مراحل — فريق واحد"),
        ("reel-07", P["portals"], (0.6, 0.5), "INSIDE OUR WORKSHOP", ["CUT. FIT.", "~WELD. CHECK."], "داخل ورشتنا"),
        ("reel-08", P["row"], (0.45, 0.5), "WALK THE FRAMES", ["SPAN", "~AFTER SPAN."], "جولة بين الإطارات"),
        ("reel-09", P["portals"], (0.35, 0.5), "GOLDEN HOUR", ["BUILT TO", "~LAST."], "نبني حلولاً تدوم"),
        ("reel-10", P["pedestals"], (0.5, 0.6), "FOUNDATIONS TO FRAMES", ["FROM THE", "~GROUND UP."], "من القواعد إلى الهياكل")]:
        reels.cover_image(n, p, eb, ln, ar, fo)


def build_stills():
    posts.post("07-two-cranes.jpg", P["cranes"], "ON SITE", ["TWO CRANES.", "~ONE PLAN."], "رافعتان — خطة واحدة", focus=(0.42, 0.5))
    posts.post("08-foundations-first.jpg", P["pedestals"], "FOUNDATIONS", ["STRONG STEEL", "~STARTS BELOW."], "الهيكل القوي يبدأ من القاعدة", focus=(0.5, 0.62))
    im = top_title(posts.FEED, P["row"], (0.74, 0.5), "STEEL STRUCTURES", ["SPAN", "~AFTER SPAN."], "هيكل بعد هيكل",
                   600, foot=footer_bar, wm_kw={"w": 170, "pos": "bl", "margin": 64, "y": posts.FEED[1] - 330})
    save(im, os.path.join(OUT, "feed", "09-span-after-span.jpg"))
    posts.post("10-set-to-the-drawing.jpg", P["bolts"], "PRECISION", ["SET TO", "~THE DRAWING."], "مطابق للرسم", focus=(0.5, 0.62))
    posts.post("11-portal-frames.jpg", P["portals"], "STEEL BUILDER · UAE", ["STRENGTH,", "~BUILT PRECISELY."], "نبني القوة بدقة.", focus=(0.4, 0.5))
    # carousel: foundations to frames
    out = os.path.join(OUT, "carousel-foundations-to-frames")
    n = 6
    def counter(d, i):
        text(d, (posts.FEED[0] - 64, posts.FEED[1] - 70), f"{i:02d} / {n:02d}", font("med", 24),
             fill=(255, 255, 255, 200), anchor="rm", spacing=3)
    im = posts.base(P["portals"], posts.FEED, (0.4, 0.5), scrim=0.95, start=0.3)
    posts.headline(im, "SITE UPDATE", ["FOUNDATIONS", "~TO FRAMES."], "من القواعد إلى الهياكل", posts.FEED[1] - 130, size=120)
    d = ImageDraw.Draw(im)
    text(d, (64, posts.FEED[1] - 70), "SWIPE  →", font("med", 24), fill=(255, 255, 255, 200), anchor="lm", spacing=4)
    counter(d, 1); watermark(im, w=170); save(im, os.path.join(out, "01-cover.jpg"))
    for i, (k, fo, eb, ln, ar) in enumerate([
            ("pedestals", (0.5, 0.62), "STEP 01", ["PEDESTALS", "POURED."], "صب القواعد الخرسانية"),
            ("bolts", (0.5, 0.62), "STEP 02", ["ANCHOR BOLTS", "SET TO LEVEL."], "تثبيت المسامير على المنسوب"),
            ("cranes", (0.42, 0.5), "STEP 03", ["COLUMNS", "STANDING."], "تركيب الأعمدة"),
            ("row", (0.74, 0.5), "STEP 04", ["RAFTERS", "LOCKED IN."], "تثبيت الجمالونات")], start=2):
        if k == "row":
            im = top_title(posts.FEED, P[k], fo, eb, ln, ar, 600, wm_kw={"w": 170, "pos": "bl", "margin": 64, "y": posts.FEED[1] - 330})
        else:
            im = posts.base(P[k], posts.FEED, fo)
            posts.headline(im, eb, ln, ar, posts.FEED[1] - 130)
        d = ImageDraw.Draw(im)
        text(d, (64, posts.FEED[1] - 70), "@STEELBUILDERUAE", font("med", 24), fill=(255, 255, 255, 200), anchor="lm", spacing=3)
        counter(d, i)
        if k != "row":
            watermark(im, w=170)
        save(im, os.path.join(out, f"{i:02d}-{k}.jpg"))
    im = posts.cta_card(posts.FEED); counter(ImageDraw.Draw(im), 6); save(im, os.path.join(out, "06-cta.jpg"))
    # stories
    so = os.path.join(OUT, "stories")
    for fn, k, fo, eb, ln, ar in [
            ("01-foundations.jpg", "pedestals", (0.5, 0.6), "SITE UPDATE", ["FOUNDATIONS", "~DONE."], "القواعد جاهزة"),
            ("02-two-cranes.jpg", "bolts", (0.5, 0.6), "THIS WEEK", ["STEEL", "~GOING UP."], "الحديد يرتفع"),
            ]:
        im = posts.base(P[k], posts.STORY, fo, scrim=0.95, start=0.36, top=0.55)
        posts.headline(im, eb, ln, ar, posts.STORY[1] - 330, size=120)
        watermark(im, w=170, pos="tl", margin=64, y=210)
        save(im, os.path.join(so, fn))
    im = top_title(posts.STORY, P["row"], (0.74, 0.5), "ON SITE", ["SPAN", "~AFTER SPAN."], "هيكل بعد هيكل", 820,
                   wm_kw={"w": 170, "pos": "tl", "margin": 64, "y": 210})
    save(im, os.path.join(so, "03-span-after-span.jpg"))


if __name__ == "__main__":
    import sys
    steps = sys.argv[1:] or ["stills", "shots", "reels", "covers"]
    if "stills" in steps: build_stills()
    if "shots" in steps: render_shots()
    if "reels" in steps: build_reels()
    if "covers" in steps: build_covers()
    print("batch2 done")
