"""Batch 7: shear-stud welding on metal deck (client-confirmed as their own work)."""
import os
from brand import *
import posts, reels

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
OUT = os.path.join(os.path.dirname(HERE), "batch-07")
V = os.path.join(SRC, "v7-stud-welding.mov")
reels.OUT = os.path.join(OUT, "reels")


def seg(name, ss, dur, eb=None, lines=None, ar=None, size=104, title_in=0.35):
    ov = reels.layer(name, eb, lines, ar, size=size) if lines else reels.layer(name)
    return reels.segment(name, V, ss, dur, ov, title_in=title_in)


if __name__ == "__main__":
    reels.concat("reel-17-stud-welding", [
        seg("s1", 0.0, 6.0, "ON THE DECK", ["STUD WELDING", "~ON METAL DECK."], "لحام مسامير القص على الصاج", size=96, title_in=0.1),
        seg("s2", 6.0, 7.0, "COMPOSITE FLOOR", ["LOCKING STEEL", "~TO CONCRETE."], "ربط الحديد بالخرسانة"),
        seg("s3", 13.0, 8.0, "STEEL BUILDER", ["STUD", "~BY STUD."], "مسمار بعد مسمار"),
        reels.endcard()])
    fr = os.path.join(reels.TMP, "f.jpg")
    reels.run(["ffmpeg", "-y", "-v", "error", "-ss", "3.0", "-i", V, "-frames:v", "1", "-q:v", "2", fr])
    im = posts.base(fr, (1080, 1920), (0.5, 0.5), scrim=0.95, start=0.3, top=0.5)
    posts.headline(im, "STUD WELDING", ["LOCKING STEEL", "~TO CONCRETE."], "ربط الحديد بالخرسانة", 1560, size=110, ar_size=54)
    watermark(im, w=190, pos="tl", margin=64, y=310)
    save(im, os.path.join(reels.OUT, "covers", "reel-17-cover.jpg"))
    print("batch7 done")
