"""Batch 18: UAE Flag Day (3 November) greeting — feed post + story in the house style.
Original design: a waving UAE flag drawn from its geometry (hoist red band, green/white/black stripes) on a steel
flagpole, over our own sunset erection photo (20.jpg), with the Nabati poem the client shared typeset in two columns."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from brand import *
import posts

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "batch-18")
PHOTO = os.path.join(HERE, "source", "20.jpg")

RED, GREEN, BLACK = (206, 17, 38), (0, 115, 47), (0, 0, 0)
POEM = [
    ("نحمي العلم وترابه", "وبأرواحنا نفديه"),
    ("نفخر به ونحيا به", "نعشقه ونحيّيه"),
    ("عزّ ومجد ومهابه", "ويلٍ على معاديه"),
    ("دونه قروم ولابه", "ضحّت لأجل تحميه"),
    ("وحرٍّ دمي مخلابه", "ذخر الوطن راعيه"),
    ("ساس العدل وصوابه", "ربّي عسى يخلّيه"),
]


def flag(w):
    """UAE flag (1:2) with a cloth wave: vertical ripple growing from the hoist, plus light/shade folds."""
    h = w // 2
    pad = int(h * 0.18)
    flat = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(flat)
    d.rectangle((0, 0, w, h // 3), fill=GREEN)
    d.rectangle((0, 2 * h // 3, w, h), fill=BLACK)
    d.rectangle((0, 0, w // 4, h), fill=RED)
    src = np.asarray(flat, np.float32)
    H = h + 2 * pad
    out = np.zeros((H, w, 4), np.float32)
    xs = np.arange(w)
    k = xs / w                                                   # wave grows away from the pole
    phase = 2 * np.pi * (xs / (w * 0.55))
    off = pad * 0.85 * k * np.sin(phase)
    shade = 1 + 0.22 * k * np.cos(phase)                         # slope of the wave -> light / shadow
    for x in xs:
        y0 = int(round(pad + off[x]))
        out[y0:y0 + h, x, :3] = np.clip(src[:, x] * shade[x], 0, 255)
        out[y0:y0 + h, x, 3] = 255
    im = Image.fromarray(out.astype(np.uint8), "RGBA").filter(ImageFilter.SMOOTH)
    return im, pad


def flag_with_pole(w, pole_h):
    fl, pad = flag(w)
    canvas = Image.new("RGBA", (w + 40, pole_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((8, 0, 22, pole_h), radius=7, fill=(196, 201, 208))          # steel pole
    d.rectangle((15, 0, 22, pole_h), fill=(150, 156, 165))                           # shaded side
    d.ellipse((2, -6, 28, 20), fill=ORANGE)                                          # brand-orange finial
    shadow = Image.new("RGBA", fl.size, (0, 0, 0, 0))
    shadow.putalpha(fl.split()[3].point(lambda v: int(v * 0.35)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    canvas.alpha_composite(shadow, (34, 26 - pad + 12))
    canvas.alpha_composite(fl, (22, 26 - pad))
    return canvas


def background(size):
    W, H = size
    ph = Image.open(PHOTO).convert("RGB").crop((0, 20, 1200, 1000))                 # above the foreground clutter
    im = grade(cover(ph, (W, H), (0.5, 0.55)), sat=1.0).convert("RGBA")
    im.alpha_composite(gradient((W, H), bottom=0.97, start=0.18))
    im.alpha_composite(top_scrim((W, H), amount=0.55, end=0.35))
    return im


def poem(d, y, W, size, gap):
    fa = font("kufi", size)
    mid = W // 2
    for right, left in POEM:
        text(d, (W - 72, y), right, fa, fill=WHITE, anchor="ra", rtl=True)
        text(d, (mid - 24, y), left, fa, fill=STEEL, anchor="ra", rtl=True)
        d.text((mid + 2, y + size * 0.55), "•", font=font("bold", size // 2), fill=ORANGE, anchor="mm")
        y += gap
    return y


def title(d, x_right, y, big):
    """Arabic title (bottom-anchored on y) with the brand eyebrow under it."""
    text(d, (x_right, y), "يوم العلم", font("kufi", big), fill=WHITE, anchor="rd", rtl=True)
    eyebrow(d, x_right, y + 44, "FLAG DAY  ·  3 NOVEMBER", right=True, size=int(big * 0.22))
    return y + 80


def greeting(d, y, W, size):
    text(d, (W // 2, y), "ستيل بيلدر تهنّئ دولة الإمارات قيادةً وشعبًا بيوم العلم", font("arb", size), fill=WHITE, anchor="ma", rtl=True)
    text(d, (W // 2, y + int(size * 1.9)), "STEEL BUILDER METAL INDUSTRY L.L.C", font("bold", int(size * 0.62)), fill=ORANGE, anchor="ma", spacing=5)


def feed():
    W, H = posts.FEED
    im = background((W, H))
    im.alpha_composite(flag_with_pole(380, 430), (64, 64))
    watermark(im, w=150, pos="tr", margin=60, y=70)
    d = ImageDraw.Draw(im)
    title(d, W - 72, 520, 118)
    y = poem(d, 660, W, 36, 64)
    greeting(d, y + 34, W, 32)
    footer_bar(im)
    return im


def story():
    W, H = posts.STORY
    im = background((W, H))
    im.alpha_composite(flag_with_pole(470, 540), (64, 210))
    watermark(im, w=170, pos="tr", margin=64, y=220)
    d = ImageDraw.Draw(im)
    title(d, W - 72, 880, 140)
    y = poem(d, 1040, W, 42, 82)
    greeting(d, y + 60, W, 36)
    return im


if __name__ == "__main__":
    save(feed(), os.path.join(OUT, "feed", "18-flag-day.jpg"), q=95)
    save(story(), os.path.join(OUT, "stories", "01-flag-day.jpg"), q=95)
    print("batch18 done")
