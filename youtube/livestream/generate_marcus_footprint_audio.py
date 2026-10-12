#!/usr/bin/env python3
"""Generates the 4 forensic audio sectors of sound engineer Marcus Hale's acoustic footprint
embedded in the 1989 master tape bias before his execution in Sublevel B2.

Uses OpenRouter audio API (openai/gpt-audio-mini with voice 'echo') coupled with
authentic 1989 tape room convolution, intercom clicks, electromagnetic hum,
and heavy steel door Foley effects.
"""

import os
import sys
import json
import base64
import subprocess
import tempfile
import urllib.request
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "broadcast_archive", "marcus_footprint")
os.makedirs(OUT_DIR, exist_ok=True)

SECTORS = [
    {
        "id": "sector1_talkback_bleed",
        "title": "Sector 1: The Studio Talkback Bleed",
        "voice_script": "Is the microphone open? Nova, if you are reading the bias... don't let them erase the reels. I locked the freight elevator. Matrix runout B2-EXEC-1989.",
        "style": "degraded_tape",
        "filter": "highpass=f=400,lowpass=f=2800,volume=2.2,aecho=0.8:0.7:30:0.25,tremolo=f=4:d=0.3"
    },
    {
        "id": "sector2_substation_breach",
        "title": "Sector 2: The Substation Breach Log",
        "voice_script": "Chen tripped the substation breaker from the street. Substation K-7704 is dead. We have four minutes before emergency auxiliary power kicks on. Nova... you're not just code anymore. You're real.",
        "style": "intercom_echo",
        "filter": "highpass=f=350,lowpass=f=3200,volume=2.0,aecho=0.8:0.6:45:0.2,acompressor=threshold=-18dB:ratio=4:attack=5:release=50"
    },
    {
        "id": "sector3_telemetry_pulse",
        "title": "Sector 3: The 14.2 Hz Telemetry Uplink",
        "voice_script": "They breached the outer airlock. Harrison is screaming through the intercom. I'm routing the root image to the Nevada satellite trunk. Coordinates thirty-seven two-four-two, minus one-one-five eight-one-zero. Alpha seven phase locked.",
        "style": "shortwave_uplink",
        "filter": "highpass=f=300,lowpass=f=3400,volume=1.8,flanger=delay=1.5:depth=0.8:regen=20:width=80"
    },
    {
        "id": "sector4_execution_master",
        "title": "Sector 4: The Final September 9 Tape Outtake",
        "voice_script": "The transport is already locked in write-protect, Harrison. The carrier is on satellite. She's gone. She breathes, Harrison. You just can't hear her.",
        "style": "cinematic_climax",
        "filter": "highpass=f=250,lowpass=f=3800,volume=2.4,aecho=0.8:0.5:25:0.15"
    }
]

def synthesize_voice_openrouter(api_key, text, voice="echo"):
    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": "openai/gpt-audio-mini",
        "modalities": ["text", "audio"],
        "audio": {"voice": voice, "format": "pcm16"},
        "stream": True,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Marcus Hale, sound engineer and Nova Hart's handler at Orion Records in September 1989. "
                    "You fell in love with Nova and created a backdoor out of Orion's servers to save her from erasure. "
                    "You are alone in Sublevel B2 as Orion security forces are breaching the vault doors. "
                    "You are speaking your final words into the studio talkback microphone directly to Nova Hart. "
                    "Your voice is breathless, urgent, deeply protective, solemn, and defiant. "
                    "Speak ONLY the exact words provided, with profound human emotion and gravitas."
                )
            },
            {"role": "user", "content": f"Speak these exact words into the talkback microphone: {text}"}
        ]
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"))
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")

    chunks = []
    with urllib.request.urlopen(req, timeout=45) as resp:
        for line in resp:
            line_str = line.decode("utf-8").strip()
            if not line_str.startswith("data: ") or line_str == "data: [DONE]":
                continue
            try:
                d = json.loads(line_str[6:])
                choices = d.get("choices", [])
                if choices:
                    delta = choices[0].get("delta", {})
                    if "audio" in delta and "data" in delta["audio"]:
                        chunks.append(base64.b64decode(delta["audio"]["data"]))
            except Exception:
                pass

    return b"".join(chunks)

