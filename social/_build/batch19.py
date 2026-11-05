"""Batch 19: ICAD project — one long, silent reel organised in numbered chapters
(structure -> columns -> rafters -> purlins -> the full frame).
Sources: two smooth AI camera moves made from our site photos (v19-icad-ai-*), the real handheld walk
(steady window only, stabilised + upscaled by sbstab) and the two site photos as slow push / slide clips."""
import os, subprocess
from brand import *
import reels, sbstab

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
OUT = os.path.join(os.path.dirname(HERE), "batch-19")
reels.OUT = os.path.join(OUT, "reels")
S = lambda f: os.path.join(SRC, f)

AI_ERECT, AI_DOLLY = S("v19-icad-ai-erection.mp4"), S("v19-icad-ai-dolly.mp4")
WALK = S("v19w-icad-walk.mp4")                         # stabilised 2.0-4.9 s of the handheld walk
PORTAL, PURLINS = S("v19-portal-push.mp4"), S("v19-purlins-slide.mp4")
PROJECT = "ICAD PROJECT · ABU DHABI"

PLAN = [  # name, src, start, dur, landscape, eyebrow, lines, arabic
    ("i1", AI_DOLLY, 0.0, 3.2, False, PROJECT, ["STEEL FRAMES,", "~STANDING TALL."], "مشروع آيكاد — أبوظبي"),
    ("i2", PORTAL, 0.2, 4.2, True, "01 · STRUCTURE", ["PORTAL", "~FRAMES."], "الإطارات الرئيسية"),
    ("i3", AI_DOLLY, 5.0, 4.0, False, "02 · COLUMNS", ["ALIGNED", "~TO THE GRID."], "الأعمدة على المحاور"),
    ("i4", WALK, 0.0, 2.8, True, None, None, None),
    ("i5", AI_ERECT, 2.2, 3.6, False, "03 · RAFTERS", ["BOLTED", "~AT HEIGHT."], "تربيط الجسور على ارتفاع"),
    ("i6", AI_ERECT, 5.0, 1.9, False, None, None, None),
    ("i7", PURLINS, 0.2, 4.2, True, "04 · PURLINS", ["ROOF", "~FRAMING."], "تركيب المدادات"),
    ("i8", AI_ERECT, 7.05, 2.9, False, "STEEL BUILDER", ["ONE FRAME.", "~ONE TEAM."], "مشروع آيكاد — ستيل بيلدر"),
]


def prep():
    run = lambda *a: subprocess.run(["ffmpeg", "-y", "-v", "error", *a], check=True)
    # real walk: the file reports 90000 fps, so normalise to 30 fps first, then stabilise the steady window
    walk30 = os.path.join(reels.TMP, "walk30.mp4")
    run("-i", S("v19-icad-walk.mov"), "-vf", "fps=30", "-c:v", "libx264", "-crf", "12", "-an", walk30)
    print("walk", sbstab.stabilise(walk30, 2.0, 2.9, WALK, size=(1080, 612), sharpen=0.3))
    # photos -> slow camera moves (landscape 1080x486, used over their own blur)
    for src, out, z, x in [(S("24.jpg"), PORTAL, "1+0.10*on/150", "iw/2-(iw/zoom/2)"),
                           (S("25.jpg"), PURLINS, "1.12", "(iw-iw/zoom)*on/150")]:
        run("-i", src, "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex",
            f"[0:v]scale=3200:1440,zoompan=z='{z}':x='{x}':y='ih/2-(ih/zoom/2)':d=150:s=1080x486:fps=30,"
            "eq=contrast=1.05:saturation=1.06[v]", "-map", "[v]", "-map", "1:a", "-t", "5",
            "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "-c:a", "aac", out)


def build():
    segs = []
    for n, src, ss, dur, land, eb, lines, ar in PLAN:
        ov = reels.layer(n, eb, lines, ar, size=112) if lines else reels.layer(n)
        segs.append(reels.segment(n, src, ss, dur, ov, landscape=land, fade_in=0.12, title_in=0.2))
    segs.append(reels.endcard(4.0))
    tmp = reels.concat("_icad", segs)
    out = os.path.join(reels.OUT, "reel-28-icad-project.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "64k", "-shortest",
                    "-movflags", "+faststart", out], check=True)
    os.remove(tmp)
    frame = os.path.join(reels.TMP, "icad-frame.png")                  # vertical AI frame: 1.5x, not the 2.7x photo blow-up
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "0.6", "-i", AI_DOLLY, "-frames:v", "1", frame], check=True)
    reels.cover_image("reel-28", frame, PROJECT, ["STEEL FRAMES,", "~STANDING TALL."], "مشروع آيكاد — أبوظبي", (0.5, 0.5))
    return out


if __name__ == "__main__":
    import sys
    steps = sys.argv[1:] or ["prep", "reel"]
    if "prep" in steps: prep()
    if "reel" in steps: print(build())
    if steps == ["cover"]:
        frame = os.path.join(reels.TMP, "icad-frame.png")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "0.6", "-i", AI_DOLLY, "-frames:v", "1", frame], check=True)
        reels.cover_image("reel-28", frame, PROJECT, ["STEEL FRAMES,", "~STANDING TALL."], "مشروع آيكاد — أبوظبي", (0.5, 0.5))
