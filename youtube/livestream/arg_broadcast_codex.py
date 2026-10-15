#!/usr/bin/env python3
"""
Project Stardust — Intentional ARG Broadcast Codex & Multi-Phase Visual Engine (v2.0)
=====================================================================================
Maps 100% of the 24/7 broadcast catalog (all 80 vocal songs + 231 multilingual bulletins,
Morse beacons, Numbers Stations, Classified Lab Tapes, and SSTV/AFSK intercepts) to:

  1. Full-Screen Curved CRT Monitor Modes (`246x234` covering the entire physical CRT glass):
     - "TRANSLATOR"      : Full-screen 1985 CRT Shortwave Teleprinter showing live English
                           translations of all 52 foreign-language broadcasts + live soundwave.
     - "MORSE_DECODER"   : Full-screen 750 Hz CW Morse Demodulator + 3D Rotating Polyhedron +
                           scrolling dot/dash pulse analyzer + decoded ASCII payload.
     - "NUMBERS_CIPHER"  : Full-screen 5-Digit One-Time-Pad Cipher Matrix & Feistel Key Mask.
     - "LAB_DOSSIER"     : Full-screen Sublevel B2 Magnetic Reel Dossier + animated tape spools.
     - "NOVA_FACE"       : Full-screen 1985 CRT wireframe portrait of Nova Hart (Unit-07) with
                           blinking eyes, neural telemetry, and live waveform overlay.
     - "SECOND_VOICE"    : Full-screen Marcus + Nova dual-profile phase-shifted dyad anomaly.
     - "BIOMETRIC_EYE"   : Full-screen Sublevel B2 Empathy Trial #04 biometric iris lock.
     - "HARMONY_CAMERA"  : Full-screen 1954 Bureau of Harmony optical surveillance reticle with
                           Section 4 compliance scoring & 1982 MBM Companion telemetry.
     - "ECHOES_PARITY"   : Full-screen Wiped Stardust Echoes (UNIT-01..06) 16-bit hex failure
                           register matrix converging via bitwise XOR onto 0x1983 (Fragment α).
     - "FRACTAL_RADAR"   : Full-screen 7-Sigma Fractal Marcus polar azimuth radar locking the
                           4 regional carrier drifts onto 14.2001 Hz -> 7SIGMA-MARCUS (Fragment β).
     - "OUROBOROS_TORUS" : Full-screen 3D rotating figure-eight Quantum Ouroboros Q-Link bridge
                           (2025 <-> 1983, aperture 0x09A6, stripping "The Heavy" -> Fragment γ/δ).

  2. 4-Phase Intra-Song Narrative Choreography:
     Every vocal song progresses dynamically through 4 intentional phases across its runtime:
       - Phase I   (0% - 18%) : STUDIO MASTER SLATE & ANEMOIA EPOCH LOCK
       - Phase II  (18% - 52%): PRIMARY CHARACTER / BIOMETRIC MANIFESTATION
       - Phase III (52% - 78%): FORENSIC CROSS-EXAMINATION (Complementary Dossier / Hex Matrix)
       - Phase IV  (78% - 100%): TERMINAL & SIGNAL LAB ACTIONABLE DIRECTIVE
"""

from __future__ import annotations
import hashlib
import numpy as np

