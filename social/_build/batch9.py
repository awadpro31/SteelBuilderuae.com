"""Batch 9: process reel — excavation → workshop → fabrication → steel erection, original soundtrack."""
import os, subprocess
from brand import *
import posts, reels, music

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
OUT = os.path.join(os.path.dirname(HERE), "batch-09")
reels.OUT = os.path.join(OUT, "reels")
S = lambda f: os.path.join(SRC, f)

# (name, src, start, dur, landscape, eyebrow, lines, arabic)
PLAN = [
    ("c1a", S("v-excavation.mp4"), 0.0, 3.0, False, "01 · EXCAVATION", ["IT STARTS", "~BELOW GROUND."], "الحفر — البداية من تحت الأرض"),
    ("c1b", S("v2-excavator.mp4"), 0.0, 1.4, True, None, None, None),
    ("c1c", S("v9-grade-beams.mov"), 2.0, 2.8, False, None, None, None),
    ("c2a", S("v8-yard-clean.mp4"), 0.5, 3.8, True, "02 · WORKSHOP", ["OUR", "~WORKSHOP."], "الورشة — مصفح"),
    ("c3a", S("v2-workshop.mp4"), 5.0, 3.8, False, "03 · FABRICATION", ["CUT. FIT.", "~WELD."], "التصنيع — قص وتجميع ولحام"),
    ("c3b", S("v8-yard-clean.mp4"), 26.0, 3.0, True, None, None, None),
    ("c4a", S("v9-rafters-prep.mov"), 0.0, 3.0, False, "04 · ERECTION", ["STEEL", "~GOES UP."], "تركيب الحديد"),
    ("c4b", S("v-lift.mp4"), 4.0, 4.5, False, None, None, None),          # stops before the hand-over-lens at 9.7s
    ("c4c", S("v2-frames-walk.mp4"), 21.0, 5.5, False, "STEEL BUILDER", ["STRENGTH,", "~BUILT PRECISELY."], "نبني القوة بدقة."),
]


def build():
    segs, t, hits = [], 0.0, []
    for name, src, ss, dur, land, eb, lines, ar in PLAN:
        if eb and not eb.startswith("STEEL"):
            hits.append(t)
        ov = reels.layer(name, eb, lines, ar, size=110) if lines else reels.layer(name)
        segs.append(reels.segment(name, src, ss, dur, ov, landscape=land, title_in=0.15 if lines else 0.0))
        t += dur
    end_at = t
    segs.append(reels.endcard())
    silent = reels.concat("_process-silent", segs)            # concat (+ loudnorm of site audio)
    total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                           "-of", "csv=p=0", silent]))
    wav = os.path.join(reels.TMP, "score.wav")
    music.track(total, hits, wav, end_at=end_at)
    out = os.path.join(reels.OUT, "reel-19-process-ground-to-steel.mp4")
    # score only: site audio (phone-mic wind noise) is dropped; clean gain + transparent peak limiter, no loudnorm pumping
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", wav, "-filter_complex",
                    "[1:a]atrim=0:%.3f,volume=1.6,alimiter=limit=0.89:attack=5:release=80:level=false[a]" % total,
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", out], check=True)
    os.remove(silent)
    print("hits", [round(h, 2) for h in hits], "end", round(end_at, 2), "total", round(total, 2))
    return out


def cover():
    im = posts.base(S("16.jpg"), (1080, 1920), (0.45, 0.5), scrim=0.95, start=0.3, top=0.5)
    posts.headline(im, "GROUND TO STEEL", ["FOUR STEPS.", "~ONE TEAM."], "الحفر · الورشة · التصنيع · التركيب", 1560, size=116, ar_size=46)
    watermark(im, w=190, pos="tr", margin=64, y=310)
    save(im, os.path.join(reels.OUT, "covers", "reel-19-cover.jpg"))


if __name__ == "__main__":
    build(); cover(); print("batch9 done")
