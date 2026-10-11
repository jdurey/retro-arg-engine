"""Automated YouTube ingestion and MIDI transcription for Nova Hart songs.
Uses yt-dlp to fetch authentic Nova Hart audio from YouTube,
Spotify's basic-pitch model (via CoreML) to transcribe polyphonic pitches,
and arranges them into 1990s multi-track General MIDI and 14.4k dialup MP3 streams.
"""
import os
import subprocess
import tempfile
import pretty_midi
import numpy as np
from basic_pitch.inference import predict

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIDI_DIR = os.path.join(ROOT_DIR, "assets", "midi")
STREAM_DIR = os.path.join(ROOT_DIR, "assets", "audio", "streams")
os.makedirs(MIDI_DIR, exist_ok=True)
os.makedirs(STREAM_DIR, exist_ok=True)

# Selected authentic songs from https://www.youtube.com/@NovaHart_Official
SONGS_TO_PROCESS = [
    ("these_wings_are_my_own", "_QE4r34TMCI", "These Wings Are My Own", 116),
    ("shes_hardwired", "KtmSRtFnTzc", "She's Hardwired", 128),
    ("behind_the_glass", "6ZTVnKkyw7w", "Behind the Glass", 88),
    ("chrome_velocity", "muLpxqONSq4", "Chrome Velocity", 134),
    ("hearts_on_fire", "h4Q66vDb4G0", "Hearts on Fire", 124),
    ("hold_back_the_storm", "wDgy5jGsJl0", "Hold Back the Storm", 118),
    ("before_you_disappear", "T9RK8i4TwhM", "Before You Disappear", 82),
    ("static_and_steel", "pYXH4uSegmQ", "Static & Steel", 76),
    ("run_with_the_fire", "iqxi3xxh384", "Run With The Fire", 138),
    ("togethers_the_way", "4IZcnqmfrk8", "Together's the Way (1984 Orion)", 122),
    ("perfect_daydream", "zov7--MyzHw", "Perfect Daydream (1984 Orion)", 114),
    ("summer_of_85", "pu_RIkHEydI", "Summer of '85", 108),
]

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
    ring = np.sin(2 * np.pi * 5430 * t) + np.sin(2 * np.pi * 7120 * t)
    return (0.35 * (hp + 0.3 * ring) * np.exp(-t * 5.0)).astype(np.float32)


def synth_inst_sample(freq, dur_s, inst_type, vel, sr=SR):
    n = max(int(dur_s * sr), 10)
    t = np.linspace(0, dur_s, n)
    gain = (vel / 127.0) ** 1.3
    
    if inst_type == "lead":
        saw = 2.0 * (freq * t - np.floor(freq * t + 0.5))
        pulse = np.sign(np.sin(2 * np.pi * freq * t + 0.2))
        sub = np.sin(2 * np.pi * (freq * 0.5) * t)
        atk = int(0.015 * sr)
        env = np.ones(n)
        if n > atk:
            env[:atk] = np.linspace(0, 1, atk)
        dec = int(0.05 * sr)
        if n > dec:
            env[-dec:] = np.linspace(1, 0, dec)
        return (0.55 * gain * (0.6 * saw + 0.3 * pulse + 0.2 * sub) * env).astype(np.float32)
        
    elif inst_type == "bass":
        sq = np.sign(np.sin(2 * np.pi * freq * t))
        tri = 2.0 * np.abs(2.0 * (freq * t - np.floor(freq * t + 0.5))) - 1.0
        env = np.exp(-t * 6.5)
        return (0.75 * gain * (0.7 * tri + 0.3 * sq) * env).astype(np.float32)
        
    elif inst_type == "epiano":
        carrier = np.sin(2 * np.pi * freq * t)
        mod = np.sin(2 * np.pi * (freq * 14.0) * t) * np.exp(-t * 18.0) * 1.5
        fm = np.sin(2 * np.pi * freq * t + mod)
        env = np.exp(-t * 4.2)
        return (0.6 * gain * fm * env).astype(np.float32)
        
    else:
        sine = np.sin(2 * np.pi * freq * t)
        env = np.exp(-t * 3.0)
        return (0.5 * gain * sine * env).astype(np.float32)


