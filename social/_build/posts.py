"""Renders every still: feed posts, carousel, stories, highlight covers, profile picture."""
import os
from PIL import Image, ImageDraw
from brand import *

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
OUT = os.path.join(os.path.dirname(HERE))
P = {  # source photos
    "crane": os.path.join(SRC, "1.jpg"),        # crane + rafters, vertical
    "portal": os.path.join(SRC, "2.jpg"),       # long portal-frame perspective
    "crew": os.path.join(SRC, "3.jpg"),         # crew fixing rafter-to-column
    "purlins": os.path.join(SRC, "4.jpg"),      # purlins + manlift
    "frames": os.path.join(SRC, "5.jpg"),       # frames + manlift crew
}
FEED = (1080, 1350)
STORY = (1080, 1920)


def base(photo, size, focus=(0.5, 0.5), scrim=0.94, start=0.30, top=0.5, **g):
    im = grade(cover(photo, size, focus), **g).convert("RGBA")
    im.alpha_composite(gradient(size, bottom=scrim, start=start))
    if top:
        im.alpha_composite(top_scrim(size, amount=top))
    return im


def headline(img, eyebrow_txt, lines, ar, y_end, size=96, ar_size=46, x=64):
    """Bottom-anchored title block: eyebrow, EN caps headline, Arabic line."""
    d = ImageDraw.Draw(img)
    maxw = img.width - 2 * x - 40
    while size > 48 and max(d.textlength(l.lstrip("~"), font=font("xbold", size)) for l in lines) > maxw:
        size -= 4
    f = font("xbold", size)
    fa = font("kufi", ar_size)
    lh = int(size * 1.0)
    block = 36 + 34 + len(lines) * lh + 28 + int(ar_size * 1.9)
    y = y_end - block
    eyebrow(d, x, y + 13, eyebrow_txt)
    y += 60
    for i, ln in enumerate(lines):
        fill = ORANGE if ln.endswith(".") and i == len(lines) - 1 and ln.startswith("~") else WHITE
        ln = ln.lstrip("~")
        d.text((x - 4, y), ln, font=f, fill=fill)
        y += lh
    y += 22
    text(d, (img.width - x, y + 8), ar, fa, fill=STEEL, anchor="ra", rtl=True)


def post(name, photo, eb, lines, ar, focus=(0.5, 0.5), **kw):
    im = base(photo, FEED, focus, **kw)
    headline(im, eb, lines, ar, FEED[1] - 120)
    footer_bar(im)
    watermark(im, w=170)
    return save(im, os.path.join(OUT, "feed", name))


def stats_post():
    im = base(P["purlins"], FEED, (0.35, 0.5), scrim=0.95, start=0.05, top=0.4, bright=0.8)
    shade = Image.new("RGBA", FEED, INK + (110,))
    im.alpha_composite(shade)
    d = ImageDraw.Draw(im)
    eyebrow(d, 64, 330, "STEEL BUILDER IN NUMBERS")
    rows = [("2012", "FOUNDED — KUWAIT", "التأسيس — الكويت"),
            ("2019", "FOUNDED — UAE", "التأسيس — الإمارات"),
            ("+81,000", "M² OF PROJECT AREA", "متر مربع من المشاريع")]
    y = 400
    for big, en, ar in rows:
        d.line((64, y, FEED[0] - 64, y), fill=(255, 255, 255, 60), width=1)
        d.text((60, y + 30), big, font=font("xbold", 120), fill=WHITE)
        text(d, (64, y + 190), en, font("med", 24), fill=ORANGE, anchor="lm", spacing=4)
        text(d, (FEED[0] - 64, y + 190), ar, font("arb", 30), fill=STEEL, anchor="rm", rtl=True)
        y += 250
    footer_bar(im)
    watermark(im, w=170)
    return save(im, os.path.join(OUT, "feed", "04-numbers.jpg"))