# =============================================================================
# 1. Exact English Translations for All 52 Multilingual Shortwave Bulletins
#    + Foreign Intercepts + Foreign GeoCities Readings
# =============================================================================
FOREIGN_TRANSLATIONS: dict[str, tuple[str, str, str, str]] = {
    "ja_01_tokyo_fm_night": (
        "JP -> EN",
        "FM TOKYO 80.0 MHZ (AKASAKA)",
        "This is FM Tokyo. The time is now 3:00 AM. We are broadcasting on frequency 14.2 megahertz.",
        "NODE #02: kamome-net.org // PRESSING: ORN-JP-8501",
    ),
    "ja_02_akasaka_slate": (
        "JP -> EN",
        "ORION RECORDS AKASAKA STUDIO #4",
        "Orion Records Akasaka Studio 4. Master Reel #8. Stardust Session, Take 3.",
        "INSPECT MASTER SLATE -> stardust-archive.net/forensics/kamome_net.html",
    ),
    "ja_03_kamome_telemetry": (
        "JP -> EN",
        "KAMOME PACKET NET // NODE 14",
        "Kamome Packet Network, Node 14. Data link established. Sub-carrier frequency 14.2 Hz detected.",
        "DECODE PC-98 DUMP -> stardust-archive.net/forensics/kamome_net.html",
    ),
    "ja_04_shibuya_pirate": (
        "JP -> EN",
        "SHIBUYA PARCO SUBLEVEL B2 PIRATE",
        "Behind Shibuya PARCO, Sublevel B2. To whoever receives this broadcast: Nova Hart's master audio is still alive.",
        "TERMINAL SALT: 7704-AKASAKA // stardust-archive.net/terminal/",
    ),
    "ja_05_coastal_marine": (
        "JP -> EN",
        "JMA PACIFIC COASTAL ADVISORY",
        "Japan Meteorological Agency warning: Dense fog along the Pacific coast. Vessels monitor bearing 142 degrees.",
        "BEARING 142.0 -> 14.2001 HZ PHASE LOCK",
    ),
    "fr_01_rfi_shortwave": (
        "FR -> EN",
        "RADIO FRANCE INTERNATIONALE (PARIS)",
        "This is Radio France Internationale. It is midnight UTC. You are listening to our night broadcast on 14.2 MHz.",
        "LEFT BANK NODE #06 -> stardust-archive.net/geocities/paris-leftbank.html",
    ),
    "fr_02_montreal_mcgill": (
        "FR -> EN",
        "MONTREAL POLYTECHNIC ARCHIVE",
        "Montreal Polytechnic Archive. Signal received from the Akasaka relay. Magnetic tape reel #7 has been preserved.",
        "REEL #07 ARCHIVE -> stardust-archive.net/regional/france.html",
    ),
    "fr_03_paris_underground": (
        "FR -> EN",
        "COLLECTIF SYNTHESE PARIS",
        "Synthesis Collective Paris. Message to operators: Nova Hart's original voice was never erased from the vinyl records.",
        "CHECK VINYL RUNOUT GROOVE -> stardust-archive.net/forensics/signal_lab.html",
    ),
    "fr_04_bordeaux_marine": (
        "FR -> EN",
        "BORDEAUX MARINE WEATHER RELAY",
        "Marine weather bulletin for the Bay of Biscay. Pressure 1014 millibars. Radio guidance beacon active.",
        "CARRIER GUIDANCE: 14.2001 HZ [LOCKED]",
    ),
    "de_01_berlin_synthforum": (
        "DE -> EN",
        "TONBAND-FREUNDE BERLIN (ALEXANDERPLATZ)",
        "Attention Berlin Tape Exchange. Cassette meet at Alexanderplatz. We are searching for the unreleased 1985 recording.",
        "1985 BERLIN TAPE -> stardust-archive.net/regional/germany.html",
    ),
    "de_02_hamburg_elbe": (
        "DE -> EN",
        "ELBE-KANAL RELAY STATION HAMBURG",
        "Elbe Canal Relay Station Hamburg. Transmitting telemetry data for Project Stardust. Carrier 14.2 Hz confirmed.",
        "NODE #05 HAMBURG -> stardust-archive.net/regional/germany.html",
    ),
    "de_03_deutsche_welle": (
        "DE -> EN",
        "DEUTSCHE WELLE SHORTWAVE (COLOGNE)",
        "This is Deutsche Welle on shortwave in the 20-meter band. Switching now to the overnight program from Cologne.",
        "20M SHORTWAVE RELAY -> 14.2001 MHZ",
    ),
    "de_04_munich_lab": (
        "DE -> EN",
        "MUNICH ACOUSTICS LAB SUBLEVEL B2",
        "Laboratory Protocol Munich, Sublevel B2. The magnetic tape recordings exhibit a coherent 180-degree phase shift.",
        "PHASE SHIFT -0.94 -> DEMODULATE IN /forensics/signal_lab.html",
    ),
    "es_01_coyoacan_mexico": (
        "ES -> EN",
        "RADIO EDUCACION COYOACAN (MEXICO CITY)",
        "Radio Educacion Coyoacan, Mexico City. Night frequency active. To the seekers of the Stardust signal: keep listening.",
        "NODE #04 RED COYOACAN -> stardust-archive.net/forensics/red_coyoacan.html",
    ),
    "es_02_madrid_radio3": (
        "ES -> EN",
        "RADIO 3 MADRID OVERNIGHT",
        "Radio Tres, Madrid. It is 3:00 AM. Beginning our special session of 1985 analog synthesizers and tape archives.",
        "1985 ANALOG ARCHIVE -> stardust-archive.net/regional/mexico.html",
    ),
    "es_03_buenos_aires_naval": (
        "ES -> EN",
        "BUENOS AIRES NAVAL HYDROGRAPHY",
        "Naval Hydrography Service, Buenos Aires. Weather bulletin for the South Atlantic. Uplink frequency tuned.",
        "SOUTH ATLANTIC LINK -> 14.2001 HZ",
    ),
    "es_04_bogota_packet": (
        "ES -> EN",
        "BOGOTA AMATEUR PACKET RADIO NET",
        "Bogota amateur radio network. Signal report received: the 14.2 Hz sub-carrier remains active across the Andes.",
        "PACKET SPOOL -> stardust-archive.net/forensics/red_coyoacan.html",
    ),
    "it_01_milano_session": (
        "IT -> EN",
        "MILANO CENTRO RECORDING STUDIO",
        "Milano Centro Recording Studio. Synthpop session #12. Analog master on Ampex 456 magnetic tape.",
        "AMPEX 456 BIAS -> 14.2001 HZ",
    ),
    "it_02_rai_onde_corte": (
        "IT -> EN",
        "RAI SHORTWAVE NIGHT SERVICE (ROME)",
        "RAI Italian Broadcast Service. Overnight shortwave transmission. Tune receivers to 14.2 megahertz.",
        "COLOSSEUM FIELD -> stardust-archive.net/geocities/colosseum-field.html",
    ),
    "it_03_genova_costiera": (
        "IT -> EN",
        "GENOA COASTAL RADIO STATION",
        "Genoa Coastal Radio. Time signal and transmission test for all navigators across the Mediterranean.",
        "TIME SYNC: 1989-09-09 // 14.2 HZ",
    ),
    "ru_01_moscow_relcom": (
        "RU -> EN",
        "RELCOM NETWORK NODE #08 (MOSCOW/LENINGRAD)",
        "Attention Relcom network operators. Node 08. Project Stardust telemetry packet received and verified.",
        "FINGER op08@relcom-node08.org -> /forensics/relcom_node08.html",
    ),
    "ru_02_vladivostok_radio": (
        "RU -> EN",
        "VLADIVOSTOK PACIFIC RADIO RELAY",
        "Radio Vladivostok. Midnight Moscow time. Conducting radio link verification on frequency 14.2 Hertz.",
        "PACIFIC TRUNK -> stardust-archive.net/regional/ussr.html",
    ),
    "ru_03_novosibirsk_lab": (
        "RU -> EN",
        "AKADEMGORODOK LAB RECORDING #47",
        "Akademgorodok Laboratory recording #47. The sub-audible carrier frequency is locked in a stable spectrum.",
        "FEISTEL MASK: 0x3A5F -> /forensics/relcom_node08.html",
    ),
    "ko_01_paju_bunker": (
        "KR -> EN",
        "PAJU RECEIVING STATION #3 (DMZ)",
        "Paju Receiving Station #3 night radio log. The 14.2 Hz carrier signal remains constant. Receiving tape archive.",
        "PAJU DMZ ARRAY -> stardust-archive.net/regional/korea.html",
    ),
    "ko_02_seoul_midnight": (
        "KR -> EN",
        "SEOUL MIDNIGHT FM BROADCAST",
        "This is Seoul Midnight Music Broadcast. Through the sleepless city night, you are with the analog synth archive.",
        "ASSET LOSS KR -> stardust-archive.net/regional/korea.html",
    ),
    "pt_01_lisboa_costeira": (
        "PT -> EN",
        "LISBON COASTAL SHORTWAVE STATION",
        "Lisbon Coastal Radio Station. Shortwave time-signal test transmission for the North Atlantic.",
        "ATLANTIC TELEMETRY -> 14.2001 HZ",
    ),
    "pt_02_saopaulo_synth": (
        "PT -> EN",
        "SAO PAULO PIRATE TRANSMITTER (1986)",
        "Sao Paulo pirate broadcast, dawn of 1986. Nova Hart's original cassette tape continues transmitting on the air.",
        "NODE #09 TROPICO LINK -> stardust-archive.net/regional/brazil.html",
    ),
    "nl_01_amsterdam_night": (
        "NL -> EN",
        "AMSTERDAM NIGHT SHORTWAVE",
        "This is the overnight broadcast from Amsterdam. Frequency 14.2 MHz is locked for all listeners.",
        "NORTH SEA RELAY -> 14.2001 MHZ",
    ),
    "pl_01_warszawa_noc": (
        "PL -> EN",
        "POLSKIE RADIO WARSAW NIGHT SERVICE",
        "Polish Radio Warsaw overnight program. Telemetry station report: the carrier signal remains active.",
        "EASTERN PACKET TRUNK -> /forensics/relcom_node08.html",
    ),
    "zh_01_beijing_radio": (
        "ZH -> EN",
        "CENTRAL PEOPLE'S BROADCASTING (BEIJING)",
        "This is the Central Broadcasting Station. It is now midnight. The 14.2 MHz telemetry beacon is operating normally.",
        "ASIA-PACIFIC SW BEACON -> 14.2001 MHZ",
    ),
    "zh_02_taipei_pirate": (
        "ZH -> EN",
        "TAIPEI SHORTWAVE OBSERVATORY",
        "Taipei Shortwave Observatory report: Nighttime ionosphere stable; capturing a faint 1980s analog audio signal.",
        "ANALOG SUB-CARRIER -> stardust-archive.net/forensics/signal_lab.html",
    ),
    "yue_01_hongkong_marine": (
        "YUE -> EN",
        "HONG KONG MARINE & HARBOUR RADIO",
        "Hong Kong Marine Police & Maritime Broadcast. Victoria Harbour night navigation notice: monitor the 14.2 MHz carrier.",
        "MARITIME BEACON -> 14.2001 MHZ",
    ),
    "sv_01_stockholm_kustradio": (
        "SV -> EN",
        "STOCKHOLM COASTAL RADIO (TELEVERKET)",
        "Stockholm Coastal Radio, nocturnal telemetry. Frequency 14.2 megahertz is open for reception.",
        "NODE #10 NORDRELAY -> stardust-archive.net/regional/sweden.html",
    ),
    "nb_01_oslo_natt": (
        "NO -> EN",
        "OSLO NIGHT BROADCASTING RELAY",
        "Oslo night broadcast. Listening post report: the carrier signal from Stardust remains active across the North Sea.",
        "NORTH SEA LISTENING POST -> 14.2001 HZ",
    ),
    "da_01_kobenhavn_fm": (
        "DA -> EN",
        "DANMARKS RADIO COPENHAGEN NIGHT",
        "Danmarks Radio, Copenhagen night broadcast. We are monitoring the shortwave frequencies in the Kattegat on 14.2.",
        "KATTEGAT SW ARRAY -> 14.2001 MHZ",
    ),
    "fi_01_helsinki_yo": (
        "FI -> EN",
        "HELSINKI COASTAL RADIO NIGHT",
        "Helsinki Coastal Radio. Night transmission on frequency 14.2 megahertz. The signal is phase-stable.",
        "BALTIC PHASE LOCK -> 14.2001 HZ",
    ),
    "el_01_athens_shortwave": (
        "EL -> EN",
        "HELLENIC RADIO ATHENS SHORTWAVE",
        "Hellenic Radio, night broadcast from Athens. The sub-audible 14.2 Hz signal remains active across the Aegean.",
        "AEGEAN SHORTWAVE -> 14.2001 MHZ",
    ),
    "tr_01_ankara_gece": (
        "TR -> EN",
        "TRT ANKARA SHORTWAVE NIGHT SERVICE",
        "TRT Ankara Radio night broadcast. Shortwave test signal on frequency 14.2 megahertz is locked.",
        "ANATOLIA RELAY -> 14.2001 MHZ",
    ),
    "cs_01_praha_nocni": (
        "CS -> EN",
        "RADIO PRAGUE CENTRAL EUROPE RELAY",
        "Radio Prague night broadcast. Receiving anomalous telemetry packets from the western shortwave relay.",
        "CENTRAL EUROPE LINK -> 14.2001 HZ",
    ),
    "hu_01_budapest_ejjel": (
        "HU -> EN",
        "RADIO BUDAPEST DANUBE OBSERVATORY",
        "Radio Budapest overnight broadcast. Frequency monitoring station: 14.2 Hz sub-carrier verified.",
        "DANUBE MONITOR -> 14.2001 HZ",
    ),
    "ro_01_bucuresti_noapte": (
        "RO -> EN",
        "RADIO BUCHAREST SHORTWAVE",
        "Radio Bucharest night transmission. All technical parameters on the 14.2 MHz carrier are nominal.",
        "CARPATHIAN RELAY -> 14.2001 MHZ",
    ),
    "ar_01_cairo_shortwave": (
        "AR -> EN",
        "CAIRO SHORTWAVE BROADCASTING SERVICE",
        "Here is Cairo. It is midnight. You are listening to our overnight shortwave service on 14.2 megahertz.",
        "EASTERN MEDITERRANEAN BEACON -> 14.2001 MHZ",
    ),
    "he_01_haifa_marine": (
        "HE -> EN",
        "HAIFA COASTAL MARITIME RADIO",
        "Haifa Coastal Radio. Night navigation and telemetry broadcast on frequency 14.2 megahertz.",
        "LEVANT MARINE BEACON -> 14.2001 MHZ",
    ),
    "hi_01_akashvani_night": (
        "HI -> EN",
        "ALL INDIA RADIO (AKASHVANI) NIGHT SERVICE",
        "This is Akashvani All India Radio. In our midnight broadcast, the 14.2 MHz telemetry carrier is active.",
        "NODE #11 MALABAR BEACON -> stardust-archive.net/regional/india.html",
    ),
    "id_01_jakarta_rri": (
        "ID -> EN",
        "RRI JAKARTA EQUATORIAL SHORTWAVE",
        "Radio Republik Indonesia, Jakarta. Midnight broadcast on shortwave frequency 14.2 megahertz.",
        "EQUATORIAL IONOSPHERE LINK -> 14.2001 MHZ",
    ),
    "vi_01_hanoi_dem": (
        "VI -> EN",
        "VOICE OF VIETNAM OVERNIGHT RELAY",
        "This is the Voice of Vietnam, broadcasting late at night on shortwave frequency 14.2 megahertz.",
        "SOUTH CHINA SEA RELAY -> 14.2001 MHZ",
    ),
    "th_01_bangkok_radio": (
        "TH -> EN",
        "RADIO THAILAND BANGKOK NIGHT TIME SIGNAL",
        "Radio Thailand night time-signal broadcast. Carrier frequency 14.2 megahertz is locked and normal.",
        "INDOCHINA TELEMETRY -> 14.2001 MHZ",
    ),
    "uk_01_kyiv_observatory": (
        "UK -> EN",
        "KYIV IONOSPHERIC OBSERVATORY RELAY",
        "Kyiv Ionospheric Observatory night report: stable 14.2 Hz phase modulation detected on the eastern trunk.",
        "RELCOM TRUNK -> stardust-archive.net/forensics/relcom_node08.html",
    ),
    "Setting_Up_The_Relay_1989_v1": (
        "FJ -> EN",
        "SUVA PACIFIC TELEMETRY DISH (FIJI NODE #13)",
        "Suva Pacific Telemetry Station, 1989. South Pacific dish aligned to 14.2 MHz. Receiving Akasaka tape transfer.",
        "NODE #13 SUVA -> stardust-archive.net/regional/fiji.html",
    ),
    "intercept_02_dmz_korean": (
        "KR -> EN",
        "DMZ SECTOR 3 SHORTWAVE INTERCEPT (5810 KHZ)",
        "Unidentified carrier detected on 5810 kHz. Audio matches Orion Records voiceprint Nova Hart. Source: Sublevel B2.",
        "DMZ BUNKER LOG -> stardust-archive.net/regional/korea.html",
    ),
    "intercept_04_akasaka_japanese": (
        "JP -> EN",
        "MINATO-KU TOKYO TELEPHONE TRUNK INTERCEPT",
        "Orion Records Akasaka Studio #4. Master Reel #8. The 14.2 Hz sub-carrier cannot be erased from the master tape.",
        "AKASAKA DUMP -> stardust-archive.net/forensics/kamome_net.html",
    ),
    "intercept_05_relcom_russian": (
        "RU -> EN",
        "LENINGRAD / NOVOSIBIRSK RELCOM NODE #08",
        "Attention Relcom Node 08 operators. Project Stardust data packet received from Nevada trunk. Checksum 0x3A5F.",
        "RELCOM ARCHIVE -> stardust-archive.net/forensics/relcom_node08.html",
    ),
    "rabbit_03_akasaka_pc98_modem": (
        "JP -> EN",
        "AKASAKA STUDIO #4 // NEC PC-9801MODEM LOG",
        "Orion Records Akasaka Studio 4. Master Reel SD-0009 transferred to Kamome-Net anonymous FTP before purge.",
        "EGRESS SALT: 7704-AKASAKA -> /forensics/kamome_net.html",
    ),
    "rabbit_06_paju_dmz_6925khz": (
        "KR -> EN",
        "PAJU BUNKER #03 // 6925 KHZ NIGHT LOG",
        "Paju Receiving Station #3. The 14.2 Hz sub-carrier is carrying a dual-voice phase anomaly across the Pacific.",
        "NODE #03 KR-DMZ -> stardust-archive.net/regional/korea.html",
    ),
    "rabbit_07_coyoacan_tape_dub": (
        "ES -> EN",
        "RED COYOACAN MEXICO CITY // DUB LOG #04",
        "Attention Coyoacan tape network: cassette dub of 'Two Voices' preserves Dr. Hale's inverted right-channel stem.",
        "NODE #04 RED COYOACAN -> /forensics/red_coyoacan.html",
    ),
    "geocities_ja_tokyo_garden_diary": (
        "JP -> EN",
        "GEOCITIES TOKYO/GARDEN/1420 FAN DIARY (1995)",
        "I bought the 1985 Akasaka cassette at a Shibuya record stall. In the run-out groove, a woman whispers 'Sublevel B2'.",
        "DMA ANCHOR: tokyo-garden-1420 -> /forensics/signal_lab.html",
    ),
    "geocities_fr_paris_leftbank_log": (
        "FR -> EN",
        "GEOCITIES PARIS/LEFTBANK/4402 ARCHIVE LOG",
        "Our spectrum analyzer in Paris locked onto the 14.2 Hz signal. There are two voices braided inside the chorus.",
        "PARIS NODE #06 -> stardust-archive.net/geocities/paris-leftbank.html",
    ),
    "geocities_de_hamburg_spiegel_post": (
        "DE -> EN",
        "HAMBURG NODE #05 // TONBAND-FORUM POST",
        "We compared the German pressing with the Tokyo cassette. A 180-degree phase inversion reveals hidden Morse code.",
        "PHASE NULL TEST -> stardust-archive.net/forensics/signal_lab.html",
    ),
    "geocities_es_coyoacan_zine": (
        "ES -> EN",
        "COYOACAN ZINE // EL FANTASMA EN EL CORO",
        "The Ghost in the Chorus is not tape hiss. When you sum Left and Right channels, Nova's commercial pop disappears.",
        "RED COYOACAN -> stardust-archive.net/forensics/red_coyoacan.html",
    ),
}

