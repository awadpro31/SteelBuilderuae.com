"""Story highlights: 9 covers + the branded stories that live inside each highlight."""
import os, shutil
from PIL import Image, ImageDraw, ImageFont
from brand import *
import posts

HERE = os.path.dirname(os.path.abspath(__file__))
SOCIAL = os.path.dirname(HERE)
SITE = os.path.dirname(SOCIAL)
COV = os.path.join(SOCIAL, "highlight-covers")
STO = os.path.join(SOCIAL, "highlight-stories")
W, H = 1080, 1920
SS = 4  # supersampling for crisp rings/icons

PHONE = "+971 50 233 2844"
WA_LINK = "wa.me/971502332844"
EMAIL = "info@steelbuilderuae.com"
WEB = "steelbuilderuae.com"
MAPS = "maps.google.com/?q=24.353325,54.513988"


def sym(size):
    return ImageFont.truetype(os.path.join(FONTS, "MaterialRounded.ttf"), size,
                              layout_engine=ImageFont.Layout.RAQM)


def glyph(kind, size, color=WHITE):
    """Return an RGBA icon tile (size x size)."""
    big = size * SS
    im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = big // 2
    if kind == "whatsapp":  # round chat bubble + handset (generic, not the trademark)
        r = int(big * 0.40); w = int(big * 0.055)
        d.ellipse((c - r, c - r, c + r, c + r), outline=color, width=w)
        tail = [(c - r * 0.62, c + r * 0.62), (c - r * 0.98, c + r * 1.02), (c - r * 0.25, c + r * 0.90)]
        d.polygon(tail, fill=color)
        d.ellipse((c - r + w, c - r + w, c + r - w, c + r - w), fill=(0, 0, 0, 0))
        d.text((c, c + big * 0.01), "call", font=sym(int(big * 0.46)), fill=color, anchor="mm")
    else:
        name = {"location": "location_on", "call": "call", "email": "mail", "web": "language",
                "projects": "warehouse", "site": "engineering", "services": "construction",
                "about": "info"}[kind]
        d.text((c, c), name, font=sym(int(big * 0.86)), fill=color, anchor="mm")
    return im.resize((size, size), Image.LANCZOS)


def ring_disc(size, fill=ORANGE, ring=None):
    big = size * SS
    im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((0, 0, big - 1, big - 1), fill=fill + (255,))
    if ring:
        w = int(big * 0.012)
        d.ellipse((w * 3, w * 3, big - w * 3, big - w * 3), outline=ring, width=w)
    return im.resize((size, size), Image.LANCZOS)


# ---------------------------------------------------------------- covers
COVERS = [("01-projects", "projects"), ("02-services", "services"), ("03-on-site", "site"),
          ("04-about", "about"), ("05-whatsapp", "whatsapp"), ("06-location", "location"),
          ("07-call", "call"), ("08-email", "email"), ("09-website", "web")]


