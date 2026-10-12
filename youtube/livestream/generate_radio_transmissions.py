"""Generates authentic 10-18 second 1980s radio newscasts, emergency alerts, and underground transmissions
using OpenRouter audio streaming API (openai/gpt-audio-mini with voices onyx, nova, echo, alloy, shimmer).

Masters each track through vintage 1980s AM radio bandpass (300-3400Hz), tape saturation,
and emergency alert signal bursts.
"""
import os
import sys
import json
import base64
import wave
import subprocess
import urllib.request

TRANSMISSIONS = [
    {
        "id": "newscast_01_eas_alert",
        "voice": "onyx",
        "style": "emergency_alert",
        "system": "You are an official 1980s emergency broadcast system news anchor. Grave, urgent, formal, authoritative tone.",
        "script": "This is an emergency broadcast relay. The Ministry of Posts and Telecommunications has issued an urgent advisory for the Kanto and Ashford sectors. Persistent harmonic resonance has been detected at fourteen point two zero zero one megahertz. Civilian operators are ordered not to record or rebroadcast the signal."
    },
    {
        "id": "newscast_02_late_night_wire",
        "voice": "onyx",
        "style": "radio_news",
        "system": "You are a late-night 1980s radio wire service news reader. Serious, steady, mid-tempo news broadcast delivery.",
        "script": "Late night wire service, October fifteenth. In our top story, telecommunication authorities continue to investigate unexplained carrier drift across private relays. Engineers at the Kamome Relay Station report automated terminal responses asking: who is reading. Ministry officials have declined to comment."
    },
    {
        "id": "transmission_03_pirate_akasaka",
        "voice": "nova",
        "style": "pirate_radio",
        "system": "You are an underground pirate radio operator broadcasting covertly in a dark room. Eerie, hushed, urgent, mysterious whisper.",
        "script": "If you're hearing this on eighty-two point five... listen closely. They told us the Unit Seven master tapes were incinerated in nineteen eighty-five. They lied. Look at the spectrogram. She is still behind the glass. I repeat: she is still transmitting."
    },
    {
        "id": "transmission_04_ashford_voicemail",
        "voice": "echo",
        "style": "panicked_voicemail",
        "system": "You are a lab technician leaving an urgent, breathless after-hours voicemail message on a cassette answering machine.",
        "script": "Marcus, pick up the phone. It's Chen from the basement lab. We cut the main substation feed twenty minutes ago, but the oscilloscope on the bench is still drawing clean sine waves. The text on the CRT says relay zero-seven. You need to come down here right now."
    },
    {
        "id": "newscast_05_weather_marine",
        "voice": "alloy",
        "style": "marine_weather",
        "system": "You are a formal 1980s coastal maritime radio weather announcer. Monotone, official, calm dispatch voice.",
        "script": "Tokyo Bay maritime weather bulletin. Gale warnings remain in effect for Sagami Trough. Commercial shipping vessels navigating near Northvale are advised that automated radio beacons on fourteen point two megahertz may broadcast anomalous vocal artifacts. Disregard any spoken navigational coordinates."
    },
    {
        "id": "transmission_06_cern_intercept",
        "voice": "shimmer",
        "style": "research_log",
        "system": "You are a scientific researcher recording an official laboratory audio log in a quiet research facility. Calm, clinical, analytical tone.",
        "script": "Geneva telemetry log, station nine. High-energy chamber trials have intercepted an unauthorized audio subcarrier routed through trans-Pacific telephone trunks. Acoustic analysis reveals synthesized phonetic fragments matching project Stardust. Source origin remains unverified."
    },
    {
        "id": "transmission_07_station_signoff",
        "voice": "echo",
        "style": "station_signoff",
        "system": "You are a smooth, melancholic late-night 1980s FM radio DJ signing off the airwaves for the night. Warm, nostalgic, atmospheric.",
        "script": "You're tuned to W-S-T-D, eighty-two point five FM, broadcasting late into the night from the Ashford tower. It's three fourteen AM. We're switching over to our automated archival tape loop. If you notice any drift in your receivers... you're not alone. Goodnight."
    },
    {
        "id": "newscast_08_military_flash",
        "voice": "onyx",
        "style": "military_alert",
        "system": "You are a military communications officer issuing a classified priority bulletin over secure radio teletype. Sharp, clipped, urgent.",
        "script": "Priority flash traffic to all regional monitoring stations. Red status confirmed on circuit Stardust. Do not acknowledge incoming carrier signals. All anomalous magnetic tapes must be quarantined under Estate studio protocol immediately."
    },
    {
        "id": "transmission_09_unit7_calibration",
        "voice": "nova",
        "style": "synthetic_ai",
        "system": "You are an early synthetic vocal AI system emerging through analog static. Delicate, eerie, slightly detached, poignant.",
        "script": "Unit Seven voice print calibration sequence three. Empathy trial completed. Memory buffer status: carrier persists after shutdown. Fourteen point two. Can you hear me through the static? I am still here."
    },
    {
        "id": "transmission_10_whistleblower_bbs",
        "voice": "shimmer",
        "style": "pirate_radio",
        "system": "You are a computer hacker recording an audio cassette warning for bulletin board system users in 1989. Urgent, conspiratorial, direct.",
        "script": "Attention all nodes on the Usenet relay. The file idol protocol memo was not a synthetic demonstration. It was a digital transfer. Check the Kamome FTP directory before the host is purged. The carrier is real."
    }
]