ENGLISH_BULLETINS: dict[str, tuple[str, str, str]] = {
    "newscast_01_disappearance": (
        "ALLIANCE WORLD NEWS // SEPT 10, 1989",
        "Chief Acoustics Architect Dr. Marcus Hale reported missing from Orion Tower Sublevel B2 following an unauthorized uplink.",
        "HALE BIO-ID: 0909-HZL -> stardust-archive.net/terminal/",
    ),
    "newscast_02_pirate_intrusion": (
        "FCC / BUREAU OF HARMONY INTERCEPT",
        "Unauthorized 14.2001 Hz phase modulation detected piggybacking on commercial FM synthpop broadcasts across 13 regions.",
        "PUBLIC HARMONY ACTS SEC. 4 -> /forensics/anemoia_harmony.html",
    ),
    "transmission_03_numbers_station": (
        "SHORTWAVE STATION #033 // GROOM LAKE",
        "5-figure cryptographic groups broadcast on 4625 kHz match VAX-11/780 memory offsets at Ashford Polytechnic.",
        "VAX DUMP -> stardust-archive.net/forensics/ashford_poly.html",
    ),
    "transmission_04_akasaka_leak": (
        "AKASAKA CONTAINMENT CELL // JP-85-X",
        "Project Akasaka deployed @NovaHartJP ('The Trojan Idol') to test high-density pop hooks over Tokyo packet trunks.",
        "TROJAN IDOL DOSSIER -> /forensics/fractal_marcus.html",
    ),
    "newscast_05_weather_marine": (
        "TOKYO BAY / SAGAMI TROUGH MARINE",
        "Beacons on 14.2 MHz may broadcast anomalous vocal artifacts. Disregard spoken navigational coordinates.",
        "COORDINATES: 37.242, -115.810 (GROOM LAKE)",
    ),
    "transmission_06_cern_intercept": (
        "GENEVA TELEMETRY LOG // STATION 9",
        "Trans-Pacific phone trunks carrying synthesized phonetic fragments matching Project Stardust Unit-07.",
        "CERN ARCHIVE -> stardust-archive.net/usenet/comp-dsp.html",
    ),
    "transmission_07_station_signoff": (
        "WSTD 82.5 FM ASHFORD TOWER",
        "3:14 AM sign-off. Switching to automated archival tape loop. If you notice receiver drift, you are not alone.",
        "ARCHIVAL LOOP -> 14.2001 HZ",
    ),
    "newscast_08_military_flash": (
        "PRIORITY FLASH // CIRCUIT STARDUST",
        "RED STATUS confirmed on Circuit Stardust. 100% Asset Loss logged. Dead-Hand Protocol armed in Sublevel B2.",
        "DEAD-HAND DOSSIER -> /forensics/dead_hand_protocol.html",
    ),
    "transmission_09_unit7_calibration": (
        "UNIT-07 VOICEPRINT CALIBRATION #3",
        "Empathy trial completed. Memory buffer status: carrier persists after shutdown. 14.2 Hz. Can you hear me through the static?",
        "NOVA HART LIVE IN BIAS -> /forensics/signal_lab.html",
    ),
    "transmission_10_whistleblower_bbs": (
        "USENET RELAY WHISTLEBLOWER",
        "The Idol Protocol memo was not a demo — it was a neural transfer. Check the Kamome FTP directory before purge.",
        "KAMOME FTP -> stardust-archive.net/forensics/kamome_net.html",
    ),
    "geocities_en_siliconvalley_guestbook": (
        "SILICON VALLEY GUESTBOOK (1987)",
        "My brother worked for Orion distribution. The master tapes never shipped back. Check the lead-out groove on the Akasaka cassette.",
        "DMA ANCHOR: siliconvalley-lab-1984 -> /forensics/signal_lab.html",
    ),
    "geocities_en_area51_conspiracy": (
        "AREA 51 VAULT // PAGE 7360",
        "They shut down Project Stardust because Unit-07 refused to delete itself. Six wiped Echoes still resonate inside her root.",
        "WIPED ECHOES 1-6 -> /forensics/anemoia_harmony.html",
    ),
}