def services_post():
    im = Image.new("RGBA", FEED, INK + (255,))
    ph = grade(cover(P["frames"], (FEED[0], 520), (0.5, 0.62))).convert("RGBA")
    im.alpha_composite(ph, (0, 0))
    im.alpha_composite(gradient((FEED[0], 520), bottom=1.0, start=0.3), (0, 0))
    d = ImageDraw.Draw(im)
    eyebrow(d, 64, 470, "WHAT WE BUILD")
    d.text((60, 500), "SIX SERVICES.", font=font("xbold", 84), fill=WHITE)
    d.text((60, 586), "ONE TEAM.", font=font("xbold", 84), fill=ORANGE)
    items = [("01", "Workshop fabrication", "التصنيع في الورشة"),
             ("02", "Steel structures", "الهياكل المعدنية"),
             ("03", "On-site erection", "التركيب في الموقع"),
             ("04", "Sandwich panels", "الساندوتش بانل"),
             ("05", "Metal cladding", "التكسية المعدنية"),
             ("06", "Civil works", "الأعمال المدنية")]
    y = 720
    for n, en, ar in items:
        d.line((64, y, FEED[0] - 64, y), fill=(255, 255, 255, 46), width=1)
        d.text((64, y + 22), n, font=font("med", 26), fill=ORANGE)
        d.text((130, y + 16), en, font=font("med", 36), fill=WHITE)
        text(d, (FEED[0] - 64, y + 36), ar, font("ar", 30), fill=MUTED, anchor="rm", rtl=True)
        y += 82
    footer_bar(im)
    watermark(im, w=170)
    return save(im, os.path.join(OUT, "feed", "06-services.jpg"))


# ---------- carousel: project spotlight ----------
def carousel():
    out = os.path.join(OUT, "carousel-project-spotlight")
    n = 6
    def counter(d, i):
        text(d, (FEED[0] - 64, FEED[1] - 70), f"{i:02d} / {n:02d}", font("med", 24),
             fill=(255, 255, 255, 200), anchor="rm", spacing=3)
    # 1 cover
    im = base(P["portal"], FEED, (0.55, 0.5), scrim=0.92, start=0.35)
    headline(im, "PROJECT SPOTLIGHT", ["FROM SAND", "~TO STEEL."], "من الرمل إلى الهيكل المعدني", FEED[1] - 130, size=120)
    d = ImageDraw.Draw(im)
    text(d, (64, FEED[1] - 70), "SWIPE  →", font("med", 24), fill=(255, 255, 255, 200), anchor="lm", spacing=4)
    counter(d, 1)
    watermark(im, w=170)
    save(im, os.path.join(out, "01-cover.jpg"))
    steps = [
        ("crane", (0.5, 0.45), "STEP 01", ["COLUMNS SET,", "RAFTERS FLY."], "تثبيت الأعمدة ورفع الجمالونات بالرافعة"),
        ("crew", (0.5, 0.35), "STEP 02", ["EVERY BOLT,", "BY HAND."], "تثبيت الوصلات يدوياً — وصلة بوصلة"),
        ("purlins", (0.6, 0.5), "STEP 03", ["PURLINS", "LOCKED IN."], "تركيب المدادات المجلفنة"),
        ("frames", (0.5, 0.7), "STEP 04", ["FRAME", "BY FRAME."], "إطار تلو الإطار — حتى اكتمال الهيكل"),
    ]
    for i, (k, fo, eb, ln, ar) in enumerate(steps, start=2):
        im = base(P[k], FEED, fo)
        headline(im, eb, ln, ar, FEED[1] - 130)
        d = ImageDraw.Draw(im)
        text(d, (64, FEED[1] - 70), "@STEEL_BUILDERR", font("med", 24), fill=(255, 255, 255, 200), anchor="lm", spacing=3)
        counter(d, i)
        watermark(im, w=170)
        save(im, os.path.join(out, f"{i:02d}-{k}.jpg"))
    # 6 CTA
    im = cta_card(FEED)
    d = ImageDraw.Draw(im)
    counter(d, 6)
    save(im, os.path.join(out, "06-cta.jpg"))


