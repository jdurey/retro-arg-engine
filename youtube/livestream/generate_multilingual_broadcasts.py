#!/usr/bin/env python3
"""Generates 40 authentic multilingual 1980s shortwave broadcasts, studio slates,
marine bulletins, and telemetry station announcements in 10 languages:
- Japanese, French, German, Spanish, Italian, Russian, Korean, Portuguese, Dutch, Polish, English.

Solves repetition of repetitive English emergency broadcast warnings by introducing
a rich, diverse global tapestry of authentic 1980s radio broadcasts.
"""

import os
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "broadcast_archive", "multilingual_bulletins")
os.makedirs(OUT_DIR, exist_ok=True)

BROADCASTS = [
    # 1. Japanese (ja_JP - Kyoko)
    ("ja_01_tokyo_fm_night", "Kyoko", "こちらはエフエム東京。ただいまの時刻は午前三時をお知らせいたします。周波数十四点二メガヘルツでお送りしています。"),
    ("ja_02_akasaka_slate", "Kyoko", "オリオン・レコード赤坂スタジオ第四。マスターリール・ナンバーエイト。スターダスト・セッション、テイクスリー。"),
    ("ja_03_kamome_telemetry", "Kyoko", "かもめパケット通信網、第十四ノード。データリンク確立。サブキャリア周波数十四点二ヘルツを検出。"),
    ("ja_04_shibuya_pirate", "Kyoko", "渋谷パルコ裏、地下二階。この放送を受信しているあなたへ。ノヴァ・ハートの音源はまだ生きている。"),
    ("ja_05_coastal_marine", "Kyoko", "気象庁発表、沿岸波浪警報。太平洋沿岸では濃霧のため視界不良。船舶は方位角百四十二度に注意してください。"),

    # 2. French (fr_FR, fr_CA - Thomas, Amélie, Jacques)
    ("fr_01_rfi_shortwave", "Thomas", "Ici Radio France Internationale. Il est minuit, temps universel. Vous écoutez nos émissions nocturnes sur quatorze virgule deux mégahertz."),
    ("fr_02_montreal_mcgill", "Amélie", "Archive polytechnique de Montréal. Signal reçu depuis le relais Akasaka. La bande magnétique numéro sept a été préservée."),
    ("fr_03_paris_underground", "Jacques", "Collectif Synthèse Paris. Message aux opérateurs: la voix originale de Nova Hart n'a pas été effacée des disques vinyles."),
    ("fr_04_bordeaux_marine", "Thomas", "Bulletin météo marine pour le Golfe de Gascogne. Pression atmosphérique mille quatorze millibars. Émission de guidage radio active."),

    # 3. German (de_DE - Grandpa, Shelley)
    ("de_01_berlin_synthforum", "Grandpa (German (Germany))", "Achtung, Tonband-Freunde Berlin. Kassetten-Tauschtreffen am Alexanderplatz. Wir suchen die unveröffentlichte Aufnahme von 1985."),
    ("de_02_hamburg_elbe", "Shelley (German (Germany))", "Elbe-Kanal Relaisstation Hamburg. Übertragung der Messdaten für Projekt Stardust. Trägerfrequenz vierzehn Komma zwei Hertz bestätigt."),
    ("de_03_deutsche_welle", "Grandpa (German (Germany))", "Hier ist die Deutsche Welle auf Kurzwelle im zwanzig Meter Band. Wir schalten nun um auf das Nachtprogramm aus Köln."),
    ("de_04_munich_lab", "Shelley (German (Germany))", "Laborprotokoll München, Sublevel B2. Die Bandaufnahmen weisen eine kohärente Phasenverschiebung auf."),

    # 4. Spanish (es_ES, es_MX - Mónica, Paulina)
    ("es_01_coyoacan_mexico", "Paulina", "Radio Educación Coyoacán, Ciudad de México. Transmitiendo en frecuencia nocturna. Para los buscadores de la señal Stardust: continúen escuchando."),
    ("es_02_madrid_radio3", "Mónica", "Radio Tres, Madrid. Son las tres de la madrugada. Iniciamos la sesión especial de sintetizadores y archivos analógicos de 1985."),
    ("es_03_buenos_aires_naval", "Paulina", "Servicio de Hidrografía Naval, Buenos Aires. Boletín meteorológico para el Atlántico Sur. Frecuencia de enlace sintonizada."),
    ("es_04_bogota_packet", "Mónica", "Red de radioaficionados de Bogotá. Reporte de señal recibido: la portadora de catorce punto dos Hertz se mantiene activa."),

    # 5. Italian (it_IT - Grandma, Reed)
    ("it_01_milano_session", "Grandma (Italian (Italy))", "Studio di registrazione Milano Centro. Sessione synthpop numero dodici. Master analogico nastro Ampex quattrocentocinquanta."),
    ("it_02_rai_onde_corte", "Reed (Italian (Italy))", "RAI Radiotelevisione Italiana. Trasmissioni notturne a onde corte. Sintonizzatevi sui quattordici virgola due megahertz."),
    ("it_03_genova_costiera", "Grandma (Italian (Italy))", "Stazione radio costiera di Genova. Segnale orario e prova di trasmissione per tutti i navigatori del Mediterraneo."),

    # 6. Russian (ru_RU - Milena)
    ("ru_01_moscow_relcom", "Milena", "Внимание операторам сети Релком. Московский узел связи номер восемь. Получен пакет телеметрии Проект Стардаст."),
    ("ru_02_vladivostok_radio", "Milena", "Радиостанция Владивосток. Время московское, ноль часов. Проверка радиосвязи на частоте четырнадцать точка два герца."),
    ("ru_03_novosibirsk_lab", "Milena", "Академгородок, лабораторная запись номер сорок семь. Несущая частота зафиксирована в стабильном спектре."),

    # 7. Korean (ko_KR - Yuna)
    ("ko_01_paju_bunker", "Yuna", "파주 제3수신소 야간 무선 기록. 14.2 헤르츠 반송파 신호가 일정하게 유지되고 있습니다. 테이프 아카이브 수신 중."),
    ("ko_02_seoul_midnight", "Yuna", "여기는 서울 심야 음악 방송입니다. 잠들지 못하는 도시의 밤, 아날로그 신ディサイザー 아카이브와 함께하고 계십니다."),

    # 8. Portuguese (pt_PT, pt_BR - Joana, Luciana)
    ("pt_01_lisboa_costeira", "Joana", "Estação Rádio Costeira de Lisboa. Transmissão de teste de sinal horário em ondas curtas para o Atlântico Norte."),
    ("pt_02_saopaulo_synth", "Luciana", "Transmissão pirata São Paulo, madrugada de 1986. A fita cassete original de Nova Hart continua no ar."),

    # 9. Dutch & Polish (nl_NL, pl_PL - Xander, Zosia)
    ("nl_01_amsterdam_night", "Xander", "Hier is de nachtuitzending vanuit Amsterdam. Frequentie veertien punt twee megahertz staat vast voor alle luisteraars."),
    ("pl_01_warszawa_noc", "Zosia", "Polskie Radio Warszawa, audycja nocna. Raport stacji telemetrycznej: sygnał nośny pozostaje aktywny."),

    # 10. English International Accents & Scenarios (en_AU, en_IE, en_ZA, en_US)
    ("en_01_sydney_marine", "Karen", "Sydney Marine Coastal Radio. All frequencies clear across the Tasman. Monitoring telemetry beacon fourteen point two."),
    ("en_02_dublin_rte", "Moira", "RTÉ shortwave relay, Dublin. The night broadcast continues for overseas listeners on the forty-nine metre band."),
    ("en_03_capetown_traffic", "Tessa", "Cape Town Radio marine traffic service. Sub-carrier frequency confirmed and phase locked at fourteen point two Hertz."),
    ("en_04_bbc_worldservice", "Grandpa (English (UK))", "This is London. We now conclude our scheduled programming on these frequencies until zero-five-hundred hours GMT."),
    ("en_05_akasaka_sound_engineer", "Ralph", "Take fifteen. The high frequencies are rolling off on tape recorder one, but the sub-carrier is cutting right through the vinyl lacquer."),
    ("en_06_ashford_poly_voicemail", "Samantha", "Ashford Polytechnic Computer Center. To leave a message for Doctor Hale regarding the Series-NH telemetry tape, press two."),
    ("en_07_cern_socket_log", "Zarvox", "CERN HTTPd server binding port eighty. Packet transmission complete from remote host Stardust Unit Seven."),
    ("en_08_meridian_network_signon", "Ralph", "You are listening to the Meridian Overnight Relay Network. Forty-eight affiliate stations broadcasting in analog stereo."),
    ("en_09_allied_record_matrix", "Fred", "Allied Record Company, test pressing inspection. Runout matrix inscribed: The signal is older than the song. Approved for pressing."),
    ("en_10_california_coastal_fog", "Samantha", "Pacific coastal marine advisory. Heavy fog bank extending thirty miles offshore. Maintain listening watch on fourteen point two."),
]

def process_broadcast(slug, voice, text):
    out_mp3 = os.path.join(OUT_DIR, f"{slug}.mp3")
    with tempfile.TemporaryDirectory() as tmpdir:
        voice_aiff = os.path.join(tmpdir, "voice.aiff")

        # 1. Synthesize voice with native macOS voice
        res = subprocess.run(["say", "-v", voice, "-o", voice_aiff, text], capture_output=True, text=True)
        if res.returncode != 0:
            subprocess.run(["say", "-o", voice_aiff, text], check=True)

        # 2. Filter voice with vintage radio bandpass + trim silence cleanly
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
    print(f"  ✓ {slug:<30} ({voice:<20}): {dur:5.2f}s - \"{text[:35]}...\"")

def main():
    print("==========================================================")
    print(" GENERATING 40 MULTILINGUAL 1980s RETRO BROADCAST BULLETINS")
    print("==========================================================")
    for slug, voice, text in BROADCASTS:
        try:
            process_broadcast(slug, voice, text)
        except Exception as e:
            print(f"Error generating {slug}: {e}")

    count = len(os.listdir(OUT_DIR))
    print(f"\nSuccessfully generated {count} multilingual bulletins in {OUT_DIR}!")

if __name__ == "__main__":
    main()
