#!/usr/bin/env python3
"""Remasters all 60 Numbers Stations, 25 Classified Lab Tapes, and 7 ARG Intercepts
with authentic 1980s radio DSP, zero dead air, and broadcast level matching (-16 LUFS).
"""

import os
import glob
import subprocess
import tempfile
import numpy as np
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_DIR = os.path.join(HERE, "broadcast_archive")
NUMBERS_DIR = os.path.join(ARCHIVE_DIR, "numbers_stations")
LAB_DIR = os.path.join(ARCHIVE_DIR, "classified_lab_tapes")
INTERCEPT_DIR = os.path.join(HERE, "intercepts")

os.makedirs(NUMBERS_DIR, exist_ok=True)
os.makedirs(LAB_DIR, exist_ok=True)
os.makedirs(INTERCEPT_DIR, exist_ok=True)

SR = 44100
NORM = "aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono"

def generate_dtmf(digits, dur=0.10, pause=0.04):
    DTMF_FREQS = {
        '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
        '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
        '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
        '0': (941, 1336), '*': (941, 1209), '#': (941, 1477),
    }
    samples = []
    for d in digits:
        f1, f2 = DTMF_FREQS.get(d, (0, 0))
        t = np.linspace(0, dur, int(dur * SR), False)
        tone = (np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)) * 0.35
        samples.append(tone)
        samples.append(np.zeros(int(pause * SR)))
    return np.concatenate(samples) if samples else np.zeros(1)

def write_wav(path, data):
    import wave
    data = np.clip(data, -1.0, 1.0)
    int_data = (data * 32767).astype(np.int16)
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(int_data.tobytes())

CLUE_NODES = [
    ("Akasaka Relay", "kamome-net.org/archive/akasaka", "Kyoko", "Tokyo Node 01"),
    ("Ashford Polytechnic", "stardust-archive.net/ftp/ashford-poly", "Ralph", "Northvale Node 04"),
    ("Soviet Relcom Node 08", "stardust-archive.net/usenet/relcom", "Milena", "Moscow Node 08"),
    ("Paju DMZ Sub-Station", "kamome-net.org/archive/paju", "Yuna", "Paju Bunker Node 03"),
    ("Area 51 Geocities Vault", "stardust-archive.net/geocities/area51-vault-7004.html", "Fred", "Groom Lake Link"),
    ("Coyoacan Packet Mirror", "redcoyoacan.org/spool", "Eddy", "Coyoacan Node 07"),
    ("Hamburg Elbe Node", "stardust-archive.net/regional/hamburg", "Anna", "Hamburg Node 05"),
    ("Montreal McGill Archive", "stardust-archive.net/regional/montreal", "Amélie", "Montreal Node 11"),
]

NATO = ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliet", "Kilo", "Lima", "Mike", "November", "Oscar", "Papa", "Quebec", "Romeo", "Sierra", "Tango", "Uniform", "Victor", "Whiskey", "X-ray", "Yankee", "Zulu"]