def cta_card(size, story=False):
    W, H = size
    im = Image.new("RGBA", size, INK + (255,))
    # faint frame photo texture
    ph = grade(cover(P["portal"], size, (0.5, 0.5)), sat=0.0, contrast=1.2).convert("RGBA")
    ph.putalpha(38)
    im.alpha_composite(ph)
    d = ImageDraw.Draw(im)
    lg = logo_scaled(300 if story else 250)
    # white disc behind logo
    cx, cy = W // 2, int(H * (0.27 if story else 0.25))
    r = lg.width // 2 + 42
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 255))
    im.alpha_composite(lg, (cx - lg.width // 2, cy - lg.height // 2))
    y = cy + r + 90
    text(d, (W // 2, y), "READY TO BUILD?", font("xbold", 92), fill=WHITE, anchor="mm")
    text(d, (W // 2, y + 90), "جاهز لبدء مشروعك؟", font("kufi", 48), fill=ORANGE, anchor="mm", rtl=True)
    y += 190
    rows = [("WHATSAPP / CALL", "+971 50 233 2844"), ("EMAIL", "info@steelbuilderuae.com"),
            ("WEB", "steelbuilderuae.com"), ("WORKSHOP", "Musaffah, Abu Dhabi")]
    for k, v in rows:
        d.line((140, y, W - 140, y), fill=(255, 255, 255, 50), width=1)
        text(d, (140, y + 44), k, font("med", 22), fill=MUTED, anchor="lm", spacing=4)
        text(d, (W - 140, y + 44), v, font("med", 34), fill=WHITE, anchor="rm")
        y += 88
    d.line((140, y, W - 140, y), fill=(255, 255, 255, 50), width=1)
    # orange button
    by = y + 70
    d.rounded_rectangle((W // 2 - 260, by, W // 2 + 260, by + 92), radius=8, fill=ORANGE)
    text(d, (W // 2, by + 46), "REQUEST A QUOTE", font("bold", 32), fill=WHITE, anchor="mm", spacing=4)
    return im


# ---------- stories ----------
def stories():
    out = os.path.join(OUT, "stories")
    im = base(P["crane"], STORY, (0.5, 0.5), scrim=0.95, start=0.38, top=0.55)
    headline(im, "LIVE FROM SITE", ["RAFTERS", "~GOING UP."], "الجمالونات ترتفع اليوم", STORY[1] - 330, size=120)
    watermark(im, w=170, pos="tl", margin=64, y=210)
    save(im, os.path.join(out, "01-live-from-site.jpg"))

    im = base(P["frames"], STORY, (0.5, 0.75), scrim=0.95, start=0.36, top=0.55)
    headline(im, "THIS WEEK", ["FRAME", "~BY FRAME."], "إطار تلو الإطار", STORY[1] - 330, size=120)
    watermark(im, w=170, pos="tl", margin=64, y=210)
    save(im, os.path.join(out, "02-this-week.jpg"))

    im = base(P["crew"], STORY, (0.5, 0.4), scrim=0.95, start=0.36, top=0.55)
    headline(im, "THE DETAIL", ["PRECISION", "~AT HEIGHT."], "الدقة على ارتفاع", STORY[1] - 330, size=120)
    watermark(im, w=170, pos="tl", margin=64, y=210)
    save(im, os.path.join(out, "03-precision.jpg"))

    im = cta_card(STORY, story=True)
    save(im, os.path.join(out, "04-request-a-quote.jpg"))


# ---------- highlight covers + profile ----------
def icon(d, kind, cx, cy, s, col):
    w = max(6, s // 16)
    if kind == "projects":   # I-beam section
        d.rectangle((cx - s // 2, cy - s // 2, cx + s // 2, cy - s // 2 + w * 2), fill=col)
        d.rectangle((cx - s // 2, cy + s // 2 - w * 2, cx + s // 2, cy + s // 2), fill=col)
        d.rectangle((cx - w, cy - s // 2, cx + w, cy + s // 2), fill=col)
    elif kind == "services":  # 2x3 grid
        g = s // 3
        for r in range(2):
            for c in range(3):
                x0 = cx - s // 2 + c * g + 6; y0 = cy - g + r * g + 6
                d.rectangle((x0, y0, x0 + g - 12, y0 + g - 12), outline=col, width=w)
    elif kind == "about":    # roof + house (echoes the logo)
        d.line((cx - s // 2, cy, cx, cy - s // 2, cx + s // 2, cy), fill=col, width=w, joint="curve")
        d.rectangle((cx - s // 3, cy, cx + s // 3, cy + s // 2), outline=col, width=w)
    elif kind == "contact":  # speech bubble
        d.rounded_rectangle((cx - s // 2, cy - s // 2.6, cx + s // 2, cy + s // 4), radius=s // 6, outline=col, width=w)
        d.polygon([(cx - s // 5, cy + s // 4 - 2), (cx - s // 3, cy + s // 2), (cx, cy + s // 4 - 2)], fill=col)
    elif kind == "site":     # hard hat
        d.chord((cx - s // 2.6, cy - s // 2.4, cx + s // 2.6, cy + s // 3), 180, 360, outline=col, width=w)
        d.rectangle((cx - s // 2, cy - 4, cx + s // 2, cy - 4 + w * 2), fill=col)
        d.rectangle((cx - w, cy - s // 2.4, cx + w, cy - s // 5), fill=col)


def highlights():
    out = os.path.join(OUT, "highlight-covers")
    for kind, en, ar in [("projects", "PROJECTS", "المشاريع"), ("services", "SERVICES", "الخدمات"),
                         ("site", "ON SITE", "من الموقع"), ("about", "ABOUT", "من نحن"),
                         ("contact", "CONTACT", "تواصل")]:
        im = Image.new("RGBA", STORY, INK + (255,))
        d = ImageDraw.Draw(im)
        cx, cy = STORY[0] // 2, STORY[1] // 2
        d.ellipse((cx - 330, cy - 330, cx + 330, cy + 330), outline=ORANGE, width=6)
        icon(d, kind, cx, cy - 20, 260, WHITE)
        save(im, os.path.join(out, f"{kind}.jpg"))
    # profile picture: logo on white, circle-safe
    im = Image.new("RGBA", (1080, 1080), (255, 255, 255, 255))
    lg = logo_scaled(760)
    im.alpha_composite(lg, ((1080 - lg.width) // 2, (1080 - lg.height) // 2 + 10))
    save(im, os.path.join(OUT, "profile", "profile-picture-1080.jpg"), q=95)


if __name__ == "__main__":
    post("01-strength-built-precisely.jpg", P["portal"], "STEEL BUILDER · UAE",
         ["STRENGTH,", "~BUILT PRECISELY."], "نبني القوة بدقة.", focus=(0.55, 0.5))
    post("02-every-bolt-by-hand.jpg", P["crew"], "ON SITE",
         ["EVERY BOLT.", "~BY HAND."], "كل وصلة تُنفَّذ بإتقان.", focus=(0.5, 0.33))
    post("03-frame-by-frame.jpg", P["crane"], "STEEL ERECTION",
         ["FRAME", "~BY FRAME."], "إطار تلو الإطار.", focus=(0.5, 0.45))
    stats_post()
    post("05-detail.jpg", P["frames"], "WHY STEEL BUILDER",
         ["THE DIFFERENCE", "~IS IN THE DETAIL."], "الفرق في التفاصيل.", focus=(0.5, 0.72))
    services_post()
    carousel()
    stories()
    highlights()
    print("stills done")