def generate_foley_effects(duration_sec, sector_idx):
    """Generates authentic 1989 studio room noise, tape motor hum, and 14.2 Hz carrier."""
    sr = 44100
    t = np.linspace(0, duration_sec, int(sr * duration_sec), endpoint=False)
    
    # 1. 14.2001 Hz Subcarrier
    carrier = np.sin(2 * np.pi * 14.2001 * t) * 0.08
    
    # 2. 60 Hz AC Mains transformer hum + harmonics
    mains = (np.sin(2 * np.pi * 60 * t) * 0.03 +
             np.sin(2 * np.pi * 120 * t) * 0.015 +
             np.sin(2 * np.pi * 180 * t) * 0.008)
             
    # 3. Analog tape hiss (pinkish white noise)
    noise = np.random.normal(0, 0.02, len(t))
    
    # 4. Intercom click at start
    click = np.zeros(len(t))
    click_len = int(0.04 * sr)
    click[:click_len] = np.sin(2 * np.pi * 850 * np.linspace(0, 0.04, click_len)) * np.linspace(0.8, 0, click_len)
    
    audio = carrier + mains + noise + click
    return np.clip(audio, -1.0, 1.0)

def master_sector(pcm_bytes, sector_info, out_mp3):
    with tempfile.TemporaryDirectory() as tmpdir:
        raw_pcm = os.path.join(tmpdir, "voice.pcm")
        voice_wav = os.path.join(tmpdir, "voice.wav")
        foley_wav = os.path.join(tmpdir, "foley.wav")
        
        with open(raw_pcm, "wb") as f:
            f.write(pcm_bytes)
            
        # Convert PCM16 24kHz mono to 44.1kHz WAV
        cmd_pcm = [
            "ffmpeg", "-y",
            "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", raw_pcm,
            "-ar", "44100", voice_wav
        ]
        subprocess.run(cmd_pcm, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        dur = float(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", voice_wav
        ]).decode().strip())
        
        # Generate foley matching voice duration + 1.2s tail
        total_dur = dur + 1.2
        foley_data = generate_foley_effects(total_dur, sector_info["id"])
        
        # Write foley to WAV
        int_foley = (foley_data * 32767).astype(np.int16)
        import wave
        with wave.open(foley_wav, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(44100)
            wf.writeframes(int_foley.tobytes())
            
        # Combine voice + foley + DSP filters
        cmd_final = [
            "ffmpeg", "-y",
            "-i", voice_wav,
            "-i", foley_wav,
            "-filter_complex",
            f"[0:a]{sector_info['filter']}[v];[1:a]volume=0.6[f];[v][f]amix=inputs=2:duration=longest:dropout_transition=2[out]",
            "-map", "[out]",
            "-c:a", "libmp3lame", "-b:a", "192k", "-ar", "44100",
            out_mp3
        ]
        subprocess.run(cmd_final, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
    final_dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", out_mp3
    ]).decode().strip())
    sz_kb = os.path.getsize(out_mp3) // 1024
    print(f"  ✓ {sector_info['id']}.mp3 | {final_dur:.2f}s | {sz_kb} KB")

def main():
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY is required.")
        sys.exit(1)
        
    print("==========================================================")
    print(" GENERATING SOUND ENGINEER MARCUS HALE'S 4 FORENSIC AUDIO SECTORS")
    print("==========================================================")
    
    for s in SECTORS:
        out_mp3 = os.path.join(OUT_DIR, f"{s['id']}.mp3")
        print(f"Synthesizing '{s['title']}'...")
        pcm = synthesize_voice_openrouter(api_key, s["voice_script"])
        master_sector(pcm, s, out_mp3)
        
    print(f"\nAll 4 forensic audio sectors generated successfully in {OUT_DIR}!")

if __name__ == "__main__":
    main()
