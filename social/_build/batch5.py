"""Excavators-only reel (requested): v-excavation + the close excavator shot from v2-excavator."""
import os
from brand import *
import reels

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
OUT = os.path.join(os.path.dirname(HERE), "batch-05")
EXC = os.path.join(SRC, "v-excavation.mp4")
EXC2 = os.path.join(SRC, "v2-excavator.mp4")
reels.OUT = os.path.join(OUT, "reels")


def seg(name, src, ss, dur, eb=None, lines=None, ar=None, size=104, landscape=False, title_in=0.35):
    ov = reels.layer(name, eb, lines, ar, size=size) if lines else reels.layer(name)
    return reels.segment(name, src, ss, dur, ov, landscape=landscape, title_in=title_in)


if __name__ == "__main__":
    reels.concat("reel-16-excavators", [
        seg("x1", EXC, 0.0, 3.0, "CIVIL WORKS", ["THE DIG", "~STARTS HERE."], "الحفر يبدأ من هنا", title_in=0.1),
        seg("x2", EXC2, 0.0, 1.4, landscape=True, title_in=0.0),
        seg("x3", EXC, 3.0, 3.0, "EXCAVATION", ["TRENCH", "~BY TRENCH."], "حفر خندق بعد خندق"),
        seg("x4", EXC, 8.1, 3.1, "BEFORE THE STEEL", ["DUG TO", "~LEVEL."], "حفر على المنسوب المطلوب"),
        reels.endcard()])
    frame = os.path.join(reels.TMP, "x.jpg")
    reels.run(["ffmpeg", "-y", "-v", "error", "-ss", "4.4", "-i", EXC, "-frames:v", "1", "-q:v", "2", frame])
    reels.cover_image("reel-16", frame, "EXCAVATORS", ["THE DIG", "~STARTS HERE."], "الحفر يبدأ من هنا", (0.5, 0.5))
    print("batch5 done")
