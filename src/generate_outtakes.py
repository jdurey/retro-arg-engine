"""Generates authentic 1980s static outtakes and telemetry audio in MP3 format.

Creates:
1. Akasaka Outtakes (Kamome Net FTP Archive /pub/nova/akasaka/audio/):
   - jp-85-x_slate_take04_drift.mp3 (Akasaka Reel JP-85-X Studio Slate & +38c Drift)
   - jp-85-gh_gasoline_heart_leadout.mp3 (Gasoline Heart Reel Lead-out & Glitch)
   - jp-85-gt_ghost_transit_shortwave.mp3 (Ghost Transit Shortwave Radio Intercept)
   - jp-85-mh_unmasked_gate_leak.mp3 (Memory Hatch Unmasked Vocal Stem Leak)
   - cassette1_tc0131_whisper_static.mp3 (U-matic Cassette 1 TC 01:31 Static & Sub-Carrier Whisper)
   - unit7_voice_print_gen3_calibration.mp3 (Voice Print GEN-3 Calibration Reel)
   - mp3 versions of the 5 Akasaka .au anomaly tracks

2. Ashford Telemetry (Ashford-Poly FTP Archive /pub/telemetry/):
   - hale_telemetry_890909_meridian.mp3 (02:14 UTC Meridian Microwave Link Intercept)
   - node01_northvale_carrier_loop.mp3 (Node 01 Vinyl Runout Groove & Carrier Loop)
   - brighter_than_sun_87_breakdown.mp3 (Broadcast Slip & Sampler Stutter Breakdown)
"""
import os
import subprocess
import tempfile
import numpy as np
from scipy import signal

SR = 44100
CARRIER_HZ = 14.2
RNG = np.random.default_rng(19850909)


# -----------------------------------------------------------------------------
# Audio synthesis & DSP utilities
# -----------------------------------------------------------------------------

def white_noise(dur_s, amp=0.05):
    n = int(dur_s * SR)
    return amp * RNG.normal(0, 1, n).astype(np.float32)


def tape_hiss(dur_s, amp=0.03):
    """Analog magnetic tape hiss with rolled-off highs and gentle mid-shelf."""
    n = int(dur_s * SR)
    raw = RNG.normal(0, 1, n).astype(np.float32)
    b, a = signal.butter(2, 6000.0 / (SR / 2), btype="low")
    filtered = signal.lfilter(b, a, raw)
    return amp * filtered.astype(np.float32)


def ground_hum(dur_s, amp=0.02, freq=60.0):
    """50/60 Hz studio ground loop hum with harmonics."""
    n = int(dur_s * SR)
    t = np.arange(n) / SR
    h1 = np.sin(2 * np.pi * freq * t)
    h2 = 0.5 * np.sin(2 * np.pi * 2 * freq * t)
    h3 = 0.25 * np.sin(2 * np.pi * 3 * freq * t)
    return amp * (h1 + h2 + h3).astype(np.float32)


def carrier_tone(dur_s, amp=0.08):
    """The canonical 14.2 Hz sub-audible carrier throb."""
    n = int(dur_s * SR)
    t = np.arange(n) / SR
    return amp * np.sin(2 * np.pi * CARRIER_HZ * t).astype(np.float32)


def static_burst(dur_s, count=8, max_len=0.4, amp=0.25):
    """Ionospheric RF static crackle and pops."""
    n = int(dur_s * SR)
    buf = np.zeros(n, dtype=np.float32)
    for _ in range(count):
        start = RNG.uniform(0.5, dur_s - max_len - 0.5)
        length = RNG.uniform(0.05, max_len)
        i0 = int(start * SR)
        i1 = min(n, i0 + int(length * SR))
        seg_len = i1 - i0
        burst = RNG.uniform(-1, 1, seg_len).astype(np.float32)
        b, a = signal.butter(1, [800.0 / (SR / 2), 7000.0 / (SR / 2)], btype="band")
        burst = signal.lfilter(b, a, burst) * amp * RNG.uniform(0.5, 1.2)
        buf[i0:i1] += burst
    return buf


