"""Batch 8: workshop yard walkthrough (deshaken copy v8-yard-clean.mp4)."""
import os
from brand import *
import posts, reels

HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(HERE, "source", "v8-yard-clean.mp4")
OUT = os.path.join(os.path.dirname(HERE), "batch-08")
reels.OUT = os.path.join(OUT, "reels")


def seg(name, ss, dur, eb=None, lines=None, ar=None, title_in=0.35):
    ov = reels.layer(name, eb, lines, ar, size=110) if lines else reels.layer(name)
    return reels.segment(name, V, ss, dur, ov, landscape=True, title_in=title_in)


if __name__ == "__main__":
    reels.concat("reel-18-workshop-yard", [
        seg("y1", 0.0, 4.8, "MUSAFFAH WORKSHOP", ["INSIDE", "~THE YARD."], "جوه ساحة الورشة", title_in=0.1),
        seg("y2", 9.5, 2.3),
        seg("y3", 16.6, 3.0, "FABRICATION", ["WORK", "~IN PROGRESS."], "التصنيع شغال"),
        seg("y4", 21.8, 2.2),
        seg("y5", 26.0, 4.0, "IN THE WORKSHOP", ["PARTS", "~FABRICATED."], "قطع مصنّعة"),
        seg("y6", 30.5, 2.9, "NEXT STOP", ["READY", "~FOR SITE."], "جاهزة للموقع"),
        reels.endcard()])
    fr = os.path.join(reels.TMP, "f.jpg")
    reels.run(["ffmpeg", "-y", "-v", "error", "-ss", "28.0", "-i", V, "-frames:v", "1", "-q:v", "2", fr])
    import batch4                                  # batch4 rebinds reels.OUT on import
    reels.OUT = os.path.join(OUT, "reels")
    im = batch4.fit_card(fr, "MUSAFFAH WORKSHOP", ["INSIDE", "~THE YARD."], "جوه ساحة الورشة", 1560)
    watermark(im, w=190, pos="tr", margin=64, y=310)
    save(im, os.path.join(reels.OUT, "covers", "reel-18-cover.jpg"))
    print("batch8 done")
