"""Batch 13: 10-second brand promo from the Google Flow (Veo) clip — four shots (pour, weld, lift, reveal)
re-titled in the house style, watermark, 2 s end card. Keeps Veo's own soundtrack continuous (its hits
already land on the cuts), so segment audio is discarded and the original track is muxed back."""
import os, subprocess
from brand import *
import reels

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source", "v13-flow-promo.mp4")
OUT = os.path.join(os.path.dirname(HERE), "batch-13")
reels.OUT = os.path.join(OUT, "reels")

SHOTS = [  # name, start, dur (cuts measured with scdet: 1.917, 4.0, 6.0), eyebrow, lines, arabic
    ("f1", 0.0, 1.917, "CIVIL WORKS", ["FOUNDATIONS", "~POURED."], "صبّ الأساسات"),
    ("f2", 1.917, 2.083, "FABRICATION", ["WELDED", "~IN-HOUSE."], "تصنيع في ورشتنا"),
    ("f3", 4.0, 2.0, "ERECTION", ["STEEL", "~RAISED."], "تركيب الهياكل المعدنية"),
    ("f4", 6.0, 2.0, "STEEL BUILDER", ["BUILT", "~TO LAST."], "نبني ليدوم"),
]
END = 2.0


def build():
    segs = [reels.segment(n, SRC, ss, d, reels.layer(n, eb, ln, ar, size=116), fade_in=0.05, title_in=0.1)
            for n, ss, d, eb, ln, ar in SHOTS]
    segs.append(reels.endcard(END))
    silent = reels.concat("_promo-video", segs)
    total = sum(s[2] for s in SHOTS) + END
    out = os.path.join(reels.OUT, "reel-22-brand-promo-10s.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", SRC, "-filter_complex",
                    f"[1:a]atrim=0:{total},afade=out:st={total - 1.5}:d=1.5,"
                    "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-t", str(total), "-movflags", "+faststart", out], check=True)
    os.remove(silent)
    frame = os.path.join(reels.TMP, "promo-frame.jpg")
    reels.run(["ffmpeg", "-y", "-v", "error", "-ss", "7.2", "-i", SRC, "-frames:v", "1", "-q:v", "2", frame])
    reels.cover_image("reel-22", frame, "STEEL BUILDER", ["BUILT", "~TO LAST."], "من الأساس للهيكل", (0.5, 0.5))
    print(out, total)


if __name__ == "__main__":
    build()