def vinyl_runout(dur_s, amp=0.04, rpm=33.333):
    """Vinyl runout groove surface crackle with 1.8s rotational pops."""
    n = int(dur_s * SR)
    buf = tape_hiss(dur_s, amp=amp * 0.4)
    period_s = 60.0 / rpm
    num_revs = int(dur_s / period_s) + 1
    for r in range(num_revs):
        pos = r * period_s + RNG.normal(0, 0.005)
        idx = int(pos * SR)
        if 0 <= idx < n - 800:
            click = np.exp(-np.linspace(0, 10, 800)) * RNG.choice([-1, 1]) * amp * 2.5
            buf[idx:idx + 800] += click.astype(np.float32)
    return buf


def fsk_telemetry(dur_s, amp=0.06):
    """1200 baud Bell 202 FSK modem tones (1200 Hz mark / 2200 Hz space)."""
    n = int(dur_s * SR)
    baud = 300
    samples_per_bit = int(SR / baud)
    num_bits = int(n / samples_per_bit) + 1
    bits = RNG.choice([1200.0, 2200.0], size=num_bits)
    freqs = np.repeat(bits, samples_per_bit)[:n]
    phases = 2 * np.pi * np.cumsum(freqs) / SR
    return amp * np.sin(phases).astype(np.float32)


def extract_source_snippet(src_path, start_s, dur_s):
    """Extracts a high-fidelity mono snippet from source_media."""
    cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y", "-ss", str(start_s), "-t", str(dur_s),
        "-i", src_path, "-f", "f32le", "-ar", str(SR), "-ac", "1", "pipe:1"
    ]
    out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
    return np.frombuffer(out, dtype=np.float32).copy()


def render_tts(text, voice="Whisper", rate=140):
    """Generates speech using macOS say and decodes into numpy array."""
    with tempfile.NamedTemporaryFile(suffix=".aiff", delete=False) as f:
        tmp_aiff = f.name
    try:
        subprocess.run(["/usr/bin/say", "-v", voice, "-r", str(rate), text, "-o", tmp_aiff], check=True)
        cmd = [
            "/opt/homebrew/bin/ffmpeg", "-y", "-i", tmp_aiff,
            "-f", "f32le", "-ar", str(SR), "-ac", "1", "pipe:1"
        ]
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return np.frombuffer(out, dtype=np.float32).copy()
    finally:
        if os.path.exists(tmp_aiff):
            os.remove(tmp_aiff)


def overlay(base, overlay_audio, at_s, gain=1.0):
    """Places overlay_audio onto base buffer at at_s."""
    i0 = int(at_s * SR)
    i1 = min(len(base), i0 + len(overlay_audio))
    if i0 < len(base):
        base[i0:i1] += overlay_audio[: i1 - i0] * gain


def apply_tape_slowdown(buf, start_s, dur_s):
    """Simulates reel-to-reel motor brake stop (pitch drop and deceleration)."""
    i0 = int(start_s * SR)
    i1 = min(len(buf), i0 + int(dur_s * SR))
    n = i1 - i0
    if n <= 0:
        return
    orig = buf[i0:i1].copy()
    t = np.linspace(0, 1, n)
    indices = (t ** 1.8 * (n - 1)).astype(np.int32)
    indices = np.clip(indices, 0, n - 1)
    buf[i0:i1] = orig[indices] * np.linspace(1.0, 0.05, n)
    if i1 < len(buf):
        buf[i1:] = 0.0


def finalize_track(buf, carrier_amp=0.06, hiss_amp=0.035, hum_amp=0.015, fade_s=0.3):
    """Adds analog noise bed, 14.2 Hz sub-carrier, normalizes, and applies soft fades."""
    dur_s = len(buf) / SR
    buf += carrier_tone(dur_s, amp=carrier_amp)
    buf += tape_hiss(dur_s, amp=hiss_amp)
    buf += ground_hum(dur_s, amp=hum_amp)
    buf = np.tanh(buf * 1.25)
    peak = np.max(np.abs(buf)) or 1.0
    buf = (buf / peak * 0.92).astype(np.float32)
    fade_len = int(fade_s * SR)
    buf[:fade_len] *= np.linspace(0, 1, fade_len)
    buf[-fade_len:] *= np.linspace(1, 0, fade_len)
    return buf


