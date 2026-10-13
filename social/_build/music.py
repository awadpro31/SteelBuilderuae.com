"""Original, royalty-free soundtrack synthesised from scratch (no samples, no third-party audio).
v2 — clean mix: no saturation/clipping anywhere, soft-attack pads, sine bass, piano-like arpeggio,
gentle filtered drums, -3 dBFS peak headroom. (v1 used tanh soft-clip + square-ish bass = audible distortion.)"""
import numpy as np, wave
from scipy.signal import lfilter, butter

SR = 44100
BPM = 96
BEAT = 60 / BPM
BAR = 4 * BEAT
rng = np.random.default_rng(11)


def lp(x, fc, order=2):
    b, a = butter(order, fc / (SR / 2), "low"); return lfilter(b, a, x)


def hp(x, fc, order=2):
    b, a = butter(order, fc / (SR / 2), "high"); return lfilter(b, a, x)


def adsr(n, a, d, s, r):
    t = np.arange(n) / SR; dur = n / SR
    e = np.where(t < a, t / a, np.where(t < a + d, 1 - (1 - s) * (t - a) / d, s))
    return e * np.clip((dur - t) / r, 0, 1)


def tone(f, n, harmonics=((1, 1.0),)):
    t = np.arange(n) / SR
    return sum(g * np.sin(2 * np.pi * f * h * t) for h, g in harmonics)


# A minor: Am – F – C – G
CHORDS = [(220.00, 261.63, 329.63), (174.61, 220.00, 261.63), (261.63, 329.63, 392.00), (196.00, 246.94, 293.66)]
BASS = [55.0, 43.65, 65.41, 49.0]


def pad(chord, n):
    x = sum(tone(f, n, ((1, 1.0), (2, 0.25), (3, 0.08))) for f in chord) / 3
    x2 = sum(tone(f * 1.003, n, ((1, 1.0), (2, 0.2))) for f in chord) / 3   # slight detune = width
    return lp(x, 2200), lp(x2, 2200)


def piano(f, n):
    x = tone(f, n, ((1, 1.0), (2, 0.35), (3, 0.12), (4, 0.05)))
    return x * adsr(n, 0.004, 0.25, 0.25, 0.25) * np.exp(-np.arange(n) / SR * 2.2)


def kick(n=int(0.40 * SR)):
    t = np.arange(n) / SR
    f = 48 + 70 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def snare(n=int(0.22 * SR)):          # soft clap: band-limited noise, short
    t = np.arange(n) / SR
    noise = hp(lp(rng.normal(0, 1, n), 4500), 900)
    return noise * np.exp(-t * 22) * 0.6


def hat(n=int(0.05 * SR)):
    t = np.arange(n) / SR
    return lp(hp(rng.normal(0, 1, n), 7000), 11000) * np.exp(-t * 80) * 0.5


def swell(n):                          # smooth riser: filtered noise + rising sine, no harsh steps
    t = np.arange(n) / SR; p = t / t[-1]
    noise = lp(hp(rng.normal(0, 1, n), 300), 3500) * p ** 2.2 * 0.25
    sine = np.sin(2 * np.pi * np.cumsum(220 + 440 * p ** 2) / SR) * p ** 3 * 0.08
    return noise + sine


def hit(n=int(1.8 * SR)):              # cinematic hit kept above 55 Hz so phone speakers don't distort
    t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (60 + 30 * np.exp(-t * 8)) * t) * np.exp(-t * 3.0)
    air = lp(hp(rng.normal(0, 1, n), 200), 2500) * np.exp(-t * 6) * 0.25
    return boom * 0.7 + air


def echo(x, delay=0.27, fb=0.32, mix=0.28):
    d = int(delay * SR); y = x.copy()
    for k in range(1, 5):
        g = mix * fb ** (k - 1)
        y[d * k:] += x[:-d * k] * g if d * k < len(x) else 0
    return y


def track(duration, hits, out_path, end_at=None):
    n = int(duration * SR)
    L = np.zeros(n); R = np.zeros(n)
    end_at = end_at or duration
    def add(x, s, gl, gr=None):
        s = int(s); m = min(len(x), n - s)
        if m > 0:
            L[s:s + m] += x[:m] * gl; R[s:s + m] += x[:m] * (gl if gr is None else gr)
    bars = int(np.ceil(duration / BAR))
    for b in range(bars):
        t0 = b * BAR; m = int(BAR * SR) + int(0.6 * SR)
        ch = CHORDS[b % 4]
        pl, pr = pad(ch, m)
        e = adsr(m, 0.6, 0.5, 0.8, 0.7)
        add(pl * e, t0 * SR, 0.10, 0.0); add(pr * e, t0 * SR, 0.0, 0.10)
        if t0 >= BAR * 0.99 and t0 < end_at:          # arpeggio from bar 2
            arp = [ch[0] * 2, ch[1] * 2, ch[2] * 2, ch[1] * 2] * 2
            for k, f in enumerate(arp):
                tt = t0 + k * BEAT / 2
                if tt >= end_at: break
                x = piano(f, int(0.9 * SR))
                add(x, tt * SR, 0.07 if k % 2 else 0.05, 0.05 if k % 2 else 0.07)
        if t0 < end_at:                                 # bass: sustained sine root, two hits per bar
            for k in (0, 2.5):
                tt = t0 + k * BEAT
                if tt >= end_at: break
                bn = int(BEAT * 1.4 * SR)
                x = tone(BASS[b % 4], bn, ((1, 1.0), (2, 0.15))) * adsr(bn, 0.01, 0.2, 0.7, 0.15)
                add(lp(x, 400), tt * SR, 0.22)
    # drums: start after the intro bar, stop at the outro
    t = hits[1] if len(hits) > 1 else BAR
    K, Sn, H = kick(), snare(), hat()
    while t < end_at - 0.05:
        for k in range(8):
            tt = t + k * BEAT / 2
            if tt >= end_at - 0.05: break
            add(H, tt * SR, 0.10 if k % 2 else 0.06, 0.06 if k % 2 else 0.10)
            if k in (0, 4): add(K, tt * SR, 0.45)
            if k in (2, 6): add(Sn, tt * SR, 0.20)
        t += BAR
    # swells into each chapter + clean hit on the cut
    for h in list(hits[1:]) + [end_at]:
        sn = int(1.4 * SR)
        add(swell(sn), h * SR - sn, 0.9, 0.9)
        add(hit(), h * SR, 0.55)
    L, R = echo(L), echo(R, delay=0.31)
    L, R = hp(L, 30), hp(R, 30)                        # remove sub rumble
    fade = int(1.8 * SR)
    for ch in (L, R):
        ch[-fade:] *= np.linspace(1, 0, fade); ch[:int(0.4 * SR)] *= np.linspace(0, 1, int(0.4 * SR))
    mix = np.stack([L, R], 1)
    mix *= 10 ** (-3 / 20) / np.max(np.abs(mix))       # peak at -3 dBFS, linear (no clipping)
    with wave.open(out_path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    return out_path


if __name__ == "__main__":
    track(20, [0.0, 5.0, 10.0, 15.0], "/tmp/music-test.wav", end_at=17)
