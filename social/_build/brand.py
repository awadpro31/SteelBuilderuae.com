"""Steel Builder social brand kit — shared rendering helpers (Pillow + raqm)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONTS = os.environ.get("SB_FONTS", os.path.join(os.path.dirname(__file__), "fonts"))

# Colours — taken from steelbuilderuae.com (index.html :root) and the logo
ORANGE = (223, 96, 53)     # --primary #df6035 (logo roof)
NAVY = (47, 75, 121)       # --secondary #2f4b79 (logo "SB")
INK = (20, 21, 23)         # near-black backdrop
STEEL = (229, 229, 229)    # --foreground dark #e5e5e5
MUTED = (150, 154, 160)
WHITE = (255, 255, 255)


def font(name, size):
    files = {
        "light": "OutLight.ttf", "med": "OutMed.ttf", "bold": "OutBold.ttf",
        "xbold": "OutXBold.ttf", "ar": "ArRegular.ttf", "arb": "ArBold.ttf",
        "kufi": "KufiBold.ttf",
    }
    return ImageFont.truetype(os.path.join(FONTS, files[name]), size,
                              layout_engine=ImageFont.Layout.RAQM)


def logo():
    return Image.open(os.path.join(ROOT, "logo.png")).convert("RGBA")


def logo_scaled(w):
    lg = logo()
    h = round(lg.height * w / lg.width)
    return lg.resize((w, h), Image.LANCZOS)


def watermark(img, w=150, pos="tr", margin=48, opacity=0.92, y=None):
    """Logo watermark with a soft white halo so it reads on sky AND steel."""
    lg = logo_scaled(w)
    a = lg.split()[3]
    halo = Image.new("RGBA", (lg.width + 60, lg.height + 60), (0, 0, 0, 0))
    glow = Image.new("RGBA", lg.size, (255, 255, 255, 255))
    glow.putalpha(a.point(lambda v: int(v * 0.85)))
    halo.paste(glow, (30, 30), glow)
    halo = halo.filter(ImageFilter.GaussianBlur(10))
    if opacity < 1:
        lg.putalpha(a.point(lambda v: int(v * opacity)))
    W, H = img.size
    x = W - lg.width - margin if pos.endswith("r") else margin
    if y is None:
        y = margin if pos.startswith("t") else H - lg.height - margin
    img.alpha_composite(halo, (x - 30, y - 30))
    img.alpha_composite(lg, (x, y))
    return img


def cover(src, size, focus=(0.5, 0.5)):
    """Crop-to-fill like CSS object-fit: cover."""
    im = Image.open(src).convert("RGB") if isinstance(src, str) else src.convert("RGB")
    W, H = size
    s = max(W / im.width, H / im.height)
    nw, nh = round(im.width * s), round(im.height * s)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = int((nw - W) * focus[0]); y = int((nh - H) * focus[1])
    return im.crop((x, y, x + W, y + H))


def grade(im, contrast=1.08, sat=0.88, bright=1.0):
    """House grade: slightly desaturated, crisper, steel-cool."""
    im = ImageEnhance.Contrast(im).enhance(contrast)
    im = ImageEnhance.Color(im).enhance(sat)
    if bright != 1.0:
        im = ImageEnhance.Brightness(im).enhance(bright)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))


def gradient(size, top=0.0, bottom=0.85, start=0.45, color=INK):
    """Vertical scrim: transparent at `start`, `bottom` alpha at the base."""
    W, H = size
    g = Image.new("L", (1, H))
    for yy in range(H):
        t = yy / H
        if t < start:
            v = top * (1 - t / start) if top else 0
        else:
            v = bottom * min(1.0, ((t - start) / (1 - start)) * 1.35) ** 1.15
        g.putpixel((0, yy), int(255 * v))
    g = g.resize((W, H))
    layer = Image.new("RGBA", (W, H), color + (0,))
    layer.putalpha(g)
    return layer


def top_scrim(size, amount=0.55, end=0.22):
    W, H = size
    g = Image.new("L", (1, H))
    for yy in range(H):
        t = yy / H
        g.putpixel((0, yy), int(255 * amount * max(0, 1 - t / end) ** 1.6))
    layer = Image.new("RGBA", (W, H), INK + (0,))
    layer.putalpha(g.resize((W, H)))
    return layer


def text(d, xy, s, f, fill=WHITE, anchor="la", spacing=0, rtl=False):
    kw = {"direction": "rtl", "language": "ar"} if rtl else {}
    if spacing:
        # manual tracking for Latin caps
        x, y = xy
        total = sum(d.textlength(c, font=f) for c in s) + spacing * (len(s) - 1)
        if anchor[0] == "r":
            x -= total
        elif anchor[0] == "m":
            x -= total / 2
        for c in s:
            d.text((x, y), c, font=f, fill=fill, anchor="l" + anchor[1])
            x += d.textlength(c, font=f) + spacing
        return total
    d.text(xy, s, font=f, fill=fill, anchor=anchor, **kw)


def eyebrow(d, x, y, s, color=ORANGE, size=26, rtl=False, right=False, label=(236, 236, 236)):
    """Orange rule + tracked caps label: the kit's signature."""
    f = font("bold", size)
    if right:
        w = text(d, (x, y), s, f, fill=color, anchor="rm", spacing=6)
        d.rectangle((x - w - 70, y - 2, x - w - 22, y + 2), fill=color)
    else:
        d.rectangle((x, y - 2, x + 48, y + 2), fill=color)
        text(d, (x + 70, y), s, f, fill=label, anchor="lm", spacing=6)


def footer_bar(img, handle="@steel_builderr", site="steelbuilderuae.com", y=None):
    W, H = img.size
    d = ImageDraw.Draw(img)
    y = H - 70 if y is None else y
    f = font("med", 24)
    d.line((64, y - 30, W - 64, y - 30), fill=(255, 255, 255, 70), width=1)
    text(d, (64, y), handle.upper(), f, fill=(255, 255, 255, 200), anchor="lm", spacing=3)
    text(d, (W - 64, y), site.upper(), f, fill=(255, 255, 255, 200), anchor="rm", spacing=3)


def save(img, path, q=93):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.convert("RGB").save(path, "JPEG", quality=q, optimize=True, progressive=True)
    return path
