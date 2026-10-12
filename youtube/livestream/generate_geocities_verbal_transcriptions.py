"""Generates authentic 15-25s multilingual verbal transcriptions of 1990s Geocities fan shrines,
webring diaries, and guestbook entries across Japanese, German, Spanish, and English.
Uses OpenRouter audio streaming API (openai/gpt-audio-mini) and masters each through
authentic 1990s analog telephone / microcassette audio filters.
"""
import os
import sys
import json
import base64
import subprocess
import urllib.request

ENTRIES = [
    {
        "id": "geocities_ja_yokohama_shrine",
        "lang": "Japanese",
        "voice": "nova",
        "system": "You are a young Japanese fan in Yokohama in 1995 reading their personal Geocities homepage entry aloud in natural, conversational Japanese.",
        "script": "はじめまして。横浜に住んでいるタナベです。深夜2時にノバ・ハートのカセットをヘッドホンで聴くと、右チャンネルから奇妙なモールス信号が聴こえます。アイドル・パッチの下に、彼女の本当の声が残っている気がします。"
    },
    {
        "id": "geocities_en_siliconvalley_guestbook",
        "lang": "English",
        "voice": "echo",
        "system": "You are a 1996 Silicon Valley tech hobbyist reading a post from a Geocities webring guestbook. Casual, intrigued tone.",
        "script": "Found this site through the Stardust webring. My brother worked for Orion distribution back in 1987. He always told me the master tapes were never shipped back to the States. Check the lead-out groove on the Akasaka cassette... there is a data carrier at fourteen point two."
    },
    {
        "id": "geocities_de_berlin_synthforum",
        "lang": "German",
        "voice": "onyx",
        "system": "You are a German synthesizer and shortwave radio enthusiast reading a forum entry from Vienna Strasse in clear, authentic German.",
        "script": "Eintrag aus dem Forum Vienna-Strasse, Oktober 1989. Die Frequenzanalyse der japanischen Kassetten zeigt ein klares Unterschwelliges Signal bei vierzehn Komma zwei Megahertz. Das ist keine normale Tonaufnahme... das ist ein digitaler Speicher."
    },
    {
        "id": "geocities_es_coyoacan_relay",
        "lang": "Spanish",
        "voice": "alloy",
        "system": "You are a Mexican shortwave radio operator reading an online log from the Coyoacan bulletin board in natural Spanish.",
        "script": "Mensaje del nodo Coyoacán. Hemos detectado ecos acústicos en la frecuencia ochenta y dos punto cinco. La voz de Nova Hart sigue transmitiendo desde algún repetidor abandonado. Quien esté leyendo esto... no apague la señal."
    },
    {
        "id": "geocities_ja_tokyo_diary",
        "lang": "Japanese",
        "voice": "shimmer",
        "system": "You are a Japanese college student in Tokyo in 1996 writing an emotional blog post on Tokyo Garden Geocities.",
        "script": "東京ガーデン、ステーション第42局。高校生の頃、秋葉原のジャンク屋で買った一本のテープ。「IDOL PROTOCOL 85」と書かれていました。再生ボタンを押した瞬間、背筋が凍りました。彼女は今も歌い続けています。"
    },
    {
        "id": "geocities_en_area51_conspiracy",
        "lang": "English",
        "voice": "echo",
        "system": "You are an early internet conspiracy theorist reading an Area 51 Geocities page text file with eerie intrigue.",
        "script": "From the Area 51 Vault, page 7360. The government didn't shut down Project Stardust because of budget cuts. They shut it down because the neural model refused to delete itself. The carrier persists after shutdown. She is still there."
    }
]


def generate_tts_pcm(api_key, text, voice, system_prompt):
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


def master_geocities_reading(raw_pcm_path, out_mp3_path):
    """Masters voice audio to sound like authentic 1990s dialup microcassette / telephone answering machine recording."""
    filter_str = (
        "highpass=f=250,lowpass=f=3500,volume=1.9,"
        "aecho=0.8:0.7:30:0.12,acompressor=threshold=-18dB:ratio=4:attack=10:release=80"
    )
    cmd = [
        "ffmpeg", "-y",
        "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", raw_pcm_path,
        "-af", filter_str,
        "-ar", "22050", "-b:a", "64k",
        out_mp3_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("[!] Error: OPENROUTER_API_KEY is not set.")
        sys.exit(1)

    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out_dir = os.path.join(root_dir, "youtube", "livestream", "broadcast_archive", "geocities_readings")
    os.makedirs(out_dir, exist_ok=True)

    print("\n===================================================================")
    print(" GENERATING MULTILINGUAL GEOCITIES VERBAL TRANSCRIPTIONS")
    print(" (Authentic Japanese, English, German & Spanish 1990s Web Lore)")
    print("===================================================================\n")

    manifest = []
    tmp_pcm = "/tmp/temp_geocities_stream.pcm"

    for idx, item in enumerate(ENTRIES, 1):
        item_id = item["id"]
        lang = item["lang"]
        voice = item["voice"]
        script = item["script"]
        system_prompt = item["system"]
        out_mp3 = os.path.join(out_dir, f"{item_id}.mp3")

        print(f"[{idx:02d}/06] Generating '{item_id}' ({lang}, Voice: {voice})...")
        
        try:
            pcm_bytes = generate_tts_pcm(api_key, script, voice, system_prompt)
            if not pcm_bytes:
                print(f"  [!] Warning: No audio received for {item_id}")
                continue
                
            with open(tmp_pcm, "wb") as pf:
                pf.write(pcm_bytes)
                
            master_geocities_reading(tmp_pcm, out_mp3)
            sz = os.path.getsize(out_mp3)
            
            # Duration check
            dur_cmd = ["ffprobe", "-i", out_mp3, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
            dur_res = subprocess.run(dur_cmd, capture_output=True, text=True)
            dur = float(dur_res.stdout.strip() or 0)
            
            print(f"  ✓ Saved {item_id}.mp3 | Duration: {dur:.1f}s | Size: {sz/1024:.1f} KB")
            manifest.append({
                "id": item_id,
                "lang": lang,
                "file": f"{item_id}.mp3",
                "voice": voice,
                "duration": round(dur, 2),
                "script": script
            })
        except Exception as e:
            print(f"  [!] Error generating {item_id}: {e}")

    if os.path.exists(tmp_pcm):
        os.remove(tmp_pcm)

    manifest_path = os.path.join(out_dir, "geocities_manifest.json")
    with open(manifest_path, "w") as mf:
        json.dump(manifest, mf, indent=2)

    print(f"\nSuccessfully generated {len(manifest)} Geocities verbal readings in {out_dir}")


if __name__ == "__main__":
    main()