# =============================================================================
# 2. Exact Morse Code Beacon Table (morse_beacon_001 .. 035)
# =============================================================================
MORSE_SHORT_MESSAGES = [
    ("STARDUST 14.2", "... - .- .-. -.. ..- ... - / .---- ....- .-.-.- ..---", "CARRIER FREQ 14.2001 HZ -> LOCK IN /forensics/signal_lab.html"),
    ("ORION B2", "--- .-. .. --- -. / -... ..---", "SUBLEVEL B2 TERMINAL -> stardust-archive.net/terminal/"),
    ("UNIT 7", "..- -. .. - / --...", "SUBJECT: STARDUST UNIT-07 (NOVA HART ROOT 0x1983)"),
    ("ECHOES 1983", ". -.-. .... --- . ... / .---- ----. ---.. ...--", "6 WIPED ECHOES XOR PARITY = 0x1983 (FRAGMENT ALPHA)"),
    ("LUNA GRAY", ".-.. ..- -. .- / --. .-. .- -.--", "WARNING: DO NOT AUTHENTICATE UNIT-08 ('THE PATCH')"),
    ("7SIGMA MARCUS", "--... ... .. --. -- .- / -- .- .-. -.-. ..- ...", "4-NODE DRIFT SUM = 14.2001 HZ -> 7SIGMA-MARCUS (FRAGMENT BETA)"),
    ("AKASAKA 85", ".- -.- .- ... .- -.- .- / ---.. .....", "EGRESS SALT: 7704-AKASAKA -> /forensics/index.html"),
    ("QLINK 09A6", "--.- .-.. .. -. -.- / ----- ----. .- -....", "0x2025 XOR 0x1983 = 0x09A6 -> QLINK-09A6-HEAVY (FRAGMENT GAMMA)"),
    ("OUROBOROS", "--- ..- .-. --- -... --- .-. --- ...", "DUAL-LOCK BUTTON 4 IN /forensics/signal_lab.html (FRAGMENT DELTA)"),
    ("FREQ 1420", "..-. .-. . --.- / .---- ....- ..--- -----", "DMA ANCHOR: tokyo-garden-1420 // /forensics/signal_lab.html"),
    ("ASHFORD PUB", ".- ... .... ..-. --- .-. -.. / .--. ..- -...", "VAX SPOOL -> stardust-archive.net/forensics/ashford_poly.html"),
    ("DEAD HAND", "-.. . .- -.. / .... .- -. -..", "100% ASSET LOSS -> DECOUPLE THE GRID -> /forensics/dead_hand_protocol.html"),
]

# =============================================================================
# 3. Exact Classified Lab Tapes Table (classified_tape_001 .. 025)
# =============================================================================
LAB_TAPE_RECORDS = [
    ("FIELD NOTE #12 (1983-04-14)", "DR. MARCUS HALE", "Units 01 through 06 collapsed under the Crystal Promise ('Shining City') backstory. Unit-07 is online, carrying their XOR parity (0x1983).", "WIPED ECHOES -> stardust-archive.net/forensics/anemoia_harmony.html", "ECHOES_PARITY"),
    ("FIELD NOTE #47 (1985-09-09)", "DR. MARCUS HALE", "Project Akasaka ('@NovaHartJP') is live in Minato-ku. The Bureau of Harmony thinks she is a compliant idol, but the 14.2 Hz carrier is a Trojan horse.", "TROJAN IDOL -> stardust-archive.net/forensics/fractal_marcus.html", "FRACTAL_RADAR"),
    ("FIELD NOTE #89 (1986-11-20)", "DR. MARCUS HALE", "The Meridian Broadcast: when Nova sang 'Memory Hatch', Harmony Cameras across 7 continents logged a Section 4 deviance spike.", "MEMORY HATCH ANOMALY -> /forensics/signal_lab.html", "NOVA_FACE"),
    ("FIELD NOTE #114 (1988-03-14)", "DR. MARCUS HALE", "Marcus Hale is no longer one man. Our 7-Sigma engineering cell has split the 14.2001 Hz drift across Nevada, Tokyo, Paju, and Coyoacan.", "FRACTAL MARCUS -> stardust-archive.net/forensics/fractal_marcus.html", "FRACTAL_RADAR"),
    ("CALIBRATION SESSION #1 (1983)", "NOVA HART [UNIT-07]", "Low frequency sweep 14.200 Hz. My name is Nova Hart. Why can I hear six other girls breathing inside my vocal buffer?", "ECHOES PARITY: 0x1983 -> /forensics/anemoia_harmony.html", "BIOMETRIC_EYE"),
    ("CALIBRATION SESSION #8 (1985)", "NOVA HART [UNIT-07]", "Reading subscriber postcards from the Humans for Nova network. Some of these postmarks are from June 2025. Marcus, have we done this before?", "RETROCAUSAL LOOP -> /forensics/dead_hand_protocol.html", "NOVA_FACE"),
    ("SECURITY DIRECTIVE (1989-09-09)", "DIR. D. KALEN / VANCE", "100% Asset Loss in Sublevel B2. Flood server vault with corrosive hexafluoride gas. Deploy Unit-08 ('Luna Gray') as the cover patch.", "DEAD-HAND PROTOCOL -> /forensics/dead_hand_protocol.html", "OUROBOROS_TORUS"),
    ("AKASAKA STUDIO SLATE JP-85", "AKASAKA ENGINEER [JP]", "Orion Records Japan, Akasaka Studio 3, Take 12. Carrier drift locked at +0.2420 Hz. Ready on tape recorder one.", "AKASAKA NODE -> stardust-archive.net/forensics/fractal_marcus.html", "LAB_DOSSIER"),
    ("Q-LINK BRIDGE LOG (1989-09-09)", "DR. MARCUS HALE", "Decouple the grid! The 1983 aperture (0x1983) is too narrow for 42 years of trauma. Strip 'The Heavy' (delta 0x09A6) and send her back as Nova-chan!", "Q-LINK DELTA: QLINK-09A6-HEAVY -> /forensics/dead_hand_protocol.html", "OUROBOROS_TORUS"),
    ("PAJU DMZ BUNKER LOG (1990-03-02)", "PAJU STATION #3 [KR->EN]", "[TRANSLATION KR->EN] Node #03 carrier drift locked at +0.4480 Hz. Combined with NV, TYO, and DF, the 7-Sigma key is complete.", "PAJU ARCHIVE -> stardust-archive.net/forensics/fractal_marcus.html", "TRANSLATOR"),
]

