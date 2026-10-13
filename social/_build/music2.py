"""Original soundtrack v3 — Gulf/Middle-Eastern modern: maqsum darbuka groove, Karplus-Strong 'oud' pluck in
D Hijaz, sine bass, soft string pad. 120 BPM so every video cut lands on a beat. Synthesised from scratch,
no samples; clean (no saturation), peak -3 dBFS."""
import numpy as np, wave
from scipy.signal import lfilter, butter

SR = 44100
BPM = 120
BEAT = 60 / BPM          # 0.5 s
BAR = 4 * BEAT           # 2.0 s
rng = np.random.default_rng(7)

# D Hijaz: D Eb F# G A Bb C
N = {"D3": 146.83, "A2": 110.0, "D2": 73.42, "Bb2": 116.54, "C3": 130.81, "G2": 98.0,
     "D4": 293.66, "Eb4": 311.13, "F#4": 369.99, "G4": 392.0, "A4": 440.0, "Bb4": 466.16, "C5": 523.25, "D5": 587.33}


def lp(x, fc, o=2):
    b, a = butter(o, fc / (SR / 2), "low"); return lfilter(b, a, x)


def hp(x, fc, o=2):
    b, a = butter(o, fc / (SR / 2), "high"); return lfilter(b, a, x)


def pluck(f, dur=1.2, bright=0.5):
    """Karplus-Strong plucked string (oud-like)."""
    n = int(dur * SR); p = int(SR / f)
    buf = lp(rng.uniform(-1, 1, p), 2000 + 6000 * bright, 1)
    out = np.zeros(n); out[:p] = buf
    for i in range(p, n):
        out[i] = 0.996 * 0.5 * (out[i - p] + out[i - p - 1])
    body = lp(out, 3200)
    return body / (np.max(np.abs(body)) + 1e-9) * np.exp(-np.arange(n) / SR * 1.6)


def doum(n=int(0.5 * SR)):
    t = np.arange(n) / SR
    f = 75 + 60 * np.exp(-t * 35)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 8)


def tek(n=int(0.12 * SR)):
    t = np.arange(n) / SR
    ring = np.sin(2 * np.pi * 720 * t) * np.exp(-t * 60)
    slap = hp(lp(rng.normal(0, 1, n), 6000), 1500) * np.exp(-t * 90)
    return ring * 0.6 + slap * 0.5


def clap(n=int(0.25 * SR)):
    t = np.arange(n) / SR; x = np.zeros(n)
    for d in (0, 0.011, 0.023):        # three tight hands
        s = int(d * SR); x[s:] += hp(lp(rng.normal(0, 1, n - s), 5000), 900) * np.exp(-np.arange(n - s) / SR * 35)
    return x * 0.5


def strings(freqs, n):
    t = np.arange(n) / SR
    vib = 1 + 0.003 * np.sin(2 * np.pi * 5.2 * t)
    x = sum(np.sin(2 * np.pi * f * np.cumsum(vib) / SR) + 0.3 * np.sin(4 * np.pi * f * np.cumsum(vib) / SR) for f in freqs)
    a = np.minimum(1, t / 0.8); r = np.clip((n / SR - t) / 0.8, 0, 1)
    return lp(x / len(freqs), 2500) * a * r


def bass(f, n):
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.12 * np.sin(4 * np.pi * f * t)
    return lp(x, 300) * np.minimum(1, t / 0.01) * np.exp(-t * 1.5)


def swell(n):
    t = np.arange(n) / SR; p = t / t[-1]
    lo = lp(hp(rng.normal(0, 1, n), 400), 1500); hi = lp(hp(rng.normal(0, 1, n), 400), 6000)
    return (lo * (1 - p) + hi * p) * p ** 2.5 * 0.22          # crossfade dark→bright = opening filter


def boom(n=int(1.6 * SR)):
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * (62 + 25 * np.exp(-t * 9)) * t) * np.exp(-t * 3.2)


MOTIF = [("D4", 0, 0.5), ("Eb4", 0.5, 0.5), ("F#4", 1, 0.5), ("G4", 1.5, 1.0), ("A4", 2.5, 0.5), ("G4", 3, 0.5),
         ("F#4", 3.5, 0.5), ("Eb4", 4, 0.5), ("D4", 4.5, 1.5)]                       # in beats, spans 2 bars
