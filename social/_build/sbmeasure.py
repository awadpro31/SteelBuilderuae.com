"""Per-second camera motion and hand-shake of a clip, to pick steady windows before cutting.
motion = mean frame-to-frame shift; shake = shift minus its 0.5 s moving average (px at 480-wide)."""
import sys, subprocess
import numpy as np


def measure(f):
    w, h = 240, 426
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", f, "-vf", f"fps=30,scale={w}:{h},format=gray",
                                   "-f", "rawvideo", "-"])
    fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(float)
    win = np.hanning(h)[:, None] * np.hanning(w)[None, :]
    d = []
    for a, b in zip(fr[:-1], fr[1:]):
        A = np.fft.fft2((a - a.mean()) * win); B = np.fft.fft2((b - b.mean()) * win)
        r = np.fft.ifft2(A * np.conj(B) / (abs(A * np.conj(B)) + 1e-9)).real
        dy, dx = np.unravel_index(r.argmax(), r.shape)
        d.append((dx - w if dx > w / 2 else dx, dy - h if dy > h / 2 else dy))
    d = np.array(d, float) * 2
    ker = np.ones(15) / 15
    sm = np.stack([np.convolve(d[:, i], ker, mode="same") for i in (0, 1)], 1)
    motion, shake = np.hypot(*d.T), np.hypot(*(d - sm).T)
    for i in range(0, len(d), 30):
        print(f"{i // 30:3d}s  motion {motion[i:i + 30].mean():5.1f}  shake {shake[i:i + 30].mean():4.1f}")


if __name__ == "__main__":
    measure(sys.argv[1])