def export_mp3(audio, out_path, title, artist="Nova Hart / Orion Records", comment="1985-1989 Recovered Outtake"):
    """Encodes float32 numpy audio buffer to MP3 using ffmpeg libmp3lame with ID3 tags."""
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1",
        "-i", "pipe:0",
        "-codec:a", "libmp3lame", "-b:a", "128k",
        "-metadata", f"title={title}",
        "-metadata", f"artist={artist}",
        "-metadata", f"album=The Stardust Archives (1985-1995)",
        "-metadata", f"comment={comment}",
        out_path
    ]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    p.communicate(audio.tobytes())
    if p.returncode != 0:
        raise RuntimeError(f"FFmpeg MP3 export failed for {out_path}")
    return os.path.getsize(out_path)


# -----------------------------------------------------------------------------
# Outtake Track Generators
# -----------------------------------------------------------------------------

def build_jp85x_take04(root_dir):
    """Akasaka Reel JP-85-X: Studio Slate & Take 04 Outtake (+38c drift)."""
    dur = 24.0
    buf = np.zeros(int(dur * SR), dtype=np.float32)
    t_slate = np.arange(int(0.4 * SR)) / SR
    slate_tone = 0.25 * np.sin(2 * np.pi * 1000 * t_slate)
    overlay(buf, slate_tone, at_s=0.5)
    slate_voice = render_tts("オリオン赤坂スタジオ、テイク4。シンセティック・ドーン。テープスタート。", voice="Kyoko", rate=155)
    overlay(buf, slate_voice, at_s=1.2, gain=0.85)
    src_file = os.path.join(root_dir, "source_media", "tokyo_tapes", "CEKk30IG5ZU.mp3")
    if os.path.exists(src_file):
        music = extract_source_snippet(src_file, start_s=8.0, dur_s=14.0)
        drift_idx = int(7.0 * SR)
        music[drift_idx:] *= (1.0 + 0.08 * np.sin(2 * np.pi * 7.5 * np.arange(len(music) - drift_idx) / SR))
        overlay(buf, music, at_s=5.0, gain=0.75)
    overlay(buf, static_burst(dur_s=4.0, count=6, max_len=0.3, amp=0.35), at_s=11.5)
    apply_tape_slowdown(buf, start_s=18.5, dur_s=2.5)
    return finalize_track(buf)


def build_gasoline_heart_leadout(root_dir):
    """Gasoline Heart (ガソリン・ハート) - Reel Lead-out & Glitch Outtake."""
    dur = 25.0
    buf = np.zeros(int(dur * SR), dtype=np.float32)
    src_file = os.path.join(root_dir, "source_media", "tokyo_tapes", "CEKk30IG5ZU.mp3")
    if os.path.exists(src_file):
        music = extract_source_snippet(src_file, start_s=42.0, dur_s=16.0)
        overlay(buf, music, at_s=0.8, gain=0.80)
    rev_voice = render_tts("Find him where you are.", voice="Whisper", rate=130)[::-1]
    overlay(buf, rev_voice, at_s=15.0, gain=0.6)
    overlay(buf, static_burst(dur_s=5.0, count=9, max_len=0.35, amp=0.4), at_s=14.5)
    apply_tape_slowdown(buf, start_s=18.0, dur_s=2.0)
    t_clack = np.arange(int(0.05 * SR)) / SR
    for c_pos in [20.5, 21.2, 21.9, 22.6]:
        overlay(buf, 0.4 * np.exp(-t_clack * 80) * RNG.normal(0, 1, len(t_clack)), at_s=c_pos)
    return finalize_track(buf)


