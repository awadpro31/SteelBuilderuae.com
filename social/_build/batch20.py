"""Batch 20: KEZAD rafter lift — one 480p phone clip prepared for Instagram.
The fast opening whip-pan (0-2.8 s) and the last half-second shake are trimmed; the 10 s lift is stabilised
and upscaled in a single resample by sbstab (with compression denoise + CAS sharpen), titled in the house
style, and closed with the end card. Silent track (site audio left out; sound is added in-app if wanted)."""
import os, subprocess
from brand import *
import reels, sbstab

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source", "v20-kezad-lift.mov")
CLIP = os.path.join(HERE, "source", "v20w-kezad-lift.mp4")
OUT = os.path.join(os.path.dirname(HERE), "batch-20")
reels.OUT = os.path.join(OUT, "reels")


def build():
    norm = os.path.join(reels.TMP, "k30.mp4")                            # odd timebase -> clean 30 fps first
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", SRC, "-vf", "fps=30", "-c:v", "libx264", "-crf", "12",
                    "-an", norm], check=True)
    print("stab", sbstab.stabilise(norm, 2.8, 10.0, CLIP, sharpen=0.35))
    reels.GRADE = "eq=contrast=1.08:saturation=1.12:gamma=0.98,unsharp=3:3:0.35"   # livelier than the house grade: blue sky, orange lifts
    ov = reels.layer("k1", "KEZAD PROJECT · ABU DHABI", ["RAFTERS", "~INTO PLACE."], "رفع الجسور — مشروع كيزاد", size=116)
    seg = reels.segment("k1", CLIP, 0.0, 10.0, ov, fade_in=0.2, title_in=0.4)
    tmp = reels.concat("_kezad", [seg, reels.endcard(3.5)])
    out = os.path.join(reels.OUT, "reel-29-kezad-rafter-lift.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "64k", "-shortest",
                    "-movflags", "+faststart", out], check=True)
    os.remove(tmp)
    frame = os.path.join(reels.TMP, "kezad-frame.png")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "6.0", "-i", CLIP, "-frames:v", "1", frame], check=True)
    reels.cover_image("reel-29", frame, "KEZAD PROJECT", ["RAFTERS", "~INTO PLACE."], "رفع الجسور — مشروع كيزاد", (0.5, 0.45))
    return out


if __name__ == "__main__":
    print(build())
