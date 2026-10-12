#!/usr/bin/env python3
"""Generates 12 additional multilingual radio bulletins across Mandarin, Cantonese,
Swedish, Norwegian, Danish, Finnish, Greek, Turkish, Arabic, Hindi, and Indonesian.
"""
import os
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "broadcast_archive", "multilingual_bulletins")
os.makedirs(OUT_DIR, exist_ok=True)

ADDITIONAL = [
    ("zh_01_beijing_radio", "Tingting", "这里是中央人民广播电台，现在是午夜十二点。十四点二兆赫遥测信标运行正常。"),
    ("zh_02_taipei_pirate", "Meijia", "台北短波觀測站報告，夜間大氣電離層穩定，捕捉到微弱的八十年代類比音訊信號。"),
    ("yue_01_hongkong_marine", "Sinji", "香港水警及海事廣播，維多利亞港夜間航行通告，請注意十四點二兆赫載波信號。"),
    ("sv_01_stockholm_kustradio", "Alva", "Stockholm kustradio, nattlig telemetri. Frekvens fjorton komma två megahertz är öppen för mottagning."),
    ("nb_01_oslo_natt", "Nora", "Oslo nattkringkasting. Rapport fra lytteposten: bæresignalet fra Stardust er fortsatt aktivt over Nordsjøen."),
    ("da_01_kobenhavn_fm", "Sara", "Danmarks Radio, København natudsendelse. Vi overvåger kortbølgefrekvenserne i Kattegat på fjorten komma to."),
    ("fi_01_helsinki_yo", "Satu", "Helsingin rannikkoradio. Yölähetys taajuudella neljätoista pilkku kaksi megahertsiä. Signaali on vakaa."),
    ("el_01_athens_shortwave", "Melina", "Ελληνική Ραδιοφωνία, νυχτερινή εκπομπή από την Αθήνα. Το υποηχητικό σήμα των δεκατεσσάρων κόμμα δύο μένει ενεργό."),
    ("tr_01_istanbul_gece", "Yelda", "İstanbul gece bülteni. Boğaz hattındaki telsiz istasyonları on dört nokta iki frekansındaki sinyali doğrulamaktadır."),
    ("ar_01_cairo_shortwave", "Majed", "هنا إذاعة القاهرة للموجات القصيرة. البث الليلي مستمر عبر التردد أربعة عشر فاصل اثنين."),
    ("hi_01_delhi_all_india", "Lekha", "यह आकाशवाणी का दिल्ली केंद्र है। रात्रि प्रसारण में चौदह दशमलव दो मेगाहर्ट्ज़ पर वाहक संकेत दर्ज किया गया है।"),
    ("id_01_jakarta_maritim", "Damayanti", "Radio Republik Indonesia, siaran malam Jakarta. Frekuensi telemetri empat belas koma dua terpantau stabil."),
]

def process(slug, voice, text):
    out_mp3 = os.path.join(OUT_DIR, f"{slug}.mp3")
    with tempfile.TemporaryDirectory() as tmpdir:
        voice_aiff = os.path.join(tmpdir, "voice.aiff")
        res = subprocess.run(["say", "-v", voice, "-o", voice_aiff, text], capture_output=True, text=True)
        if res.returncode != 0:
            subprocess.run(["say", "-o", voice_aiff, text], check=True)

        cmd = [
            "ffmpeg", "-y",
            "-i", voice_aiff,
            "-af", "highpass=f=180,lowpass=f=4200,volume=1.4,silenceremove=start_periods=1:start_duration=0.02:start_threshold=-35dB:detection=peak,areverse,silenceremove=start_periods=1:start_duration=0.05:start_threshold=-35dB:detection=peak,areverse",
            "-c:a", "libmp3lame", "-b:a", "192k", "-ar", "44100", "-ac", "1",
            out_mp3
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    cmd_info = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", out_mp3]
    dur = float(subprocess.check_output(cmd_info).decode().strip())
    print(f"  ✓ {slug:<30} ({voice:<15}): {dur:5.2f}s")

def main():
    print("Generating 12 additional multilingual radio bulletins...")
    for slug, voice, text in ADDITIONAL:
        try:
            process(slug, voice, text)
        except Exception as e:
            print(f"Error on {slug}: {e}")

if __name__ == "__main__":
    main()