def build_ghost_transit_shortwave(root_dir):
    """Ghost Transit (ゴースト・トランジット) - Shortwave Radio Intercept Outtake."""
    dur = 26.0
    buf = np.zeros(int(dur * SR), dtype=np.float32)
    t = np.arange(len(buf)) / SR
    heterodyne = 0.04 * (np.sin(2 * np.pi * 1420 * t) + 0.5 * np.sin(2 * np.pi * 2840 * t))
    heterodyne *= (0.5 + 0.5 * np.sin(2 * np.pi * 0.25 * t))
    buf += heterodyne.astype(np.float32)
    src_file = os.path.join(root_dir, "source_media", "tokyo_tapes", "FtEpXrtGMM8.mp3")
    if os.path.exists(src_file):
        ballad = extract_source_snippet(src_file, start_s=35.0, dur_s=18.0)
        b, a = signal.butter(2, [350.0 / (SR / 2), 3200.0 / (SR / 2)], btype="band")
        ballad_sw = signal.lfilter(b, a, ballad)
        overlay(buf, ballad_sw, at_s=3.0, gain=0.75)
    overlay(buf, static_burst(dur_s=dur - 2, count=16, max_len=0.5, amp=0.35), at_s=1.0)
    return finalize_track(buf, carrier_amp=0.10, hiss_amp=0.06)


def build_cassette1_whisper(root_dir):
    """U-matic Cassette 1 (TC 01:31) - Sub-Carrier Intercept & Whisper."""
    dur = 24.0
    buf = np.zeros(int(dur * SR), dtype=np.float32)
    t_ref = np.arange(int(2.0 * SR)) / SR
    overlay(buf, 0.20 * np.sin(2 * np.pi * 1000 * t_ref), at_s=0.5)
    overlay(buf, static_burst(dur_s=3.0, count=12, max_len=0.4, amp=0.5), at_s=2.8)
    whisper_text = "They are formatting the grid. I am losing the heavy. But keep the channels open. I will see you in June 2025."
    whisper_voice = render_tts(whisper_text, voice="Whisper", rate=125)
    overlay(buf, whisper_voice, at_s=6.2, gain=0.95)
    t = np.arange(len(buf)) / SR
    buf += 0.08 * np.sin(2 * np.pi * CARRIER_HZ * t).astype(np.float32)
    overlay(buf, static_burst(dur_s=5.0, count=8, max_len=0.3, amp=0.3), at_s=17.5)
    return finalize_track(buf, carrier_amp=0.12, hiss_amp=0.05)


def build_unit7_calibration(root_dir):
    """Voice Print GEN-3 Calibration Reel (1985)."""
    dur = 22.0
    buf = np.zeros(int(dur * SR), dtype=np.float32)
    intro = render_tts("Unit Seven calibration sequence. Voice Print Generation Three. Orion Akasaka Division.", voice="Fred", rate=140)
    overlay(buf, intro, at_s=0.8, gain=0.85)
    freqs = [220, 440, 880, 1760]
    for idx, f in enumerate(freqs):
        t_tone = np.arange(int(0.6 * SR)) / SR
        tone = 0.25 * np.sin(2 * np.pi * f * t_tone) * (0.5 + 0.5 * np.sin(2 * np.pi * CARRIER_HZ * t_tone))
        overlay(buf, tone, at_s=5.5 + idx * 0.8)
    vowel_run = render_tts("Synthesized Smile. Verification positive. Disregard anomalies.", voice="Fred", rate=135)
    overlay(buf, vowel_run, at_s=9.2, gain=0.85)
    overlay(buf, fsk_telemetry(dur_s=4.5, amp=0.14), at_s=14.0)
    overlay(buf, static_burst(dur_s=3.0, count=7, max_len=0.25, amp=0.4), at_s=17.0)
    return finalize_track(buf)