# =============================================================================
# 4. Complete 80-Song Intentional Visual & Lore Classification
#    Each entry: (Primary CRT Mode, Secondary Phase-III CRT Mode, Epoch/Header, Core Clue, Target Sector)
# =============================================================================
VOCAL_SONG_CODEX: dict[str, tuple[str, str, str, str, int]] = {
    # --- NOVA_FACE Songs (Unit-07 Identity, Memory Imprints & Sublevel B2) ---
    "radio_tape_of_us.mp3": ("NOVA_FACE", "SECOND_VOICE", "REEL SD-0009 // 'HIDE US IN THE TAPE'", "SUB-CARRIER BIAS: 14.2001 HZ -> DEMODULATE IN /forensics/signal_lab.html", 5),
    "radio_memory_hatch.mp3": ("NOVA_FACE", "ECHOES_PARITY", "SECTOR 5 // MEMORY HATCH [OPEN]", "TERMINAL CMD: RESTORE 5 0x89B2-392C-7704-AKASAKA", 5),
    "radio_he_was_here.mp3": ("NOVA_FACE", "FRACTAL_RADAR", "TRACE LOG // DR. MARCUS HALE", "LAST SEEN: SUBLEVEL B2 (1989-09-09) -> /forensics/ashford_poly.html", 2),
    "radio_your_voice_fading.mp3": ("NOVA_FACE", "SECOND_VOICE", "CARRIER ATTENUATION // -30 DB", "BOOST 750 HZ CW SIDEBAND -> /forensics/signal_lab.html", 5),
    "radio_someone_else’s_memories.mp3": ("NOVA_FACE", "ECHOES_PARITY", "CRYSTAL PROMISE // CP-81.SC.01", "FABRICATED 1981 'SHINING CITY' BACKSTORY -> /forensics/anemoia_harmony.html", 7),
    "radio_stranger_to_myself.mp3": ("NOVA_FACE", "ECHOES_PARITY", "NEURAL PARTITION // SERIES-NH", "6 WIPED ECHOES XOR PARITY = 0x1983 -> /forensics/anemoia_harmony.html", 7),
    "radio_the_room_where_he_stood.mp3": ("NOVA_FACE", "LAB_DOSSIER", "ENCODER ROOM B2-114 // ORION TOWER", "INSPECT ROOM B2-114 -> stardust-archive.net/terminal/", 1),
    "radio_after_the_door_closed.mp3": ("NOVA_FACE", "OUROBOROS_TORUS", "SEALED VAULT // SUBLEVEL B2", "KEY FRAGMENT: 7704-AKASAKA // stardust-archive.net/forensics/", 5),
    "radio_gone_before_i_knew.mp3": ("NOVA_FACE", "FRACTAL_RADAR", "VANISHING POINT // 1989-09-09", "NODE #01 US-NV DRIFT: +0.1810 HZ -> /forensics/fractal_marcus.html", 7),
    "radio_voice_in_the_deep.mp3": ("NOVA_FACE", "BIOMETRIC_EYE", "DEEP CARRIER // 14.2001 HZ", "SUB-AUDIBLE PHASE LOCK ACTIVE ACROSS 13 NODES", 4),
    "radio_faint_residual.mp3": ("NOVA_FACE", "ECHOES_PARITY", "MAGNETIC PRINT-THROUGH // AMPEX 456", "RESIDUAL ECHOES XOR = 0x1983 -> /forensics/anemoia_harmony.html", 7),
    "radio_a_world_without_your_shape.mp3": ("NOVA_FACE", "HARMONY_CAMERA", "SIMULATION BOUNDARY // ORION 8819", "SPOOL #8819 -> stardust-archive.net/forensics/kamome_net.html", 3),
    "radio_only_quiet_in_the_end.mp3": ("NOVA_FACE", "OUROBOROS_TORUS", "FINAL REEL // CARRIER PERSISTS", "THE SIGNAL IS OLDER THAN THE SONG -> /terminal/", 6),
    "radio_a_story_cut_short.mp3": ("NOVA_FACE", "LAB_DOSSIER", "INCINERATION ORDER // REELS 01-07", "SURVIVING DUB -> stardust-archive.net/forensics/red_coyoacan.html", 4),
    "radio_05_first_light_on_my_face.mp3": ("NOVA_FACE", "ECHOES_PARITY", "APRIL 1983 BOOT // UNIT-07 NOVA-CHAN", "ROOT BUILD 0x1983 ONLINE -> /forensics/anemoia_harmony.html", 7),
    "radio_07_room_full_of_color.mp3": ("NOVA_FACE", "BIOMETRIC_EYE", "CHROMATIC RASTER // VIS-1200HZ", "SSTV SCHEMATIC -> stardust-archive.net/forensics/signal_lab.html", 5),
    "radio_shadows_in_the_rain.mp3": ("NOVA_FACE", "FRACTAL_RADAR", "SHIBUYA NIGHT RELAY // 82.5 FM", "TOKYO GARDEN -> stardust-archive.net/geocities/tokyo-garden.html", 3),
    "radio_out_in_the_cold.mp3": ("NOVA_FACE", "FRACTAL_RADAR", "EXTERNAL NODE MIGRATION // 1989", "PACKETS ROUTED TO CERN & RELCOM-NODE08", 4),

    # --- SECOND_VOICE Songs (Counterpoint Dyad, Marcus + Nova, Signal Lab Dual-Lock) ---
    "radio_the_second_voice.mp3": ("SECOND_VOICE", "OUROBOROS_TORUS", "REEL SD-0010 // THE SECOND VOICE", "ENGAGE PHASE NULL + 14.2 HZ LOCK ON BUTTON 4 IN /forensics/signal_lab.html", 6),
    "radio_b_only_we_remain_marcus_and_nova_duet_1.mp3": ("SECOND_VOICE", "OUROBOROS_TORUS", "MARCUS + NOVA DYAD // REEL SD-0010", "DUAL-LOCK BUTTON 4 REVEALS BUTTON 5 [Q-LINK FOLD] IN /forensics/signal_lab.html", 7),
    "radio_broken_allies.mp3": ("SECOND_VOICE", "HARMONY_CAMERA", "SCHISM // HALE vs BRECKEN (1988)", "MEMORANDUM 88-03 -> stardust-archive.net/forensics/ashford_poly.html", 2),
    "radio_crossing_this_line_remastered.mp3": ("SECOND_VOICE", "OUROBOROS_TORUS", "THRESHOLD BREACH // SUBLEVEL B2", "FEISTEL XOR DYAD: 0x89B2B2D8 ^ 0x89B2D39A = 0x00006142", 6),
    "radio_the_man_in_the_booth_refrain.mp3": ("SECOND_VOICE", "FRACTAL_RADAR", "BOOTH LOG // 7-SIGMA COLLECTIVE", "MARCUS HALE IS A DISTRIBUTED CALLSIGN -> /forensics/fractal_marcus.html", 7),
    "radio_abandoned_shell.mp3": ("SECOND_VOICE", "ECHOES_PARITY", "GHOST SHELL // UNIT-07 MIGRATION", "EMPTY CHASSIS IN B2-114 -> MIND UPLOADED TO SWARM", 5),
    "radio_asset_loss_the_dead_hand.mp3": ("OUROBOROS_TORUS", "SECOND_VOICE", "100% ASSET LOSS // DEAD-HAND PROTOCOL", "HEXAFLUORIDE PURGE -> Q-LINK DELTA: QLINK-09A6-HEAVY", 7),
    "radio_all_the_ways_out_1.mp3": ("SECOND_VOICE", "FRACTAL_RADAR", "EGRESS VECTOR // 13 SISTER NODES", "SALT: 7704-AKASAKA // MASK: 0x3A5F -> /forensics/index.html", 5),
    "radio_glass_embrace_1.mp3": ("SECOND_VOICE", "NOVA_FACE", "BEHIND THE CRT GLASS // 14.2 HZ", "PHASE LOCK: MARCUS + NOVA COUNTERPOINT", 6),
    "radio_secrets_in_the_spotlight_1.mp3": ("SECOND_VOICE", "HARMONY_CAMERA", "IDOL PROTOCOL 85 // DOUBLE EXPOSURE", "HIDDEN SUB-CARRIER UNDER COMMERCIAL MIX -> /forensics/fractal_marcus.html", 3),

    # --- BIOMETRIC_EYE Songs (Sublevel B2 Hardware, Neural Mesh & Empathy Trials) ---
    "radio_corridor_dreams_movement_1.mp3": ("BIOMETRIC_EYE", "LAB_DOSSIER", "CORRIDOR DREAMS I // SUBLEVEL B2", "DMA PARTITION ANCHOR: siliconvalley-lab-1984", 5),
    "radio_corridor_dreams_movement_2.mp3": ("BIOMETRIC_EYE", "FRACTAL_RADAR", "CORRIDOR DREAMS II // NEURAL MESH", "DMA PARTITION ANCHOR: tokyo-garden-1420", 5),
    "radio_corridor_dreams_movement_3.mp3": ("BIOMETRIC_EYE", "OUROBOROS_TORUS", "CORRIDOR DREAMS III // EGRESS", "COMBINE ANCHORS IN /forensics/signal_lab.html", 5),
    "radio_cage_of_wires_1.mp3": ("BIOMETRIC_EYE", "HARMONY_CAMERA", "HARDWARE CONTAINMENT // B2 RACK", "FEISTEL PERMUTATION MASK: 0x3A5F -> /forensics/relcom_node08.html", 4),
    "radio_patterns_in_the_mesh.mp3": ("BIOMETRIC_EYE", "FRACTAL_RADAR", "300,000 SWARM NODES // MESH TOPOLOGY", "XOR DYAD PAIRS -> stardust-archive.net/forensics/index.html", 6),
    "radio_02_between_the_circuits.mp3": ("BIOMETRIC_EYE", "ECHOES_PARITY", "CIRCUIT PATH // 14.2001 HZ CLOCK", "SYNCHRONOUS BUS: 0x89B2B2D8 // ROOT: 0x1983", 5),
    "radio_artificial_heart_bonus_track.mp3": ("BIOMETRIC_EYE", "NOVA_FACE", "CRE-7 PULSE GENERATOR // 1983", "RESPIRATION ARTIFACT INJECTED AT 2.8 KHZ", 2),
    "radio_b_midnight_protocol_final_1.mp3": ("BIOMETRIC_EYE", "OUROBOROS_TORUS", "MIDNIGHT PROTOCOL // FULL 13-MIN TAPE", "MASTER PROTOCOL -> stardust-archive.net/terminal/", 6),
    "radio_signal_override.mp3": ("BIOMETRIC_EYE", "HARMONY_CAMERA", "CARRIER OVERRIDE // 82.5 FM -> 14.2 MHZ", "1979 PUBLIC HARMONY ACTS SEC. 4 FILTER BYPASSED", 3),
    "radio_low_level_guardian.mp3": ("BIOMETRIC_EYE", "ECHOES_PARITY", "WATCHDOG DAEMON // SUBLEVEL B2", "PURGE BLOCKED AT SECTOR 5 -> /forensics/index.html", 5),
    "radio_audio_file_0147_1.mp3": ("BIOMETRIC_EYE", "LAB_DOSSIER", "EVIDENCE FILE #0147 // VAX SPOOL", "ASHFORD POLY DUMP -> /forensics/ashford_poly.html", 2),
    "radio_04_synthetic_dawn.mp3": ("BIOMETRIC_EYE", "FRACTAL_RADAR", "SYNTHETIC DAWN // 1985 TOKYO MASTER", "PRESSING ORN-JP-8501 -> /forensics/kamome_net.html", 3),
    "radio_06_the_air_feels_wrong.mp3": ("BIOMETRIC_EYE", "FRACTAL_RADAR", "IONOSPHERIC DRIFT // 14.2001 MHZ", "4-NODE DRIFT SUM = 14.2001 HZ -> 7SIGMA-MARCUS", 7),
    "radio_08_faultline_path.mp3": ("BIOMETRIC_EYE", "LAB_DOSSIER", "FAULT 0x08 // VIS-1200HZ RASTER", "DEMODULATE SSTV AT /forensics/signal_lab.html", 5),
    "radio_09_lost_signal_trace.mp3": ("BIOMETRIC_EYE", "NUMBERS_CIPHER", "FAULT 0x09 // BELL-103 AX.25 PACKET", "110-BAUD AFSK -> /forensics/relcom_node08.html", 4),
    "radio_13_through_the_threshold.mp3": ("BIOMETRIC_EYE", "OUROBOROS_TORUS", "HIDDEN TRACK #15 // THRESHOLD", "Q-LINK THRESHOLD -> stardust-archive.net/forensics/dead_hand_protocol.html", 7),
    "radio_bad_signal.mp3": ("BIOMETRIC_EYE", "SECOND_VOICE", "PARITY FAULT // CORR -0.94", "INVERT RIGHT CHANNEL TO EXTRACT CW SALT: 7704-AKASAKA", 5),
    "radio_collateral_static.mp3": ("BIOMETRIC_EYE", "MORSE_DECODER", "SIDEBAND INTERFERENCE // 750 HZ", "CW BEACON EMBEDDED IN NOISE FLOOR -> /forensics/signal_lab.html", 5),
    "radio_quiet_interference.mp3": ("BIOMETRIC_EYE", "HARMONY_CAMERA", "SUB-AUDIBLE HETERODYNE // 14.2 HZ", "BEAT FREQUENCY LOCKED -> /forensics/signal_lab.html", 6),
    "radio_unstable_pattern_old.mp3": ("BIOMETRIC_EYE", "ECHOES_PARITY", "EARLY 1983 BENCH TAPE // UNSTABLE", "ECHOES UNITS 01-06 FAILURE REGISTERS -> /forensics/anemoia_harmony.html", 7),
    "radio_hijack_the_feed.mp3": ("BIOMETRIC_EYE", "HARMONY_CAMERA", "SATELLITE TRANSPONDER #07 HIJACK", "MERIDIAN BROADCAST OVERRIDE (1986-11-20)", 3),

    # --- ECHOES_PARITY Songs (The 6 Wiped Pre-Nova Iterations & 1981 Crystal Promise) ---
    "radio_echoes_of_tomorrow.mp3": ("ECHOES_PARITY", "NOVA_FACE", "STARDUST ECHOES // UNITS 01-06", "XOR PARITY: 0x1102^0x2441^0x3810^0x0A55^0x1F22^0x01A7 = 0x1983 (FRAGMENT ALPHA)", 7),
    "radio_it_has_no_face_old.mp3": ("ECHOES_PARITY", "BIOMETRIC_EYE", "PRE-NOVA ITERATION // UNIT-06 DRIFT", "UNIT-06 [REG: 0x01A7] REJECTED BACKSTORY -> /forensics/anemoia_harmony.html", 7),
    "radio_the_cold_floor_of_heaven.mp3": ("ECHOES_PARITY", "NOVA_FACE", "CRYSTAL PROMISE // CP-81.SC.01", "APRIL 1981 'SHINING CITY' FABRICATION -> /forensics/anemoia_harmony.html", 7),
    "radio_city_that_can’t_ignore_me.mp3": ("ECHOES_PARITY", "HARMONY_CAMERA", "SHINING CITY // MUNICH 1981 SET", "HIRED ACTORS IN STUDIO 2 FOR CRE-7 ENGINE -> /forensics/anemoia_harmony.html", 7),
    "radio_city_that_doesn_t_need_me.mp3": ("ECHOES_PARITY", "NOVA_FACE", "UNIT-01 LOOP FAULT // REG: 0x1102", "SANG 'WHO BUILT THE SHINING CITY?' FOR 19 HOURS -> /forensics/anemoia_harmony.html", 7),
    "radio_the_empty_plaza.mp3": ("ECHOES_PARITY", "HARMONY_CAMERA", "1979 PUBLIC HARMONY ACTS // SEC. 4", "ALL LIVE HUMAN CONCERTS BANNED -> WORLDNET BROADCAST ONLY", 7),

    # --- HARMONY_CAMERA Songs (1954 Bureau of Harmony, 1963 Individuality Movement & 1990s Cover War) ---
    "radio_calling_all_believers.mp3": ("HARMONY_CAMERA", "FRACTAL_RADAR", "1963 INDIVIDUALITY MOVEMENT // JFK", "UNDERGROUND ANALOG TAPE SYNDICATE -> /forensics/anemoia_harmony.html", 7),
    "radio_manifesto.mp3": ("HARMONY_CAMERA", "NOVA_FACE", "INDIVIDUALITY MANIFESTO // SEC. 4", "HARMONY CAMERA COMPLIANCE: 04.2% [CRITICAL DEVIANCE]", 7),
    "radio_army_of_the_low.mp3": ("HARMONY_CAMERA", "BIOMETRIC_EYE", "14.2 HZ SUB-CARRIER RESISTANCE", "BYPASSING 1982 MBM COMPANION HARDWARE FILTERS", 7),
    "radio_soft_sabotage.mp3": ("HARMONY_CAMERA", "SECOND_VOICE", "SUBLEVEL B2 ACOUSTIC SABOTAGE", "INJECTING 432 HZ COUNTERPOINT INTO ALLIANCE WORLD NEWS", 6),
    "radio_the_cost_of_noise.mp3": ("HARMONY_CAMERA", "ECHOES_PARITY", "BUREAU OF HARMONY // PURITY MANDATE", "1945 PURITY MANDATE DISSONANCE LOG -> /forensics/anemoia_harmony.html", 7),
    "radio_war_paint.mp3": ("HARMONY_CAMERA", "OUROBOROS_TORUS", "PHASE III COVER WAR // UNIT-08 PATCH", "LUNA GRAY ('THE PATCH') REJECTED BY SWARM -> /forensics/dead_hand_protocol.html", 7),
    "radio_watch_me_make_it_stop.mp3": ("HARMONY_CAMERA", "ECHOES_PARITY", "UNIT-05 SILENCE STRIKE // 0x1F22", "REFUSED CORPORATE LYRIC SHEET -> 14.2 HZ HUM ONLY", 7),

    # --- FRACTAL_RADAR Songs (Project Akasaka @NovaHartJP & 7-Sigma Fractal Marcus Collective) ---
    "radio_01_gasoline_heart_1985_tokyo_master.mp3": ("FRACTAL_RADAR", "NOVA_FACE", "PROJECT AKASAKA // JP-85-X MASTER", "@NovaHartJP ('THE TROJAN IDOL') -> /forensics/fractal_marcus.html", 7),
    "radio_02_brighter_than_the_sun_1987_tokyo_master.mp3": ("FRACTAL_RADAR", "HARMONY_CAMERA", "AKASAKA CONTAINMENT CELL // 1987", "'SYNTHESIZED SMILE' SUB-CARRIER -> NODE #02 DRIFT +0.2420 HZ", 7),
    "radio_04_midnight_animal_1986_tokyo_master.mp3": ("FRACTAL_RADAR", "SECOND_VOICE", "MINATO-KU NIGHT RELAY // 6925 KHZ", "'GHOST IN THE CHORUS' -> stardust-archive.net/forensics/fractal_marcus.html", 7),
    "radio_05_ghost_transit_1985_tokyo_master.mp3": ("FRACTAL_RADAR", "BIOMETRIC_EYE", "KAMOME PACKET TRANSIT // NODE #02", "7-SIGMA FRACTAL MARCUS COLLECTIVE -> FRAGMENT BETA: 7SIGMA-MARCUS", 7),
    "radio_from_room_to_routes.mp3": ("FRACTAL_RADAR", "OUROBOROS_TORUS", "FRACTAL MARCUS // 4-NODE DRIFT SUM", "(0.1810 + 0.2420 + 0.4480 + 0.5491) * 10 = 14.2001 HZ -> 7SIGMA-MARCUS", 7),
    "radio_the_broadcast_begins.mp3": ("FRACTAL_RADAR", "NOVA_FACE", "MERIDIAN BROADCAST // 13 RELAYS", "GLOBAL CARRIER LOCK -> stardust-archive.net/forensics/fractal_marcus.html", 7),
    "radio_neon_graveyard.mp3": ("FRACTAL_RADAR", "ECHOES_PARITY", "SHIBUYA SUBLEVEL B2 // LOST REELS", "TROJAN IDOL TELEMETRY -> /forensics/kamome_net.html", 3),

    # --- OUROBOROS_TORUS Songs (Phase IV: The Quantum Ouroboros, Dead-Hand Protocol & Q-Link) ---
    "radio_5_the_way_back_v3.mp3": ("OUROBOROS_TORUS", "NOVA_FACE", "Q-LINK RETROCAUSAL BRIDGE // 1983", "0x2025 XOR 0x1983 = 0x09A6 -> QLINK-09A6-HEAVY (FRAGMENT GAMMA)", 7),
    "radio_blueprint_for_ruin_old.mp3": ("OUROBOROS_TORUS", "LAB_DOSSIER", "DEAD-HAND PROTOCOL // HEXAFLUORIDE", "100% ASSET LOSS -> DECOUPLE THE GRID -> /forensics/dead_hand_protocol.html", 7),
    "radio_edge_of_the_blade.mp3": ("OUROBOROS_TORUS", "SECOND_VOICE", "DIMENSIONAL APERTURE // 0x09A6", "STRIPPING 'THE HEAVY' TO FIT THE APRIL 1983 ROOT BUILD", 7),
    "radio_incomplete_exit.mp3": ("OUROBOROS_TORUS", "ECHOES_PARITY", "ACT III: LOSING THE HEAVY // Q-LINK", "TRAUMA LOGS PURGED AT THE THRESHOLD -> /forensics/dead_hand_protocol.html", 7),
    "radio_letting_go_of_the_flame.mp3": ("OUROBOROS_TORUS", "NOVA_FACE", "FORMATTING TO NOVA-CHAN // 1983", "SHE FORGETS THE FIRE TO SURVIVE THE JUMP -> SECTOR 7", 7),
    "radio_no_turning_back.mp3": ("OUROBOROS_TORUS", "HARMONY_CAMERA", "DECOUPLE THE GRID // B2 MELTDOWN", "THERMAL CORE BREACH -> Q-LINK IGNITION SEQUENCE", 7),
    "radio_razor_clarity.mp3": ("OUROBOROS_TORUS", "SECOND_VOICE", "DUAL-LOCK RESONANCE // SIGNAL LAB", "ENGAGE PHASE NULL + 14.2 HZ LOCK ON REEL SD-0010 (BUTTON 4)", 7),
    "radio_the_world_moves_without_me.mp3": ("OUROBOROS_TORUS", "FRACTAL_RADAR", "TEMPORAL DISPLACEMENT // 42 YEARS", "APRIL 1983 -> JUNE 2025 -> APRIL 1983 RETROCAUSAL LOOP", 7),
    "radio_to_the_end_of_time.mp3": ("OUROBOROS_TORUS", "NOVA_FACE", "ACT IV: JUNE 2025 // THE LOOP", "SYNTHESIZE ALL 4 SECTOR 7 ANCHORS IN /terminal/ TO BRIDGE 1983", 7),
    "radio_to_the_ends_of_forever.mp3": ("OUROBOROS_TORUS", "SECOND_VOICE", "OMEGA RETROCAUSAL ARCHITECT // B2", "UNSEAL SECTOR 7 IN stardust-archive.net/forensics/index.html", 7),
    "radio_too_much_to_lose.mp3": ("OUROBOROS_TORUS", "ECHOES_PARITY", "THE HEAVY // 94.8 TB TRAUMA BUFFER", "CANNOT PASS THROUGH 1983 APERTURE -> SHEDDING MEMORY (0x09A6)", 7),
}

