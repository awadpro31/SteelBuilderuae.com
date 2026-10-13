"""Original, royalty-free soundtrack synthesised from scratch (no samples, no third-party audio).
Cinematic-industrial: A-minor pad, pulsing bass, drums, risers into each chapter, impacts on cuts."""
import numpy as np, wave

SR = 44100
BPM = 100
BEAT = 60 / BPM
rng = np.random.default_rng(11)


def env(n, a=0.01, r=0.2):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4))
    rel = np.clip((n / SR - t) / max(r, 1e-4), 0, 1)
    return e * rel


def osc_saw(f, n, detune=0.0):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for d in (-detune, 0, detune):
        ph = (t * f * (1 + d)) % 1.0
        out += 2 * ph - 1
    return out / 3


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):  # one-pole, fine for short buffers
        acc = (1 - a) * v + a * acc; y[i] = acc
    return y


def lp_fast(x, cutoff, passes=2):
    for _ in range(passes):
        a = np.exp(-2 * np.pi * cutoff / SR)
        b = np.zeros_like(x); b[0] = x[0] * (1 - a)
        # vectorised IIR via cumulative trick on blocks
        from scipy.signal import lfilter
        x = lfilter([1 - a], [1, -a], x)
    return x


def kick(n=int(0.45 * SR)):
    t = np.arange(n) / SR
    f = 50 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7) * 0.95


def snare(n=int(0.3 * SR)):
    t = np.arange(n) / SR
    noise = rng.normal(0, 1, n)
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25)
    return (lp_fast(noise, 6000) * np.exp(-t * 16) * 0.55 + body * 0.45)


def hat(n=int(0.06 * SR)):
    t = np.arange(n) / SR
    noise = rng.normal(0, 1, n)
    hp = noise - lp_fast(noise, 7000)
    return hp * np.exp(-t * 70) * 0.22


def impact(n=int(2.2 * SR)):
    t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (38 + 40 * np.exp(-t * 6)) * t) * np.exp(-t * 2.2)
    noise = lp_fast(rng.normal(0, 1, n), 1800) * np.exp(-t * 5) * 0.5
    return (boom + noise) * 0.9


def riser(n):
    t = np.arange(n) / SR
    noise = rng.normal(0, 1, n)
    sweep = np.zeros(n)
    k = n // 8
    for i in range(8):  # stepped filter sweep
        seg = noise[i * k:(i + 1) * k]
        sweep[i * k:(i + 1) * k] = lp_fast(seg, 400 + i * 900)
    return sweep * (t / t[-1]) ** 2 * 0.45


CHORDS = [  # A minor: Am – F – C – G   (root, third, fifth in Hz)
    (110.0, 130.81, 164.81), (87.31, 110.0, 130.81), (130.81, 164.81, 196.0), (98.0, 123.47, 146.83)]


def track(duration, hits, out_path, end_at=None):
    """hits: chapter-start times (s) → impact + drum fill; end_at: outro (drums stop, pad rings)."""
    n = int(duration * SR)
    mix = np.zeros((n, 2))
    bar = 4 * BEAT
    end_at = end_at or duration
    # pad: detuned saws, low-passed, one chord per bar
    t0 = 0.0; ci = 0
    while t0 < duration:
        m = min(int(bar * SR), n - int(t0 * SR))
        if m <= 0:
            break
        root, third, fifth = CHORDS[ci % 4]
        pad = sum(osc_saw(f * 2, m, 0.004) for f in (root, third, fifth)) / 3
        pad = lp_fast(pad, 900) * env(m, 0.4, 0.4) * 0.22
        s = int(t0 * SR)
        mix[s:s + m, 0] += pad; mix[s:s + m, 1] += np.roll(pad, 220)
        # bass: 8th-note pulse on chord root (only after intro)
        if t0 >= bar * 0.5 and t0 < end_at:
            step = BEAT / 2
            for k in range(8):
                bs = int((t0 + k * step) * SR); bn = int(step * 0.9 * SR)
                if bs + bn > n or (t0 + k * step) >= end_at:
                    break
                b = np.sin(2 * np.pi * root / 2 * np.arange(bn) / SR)
                b += 0.35 * np.sign(b)
                b = lp_fast(b, 380) * env(bn, 0.005, 0.08) * 0.32
                mix[bs:bs + bn] += b[:, None]
        t0 += bar; ci += 1
    # drums from first hit until outro
    start = hits[0] + bar if len(hits) else 2 * bar
    t = start
    K, S_, H = kick(), snare(), hat()
    while t < end_at - 0.05:
        for k in range(8):
            tt = t + k * BEAT / 2
            if tt >= end_at - 0.05:
                break
            s = int(tt * SR)
            def add(x, g=1.0, pan=0.0):
                m = min(len(x), n - s)
                if m > 0:
                    mix[s:s + m, 0] += x[:m] * g * (1 - pan)
                    mix[s:s + m, 1] += x[:m] * g * (1 + pan)
            add(H, 1.0, 0.3 if k % 2 else -0.3)
            if k in (0, 3, 4):
                add(K, 1.0)
            if k in (2, 6):
                add(S_, 0.8)
        t += bar
    # risers into each chapter + impacts on the cut
    for h in list(hits) + [end_at]:
        rn = int(1.6 * SR); rs = int(h * SR) - rn
        if rs > 0:
            r = riser(rn); mix[rs:rs + rn, 0] += r; mix[rs:rs + rn, 1] += r[::-1] * 0.9 + r * 0.1
        im = impact(); s = int(h * SR); m = min(len(im), n - s)
        if m > 0:
            mix[s:s + m] += im[:m, None] * 0.8
    # master: soft clip, fades, normalise
    fade = int(1.5 * SR)
    mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
    mix[:int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))[:, None]
    mix = np.tanh(mix * 1.3)
    mix /= np.max(np.abs(mix)) * 1.05
    data = (mix * 32767).astype(np.int16)
    with wave.open(out_path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())
    return out_path


if __name__ == "__main__":
    track(20, [0.0, 5.0, 10.0, 15.0], "/tmp/music-test.wav")
