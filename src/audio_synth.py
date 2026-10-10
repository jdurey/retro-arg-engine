"""Synthesises the 'Idol Protocol' excerpts recovered from Orion's Akasaka Branch.

Writes 8 kHz mu-law Sun/NeXT .au files (the native audio format of 1995 FTP
archives). Each excerpt is a bright mid-80s City Pop / kayokyoku arrangement
(FM electric piano, slap bass, drum machine, a lead 'vocal' line) carrying one
deliberate emotional anomaly, as documented in docs/anomalies.txt.

Run once; results are committed under assets/akasaka/audio/ and copied by the
generator. Requires numpy (build-time only).

    python3 src/audio_synth.py [outdir]
"""
import os
import struct
import sys

import numpy as np

SR = 8000
CARRIER_HZ = 14.2
RNG = np.random.default_rng(1985)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12.0)


# ----------------------------------------------------------------------------- voices
def env_exp(n, rate):
    return np.exp(-np.arange(n) / SR * rate)


def fm_epiano(f, dur, amp=0.18):
    n = int(dur * SR)
    t = np.arange(n) / SR
    index = 1.6 * np.exp(-t * 5) + 0.25
    tine = 0.12 * np.sin(2 * np.pi * f * 14 * t) * np.exp(-t * 30)
    return amp * (np.sin(2 * np.pi * f * t + index * np.sin(2 * np.pi * f * t)) + tine) * env_exp(n, 2.2)


def slap_bass(f, dur, amp=0.32):
    n = int(dur * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * f * t + 0.8 * np.exp(-t * 20) * np.sin(2 * np.pi * 2 * f * t))
    click = np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 60) * 0.5
    return amp * (body + click) * env_exp(n, 6)


def kick(amp=0.55):
    n = int(0.25 * SR)
    t = np.arange(n) / SR
    f = 50 + 90 * np.exp(-t * 30)
    return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 12)


def snare(amp=0.30):
    n = int(0.2 * SR)
    t = np.arange(n) / SR
    noise = RNG.uniform(-1, 1, n)
    return amp * (0.8 * noise * env_exp(n, 22) + 0.4 * np.sin(2 * np.pi * 190 * t) * env_exp(n, 30))


def hat(amp=0.07):
    n = int(0.05 * SR)
    noise = RNG.uniform(-1, 1, n + 1)
    return amp * np.diff(noise) * env_exp(n, 70)


def lead(f, dur, amp=0.20, vibrato=True, drift_cents=None, quantised=False):
    """Bright FM 'vocal' line. drift_cents=(start_s, depth) bends pitch and snaps back."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    cents = np.zeros(n)
    if vibrato and not quantised:
        cents += 18 * np.sin(2 * np.pi * 5.6 * t) * np.clip(t * 3, 0, 1)
    if drift_cents:
        s, depth = drift_cents
        bend = np.clip((t - s) / 0.35, 0, 1) * depth
        bend[t > s + 0.55] = 0.0  # snap back
        cents += bend
    freq = f * 2 ** (cents / 1200.0)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    a = np.minimum(1, t * 25) * np.exp(-t * 0.6)
    a[-int(0.03 * SR):] *= np.linspace(1, 0, int(0.03 * SR))
    tone = np.sin(phase + 0.9 * np.sin(2 * phase)) if not quantised else np.sign(np.sin(phase)) * 0.55
    return amp * tone * a


def rage(f, dur, amp=0.30):
    """The unmasked take: distorted, minor, 14.2 Hz tremolo."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    saw = 2 * ((f * t + 0.5 * np.sin(2 * np.pi * 3 * t)) % 1.0) - 1
    saw2 = 2 * ((f * 1.007 * t) % 1.0) - 1
    dist = np.tanh(6 * (saw + saw2))
    trem = 0.55 + 0.45 * np.sin(2 * np.pi * CARRIER_HZ * t)
    return amp * dist * trem


def place(buf, sig, at_s):
    i = int(at_s * SR)
    j = min(len(buf), i + len(sig))
    if i < len(buf):
        buf[i:j] += sig[: j - i]


# ----------------------------------------------------------------------------- arrangement
PROG_CITYPOP = [[53, 57, 60, 64], [52, 56, 59, 62], [57, 60, 64, 67], [55, 58, 62, 65]]  # Fmaj7 E7 Am7 Gm7
PROG_KAYO = [[57, 60, 64], [53, 57, 60], [55, 59, 62], [52, 56, 59]]                     # Am F G E


