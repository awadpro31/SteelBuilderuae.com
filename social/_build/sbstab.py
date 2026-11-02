"""Window stabiliser + upscaler for low-res phone footage (OpenCV feature tracking).

Per window: track corners frame to frame (LK optical flow) -> similarity transform (dx, dy, da) ->
cumulative camera path -> Savitzky-Golay smoothing (keeps intentional pans, drops hand shake) ->
one combined warp per frame: shake correction + border-hiding zoom + upscale to the output size, a single
Lanczos resample (vidstab + crop + scale used to resample three times and softened 480p sources badly).
Decoding applies a temporal denoise to clean messaging-app compression; encoding adds a light CAS sharpen."""
import subprocess
import numpy as np
import cv2


def _frames(src, ss, dur, pre="hqdn3d=3:2:6:5"):
    probe = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries",
                                     "stream=width,height", "-of", "csv=p=0", src]).decode().split(",")
    w, h = int(probe[0]), int(probe[1])
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(dur), "-i", src,
                                   "-vf", f"{pre},fps=30", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"])
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)


def _motion(frames):
    out, prev = [], cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
    for f in frames[1:]:
        cur = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        pts = cv2.goodFeaturesToTrack(prev, maxCorners=400, qualityLevel=0.01, minDistance=12, blockSize=3)
        m = None
        if pts is not None and len(pts) >= 8:
            nxt, st, _ = cv2.calcOpticalFlowPyrLK(prev, cur, pts, None)
            ok = st.ravel() == 1
            if ok.sum() >= 8:
                m, _ = cv2.estimateAffinePartial2D(pts[ok], nxt[ok], method=cv2.RANSAC, ransacReprojThreshold=2.0)
        if m is None:
            out.append((0.0, 0.0, 0.0))
        else:
            out.append((m[0, 2], m[1, 2], np.arctan2(m[1, 0], m[0, 0])))
        prev = cur
    return np.array(out)


def _smooth(path, radius):
    """Local quadratic fit (Savitzky-Golay): follows pans and tilts without lag, removes hand shake."""
    from scipy.signal import savgol_filter
    k = min(2 * radius + 1, len(path) - (1 - len(path) % 2))
    return savgol_filter(path, k, 2, axis=0, mode="interp") if k > 3 else path.copy()


def _need(corr, w, h):
    """Zoom that keeps every corrected frame free of borders (translation + rotation of the corners)."""
    return 1 + 2 * max(np.abs(corr[:, 0]).max() / w, np.abs(corr[:, 1]).max() / h) \
             + np.abs(corr[:, 2]).max() * np.hypot(w, h) / min(w, h)


def stabilise(src, ss, dur, out, size=(1080, 1920), radius=45, max_zoom=1.10, sharpen=0.4):
    """Write a stabilised, upscaled, silent clip of src[ss:ss+dur] to out.
    Uses the strongest smoothing (largest radius) whose correction fits inside max_zoom.
    Returns (radius used, zoom)."""
    frames = _frames(src, ss, dur)
    h, w = frames.shape[1:3]
    mot = _motion(frames)
    path = np.vstack([[0, 0, 0], np.cumsum(mot, 0)])
    r = min(radius, len(path) // 2)
    while True:
        corr = _smooth(path, r) - path                                   # per-frame correction (dx, dy, da)
        need = _need(corr, w, h)
        if need <= max_zoom or r <= 3:
            break
        r = max(3, int(r * 0.7))
    if need > max_zoom:                                                  # still too big: scale the correction down
        corr *= (max_zoom - 1) / (need - 1)
        need = max_zoom
    zoom = max(1.02, need * 1.005)
    W, H = size
    s = max(W / w, H / h) * zoom
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", "30", "-i", "-", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                            "-vf", f"cas={sharpen}", "-map", "0:v", "-map", "1:a", "-shortest",
                            "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", out], stdin=subprocess.PIPE)
    cx, cy = w / 2, h / 2
    for f, (dx, dy, da) in zip(frames, corr):
        # correction about the frame centre, then scale about the centre into the output canvas
        c, sn = np.cos(da), np.sin(da)
        A = np.array([[c, -sn, dx + cx - c * cx + sn * cy], [sn, c, dy + cy - sn * cx - c * cy]])
        S = np.array([[s, 0, W / 2 - s * cx], [0, s, H / 2 - s * cy]])
        M = S @ np.vstack([A, [0, 0, 1]])
        enc.stdin.write(cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE).tobytes())
    enc.stdin.close(); enc.wait()
    return r, round(zoom, 3)
