"""Millillion podcast intro: an original ~12s piece, synthesized from scratch.

Japanese "in" scale (miyako-bushi) on D: D Eb G A Bb. The koto melody is a
palindrome, like the mark ɛ∞ɜ. Plucks are Karplus-Strong strings, the taiko is a
pitched membrane hit, the pad is detuned sines, and a convolution reverb made from
decaying noise gives the room.

  python3 episodes-src/make_intro.py episodes-src/intro.wav
"""
import sys
import numpy as np
import wave

SR = 44100
rng = np.random.default_rng(3003)  # v2: bright yo-scale version; v1 (in scale) is make_intro_v1_dark.py


def hz(note):
    names = {"C": 0, "C#": 1, "D": 2, "Eb": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "Ab": 8, "A": 9, "Bb": 10, "B": 11}
    n, octave = note[:-1], int(note[-1])
    return 440.0 * 2 ** ((names[n] + 12 * (octave + 1) - 69) / 12)


def koto(freq, dur, bright=0.55, bend=0.0):
    """Karplus-Strong plucked string with a slight pitch 'oshi' bend at the attack."""
    n = int(SR * dur)
    period = int(SR / freq)
    buf = rng.uniform(-1, 1, period) * np.hanning(period) ** 0.3
    out = np.zeros(n)
    idx = 0
    for i in range(n):
        out[i] = buf[idx]
        nxt = (idx + 1) % period
        buf[idx] = 0.996 * (bright * buf[idx] + (1 - bright) * buf[nxt]) + (1 - 0.996) * 0
        idx = nxt
    if bend:
        t = np.arange(n) / SR
        ratio = 1 + bend * np.exp(-t * 18)
        pos = np.cumsum(ratio)
        pos = np.clip(pos, 0, n - 1)
        out = np.interp(pos, np.arange(n), out)
    env = np.minimum(1, np.arange(n) / (0.002 * SR))
    return out * env


def taiko(dur=1.6, f0=92, f1=46, gain=1.0):
    n = int(SR * dur)
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 9)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    skin = rng.normal(0, 1, n) * np.exp(-t * 55) * 0.35
    lp = np.convolve(skin, np.ones(24) / 24, mode="same")
    return (body + lp) * gain


def pad(freqs, dur, attack=2.5, release=3.0):
    n = int(SR * dur)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for f in freqs:
        for det in (-0.35, 0.0, 0.42):
            s += np.sin(2 * np.pi * (f + det) * t + rng.uniform(0, 6.28))
    s /= len(freqs) * 3
    env = np.minimum(1, t / attack) * np.minimum(1, (dur - t) / release).clip(0, 1)
    return s * env * (0.92 + 0.08 * np.sin(2 * np.pi * 0.23 * t))


def sho(freqs, dur, attack=1.6):
    """Reedy cluster: odd harmonics, slow swell, like a shō chord."""
    n = int(SR * dur)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for f in freqs:
        for h, a in ((1, 1.0), (3, 0.18), (5, 0.05)):
            s += a * np.sin(2 * np.pi * f * h * t + rng.uniform(0, 6.28))
    s /= len(freqs) * 1.45
    env = np.minimum(1, (t / attack) ** 2) * np.minimum(1, (dur - t) / 1.4).clip(0, 1)
    return s * env


def reverb(x, seconds=3.2, mix=0.32):
    n = int(SR * seconds)
    t = np.arange(n) / SR
    ir = rng.normal(0, 1, n) * np.exp(-t * 2.2)
    ir[: int(0.012 * SR)] = 0  # pre-delay
    ir /= np.sqrt(np.sum(ir ** 2))
    wet = np.fft.irfft(np.fft.rfft(x, len(x) + n) * np.fft.rfft(ir, len(x) + n))[: len(x) + n]
    dry = np.concatenate([x, np.zeros(n)])
    return (1 - mix) * dry + mix * wet


def place(track, sound, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    end = min(len(track), i + len(sound))
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    track[i:end, 0] += sound[: end - i] * gain * l
    track[i:end, 1] += sound[: end - i] * gain * r


def main(out):
    """v2: the yo scale (D E F# A B) for a bright, hopeful, rising feel."""
    length = 12.5
    mix = np.zeros((int(SR * length), 2))

    # warm open pad: D major-pentatonic colour (D A E F#), swelling in
    place(mix, pad([hz("D3"), hz("A3"), hz("E4"), hz("F#4")], 12.0, attack=1.6), 0.0, 0.15)
    # light, lifting pulse: soft taiko on the downbeats, a quicker ghost hit before each
    for at, g in ((0.30, 0.65), (2.30, 0.45), (4.30, 0.6), (6.30, 0.5), (8.30, 0.55)):
        place(mix, taiko(dur=1.0, f0=110, f1=60, gain=g), at, 0.42)
        place(mix, taiko(dur=0.5, f0=150, f1=90, gain=g * 0.35), at - 0.25, 0.42, pan=0.2)

    # koto: a rising arpeggio, then the palindrome motif in the yo scale
    for k, nt in enumerate(["D4", "A4", "D5", "E5"]):
        place(mix, koto(hz(nt), 2.4, bright=0.6), 0.55 + 0.16 * k, 0.24, pan=-0.4 + 0.25 * k)
    phrase = ["D5", "E5", "F#5", "A5", "B5", "A5", "F#5", "E5", "D5"]
    times = [1.55, 1.82, 2.09, 2.36, 2.90, 3.44, 3.71, 3.98, 4.25]
    for k, (nt, at) in enumerate(zip(phrase, times)):
        place(mix, koto(hz(nt), 3.0, bright=0.62, bend=0.02 if nt == "B5" else 0.0), at, 0.33,
              pan=-0.3 + 0.6 * k / (len(phrase) - 1))
    # the answer climbs instead of falling: hope, then lift-off
    for nt, at in (("E5", 5.15), ("F#5", 5.45), ("A5", 5.75), ("B5", 6.05), ("D6", 6.55)):
        place(mix, koto(hz(nt), 3.6, bright=0.64), at, 0.30, pan=0.2)
    # bright sho-like chord (D A E F# B) blooms under the resolution
    place(mix, sho([hz("D4"), hz("A4"), hz("E5"), hz("F#5")], 5.0, attack=1.4), 6.3, 0.075)
    # warm landing: a soft low D and A, letting the chord settle (no high, ringing notes)
    for nt, at, g in (("D4", 8.6, 0.26), ("A3", 8.62, 0.18), ("D3", 8.64, 0.16)):
        place(mix, koto(hz(nt), 4.0, bright=0.42), at, g, pan=-0.1)

    stereo = np.stack([reverb(mix[:, 0]), reverb(mix[:, 1])], axis=1)[: int(SR * (length + 2.0))]
    fade = int(2.4 * SR)
    stereo[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
    stereo /= np.max(np.abs(stereo)) / 0.89
    pcm = (stereo * 32767).astype("<i2")
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("wrote", out, f"{len(stereo) / SR:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "intro.wav")
