"""Batch 10: beat-synced process reel (120 BPM) — every cut on a beat, every chapter on a bar line,
with the new maqsum/oud soundtrack (music2). Ground → workshop → fabrication → erection."""
import os, subprocess
from brand import *
import reels, music2

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
OUT = os.path.join(os.path.dirname(HERE), "batch-10")
reels.OUT = os.path.join(OUT, "reels")
S = lambda f: os.path.join(SRC, f)
B = music2.BEAT  # 0.5 s

# durations are whole beats; chapter starts fall on bar lines (multiples of 2.0 s)
PLAN = [  # name, src, start, beats, landscape, eyebrow, lines, arabic
    ("d1", S("v-excavation.mp4"), 0.0, 6, False, "01 · EXCAVATION", ["IT STARTS", "~BELOW GROUND."], "الحفر — البداية من تحت الأرض"),
    ("d2", S("v2-excavator.mp4"), 0.0, 3, True, None, None, None),
    ("d3", S("v9-grade-beams.mov"), 2.0, 3, False, None, None, None),
    ("w1", S("v8-yard-clean.mp4"), 0.5, 8, True, "02 · WORKSHOP", ["OUR", "~WORKSHOP."], "الورشة — مصفح"),
    ("f1", S("v2-workshop.mp4"), 5.0, 8, False, "03 · FABRICATION", ["CUT. FIT.", "~WELD."], "التصنيع — قص وتجميع ولحام"),
    ("f2", S("v8-yard-clean.mp4"), 26.0, 4, True, None, None, None),
    ("e1", S("v9-rafters-prep.mov"), 0.0, 6, False, "04 · ERECTION", ["STEEL", "~GOES UP."], "تركيب الحديد"),
    ("e2", S("v-lift.mp4"), 4.0, 8, False, None, None, None),                 # ends 8.0 s, before the hand at 9.7 s
    ("e3", S("v2-frames-walk.mp4"), 21.0, 10, False, "STEEL BUILDER", ["STRENGTH,", "~BUILT PRECISELY."], "نبني القوة بدقة."),
]
END_BEATS = 8   # end card = 2 bars


def build():
    segs, t, cuts, starts = [], 0.0, [], {}
    for name, src, ss, beats, land, eb, lines, ar in PLAN:
        dur = beats * B
        ov = reels.layer(name, eb, lines, ar, size=110) if lines else reels.layer(name)
        segs.append(reels.segment(name, src, ss, dur, ov, landscape=land, fade_in=0.08, title_in=0.1))
        if t > 0: cuts.append(t)
        starts[name] = t; t += dur
    end = t
    segs.append(reels.endcard(END_BEATS * B))
    silent = reels.concat("_beat-silent", segs)
    total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", silent]))
    sec = {"groove": starts["w1"], "layer2": starts["f1"], "peak": starts["e1"], "final": starts["e3"], "end": end}
    wav = os.path.join(reels.TMP, "score2.wav")
    music2.track(wav, total, sec, cuts)
    out = os.path.join(reels.OUT, "reel-20-ground-to-steel-beat.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", wav, "-filter_complex",
                    "[1:a]atrim=0:%.3f,volume=1.6,alimiter=limit=0.89:attack=5:release=80:level=false[a]" % total,
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    os.remove(silent)
    print("sections", sec, "cuts", cuts, "total", round(total, 2))
    return out


if __name__ == "__main__":
    build(); print("batch10 done")