def backing(seconds, bpm, prog, buf, swing=True):
    beat = 60.0 / bpm
    bar = beat * 4
    nbars = int(seconds / bar) + 1
    for b in range(nbars):
        chord = prog[b % len(prog)]
        t0 = b * bar
        for stab in (0.0, 1.5, 2.5) if swing else (0.0, 2.0):
            for nn in chord:
                place(buf, fm_epiano(midi(nn), beat * 1.4), t0 + stab * beat)
        root = chord[0] - 12
        for pos, nn in ((0, root), (1.5, root + 12), (2, root), (3, root + 7), (3.5, root + 12)):
            place(buf, slap_bass(midi(nn), beat * 0.6), t0 + pos * beat)
        for k in range(4):
            place(buf, kick() if k in (0, 2) else snare(), t0 + k * beat)
        for k in range(8):
            place(buf, hat(), t0 + k * beat / 2)


MELODY = [(0, 1, 72), (1, 0.5, 74), (1.5, 1.5, 76), (4, 1, 79), (5, 1, 76), (6, 2, 74),
          (8, 0.5, 72), (8.5, 0.5, 74), (9, 1, 76), (10, 2, 81), (12, 1, 79), (13, 1, 76), (14, 2, 74)]


def melody(buf, bpm, start_s, notes=MELODY, repeat=2, **kw):
    beat = 60.0 / bpm
    span = 16 * beat
    for r in range(repeat):
        for pos, dur, nn in notes:
            place(buf, lead(midi(nn), dur * beat * 0.95, **kw), start_s + r * span + pos * beat)


def master(buf, carrier_db=-58.0):
    t = np.arange(len(buf)) / SR
    # 14.2 Hz carrier: inaudible in itself, but present in the file, as on every reel.
    buf = buf + 10 ** (carrier_db / 20) * np.sin(2 * np.pi * CARRIER_HZ * t)
    buf = buf + RNG.normal(0, 0.004, len(buf))  # tape hiss
    peak = np.max(np.abs(buf)) or 1.0
    buf = buf / peak * 0.9
    fade = int(0.25 * SR)
    buf[:fade] *= np.linspace(0, 1, fade)
    buf[-fade:] *= np.linspace(1, 0, fade)
    return buf


PROG_SYNTHETIC = [[45, 52, 57, 60], [41, 48, 53, 57], [48, 55, 60, 64], [43, 50, 55, 59]]  # Am F C G
PROG_HATCH = [[47, 54, 59, 62], [43, 50, 55, 59], [40, 47, 52, 55], [42, 49, 54, 58]]          # Bm7 Gmaj7 Em9 F#7
PROG_SMILE = [[48, 52, 55, 60], [45, 48, 52, 55], [41, 45, 48, 52], [43, 47, 50, 53]]          # Cmaj7 Am7 Dm7 G7

MELODY_SYNTHETIC = [
    (0, 1.0, 69), (1, 0.5, 72), (1.5, 0.5, 71), (2, 1.0, 69), (3, 1.0, 67), (4, 2.0, 69),
    (6, 1.0, 69), (7, 0.5, 72), (7.5, 0.5, 74), (8, 2.0, 76), (10, 1.0, 74), (11, 1.0, 72), (12, 3.0, 69)
]

MELODY_HATCH = [
    (0, 1.5, 71), (1.5, 0.5, 74), (2, 1.0, 76), (3, 1.0, 74), (4, 2.0, 71), (6, 1.0, 69), (7, 1.0, 67),
    (8, 1.5, 71), (9.5, 0.5, 74), (10, 1.0, 78), (11, 1.0, 76), (12, 2.0, 74), (14, 2.0, 71)
]

MELODY_SMILE = [
    (0, 0.5, 72), (0.5, 0.5, 76), (1, 0.5, 79), (1.5, 0.5, 84), (2, 1.0, 81), (3, 1.0, 79),
    (4, 0.5, 77), (4.5, 0.5, 79), (5, 0.5, 81), (5.5, 0.5, 79), (6, 2.0, 76),
    (8, 0.5, 72), (8.5, 0.5, 74), (9, 1.0, 76), (10, 1.0, 79), (11, 1.0, 77), (12, 3.0, 72)
]


# ----------------------------------------------------------------------------- tracks
def track_a1():  # Synthetic Dawn (Akasaka Mix): A minor, industrial square wave, +38 cent drift at 0:07
    secs, bpm = 12.0, 116
    buf = np.zeros(int(secs * SR))
    backing(secs, bpm, PROG_SYNTHETIC, buf, swing=False)
    melody(buf, bpm, 0.0, notes=MELODY_SYNTHETIC, repeat=1)
    beat = 60.0 / bpm
    place(buf, lead(midi(81), 1.6, drift_cents=(0.35, 38)), 7.0)
    melody(buf, bpm, 16 * beat + 1.6, notes=MELODY_SYNTHETIC[:6], repeat=1)
    return master(buf)