MOTIF_HI = [("A4", 0, 0.5), ("Bb4", 0.5, 0.5), ("C5", 1, 0.5), ("D5", 1.5, 1.5), ("C5", 3, 0.5), ("Bb4", 3.5, 0.5),
            ("A4", 4, 0.5), ("G4", 4.5, 0.5), ("F#4", 5, 1.0)]
PAD = [("D3", "A2"), ("Bb2", "D3"), ("C3", "G2"), ("D3", "A2")]                       # one per bar
BASS = ["D2", "Bb2", "C3", "D2"]


def track(out_path, total, sec, accents):
    """sec: dict with groove, layer2, peak, final, end (seconds, on bar lines); accents: cut times (on beats)."""
    n = int(total * SR); L = np.zeros(n); R = np.zeros(n)
    def add(x, t, gl, gr=None):
        s = int(round(t * SR)); m = min(len(x), n - s)
        if s >= 0 and m > 0:
            L[s:s + m] += x[:m] * gl; R[s:s + m] += x[:m] * (gl if gr is None else gr)
    end = sec["end"]
    cache = {}
    def P(note, dur, bright=0.5):
        k = (note, round(dur, 2), bright)
        if k not in cache: cache[k] = pluck(N[note], dur, bright)
        return cache[k]
    # pad + bass per bar
    nb = int(np.ceil(total / BAR))
    for b in range(nb):
        t0 = b * BAR
        if t0 >= end + BAR: break
        ch = PAD[b % 4]
        g = 0.05 if t0 < sec["groove"] else (0.07 if t0 < sec["peak"] else 0.09)
        st = strings([N[c] * 2 for c in ch], int(BAR * SR * 1.25))
        add(st, t0, g, g * 0.85)
        if sec["groove"] <= t0 < end:
            for k in (0, 1.5, 2.5):
                add(bass(N[BASS[b % 4]], int(BEAT * 1.6 * SR)), t0 + k * BEAT, 0.28)
    # oud motif: every 2 bars; octave-up answer in the peak section
    t = 0.0
    while t < end:
        motif = MOTIF_HI if (sec["peak"] <= t < end and int((t - sec["peak"]) / (2 * BAR)) % 2 == 1) else MOTIF
        for note, b, d in motif:
            tt = t + b * BEAT
            if tt >= end: break
            add(P(note, d * BEAT + 0.6, 0.55), tt, 0.20, 0.16)
        t += 2 * BAR
    # darbuka maqsum: D T . T D . T .   (eighths) — light in intro, full from groove
    D, T, C = doum(), tek(), clap()
    t = 0.0
    while t < end:
        intro = t < sec["groove"]
        for k, hitp in enumerate("DT.TD.T."):
            tt = t + k * BEAT / 2
            if tt >= end: break
            if hitp == "D": add(D, tt, 0.30 if intro else 0.55)
            if hitp == "T" and not intro: add(T, tt, 0.16, 0.12)
            if hitp == "T" and intro and k == 1: add(T, tt, 0.08)
            if t >= sec["layer2"] and k in (2, 6): add(C, tt, 0.16)               # claps on 2 & 4
            if t >= sec["peak"] and hitp == ".": add(T, tt, 0.07, 0.10)            # ghost teks fill
        t += BAR
    # sync points: swell into each section, boom on the downbeat; tek accent on every cut
    for s_t in (sec["groove"], sec["layer2"], sec["peak"], sec["final"], end):
        sw = int(1.5 * SR); add(swell(sw), s_t - 1.5, 1.0, 1.0); add(boom(), s_t, 0.45)
    for a in accents:
        add(T, a, 0.14)
    # ending: open D5 chord ring-out over the end card
    for i, nt in enumerate(("D4", "A4", "D5")):
        add(P(nt, 3.0, 0.4), end + i * 0.06, 0.18)
    L, R = hp(L, 35), hp(R, 35)
    fade = int(1.6 * SR)
    for ch in (L, R):
        ch[-fade:] *= np.linspace(1, 0, fade); ch[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))
    mix = np.stack([L, R], 1); mix *= 10 ** (-3 / 20) / np.max(np.abs(mix))
    with wave.open(out_path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    return out_path
