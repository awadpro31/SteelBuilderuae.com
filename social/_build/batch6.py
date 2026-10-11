"""Batch 6: the enhanced 2x2 progress collage -> feed post (4:5) + story (9:16)."""
import os
from PIL import Image, ImageDraw
from brand import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "batch-06")
COLLAGE = os.path.join(HERE, "source", "13-collage-enhanced.jpg")
LABELS = [("01", "FORMWORK", "الشدّات"), ("02", "PEDESTALS", "القواعد"), ("03", "ANCHOR BOLTS", "المسامير"), ("04", "FRAMES", "الهياكل")]
TILES = [(0, 0, 636, 370), (644, 0, 1280, 370), (0, 376, 636, 720), (644, 376, 1280, 720)]  # 8px white gutters in the source


def grid(width):
    """Rebuild the collage with our own ink gutters + numbered labels (drops the source's white gutters)."""
    src = Image.open(COLLAGE).convert("RGB")
    g = 8
    tw = (width - g) // 2
    th = round(tw * 370 / 636)
    out = Image.new("RGBA", (width, th * 2 + g), INK + (255,))
    d = ImageDraw.Draw(out)
    for i, (box, (n, en, ar)) in enumerate(zip(TILES, LABELS)):
        t = grade(src.crop(box).resize((tw, th), Image.LANCZOS), sat=0.92).convert("RGBA")
        t.alpha_composite(gradient((tw, th), bottom=0.85, start=0.5))
        x = (i % 2) * (tw + g); y = (i // 2) * (th + g)
        out.alpha_composite(t, (x, y))
        text(d, (x + 22, y + th - 62), n, font("bold", 24), fill=ORANGE)
        text(d, (x + 22, y + th - 32), en, font("bold", 26), fill=WHITE, spacing=3)
        text(d, (x + tw - 22, y + th - 32), ar, font("arb", 28), fill=STEEL, anchor="rs", rtl=True)
    return out


def header(d, y, size=78):
    eyebrow(d, 64, y, "SITE PROGRESS")
    d.text((60, y + 34), "FROM FORMWORK", font=font("xbold", size), fill=WHITE)
    d.text((60, y + 34 + size), "TO FRAMES.", font=font("xbold", size), fill=ORANGE)
    text(d, (1080 - 64, y + 34 + size * 2 + 40), "من الشدّات إلى الهياكل", font("kufi", 42), fill=STEEL, anchor="rm", rtl=True)


def post():
    im = Image.new("RGBA", (1080, 1350), INK + (255,))
    d = ImageDraw.Draw(im)
    header(d, 140)
    gr = grid(1080 - 2 * 40)
    im.alpha_composite(gr, (40, 470))
    text(d, (540, 470 + gr.height + 70), "ONE TEAM · ONE SITE", font("bold", 28), fill=ORANGE, anchor="mm", spacing=6)
    text(d, (540, 470 + gr.height + 120), "فريق واحد · موقع واحد", font("arb", 32), fill=STEEL, anchor="mm", rtl=True)
    footer_bar(im)
    watermark(im, w=150, margin=48)
    save(im, os.path.join(OUT, "feed", "14-formwork-to-frames.jpg"))


def story():
    im = Image.new("RGBA", (1080, 1920), INK + (255,))
    d = ImageDraw.Draw(im)
    header(d, 420, size=92)
    gr = grid(1080 - 2 * 40)
    im.alpha_composite(gr, (40, 800))
    text(d, (540, 800 + gr.height + 90), "ONE TEAM · ONE SITE", font("bold", 30), fill=ORANGE, anchor="mm", spacing=6)
    text(d, (540, 800 + gr.height + 145), "فريق واحد · موقع واحد", font("arb", 34), fill=STEEL, anchor="mm", rtl=True)
    watermark(im, w=170, pos="tl", margin=64, y=190)
    save(im, os.path.join(OUT, "stories", "04-formwork-to-frames.jpg"))


if __name__ == "__main__":
    post(); story(); print("batch6 done")
