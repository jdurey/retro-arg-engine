"""Synthesizes Standard MIDI compositions into authentic 1990s Sound Blaster / FM audio.

Encodes each song as an authentic 14.4 kb/s (16 kbps mono) MP3 stream.
"""
import os
import subprocess
import numpy as np

import generate_midis as gm

SR = 22050


def midi_to_hz(note):
    return 440.0 * (2.0 ** ((note - 69) / 12.0))


def synth_kick(sr=SR):
    dur = 0.22
    n = int(dur * sr)
    t = np.linspace(0, dur, n)
    freq = 150.0 * np.exp(-t * 28.0) + 42.0
    phase = 2 * np.pi * np.cumsum(freq) / sr
    env = np.exp(-t * 20.0)
    return (0.85 * np.sin(phase) * env).astype(np.float32)


def synth_snare(sr=SR):
    dur = 0.22
    n = int(dur * sr)
    t = np.linspace(0, dur, n)
    tone = np.sin(2 * np.pi * 185.0 * t) * np.exp(-t * 30.0)
    noise = np.random.normal(0, 1, n) * np.exp(-t * 16.0)
    return (0.75 * (0.35 * tone + 0.65 * noise)).astype(np.float32)


def synth_hihat(open_hat=False, sr=SR):
    dur = 0.28 if open_hat else 0.05
    n = int(dur * sr)
    t = np.linspace(0, dur, n)
    noise = np.random.normal(0, 1, n)
    hp = noise - np.roll(noise, 1)
    hp[0] = 0
    decay = 14.0 if open_hat else 55.0
    return (0.45 * hp * np.exp(-t * decay)).astype(np.float32)


def synth_cymbal(sr=SR):
    dur = 0.8
    n = int(dur * sr)
    t = np.linspace(0, dur, n)
    noise = np.random.normal(0, 1, n)
    hp = noise - 0.7 * np.roll(noise, 1)
    hp[0] = 0
    # Metallic resonant ring
    ring = np.sin(2 * np.pi * 5430 * t) + np.sin(2 * np.pi * 7120 * t)
    return (0.35 * (hp + 0.3 * ring) * np.exp(-t * 5.0)).astype(np.float32)


def synth_note(freq, dur_s, inst_type, vel, sr=SR):
    n = max(int(dur_s * sr), 1)
    t = np.arange(n) / sr
    amp = (vel / 127.0)
    
    if inst_type == "bass":
        # Triangle + pulse punch
        phase = 2 * np.pi * freq * t
        tri = 2.0 * np.abs(2.0 * (t * freq - np.floor(t * freq + 0.5))) - 1.0
        square = np.sign(np.sin(phase))
        env = np.exp(-t * 7.0)
        return (amp * 0.7 * (0.6 * tri + 0.4 * square) * env).astype(np.float32)
        
    elif inst_type == "lead":
        # Pulse wave with 5.5 Hz vibrato
        vib = 1.0 + 0.015 * np.sin(2 * np.pi * 5.5 * t)
        phase = 2 * np.pi * freq * np.cumsum(vib) / sr
        pulse = np.where((phase % (2 * np.pi)) < (0.38 * 2 * np.pi), 1.0, -1.0)
        # ADSR: 0.02s attack, sustained with soft release
        att = min(int(0.02 * sr), n)
        env = np.ones(n, dtype=np.float32)
        if att > 0:
            env[:att] = np.linspace(0, 1, att)
        rel = min(int(0.06 * sr), n)
        if rel > 0:
            env[-rel:] = np.linspace(1, 0, rel)
        return (amp * 0.4 * pulse * env).astype(np.float32)

    elif inst_type == "epiano":
        # 2-Op FM: carrier = f, mod = 2*f with fast decaying index
        mod_idx = 2.8 * np.exp(-t * 9.0)
        modulator = mod_idx * np.sin(2 * np.pi * (2.0 * freq) * t)
        carrier = np.sin(2 * np.pi * freq * t + modulator)
        env = np.exp(-t * 3.5)
        return (amp * 0.5 * carrier * env).astype(np.float32)

    elif inst_type == "brass":
        # Dual detuned saw stabs
        saw1 = 2.0 * (t * freq - np.floor(t * freq + 0.5))
        saw2 = 2.0 * (t * (freq * 1.006) - np.floor(t * (freq * 1.006) + 0.5))
        env = np.exp(-t * 5.0)
        return (amp * 0.35 * (saw1 + saw2) * env).astype(np.float32)

    else: # strings / default pad
        saw1 = 2.0 * (t * freq - np.floor(t * freq + 0.5))
        saw2 = 2.0 * (t * (freq * 0.996) - np.floor(t * (freq * 0.996) + 0.5))
        att = min(int(0.08 * sr), n)
        env = np.ones(n, dtype=np.float32)
        if att > 0:
            env[:att] = np.linspace(0, 1, att)
        rel = min(int(0.12 * sr), n)
        if rel > 0:
            env[-rel:] = np.linspace(1, 0, rel)
        return (amp * 0.25 * (saw1 + saw2) * env).astype(np.float32)


