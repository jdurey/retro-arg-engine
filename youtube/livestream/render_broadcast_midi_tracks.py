#!/usr/bin/env python3
"""High-Fidelity 1980s Roland & Yamaha FM Synthesizer for Standard MIDI Files.
Renders all 30 Project Stardust MIDI compositions into high-resolution 44.1kHz stereo
broadcast masters for the 24/7 YouTube live stream.

Features:
- Stereo spatial panning & chorus width
- 4-Op FM DX7 electric piano simulation
- Detuned analog supersaw synth strings & pads
- Authentic punchy LinnDrum / TR-707 drum synthesis
- Sub-audible 14.2001 Hz carrier tone embedded
- 192 Kbps 44.1kHz stereo MP3 output
"""

import os
import sys
import glob
import subprocess
import numpy as np

SR = 44100

def midi_to_hz(note):
    return 440.0 * (2.0 ** ((note - 69) / 12.0))

def synth_kick(sr=SR):
    dur = 0.28
    n = int(dur * sr)
    t = np.linspace(0, dur, n)
    freq = 160.0 * np.exp(-t * 26.0) + 40.0
    phase = 2 * np.pi * np.cumsum(freq) / sr
    env = np.exp(-t * 18.0)
    click = np.random.normal(0, 0.4, n) * np.exp(-t * 90.0)
    return (0.9 * np.sin(phase) * env + 0.15 * click).astype(np.float32)

def synth_snare(sr=SR):
    dur = 0.26
    n = int(dur * sr)
    t = np.linspace(0, dur, n)
    tone = np.sin(2 * np.pi * 190.0 * t) * np.exp(-t * 28.0)
    noise = np.random.normal(0, 1, n) * np.exp(-t * 14.0)
    snap = np.sin(2 * np.pi * 330.0 * t) * np.exp(-t * 45.0)
    return (0.75 * (0.3 * tone + 0.55 * noise + 0.15 * snap)).astype(np.float32)

def synth_hihat(open_hat=False, sr=SR):
    dur = 0.35 if open_hat else 0.06
    n = int(dur * sr)
    t = np.linspace(0, dur, n)
    noise = np.random.normal(0, 1, n)
    hp = noise - 0.8 * np.roll(noise, 1)
    hp[0] = 0
    decay = 12.0 if open_hat else 50.0
    ring = np.sin(2 * np.pi * 8400 * t) + np.sin(2 * np.pi * 11200 * t)
    return (0.4 * (0.8 * hp + 0.2 * ring) * np.exp(-t * decay)).astype(np.float32)

def synth_cymbal(sr=SR):
    dur = 1.2
    n = int(dur * sr)
    t = np.linspace(0, dur, n)
    noise = np.random.normal(0, 1, n)
    hp = noise - 0.7 * np.roll(noise, 1)
    hp[0] = 0
    ring = np.sin(2 * np.pi * 5870 * t) + np.sin(2 * np.pi * 7340 * t) + np.sin(2 * np.pi * 9210 * t)
    return (0.35 * (hp + 0.35 * ring) * np.exp(-t * 4.5)).astype(np.float32)

