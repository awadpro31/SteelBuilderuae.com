"""Batch 12: KEZAD site progress — 3 site photos (anchor bolts, soil removal, PEB rafters).
Sources are ~975px screenshots, so the photo is width-fitted (≈1.1x) instead of blown up full-bleed:
editorial layout — photo on top, ink panel with the headline below; stories float it over its own blur."""
import os
from PIL import Image, ImageDraw, ImageFilter
from brand import *
import posts

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
OUT = os.path.join(os.path.dirname(HERE), "batch-12")
W = 1080

ITEMS = [  # file, slug, eyebrow, lines, arabic
    ("v12-anchor.png", "anchor-bolts", "KEZAD · GRID A (15–19)", ["ANCHOR BOLTS", "~SET TO GRID."], "تثبيت الأنكور بولت على القواعد"),
    ("v12-soil.png", "site-clearing", "KEZAD · SITE WORKS", ["EXCESS SOIL", "~CLEARED."], "إزالة التربة الزائدة من الموقع"),
    ("v12-rafter.png", "peb-rafters", "KEZAD · GRID (5–9)", ["PEB RAFTERS", "~GOING UP."], "تجميع جسور الرافتر — المباني الجاهزة"),
]


def photo(path, w, h):
    """Cover-fit with a gentle sharpen to compensate for the small source."""
    im = cover(path, (w, h)).filter(ImageFilter.UnsharpMask(radius=1.6, percent=70, threshold=2))
    return grade(im, sat=0.95).convert("RGBA")


def feed(i, src, eb, lines, ar):
    Wf, Hf = posts.FEED
    ph = 900
    im = Image.new("RGBA", (Wf, Hf), INK + (255,))
    im.alpha_composite(photo(src, Wf, ph))
    im.alpha_composite(gradient((Wf, ph), bottom=1.0, start=0.55), (0, 0))   # photo melts into the ink panel
    im.alpha_composite(top_scrim((Wf, Hf), amount=0.45))
    posts.headline(im, eb, lines, ar, Hf - 120, size=104)
    footer_bar(im)
    watermark(im, w=170)
    return im


def story(src, eb, lines, ar):
    Ws, Hs = posts.STORY
    bg = cover(src, (Ws, Hs)).filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new("RGB", (Ws, Hs), INK), 0.55).convert("RGBA")
    fh = round(Ws * 734 / 975)
    ph = photo(src, Ws, fh)
    ph.alpha_composite(gradient((Ws, fh), bottom=0.85, start=0.6))       # soft lower edge, no hard line
    bg.alpha_composite(ph, (0, 300))
    bg.alpha_composite(gradient((Ws, Hs), bottom=0.9, start=0.62))
    posts.headline(bg, eb, lines, ar, Hs - 300, size=112, ar_size=50)
    watermark(bg, w=170, pos="tl", margin=64, y=210)
    return bg


if __name__ == "__main__":
    for i, (f, slug, eb, lines, ar) in enumerate(ITEMS, start=1):
        src = os.path.join(SRC, f)
        save(feed(i, src, eb, lines, ar), os.path.join(OUT, "feed", f"{15 + i}-kezad-{slug}.jpg"))
        save(story(src, eb, lines, ar), os.path.join(OUT, "stories", f"0{i}-kezad-{slug}.jpg"))
    print("batch12 done")