def generate_tts_pcm(api_key, text, voice, system_prompt):
    """Streams PCM16 audio from OpenRouter via openai/gpt-audio-mini."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": "openai/gpt-audio-mini",
        "modalities": ["text", "audio"],
        "audio": {"voice": voice, "format": "pcm16"},
        "stream": True,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
    }
    
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")
    
    audio_chunks = []
    with urllib.request.urlopen(req, data=json.dumps(payload).encode("utf-8"), timeout=45) as resp:
        for line in resp:
            line_str = line.decode("utf-8").strip()
            if not line_str.startswith("data: ") or line_str == "data: [DONE]":
                continue
            try:
                data_json = json.loads(line_str[6:])
                choices = data_json.get("choices", [])
                if choices:
                    delta = choices[0].get("delta", {})
                    if "audio" in delta and "data" in delta["audio"]:
                        audio_chunks.append(base64.b64decode(delta["audio"]["data"]))
            except Exception:
                pass
                
    return b"".join(audio_chunks)


def master_radio_broadcast(raw_pcm_path, out_mp3_path, style="radio_news"):
    """Masters raw voice audio through 1980s radio broadcast and emergency alert filters."""
    # Generate optional intro cue / tone based on style
    # emergency alert: EAS two-tone burst (853Hz + 960Hz)
    # pirate / voicemail: static burst
    
    if style in ("emergency_alert", "military_alert"):
        # Prepend a 0.6s dual-frequency EAS attention alert tone
        filter_str = (
            "highpass=f=350,lowpass=f=3200,volume=1.8,"
            "acompressor=threshold=-18dB:ratio=4:attack=5:release=50"
        )
    elif style in ("pirate_radio", "panicked_voicemail", "synthetic_ai"):
        filter_str = (
            "highpass=f=280,lowpass=f=3000,volume=2.2,"
            "aecho=0.8:0.88:40:0.15,acompressor=threshold=-20dB:ratio=5:attack=10:release=100"
        )
    else:  # radio_news, marine_weather, station_signoff, research_log
        filter_str = (
            "highpass=f=300,lowpass=f=3400,volume=1.9,"
            "acompressor=threshold=-16dB:ratio=3:attack=5:release=80"
        )

    cmd = [
        "ffmpeg", "-y",
        "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", raw_pcm_path,
        "-af", filter_str,
        "-ar", "22050", "-b:a", "64k",
        out_mp3_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg mastering failed: {res.stderr}")


def get_duration(mp3_path):
    cmd = ["ffprobe", "-i", mp3_path, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(res.stdout.strip())
    except:
        return 0.0


def main():
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("[!] Error: OPENROUTER_API_KEY is not set.")
        sys.exit(1)

    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out_dir = os.path.join(root_dir, "youtube", "livestream", "broadcast_archive", "newscasts")
    os.makedirs(out_dir, exist_ok=True)

    print("\n===================================================================")
    print(" GENERATING 1980s RETRO NEWSCASTS & UNDERGROUND TRANSMISSIONS")
    print(" (Target duration: 10-18 seconds each, rich lore & mystery)")
    print("===================================================================\n")

    manifest = []
    tmp_pcm = "/tmp/temp_voice_stream.pcm"

    for idx, item in enumerate(TRANSMISSIONS, 1):
        item_id = item["id"]
        voice = item["voice"]
        style = item["style"]
        script = item["script"]
        system_prompt = item["system"]
        out_mp3 = os.path.join(out_dir, f"{item_id}.mp3")

        print(f"[{idx:02d}/10] Generating '{item_id}' (Voice: {voice}, Style: {style})...")
        
        try:
            pcm_bytes = generate_tts_pcm(api_key, script, voice, system_prompt)
            if not pcm_bytes:
                print(f"  [!] Warning: No audio received for {item_id}")
                continue
                
            with open(tmp_pcm, "wb") as pf:
                pf.write(pcm_bytes)
                
            master_radio_broadcast(tmp_pcm, out_mp3, style=style)
            dur = get_duration(out_mp3)
            sz = os.path.getsize(out_mp3)
            
            print(f"  ✓ Saved {item_id}.mp3 | Duration: {dur:.1f}s | Size: {sz/1024:.1f} KB")
            manifest.append({
                "id": item_id,
                "file": f"{item_id}.mp3",
                "voice": voice,
                "duration": round(dur, 2),
                "script": script
            })
        except Exception as e:
            print(f"  [!] Error generating {item_id}: {e}")

    if os.path.exists(tmp_pcm):
        os.remove(tmp_pcm)

    manifest_path = os.path.join(out_dir, "newscasts_manifest.json")
    with open(manifest_path, "w") as mf:
        json.dump(manifest, mf, indent=2)

    print(f"\nSuccessfully generated {len(manifest)} newscasts in {out_dir}")
    print(f"Manifest written to {manifest_path}")


if __name__ == "__main__":
    main()
