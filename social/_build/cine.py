"""Cinematic camera moves on real site photos -> 12 shots + 3 branded reels.

Each shot is rendered frame-by-frame: an eased virtual camera (pan / tilt / push / pull / roll) over the
photo, plus drifting dust, optional warm light flare, film grain and vignette. Nothing is added to the
structure itself: every frame is the real photograph.
"""
import os, sys, math, random, subprocess
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from brand import *
import reels

HERE = os.path.dirname(os.path.abspath(__file__))
SOC = os.path.dirname(HERE)
SITE = os.path.dirname(SOC)
SHOTS = os.path.join(SOC, "cinematic", "shots")
OUT = os.path.join(SOC, "cinematic")
W, H, FPS, DUR = 1080, 1920, 30, 5.0
src = lambda f: os.path.join(HERE, "source", f) if f[0].isdigit() else os.path.join(SITE, f)

# id, photo, (cx,cy,zoom,roll) start, end, flare, fit
SHOT_LIST = [
    ("01-portal-push",   "2.jpg",              (0.55, 0.55, 1.00, 0), (0.60, 0.55, 1.38, 0), True, False),
    ("02-crane-tilt",    "1.jpg",              (0.50, 0.66, 1.18, 0), (0.50, 0.38, 1.18, 0), False, False),
    ("03-crew-orbit",    "3.jpg",              (0.44, 0.40, 1.12, -1.6), (0.56, 0.36, 1.24, 1.6), False, False),
    ("04-purlins-slide", "4.jpg",              (0.28, 0.50, 1.04, 0), (0.72, 0.50, 1.10, 0), False, False),
    ("05-frames-pull",   "5.jpg",              (0.52, 0.66, 1.45, 0), (0.50, 0.58, 1.04, 0), False, False),
    ("06-sunset-push",   "p-sunset.jpg",       (0.50, 0.46, 1.02, 0), (0.48, 0.42, 1.28, 0), True, False),
    ("07-beam-rise",     "p-crane-lift.jpg",   (0.50, 0.62, 1.16, 0), (0.52, 0.40, 1.20, 0), False, False),
    ("08-boom-drift",    "p-erect-boom.jpg",   (0.64, 0.50, 1.06, 0), (0.36, 0.50, 1.10, 0), False, False),
    ("09-roof-rotate",   "p-frame-square.jpg", (0.50, 0.45, 1.22, -3.0), (0.50, 0.42, 1.30, 3.0), False, False),
    ("10-portal-reveal", "p-portal.jpg",       (0.50, 0.55, 1.30, 0), (0.50, 0.50, 1.02, 0), True, False),
    ("11-column-push",   "p-crane-columns.jpg",(0.50, 0.52, 1.02, 0), (0.50, 0.68, 1.30, 0), False, False),
    ("12-yard-dolly",    "p-yard.jpg",         (0.42, 0.72, 1.62, 0), (0.70, 0.70, 1.66, 0), False, False),  # framed below the gate sign
]


def ease(t):  # smootherstep
    return t * t * t * (t * (t * 6 - 15) + 10)