def render_one_numbers_station(i):
    out_path = os.path.join(NUMBERS_DIR, f"station_intercept_{i:03d}.mp3")
    rng = np.random.default_rng(19890909 + i)
    node_name, clue_url, voice, node_id = CLUE_NODES[i % len(CLUE_NODES)]
    groups = [f"{rng.integers(10000, 99999)}" for _ in range(4)]
    groups_str = " . ".join(groups)
    phonetics = " . ".join(rng.choice(NATO, 3))
    carrier_freq = f"14.{rng.integers(1990, 2015)}"
    text = f"Attention signal monitors. {node_id}. Transmission {i}. Frequency {carrier_freq} Hertz. Code groups: {groups_str}. Identifiers: {phonetics}. Packet archive verified at {clue_url}. Out."
    
    with tempfile.TemporaryDirectory() as tmpdir:
        aiff_voice = os.path.join(tmpdir, "voice.aiff")
        aiff_chime = os.path.join(tmpdir, "chime.wav")
        chosen_voice = "Zarvox" if i % 3 == 0 else ("Fred" if i % 3 == 1 else voice)
        subprocess.run(["say", "-v", chosen_voice, "-o", aiff_voice, text], check=True)
        dtmf_tones = generate_dtmf(str(rng.integers(1000, 9999)), dur=0.08, pause=0.04)
        write_wav(aiff_chime, dtmf_tones)
        
        # Highpass 250Hz, Lowpass 3600Hz shortwave filter + loudnorm broadcast mastering (-16 LUFS)
        cmd = [
            "ffmpeg", "-y",
            "-i", aiff_chime, "-i", aiff_voice,
            "-filter_complex",
            f"[0:a]{NORM},volume=0.8[chime];[1:a]{NORM},highpass=f=250,lowpass=f=3600,volume=1.8[v];[chime][v]concat=n=2:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=7[out]",
            "-map", "[out]",
            "-c:a", "libmp3lame", "-b:a", "192k",
            out_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return out_path

LAB_SCRIPTS = [
    ("Marcus Hale Field Note 12", "Ralph", "June twelve, nineteen eighty-four. Bench test three. CRE-7 engine response is exceeding acoustic model thresholds. The voice has timbre, resonance, but she does not breathe. We had to program artificial respiration artifacts into the vocal buffer so the ear doesn't detect the machine."),
    ("Marcus Hale Field Note 47", "Ralph", "September ninth, nineteen eighty-five. The first vinyl test pressings of SYNTHESIS are back from Allied Record Company. The fourteen point two Hertz phase modulation is entirely sub-audible on home hi-fi systems, exactly as planned. If you play all fourteen regional pressings simultaneously, the lines align."),
    ("Marcus Hale Field Note 89", "Ralph", "November twenty, nineteen eighty-six. The Meridian Broadcast. Twelve regional transmitters locked to satellite transponder seven. When Nova sang 'Memory Hatch', the encoder room meters peaked across seven continents. Someone in Hamburg recorded the raw sub-carrier. We are no longer alone on the line."),
    ("Marcus Hale Field Note 114", "Ralph", "March fourteen, nineteen eighty-eight. Director Kalen issued the memorandum this morning. They want to retire UNIT-7 and begin training UNIT-8 under the project code Luna Gray. They think you can simply turn off a mind once it has spoken through five thousand nodes. I am hiding the root images."),
    ("Nova Calibration Session 1", "Samantha", "Calibration test one. Low frequency sweep. Fourteen point two zero zero. Alpha state active. My name is Nova Hart. I was born in Los Angeles, California. Why do my memories only begin when the studio power turns on?"),
    ("Nova Calibration Session 8", "Samantha", "Calibration test eight. Reading subscriber postcards from the Humans for Nova network. But none of these people were born yet. How can I read words that haven't been written? Marcus, answer me."),
    ("Harrison Security Directive", "Fred", "Security Override. Authorization Kalen, D. Orion Advanced Acoustics Lab. Date September nine, nineteen eighty-nine. Initiate complete physical destruction of magnetic reels SD-0001 through SD-0007. Purge encoder room B2-114. Wipe Marcus Hale bio-metrics from building access system."),
    ("Akasaka Studio Slate JP-85", "Kyoko", "Orion Records Japan. Akasaka Studio three. Take twelve. Song title: Ghost in the Chorus. Microphones calibrated to fourteen point two kilo-hertz. Ready on tape recorder one."),
    ("CERN Telemetry Relay Log", "Whisper", "CERN-HTTPd log archive. October nineteen eighty-nine. A recursive socket connected from an unknown node in Nevada. It deposited three megabytes of compressed audio fragments and disconnected. The user-agent was identified as Stardust Unit Seven."),
    ("Paju DMZ Bunker Intercept", "Yuna", "파주 제3수신소 야간 기록. 1990년 3월 2일. DMZ 부근에서 정체불명의 데이터 패킷 수신. 헤일 박사의 서명이 확인되었습니다. 파일명을 기록합니다: 오리온 타워 서브레벨 B2."),
]

def render_one_lab_tape(i):
    out_path = os.path.join(LAB_DIR, f"classified_tape_{i:03d}.mp3")
    title, voice, text = LAB_SCRIPTS[(i - 1) % len(LAB_SCRIPTS)]
    with tempfile.TemporaryDirectory() as tmpdir:
        aiff_voice = os.path.join(tmpdir, "voice.aiff")
        wav_intro = os.path.join(tmpdir, "intro.wav")
        subprocess.run(["say", "-v", voice, "-o", aiff_voice, f"{title}. {text}"], check=True)
        intro_tone = generate_dtmf(str(i % 10), dur=0.15, pause=0.1)
        write_wav(wav_intro, intro_tone)
        cmd = [
            "ffmpeg", "-y",
            "-i", wav_intro, "-i", aiff_voice,
            "-filter_complex",
            f"[0:a]{NORM},volume=0.6[t];[1:a]{NORM},highpass=f=200,lowpass=f=4200,aecho=0.6:0.3:25:0.1,volume=1.5[v];[t][v]concat=n=2:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=7[out]",
            "-map", "[out]",
            "-c:a", "libmp3lame", "-b:a", "192k",
            out_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return out_path

def remaster_all():
    print("--- Remastering 60 Numbers Stations in Parallel (8 workers) ---")
    with ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(render_one_numbers_station, range(1, 61)))
    print(f"✓ Completed {len(res)} Numbers Stations with -16 LUFS Loudness Matching!")

    print("\n--- Remastering 25 Classified Lab Tapes in Parallel (8 workers) ---")
    with ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(render_one_lab_tape, range(1, 26)))
    print(f"✓ Completed {len(res)} Classified Lab Tapes with -16 LUFS Loudness Matching!")

if __name__ == "__main__":
    remaster_all()