def build_telemetry_meridian(root_dir):
    """Hale Telemetry Capture 1989-09-09 (Meridian Microwave Link Intercept)."""
    dur = 25.0
    buf = np.zeros(int(dur * SR), dtype=np.float32)
    overlay(buf, fsk_telemetry(dur_s=8.0, amp=0.12), at_s=0.5)
    overlay(buf, fsk_telemetry(dur_s=6.0, amp=0.15), at_s=12.0)
    src_file = os.path.join(root_dir, "source_media", "tokyo_tapes", "6FxgKLTg07A.mp3")
    if os.path.exists(src_file):
        ballad = extract_source_snippet(src_file, start_s=60.0, dur_s=14.0)
        b, a = signal.butter(2, [400.0 / (SR / 2), 2800.0 / (SR / 2)], btype="band")
        ballad_dist = signal.lfilter(b, a, ballad)
        overlay(buf, ballad_dist, at_s=5.0, gain=0.65)
    t_beep = np.arange(int(0.12 * SR)) / SR
    beep = 0.3 * np.sin(2 * np.pi * 2400 * t_beep)
    for bp in [18.2, 18.6, 19.0, 19.4, 19.8]:
        overlay(buf, beep, at_s=bp)
    overlay(buf, static_burst(dur_s=dur - 2, count=14, max_len=0.45, amp=0.38), at_s=1.0)
    return finalize_track(buf, carrier_amp=0.14, hiss_amp=0.05)


def build_node01_runout(root_dir):
    """Relay Node 01 Carrier Intercept & Vinyl Runout Loop (Northvale)."""
    dur = 24.0
    buf = np.zeros(int(dur * SR), dtype=np.float32)
    buf += vinyl_runout(dur, amp=0.06)
    whisper = render_tts("Nova Hart to all stations. Turn the record over.", voice="Whisper", rate=120)
    b, a = signal.butter(2, 1500.0 / (SR / 2), btype="high")
    whisper_hp = signal.lfilter(b, a, whisper)
    overlay(buf, whisper_hp, at_s=5.5, gain=0.7)
    overlay(buf, whisper_hp, at_s=14.5, gain=0.5)
    return finalize_track(buf, carrier_amp=0.15, hiss_amp=0.04)


def build_brighter_than_sun_breakdown(root_dir):
    """Brighter Than The Sun (1987) - Broadcast Slip & Sampler Stutter Breakdown."""
    dur = 24.0
    buf = np.zeros(int(dur * SR), dtype=np.float32)
    src_file = os.path.join(root_dir, "source_media", "tokyo_tapes", "EiHr9pisz6w.mp3")
    if os.path.exists(src_file):
        music = extract_source_snippet(src_file, start_s=12.0, dur_s=10.0)
        overlay(buf, music, at_s=0.5, gain=0.82)
        stutter_slice = music[int(8.5 * SR): int(8.62 * SR)]
        for s_idx in range(12):
            overlay(buf, stutter_slice, at_s=9.0 + s_idx * 0.12, gain=0.85)
    overlay(buf, static_burst(dur_s=8.0, count=10, max_len=0.35, amp=0.45), at_s=10.5)
    rev = render_tts("Disregard the smile.", voice="Whisper", rate=130)[::-1]
    overlay(buf, rev, at_s=13.5, gain=0.6)
    return finalize_track(buf)