def synth_note(freq, dur_s, inst_type, vel, sr=SR):
    n = max(int(dur_s * sr), 1)
    t = np.arange(n) / sr
    amp = (vel / 127.0) ** 1.1

    if inst_type == "bass":
        # Moog / Roland punchy bass
        phase = 2 * np.pi * freq * t
        tri = 2.0 * np.abs(2.0 * (t * freq - np.floor(t * freq + 0.5))) - 1.0
        square = np.sign(np.sin(phase))
        env = np.exp(-t * 6.0)
        # Stereo left/right equal
        mono = amp * 0.85 * (0.65 * tri + 0.35 * square) * env
        return mono.astype(np.float32), mono.astype(np.float32)

    elif inst_type == "lead":
        # 1980s Saw/Pulse Lead with stereo detune
        vib = 1.0 + 0.012 * np.sin(2 * np.pi * 5.2 * t)
        p_l = 2 * np.pi * (freq * 0.998) * np.cumsum(vib) / sr
        p_r = 2 * np.pi * (freq * 1.002) * np.cumsum(vib) / sr
        pulse_l = np.where((p_l % (2 * np.pi)) < (0.42 * 2 * np.pi), 1.0, -1.0)
        pulse_r = np.where((p_r % (2 * np.pi)) < (0.42 * 2 * np.pi), 1.0, -1.0)
        saw_l = 2.0 * ((t * freq * 0.998) - np.floor(t * freq * 0.998 + 0.5))
        saw_r = 2.0 * ((t * freq * 1.002) - np.floor(t * freq * 1.002 + 0.5))

        att = min(int(0.015 * sr), n)
        env = np.ones(n, dtype=np.float32)
        if att > 0:
            env[:att] = np.linspace(0, 1, att)
        rel = min(int(0.08 * sr), n)
        if rel > 0:
            env[-rel:] = np.linspace(1, 0, rel)

        out_l = amp * 0.45 * (0.6 * saw_l + 0.4 * pulse_l) * env
        out_r = amp * 0.45 * (0.6 * saw_r + 0.4 * pulse_r) * env
        return out_l.astype(np.float32), out_r.astype(np.float32)

    elif inst_type == "epiano":
        # Yamaha DX7 FM E.Piano
        mod_idx = 3.2 * np.exp(-t * 8.5)
        modulator_l = mod_idx * np.sin(2 * np.pi * (2.0 * freq * 0.999) * t)
        modulator_r = mod_idx * np.sin(2 * np.pi * (2.0 * freq * 1.001) * t)
        carrier_l = np.sin(2 * np.pi * freq * t + modulator_l)
        carrier_r = np.sin(2 * np.pi * freq * t + modulator_r)
        env = np.exp(-t * 3.2)
        out_l = amp * 0.55 * carrier_l * env
        out_r = amp * 0.55 * carrier_r * env
        return out_l.astype(np.float32), out_r.astype(np.float32)

    elif inst_type == "brass":
        # Roland Juno Synth Brass
        saw1 = 2.0 * (t * freq - np.floor(t * freq + 0.5))
        saw2 = 2.0 * (t * (freq * 1.008) - np.floor(t * (freq * 1.008) + 0.5))
        saw3 = 2.0 * (t * (freq * 0.992) - np.floor(t * (freq * 0.992) + 0.5))
        env = np.exp(-t * 4.5)
        out_l = amp * 0.38 * (saw1 + saw2) * env
        out_r = amp * 0.38 * (saw1 + saw3) * env
        return out_l.astype(np.float32), out_r.astype(np.float32)

    else: # strings / pads
        # Detuned supersaw pad
        saw1 = 2.0 * (t * (freq * 0.996) - np.floor(t * (freq * 0.996) + 0.5))
        saw2 = 2.0 * (t * (freq * 1.004) - np.floor(t * (freq * 1.004) + 0.5))
        saw3 = 2.0 * (t * (freq * 1.0) - np.floor(t * (freq * 1.0) + 0.5))
        att = min(int(0.06 * sr), n)
        env = np.ones(n, dtype=np.float32)
        if att > 0:
            env[:att] = np.linspace(0, 1, att)
        rel = min(int(0.12 * sr), n)
        if rel > 0:
            env[-rel:] = np.linspace(1, 0, rel)
        out_l = amp * 0.3 * (saw1 + 0.5 * saw3) * env
        out_r = amp * 0.3 * (saw2 + 0.5 * saw3) * env
        return out_l.astype(np.float32), out_r.astype(np.float32)

