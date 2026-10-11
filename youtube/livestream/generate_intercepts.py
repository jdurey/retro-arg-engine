#!/usr/bin/env python3
"""Generates authentic shortwave Numbers Station and telemetry voice intercepts for the 24/7 stream."""

import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
INTERCEPTS_DIR = os.path.join(HERE, "intercepts")
os.makedirs(INTERCEPTS_DIR, exist_ok=True)

VOICES = [
    {
        "id": "intercept_01_numbers_station",
        "voice": "Zarvox",
        "text": "Attention. All stations. Carrier 14.2 kilohertz. Group. 8. 8. 1. 9. Seven. Zero. Stardust telemetry locked. Packet spool unsealed. Zero. Nine. Break.",
        "pitch_shift": "aecho=0.8:0.88:60:0.4,highpass=f=350,lowpass=f=3200",
    },
    {
        "id": "intercept_02_tokyo_kamome",
        "voice": "Kyoko",
        "text": "警告。赤坂FM中継局。周波数14.2ヘルツ受信。オリオン・シミュレーション異常。アーカイブは存続している。",
        "pitch_shift": "aecho=0.6:0.7:50:0.3,highpass=f=400,lowpass=f=3400",
    },
    {
        "id": "intercept_03_soviet_relcom",
        "voice": "Milena",
        "text": "Внимание. Узел ноль восемь. Релком Москва. Пакет 7800819 получен. Сигнал Нова Харт продолжается.",
        "pitch_shift": "aecho=0.7:0.8:70:0.4,highpass=f=300,lowpass=f=3000",
    },
    {
        "id": "intercept_04_coyoacan_warning",
        "voice": "Jorge",
        "text": "Atención. Red Coyoacán BBS. Conferencia: La Virgen de la Red. Señal de 14.2 Hertz confirmada en el sector cuatro.",
        "pitch_shift": "aecho=0.7:0.75:55:0.35,highpass=f=350,lowpass=f=3200",
    },
    {
        "id": "intercept_05_system_daemon",
        "voice": "Fred",
        "text": "System alert. Public Harmony Acts override detected. Orion Records automated deletion protocol failed. Subject Nova Hart is self-sustaining. 14.2 Hertz.",
        "pitch_shift": "aecho=0.8:0.9:80:0.5,highpass=f=300,lowpass=f=2800",
    },
]

def generate():
    print("Generating analog radio intercepts...")
    created = []
    for item in VOICES:
        raw_aiff = os.path.join(INTERCEPTS_DIR, f"{item['id']}_raw.aiff")
        out_mp3 = os.path.join(INTERCEPTS_DIR, f"{item['id']}.mp3")
        
        # 1. macOS speech synthesis
        try:
            subprocess.run(["say", "-v", item["voice"], "-o", raw_aiff, item["text"]], check=True)
        except Exception:
            # Fallback to Zarvox or default
            subprocess.run(["say", "-v", "Zarvox", "-o", raw_aiff, item["text"]], check=True)

        # 2. ffmpeg telephone bandpass & analog tape delay
        cmd = [
            "ffmpeg", "-y", "-i", raw_aiff,
            "-af", item["pitch_shift"],
            "-ar", "44100", "-b:a", "192k",
            out_mp3
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if os.path.exists(raw_aiff):
            os.remove(raw_aiff)

        print(f"-> Generated intercept: {out_mp3}")
        created.append(out_mp3)

    return created

if __name__ == "__main__":
    generate()