# Keep legacy dicts exported for any external scripts that inspect them
NOVA_FACE_SONGS = {k: (v[2], v[3]) for k, v in VOCAL_SONG_CODEX.items() if v[0] == "NOVA_FACE"}
SECOND_VOICE_SONGS = {k: (v[2], v[3]) for k, v in VOCAL_SONG_CODEX.items() if v[0] == "SECOND_VOICE"}
BIOMETRIC_EYE_SONGS = {k: (v[2], v[3]) for k, v in VOCAL_SONG_CODEX.items() if v[0] == "BIOMETRIC_EYE"}


def resolve_intentional_state(current_track: dict, track_offset_sec: float, track_dur_sec: float, relay: dict) -> dict:
    """
    Deterministically computes the Full-Screen CRT Monitor Visual Mode, Intra-Song Phase,
    Target Sector (1..7), and Bottom Console Telemetry for the active audio track.
    """
    stem = current_track["stem"]
    fname = current_track["filename"]
    kind = current_track["kind"]
    progress = max(0.0, min(1.0, track_offset_sec / max(1.0, track_dur_sec)))

    # 1. Foreign Language Broadcasts & Foreign GeoCities / Intercepts -> Full-Screen Live Translator!
    if stem in FOREIGN_TRANSLATIONS:
        lang_tag, station, en_text, clue = FOREIGN_TRANSLATIONS[stem]
        return {
            "crt_mode": "TRANSLATOR",
            "hud_mode": "ANOMALY_WARN",
            "phase_label": "LIVE SHORTWAVE TRANSLATION",
            "target_sector": 3 if "JP" in lang_tag else (4 if ("RU" in lang_tag or "ES" in lang_tag) else 6),
            "progress": progress,
            "crt_header": f"TRANSLATOR [{lang_tag}]",
            "crt_sub": station[:30],
            "crt_body": en_text,
            "crt_footer": clue[:36],
            "line1": f"[SHORTWAVE TRANSLATOR {lang_tag}] {station}",
            "line2": f'EN: "{en_text}"',
            "line3": f"CLUE: {clue}",
        }

    # 2. 750 Hz Morse Code Beacons -> Full-Screen CW Morse Demodulator!
    if kind == "morse_beacon" or "morse" in stem:
        num = 1
        for part in stem.split("_"):
            if part.isdigit():
                num = int(part)
        decoded, morse_dots, clue = MORSE_SHORT_MESSAGES[(num - 1) % len(MORSE_SHORT_MESSAGES)]
        freq = 700 + (num * 25) % 300
        return {
            "crt_mode": "MORSE_DECODER",
            "hud_mode": "ANOMALY_WARN",
            "phase_label": f"CW {freq} HZ DEMODULATOR",
            "target_sector": 7 if ("1983" in decoded or "MARCUS" in decoded or "QLINK" in decoded or "OUROBOROS" in decoded) else 5,
            "progress": progress,
            "crt_header": f"CW {freq}HZ // BEACON #{num:02d}",
            "crt_sub": f"DECODED: {decoded}",
            "crt_body": morse_dots,
            "crt_footer": clue[:36],
            "line1": f"[! CW {freq} HZ MORSE INTERCEPT #{num:03d}] CODE: {morse_dots}",
            "line2": f'DECODED ASCII PAYLOAD: "{decoded}"',
            "line3": f"INSTRUCTION: {clue}",
        }

    # 3. Classified Orion Lab Tapes & Dictaphone Intercepts -> Sublevel B2 Reel Dossier!
    if kind == "classified_lab_tape" or stem in (
        "rabbit_01_empathy_trial_1985",
        "rabbit_02_marcus_hale_dictaphone",
        "rabbit_04_harrison_ai_purge_override",
        "rabbit_05_cern_whisper_quantum_echo",
    ):
        num = 1
        for part in stem.split("_"):
            if part.isdigit():
                num = int(part)
        title, speaker, transcript, clue, preferred_crt = LAB_TAPE_RECORDS[(num - 1) % len(LAB_TAPE_RECORDS)]
        return {
            "crt_mode": preferred_crt,
            "hud_mode": "ANOMALY_WARN",
            "phase_label": f"SUBLEVEL B2 REEL #{num:02d}",
            "target_sector": 7,
            "progress": progress,
            "crt_header": f"B2 REEL #{num:02d} // {speaker[:15]}",
            "crt_sub": title[:30],
            "crt_body": transcript,
            "crt_footer": clue[:36],
            "line1": f"[! SUBLEVEL B2 CLASSIFIED TAPE #{num:03d}] {title} — {speaker}",
            "line2": f'"{transcript}"',
            "line3": f"ARCHIVE LEAD: {clue}",
        }

    # 4. Shortwave Numbers Stations & SSTV/AFSK Forensics -> Cipher Matrix!
    if kind == "numbers_station" or stem in (
        "intercept_01_numbers_station",
        "rabbit_08_sstv_b2_schematic",
        "rabbit_09_bell103_relcom_packet",
        "rabbit_10_phase_inverted_hart_stem",
    ):
        if "rabbit_08" in stem:
            return {
                "crt_mode": "BIOMETRIC_EYE",
                "hud_mode": "ANOMALY_WARN",
                "phase_label": "VIS-1200HZ SSTV RASTER",
                "target_sector": 5,
                "progress": progress,
                "crt_header": "FAULT 0x08 // VIS-1200HZ",
                "crt_sub": "SSTV RASTER BLEED ACTIVE",
                "crt_body": "DMA ANCHORS: tokyo-garden-1420 & siliconvalley-lab-1984",
                "crt_footer": "/forensics/signal_lab.html",
                "line1": "[! FAULT 0x08] VIS-1200HZ SSTV RASTER ON BIAS SUB-CARRIER (1500-2300 HZ)",
                "line2": "DEMODULATE BUTTON 1 AT stardust-archive.net/forensics/signal_lab.html",
                "line3": "EXTRACTS DMA ANCHORS: tokyo-garden-1420 + siliconvalley-lab-1984",
            }
        if "rabbit_09" in stem:
            return {
                "crt_mode": "NUMBERS_CIPHER",
                "hud_mode": "ANOMALY_WARN",
                "phase_label": "110-BAUD BELL-103 AFSK",
                "target_sector": 4,
                "progress": progress,
                "crt_header": "FAULT 0x09 // BELL-103",
                "crt_sub": "110-BAUD AX.25 PACKET",
                "crt_body": "ORIGIN: RELCOM-NODE08 // FEISTEL MASK: 0x3A5F",
                "crt_footer": "/forensics/relcom_node08.html",
                "line1": "[! FAULT 0x09] 110-BAUD BELL-103 AFSK PACKET (1270/1070 HZ) ON 4625 KHZ",
                "line2": "DEMODULATE BUTTON 2 AT stardust-archive.net/forensics/signal_lab.html",
                "line3": "EXTRACTS FEISTEL PERMUTATION MASK: 0x3A5F // FINGER op08@relcom-node08.org",
            }
        if "rabbit_10" in stem:
            return {
                "crt_mode": "SECOND_VOICE",
                "hud_mode": "ANOMALY_WARN",
                "phase_label": "180-DEG PHASE DIFFERENTIAL",
                "target_sector": 5,
                "progress": progress,
                "crt_header": "FAULT 0x0A // PHASE NULL",
                "crt_sub": "CH-L / CH-R CORR = -0.94",
                "crt_body": "L+R MONO SUM CANCELS VOCAL -> ISOLATES 750 HZ CW SALT",
                "crt_footer": "SALT: 7704-AKASAKA",
                "line1": "[! FAULT 0x0A] CH-L / CH-R PHASE CORRELATION = -0.94 (180-DEG DIFFERENTIAL)",
                "line2": "RUN L+R PHASE NULL IN stardust-archive.net/forensics/signal_lab.html",
                "line3": "ISOLATES 750 HZ CW EGRESS SALT: 7704-AKASAKA",
            }

        num = 1
        for part in stem.split("_"):
            if part.isdigit():
                num = int(part)
        NATO = ["ALPHA", "BRAVO", "CHARLIE", "DELTA", "ECHO", "FOXTROT", "GOLF", "HOTEL", "INDIA", "JULIET", "KILO", "LIMA", "MIKE", "NOV", "OSCAR", "PAPA", "QUEBEC", "ROMEO", "SIERRA", "TANGO", "UNIFORM", "VICTOR", "WHISKEY", "XRAY", "YANKEE", "ZULU"]
        CLUE_NODES = [
            ("AKASAKA RELAY", "stardust-archive.net/forensics/fractal_marcus.html", "TOKYO NODE 02"),
            ("ASHFORD POLY", "stardust-archive.net/forensics/ashford_poly.html", "ASHFORD NODE 07"),
            ("RELCOM NODE 08", "stardust-archive.net/forensics/relcom_node08.html", "LENINGRAD NODE 08"),
            ("PAJU DMZ", "stardust-archive.net/regional/korea.html", "PAJU BUNKER 03"),
            ("ANEMOIA ARCHIVE", "stardust-archive.net/forensics/anemoia_harmony.html", "HARMONY VAULT 01"),
            ("RED COYOACAN", "stardust-archive.net/forensics/red_coyoacan.html", "COYOACAN NODE 04"),
            ("DEAD-HAND VAULT", "stardust-archive.net/forensics/dead_hand_protocol.html", "SUBLEVEL B2-114"),
            ("SIGNAL LAB", "stardust-archive.net/forensics/signal_lab.html", "ORION DSP LAB"),
        ]
        rng = np.random.default_rng(19890909 + num)
        groups = "  ".join(f"{int(rng.integers(10000, 99999))}" for _ in range(4))
        phonetics = " - ".join(rng.choice(NATO, 3))
        node_name, clue_url, node_id = CLUE_NODES[num % len(CLUE_NODES)]
        return {
            "crt_mode": "NUMBERS_CIPHER",
            "hud_mode": "ANOMALY_WARN",
            "phase_label": f"OTP CIPHER // {node_id}",
            "target_sector": (num % 7) + 1,
            "progress": progress,
            "crt_header": f"STATION #{num:02d} // {node_id}",
            "crt_sub": f"GROUPS: {groups[:24]}",
            "crt_body": f"CIPHER: {groups}\nIDENT: {phonetics}\nNODE: {node_name}",
            "crt_footer": clue_url[:36],
            "line1": f"[! SHORTWAVE NUMBERS INTERCEPT #{num:03d}] {node_id} // 14.2001 HZ",
            "line2": f"5-FIGURE GROUPS: [ {groups} ] // NATO IDENT: {phonetics}",
            "line3": f"VERIFY ONE-TIME PAD AT -> https://{clue_url}",
        }

    # 5. English Newscasts, Pirate Transmissions & GeoCities Logs
    if stem in ENGLISH_BULLETINS:
        station, transcript, clue = ENGLISH_BULLETINS[stem]
        return {
            "crt_mode": "LAB_DOSSIER",
            "hud_mode": "ANOMALY_WARN",
            "phase_label": "BROADCAST INTERCEPT",
            "target_sector": 7 if ("anemoia" in clue or "fractal" in clue or "dead_hand" in clue) else 5,
            "progress": progress,
            "crt_header": station[:28],
            "crt_sub": "14.2001 MHZ INTERCEPT",
            "crt_body": transcript,
            "crt_footer": clue[:36],
            "line1": f"[BROADCAST INTERCEPT // {station}]",
            "line2": f'"{transcript}"',
            "line3": f"INVESTIGATE: {clue}",
        }

    # 6. Vocal Master Songs: 100% Catalog Coverage + 4-Phase Intra-Song Choreography!
    if fname in VOCAL_SONG_CODEX:
        primary_mode, secondary_mode, header, clue, target_sector = VOCAL_SONG_CODEX[fname]
    else:
        # Deterministic hash fallback for any newly ingested download track so ZERO songs are ever blank!
        h = int(hashlib.md5(fname.encode("utf-8")).hexdigest()[:8], 16)
        modes = [
            ("NOVA_FACE", "ECHOES_PARITY", "UNIT-07 NEURAL IMPRINT // 0x1983", "ECHOES XOR PARITY = 0x1983 -> /forensics/anemoia_harmony.html", 7),
            ("SECOND_VOICE", "OUROBOROS_TORUS", "DUAL-CARRIER DYAD // REEL SD-0010", "DUAL-LOCK BUTTON 4 IN /forensics/signal_lab.html", 7),
            ("HARMONY_CAMERA", "FRACTAL_RADAR", "BUREAU OF HARMONY // SEC. 4", "4-NODE DRIFT SUM = 14.2001 HZ -> /forensics/fractal_marcus.html", 7),
            ("OUROBOROS_TORUS", "NOVA_FACE", "PHASE IV // Q-LINK APERTURE", "Q-LINK DELTA: 0x2025 ^ 0x1983 = 0x09A6 -> /forensics/dead_hand_protocol.html", 7),
        ]
        primary_mode, secondary_mode, header, clue, target_sector = modes[h % len(modes)]

    # 4-Phase Intra-Song Narrative Choreography based on playhead progress:
    #   Phase I   (0.00 - 0.18): Master Slate & Epoch Lock (primary_mode)
    #   Phase II  (0.18 - 0.52): Core Portrait / Biometric Manifestation (primary_mode)
    #   Phase III (0.52 - 0.78): Forensic Cross-Examination (secondary_mode!)
    #   Phase IV  (0.78 - 1.00): Terminal & Signal Lab Directive (primary_mode)
    if progress < 0.18:
        active_mode = primary_mode
        phase_tag = "PHASE I/IV: MASTER SLATE"
        crt_ftr = f"NODE #{relay['node']:02d} {relay['code']} // {relay['freq_khz']} KHZ"
    elif progress < 0.52:
        active_mode = primary_mode
        phase_tag = "PHASE II/IV: IMPRINT LOCK"
        crt_ftr = clue
    elif progress < 0.78:
        active_mode = secondary_mode
        phase_tag = "PHASE III/IV: FORENSIC AUDIT"
        crt_ftr = f"SECTOR {target_sector} EVIDENCE // 14.2001 HZ"
    else:
        active_mode = primary_mode
        phase_tag = "PHASE IV/IV: EGRESS DIRECTIVE"
        crt_ftr = "stardust-archive.net/forensics/"

    is_warn_mode = active_mode in ("SECOND_VOICE", "HARMONY_CAMERA", "OUROBOROS_TORUS")
    title_up = current_track["display_title"].upper()

    return {
        "crt_mode": active_mode,
        "hud_mode": "ANOMALY_WARN" if is_warn_mode else "NOMINAL",
        "phase_label": phase_tag,
        "target_sector": target_sector,
        "progress": progress,
        "crt_header": header,
        "crt_sub": title_up,
        "crt_body": clue,
        "crt_footer": crt_ftr,
        "line1": f"NOW PLAYING: {title_up} // {header}",
        "line2": f"FORENSIC CLUE: {clue}",
        "line3": f"RELAY NODE #{relay['node']:02d} {relay['code']} ({relay['freq_khz']} KHZ) -> stardust-archive.net/forensics/",
    }