def render_midi_to_stereo_mp3(midi_path, out_mp3_path):
    try:
        import pretty_midi
        pm = pretty_midi.PrettyMIDI(midi_path)
    except Exception as e:
        print(f"Skipping {midi_path} due to load error: {e}")
        return

    dur = pm.get_end_time() + 2.0
    n_total = int(dur * SR)
    mix_l = np.zeros(n_total, dtype=np.float32)
    mix_r = np.zeros(n_total, dtype=np.float32)

    sample_kick = synth_kick()
    sample_snare = synth_snare()
    sample_hat_closed = synth_hihat(open_hat=False)
    sample_hat_open = synth_hihat(open_hat=True)
    sample_cymbal = synth_cymbal()

    def add_sample_stereo(s_idx, smp, pan=0.5, gain=1.0):
        # pan: 0.0 (full left) to 1.0 (full right)
        end_idx = min(s_idx + len(smp), n_total)
        needed = end_idx - s_idx
        if needed > 0 and s_idx < n_total:
            chunk = smp[:needed] * gain
            mix_l[s_idx:end_idx] += chunk * (1.0 - pan * 0.7)
            mix_r[s_idx:end_idx] += chunk * (0.3 + pan * 0.7)

    def add_inst_stereo(s_idx, chunk_l, chunk_r, pan=0.5):
        end_idx = min(s_idx + len(chunk_l), n_total)
        needed = end_idx - s_idx
        if needed > 0 and s_idx < n_total:
            mix_l[s_idx:end_idx] += chunk_l[:needed] * (1.2 - pan * 0.6)
            mix_r[s_idx:end_idx] += chunk_r[:needed] * (0.6 + pan * 0.6)

    for inst in pm.instruments:
        name_lower = inst.name.lower()
        if inst.is_drum:
            for note in inst.notes:
                s_idx = int(note.start * SR)
                gain = (note.velocity / 127.0)
                if note.pitch in (35, 36):
                    add_sample_stereo(s_idx, sample_kick, pan=0.5, gain=gain)
                elif note.pitch in (38, 40):
                    add_sample_stereo(s_idx, sample_snare, pan=0.52, gain=gain)
                elif note.pitch in (42, 44):
                    add_sample_stereo(s_idx, sample_hat_closed, pan=0.68, gain=gain)
                elif note.pitch == 46:
                    add_sample_stereo(s_idx, sample_hat_open, pan=0.35, gain=gain)
                elif note.pitch in (49, 51, 57):
                    add_sample_stereo(s_idx, sample_cymbal, pan=0.8, gain=gain)
                else:
                    add_sample_stereo(s_idx, sample_snare, pan=0.5, gain=gain * 0.6)
        else:
            if "bass" in name_lower:
                inst_t = "bass"
                pan = 0.5
            elif "piano" in name_lower or "rhodes" in name_lower or "keys" in name_lower:
                inst_t = "epiano"
                pan = 0.42
            elif "brass" in name_lower:
                inst_t = "brass"
                pan = 0.58
            elif "string" in name_lower or "pad" in name_lower or "orchestra" in name_lower:
                inst_t = "strings"
                pan = 0.5
            else:
                inst_t = "lead"
                pan = 0.5

            for note in inst.notes:
                dur_s = max(note.end - note.start, 0.05)
                s_idx = int(note.start * SR)
                freq = midi_to_hz(note.pitch)
                audio_l, audio_r = synth_note(freq, dur_s, inst_t, note.velocity, sr=SR)
                add_inst_stereo(s_idx, audio_l, audio_r, pan=pan)

    # Embed 14.2001 Hz carrier tone & subtle vintage tape hiss
    t_axis = np.arange(n_total) / SR
    carrier = 0.025 * np.sin(2 * np.pi * 14.2001 * t_axis)
    tape_l = 0.012 * np.random.normal(0, 1, n_total).astype(np.float32)
    tape_r = 0.012 * np.random.normal(0, 1, n_total).astype(np.float32)
    mix_l += carrier + tape_l
    mix_r += carrier + tape_r

    # Soft clip limiter
    peak = max(np.max(np.abs(mix_l)), np.max(np.abs(mix_r)), 1e-6)
    if peak > 0.85:
        mix_l = np.tanh(mix_l / (peak * 0.8)) * 0.95
        mix_r = np.tanh(mix_r / (peak * 0.8)) * 0.95

    # Interleave to 16-bit PCM stereo
    int_l = (mix_l * 32767.0).astype(np.int16)
    int_r = (mix_r * 32767.0).astype(np.int16)
    stereo = np.empty((n_total * 2,), dtype=np.int16)
    stereo[0::2] = int_l
    stereo[1::2] = int_r

    os.makedirs(os.path.dirname(out_mp3_path), exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "pipe:0",
        "-filter_complex",
        "[0:a]volume=0.40,highpass=f=140:poles=1,lowpass=f=5200:poles=2,equalizer=f=400:t=q:w=1.2:g=2.5,equalizer=f=1800:t=q:w=1.5:g=1.5,equalizer=f=3500:t=q:w=1.0:g=-3[out]",
        "-map", "[out]",
        "-c:a", "libmp3lame", "-b:a", "192k",
        out_mp3_path
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate(input=stereo.tobytes())
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg failed for {out_mp3_path}")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(os.path.dirname(here))
    midi_sources = os.path.join(root, "assets", "midi")
    out_dir = os.path.join(here, "broadcast_archive", "midi_masters")
    os.makedirs(out_dir, exist_ok=True)

    midi_files = sorted(glob.glob(os.path.join(midi_sources, "*.mid")))
    print(f"Found {len(midi_files)} MIDI tracks to render into broadcast masters...")

    for idx, mf_path in enumerate(midi_files, 1):
        slug = os.path.splitext(os.path.basename(mf_path))[0]
        out_mp3 = os.path.join(out_dir, f"midi_{slug}.mp3")
        print(f" [{idx:02d}/{len(midi_files):02d}] Rendering {slug}.mid -> {os.path.basename(out_mp3)}...")
        render_midi_to_stereo_mp3(mf_path, out_mp3)
        sz = os.path.getsize(out_mp3)
        print(f"       ✓ {sz // 1024} KB (Stereo 192k 44.1kHz)")

    print(f"\nAll {len(midi_files)} MIDI tracks successfully rendered to {out_dir}!")


if __name__ == "__main__":
    main()