def lerp(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def vignette():
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt(((x - W / 2) / (W * 0.62)) ** 2 + ((y - H / 2) / (H * 0.62)) ** 2)
    return np.clip(1 - 0.42 * np.clip(d - 0.55, 0, 1) ** 1.5 * 2.2, 0.55, 1)[..., None].astype(np.float32)


VIG = vignette()
RNG = np.random.default_rng(7)
GRAIN = [RNG.normal(0, 5.5, (H // 2, W // 2, 1)).astype(np.float32).repeat(2, 0).repeat(2, 1) for _ in range(6)]


def flare_layer(t):
    """Warm low sun glow drifting slowly across the top third."""
    cx = W * (0.78 - 0.12 * t); cy = H * 0.22
    y, x = np.mgrid[0:H:4, 0:W:4]
    d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / (W * 0.55)
    g = np.clip(1 - d, 0, 1) ** 2.2
    g = np.repeat(np.repeat(g, 4, 0), 4, 1)[:H, :W, None]
    return g * np.array([255, 170, 90], np.float32) * 0.28


class Dust:
    def __init__(self, n=70, seed=3):
        r = random.Random(seed)
        self.p = [[r.uniform(0, W), r.uniform(0, H), r.uniform(1.5, 4.5), r.uniform(-14, -4),
                   r.uniform(-6, 6), r.uniform(40, 110)] for _ in range(n)]

    def layer(self, f):
        im = Image.new("L", (W // 2, H // 2), 0)
        d = ImageDraw.Draw(im)
        for x, y, s, vx, vy, a in self.p:
            px = ((x + vx * f / FPS * 6) % W) / 2
            py = ((y + vy * f / FPS * 6 + math.sin(f / 20 + x) * 6) % H) / 2
            d.ellipse((px - s / 2, py - s / 2, px + s / 2, py + s / 2), fill=int(a))
        im = im.filter(ImageFilter.GaussianBlur(1.2)).resize((W, H), Image.BILINEAR)
        return np.asarray(im, np.float32)[..., None] / 255.0


def prepare(path):
    im = Image.open(path).convert("RGB")
    s = max(2, int(math.ceil(2400 / max(im.size))))
    return im.resize((im.width * s, im.height * s), Image.LANCZOS)


def camera(img, cx, cy, zoom, roll):
    iw, ih = img.size
    w0 = min(iw, ih * W / H)
    w = w0 / zoom
    s = w / W
    hw, hh = w / 2, w * H / W / 2
    th = math.radians(roll)
    # keep the rotated window inside the photo
    ex = hw * abs(math.cos(th)) + hh * abs(math.sin(th)); ey = hw * abs(math.sin(th)) + hh * abs(math.cos(th))
    X = min(max(cx * iw, ex), iw - ex); Y = min(max(cy * ih, ey), ih - ey)
    a, b = s * math.cos(th), -s * math.sin(th)
    d, e = s * math.sin(th), s * math.cos(th)
    c = X - (a * W / 2 + b * H / 2); f = Y - (d * W / 2 + e * H / 2)
    return img.transform((W, H), Image.AFFINE, (a, b, c, d, e, f), resample=Image.BICUBIC)


def fit_frame(img, bg, zoom):
    """Landscape photo: full width over its own blurred, darkened copy; slow zoom on the foreground."""
    fw = int(W * zoom); fh = int(fw * img.height / img.width)
    fg = img.resize((fw, fh), Image.BICUBIC).crop(((fw - W) // 2, 0, (fw - W) // 2 + W, fh))
    out = bg.copy(); out.paste(fg, (0, (H - fh) // 2 - 120))
    return out


def render(shot):
    name, photo, a, b, flare, fit = shot
    out = os.path.join(SHOTS, name + ".mp4")
    img = prepare(src(photo))
    if fit:
        bg = cover(img, (W, H)).filter(ImageFilter.GaussianBlur(45))
        bg = Image.blend(bg, Image.new("RGB", (W, H), INK), 0.45)
    dust = Dust(seed=hash(name) % 1000)
    n = int(DUR * FPS)
    os.makedirs(SHOTS, exist_ok=True)
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-f", "lavfi", "-t", str(DUR), "-i",
                           "anullsrc=r=44100:cl=stereo", "-map", "0:v", "-map", "1:a",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(n):
        t = ease(i / (n - 1))
        cx, cy, z, r = lerp(a, b, t)
        fr = fit_frame(img, bg, z) if fit else camera(img, cx, cy, z, r)
        arr = np.asarray(fr, np.float32)
        if flare:
            arr = 255 - (255 - arr) * (1 - flare_layer(i / n) / 255)  # screen blend
        arr = arr + dust.layer(i) * np.array([235, 215, 190], np.float32) * 0.55
        arr = arr * VIG + GRAIN[i % len(GRAIN)]
        ff.stdin.write(np.clip(arr, 0, 255).astype(np.uint8).tobytes())
    ff.stdin.close(); ff.wait()
    return out


def shot_path(k):
    return os.path.join(SHOTS, k + ".mp4")


def reel(name, parts):
    segs = []
    for i, (k, eb, lines, ar) in enumerate(parts):
        ov = reels.layer(f"{name}{i}", eb, lines, ar, size=104) if lines else reels.layer(f"{name}{i}")
        segs.append(reels.segment(f"{name}{i}", shot_path(k), 0.25, 4.5, ov, title_in=0.3 if i else 0.1))
    segs.append(reels.endcard())
    lst = os.path.join(reels.TMP, name + ".txt")
    open(lst, "w").writelines(f"file '{p}'\n" for p in segs)
    out = os.path.join(OUT, name + ".mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264",
                    "-preset", "slow", "-crf", "19", "-c:a", "aac", "-movflags", "+faststart", out], check=True)
    return out


if __name__ == "__main__":
    only = set(sys.argv[1:])
    if "reels" not in only:
        for s in SHOT_LIST:
            if not only or s[0] in only:
                print("render", s[0], flush=True); render(s)
    reel("cine-01-brand-film", [
        ("10-portal-reveal", "STEEL BUILDER · UAE", ["STRENGTH,", "~BUILT PRECISELY."], "نبني القوة بدقة."),
        ("01-portal-push", "STEEL STRUCTURES", ["SPAN", "~AFTER SPAN."], "هيكل بعد هيكل"),
        ("02-crane-tilt", "ERECTION", ["LIFTED", "~WITH A PLAN."], "رفع بخطة واضحة"),
        ("03-crew-orbit", "OUR CREW", ["EVERY BOLT.", "~BY HAND."], "كل وصلة تُنفَّذ بإتقان"),
        ("05-frames-pull", "ON SITE", ["FRAME", "~BY FRAME."], "إطار تلو الإطار"),
        ("06-sunset-push", "SINCE 2012", ["BUILT TO", "~LAST."], "نبني حلولاً تدوم"),
    ])
    reel("cine-02-workshop-to-site", [
        ("12-yard-dolly", "MUSAFFAH WORKSHOP", ["FROM THE", "~WORKSHOP…"], "من الورشة…"),
        ("07-beam-rise", "THE LIFT", ["…TO THE", "~SITE."], "…إلى الموقع"),
        ("08-boom-drift", "STEEL ERECTION", ["ONE TEAM.", "~START TO FINISH."], "فريق واحد من البداية للنهاية"),
        ("11-column-push", "PRECISION", ["SET TO", "~THE DRAWING."], "مطابق للرسم"),
    ])
    reel("cine-03-golden-hour", [
        ("06-sunset-push", "GOLDEN HOUR", ["STEEL", "~AT SUNSET."], "الحديد عند الغروب"),
        ("09-roof-rotate", "ROOF STRUCTURE", ["THE GRID", "~TAKES SHAPE."], "الهيكل يكتمل"),
        ("01-portal-push", "STEEL BUILDER", ["STRENGTH,", "~BUILT PRECISELY."], "نبني القوة بدقة."),
    ])
    print("cine done")
