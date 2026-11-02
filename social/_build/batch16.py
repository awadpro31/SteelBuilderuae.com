"""Batch 16: Saih Shuaib project — two reels, no music (silent track; sound is added in-app if wanted).
A: foundations (formwork, rebar, pad pour). B: steel erection (crane lifts, frames, bolting at height).
Phone clips are vidstab-stabilised (*-stab files) and cut to their steady windows; the night clip was left out
(camera date/GPS stamp burnt in). Frames showing third-party names (container line, crane hire) are avoided."""
import os, subprocess
from brand import *
import reels, cine

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
OUT = os.path.join(os.path.dirname(HERE), "batch-16")
reels.OUT = os.path.join(OUT, "reels")
cine.SHOTS = os.path.join(OUT, "cinematic-shots")
S = lambda f: os.path.join(SRC, f)
V = lambda i: S(f"v16-ss-{i}-stab.mp4")

SHOT = ("b16-pad-pour", S("22.jpg"), (0.50, 0.58, 1.04, 0), (0.50, 0.50, 1.24, 0), False, False)
BOLT = S("v16-bolting-push.mp4")      # landscape photo 23.jpg -> slow push clip

PROJECT = "SAIH SHUAIB PROJECT"
REELS = {
    "reel-25-saih-shuaib-foundations": [  # name, src, start, dur, landscape, eyebrow, lines, arabic
        ("a1", V(3), 0.5, 4.0, False, PROJECT, ["FOUNDATIONS", "~TAKING SHAPE."], "مشروع سيح شعيب — الأساسات"),
        ("a2", V(1), 11.0, 3.0, False, None, None, None),
        ("a3", V(1), 42.3, 3.5, False, None, None, None),
        ("a4", V(2), 0.3, 3.5, False, "CONCRETE", ["PADS", "~POURED."], "صبّ القواعد"),
        ("a5", "shot", 0.25, 4.0, False, "STEEL BUILDER", ["BUILT FROM", "~THE GROUND UP."], "نبني من الأساس"),
    ],
    "reel-26-saih-shuaib-steel-erection": [
        ("b1", V(4), 0.0, 2.0, False, PROJECT, ["STEEL", "~ERECTION."], "مشروع سيح شعيب — تركيب الهيكل"),
        ("b2", V(4), 11.8, 4.5, False, None, None, None),
        ("b3", V(6), 3.8, 3.5, False, "FRAMES", ["RAFTERS", "~IN PLACE."], "الجسور في مكانها"),
        ("b5", V(6), 14.8, 1.7, False, None, None, None),
        ("b6", BOLT, 0.2, 4.0, True, "STEEL BUILDER", ["BOLTED", "~AT HEIGHT."], "تربيط على ارتفاع"),
    ],
}


def prep():
    cine.render(SHOT)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", S("23.jpg"), "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                    "-filter_complex", "[0:v]scale=3198:1798,zoompan=z='1+0.08*on/150':x='iw/2-(iw/zoom/2)':"
                    "y='ih/2-(ih/zoom/2)':d=150:s=1080x608:fps=30,eq=contrast=1.05:saturation=1.06[v]",
                    "-map", "[v]", "-map", "1:a", "-t", "5", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", BOLT], check=True)


def build(name, plan):
    segs = []
    for n, src, ss, dur, land, eb, lines, ar in plan:
        src = os.path.join(cine.SHOTS, SHOT[0] + ".mp4") if src == "shot" else src
        ov = reels.layer(n, eb, lines, ar, size=116) if lines else reels.layer(n)
        segs.append(reels.segment(n, src, ss, dur, ov, landscape=land, fade_in=0.08, title_in=0.15))
    segs.append(reels.endcard(3.5))
    tmp = reels.concat("_" + name, segs)
    out = os.path.join(reels.OUT, name + ".mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "64k", "-shortest",
                    "-movflags", "+faststart", out], check=True)
    os.remove(tmp)
    return out


def covers():
    reels.cover_image("reel-25", S("22.jpg"), PROJECT, ["FOUNDATIONS", "~TAKING SHAPE."], "مشروع سيح شعيب", (0.5, 0.55))
    reels.cover_image("reel-26", S("23.jpg"), PROJECT, ["STEEL", "~ERECTION."], "مشروع سيح شعيب", (0.62, 0.45))


if __name__ == "__main__":
    import sys
    steps = sys.argv[1:] or ["prep", "reels", "covers"]
    if "prep" in steps: prep()
    if "reels" in steps:
        for k, p in REELS.items(): print(build(k, p))
    if "covers" in steps: covers()