def track_a2():  # Memory Hatch (City Pop Version): B minor, Rhodes & slap bass, 1.2 s unmasked take at 0:09
    secs, bpm = 13.0, 104
    buf = np.zeros(int(secs * SR))
    backing(secs, bpm, PROG_HATCH, buf, swing=True)
    melody(buf, bpm, 0.0, notes=MELODY_HATCH, repeat=2)
    a, b = int(9.0 * SR), int(10.2 * SR)
    buf[a:b] *= 0.18  # the smile ducks...
    for k, nn in enumerate((59, 62, 58, 59)):  # B minor unmasked take
        place(buf, rage(midi(nn), 0.3), 9.0 + k * 0.3)
    buf[b:b + int(0.04 * SR)] = 0.0  # gate clamps
    return master(buf)


def track_a3():  # Synthesized Smile: C major, rigidly quantised to the cent, clockwork idol pop
    secs, bpm = 12.0, 128
    buf = np.zeros(int(secs * SR))
    backing(secs, bpm, PROG_SMILE, buf, swing=False)
    melody(buf, bpm, 0.0, notes=MELODY_SMILE, repeat=2, quantised=True, vibrato=False)
    return master(buf)


def track_b1():  # Threshold (Kayo Version): F#4 sustain cut at half a bar, continues under silence
    secs, bpm = 14.0, 76
    buf = np.zeros(int(secs * SR))
    body = 9.0
    backing(body, bpm, PROG_KAYO, buf, swing=False)
    notes = [(0, 2, 69), (2, 1, 72), (3, 1, 71), (4, 2, 69), (6, 2, 64), (8, 1, 65), (9, 1, 67), (10, 2, 64)]
    melody(buf, bpm, 0.0, notes=notes, repeat=1)
    beat = 60.0 / bpm
    buf[int(body * SR):] = 0.0
    place(buf, lead(midi(66), beat * 2), body - beat * 2)  # F#4, half a bar, as ordered
    t = np.arange(int((secs - body) * SR)) / SR
    ghost = 0.012 * np.sin(2 * np.pi * midi(66) * t) * (0.5 + 0.5 * np.sin(2 * np.pi * CARRIER_HZ * t))
    place(buf, ghost * np.exp(-t * 0.25), body)
    return master(buf)


def track_b2():  # Ghost in the Chorus: the double-track leaves the sheet six times
    secs, bpm = 12.0, 118
    buf = np.zeros(int(secs * SR))
    backing(secs, bpm, PROG_CITYPOP, buf)
    melody(buf, bpm, 0.0, repeat=2)
    beat = 60.0 / bpm
    subs = {1: 73, 4: 78, 6: 75, 9: 80, 10: 70, 12: 77}  # six substituted syllables
    for r in range(2):
        for i, (pos, dur, nn) in enumerate(MELODY):
            sung = subs.get(i, nn) if r == 1 else nn
            place(buf, lead(midi(sung) * 1.003, dur * beat * 0.95, amp=0.11), r * 16 * beat + pos * beat + 0.012)
    return master(buf)


TRACKS = [
    ("jp-85-sd-r_synthetic_dawn_rework.au", "AKASAKA REEL JP-85-SD-R SYNTHETIC DAWN (AKASAKA REWORK) VOICE PRINT GEN-3", track_a1),
    ("jp-85-mh-r_memory_hatch_citypop.au", "AKASAKA REEL JP-85-MH-R MEMORY HATCH (CITY POP REWORK) VOICE PRINT GEN-3", track_a2),
    ("jp-85-th-r_threshold_kayo.au", "AKASAKA REEL JP-85-TH-R THRESHOLD (KAYOKYOKU REWORK) VOICE PRINT GEN-3", track_b1),
    ("synthesized_smile.au", "AKASAKA REEL (NO FILE) SYNTHESIZED SMILE 85", track_a3),
    ("ghost_in_the_chorus.au", "AKASAKA REEL (NO FILE) GHOST IN THE CHORUS 85", track_b2),
]


# ----------------------------------------------------------------------------- encoding
def mulaw(x):
    """ITU-T G.711 mu-law, bit-exact with the classic Sun/CCITT encoder."""
    s = np.clip(np.round(x * 32767), -32767, 32767).astype(np.int32)
    sign = np.where(s < 0, 0x80, 0)
    mag = np.minimum(np.abs(s), 32635) + 0x84
    exp = np.floor(np.log2(mag)).astype(np.int32) - 7
    exp = np.clip(exp, 0, 7)
    mant = (mag >> (exp + 3)) & 0x0F
    return (~(sign | (exp << 4) | mant) & 0xFF).astype(np.uint8)


def write_au(path, samples, annotation):
    ann = annotation.encode("ascii") + b"\0"
    ann += b"\0" * ((-len(ann)) % 8)
    data = mulaw(samples).tobytes()
    header = struct.pack(">4sIIIII", b".snd", 24 + len(ann), len(data), 1, SR, 1)
    with open(path, "wb") as f:
        f.write(header + ann + data)
    return len(header) + len(ann) + len(data)


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    for fname, ann, fn in TRACKS:
        size = write_au(os.path.join(outdir, fname), fn(), ann)
        print("  %-36s %7d bytes" % (fname, size))


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "assets", "akasaka", "audio"))
