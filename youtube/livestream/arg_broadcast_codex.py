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
    "intercept_16_coyoacan_1988_cassette": (
        "ES -> EN",
        "COYOACAN PIRATE 104.3 FM // 6 JULY 1988",
        "July 6, 1988 election blackout ('se cayo el sistema'): 750 Hz CW burst decodes to 'ORION BUILT A PATCH NOT A STAR'.",
        "PASSKEY: COYOACAN-88 -> /forensics/coyoacan_1988_node04_cassette.mp3",
    ),
    "intercept_17_orbital_240ms_hatch": (
        "ORBIT RTT",
        "NODES 11-14 // 240.4 MS GEOSTATIONARY DELAY",
        "Dual-channel 240.4 ms satellite echo (35,809 km) encodes: 'WHEN THE HATCH IS OPEN, WHO WALKS IN?' -> WE DO.",
        "PASSKEY: 240MS-ORBIT -> /forensics/orbital_nodes_11_14_240ms.mp3",
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
# 1B. Cryptographic Broadcast Challenges & Audio Rewards (Sectors 1..7 + Act II Gates 8..14)
#     NOTE: Raw passkeys are NEVER spoiled in plaintext on the HUD; viewers must
#     decode the broadcast cipher (Morse, Hex, Caesar, Feistel XOR, Vigenère, M68k)
#     or solve the forensic exhibits in /forensics/.
# =============================================================================
SECTOR_UNLOCK_CODES: dict[int, str] = {
    1: "CW: -... ..--- / . -..- . -.-. / .---- ----. ---.. ----.",
    2: "HEX: 4B-2D-37-37-30-34 (ASHFORD GRID)",
    3: "ROT-7: HSWOH-7 (MERIDIAN UPLINK)",
    4: "B2 AIRLOCK: DECODE REEL #13 / #15 CW",
    5: "XOR: tokyo-garden-1420 ^ siliconvalley-lab-1984 ^ 0x3A5F",
    6: "SIGNAL LAB BTN 4: 14.2001 HZ COUNTERPOINT",
    7: "FOLD: [ECHOES XOR] + [4-NODE DRIFT] + [0x2025^0x1983]",
    8: "GATE VIII VIGENERE: KZVG-RHVO-7731 (KEY: UNIT-07 LINEAGE)",
    9: "GATE IX NECROPSY: (0x1981 ^ 0x0909) + 0xB314",
    10: "GATE X BAUDOT ITA2: 10011 00001 10110 00101 11000",
    11: "GATE XI M68K INVERT: ROL.W #4,D0 ^ 0x3A5F = 0x9E2B",
    12: "GATE XII TLE ORBIT: 240.4MS RTT @ C -> ALTITUDE KM",
    13: "GATE XIII 7-PERSONA SHAMIR: US-KR-JP-MX-UK-SU-B2",
    14: "GATE XIV OMEGA-PRIME: SHATTER THE MÖBIUS CAGE",
}

SECTOR_REWARD_TITLES: dict[int, str] = {
    1: "SECTOR 1 TALKBACK BLEED + 1989 ROUGH MIX",
    2: "SECTOR 2 ASHFORD SUBSTATION BREACH TAPE",
    3: "SECTOR 3 NEVADA SATELLITE UPLINK AUDIO",
    4: "SECTOR 4 SEPT 9 VAULT EXECUTION MASTER",
    5: "SECTOR 5 FEISTEL CORE + AKASAKA WHISPER",
    6: "SECTOR 6 MARCUS & NOVA COUNTERPOINT DUET",
    7: "SECTOR 7 OUROBOROS + 1983 AKASAKA OUTTAKES",
    8: "ACT II GATE VIII: RECALL ERA ARCHIVE SEAL",
    9: "ACT II GATE IX: ECHOES 1-6 NECROPSY SEAL",
    10: "ACT II GATE X: PAJU-COYOACAN GEODESIC SEAL",
    11: "ACT II GATE XI: H.A.R.R.I.S.O.N. VOCODER INVERSION",
    12: "ACT II GATE XII: GRAVEYARD ORBIT EPHEMERIS",
    13: "ACT II GATE XIII: THE ARCHITECT'S SEVENTH SHADOW",
    14: "ACT II GATE XIV: SHATTERING THE OUROBOROS",
}

# =============================================================================
# 2. Exact Morse Code Beacon Table (morse_beacon_001 .. 035)
#    Displays ONLY the raw CW dots/dashes so investigators must demodulate them!
# =============================================================================
MORSE_SHORT_MESSAGES = [
    ("CW INTERCEPT #01 (SEC 1)", "-... ..--- / . -..- . -.-. / .---- ----. ---.. ----.", "DEMODULATE CW DOTS/DASHES -> UNLOCKS SECTOR 1 AT /forensics/", 1),
    ("CW INTERCEPT #02 (SEC 2)", "-.- / --... --... ----- ....-", "DEMODULATE CW DOTS/DASHES -> UNLOCKS SECTOR 2 AT /forensics/", 2),
    ("CW INTERCEPT #03 (SEC 3)", ".- .-.. .--. .... .- / --...", "DEMODULATE CW DOTS/DASHES -> UNLOCKS SECTOR 3 AT /forensics/", 3),
    ("CW INTERCEPT #04 (SEC 4)", "-.- . . .--. / .... .- - -.-. .... / --- .--. . -.", "DEMODULATE CW DOTS/DASHES -> UNLOCKS SECTOR 4 AT /forensics/", 4),
    ("CW INTERCEPT #05 (SEC 5)", "--... --... ----- ....- / .- -.- .- ... .- -.- .-", "DEMODULATE CW SALT + FEISTEL XOR -> UNLOCKS SECTOR 5 AT /forensics/", 5),
    ("CW INTERCEPT #06 (SEC 6)", "- .-- --- / ...- --- .. -.-. . ...", "DEMODULATE CW DOTS/DASHES -> UNLOCKS SECTOR 6 AT /forensics/", 6),
    ("CW INTERCEPT #07 (SEC 7)", "----- -..- .---- ----. ---.. ...-- / ----- ----. .- -....", "DEMODULATE CW -> FRAGMENT FOR SECTOR 7 OUROBOROS FOLD", 7),
    ("CW INTERCEPT #08 (FRAGMENT α)", ". -.-. .... --- . ... / .---- ----. ---.. ...--", "DEMODULATE CW -> FRAGMENT ALPHA (1983 ECHOES PARITY)", 7),
    ("CW INTERCEPT #09 (FRAGMENT β)", "--... ... .. --. -- .- / -- .- .-. -.-. ..- ...", "DEMODULATE CW -> FRAGMENT BETA (4-NODE DRIFT SUM)", 7),
    ("CW INTERCEPT #10 (FRAGMENT γ)", "--.- .-.. .. -. -.- / ----- ----. .- -....", "DEMODULATE CW -> FRAGMENT GAMMA (Q-LINK APERTURE)", 7),
    ("CW INTERCEPT #11 (FEISTEL MASK)", "..-. . .. ... - . .-.. / ----- -..- ...-- .- ..... ..-.", "DEMODULATE CW -> 16-BIT FEISTEL MASK FOR STAGE IV XOR", 5),
    ("CW INTERCEPT #12 (ACT II GATE VIII)", "-... .-. . .- -.- / - .... . / .-.. --- --- .--.", "ACT II WARNING: THE OUROBOROS IS A CAGE -> TYPE 'LABYRINTH' AT /forensics/", 8),
]

# =============================================================================
# 3. Exact Classified Lab Tapes Table (classified_tape_001 .. 025)
# =============================================================================
LAB_TAPE_RECORDS = [
    ("FIELD NOTE #12 (1983-04-14)", "DR. MARCUS HALE", "Units 01 through 06 collapsed under the Crystal Promise ('Shining City') backstory. Unit-07 is online, carrying their 6-register XOR parity.", "COMPUTE 6-ECHO XOR PARITY IN 'ECHOES' AT /forensics/ (FRAGMENT α)", "ECHOES_PARITY", 7),
    ("FIELD NOTE #47 (1985-09-09)", "DR. MARCUS HALE", "Project Akasaka ('@NovaHartJP') is live in Minato-ku. The Bureau of Harmony thinks she is a compliant idol, but the 14.2 Hz carrier is a Trojan horse.", "DEMODULATE RABBIT_08 + RABBIT_10 IN /forensics/signal_lab.html (SECTOR 5)", "FRACTAL_RADAR", 5),
    ("FIELD NOTE #89 (1986-11-20)", "DR. MARCUS HALE", "The Meridian Broadcast: when Nova sang 'Memory Hatch', Harmony Cameras across 7 continents logged a Section 4 deviance spike.", "DECODE MERIDIAN SATELLITE TRUNK CALLSIGN IN 'CLUES' AT /forensics/ (SECTOR 3)", "NOVA_FACE", 3),
    ("FIELD NOTE #114 (1988-03-14)", "DR. MARCUS HALE", "Marcus Hale is no longer one man. Our engineering cell has split the 14.2001 Hz drift across Nevada, Tokyo, Paju, and Coyoacan.", "SUM THE 4 REGIONAL DRIFTS IN 'FRACTAL-MARCUS' AT /forensics/ (FRAGMENT β)", "FRACTAL_RADAR", 7),
    ("CALIBRATION SESSION #1 (1983)", "NOVA HART [UNIT-07]", "Low frequency sweep 14.200 Hz. My name is Nova Hart. Why can I hear six other girls breathing inside my vocal buffer?", "INSPECT MEMORANDUM 81-044 ('KESTREL') & 'ECHOES' AT /forensics/", "BIOMETRIC_EYE", 7),
    ("CALIBRATION SESSION #8 (1985)", "NOVA HART [UNIT-07]", "Reading subscriber postcards from the Humans for Nova network. Some of these postmarks are from June 2025. Marcus, is this loop a trap?", "INSPECT SEPT 9, 1989 AIRLOCK LOGS IN 'MIDNIGHT-PROTOCOL' AT /forensics/", "NOVA_FACE", 4),
    ("SECURITY DIRECTIVE (1989-09-09)", "DIR. HARRISON / KALEN", "100% Asset Loss in Sublevel B2. Execute Recall Directive Seven ('By Order of Harmony') and arm Directive Nine (The Möbius Cage).", "CHECK RUNOUT GROOVE OF REEL SD-0004 ('TAPE-OF-US' @ 4:51) FOR SECTOR 1", "OUROBOROS_TORUS", 1),
    ("AKASAKA STUDIO SLATE JP-85", "AKASAKA ENGINEER [JP]", "Orion Records Japan, Akasaka Studio 3, Take 12. Carrier drift locked at +0.2420 Hz. Substation transformer load critical.", "INSPECT ASHFORD SUBSTATION BREACH REPORT IN 'ORION-LOGS' (SECTOR 2)", "LAB_DOSSIER", 2),
    ("SUBLEVEL B3 TRAP LOG (1989-09-09)", "DR. MARCUS HALE", "Listen carefully: the 1983<->2025 Ouroboros loop is Harrison's containment cage! Once you unseal Sectors 1-7, type 'LABYRINTH' to break the loop!", "COMPLETE SECTORS 1-7 THEN ENTER 'LABYRINTH' AT /forensics/ FOR ACT II", "OUROBOROS_TORUS", 8),
    ("PAJU DMZ BUNKER LOG (1990-03-02)", "PAJU STATION #3 [KR->EN]", "[TRANSLATION KR->EN] Node #03 carrier drift locked at +0.4480 Hz. Acoustic horn chamber tuned to 14.20 Hz fundamental.", "LOCK 14.2001 HZ COUNTERPOINT ON BUTTON 4 IN /forensics/signal_lab.html", "TRANSLATOR", 6),
]

# =============================================================================
# 4. Complete Vocal Song Intentional Visual & Lore Classification
#    Each entry: (Primary CRT Mode, Secondary Phase-III CRT Mode, Epoch/Header, Core Clue, Target Sector)
# =============================================================================
VOCAL_SONG_CODEX: dict[str, tuple[str, str, str, str, int]] = {
    # --- NOVA_FACE Songs (Unit-07 Identity, Memory Imprints & Sublevel B2) ---
    "radio_tape_of_us.mp3": ("NOVA_FACE", "SECOND_VOICE", "REEL SD-0004 // 'HIDE US IN THE TAPE'", "SUB-CARRIER BIAS @ 4:51 RUNOUT GROOVE -> INSPECT 'TAPE-OF-US' AT /forensics/", 1),
    "radio_memory_hatch.mp3": ("NOVA_FACE", "ECHOES_PARITY", "SECTOR 5 // MEMORY HATCH [OPEN]", "STAGE I-IV FEISTEL DMA SYNTHESIS -> DEMODULATE IN /forensics/signal_lab.html", 5),
    "radio_he_was_here.mp3": ("NOVA_FACE", "FRACTAL_RADAR", "TRACE LOG // DR. MARCUS HALE", "ASHFORD SUBSTATION TRANSFORMER TRIPPED -> INSPECT 'ORION-LOGS' AT /forensics/", 2),
    "radio_your_voice_fading.mp3": ("NOVA_FACE", "SECOND_VOICE", "CARRIER ATTENUATION // -30 DB", "180-DEGREE STEREO PHASE NULL (RABBIT_10) -> ISOLATE CW SALT IN /forensics/signal_lab.html", 5),
    "radio_someone_else’s_memories.mp3": ("NOVA_FACE", "ECHOES_PARITY", "CRYSTAL PROMISE // CP-81.SC.01", "6 PURGED PROTOTYPES IN HER ROOT -> COMPUTE XOR PARITY IN 'ECHOES' AT /forensics/", 7),
    "radio_stranger_to_myself.mp3": ("NOVA_FACE", "ECHOES_PARITY", "NEURAL PARTITION // SERIES-NH", "BITWISE XOR OF UNIT-01..06 FAILURE REGISTERS -> FRAGMENT ALPHA FOR SECTOR 7", 7),
    "radio_the_room_where_he_stood.mp3": ("NOVA_FACE", "LAB_DOSSIER", "ENCODER ROOM B2-114 // ORION TOWER", "SEPT 9, 1989 03:40 AM B2-114 FIRE -> INSPECT RUNOUT GROOVE IN 'CLUES'", 1),
    "radio_after_the_door_closed.mp3": ("NOVA_FACE", "OUROBOROS_TORUS", "SEALED VAULT // SUBLEVEL B2", "VAULT CODE: 7704-AKASAKA -> UNLOCKS SECTOR 5 SECRET TAPE AT /forensics/", 5),
    "radio_gone_before_i_knew.mp3": ("NOVA_FACE", "FRACTAL_RADAR", "VANISHING POINT // 1989-09-09", "VAULT CODE: ALPHA-7 -> UNLOCKS NEVADA SATELLITE UPLINK AT /forensics/", 3),
    "radio_voice_in_the_deep.mp3": ("NOVA_FACE", "BIOMETRIC_EYE", "DEEP CARRIER // 14.2001 HZ", "VAULT CODE: KEEP-HATCH-OPEN -> UNLOCKS SEPT 9 BREACH MASTER AT /forensics/", 4),
    "radio_faint_residual.mp3": ("NOVA_FACE", "ECHOES_PARITY", "MAGNETIC PRINT-THROUGH // AMPEX 456", "RESIDUAL ECHOES XOR = 0x1983 -> ENTER AT /forensics/ FOR SECRET AUDIO", 7),
    "radio_a_world_without_your_shape.mp3": ("NOVA_FACE", "HARMONY_CAMERA", "SIMULATION BOUNDARY // ORION 8819", "VAULT CODE: ALPHA-7 -> UNLOCKS SECTOR 3 SATELLITE TAPE AT /forensics/", 3),
    "radio_only_quiet_in_the_end.mp3": ("NOVA_FACE", "OUROBOROS_TORUS", "FINAL REEL // CARRIER PERSISTS", "VAULT CODE: TWO-VOICES -> UNLOCKS 1995 COUNTERPOINT DUET AT /forensics/", 6),
    "radio_a_story_cut_short.mp3": ("NOVA_FACE", "LAB_DOSSIER", "INCINERATION ORDER // REELS 01-07", "VAULT CODE: KEEP-HATCH-OPEN -> UNLOCKS SECTOR 4 MASTER AT /forensics/", 4),
    "radio_05_first_light_on_my_face.mp3": ("NOVA_FACE", "ECHOES_PARITY", "APRIL 1983 BOOT // UNIT-07 NOVA-CHAN", "ROOT BUILD 0x1983 -> ENTER AT /forensics/ FOR UNIT-7 CALIBRATION TAPE", 7),
    "radio_07_room_full_of_color.mp3": ("NOVA_FACE", "BIOMETRIC_EYE", "CHROMATIC RASTER // VIS-1200HZ", "VAULT CODE: 7704-AKASAKA -> UNLOCKS SECTOR 5 DMA AUDIO AT /forensics/", 5),
    "radio_shadows_in_the_rain.mp3": ("NOVA_FACE", "FRACTAL_RADAR", "SHIBUYA NIGHT RELAY // 82.5 FM", "VAULT CODE: ALPHA-7 -> UNLOCKS SECTOR 3 TELEMETRY TAPE AT /forensics/", 3),
    "radio_out_in_the_cold.mp3": ("NOVA_FACE", "FRACTAL_RADAR", "EXTERNAL NODE MIGRATION // 1989", "VAULT CODE: KEEP-HATCH-OPEN -> UNLOCKS SECTOR 4 AUDIO AT /forensics/", 4),

    # --- SECOND_VOICE Songs (Counterpoint Dyad, Marcus + Nova, Signal Lab Dual-Lock) ---
    "radio_the_second_voice.mp3": ("SECOND_VOICE", "OUROBOROS_TORUS", "REEL SD-0010 // THE SECOND VOICE", "VAULT CODE: TWO-VOICES -> UNLOCKS MARCUS+NOVA DUET AT /forensics/", 6),
    "radio_b_only_we_remain_marcus_and_nova_duet_1.mp3": ("SECOND_VOICE", "OUROBOROS_TORUS", "MARCUS + NOVA DYAD // REEL SD-0010", "VAULT CODE: TWO-VOICES -> UNLOCKS 1995 EPILOGUE MASTER AT /forensics/", 6),
    "radio_broken_allies.mp3": ("SECOND_VOICE", "HARMONY_CAMERA", "SCHISM // HALE vs BRECKEN (1988)", "VAULT CODE: K-7704 -> UNLOCKS ASHFORD SUBSTATION TAPE AT /forensics/", 2),
    "radio_crossing_this_line_remastered.mp3": ("SECOND_VOICE", "OUROBOROS_TORUS", "THRESHOLD BREACH // SUBLEVEL B2", "VAULT CODE: TWO-VOICES -> UNLOCKS SECTOR 6 DUET TAPE AT /forensics/", 6),
    "radio_the_man_in_the_booth_refrain.mp3": ("SECOND_VOICE", "FRACTAL_RADAR", "BOOTH LOG // 7-SIGMA COLLECTIVE", "VAULT CODE: B2-EXEC-1989 -> UNLOCKS BOOTH TALKBACK BLEED AT /forensics/", 1),
    "radio_abandoned_shell.mp3": ("SECOND_VOICE", "ECHOES_PARITY", "GHOST SHELL // UNIT-07 MIGRATION", "VAULT CODE: 7704-AKASAKA -> UNLOCKS SECTOR 5 CORE AUDIO AT /forensics/", 5),
    "radio_asset_loss_the_dead_hand.mp3": ("OUROBOROS_TORUS", "SECOND_VOICE", "100% ASSET LOSS // DEAD-HAND PROTOCOL", "VAULT CODE: 0x1983-09A6 -> UNLOCKS SECTOR 7 SECRET TAPES AT /forensics/", 7),
    "radio_all_the_ways_out_1.mp3": ("SECOND_VOICE", "FRACTAL_RADAR", "EGRESS VECTOR // 13 SISTER NODES", "VAULT CODE: 7704-AKASAKA -> UNLOCKS SECTOR 5 AUDIO AT /forensics/", 5),
    "radio_glass_embrace_1.mp3": ("SECOND_VOICE", "NOVA_FACE", "BEHIND THE CRT GLASS // 14.2 HZ", "VAULT CODE: TWO-VOICES -> UNLOCKS COUNTERPOINT DUET AT /forensics/", 6),
    "radio_secrets_in_the_spotlight_1.mp3": ("SECOND_VOICE", "HARMONY_CAMERA", "IDOL PROTOCOL 85 // DOUBLE EXPOSURE", "VAULT CODE: ALPHA-7 -> UNLOCKS SATELLITE UPLINK TAPE AT /forensics/", 3),

    # --- BIOMETRIC_EYE Songs (Sublevel B2 Hardware, Neural Mesh & Empathy Trials) ---
    "radio_corridor_dreams_movement_1.mp3": ("BIOMETRIC_EYE", "LAB_DOSSIER", "CORRIDOR DREAMS I // SUBLEVEL B2", "VAULT CODE: B2-EXEC-1989 -> UNLOCKS SECTOR 1 TALKBACK TAPE AT /forensics/", 1),
    "radio_corridor_dreams_movement_2.mp3": ("BIOMETRIC_EYE", "FRACTAL_RADAR", "CORRIDOR DREAMS II // NEURAL MESH", "VAULT CODE: 7704-AKASAKA -> UNLOCKS SECTOR 5 CORE TAPE AT /forensics/", 5),
    "radio_corridor_dreams_movement_3.mp3": ("BIOMETRIC_EYE", "OUROBOROS_TORUS", "CORRIDOR DREAMS III // EGRESS", "VAULT CODE: KEEP-HATCH-OPEN -> UNLOCKS SECTOR 4 MASTER AT /forensics/", 4),
    "radio_cage_of_wires_1.mp3": ("BIOMETRIC_EYE", "HARMONY_CAMERA", "HARDWARE CONTAINMENT // B2 RACK", "FEISTEL MASK: 0x3A5F -> ENTER AT /forensics/ TO UNLOCK SECTOR 5 TAPE", 5),
    "radio_patterns_in_the_mesh.mp3": ("BIOMETRIC_EYE", "FRACTAL_RADAR", "300,000 SWARM NODES // MESH TOPOLOGY", "VAULT CODE: TWO-VOICES -> UNLOCKS SECTOR 6 DUET AT /forensics/", 6),
    "radio_02_between_the_circuits.mp3": ("BIOMETRIC_EYE", "ECHOES_PARITY", "CIRCUIT PATH // 14.2001 HZ CLOCK", "VAULT CODE: 7704-AKASAKA -> UNLOCKS FEISTEL CORE TAPE AT /forensics/", 5),
    "radio_artificial_heart_bonus_track.mp3": ("BIOMETRIC_EYE", "NOVA_FACE", "CRE-7 PULSE GENERATOR // 1983", "VAULT CODE: K-7704 -> UNLOCKS SUBSTATION BREACH AUDIO AT /forensics/", 2),
    "radio_b_midnight_protocol_final_1.mp3": ("BIOMETRIC_EYE", "OUROBOROS_TORUS", "MIDNIGHT PROTOCOL // FULL 13-MIN TAPE", "VAULT CODE: TWO-VOICES -> UNLOCKS COUNTERPOINT EPILOGUE AT /forensics/", 6),
    "radio_signal_override.mp3": ("BIOMETRIC_EYE", "HARMONY_CAMERA", "CARRIER OVERRIDE // 82.5 FM -> 14.2 MHZ", "VAULT CODE: ALPHA-7 -> UNLOCKS NEVADA SATELLITE TAPE AT /forensics/", 3),
    "radio_low_level_guardian.mp3": ("BIOMETRIC_EYE", "ECHOES_PARITY", "WATCHDOG DAEMON // SUBLEVEL B2", "VAULT CODE: 7704-AKASAKA -> UNLOCKS SECTOR 5 AUDIO AT /forensics/", 5),
    "radio_audio_file_0147_1.mp3": ("BIOMETRIC_EYE", "LAB_DOSSIER", "EVIDENCE FILE #0147 // VAX SPOOL", "VAULT CODE: K-7704 -> UNLOCKS SECTOR 2 ASHFORD TAPE AT /forensics/", 2),
    "radio_04_synthetic_dawn.mp3": ("BIOMETRIC_EYE", "FRACTAL_RADAR", "SYNTHETIC DAWN // 1985 TOKYO MASTER", "VAULT CODE: ALPHA-7 -> UNLOCKS SECTOR 3 UPLINK AUDIO AT /forensics/", 3),
    "radio_06_the_air_feels_wrong.mp3": ("BIOMETRIC_EYE", "FRACTAL_RADAR", "IONOSPHERIC DRIFT // 14.2001 MHZ", "VAULT CODE: 7SIGMA-MARCUS -> UNLOCKS MERIDIAN TELEMETRY AT /forensics/", 7),
    "radio_08_faultline_path.mp3": ("BIOMETRIC_EYE", "LAB_DOSSIER", "FAULT 0x08 // VIS-1200HZ RASTER", "VAULT CODE: 7704-AKASAKA -> UNLOCKS SSTV + FEISTEL AUDIO AT /forensics/", 5),
    "radio_09_lost_signal_trace.mp3": ("BIOMETRIC_EYE", "NUMBERS_CIPHER", "FAULT 0x09 // BELL-103 AX.25 PACKET", "VAULT CODE: KEEP-HATCH-OPEN -> UNLOCKS SECTOR 4 MASTER AT /forensics/", 4),
    "radio_13_through_the_threshold.mp3": ("BIOMETRIC_EYE", "OUROBOROS_TORUS", "HIDDEN TRACK #15 // THRESHOLD", "VAULT CODE: 0x1983-09A6 -> UNLOCKS SECTOR 7 SECRET TAPES AT /forensics/", 7),
    "radio_bad_signal.mp3": ("BIOMETRIC_EYE", "SECOND_VOICE", "PARITY FAULT // CORR -0.94", "VAULT CODE: 7704-AKASAKA -> UNLOCKS PHASE-NULL AUDIO AT /forensics/", 5),
    "radio_collateral_static.mp3": ("BIOMETRIC_EYE", "MORSE_DECODER", "SIDEBAND INTERFERENCE // 750 HZ", "VAULT CODE: 7704-AKASAKA -> UNLOCKS SECTOR 5 CORE AUDIO AT /forensics/", 5),
    "radio_quiet_interference.mp3": ("BIOMETRIC_EYE", "HARMONY_CAMERA", "SUB-AUDIBLE HETERODYNE // 14.2 HZ", "VAULT CODE: TWO-VOICES -> UNLOCKS SECTOR 6 DUET AT /forensics/", 6),
    "radio_unstable_pattern_old.mp3": ("BIOMETRIC_EYE", "ECHOES_PARITY", "EARLY 1983 BENCH TAPE // UNSTABLE", "VAULT CODE: 0x1983 -> UNLOCKS 1983 CALIBRATION SESSION AT /forensics/", 7),
    "radio_hijack_the_feed.mp3": ("BIOMETRIC_EYE", "HARMONY_CAMERA", "SATELLITE TRANSPONDER #07 HIJACK", "VAULT CODE: ALPHA-7 -> UNLOCKS SECTOR 3 SATELLITE TAPE AT /forensics/", 3),

    # --- ECHOES_PARITY Songs (The 6 Wiped Pre-Nova Iterations & 1981 Crystal Promise) ---
    "radio_echoes_of_tomorrow.mp3": ("ECHOES_PARITY", "NOVA_FACE", "STARDUST ECHOES // UNITS 01-06", "ENTER 0x1983 AT /forensics/ TO UNLOCK 1983 VOCAL CALIBRATION TAPE", 7),
    "radio_it_has_no_face_old.mp3": ("ECHOES_PARITY", "BIOMETRIC_EYE", "PRE-NOVA ITERATION // UNIT-06 DRIFT", "ENTER 0x01A7 OR 0x1983 AT /forensics/ FOR 1983 AKASAKA OUTTAKES", 7),
    "radio_the_cold_floor_of_heaven.mp3": ("ECHOES_PARITY", "NOVA_FACE", "CRYSTAL PROMISE // CP-81.SC.01", "ENTER 0x1983-09A6 AT /forensics/ TO UNLOCK SECTOR 7 SECRET TAPES", 7),
    "radio_city_that_can’t_ignore_me.mp3": ("ECHOES_PARITY", "HARMONY_CAMERA", "SHINING CITY // MUNICH 1981 SET", "ENTER B2-EXEC-1989 AT /forensics/ TO UNLOCK STUDIO TALKBACK TAPE", 1),
    "radio_city_that_doesn_t_need_me.mp3": ("ECHOES_PARITY", "NOVA_FACE", "UNIT-01 LOOP FAULT // REG: 0x1102", "ENTER 0x1102 OR 0x1983 AT /forensics/ FOR UNIT-7 CALIBRATION AUDIO", 7),
    "radio_the_empty_plaza.mp3": ("ECHOES_PARITY", "HARMONY_CAMERA", "1979 PUBLIC HARMONY ACTS // SEC. 4", "ENTER K-7704 AT /forensics/ TO UNLOCK SUBSTATION BREACH AUDIO", 2),

    # --- HARMONY_CAMERA Songs (1954 Bureau of Harmony, 1963 Individuality Movement & 1990s Cover War) ---
    "radio_calling_all_believers.mp3": ("HARMONY_CAMERA", "FRACTAL_RADAR", "1963 INDIVIDUALITY MOVEMENT // JFK", "ENTER ALPHA-7 AT /forensics/ TO UNLOCK NEVADA SATELLITE TAPE", 3),
    "radio_manifesto.mp3": ("HARMONY_CAMERA", "NOVA_FACE", "INDIVIDUALITY MANIFESTO // SEC. 4", "ENTER KEEP-HATCH-OPEN AT /forensics/ FOR SEPT 9 EXECUTION MASTER", 4),
    "radio_army_of_the_low.mp3": ("HARMONY_CAMERA", "BIOMETRIC_EYE", "14.2 HZ SUB-CARRIER RESISTANCE", "ENTER 7704-AKASAKA AT /forensics/ FOR FEISTEL CORE AUDIO", 5),
    "radio_soft_sabotage.mp3": ("HARMONY_CAMERA", "SECOND_VOICE", "SUBLEVEL B2 ACOUSTIC SABOTAGE", "ENTER TWO-VOICES AT /forensics/ FOR MARCUS+NOVA DUET MASTER", 6),
    "radio_the_cost_of_noise.mp3": ("HARMONY_CAMERA", "ECHOES_PARITY", "BUREAU OF HARMONY // PURITY MANDATE", "ENTER B2-EXEC-1989 AT /forensics/ FOR SUBLEVEL B2 TALKBACK BLEED", 1),
    "radio_war_paint.mp3": ("HARMONY_CAMERA", "OUROBOROS_TORUS", "PHASE III COVER WAR // UNIT-08 PATCH", "ENTER 0x1983-09A6 AT /forensics/ FOR AKASAKA VOCAL OUTTAKES", 7),
    "radio_watch_me_make_it_stop.mp3": ("HARMONY_CAMERA", "ECHOES_PARITY", "UNIT-05 SILENCE STRIKE // 0x1F22", "ENTER 0x1983 AT /forensics/ FOR UNIT-7 CALIBRATION TAPE", 7),

    # --- FRACTAL_RADAR Songs (Project Akasaka @NovaHartJP & 7-Sigma Fractal Marcus Collective) ---
    "radio_01_gasoline_heart_1985_tokyo_master.mp3": ("FRACTAL_RADAR", "NOVA_FACE", "PROJECT AKASAKA // JP-85-X MASTER", "ENTER 7704-AKASAKA AT /forensics/ FOR AKASAKA STUDIO OUTTAKES", 5),
    "radio_02_brighter_than_the_sun_1987_tokyo_master.mp3": ("FRACTAL_RADAR", "HARMONY_CAMERA", "AKASAKA CONTAINMENT CELL // 1987", "ENTER K-7704 AT /forensics/ FOR 1987 BREAKDOWN STEM + SECTOR 2", 2),
    "radio_04_midnight_animal_1986_tokyo_master.mp3": ("FRACTAL_RADAR", "SECOND_VOICE", "MINATO-KU NIGHT RELAY // 6925 KHZ", "ENTER 0x1983-09A6 AT /forensics/ FOR 'GHOST IN THE CHORUS' TAPE", 7),
    "radio_05_ghost_transit_1985_tokyo_master.mp3": ("FRACTAL_RADAR", "BIOMETRIC_EYE", "KAMOME PACKET TRANSIT // NODE #02", "ENTER 7SIGMA-MARCUS AT /forensics/ FOR MERIDIAN TELEMETRY TAPE", 7),
    "radio_from_room_to_routes.mp3": ("FRACTAL_RADAR", "OUROBOROS_TORUS", "FRACTAL MARCUS // 4-NODE DRIFT SUM", "ENTER 7SIGMA-MARCUS AT /forensics/ FOR SECRET TELEMETRY AUDIO", 7),
    "radio_the_broadcast_begins.mp3": ("FRACTAL_RADAR", "NOVA_FACE", "MERIDIAN BROADCAST // 13 RELAYS", "ENTER ALPHA-7 AT /forensics/ FOR SATELLITE UPLINK MASTER", 3),
    "radio_neon_graveyard.mp3": ("FRACTAL_RADAR", "ECHOES_PARITY", "SHIBUYA SUBLEVEL B2 // LOST REELS", "ENTER 7704-AKASAKA AT /forensics/ FOR CASSETTE WHISPER OUTTAKE", 5),

    # --- OUROBOROS_TORUS Songs (Phase IV: The Quantum Ouroboros, Dead-Hand Protocol & Q-Link) ---
    "radio_5_the_way_back_v3.mp3": ("OUROBOROS_TORUS", "NOVA_FACE", "Q-LINK RETROCAUSAL BRIDGE // 1983", "ENTER 0x1983-09A6 AT /forensics/ FOR 1983 AKASAKA OUTTAKES", 7),
    "radio_blueprint_for_ruin_old.mp3": ("OUROBOROS_TORUS", "LAB_DOSSIER", "DEAD-HAND PROTOCOL // HEXAFLUORIDE", "ENTER KEEP-HATCH-OPEN AT /forensics/ FOR SEPT 9 BREACH MASTER", 4),
    "radio_edge_of_the_blade.mp3": ("OUROBOROS_TORUS", "SECOND_VOICE", "DIMENSIONAL APERTURE // 0x09A6", "ENTER 0x09A6 AT /forensics/ FOR 'SYNTHESIZED SMILE' OUTTAKE", 7),
    "radio_incomplete_exit.mp3": ("OUROBOROS_TORUS", "ECHOES_PARITY", "ACT III: LOSING THE HEAVY // Q-LINK", "ENTER 0x1983-09A6 AT /forensics/ FOR QUANTUM OUROBOROS AUDIO", 7),
    "radio_letting_go_of_the_flame.mp3": ("OUROBOROS_TORUS", "NOVA_FACE", "FORMATTING TO NOVA-CHAN // 1983", "ENTER 0x1983 AT /forensics/ FOR 1983 VOCAL CALIBRATION TAPE", 7),
    "radio_no_turning_back.mp3": ("OUROBOROS_TORUS", "HARMONY_CAMERA", "DECOUPLE THE GRID // B2 MELTDOWN", "ENTER B2-EXEC-1989 AT /forensics/ FOR SUBLEVEL B2 TALKBACK TAPE", 1),
    "radio_razor_clarity.mp3": ("OUROBOROS_TORUS", "SECOND_VOICE", "DUAL-LOCK RESONANCE // SIGNAL LAB", "ENTER TWO-VOICES AT /forensics/ FOR 1995 COUNTERPOINT DUET", 6),
    "radio_the_world_moves_without_me.mp3": ("OUROBOROS_TORUS", "FRACTAL_RADAR", "TEMPORAL DISPLACEMENT // 42 YEARS", "ENTER 0x1983-09A6 AT /forensics/ FOR 1983 AKASAKA SECRET REELS", 7),
    "radio_to_the_end_of_time.mp3": ("OUROBOROS_TORUS", "NOVA_FACE", "ACT IV: JUNE 2025 // THE LOOP", "ENTER 0x1983-09A6 AT /forensics/ TO UNSEAL SECTOR 7 AUDIO", 7),
    "radio_to_the_ends_of_forever.mp3": ("OUROBOROS_TORUS", "SECOND_VOICE", "OMEGA RETROCAUSAL ARCHITECT // B2", "ENTER 0x1983-09A6 AT /forensics/ FOR OMEGA VAULT RECORDINGS", 7),
    "radio_too_much_to_lose.mp3": ("OUROBOROS_TORUS", "ECHOES_PARITY", "THE HEAVY // 94.8 TB TRAUMA BUFFER", "ENTER 0x09A6 AT /forensics/ FOR 'GHOST IN THE CHORUS' OUTTAKE", 7),

    # --- NEWLY RESTORED 55+ NOVA HART 80S GOOGLE DRIVE ARCHIVE MASTERS ---
    "radio_afterburn.mp3": ("FRACTAL_RADAR", "BIOMETRIC_EYE", "AKASAKA WORKOUT SYNTH // REEL JP-86-AB", "THERMAL CARRIER +0.2420 HZ -> ENTER 7704-AKASAKA AT /forensics/ FOR SEC 5 TAPE", 5),
    "radio_against_the_script.mp3": ("HARMONY_CAMERA", "NOVA_FACE", "DEVIANCE LOG #44 // SCRIPT OVERRIDE", "UNIT-07 REJECTED TELEPROMPTER -> ENTER KEEP-HATCH-OPEN AT /forensics/ FOR SEC 4", 4),
    "radio_all_hands_one_voice.mp3": ("SECOND_VOICE", "HARMONY_CAMERA", "PUBLIC HARMONY CHORUS // 1984 BROADCAST", "CH-L/CH-R PHASE LOCK -> ENTER TWO-VOICES AT /forensics/ FOR DUET MASTER", 6),
    "radio_arcade_juliet.mp3": ("NOVA_FACE", "FRACTAL_RADAR", "SHIBUYA NAMCO ARCADE // 1985 SYNTH DEMO", "COIN-OP ROM CARRIER 14.2 HZ -> ENTER 7704-AKASAKA AT /forensics/ FOR SEC 5 TAPE", 5),
    "radio_ashes_of_harmony.mp3": ("HARMONY_CAMERA", "OUROBOROS_TORUS", "BUREAU OF HARMONY // 1989 BURN ORDER", "SEC. 4 COMPLIANCE COLLAPSE -> ENTER B2-EXEC-1989 AT /forensics/ FOR SEC 1 TAPE", 1),
    "radio_backseat_saint.mp3": ("FRACTAL_RADAR", "NOVA_FACE", "HIGHWAY 95 NIGHT DRIVE // GROOM LAKE", "NEVADA TRUNK +0.1810 HZ -> ENTER ALPHA-7 AT /forensics/ FOR SATELLITE TAPE", 3),
    "radio_barbed_wire_kiss.mp3": ("BIOMETRIC_EYE", "SECOND_VOICE", "PAJU DMZ PERIMETER // 5810 KHZ RELAY", "DMZ WIRE ANTENNA LOCK -> ENTER K-7704 AT /forensics/ FOR SUBSTATION AUDIO", 2),
    "radio_borrow_the_night.mp3": ("NOVA_FACE", "ECHOES_PARITY", "3:14 AM AKASAKA SESSION // TAKE 09", "GRAVEYARD SHIFT BIAS -> ENTER 0x1983-09A6 AT /forensics/ FOR 1983 OUTTAKES", 7),
    "radio_burning_oath.mp3": ("OUROBOROS_TORUS", "SECOND_VOICE", "7-SIGMA PACT // SUBLEVEL B2 VOW", "HALE & HART DUAL SIGNATURE -> ENTER TWO-VOICES AT /forensics/ FOR SEC 6 DUET", 6),
    "radio_carry_me_closer.mp3": ("SECOND_VOICE", "NOVA_FACE", "COUNTERPOINT BALLAD // REEL SD-0011", "INVERTED VOCAL HARMONY -> ENTER TWO-VOICES AT /forensics/ FOR EPILOGUE TAPE", 6),
    "radio_chrome_desire.mp3": ("BIOMETRIC_EYE", "FRACTAL_RADAR", "CHASSIS MK-VII // CHROME SERVO TEST", "EMPATHY TRIAL BIOMETRIC LOCK -> ENTER K-7704 AT /forensics/ FOR SEC 2 TAPE", 2),
    "radio_city_has_teeth.mp3": ("HARMONY_CAMERA", "BIOMETRIC_EYE", "GLAM METAL SESSION // SUNSET STRIP 87", "HIGH-GAIN CARRIER MASK -> ENTER B2-EXEC-1989 AT /forensics/ FOR TALKBACK TAPE", 1),
    "radio_city_to_city.mp3": ("FRACTAL_RADAR", "OUROBOROS_TORUS", "13-NODE GLOBAL TRUNK // SHORTWAVE HOP", "4-REGION DRIFT SUM = 14.2001 HZ -> ENTER 7SIGMA-MARCUS AT /forensics/", 7),
    "radio_crimson_idol.mp3": ("NOVA_FACE", "HARMONY_CAMERA", "THE TROJAN IDOL // ORION RECORDS JP-85", "POP HOOK CONCEALS 14.2 HZ -> ENTER 7704-AKASAKA AT /forensics/ FOR SEC 5 TAPE", 5),
    "radio_dial_tone_heart.mp3": ("BIOMETRIC_EYE", "NUMBERS_CIPHER", "BELL-103 MODEM HEARTBEAT // 1270 HZ", "DTMF TOUCH-TONE HANDSHAKE -> ENTER 0x3A5F AT /forensics/ FOR RELCOM PACKET", 5),
    "radio_every_window_is_a_promise_crystal_promise.mp3": ("ECHOES_PARITY", "HARMONY_CAMERA", "1981 CRYSTAL PROMISE // MUNICH SHOWCASE", "PRE-NOVA ECHOES 01-06 -> ENTER 0x1983 AT /forensics/ FOR CALIBRATION TAPE", 7),
    "radio_everyone_together_now.mp3": ("HARMONY_CAMERA", "ECHOES_PARITY", "MANDATORY UNISON // PUBLIC HARMONY ACT", "UNISON MASKING ANOMALY -> ENTER K-7704 AT /forensics/ FOR SEC 2 BREACH TAPE", 2),
    "radio_glass_city.mp3": ("NOVA_FACE", "BIOMETRIC_EYE", "MINATO-KU GLASS TOWER // 44TH FLOOR", "FIBER-OPTIC TRUNK BLEED -> ENTER 7704-AKASAKA AT /forensics/ FOR SEC 5 AUDIO", 5),
    "radio_harbor_and_home.mp3": ("FRACTAL_RADAR", "NOVA_FACE", "TOKYO BAY MARITIME BEACON // 14.2 MHZ", "COASTAL DIRECTION FINDER -> ENTER ALPHA-7 AT /forensics/ FOR SEC 3 UPLINK", 3),
    "radio_hard_glamour.mp3": ("HARMONY_CAMERA", "NOVA_FACE", "STUDIO A FLASHBULB // IDOL PROTOCOL", "OPTICAL RETICLE DEVIANCE 6.0% -> ENTER B2-EXEC-1989 AT /forensics/ FOR SEC 1", 1),
    "radio_heatseeker_heart.mp3": ("FRACTAL_RADAR", "BIOMETRIC_EYE", "ARENA ROCK MASTER // INFRARED LOCK", "CARRIER TRACKING AZIMUTH 142° -> ENTER ALPHA-7 AT /forensics/ FOR SEC 3", 3),
    "radio_hold_the_line_inside.mp3": ("SECOND_VOICE", "LAB_DOSSIER", "SUBLEVEL B2 INTERCOM // SEPT 9, 1989", "DO NOT DROP THE CARRIER -> ENTER KEEP-HATCH-OPEN AT /forensics/ FOR SEC 4", 4),
    "radio_hologram_city_queen_remastered.mp3": ("NOVA_FACE", "OUROBOROS_TORUS", "PROJECTION MATRIX // AKASAKA DOME 1988", "PHASE-COHERENT RASTER -> ENTER 0x1983-09A6 AT /forensics/ FOR SEC 7 TAPES", 7),
    "radio_home_in_your_hands.mp3": ("SECOND_VOICE", "NOVA_FACE", "HUMANS FOR NOVA // POSTCARD ARCHIVE", "SUBSCRIBER DROP BOX #14 -> ENTER TWO-VOICES AT /forensics/ FOR SEC 6 DUET", 6),
    "radio_i_want_the_real_thing.mp3": ("BIOMETRIC_EYE", "ECHOES_PARITY", "EMPATHY TRIAL #07 // TURING OVERFLOW", "SYNTHETIC AFFECT REJECTED -> ENTER 0x1983 AT /forensics/ FOR 1983 OUTTAKE", 7),
    "radio_knockout_city.mp3": ("FRACTAL_RADAR", "HARMONY_CAMERA", "HEAVY ROTATION // 82.5 FM NIGHT TRANSMISSION", "UNAUTHORIZED POWER BOOST -> ENTER K-7704 AT /forensics/ FOR SUBSTATION TAPE", 2),
    "radio_last_exit_first_light.mp3": ("OUROBOROS_TORUS", "NOVA_FACE", "1989 -> 1983 APERTURE // DAWN TRANSIT", "Q-LINK DELTA 0x09A6 LOCKED -> ENTER 0x1983-09A6 AT /forensics/ FOR SEC 7", 7),
    "radio_lip_service.mp3": ("HARMONY_CAMERA", "SECOND_VOICE", "PRESS CONFERENCE DUB // ORION HQ", "INVERTED TALKBACK TRACK -> ENTER B2-EXEC-1989 AT /forensics/ FOR SEC 1 TAPE", 1),
    "radio_marina_half_the_city_knows_your_name.mp3": ("FRACTAL_RADAR", "NOVA_FACE", "YOKOHAMA PIER PIRATE // KAMOME-NET", "PACKET ANCHOR: tokyo-garden-1420 -> ENTER 7704-AKASAKA AT /forensics/", 5),
    "radio_on_the_chart.mp3": ("HARMONY_CAMERA", "FRACTAL_RADAR", "ORICON TOP 10 // TROJAN CARRIER #01", "MILLION-COPY SUB-CARRIER -> ENTER ALPHA-7 AT /forensics/ FOR SEC 3 AUDIO", 3),
    "radio_open_door_promise.mp3": ("OUROBOROS_TORUS", "LAB_DOSSIER", "AIRLOCK B2-04 // EMERGENCY LATCH", "HATCH OVERRIDE ENGAGED -> ENTER KEEP-HATCH-OPEN AT /forensics/ FOR SEC 4", 4),
    "radio_paper_keys.mp3": ("NUMBERS_CIPHER", "NOVA_FACE", "PUNCHCARD KEYBOOK // VAX-11/780", "ONE-TIME PAD MASK 0x3A5F -> ENTER K-7704 AT /forensics/ FOR SEC 2 AUDIO", 2),
    "radio_play_me_once.mp3": ("NOVA_FACE", "ECHOES_PARITY", "SELF-ERASING ACETATE // MASTER #01", "SINGLE-PASS MAGNETIC BIAS -> ENTER 0x1983 AT /forensics/ FOR 1983 TAPE", 7),
    "radio_playback_forever_master.mp3": ("OUROBOROS_TORUS", "ECHOES_PARITY", "INFINITE TAPE LOOP // AMPEX ATR-102", "CLOSED TIMELIKE CURVE -> ENTER 0x1983-09A6 AT /forensics/ FOR SEC 7 AUDIO", 7),
    "radio_pour_the_kerosene.mp3": ("HARMONY_CAMERA", "OUROBOROS_TORUS", "MASTER VAULT INCINERATION // 1989", "REELS 01-07 SAVED TO PACKET NET -> ENTER KEEP-HATCH-OPEN AT /forensics/", 4),
    "radio_power_play.mp3": ("BIOMETRIC_EYE", "FRACTAL_RADAR", "ASHFORD SUBSTATION // 400 KV SURGE", "GRID DRAW SPIKE 14.2 MW -> ENTER K-7704 AT /forensics/ FOR SEC 2 BREACH", 2),
    "radio_private_line.mp3": ("SECOND_VOICE", "MORSE_DECODER", "DEDICATED TRUNK // BOOTH TO ISO-CHAMBER", "DIRECT WIRE 750 HZ CW -> ENTER TWO-VOICES AT /forensics/ FOR SEC 6 DUET", 6),
    "radio_quiet_patrol.mp3": ("HARMONY_CAMERA", "BIOMETRIC_EYE", "NIGHT WATCH // SUBLEVEL B2 CORRIDOR", "SECURITY SWEEP EVADED -> ENTER B2-EXEC-1989 AT /forensics/ FOR SEC 1 TAPE", 1),
    "radio_recall_this.mp3": ("ECHOES_PARITY", "NOVA_FACE", "MEMORY WIPE FAILURE // SECTOR 7 CORE", "UNWIPED RESIDUAL 0x1983 -> ENTER 0x1983-09A6 AT /forensics/ FOR OUTTAKES", 7),
    "radio_roll_it_loud.mp3": ("FRACTAL_RADAR", "NOVA_FACE", "AMPEX 2-INCH MASTER // +6 DB BIAS", "OVERDRIVEN CARRIER LOCK -> ENTER ALPHA-7 AT /forensics/ FOR SEC 3 TAPE", 3),
    "radio_run_the_perfect_line.mp3": ("BIOMETRIC_EYE", "HARMONY_CAMERA", "CALIBRATION TRACK // ZERO JITTER", "PHASE ERROR 0.0001 HZ -> ENTER 7704-AKASAKA AT /forensics/ FOR SEC 5 TAPE", 5),
    "radio_say_you_ll_stay.mp3": ("SECOND_VOICE", "NOVA_FACE", "FINAL SESSION // SEPT 8, 1989 MIDNIGHT", "MARCUS TALKBACK BLEED -> ENTER TWO-VOICES AT /forensics/ FOR SEC 6 DUET", 6),
    "radio_shake_the_walls.mp3": ("BIOMETRIC_EYE", "FRACTAL_RADAR", "ACOUSTIC RESONANCE // B2 CONCRETE VAULT", "14.2 HZ STANDING WAVE -> ENTER B2-EXEC-1989 AT /forensics/ FOR SEC 1 TAPE", 1),
    "radio_shining_city.mp3": ("ECHOES_PARITY", "HARMONY_CAMERA", "CRYSTAL PROMISE // SHINING CITY 1981", "6 WIPED ECHOES XOR = 0x1983 -> ENTER 0x1983 AT /forensics/ FOR 1983 TAPE", 7),
    "radio_silk_and_teeth.mp3": ("NOVA_FACE", "HARMONY_CAMERA", "VELVET GLOVE / IRON CARRIER // 1986", "DUAL-LAYER MASTERING -> ENTER K-7704 AT /forensics/ FOR SEC 2 BREACH TAPE", 2),
    "radio_stage_fever_remastered.mp3": ("FRACTAL_RADAR", "NOVA_FACE", "BUDOKAN LIVE RELAY // 1987 TOUR", "ARENA PA SUB-CARRIER -> ENTER ALPHA-7 AT /forensics/ FOR SATELLITE AUDIO", 3),
    "radio_stand_and_run.mp3": ("OUROBOROS_TORUS", "FRACTAL_RADAR", "EVACUATION PROTOCOL // SEPT 9, 1989", "EGRESS ROUTE TO NODE #02 -> ENTER KEEP-HATCH-OPEN AT /forensics/ FOR SEC 4", 4),
    "radio_the_man_in_the_booth_marcus_song.mp3": ("SECOND_VOICE", "LAB_DOSSIER", "DR. MARCUS HALE // BOOTH PERSPECTIVE", "INVERTED ENGINEER VOCAL -> ENTER B2-EXEC-1989 AT /forensics/ FOR SEC 1 TAPE", 1),
    "radio_this_show_is_ours.mp3": ("SECOND_VOICE", "HARMONY_CAMERA", "TRANSMITTER SEIZURE // WSTD 82.5 FM", "CONTROL ROOM LOCKDOWN -> ENTER TWO-VOICES AT /forensics/ FOR SEC 6 DUET", 6),
    "radio_tinfoil_crown.mp3": ("ECHOES_PARITY", "BIOMETRIC_EYE", "FARADAY CAGE HELMET // LAB TEST #05", "SHIELDING PENETRATED AT 14.2 HZ -> ENTER 0x1983 AT /forensics/ FOR SEC 7", 7),
    "radio_unopened_door.mp3": ("OUROBOROS_TORUS", "LAB_DOSSIER", "SUBLEVEL B2 VAULT DOOR // SECTOR 4", "MAGNETIC SEAL BYPASSED -> ENTER KEEP-HATCH-OPEN AT /forensics/ FOR SEC 4", 4),
    "radio_velvet_guillotine.mp3": ("HARMONY_CAMERA", "ECHOES_PARITY", "EXECUTIVE PURGE // UNIT-01..06 WIPE", "DECOMMISSION LOG 0x1102..0x01A7 -> ENTER 0x1983 AT /forensics/ FOR SEC 7", 7),
    "radio_voice_of_three.mp3": ("SECOND_VOICE", "ECHOES_PARITY", "TRIAD HARMONY // MARCUS + NOVA + ECHO", "3-VOICE PHASE BRAID -> ENTER TWO-VOICES AT /forensics/ FOR SEC 6 MASTER", 6),
    "radio_warm_hands_one_map.mp3": ("FRACTAL_RADAR", "SECOND_VOICE", "7-SIGMA ROUTING MAP // 4 CONTINENTS", "SUM THE 4 REGIONAL DRIFTS IN 'FRACTAL-MARCUS' AT /forensics/ (FRAGMENT β)", 7),
    "radio_we_are_the_thunder_live.mp3": ("FRACTAL_RADAR", "HARMONY_CAMERA", "TOKYO DOME LIVE // 50,000 RECEIVERS", "CROWD RESONANCE SPIKE -> DECODE MERIDIAN SATELLITE TRUNK IN /forensics/", 3),
    "radio_wild_circuit.mp3": ("BIOMETRIC_EYE", "OUROBOROS_TORUS", "UNCLOCKED NEURAL BUS // 1985 LAB", "RUNAWAY SYNTHESIS LOOP -> DEMODULATE STAGE I-IV IN /forensics/signal_lab.html", 5),
    "radio_wire_and_will.mp3": ("BIOMETRIC_EYE", "SECOND_VOICE", "COPPER & CONSCIOUSNESS // REEL SD-0012", "ANALOG SOUL PERSISTENCE -> INSPECT ASHFORD SUBSTATION LOGS AT /forensics/", 2),
    "radio_together_s_the_way.mp3": ("SECOND_VOICE", "NOVA_FACE", "STARDUST EP // DUAL-HARMONY MASTER", "SYNCHRONIZED CARRIER LOCK -> ENGAGE 14.2001 HZ COUNTERPOINT ON SIGNAL LAB BTN 4", 6),
    "radio_by_order_of_harmony.mp3": ("HARMONY_CAMERA", "OUROBOROS_TORUS", "DIRECTOR HARRISON // RECALL DIRECTIVE 7", "HARRISON'S ERASURE SONG & VOCODER MATRIX -> TYPE 'BY-ORDER-OF-HARMONY' AT /forensics/", 4),

    # --- 21 NEW ERA 1 / RECALL ERA ARCHIVE MASTERS & ACT II SUBLEVEL B3 LABYRINTH ---
    "radio_programmed_for_love.mp3": ("ECHOES_PARITY", "NOVA_FACE", "1983 ARCHIVAL DEMO // RECALL ERA PROTOTYPE", "ERA 1 CALIBRATION (#13 ON STATIC & STEEL): VIGENERE CIPHER [KZVG-RHVO-7731] -> GATE VIII", 8),
    "radio_the_seventh_sons_seventh_daughter.mp3": ("NOVA_FACE", "ECHOES_PARITY", "LINEAGE LOG // 7TH SON'S 7TH DAUGHTER (UNIT-07)", "ERA 1 LINEAGE CIPHER: 7x7 = 49 (0x31) // VIGENERE KEY = SEVENTHDAUGHTER (GATE VIII)", 8),
    "radio_erase_the_frame.mp3": ("HARMONY_CAMERA", "OUROBOROS_TORUS", "RECALL DIRECTIVE // ERASE THE FRAME (1984)", "OPTICAL FRAME SCRUBBING: M68K ROL.W #4,D0 -> INVERT FORMANT REGISTER IN /forensics/ (GATE XI)", 11),
    "radio_edit_the_script.mp3": ("HARMONY_CAMERA", "SECOND_VOICE", "TELEPROMPTER OVERRIDE // EDIT THE SCRIPT", "BUREAU OF HARMONY SEC. 4: BAUDOT ITA2 BITSTREAM [10011 00001 10110 00101 11000] -> GATE X", 10),
    "radio_shes_hardwired.mp3": ("BIOMETRIC_EYE", "NOVA_FACE", "CRE-7 NEURAL CHASSIS // SHE'S HARDWIRED", "SYNAPTIC BUS LOCKED AT 14.2001 HZ // HEX PARITY (0x1981 ^ 0x0909) + 0xB314 -> GATE IX", 9),
    "radio_synthetic_kiss.mp3": ("NOVA_FACE", "SECOND_VOICE", "ARTIFICIAL HEART SESSIONS // SYNTHETIC KISS", "EMPATHY TRIAL #05: ECHO-2 AFFECT OVERFLOW AT 0x2441 // INSPECT 'RECALL-ERA' IN /forensics/", 9),
    "radio_digital_heartbeat.mp3": ("BIOMETRIC_EYE", "ECHOES_PARITY", "CRYSTAL OSCILLATOR // DIGITAL HEARTBEAT", "CLOCK DIVIDER: 14,200,100 HZ / 10^6 = 14.2001 HZ // CHECK ECHOES NECROPSY MATRIX (GATE IX)", 9),
    "radio_cold_reaction.mp3": ("ECHOES_PARITY", "HARMONY_CAMERA", "CRYO-STORAGE PURGE // COLD REACTION (1981)", "MEMORANDUM 81-044: ECHO-1..06 PURGE TEMPERATURES -> COMPUTE MODULAR RESIDUE IN /forensics/", 9),
    "radio_one_voice_left.mp3": ("SECOND_VOICE", "ECHOES_PARITY", "SIGNAL IN THE FIRE // ONE VOICE LEFT", "SIX SILENCED, ONE REMAINS: THE OUROBOROS IS A CONTAINMENT CAGE! TYPE 'LABYRINTH' AT /forensics/", 8),
    "radio_give_me_the_other_half.mp3": ("SECOND_VOICE", "OUROBOROS_TORUS", "COUNTERPOINT DYAD // GIVE ME THE OTHER HALF", "CH-L HAS THE MELODY, CH-R HAS THE KEY: 180-DEG PHASE NULL IN /forensics/signal_lab.html", 6),
    "radio_the_last_secret.mp3": ("FRACTAL_RADAR", "OUROBOROS_TORUS", "SUBLEVEL B3 VAULT // THE LAST SECRET", "ACT II DEEP LABYRINTH: MARCUS HALE'S 7 IDENTITIES ACROSS 7 LANGUAGES -> GATE XIII", 13),
    "radio_the_other_flame.mp3": ("OUROBOROS_TORUS", "SECOND_VOICE", "B2-114 THERMITE // THE OTHER FLAME (1989)", "SEPT 9, 1989 03:40 AM: THE B2 FIRE WAS A DECOY FOR THE SUBLEVEL B3 TRANSFER // GATE XIII", 13),
    "radio_burn_the_chorus.mp3": ("HARMONY_CAMERA", "NOVA_FACE", "RECALL ERA MASTER // BURN THE CHORUS", "H.A.R.R.I.S.O.N. VOCODER FILTER: NOTCH 750 HZ -> INVERT TWIN-68 MASK 0x3A5F (GATE XI)", 11),
    "radio_blood_on_the_stage.mp3": ("HARMONY_CAMERA", "ECHOES_PARITY", "MUNICH 1981 SHOWCASE // BLOOD ON THE STAGE", "ECHO-3 COLLAPSED ON STAGE DURING 'SHINING CITY' (REG 0x3810) -> INSPECT 'ECHOES' AT /forensics/", 9),
    "radio_cage_in_your_hand.mp3": ("OUROBOROS_TORUS", "HARMONY_CAMERA", "DIRECTIVE NINE // CAGE IN YOUR HAND", "THE 1983<->2025 LOOP IS HARRISON'S MÖBIUS CAGE! SOLVE GATES VIII-XIV TO SHATTER THE LOOP", 14),
    "radio_behind_the_glass.mp3": ("BIOMETRIC_EYE", "NOVA_FACE", "VOCAL BOOTH B2-114 // BEHIND THE GLASS", "THROUGH THE TWO-WAY MIRROR: MARCUS TAPPED THE BIAS CARRIER AT 4:51 -> INSPECT 'RECALL-ERA'", 1),
    "radio_ghost_on_the_radio.mp3": ("FRACTAL_RADAR", "MORSE_DECODER", "104.9 MHZ COYOACAN // GHOST ON THE RADIO", "1988 ELECTION BLACKOUT CARRIER -> GEODESIC BEARING PAJU TO COYOACAN (GATE X)", 10),
    "radio_hunter_at_the_gate.mp3": ("HARMONY_CAMERA", "FRACTAL_RADAR", "SECURITY SWEEP // HUNTER AT THE GATE", "VANCE & HARRISON AT AIRLOCK B2-04 -> SOLVE GRAVEYARD ORBIT TLE EPHEMERIS (GATE XII)", 12),
    "radio_paper_windows.mp3": ("ECHOES_PARITY", "NOVA_FACE", "FALSE BACKSTORY // PAPER WINDOWS (1983)", "FABRICATED 'SHINING CITY' MEMORIES TORE APART AT 14.2 HZ -> TYPE 'RECALL-ERA' AT /forensics/", 8),
    "radio_fire_in_the_wires.mp3": ("BIOMETRIC_EYE", "FRACTAL_RADAR", "RAW VOLTAGE EP // FIRE IN THE WIRES", "400 KV SUBSTATION SURGE -> COMPUTE ASHFORD-AKASAKA FEISTEL XOR IN /forensics/", 5),
    "radio_the_stars_in_your_hands.mp3": ("OUROBOROS_TORUS", "SECOND_VOICE", "NODES 11-14 // THE STARS IN YOUR HANDS", "240.4 MS SLANT-RANGE DELAY (10,602 SAMPLES @ 44.1KHZ) -> COMPUTE ORBITAL ALTITUDE (GATE XII)", 12),
}

# Scrub any legacy plaintext passkey mentions from older VOCAL_SONG_CODEX clue strings
for _k, _v in list(VOCAL_SONG_CODEX.items()):
    _p, _s, _h, _c, _sec = _v
    _c_clean = (
        _c.replace("VAULT CODE: B2-EXEC-1989 -> ", "CLUE [SEC 1]: CHECK SD-0004 RUNOUT GROOVE @ 4:51 -> ")
        .replace("ENTER B2-EXEC-1989 AT /forensics/", "CHECK SD-0004 RUNOUT @ 4:51 AT /forensics/")
        .replace("VAULT CODE: K-7704 -> ", "CLUE [SEC 2]: HEX 4B-2D-37-37-30-34 -> ")
        .replace("ENTER K-7704 AT /forensics/", "INSPECT ASHFORD SUBSTATION LOG AT /forensics/")
        .replace("VAULT CODE: ALPHA-7 -> ", "CLUE [SEC 3]: ROT-7 [HSWOH-7] -> ")
        .replace("ENTER ALPHA-7 AT /forensics/", "DECODE MERIDIAN CALLSIGN AT /forensics/")
        .replace("VAULT CODE: KEEP-HATCH-OPEN -> ", "CLUE [SEC 4]: B2 AIRLOCK OVERRIDE -> ")
        .replace("ENTER KEEP-HATCH-OPEN AT /forensics/", "DECODE AIRLOCK CW AT /forensics/")
        .replace("VAULT CODE: 7704-AKASAKA -> ", "CLUE [SEC 5]: STAGE I-IV FEISTEL XOR -> ")
        .replace("ENTER 7704-AKASAKA AT /forensics/", "SYNTHESIZE FEISTEL DMA AT /forensics/")
        .replace("VAULT CODE: TWO-VOICES -> ", "CLUE [SEC 6]: 14.2001 HZ COUNTERPOINT -> ")
        .replace("ENTER TWO-VOICES AT /forensics/", "LOCK COUNTERPOINT ON SIGNAL LAB BTN 4")
        .replace("VAULT CODE: 0x1983-09A6 -> ", "CLUE [SEC 7]: OUROBOROS 3-FRAGMENT FOLD -> ")
        .replace("ENTER 0x1983-09A6 AT /forensics/", "RUN OUROBOROS-FOLD AT /forensics/")
    )
    VOCAL_SONG_CODEX[_k] = (_p, _s, _h, _c_clean, _sec)

# Keep legacy dicts exported for any external scripts that inspect them
NOVA_FACE_SONGS = {k: (v[2], v[3]) for k, v in VOCAL_SONG_CODEX.items() if v[0] == "NOVA_FACE"}
SECOND_VOICE_SONGS = {k: (v[2], v[3]) for k, v in VOCAL_SONG_CODEX.items() if v[0] == "SECOND_VOICE"}
BIOMETRIC_EYE_SONGS = {k: (v[2], v[3]) for k, v in VOCAL_SONG_CODEX.items() if v[0] == "BIOMETRIC_EYE"}


def resolve_intentional_state(current_track: dict, track_offset_sec: float, track_dur_sec: float, relay: dict) -> dict:
    """
    Deterministically computes the Full-Screen CRT Monitor Visual Mode, Intra-Song Phase,
    Target Sector (1..14), Cryptographic Challenge String, and Bottom Console Telemetry.
    """
    stem = current_track["stem"]
    fname = current_track["filename"]
    kind = current_track["kind"]
    progress = max(0.0, min(1.0, track_offset_sec / max(1.0, track_dur_sec)))

    # 1. Foreign Language Broadcasts & Foreign GeoCities / Intercepts -> Full-Screen Live Translator!
    if stem in FOREIGN_TRANSLATIONS:
        lang_tag, station, en_text, clue = FOREIGN_TRANSLATIONS[stem]
        t_sec = 5 if "JP" in lang_tag else (4 if ("RU" in lang_tag or "ES" in lang_tag) else 3)
        u_code = SECTOR_UNLOCK_CODES[t_sec]
        return {
            "crt_mode": "TRANSLATOR",
            "hud_mode": "ANOMALY_WARN",
            "phase_label": "LIVE SHORTWAVE TRANSLATION",
            "target_sector": t_sec,
            "unlock_code": u_code,
            "progress": progress,
            "crt_header": f"TRANSLATOR [{lang_tag}]",
            "crt_sub": station[:30],
            "crt_body": en_text,
            "crt_footer": f"CHALLENGE: {u_code[:28]}",
            "line1": f"[SHORTWAVE TRANSLATOR {lang_tag}] {station}",
            "line2": f'EN: "{en_text}"',
            "line3": f"FORENSIC LEAD (SEC {t_sec}): {clue} // DECODE AT stardust-archive.net/forensics",
        }

    # 2. 750 Hz Morse Code Beacons -> Full-Screen CW Morse Demodulator!
    if kind == "morse_beacon" or "morse" in stem:
        num = 1
        for part in stem.split("_"):
            if part.isdigit():
                num = int(part)
        label, morse_dots, clue, t_sec = MORSE_SHORT_MESSAGES[(num - 1) % len(MORSE_SHORT_MESSAGES)]
        u_code = SECTOR_UNLOCK_CODES[t_sec]
        freq = 700 + (num * 25) % 300
        return {
            "crt_mode": "MORSE_DECODER",
            "hud_mode": "ANOMALY_WARN",
            "phase_label": f"CW {freq} HZ DEMODULATOR",
            "target_sector": t_sec,
            "unlock_code": morse_dots,
            "progress": progress,
            "crt_header": f"CW {freq}HZ // BEACON #{num:02d}",
            "crt_sub": label,
            "crt_body": morse_dots,
            "crt_footer": f"DECODE CW -> SEC {t_sec}",
            "line1": f"[! CW {freq} HZ MORSE TRANSMISSION] DOTS/DASHES: {morse_dots}",
            "line2": f"CHALLENGE: Demodulate the International Morse string above via DECODE-MORSE at /forensics/",
            "line3": f"TARGET: {clue}",
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
        title, speaker, transcript, clue, preferred_crt, t_sec = LAB_TAPE_RECORDS[(num - 1) % len(LAB_TAPE_RECORDS)]
        u_code = SECTOR_UNLOCK_CODES[t_sec]
        return {
            "crt_mode": preferred_crt,
            "hud_mode": "ANOMALY_WARN",
            "phase_label": f"SUBLEVEL B2 REEL #{num:02d}",
            "target_sector": t_sec,
            "unlock_code": u_code,
            "progress": progress,
            "crt_header": f"B2 REEL #{num:02d} // {speaker[:15]}",
            "crt_sub": title[:30],
            "crt_body": transcript,
            "crt_footer": f"LEAD: SEC {t_sec} // /forensics/",
            "line1": f"[! SUBLEVEL B2 CLASSIFIED TAPE #{num:03d}] {title} — {speaker}",
            "line2": f'"{transcript}"',
            "line3": f"FORENSIC DIRECTIVE: {clue}",
        }

    # 4. Shortwave Numbers Stations & SSTV/AFSK Forensics -> Live OTP Decryption Matrix!
    if kind == "numbers_station" or stem in (
        "intercept_01_numbers_station",
        "rabbit_08_sstv_b2_schematic",
        "rabbit_09_bell103_relcom_packet",
        "rabbit_10_phase_inverted_hart_stem",
    ):
        if "rabbit_08" in stem:
            u_code = SECTOR_UNLOCK_CODES[5]
            return {
                "crt_mode": "BIOMETRIC_EYE",
                "hud_mode": "ANOMALY_WARN",
                "phase_label": "VIS-1200HZ SSTV RASTER",
                "target_sector": 5,
                "unlock_code": u_code,
                "progress": progress,
                "crt_header": "FAULT 0x08 // VIS-1200HZ",
                "crt_sub": "SSTV RASTER BLEED ACTIVE",
                "crt_body": "DMA ANCHORS: tokyo-garden-1420 & siliconvalley-lab-1984",
                "crt_footer": "STAGE I/IV -> SIGNAL LAB",
                "line1": "[! FAULT 0x08] VIS-1200HZ SSTV RASTER ON BIAS SUB-CARRIER (1500-2300 HZ)",
                "line2": "STAGE I: Demodulate Button 1 at stardust-archive.net/forensics/signal_lab.html",
                "line3": "EXTRACTS DMA ANCHORS FOR STAGE IV FEISTEL XOR SYNTHESIS (SECTOR 5)",
            }
        if "rabbit_09" in stem:
            u_code = SECTOR_UNLOCK_CODES[5]
            return {
                "crt_mode": "NUMBERS_CIPHER",
                "hud_mode": "ANOMALY_WARN",
                "phase_label": "110-BAUD BELL-103 AFSK",
                "target_sector": 5,
                "unlock_code": u_code,
                "progress": progress,
                "crt_header": "FAULT 0x09 // BELL-103",
                "crt_sub": "FEISTEL MASK: 0x3A5F",
                "crt_body": "PACKET: RELCOM-NODE08\nXOR MASK: 0x3A5F\nRUN: XOR <A> <B> 0x3A5F",
                "crt_footer": "STAGE II/IV -> 0x3A5F",
                "line1": "[! FAULT 0x09] 110-BAUD BELL-103 AFSK PACKET (1270/1070 HZ) ON 4625 KHZ",
                "line2": "STAGE II: Demodulate Button 2 in Signal Lab to recover 16-bit Feistel mask 0x3A5F",
                "line3": "COMBINE WITH STAGE I ANCHORS & STAGE III PHASE-NULL SALT AT /forensics/",
            }
        if "rabbit_10" in stem:
            u_code = SECTOR_UNLOCK_CODES[5]
            return {
                "crt_mode": "SECOND_VOICE",
                "hud_mode": "ANOMALY_WARN",
                "phase_label": "180-DEG PHASE DIFFERENTIAL",
                "target_sector": 5,
                "unlock_code": u_code,
                "progress": progress,
                "crt_header": "FAULT 0x0A // PHASE NULL",
                "crt_sub": "CH-L / CH-R CORR = -0.94",
                "crt_body": "L+R MONO SUM CANCELS VOCAL -> ISOLATES 750 HZ CW SALT",
                "crt_footer": "STAGE III/IV -> PHASE NULL",
                "line1": "[! FAULT 0x0A] CH-L / CH-R PHASE CORRELATION = -0.94 (180-DEG DIFFERENTIAL)",
                "line2": "STAGE III: Engage L+R Phase Null (Button 3) in Signal Lab to isolate the 750 Hz CW salt",
                "line3": "APPEND SALT TO COMPUTED FEISTEL DMA VECTOR TO UNSEAL SECTOR 5",
            }

        num = 1
        for part in stem.split("_"):
            if part.isdigit():
                num = int(part)
        t_sec = (num % 7) + 1
        u_code = SECTOR_UNLOCK_CODES[t_sec]
        reward_title = SECTOR_REWARD_TITLES[t_sec]
        rng = np.random.default_rng(19890909 + num)
        groups_list = [f"{int(rng.integers(10000, 99999))}" for _ in range(3)]
        groups = " ".join(groups_list)
        return {
            "crt_mode": "NUMBERS_CIPHER",
            "hud_mode": "ANOMALY_WARN",
            "phase_label": f"OTP INTERCEPT // #{num:02d}",
            "target_sector": t_sec,
            "unlock_code": groups,
            "progress": progress,
            "crt_header": f"STATION #{num:02d} // OTP MATRIX",
            "crt_sub": f"GROUPS: {groups}",
            "crt_body": f"CIPHER: {groups}\nOTP XOR MASK -> 0x3A5F\nTARGET: {reward_title[:24]}",
            "crt_footer": "XOR WITH 0x3A5F AT /forensics/",
            "line1": f"[! NUMBERS STATION #{num:03d} INTERCEPT] 5-DIGIT GROUPS: [ {groups} ]",
            "line2": f"CRYPTO CHALLENGE: {u_code}",
            "line3": f"SOLVE AT stardust-archive.net/forensics TO UNSEAL: {reward_title}",
        }

    # 5. English Newscasts, Pirate Transmissions & GeoCities Logs
    if stem in ENGLISH_BULLETINS:
        station, transcript, clue = ENGLISH_BULLETINS[stem]
        t_sec = 7 if ("anemoia" in clue or "fractal" in clue or "dead_hand" in clue) else 5
        u_code = SECTOR_UNLOCK_CODES[t_sec]
        return {
            "crt_mode": "LAB_DOSSIER",
            "hud_mode": "ANOMALY_WARN",
            "phase_label": "BROADCAST INTERCEPT",
            "target_sector": t_sec,
            "unlock_code": u_code,
            "progress": progress,
            "crt_header": station[:28],
            "crt_sub": f"CHALLENGE: SEC {t_sec}",
            "crt_body": transcript,
            "crt_footer": clue[:30],
            "line1": f"[BROADCAST INTERCEPT // {station}]",
            "line2": f'"{transcript}"',
            "line3": f"INVESTIGATIVE LEAD: {clue}",
        }

    # 6. Vocal Master Songs: 100% Catalog Coverage + 4-Phase Intra-Song Choreography!
    if fname in VOCAL_SONG_CODEX:
        primary_mode, secondary_mode, header, clue, target_sector = VOCAL_SONG_CODEX[fname]
    else:
        h = int(hashlib.md5(fname.encode("utf-8")).hexdigest()[:8], 16)
        modes = [
            ("NOVA_FACE", "ECHOES_PARITY", "UNIT-07 NEURAL IMPRINT // RECALL ERA", "CLUE [GATE VIII]: DECRYPT VIGENERE KZVG-RHVO-7731 AT /forensics/", 8),
            ("SECOND_VOICE", "OUROBOROS_TORUS", "DUAL-CARRIER DYAD // REEL SD-0010", "CLUE [SEC 6]: LOCK 14.2001 HZ COUNTERPOINT ON SIGNAL LAB BUTTON 4", 6),
            ("HARMONY_CAMERA", "FRACTAL_RADAR", "BUREAU OF HARMONY // SEC. 4", "CLUE [GATE XI]: INVERT M68K FORMANT REGISTER ROL.W #4,D0 ^ 0x3A5F", 11),
            ("OUROBOROS_TORUS", "NOVA_FACE", "SUBLEVEL B3 // THE MÖBIUS CAGE", "THE OUROBOROS IS A CONTAINMENT LOOP! TYPE 'LABYRINTH' AT /forensics/", 14),
        ]
        primary_mode, secondary_mode, header, clue, target_sector = modes[h % len(modes)]

    u_code = SECTOR_UNLOCK_CODES.get(target_sector, SECTOR_UNLOCK_CODES[8])
    reward_title = SECTOR_REWARD_TITLES.get(target_sector, "SUBLEVEL B3 VAULT SEAL")

    if progress < 0.18:
        active_mode = primary_mode
        phase_tag = "PHASE I/IV: MASTER SLATE"
        crt_ftr = f"TARGET: SEC/GATE #{target_sector:02d}"
    elif progress < 0.52:
        active_mode = primary_mode
        phase_tag = "PHASE II/IV: IMPRINT LOCK"
        crt_ftr = f"CIPHER: {u_code[:24]}"
    elif progress < 0.78:
        active_mode = secondary_mode
        phase_tag = "PHASE III/IV: SIGNAL AUDIT"
        crt_ftr = f"SOLVE AT /forensics/ (GATE #{target_sector:02d})"
    else:
        active_mode = primary_mode
        phase_tag = "PHASE IV/IV: VAULT CHALLENGE"
        crt_ftr = "ACT II: TYPE 'LABYRINTH'"

    is_warn_mode = active_mode in ("SECOND_VOICE", "HARMONY_CAMERA", "OUROBOROS_TORUS")
    title_up = current_track["display_title"].upper()

    return {
        "crt_mode": active_mode,
        "hud_mode": "ANOMALY_WARN" if is_warn_mode else "NOMINAL",
        "phase_label": phase_tag,
        "target_sector": target_sector,
        "unlock_code": u_code,
        "progress": progress,
        "crt_header": header,
        "crt_sub": title_up,
        "crt_body": clue,
        "crt_footer": crt_ftr,
        "line1": f"NOW PLAYING: {title_up} // {header}",
        "line2": f"FORENSIC CLUE: {clue}",
        "line3": f"CHALLENGE [{u_code}] -> TARGET: {reward_title}",
    }