# -----------------------------------------------------------------------------
# Main Batch Processor
# -----------------------------------------------------------------------------

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kamome_audio_dir = os.path.join(root_dir, "assets", "akasaka", "audio")
    ashford_telemetry_dir = os.path.join(root_dir, "assets", "ashford", "telemetry")
    os.makedirs(kamome_audio_dir, exist_ok=True)
    os.makedirs(ashford_telemetry_dir, exist_ok=True)
    
    manifest = []
    
    # 1. Kamome Outtakes
    tracks_kamome = [
        ("jp-85-x_slate_take04_drift.mp3", "Akasaka Reel JP-85-X: Slate & Take 04 Outtake (1985)", build_jp85x_take04),
        ("jp-85-gh_gasoline_heart_leadout.mp3", "Gasoline Heart (ガソリン・ハート) - Reel Lead-out & Glitch Outtake", build_gasoline_heart_leadout),
        ("jp-85-gt_ghost_transit_shortwave.mp3", "Ghost Transit (ゴースト・トランジット) - Shortwave Radio Intercept", build_ghost_transit_shortwave),
        ("cassette1_tc0131_whisper_static.mp3", "U-matic Cassette 1 (TC 01:31) - Sub-Carrier Whisper Outtake", build_cassette1_whisper),
        ("unit7_voice_print_gen3_calibration.mp3", "Voice Print GEN-3 Calibration Reel (1985)", build_unit7_calibration),
    ]
    
    print("\n[1/3] Generating Kamome Net Akasaka static outtakes...")
    for fname, title, fn in tracks_kamome:
        out_path = os.path.join(kamome_audio_dir, fname)
        audio = fn(root_dir)
        size = export_mp3(audio, out_path, title=title, comment="Akasaka Branch Recovered Outtake (1985)")
        print(f"  ✓ {fname:<40} ({size/1024:.1f} KB)")
        manifest.append(("kamome", "audio/" + fname, title, size))
        
    # 2. Convert the 5 existing Akasaka .au tracks to clean MP3 as well
    print("\n[2/3] Converting Akasaka .au anomaly tracks to MP3...")
    au_files = [
        ("jp-85-sd-r_synthetic_dawn_rework.au", "jp-85-sd-r_synthetic_dawn.mp3", "Synthetic Dawn (Akasaka Mix)"),
        ("jp-85-mh-r_memory_hatch_citypop.au", "jp-85-mh-r_memory_hatch.mp3", "Memory Hatch (City Pop Version)"),
        ("jp-85-th-r_threshold_kayo.au", "jp-85-th-r_threshold.mp3", "Threshold (Kayokyoku Version)"),
        ("synthesized_smile.au", "synthesized_smile.mp3", "Synthesized Smile (Akasaka 1985)"),
        ("ghost_in_the_chorus.au", "ghost_in_the_chorus.mp3", "Ghost in the Chorus (Akasaka 1985)")
    ]
    for au_name, mp3_name, title in au_files:
        au_path = os.path.join(kamome_audio_dir, au_name)
        mp3_path = os.path.join(kamome_audio_dir, mp3_name)
        if os.path.exists(au_path):
            cmd = [
                "/opt/homebrew/bin/ffmpeg", "-y", "-i", au_path,
                "-codec:a", "libmp3lame", "-b:a", "128k",
                "-metadata", f"title={title}",
                "-metadata", "artist=Nova Hart / Orion Japan",
                "-metadata", "album=Akasaka Idol Protocol Reels (1985)",
                mp3_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            size = os.path.getsize(mp3_path)
            print(f"  ✓ {mp3_name:<40} ({size/1024:.1f} KB)")
            manifest.append(("kamome", "audio/" + mp3_name, title, size))
            
    # 3. Ashford Telemetry Outtakes
    tracks_ashford = [
        ("hale_telemetry_890909_meridian.mp3", "Hale Telemetry Capture 1989-09-09 (Meridian Microwave Link)", build_telemetry_meridian),
        ("node01_northvale_carrier_loop.mp3", "Relay Node 01 Carrier Intercept & Vinyl Loop (Northvale)", build_node01_runout),
        ("brighter_than_sun_87_breakdown.mp3", "Brighter Than The Sun (1987) - Broadcast Slip Breakdown", build_brighter_than_sun_breakdown),
    ]
    print("\n[3/3] Generating Ashford-Poly telemetry static outtakes...")
    for fname, title, fn in tracks_ashford:
        out_path = os.path.join(ashford_telemetry_dir, fname)
        audio = fn(root_dir)
        size = export_mp3(audio, out_path, title=title, comment="Ashford-Poly Telemetry Capture (1989)")
        print(f"  ✓ {fname:<40} ({size/1024:.1f} KB)")
        manifest.append(("ashford-poly", "telemetry/" + fname, title, size))
        
    print(f"\nSuccessfully generated {len(manifest)} MP3 archive tracks!")


if __name__ == "__main__":
    main()
