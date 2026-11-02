"""Batch 16: Saih Shuaib project — two reels, no music (silent track; sound is added in-app if wanted).
A: foundations (formwork, rebar, pad pour). B: steel erection (crane lifts, frames, bolting at height).
Phone clips: steady windows only, stabilised + upscaled by sbstab (v16w-* files); the night clip was left out
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

SHOT = ("b16-pad-pour", S("22.jpg"), (0.50, 0.58, 1.04, 0), (0.50, 0.50, 1.24, 0), False, False)
BOLT = S("v16-bolting-push.mp4")      # landscape photo 23.jpg -> slow push clip

PROJECT = "SAIH SHUAIB PROJECT"
# v2: only windows with low measured hand-shake (walking shots dropped), each stabilised and upscaled in one
# resample by sbstab (the first version's vidstab + crop + rescale chain left shake and softened the 480p clips)
WINDOWS = {  # clip name: (source, start, dur)
    "w-forms-worker": (S("v16-ss-3.mov"), 8.0, 3.6),
    "w-forms-row": (S("v16-ss-1.mov"), 42.0, 3.6),
    "w-pour": (S("v16-ss-2.mov"), 0.3, 3.7),
    "w-manlift": (S("v16-ss-4.mov"), 0.0, 3.1),
    "w-crane-lift": (S("v16-ss-4.mov"), 3.0, 5.1),
    "w-frames": (S("v16-ss-6.mov"), 4.0, 4.1),
}
CLIP = lambda k: os.path.join(SRC, "v16w-" + k + ".mp4")

REELS = {
    "reel-25-saih-shuaib-foundations": [  # name, src, start, dur, landscape, eyebrow, lines, arabic
        ("a1", CLIP("w-forms-worker"), 0.0, 3.5, False, PROJECT, ["FOUNDATIONS", "~TAKING SHAPE."], "مشروع سيح شعيب — الأساسات"),
        ("a2", CLIP("w-forms-row"), 0.0, 3.5, False, None, None, None),
        ("a3", CLIP("w-pour"), 0.0, 3.6, False, "CONCRETE", ["PADS", "~POURED."], "صبّ القواعد"),
        ("a4", "shot", 0.25, 4.5, False, "STEEL BUILDER", ["BUILT FROM", "~THE GROUND UP."], "نبني من الأساس"),
    ],
    "reel-26-saih-shuaib-steel-erection": [
        ("b1", CLIP("w-manlift"), 0.0, 3.0, False, PROJECT, ["STEEL", "~ERECTION."], "مشروع سيح شعيب — تركيب الهيكل"),
        ("b2", CLIP("w-crane-lift"), 0.0, 5.0, False, None, None, None),
        ("b3", CLIP("w-frames"), 0.0, 4.0, False, "FRAMES", ["RAFTERS", "~IN PLACE."], "الجسور في مكانها"),
        ("b4", BOLT, 0.2, 4.5, True, "STEEL BUILDER", ["BOLTED", "~AT HEIGHT."], "تربيط على ارتفاع"),
    ],
}


def prep_windows():
    import sbstab
    for k, (src, ss, dur) in WINDOWS.items():
        print(k, sbstab.stabilise(src, ss, dur, CLIP(k), sharpen=0.3))


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
    steps = sys.argv[1:] or ["prep", "windows", "reels", "covers"]
    if "prep" in steps: prep()
    if "windows" in steps: prep_windows()
    if "reels" in steps:
        for k, p in REELS.items(): print(build(k, p))
    if "covers" in steps: covers()
