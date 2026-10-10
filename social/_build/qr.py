"""QR codes (WhatsApp, Location, Company Profile): print files + Instagram highlight stories + cover.
Every QR is decoded back with OpenCV before it is saved as final."""
import os, urllib.parse
import segno, cv2, numpy as np
from PIL import Image, ImageDraw
from brand import *
import highlights as hl

HERE = os.path.dirname(os.path.abspath(__file__))
SOC = os.path.dirname(HERE)
OUT = os.path.join(SOC, "qr")
W, H = 1080, 1920

CODES = {
    "whatsapp": ("https://wa.me/971502332844?text=" + urllib.parse.quote("Hello Steel Builder, I'd like a quote."),
                 "WhatsApp", "CHAT WITH US", "تواصل معنا على واتساب", "+971 50 233 2844", "whatsapp"),
    "location": ("https://maps.google.com/?q=24.353325,54.513988",
                 "Location", "VISIT OUR WORKSHOP", "موقع ورشتنا — مصفح", "Musaffah, Abu Dhabi", "location"),
    "profile": ("https://steelbuilderuae.com/profile.pdf",
                "Company Profile", "COMPANY PROFILE", "الملف التعريفي للشركة", "steelbuilderuae.com/profile.pdf", "profile"),
}


def decode(img):
    """Return the payload only if BOTH OpenCV decoders read it (strict: stands in for older phone cameras)."""
    arr = cv2.cvtColor(np.asarray(img.convert("RGB")), cv2.COLOR_RGB2BGR)
    a = cv2.QRCodeDetector().detectAndDecode(arr)[0]
    b = cv2.QRCodeDetectorAruco().detectAndDecode(arr)[0]
    return a if a == b else ""


def qr_image(url, size=1400, logo=True):
    q = segno.make(url, error="h")
    m = [list(r) for r in q.matrix]
    n = len(m); quiet = 4; cell = size // (n + 2 * quiet)
    side = cell * (n + 2 * quiet)
    im = Image.new("RGBA", (side, side), (255, 255, 255, 255))
    d = ImageDraw.Draw(im)
    finders = [(0, 0), (0, n - 7), (n - 7, 0)]
    def in_finder(r, c):
        return any(fr <= r < fr + 7 and fc <= c < fc + 7 for fr, fc in finders)
    for r in range(n):
        for c in range(n):
            if m[r][c] and not in_finder(r, c):
                x = (c + quiet) * cell; y = (r + quiet) * cell
                d.rectangle((x, y, x + cell - 1, y + cell - 1), fill=INK)
    for fr, fc in finders:  # brand-navy finder eyes (square: rounded eyes failed OpenCV's classic detector)
        x = (fc + quiet) * cell; y = (fr + quiet) * cell
        d.rectangle((x, y, x + 7 * cell - 1, y + 7 * cell - 1), fill=NAVY)
        d.rectangle((x + cell, y + cell, x + 6 * cell - 1, y + 6 * cell - 1), fill=WHITE)
        d.rectangle((x + 2 * cell, y + 2 * cell, x + 5 * cell - 1, y + 5 * cell - 1), fill=NAVY)
    if logo:  # centre logo on a white disc — within error-correction H budget (~7% of area)
        lw = int(side * 0.20)
        lg = logo_scaled(lw)
        r = int(lw * 0.62)
        cx = cy = side // 2
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE)
        im.alpha_composite(lg, (cx - lg.width // 2, cy - lg.height // 2))
    return im, q


def story(key):
    url, label, en, ar, sub, icon = CODES[key]
    im = hl.bg()
    y = hl.badge(im, icon if icon != "profile" else "about", y=300, size=200)
    y = hl.title(im, y - 20, en, ar, size=84)
    card = 760
    qr, _ = qr_image(url, size=card - 80)
    qr = qr.resize((card - 80, card - 80), Image.LANCZOS)
    cy = y + 30
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(((W - card) // 2, cy, (W + card) // 2, cy + card), radius=36, fill=WHITE)
    im.alpha_composite(qr, ((W - qr.width) // 2, cy + 40))
    y = cy + card + 60
    text(d, (W // 2, y), "SCAN WITH YOUR CAMERA", font("bold", 30), fill=ORANGE, anchor="mm", spacing=6)
    text(d, (W // 2, y + 52), "امسح الكود بكاميرا الموبايل", font("arb", 34), fill=STEEL, anchor="mm", rtl=True)
    text(d, (W // 2, y + 112), sub, font("med", 36), fill=WHITE, anchor="mm")
    watermark(im, w=150, pos="tl", margin=64, y=150)
    hl.foot(im)
    return im


def cover_profile():
    """Highlight cover for the new 'Profile' highlight — same ring + white icon system."""
    im = Image.new("RGBA", (W, H), INK + (255,))
    disc = hl.ring_disc(1000, fill=INK, ring=ORANGE)
    im.alpha_composite(disc, ((W - 1000) // 2, (H - 1000) // 2))
    big = 560 * hl.SS
    ic = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    ImageDraw.Draw(ic).text((big // 2, big // 2), "description", font=hl.sym(int(big * 0.86)), fill=WHITE, anchor="mm")
    ic = ic.resize((560, 560), Image.LANCZOS)
    im.alpha_composite(ic, ((W - 560) // 2, (H - 560) // 2))
    return im


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "print"), exist_ok=True)
    report = []
    for key, (url, label, *_rest) in CODES.items():
        qr, q = qr_image(url, size=2000)
        assert decode(qr) == url, f"{key}: print QR does not decode"
        qr.convert("RGB").save(os.path.join(OUT, "print", f"qr-{key}.png"), dpi=(300, 300))
        q.save(os.path.join(OUT, "print", f"qr-{key}-plain.svg"), scale=10, border=4, dark="#141517")
        st = story(key)
        small = st.convert("RGB").resize((540, 960), Image.LANCZOS)   # phone-screen size check
        assert decode(st) == url and decode(small) == url, f"{key}: story QR does not decode"
        save(st, os.path.join(OUT, "stories", f"qr-{key}.jpg"), q=95)
        report.append(f"{key}: OK  {url}  (version {q.version}, error H)")
    save(cover_profile(), os.path.join(OUT, "stories", "cover-profile.jpg"), q=95)
    print("\n".join(report))
