"""Batch 17: foundation-steps clip (Flow) re-branded with kinetic Arabic subtitles.
The source carries a mis-spelt logo box (top-left, x<158 y<118) and burnt-in subtitles (y>=470): the frame is
cropped to x>=160, y<462, which removes both, then floated on its own blur. Subtitles are re-typeset (typos fixed)
and animated word by word: orange step number, rule wipe, staggered rise-and-fade, keyword in orange."""
import os, subprocess, math
import numpy as np
from PIL import Image, ImageDraw
from brand import *
import reels

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source", "v17-foundation-steps.mov")
OUT = os.path.join(os.path.dirname(HERE), "batch-17")
reels.OUT = os.path.join(OUT, "reels")
W, H, FPS, DUR = 1080, 1920, 30, 10.0
FG_Y, FG_H = 470, 578                  # cropped 864x462 source scaled to 1080x578
SUB_Y = 1170                           # top of the subtitle block
R = W - 72                             # right margin (Arabic is right-aligned)

CUES = [  # start, end, text, index of the word set in orange
    (0.15, 1.40, "بدء تجهيز الموقع الإنشائي", 2),
    (1.55, 2.90, "تركيب حديد التسليح والقوالب بدقة عالية", 2),
    (3.05, 4.35, "فحص جودة الهياكل الحديدية", 1),
    (4.50, 5.90, "صبّ الخرسانة وفق أعلى المعايير", 4),
    (6.05, 7.40, "الموقع جاهز للمراحل التالية", 1),
    (7.55, 8.85, "دقة في التنفيذ، وجودة في الإنشاء", 5),
]
FA = font("kufi", 74)
FN = font("xbold", 44)
AR = {"direction": "rtl", "language": "ar"}


def ease_out(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def layout(words, d, maxw=W - 144):
    """Greedy RTL line wrap -> list of lines, each a list of (word_index, word, width)."""
    sp = d.textlength(" ", font=FA)
    lines, cur, cw = [], [], 0
    for i, w in enumerate(words):
        ww = d.textlength(w, font=FA, **AR)
        if cur and cw + sp + ww > maxw:
            lines.append(cur); cur, cw = [], 0
        cur.append((i, w, ww)); cw += (sp if len(cur) > 1 else 0) + ww
    lines.append(cur)
    return lines, sp


def static_layer():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    im.alpha_composite(gradient((W, H), bottom=0.85, start=0.55))
    d = ImageDraw.Draw(im)
    eyebrow(d, 72, FG_Y - 52, "FOUNDATION WORKS")
    text(d, (R, FG_Y - 52), "مراحل تنفيذ الأساسات", font("ar", 34), fill=STEEL, anchor="rm", rtl=True)
    watermark(im, w=170, pos="tl", margin=64, y=190)
    return im


def subtitle_frame(t, base):
    im = base.copy()
    d = ImageDraw.Draw(im)
    for n, (s, e, txt, key) in enumerate(CUES, start=1):
        if not (s - 0.01 <= t <= e + 0.25):
            continue
        out = ease_out((t - e) / 0.25) if t > e else 0.0            # exit: fade + lift
        lift = -24 * out
        alpha_all = 1 - out
        # step number + rule wipe (right side)
        p = ease_out((t - s) / 0.3)
        num = f"{n:02d}"
        a = int(255 * p * alpha_all)
        d.text((R, SUB_Y + lift + (1 - p) * 20), num, font=FN, fill=ORANGE + (a,), anchor="ra")
        nw = d.textlength(num, font=FN)
        rule = (W - 144 - nw - 24) * ease_out((t - s) / 0.45)
        y_rule = SUB_Y + 26 + lift
        d.rectangle((R - nw - 24 - rule, y_rule - 2, R - nw - 24, y_rule + 2), fill=ORANGE + (int(200 * alpha_all),))
        # words: staggered rise + fade, right to left
        words = txt.split()
        lines, sp = layout(words, d)
        y = SUB_Y + 78 + lift
        for line in lines:
            x = R
            for i, w, ww in line:
                q = ease_out((t - s - 0.12 - i * 0.07) / 0.32)
                if q > 0:
                    col = ORANGE if i == key else WHITE
                    d.text((x, y + (1 - q) * 46), w, font=FA, fill=col + (int(255 * q * alpha_all),), anchor="ra", **AR)
                x -= ww + sp
            y += 116
    return im


def make_cover():
    """Wide 'site ready' frame at full width over its own blur; title on the ink below."""
    import posts
    from PIL import ImageFilter
    frame = os.path.join(reels.TMP, "fs-frame.png")
    reels.run(["ffmpeg", "-y", "-v", "error", "-ss", "6.8", "-i", SRC, "-frames:v", "1", "-vf", "crop=864:462:160:0", frame])
    ph = Image.open(frame).convert("RGB")
    bg = cover(ph, (W, H)).filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new("RGB", (W, H), INK), 0.55).convert("RGBA")
    fg = grade(ph.resize((W, FG_H), Image.LANCZOS), sat=1.0).convert("RGBA")
    fg.alpha_composite(gradient(fg.size, bottom=0.8, start=0.65))
    bg.alpha_composite(fg, (0, 380))
    bg.alpha_composite(gradient((W, H), bottom=0.92, start=0.55))
    posts.headline(bg, "FOUNDATION WORKS", ["STEP BY", "~STEP."], "مراحل تنفيذ الأساسات", 1560, size=120, ar_size=54)
    watermark(bg, w=190, pos="tr", margin=64, y=310)
    save(bg, os.path.join(reels.OUT, "covers", "reel-27-cover.jpg"))


def build():
    os.makedirs(reels.OUT, exist_ok=True)
    main = os.path.join(reels.TMP, "fs-main.mp4")
    vf = ("[0:v]crop=864:462:160:0,split[a][b];"
          f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=40,"
          "eq=brightness=-0.2:saturation=0.6[bg];"
          f"[b]scale={W}:{FG_H}:flags=lanczos,eq=contrast=1.06:saturation=1.05,unsharp=5:5:0.6[fg];"
          f"[bg][fg]overlay=0:{FG_Y},fps={FPS},format=rgba[v0];"
          "[1:v]format=rgba[sub];[v0][sub]overlay=0:0,fade=in:st=0:d=0.3,format=yuv420p[v];"
          f"[0:a]afade=out:st={DUR - 0.8}:d=0.8[a]")
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-i", SRC, "-f", "rawvideo", "-pix_fmt", "rgba",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-filter_complex", vf,
                           "-map", "[v]", "-map", "[a]", "-t", str(DUR), "-c:v", "libx264", "-preset", "medium",
                           "-crf", "18", "-c:a", "aac", "-b:a", "160k", "-ac", "2", "-ar", "44100", main],
                          stdin=subprocess.PIPE)
    base = static_layer()
    for i in range(int(DUR * FPS)):
        ff.stdin.write(subtitle_frame(i / FPS, base).tobytes())
    ff.stdin.close(); ff.wait()
    out = reels.concat("reel-27-foundation-steps", [main, reels.endcard(3.5)])
    make_cover()
    return out


if __name__ == "__main__":
    import sys
    print(make_cover() if sys.argv[1:] == ["cover"] else build())
