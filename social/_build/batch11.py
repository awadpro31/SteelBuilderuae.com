"""Batch 11: Dubai Industrial City pour — night pour → next-morning pads. Enhanced footage
(vidstab two-pass stabilisation, denoise, exposure/colour, sharpen — see *-stab files), cinematic shots from the 3 photos,
120 BPM beat-synced cut with the music2 score."""
import os, subprocess
from brand import *
import posts, reels, cine, music2

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
OUT = os.path.join(os.path.dirname(HERE), "batch-11")
reels.OUT = os.path.join(OUT, "reels")
cine.SHOTS = os.path.join(OUT, "cinematic-shots")
S = lambda f: os.path.join(SRC, f)
B = music2.BEAT

SHOTS = [("b11-pad-close", S("19.jpg"), (0.45, 0.62, 1.04, 0), (0.45, 0.54, 1.30, 0), False, False),
         ("b11-pads-row", S("17.jpg"), (0.50, 0.64, 1.04, 0), (0.50, 0.50, 1.32, 0), True, False),
         ("b11-pads-forms", S("18.jpg"), (0.50, 0.66, 1.12, 0), (0.50, 0.52, 1.24, 0), False, False)]

PLAN = [  # name, src, start, beats, landscape, eyebrow, lines, arabic
    # v2: vidstab-stabilised sources; only the steady windows of the night clip (3-11 s is whip pans);
    # the handheld walk clip is replaced by a locked-off cinematic shot.
    ("n1", S("v11-night-stab.mp4"), 11.0, 10, True, "DUBAI INDUSTRIAL CITY", ["NIGHT", "~POUR."], "صبّة ليلية — دبي الصناعية"),
    ("n2", S("v11-night-spray-slow.mp4"), 0.0, 6, True, None, None, None),
    ("m1", "shot:b11-pads-forms", 0.25, 8, False, "THE NEXT MORNING", ["PADS", "~POURED."], "الصبح — القواعد مصبوبة"),
    ("m2", "shot:b11-pad-close", 0.25, 8, False, None, None, None),
    ("m3", S("v11-pads-day-stab.mp4"), 0.3, 10, False, "STEEL BUILDER", ["READY", "~FOR STEEL."], "جاهزة لتركيب الحديد"),
    ("m4", "shot:b11-pads-row", 0.25, 6, False, None, None, None),
]


def build():
    segs, t, cuts, starts = [], 0.0, [], {}
    for name, src, ss, beats, land, eb, lines, ar in PLAN:
        if src.startswith("shot:"):
            src = os.path.join(cine.SHOTS, src[5:] + ".mp4")
        dur = beats * B
        ov = reels.layer(name, eb, lines, ar, size=116) if lines else reels.layer(name)
        segs.append(reels.segment(name, src, ss, dur, ov, landscape=land, fade_in=0.08, title_in=0.1))
        if t > 0: cuts.append(t)
        starts[name] = t; t += dur
    end = t
    segs.append(reels.endcard(8 * B))
    silent = reels.concat("_pour-silent", segs)
    total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", silent]))
    sec = {"groove": starts["m1"], "layer2": starts["m2"], "peak": starts["m3"], "final": starts["m4"], "end": end}
    wav = os.path.join(reels.TMP, "score.wav")
    music2.track(wav, total, sec, cuts)
    out = os.path.join(reels.OUT, "reel-21-dic-night-pour.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", wav, "-filter_complex",
                    "[1:a]atrim=0:%.3f,volume=1.6,alimiter=limit=0.89:attack=5:release=80:level=false[a]" % total,
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    os.remove(silent)
    print("sections", sec, "cuts", cuts, "total", round(total, 2))


def covers_and_stills():
    im = posts.base(S("17.jpg"), (1080, 1920), (0.5, 0.55), scrim=0.95, start=0.3, top=0.5)
    posts.headline(im, "DUBAI INDUSTRIAL CITY", ["NIGHT", "~POUR."], "صبّة ليلية — دبي الصناعية", 1560, size=120, ar_size=52)
    watermark(im, w=190, pos="tr", margin=64, y=310)
    save(im, os.path.join(reels.OUT, "covers", "reel-21-cover.jpg"))
    posts.OUT = OUT
    posts.post("15-dic-pads.jpg", S("17.jpg"), "DUBAI INDUSTRIAL CITY", ["PADS", "~POURED."], "صب القواعد — دبي الصناعية", focus=(0.5, 0.6))
    im = posts.base(S("18.jpg"), posts.STORY, (0.5, 0.6), scrim=0.95, start=0.36, top=0.55)
    posts.headline(im, "SITE UPDATE", ["POURED", "~OVERNIGHT."], "صبّة ليلية — دبي الصناعية", posts.STORY[1] - 330, size=120)
    watermark(im, w=170, pos="tl", margin=64, y=210)
    save(im, os.path.join(OUT, "stories", "01-dic-pour.jpg"))


if __name__ == "__main__":
    import sys
    steps = sys.argv[1:] or ["shots", "reel", "stills"]
    if "shots" in steps:
        for s in SHOTS: cine.render(s)
    if "reel" in steps: build()
    if "stills" in steps: covers_and_stills()
    print("batch11 done")
