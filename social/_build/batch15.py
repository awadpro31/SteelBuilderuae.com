"""Batch 15: Royal Steel site reel — aerial over the steel stock and erected columns, crane setup,
rafter lift (phone clips vidstab-stabilised: see *-stab files), cinematic push on the lift photo,
120 BPM beat-synced cut with the music2 score."""
import os, subprocess
from brand import *
import reels, cine, music2

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
OUT = os.path.join(os.path.dirname(HERE), "batch-15")
reels.OUT = os.path.join(OUT, "reels")
cine.SHOTS = os.path.join(OUT, "cinematic-shots")
S = lambda f: os.path.join(SRC, f)
B = music2.BEAT

SHOT = ("b15-beam-lift", S("21.jpg"), (0.50, 0.46, 1.02, 0), (0.50, 0.40, 1.22, 0), False, False)

PLAN = [  # name, src, start, beats, landscape, title_in, eyebrow, lines, arabic
    ("r1", "v15-rs-aerial.mp4", 0.3, 4, True, 0.1, "ROYAL STEEL PROJECT", ["STEEL", "~ON SITE."], "موقع رويال ستيل"),
    ("r2", "v15-rs-aerial.mp4", 3.9, 12, True, 3.2, "ERECTION", ["COLUMNS", "~STANDING."], "تركيب الأعمدة"),
    ("r3", "v15-rs-stock-pan-stab.mp4", 5.1, 4, False, 0.1, None, None, None),
    ("r4", "v15-rs-crane-walk-stab.mp4", 9.0, 8, False, 0.1, "LIFTING", ["RAFTERS", "~IN THE AIR."], "رفع الجسور بالكرين"),
    ("r5", "shot:b15-beam-lift", 0.25, 8, False, 0.1, "STEEL BUILDER", ["BEAMS", "~INTO PLACE."], "رفع الجسور لمكانها"),
]


def build():
    segs, t, cuts, starts = [], 0.0, [], {}
    for name, src, ss, beats, land, tin, eb, lines, ar in PLAN:
        src = os.path.join(cine.SHOTS, src[5:] + ".mp4") if src.startswith("shot:") else S(src)
        dur = beats * B
        ov = reels.layer(name, eb, lines, ar, size=116) if lines else reels.layer(name)
        segs.append(reels.segment(name, src, ss, dur, ov, landscape=land, fade_in=0.08, title_in=tin))
        if t > 0: cuts.append(t)
        starts[name] = t; t += dur
    end = t
    segs.append(reels.endcard(8 * B))
    silent = reels.concat("_rs-silent", segs)
    total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", silent]))
    sec = {"groove": starts["r2"], "layer2": starts["r3"], "peak": starts["r4"], "final": starts["r5"], "end": end}
    wav = os.path.join(reels.TMP, "score.wav")
    music2.track(wav, total, sec, cuts)
    out = os.path.join(reels.OUT, "reel-24-royal-steel-site.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", wav, "-filter_complex",
                    "[1:a]atrim=0:%.3f,volume=1.6,alimiter=limit=0.89:attack=5:release=80:level=false[a]" % total,
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    os.remove(silent)
    reels.cover_image("reel-24", S("21.jpg"), "ROYAL STEEL PROJECT", ["BEAMS", "~INTO PLACE."], "موقع رويال ستيل", (0.5, 0.42))
    print("sections", sec, "cuts", cuts, "total", round(total, 2))


if __name__ == "__main__":
    import sys
    steps = sys.argv[1:] or ["shots", "reel"]
    if "shots" in steps: cine.render(SHOT)
    if "reel" in steps: build()