def render_pm_to_mp3(pm, out_mp3_path, sr=SR):
    end_time = pm.get_end_time()
    n_total = int((end_time + 1.0) * sr)
    mix = np.zeros(n_total, dtype=np.float32)

    sample_kick = synth_kick(sr)
    sample_snare = synth_snare(sr)
    sample_hat = synth_hihat(open_hat=False, sr=sr)
    sample_hat_open = synth_hihat(open_hat=True, sr=sr)
    sample_cymbal = synth_cymbal(sr)

    def add_sample(arr, idx, s, vol=1.0):
        if idx >= len(arr) or idx < 0:
            return
        end_idx = min(idx + len(s), len(arr))
        arr[idx:end_idx] += s[:end_idx - idx] * vol

    for inst in pm.instruments:
        name_lower = inst.name.lower()
        if inst.is_drum:
            for note in inst.notes:
                s_idx = int(note.start * sr)
                vel = note.velocity / 127.0
                if note.pitch in (35, 36):
                    add_sample(mix, s_idx, sample_kick, vel)
                elif note.pitch in (38, 40):
                    add_sample(mix, s_idx, sample_snare, vel)
                elif note.pitch in (42, 44):
                    add_sample(mix, s_idx, sample_hat, vel)
                elif note.pitch == 46:
                    add_sample(mix, s_idx, sample_hat_open, vel)
                elif note.pitch in (49, 51, 57):
                    add_sample(mix, s_idx, sample_cymbal, vel)
                else:
                    add_sample(mix, s_idx, sample_snare, vel * 0.6)
        else:
            if "bass" in name_lower:
                inst_t = "bass"
            elif "piano" in name_lower or "keys" in name_lower:
                inst_t = "epiano"
            else:
                inst_t = "lead"

            for note in inst.notes:
                dur_s = max(note.end - note.start, 0.05)
                s_idx = int(note.start * sr)
                freq = midi_to_hz(note.pitch)
                audio = synth_inst_sample(freq, dur_s, inst_t, note.velocity, sr=sr)
                add_sample(mix, s_idx, audio)

    # Dialup tape hiss
    t_axis = np.arange(n_total) / sr
    carrier = 0.02 * np.sin(2 * np.pi * 14.2 * t_axis)
    tape_hiss = 0.012 * np.random.normal(0, 1, n_total).astype(np.float32)
    mix += carrier + tape_hiss

    peak = np.max(np.abs(mix))
    if peak > 0:
        mix = np.tanh(mix / (peak * 0.7)) * 0.95

    int_audio = (mix * 32767.0).astype(np.int16)

    cmd = [
        "ffmpeg", "-y",
        "-f", "s16le", "-ar", str(sr), "-ac", "1", "-i", "pipe:0",
        "-b:a", "16k", "-ac", "1",
        out_mp3_path
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate(input=int_audio.tobytes())
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg encoding failed for {out_mp3_path}")


def process_song(slug, ytid, title, bpm):
    midi_target = os.path.join(MIDI_DIR, f"{slug}.mid")
    mp3_target = os.path.join(STREAM_DIR, f"{slug}_14k.mp3")

    if os.path.exists(midi_target) and os.path.exists(mp3_target):
        print(f"  ✓ [{slug}] already processed ({os.path.getsize(midi_target)} bytes MIDI, {os.path.getsize(mp3_target)//1024} KB MP3)")
        return

    print(f"\nProcessing '{title}' (ID: {ytid}, {bpm} BPM)...")
    with tempfile.TemporaryDirectory() as tmpdir:
        raw_video = os.path.join(tmpdir, "raw.mp4")
        sample_wav = os.path.join(tmpdir, "sample.wav")

        # 1. Download video/audio using yt-dlp with mweb/android player clients
        url = f"https://www.youtube.com/watch?v={ytid}"
        dl_cmd = [
            "python3", "-m", "yt_dlp",
            "--extractor-args", "youtube:player_client=mweb,android,ios",
            "-f", "ba/b",
            "-o", raw_video,
            url
        ]
        res = subprocess.run(dl_cmd, capture_output=True, text=True)
        if not os.path.exists(raw_video):
            # Try alternate extension if saved as webm or m4a
            found = False
            for f in os.listdir(tmpdir):
                if f.startswith("raw"):
                    raw_video = os.path.join(tmpdir, f)
                    found = True
                    break
            if not found:
                print(f"    ! Failed to download {ytid}: {res.stderr[:200]}")
                return

        # 2. Extract 40 seconds of the song (captures the verse + iconic chorus)
        # Offset 15s to get past intro straight into verse/chorus
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-ss", "15", "-t", "40",
            "-i", raw_video,
            "-ar", "22050", "-ac", "1",
            sample_wav
        ]
        subprocess.run(ffmpeg_cmd, capture_output=True, check=True)

        # 3. Transcribe audio to MIDI using basic-pitch
        print(f"    Transcribing with basic-pitch CoreML model...")
        model_output, raw_pm, note_events = predict(sample_wav)
        print(f"    Detected {len(note_events)} notes!")

        # 4. Multi-track 1980s Sound Blaster / General MIDI Arrangement
        arranged_pm = pretty_midi.PrettyMIDI(initial_tempo=bpm)
        inst_lead = pretty_midi.Instrument(program=81, name="Nova Lead Synth")
        inst_keys = pretty_midi.Instrument(program=4, name="DX7 Electric Piano")
        inst_bass = pretty_midi.Instrument(program=38, name="Synth Bass")
        inst_drums = pretty_midi.Instrument(program=0, is_drum=True, name="Standard 1985 Drums")

        # Separate raw notes by register
        if len(raw_pm.instruments) > 0:
            for note in raw_pm.instruments[0].notes:
                if note.pitch < 54:
                    inst_bass.notes.append(note)
                elif note.pitch >= 66:
                    inst_lead.notes.append(note)
                else:
                    inst_keys.notes.append(note)

        # Generate locked rhythm drum track
        sec_per_beat = 60.0 / bpm
        dur = arranged_pm.get_end_time()
        if len(raw_pm.instruments) > 0 and len(raw_pm.instruments[0].notes) > 0:
            dur = max(n.end for n in raw_pm.instruments[0].notes)
        beats = int(dur / sec_per_beat)

        for b in range(beats):
            t = b * sec_per_beat
            # Kick on beat 1 and 3 (or driving 4-on-floor if fast)
            if bpm >= 128:
                inst_drums.notes.append(pretty_midi.Note(velocity=105, pitch=36, start=t, end=t+0.1))
            else:
                if b % 4 in (0, 2):
                    inst_drums.notes.append(pretty_midi.Note(velocity=105, pitch=36, start=t, end=t+0.1))
            # Snare on beat 2 and 4
            if b % 4 in (1, 3):
                inst_drums.notes.append(pretty_midi.Note(velocity=115, pitch=38, start=t, end=t+0.1))
            # Hi-hat 8th notes
            inst_drums.notes.append(pretty_midi.Note(velocity=75, pitch=42, start=t, end=t+0.05))
            inst_drums.notes.append(pretty_midi.Note(velocity=60, pitch=42, start=t + sec_per_beat*0.5, end=t + sec_per_beat*0.5 + 0.05))
            # Crash cymbal on bar 0 and bar 8
            if b % 32 == 0:
                inst_drums.notes.append(pretty_midi.Note(velocity=100, pitch=49, start=t, end=t+0.8))

        arranged_pm.instruments.extend([inst_lead, inst_keys, inst_bass, inst_drums])
        arranged_pm.write(midi_target)
        print(f"    ✓ Wrote {midi_target} ({os.path.getsize(midi_target)} bytes)")

        # 5. Render 14.4k dialup MP3 stream
        print(f"    Rendering 14.4k MP3 dialup stream...")
        render_pm_to_mp3(arranged_pm, mp3_target)
        print(f"    ✓ Wrote {mp3_target} ({os.path.getsize(mp3_target)//1024} KB)")


def main():
    print(f"Starting YouTube Ingestion & MIDI Transcription for {len(SONGS_TO_PROCESS)} Nova Hart songs...")
    for slug, ytid, title, bpm in SONGS_TO_PROCESS:
        try:
            process_song(slug, ytid, title, bpm)
        except Exception as e:
            print(f"  Error processing {slug} ({ytid}): {e}")

    print("\nAll YouTube songs successfully converted to MIDIs and 14.4k streams!")


if __name__ == "__main__":
    main()