def render_midi_to_audio(mf, out_mp3_path):
    div = mf.division
    
    # Extract tempo from track 0
    bpm = 120.0
    for tick, b in mf.tracks[0].events:
        if len(b) >= 6 and b[:3] == b"\xFF\x51\x03":
            us = (b[3] << 16) | (b[4] << 8) | b[5]
            bpm = 60_000_000.0 / us
            break
            
    # Find total length
    max_tick = 0
    for t in mf.tracks:
        for tick, b in t.events:
            if tick > max_tick:
                max_tick = tick
                
    dur_total = (max_tick / div) * (60.0 / bpm) + 1.2
    n_total = int(dur_total * SR)
    mix = np.zeros(n_total, dtype=np.float32)
    
    # Pre-render drum samples
    sample_kick = synth_kick()
    sample_snare = synth_snare()
    sample_hat_closed = synth_hihat(open_hat=False)
    sample_hat_open = synth_hihat(open_hat=True)
    sample_cymbal = synth_cymbal()

    def add_sample(buf, start_idx, smp, gain=1.0):
        end_idx = min(start_idx + len(smp), len(buf))
        needed = end_idx - start_idx
        if needed > 0 and start_idx < len(buf):
            buf[start_idx:end_idx] += smp[:needed] * gain

    # Parse and render each track
    for t_idx, t in enumerate(mf.tracks):
        # Determine track instrument type
        name_lower = t.name.lower()
        if "lead" in name_lower or "vocal" in name_lower:
            inst = "lead"
        elif "bass" in name_lower:
            inst = "bass"
        elif "piano" in name_lower or "rhodes" in name_lower or "chord" in name_lower:
            inst = "epiano"
        elif "brass" in name_lower:
            inst = "brass"
        elif "string" in name_lower or "pad" in name_lower:
            inst = "strings"
        else:
            inst = "lead"
            
        active = {}
        for tick, b in t.events:
            t_sec = (tick / div) * (60.0 / bpm)
            s_idx = int(t_sec * SR)
            
            # Note On
            if len(b) >= 3 and (b[0] & 0xF0) == 0x90 and b[2] > 0:
                ch = b[0] & 0x0F
                pitch = b[1]
                vel = b[2]
                if ch == 9: # Drum channel
                    gain = vel / 127.0
                    if pitch in (35, 36):
                        add_sample(mix, s_idx, sample_kick, gain)
                    elif pitch in (38, 40):
                        add_sample(mix, s_idx, sample_snare, gain)
                    elif pitch in (42, 44):
                        add_sample(mix, s_idx, sample_hat_closed, gain)
                    elif pitch == 46:
                        add_sample(mix, s_idx, sample_hat_open, gain)
                    elif pitch in (49, 51, 57):
                        add_sample(mix, s_idx, sample_cymbal, gain)
                    else:
                        add_sample(mix, s_idx, sample_snare, gain * 0.6)
                else:
                    active[(ch, pitch)] = (tick, vel)
                    
            # Note Off
            elif len(b) >= 3 and (((b[0] & 0xF0) == 0x80) or ((b[0] & 0xF0) == 0x90 and b[2] == 0)):
                ch = b[0] & 0x0F
                pitch = b[1]
                if (ch, pitch) in active and ch != 9:
                    st, vel = active.pop((ch, pitch))
                    st_sec = (st / div) * (60.0 / bpm)
                    dur_s = max((tick - st) / div * (60.0 / bpm), 0.05)
                    st_idx = int(st_sec * SR)
                    freq = midi_to_hz(pitch)
                    note_audio = synth_note(freq, dur_s, inst, vel, sr=SR)
                    add_sample(mix, st_idx, note_audio)

    # Add a touch of authentic analog tape hiss & 14.2 Hz carrier
    t_axis = np.arange(n_total) / SR
    carrier = 0.03 * np.sin(2 * np.pi * 14.2 * t_axis)
    tape_hiss = 0.015 * np.random.normal(0, 1, n_total).astype(np.float32)
    mix += carrier + tape_hiss

    # Soft clip limiter
    peak = np.max(np.abs(mix))
    if peak > 0:
        mix = np.tanh(mix / (peak * 0.7)) * 0.95
        
    int_audio = (mix * 32767.0).astype(np.int16)
    
    # Encode with ffmpeg to 16 kbps mono MP3 (authentic 14.4k modem streaming)
    os.makedirs(os.path.dirname(out_mp3_path), exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "pipe:0",
        "-b:a", "16k", "-ac", "1",
        out_mp3_path
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate(input=int_audio.tobytes())
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg encoding failed for {out_mp3_path}")
    print(f"Generated {out_mp3_path} ({os.path.getsize(out_mp3_path) / 1024:.1f} KB)")


def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(root_dir, "assets", "audio", "streams")
    os.makedirs(out_dir, exist_ok=True)
    
    songs = [
        ("gasoline_heart", gm.make_gasoline_heart()),
        ("ghost_transit", gm.make_ghost_transit()),
        ("midnight_animal", gm.make_midnight_animal()),
        ("brighter_than_sun", gm.make_brighter_than_sun()),
        ("only_we_remain", gm.make_only_we_remain()),
        ("synthetic_dawn", gm.make_synthetic_dawn()),
        ("memory_hatch", gm.make_memory_hatch()),
    ]
    
    print(f"Rendering {len(songs)} Nova Hart MIDI tracks to 14.4k audio streams...")
    for slug, mf in songs:
        target = os.path.join(out_dir, f"{slug}_14k.mp3")
        render_midi_to_audio(mf, target)
        
    print("\nAll 14.4k audio streams generated successfully!")


if __name__ == "__main__":
    main()