def covers():
    shutil.rmtree(COV, ignore_errors=True); os.makedirs(COV)
    for name, kind in COVERS:
        im = Image.new("RGBA", (W, H), INK + (255,))
        disc = ring_disc(1000, fill=INK, ring=ORANGE)
        im.alpha_composite(disc, ((W - 1000) // 2, (H - 1000) // 2))
        ic = glyph(kind, 560)
        im.alpha_composite(ic, ((W - 560) // 2, (H - 560) // 2))
        save(im, os.path.join(COV, name + ".jpg"), q=95)


# ---------------------------------------------------------------- stories
def bg(photo=None, focus=(0.5, 0.5), dim=150):
    if photo:
        im = grade(cover(photo, (W, H), focus), sat=0.8).convert("RGBA")
        im.alpha_composite(Image.new("RGBA", (W, H), INK + (dim,)))
        im.alpha_composite(gradient((W, H), bottom=0.95, start=0.25))
    else:
        im = Image.new("RGBA", (W, H), INK + (255,))
        tex = grade(cover(posts.P["portal"], (W, H)), sat=0.0, contrast=1.2).convert("RGBA")
        tex.putalpha(34); im.alpha_composite(tex)
    return im


def badge(im, kind, y=430, size=230):
    disc = ring_disc(size, fill=ORANGE)
    im.alpha_composite(disc, ((W - size) // 2, y))
    ic = glyph(kind, int(size * 0.62))
    im.alpha_composite(ic, ((W - ic.width) // 2, y + (size - ic.height) // 2))
    return y + size


def title(im, y, en, ar, size=92):
    d = ImageDraw.Draw(im)
    f = font("xbold", size)
    while d.textlength(en, font=f) > W - 140:
        size -= 4; f = font("xbold", size)
    text(d, (W // 2, y + 70), en, f, fill=WHITE, anchor="mm")
    text(d, (W // 2, y + 70 + size * 0.95), ar, font("kufi", 50), fill=ORANGE, anchor="mm", rtl=True)
    return int(y + 70 + size * 0.95 + 70)


def rows(im, y, items, key=28, val=40):
    d = ImageDraw.Draw(im)
    for k, v in items:
        d.line((110, y, W - 110, y), fill=(255, 255, 255, 60), width=2)
        text(d, (110, y + 52), k, font("med", key), fill=MUTED, anchor="lm", spacing=4)
        if any("؀" <= ch <= "ۿ" for ch in v):
            text(d, (W - 110, y + 52), v, font("arb", val - 4), fill=WHITE, anchor="rm", rtl=True)
        else:
            text(d, (W - 110, y + 52), v, font("med", val), fill=WHITE, anchor="rm")
        y += 104
    d.line((110, y, W - 110, y), fill=(255, 255, 255, 60), width=2)
    return y


def big_line(im, y, s, size=64, color=WHITE):
    d = ImageDraw.Draw(im)
    f = font("bold", size)
    while d.textlength(s, font=f) > W - 140:
        size -= 2; f = font("bold", size)
    text(d, (W // 2, y), s, f, fill=color, anchor="mm")
    return y + size


def sticker_hint(im, y, en, ar):
    """Arrow pointing at the empty zone where the in-app link/location sticker goes."""
    d = ImageDraw.Draw(im)
    text(d, (W // 2, y), en, font("bold", 30), fill=WHITE, anchor="mm", spacing=6)
    text(d, (W // 2, y + 52), ar, font("arb", 32), fill=STEEL, anchor="mm", rtl=True)
    ax, ay = W // 2, y + 100
    d.line((ax, ay, ax, ay + 70), fill=ORANGE, width=6)
    d.polygon([(ax - 22, ay + 60), (ax + 22, ay + 60), (ax, ay + 92)], fill=ORANGE)
    # the free sticker zone sits at y+130 .. y+330 — keep it empty


def foot(im):
    d = ImageDraw.Draw(im)
    text(d, (W // 2, H - 200), "@STEELBUILDERUAE  ·  STEELBUILDERUAE.COM", font("med", 26),
         fill=(255, 255, 255, 190), anchor="mm", spacing=3)


def story(name, im, wm=True):
    if wm:
        watermark(im, w=170, pos="tl", margin=64, y=190)
    foot(im)
    return save(im, os.path.join(STO, name))


def stories():
    shutil.rmtree(STO, ignore_errors=True); os.makedirs(STO)
    yard = os.path.join(SITE, "p-yard.jpg")

    # WHATSAPP
    im = bg()
    y = badge(im, "whatsapp")
    y = title(im, y, "CHAT WITH US", "تواصل معنا على واتساب")
    y = big_line(im, y + 60, PHONE, 84)
    d = ImageDraw.Draw(im)
    text(d, (W // 2, y + 30), "Send your drawings — get a quote.", font("med", 36), fill=STEEL, anchor="mm")
    text(d, (W // 2, y + 90), "أرسل المخططات واحصل على عرض سعر", font("ar", 34), fill=MUTED, anchor="mm", rtl=True)
    sticker_hint(im, y + 200, "TAP THE LINK", "اضغط على الرابط")
    story("05-whatsapp/01-whatsapp.jpg", im)

    # LOCATION
    im = bg(yard, (0.5, 0.5), dim=120)
    y = badge(im, "location", y=400)
    y = title(im, y, "VISIT OUR WORKSHOP", "زوروا ورشتنا")
    y = rows(im, y + 30, [("AREA", "Musaffah, Abu Dhabi"), ("COUNTRY", "United Arab Emirates"),
                          ("HOURS", "Mon – Sat · 08:00 – 18:00"), ("GPS", "24.353325, 54.513988")])
    sticker_hint(im, y + 90, "TAP FOR DIRECTIONS", "اضغط للوصول")
    story("06-location/01-location.jpg", im)

    # CALL
    im = bg()
    y = badge(im, "call")
    y = title(im, y, "CALL US", "اتصل بنا")
    y = big_line(im, y + 60, PHONE, 84)
    y = rows(im, y + 60, [("DAYS", "Monday – Saturday"), ("HOURS", "08:00 – 18:00 GST")])
    sticker_hint(im, y + 90, "TAP TO CALL", "اضغط للاتصال")
    story("07-call/01-call.jpg", im)

    # EMAIL
    im = bg()
    y = badge(im, "email")
    y = title(im, y, "EMAIL US", "راسلنا")
    y = big_line(im, y + 60, EMAIL, 60)
    d = ImageDraw.Draw(im)
    text(d, (W // 2, y + 40), "Drawings · BOQ · Site location · Timeline", font("med", 34), fill=STEEL, anchor="mm")
    text(d, (W // 2, y + 100), "المخططات · جدول الكميات · موقع المشروع · المدة", font("ar", 32), fill=MUTED, anchor="mm", rtl=True)
    sticker_hint(im, y + 210, "TAP TO EMAIL", "اضغط للمراسلة")
    story("08-email/01-email.jpg", im)

    # WEBSITE
    im = bg(os.path.join(SITE, "p-portal.jpg"), dim=130)
    y = badge(im, "web", y=400)
    y = title(im, y, "OUR WEBSITE", "موقعنا الإلكتروني")
    y = big_line(im, y + 60, WEB, 72)
    d = ImageDraw.Draw(im)
    text(d, (W // 2, y + 40), "Projects · Services · Request a quote", font("med", 34), fill=STEEL, anchor="mm")
    sticker_hint(im, y + 150, "TAP THE LINK", "اضغط على الرابط")
    story("09-website/01-website.jpg", im)

    # ABOUT
    im = bg(os.path.join(SITE, "p-portal.jpg"), dim=170)
    y = badge(im, "about", y=380)
    y = title(im, y, "WHO WE ARE", "من نحن")
    d = ImageDraw.Draw(im)
    text(d, (W // 2, y + 10), "Steel structures — fabricated in our workshop,", font("med", 34), fill=STEEL, anchor="mm")
    text(d, (W // 2, y + 58), "erected by our own team.", font("med", 34), fill=STEEL, anchor="mm")
    y = rows(im, y + 120, [("FOUNDED", "Kuwait · 2012"), ("UAE", "Since 2019"),
                           ("PROJECT AREA", "+81,000 m²"), ("WORKSHOP", "Musaffah, Abu Dhabi")])
    story("04-about/01-who-we-are.jpg", im)

    im = bg()
    y = badge(im, "about", y=300)
    y = title(im, y, "WHAT WE BUILD FOR", "مجالات العمل")
    rows(im, y + 20, [("01", "Warehouses & stores"), ("02", "Private warehouses"), ("03", "Cattle farms"),
                      ("04", "Poultry houses"), ("05", "Villas"), ("06", "Any steel-framed facility")])
    story("04-about/02-fields.jpg", im)

    # SERVICES
    im = bg()
    y = badge(im, "services", y=300)
    y = title(im, y, "SIX SERVICES. ONE TEAM.", "ست خدمات — فريق واحد")
    rows(im, y + 20, [("01", "Workshop fabrication"), ("02", "Steel structures"), ("03", "On-site erection"),
                      ("04", "Sandwich panels"), ("05", "Metal cladding"), ("06", "Civil works")])
    story("02-services/01-services.jpg", im)

    # PROJECTS — list from steelbuilderuae.com
    im = bg()
    y = badge(im, "projects", y=300)
    y = title(im, y, "SELECTED PROJECTS", "من مشاريعنا")
    rows(im, y + 20, [("KIZAD · ABU DHABI", "35,000 m²"), ("SAIH SHUAIB · ABU DHABI", "12,000 m²"),
                      ("ICAD · ABU DHABI", "8,000 m²"), ("HABSHAN", "7,000 m²"),
                      ("ROYAL STEEL · DUBAI", "1,200 m²")], key=26, val=40)
    story("01-projects/01-selected-projects.jpg", im)
    for i, f in enumerate(sorted(os.listdir(os.path.join(SOCIAL, "carousel-project-spotlight")))[:5], start=2):
        src = Image.open(os.path.join(SOCIAL, "carousel-project-spotlight", f)).convert("RGBA")
        canvas = Image.new("RGBA", (W, H), INK + (255,))
        blur = cover(src.convert("RGB"), (W, H)).filter(ImageFilter.GaussianBlur(40)).convert("RGBA")
        blur.alpha_composite(Image.new("RGBA", (W, H), INK + (140,)))
        canvas.alpha_composite(blur)
        canvas.alpha_composite(src, (0, (H - src.height) // 2))
        save(canvas, os.path.join(STO, "01-projects", f"{i:02d}-{f}"))

    # ON SITE — the existing site stories
    os.makedirs(os.path.join(STO, "03-on-site"))
    for f in ["01-live-from-site.jpg", "02-this-week.jpg", "03-precision.jpg"]:
        shutil.copy(os.path.join(SOCIAL, "stories", f), os.path.join(STO, "03-on-site", f))


if __name__ == "__main__":
    covers()
    stories()
    print("highlights done")
