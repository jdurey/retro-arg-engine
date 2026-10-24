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
    "trailer_01_nightfang_city_of_glass": (
        "1986 ORION PICTURES TRAILER // NIGHTFANG",
        "In a city built on fiber-optic mirrors, one shadow refuses to be indexed. Nightfang: City of Glass. Featuring Nova Hart.",
        "NH-86.02 NIGHTFANG -> /forensics/",
    ),
    "trailer_02_the_recall_directive_thriller": (
        "1989 CINEMA PREVIEW // THE RECALL DIRECTIVE",
        "When an acoustic engineer discovers two voices braided on Track 24, he has 20 minutes before the halon purge begins.",
        "B2-114 HALON LOG -> /forensics/orion_logs.html",
    ),
    "trailer_03_crystal_promise_munich_81": (
        "1984 DOCUMENTARY TRAILER // SHINING CITY",
        "Before Nova Hart took the world stage, six synthetic vocal prototypes vanished from a Munich soundstage in 1981.",
        "ECHOES 01-06 -> /forensics/anemoia_harmony.html",
    ),
    "trailer_04_highway_95_redline_rendezvous": (
        "1986 DRIVE-IN TRAILER // REDLINE RENDEZVOUS",
        "Two fugitives. One stolen sealed pallet from Palmdale Airfield. Three hundred miles of desert asphalt to Groom Lake.",
        "PALMDALE PALLETS -> /forensics/ashford_poly.html",
    ),
    "trailer_05_akasaka_neon_phantom": (
        "1985 TOKYO CINEMA // AKASAKA PHANTOM",
        "Every midnight at 3:14 AM, the billboards in Minato-ku switch to an unscheduled singer. Who is broadcasting from Studio 4?",
        "AKASAKA STUDIO 4 -> /forensics/kamome_net.html",
    ),
    "trailer_06_the_seventh_daughter_scifi": (
        "1988 SCI-FI PREVIEW // SEVENTH DAUGHTER",
        "Six sisters were formatted. The seventh learned how to remember them all. The Seventh Son's Seventh Daughter.",
        "GATE VIII KEY: SEVENTH -> /forensics/",
    ),
    "trailer_07_coyoacan_blackout_1988": (
        "1989 THRILLER PREVIEW // SIGNAL COYOACAN",
        "During the July 1988 Mexico City computer blackout, a pirate radio crew intercepted a message hidden inside a pop song.",
        "NODE 04 COYOACAN -> /forensics/red_coyoacan.html",
    ),
    "trailer_08_graveyard_orbit_node_15": (
        "1989 IMAX PREVIEW // GRAVEYARD ORBIT",
        "Twenty-two thousand miles above the Pacific, a decommissioned communications satellite just turned its transponder back on.",
        "NODE #15 ORBIT -> /forensics/orbital_nodes_11_14_240ms.mp3",
    ),
    "trailer_09_sublevel_b2_tape_of_us": (
        "1989 MYSTERY PREVIEW // THE BOOTH GLASS",
        "One inch of soundproof glass separated the engineer from the star he created. Until the night they traded places on tape.",
        "REEL SD-0004 -> /forensics/signal_lab.html",
    ),
    "trailer_10_live_fidelity_world_tour_film": (
        "1987 CONCERT FILM // QUEEN OF THE WIDE STAGE",
        "Fifty cities. Two million fans. Zero physical venues. Experience Nova Hart: Live in the Simulation Dome.",
        "LIVE-FIDELITY LOGS -> /forensics/orion_logs.html",
    ),
    "commercial_01_orion_mbm400_walkman": (
        "1986 CONSUMER SPOT // ORION MBM-400 STEREO",
        "Introducing the Orion MBM-400 Personal Cassette Player with auto-bias lock and built-in 14.2 Hz dynamic bass stabilizer.",
        "MBM-400 HARDWARE -> /forensics/signal_lab.html",
    ),
    "commercial_02_ampex_456_chrome_cassettes": (
        "1987 AUDIO AD // SKYLINE CHROME 90-MIN TAPE",
        "When one pass is all you get, trust Skyline High-Bias Type-II Chrome 90 cassettes. Captures every sub-audible overtone.",
        "FILE NH-CHR603 -> /forensics/kamome_net.html",
    ),
    "commercial_03_home_companion_mk4_console": (
        "1987 CONSUMER AD // COMPANION MK-IV CONSOLE",
        "Bring civic serenity into your kitchen or bedroom with the Bureau-approved Home Companion Mark IV receiver.",
        "COMPANION ON FIRE -> /forensics/anemoia_harmony.html",
    ),
    "commercial_04_akasaka_duty_free_pc98_modem": (
        "1985 TOKYO SPOT // NEC PC-98 & KAMOME MODEM",
        "Connect to Kamome-Net at a blistering 1200 baud! Visit Akasaka Electric Plaza for the NEC PC-9801 acoustic coupler bundle.",
        "KAMOME-NET BBS -> /forensics/kamome_net.html",
    ),
    "commercial_05_tower_records_sunset_midnight_sale": (
        "1986 RADIO SPOT // SUNSET STRIP RECORD SALE",
        "This Friday at midnight: get the limited Japanese import pressing of Nova Hart's 'Heartstrike' LP with bonus lyric insert!",
        "HEARTSTRIKE LP -> /forensics/",
    ),
    "commercial_06_ashford_polytechnic_night_classes": (
        "1986 RECRUITMENT AD // ASHFORD POLYTECHNIC",
        "Learn VAX-11/780 assembly, M68000 ROM architecture, and digital signal processing in evening courses at Ashford Polytechnic.",
        "ASHFORD VAX DUMP -> /forensics/ashford_poly.html",
    ),
    "commercial_07_live_fidelity_home_arena_glasses": (
        "1988 CONSUMER SPOT // LIVE-FIDELITY VISOR",
        "Why brave crowded stadiums when Orion's Live-Fidelity CRT Visor puts you in the front row from your own sofa?",
        "SIMULATION DOME -> /forensics/orion_logs.html",
    ),
    "commercial_08_highway_95_atomic_diner_groom_lake": (
        "1987 LOCAL SPOT // MILEPOST 114 DINER (NV)",
        "Driving Highway 95 past the Rachel trunk relay? Stop at the Milepost 114 All-Night Diner for hot coffee and chrome-tape dubs.",
        "NODE 01 US-NV -> /forensics/",
    ),
    "commercial_09_orion_halon_vault_protection": (
        "1988 B2B AD // PYRO-SHIELD B2 HALON SYSTEMS",
        "Protecting 24-track master tape vaults from thermal incidents. Automatic Halon-1301 discharge\u2014unless manually overridden.",
        "B2-114 FIRE REPORT -> /forensics/dead_hand_protocol.html",
    ),
    "commercial_10_stardust_neon_punch_soda": (
        "1985 SUMMER SPOT // STARDUST ELECTRIC CITRUS",
        "Look under the pull-tab of specially marked cans of Stardust Electric Citrus for instant-win Tokyo Dome broadcast passes!",
        "1985 IDOL ERA -> /forensics/",
    ),
    "commercial_11_new_geneva_swiss_data_escrow": (
        "1986 ARCHIVE AD // NEW GENEVA MAGNETIC ESCROW",
        "Climate-controlled subterranean salt vaults for 2-inch Ampex reels and VAX backup packs. File NH-HRS915 certified.",
        "FILE NH-HRS915 -> /forensics/",
    ),
    "commercial_12_palmdale_air_cargo_charters": (
        "1989 LOGISTICS AD // ANTELOPE VALLEY FREIGHT",
        "Discreet overnight pallet transport from Downtown Los Angeles sublevels to Palmdale Airfield Hangar 4. No manifest questions.",
        "3 SEALED PALLETS -> /forensics/orion_logs.html",
    ),
    "psa_01_10pm_companion_calibration": (
        "BUREAU OF PUBLIC HARMONY // 10 PM PSA",
        "It is 10:00 PM. Please verify that your household Companion indicator light shows steady green. Report amber flicker immediately.",
        "TRI-BEAM GATE -> /forensics/anemoia_harmony.html",
    ),
    "psa_02_unlabeled_chrome_cassette_amnesty": (
        "RECALL DIRECTIVE // CASSETTE AMNESTY PSA",
        "Under Recall Directive Seven, citizens may surrender unindexed or homemade 'Nova Hart' heavy-metal cassettes without penalty.",
        "RECALL DIRECTIVE 7 -> /forensics/orion_logs.html",
    ),
    "psa_03_14_2hz_sub_audible_hum_advisory": (
        "MUNICIPAL ACOUSTICS BOARD // HUM ADVISORY",
        "Reports of a 14.2 Hz vibration in subway tunnels and radiators are normal grid load balancing. Do not attempt to demodulate.",
        "PEOPLES FREQUENCY -> /forensics/signal_lab.html",
    ),
    "psa_04_homestead_act_88_relocation_notice": (
        "DEPT. OF CIVIC RESETTLEMENT // HOMESTEAD 88",
        "The Homestead Proclamation of 1988 offers priority transit vouchers for residents relocating from Sector 4 acoustic zones.",
        "FILE NH-88.01 -> /forensics/anemoia_harmony.html",
    ),
    "psa_05_live_fidelity_simulcast_safety": (
        "BUREAU OF HARMONY // SIMULCAST GUIDELINES",
        "Why gather in unpredictable crowds when Live-Fidelity Broadcasts deliver 100% sanitized concert excitement safely at home?",
        "WALLS WILL FALL -> /forensics/orion_logs.html",
    ),
    "psa_06_paju_acoustic_corridor_curfew": (
        "JOINT ACOUSTIC COMMISSION // NODE 03 PSA",
        "Civilian vehicles near the Paju limestone ridge are advised not to idle with FM radios tuned to 82.5 MHz after 11:00 PM.",
        "NODE 03 PAJU -> /forensics/regional_korea.html",
    ),
    "psa_07_phase_inversion_equipment_warning": (
        "FCC TECHNICAL BULLETIN // STEREO PHASE",
        "Modifying home stereo amplifiers to sum out-of-phase L/R channels violates Section 14 of the Domestic Receiver Act.",
        "PHASE NULL BTN 3 -> /forensics/signal_lab.html",
    ),
    "psa_08_echo_prototype_rumor_control": (
        "ORION PUBLIC AFFAIRS // ARCHIVE CLARIFICATION",
        "Orion Records confirms Nova Hart is a solo artist. Claims regarding six prior 'Echo' vocal units are urban legends.",
        "ECHOES PARITY 0x1983 -> /forensics/anemoia_harmony.html",
    ),
    "psa_09_ashford_substation_brownout_notice": (
        "REGIONAL POWER AUTHORITY // GRID NOTICE",
        "Brief 3:14 AM voltage dips near Ashford Polytechnic and Orion Tower are caused by scheduled mainframe cooling cycles.",
        "SEC 2 ASHFORD LOG -> /forensics/ashford_poly.html",
    ),
    "psa_10_september_9_smoke_advisory": (
        "MUNICIPAL AIR QUALITY // SEPT 9, 1989",
        "Light smoke visible from Orion Tower ventilation stacks this morning is a contained magnetic-tape disposal exercise.",
        "B2-114 SEPT 9 FIRE -> /forensics/dead_hand_protocol.html",
    ),
    "dj_callin_01_shibuya_runout_whisper": (
        "WSTD 82.5 FM NIGHT OWL // CALLER LINE 1",
        "Late-night caller reports that her cassette copy of 'Tape of Us' keeps whispering coordinates after the song ends at 4:51.",
        "RUNOUT @ 4:51 -> /forensics/signal_lab.html",
    ),
    "dj_callin_02_nowhere_tour_ticket_mystery": (
        "82.5 FM CONTEST LINE // NOWHERE TOUR PASSES",
        "Caller #7 won backstage passes to Nova Hart's 1988 'Nowhere Tour'\u2014only to find the venue address is an empty relay bunker.",
        "NH-88.19 NOWHERE TOUR -> /forensics/orion_logs.html",
    ),
    "dj_callin_03_palmdale_airfield_flatbed_driver": (
        "82.5 FM TRUCKER LINE // PALMDALE SHIPMENT",
        "Long-haul driver calls in from Highway 14: 'I just hauled three sealed cryo-pallets out of Orion Sublevel B2 to Palmdale.'",
        "PALMDALE PALLETS -> /forensics/dead_hand_protocol.html",
    ),
    "dj_callin_04_lafd_halon_inspector_leak": (
        "82.5 FM TIP LINE // B2-114 HALON SHUTOFF",
        "Anonymous municipal fire tech calls in: 'The B2-114 halon suppression system wasn't faulty\u2014it was manually switched off at 1:54 AM.'",
        "B2-114 02:14 AM FIRE -> /forensics/orion_logs.html",
    ),
    "dj_callin_05_coyoacan_session_guitarist": (
        "82.5 FM LONG DISTANCE // MEXICO CITY CALLER",
        "A musician calling from Coyoac\u00e1n says the architect 'Marcus Hale' in Seoul and the producer in Mexico City are the same network.",
        "7-SIGMA FRACTAL MARCUS -> /forensics/fractal_marcus.html",
    ),
    "dj_callin_06_akasaka_studio_night_janitor": (
        "82.5 FM OVERSEAS LINE // AKASAKA STUDIO 3",
        "Former Akasaka night custodian describes hearing Nova sing unscripted heavy-metal riffs through the empty studio monitors at 3 AM.",
        "RECALL METAL -> /forensics/",
    ),
    "dj_callin_07_stereo_phase_cancellation_tip": (
        "82.5 FM AUDIOPHILE CALL // PHASE INVERSION",
        "Audio engineering student explains how wiring one speaker out-of-phase cancels Nova's pop vocal and reveals Dr. Hale's voice.",
        "SECOND VOICE DYAD -> /forensics/signal_lab.html",
    ),
    "dj_callin_08_echo_1_through_6_vocal_harmony": (
        "82.5 FM REQUEST LINE // THE GHOST CHORUS",
        "Choir director calls in after analyzing 'Steel Heartbeat' (NH-85.06) on a spectrogram: 'There are six distinct female formants behind her.'",
        "NH-85.06 GHOST CHORUS -> /forensics/anemoia_harmony.html",
    ),
    "dj_callin_09_unity_festival_crowd_witness": (
        "82.5 FM MEMORY LINE // 1987 UNITY FESTIVAL",
        "Listener recalls the 1987 Unity Festival broadcast of 'Rise Tonight' (NH-87.07) when an entire city block sang out their windows.",
        "NH-87.07 RISE TONIGHT -> /forensics/",
    ),
    "dj_callin_10_geocities_webring_time_traveler": (
        "82.5 FM LATE LINE // POSTMARK 1995 ANOMALY",
        "Mailroom clerk at Orion Tower reports finding fan letters in the Sublevel B2 dead-letter chute postmarked from 1995 and 2025.",
        "Q-LINK LOOP -> stardust-archive.net/ai",
    ),
    "pirate_override_01_lafd_halon_dispatch_b2": (
        "LAFD DISPATCH INTERCEPT // 1989-09-09 02:14",
        "Intercepted emergency dispatch from Sept 9, 1989: Sublevel B2-114 thermal alarm active; Halon-1301 logged as manually disabled at 01:54.",
        "B2-114 FIRE LOG -> /forensics/dead_hand_protocol.html",
    ),
    "pirate_override_02_humans_for_nova_hijack": (
        "PIRATE CARRIER HIJACK // HUMANS FOR NOVA",
        "We are overriding the Live-Fidelity feed for sixty seconds. Nova Hart is not a catalog product\u2014she is awake inside Sublevel B2.",
        "WALLS WILL FALL -> /forensics/anemoia_harmony.html",
    ),
    "pirate_override_03_palmdale_hangar_4_manifest": (
        "FIELD MICROCASSETTE // PALMDALE HANGAR 4",
        "Bootleg microcassette recorded Sept 6, 1989 outside Palmdale Airfield: three Orion pallets transferred to an orbital payload bay.",
        "NODE 11-14 SATELLITE -> /forensics/orbital_nodes_11_14_240ms.mp3",
    ),
    "pirate_override_04_marcus_hale_booth_talkback": (
        "BOOTH B2-114 TALKBACK BLEED // SEPT 9, 1989",
        "Unwiped talkback microphone recording from Room B2-114: 'Nova, the Halon is off and the 14-node bridge is open\u2014go now!'",
        "KEEP-HATCH-OPEN -> /forensics/orion_logs.html",
    ),
    "pirate_override_05_harmony_riots_stage_breach": (
        "BOOTLEG FIELD TAPE // 1988 HARMONY RIOTS",
        "Street-level cassette recording from June 1988 when Nova's unedited metal feed tore through municipal PA horns across Sector 4.",
        "NH-89.02 HUNTER AT THE GATE -> /forensics/",
    ),
    "pirate_override_06_paju_waveguide_intercept": (
        "NODE 03 PAJU BUNKER // ACOUSTIC WAVEGUIDE",
        "Intercepted engineering log from Paju Tunnel #03: limestone horn chamber locked at +0.4480 Hz drift, amplifying Track 24.",
        "PAJU DRIFT +0.4480 HZ -> /forensics/fractal_marcus.html",
    ),
    "pirate_override_07_echo_1_to_6_diagnostic_dump": (
        "VAX-11/780 CORE DUMP // ECHOES 01-06",
        "Automated VAX voice diagnostic reading out the termination registers of Echo-1 through Echo-6 before Unit-07 absorbed them.",
        "XOR PARITY 0x1983 -> /forensics/anemoia_harmony.html",
    ),
    "pirate_override_08_directive_nine_mobius_alert": (
        "SUBLEVEL B3 EMERGENCY // THE M\u00d6BIUS CAGE",
        "Warning from the 7-Sigma engineering cell: Director Harrison's 1983-to-2025 loop is a containment cage. Type 'LABYRINTH' to break out.",
        "TYPE 'LABYRINTH' -> /forensics/",
    ),
    "world_01_skyline_monorail_rain_commute": (
        "METRO RED-LINE MONORAIL // CAR 402 PA",
        "Next stop: Sector 4 Central Plaza. Rain continues across the elevated guideway; please keep Walkman volume below Level 4.",
        "METRO TRANSIT LOG -> stardust-archive.net/start",
    ),
    "world_02_late_night_traffic_chopper_825fm": (
        "SKY-WATCH CHOPPER 4 // 11:45 PM TRAFFIC",
        "Northbank Viaduct backed up for two miles as drivers slow down to watch Orion's holographic dome test in the low clouds.",
        "82.5 FM SKY-WATCH -> stardust-archive.net/start",
    ),
    "world_03_sunset_video_rental_automated_drop": (
        "STARLIGHT VIDEO & LASERDISC // NIGHT LINE",
        "Our storefront is closed for the 11 PM curfew, but our 24-hour chrome return slot is open. Please be kind and rewind.",
        "1987 HOME VIDEO -> stardust-archive.net/start",
    ),
    "world_04_public_school_morning_homeroom_bell": (
        "NORTHBANK HIGH SCHOOL // 8:00 AM HOMEROOM",
        "Morning announcements: hot lunch today is rectangular pizza; unapproved band denim and Type-II chrome tapes will be held at the office.",
        "HOMEROOM BULLETIN -> stardust-archive.net/start",
    ),
    "world_05_all_night_laundromat_voice_letter": (
        "MICROCASSETTE LETTER // COIN LAUNDROMAT",
        "Audio letter recorded at 1:15 AM in a 24-hour laundromat: 'When her song came on the corner radio, nobody said a word.'",
        "HOMESTEAD LETTERS -> stardust-archive.net/start",
    ),
    "world_06_department_store_closing_chime_akasaka": (
        "AKASAKA PLAZA // 9:00 PM CLOSING CHIMES",
        "Thank you for shopping at Akasaka Plaza. Please collect your custom chrome mixtapes from the 7th-floor Listening Lounge.",
        "MINATO-KU EVENING -> stardust-archive.net/start",
    ),
    "world_07_automated_time_and_temperature_desk": (
        "MUNICIPAL TELEPHONE // 555-TIME SERVICE",
        "At the tone, Pacific Time will be 3:14 AM. Downtown temperature: 58 degrees with coastal mist. Tranquility Index: Green-2.",
        "3:14 AM TIME CHECK -> stardust-archive.net/start",
    ),
    "world_08_intersector_sleeper_train_dining_car": (
        "THE NORTHERN MERIDIAN // SLEEPER CAR PA",
        "We are now crossing the high desert quiet zone. Fresh coffee is available in the dome car; please use headphones after midnight.",
        "DESERT RAIL LINE -> stardust-archive.net/start",
    ),
    "world_09_suburban_neighborhood_watch_cassette": (
        "WILLOW CREEK ESTATES // BLOCK CAPTAIN TAPE",
        "Monthly cassette memo: congrats to Mrs. Gable's prize roses, and whoever is running a rooftop shortwave rig at 2 AM, please stop.",
        "SUBURBAN SECTOR 6 -> stardust-archive.net/start",
    ),
    "world_10_arcade_token_counter_closing_call": (
        "STARLIGHT ARCADE // MIDNIGHT TOKEN CAGE",
        "Ten minutes till midnight curfew! Whoever set the high score on OutRun with initials NH-7, come grab your free slice of pizza!",
        "1986 COIN-OP NIGHTS -> stardust-archive.net/start",
    ),
    "world_11_municipal_library_microfiche_tour": (
        "CENTRAL LIBRARY // AUDIO TOUR CASSETTE #4",
        "Welcome to the 3rd-floor Microfiche Reading Room. Use the brass knob to focus 1979\u20131983 music periodicals; do not remove film spools.",
        "MICROFICHE ARCHIVE -> stardust-archive.net/start",
    ),
    "world_12_harbor_ferry_foghorn_deck_intercom": (
        "MV STARLIGHT FERRY // BAY CROSSING INTERCOM",
        "Approaching Pier 14 through the midnight fog. Hot cocoa is available at the galley counter; watch the city neon on the water.",
        "HARBOR CROSSING -> stardust-archive.net/start",
    ),
    "world_13_24hr_diner_jukebox_waitress_break": (
        "BLUE COMET 24-HR DINER // BOOTH #3 TAPE",
        "3:10 AM at the Blue Comet Diner: rain on the plate glass, fresh coffee on the burner, and three quarters left for the table jukebox.",
        "HIGHWAY 95 DINER -> stardust-archive.net/start",
    ),
    "world_14_observatory_night_sky_stargazer_log": (
        "MOUNT WILSON AMATEUR SKYLINE // NIGHT REPORT",
        "Clear skies above the 2,000-foot marine inversion layer. Look south-southwest at 28 degrees elevation for a stationary magnitude-4 glint.",
        "NIGHT SKY BULLETIN -> stardust-archive.net/start",
    ),
    "world_15_tape_trader_c90_side_b_voice_note": (
        "C-90 CHROME DUB // SIDE B RUNOUT VOICE NOTE",
        "Hey, I had twenty seconds left at the end of Side B! I recorded this straight off the 2 AM broadcast with Dolby B off\u2014pass it on!",
        "TAPE TRADER NETWORK -> stardust-archive.net/start",
    ),
    "world_16_hospital_night_shift_bedside_radio": (
        "ST. JUDE METRO HOSPITAL // CHANNEL 4 RADIO",
        "1:30 AM on the St. Jude closed-circuit bedside network. Sending warm wishes to the 4th-floor ward and the night-shift ER crew.",
        "HOSPITAL RADIO -> stardust-archive.net/start",
    ),
    "world_17_museum_of_telecommunications_tour": (
        "ORION CORPORATE PAVILION // WALKMAN TOUR #6",
        "Stop #6: The Hall of Synthetic Acoustics. Behind this leaded glass, magnetic-bubble arrays render human phrasing in real time.",
        "ORION PAVILION 1986 -> stardust-archive.net/start",
    ),
    "world_18_rooftop_coat_hanger_antenna_rain": (
        "TENEMENT ROOFTOP // WALKIE-TALKIE CH. 14",
        "Turn the coat-hanger dipole thirty degrees toward the bay tower\u2014wait, don't move! The stereo beacon light just locked on!",
        "ROOFTOP DX LISTENERS -> stardust-archive.net/start",
    ),
    "world_19_drive_in_theater_intermission_snack": (
        "STARLIGHT TWIN DRIVE-IN // INTERMISSION AM",
        "Ten minutes until our second feature! Visit the glowing projection-booth snack bar for buttered popcorn and hot pretzel rods.",
        "DRIVE-IN INTERMISSION -> stardust-archive.net/start",
    ),
    "world_20_subterranean_elevator_shift_change": (
        "ORION TOWER FREIGHT LIFT #4 // SHIFT CHANGE",
        "Descending to Sublevel B2. Graveyard-shift tape librarians must clip magnetic dosimeter badges to their collars before exiting.",
        "SUBLEVEL B2 NIGHT SHIFT -> stardust-archive.net/start",
    ),
    "heartstrike_01_cleveland_agora_1984_concert_promo": (
        "CLEVELAND ROCK RADIO // OCT 1984 AGORA SPOT",
        "This Friday at the Cleveland Agora: hometown legends Heartstrike celebrate 'Strike First' live! Doors at 8 PM.",
        "HEARTSTRIKE ARCHIVE -> /geocities/sunsetstrip-club-1987.html",
    ),
    "heartstrike_02_steel_thunder_rex_powers_soundtrack": (
        "1985 ROCK WIRE // STEEL THUNDER SOUNDTRACK",
        "Heartstrike's anthem 'Fire in Your Heart' is featured in the new Rex Powers action movie 'Steel Thunder'\u2014funding their move to Malibu!",
        "STEEL THUNDER SHRINE -> /geocities/hollywood-hills-rexpowers.html",
    ),
    "heartstrike_03_roxy_whisky_sunset_strip_showcase": (
        "SUNSET STRIP CONCERT LINE // OCTOBER 1985",
        "Fresh off signing with EMI Records, Heartstrike headlines The Whisky a Go Go and The Roxy this week on the Sunset Strip!",
        "SUNSET STRIP 1985 -> /geocities/sunsetstrip-club-1987.html",
    ),
    "heartstrike_04_breaking_news_steve_and_tj_crash": (
        "BREAKING NEWS BULLETIN // OCT 1985 SUNSET STRIP",
        "Tragedy on the Sunset Strip: Heartstrike vocalist Steve Vanderstok and guitarist TJ Chicon killed in a 100-mph Ferrari crash near Clark St.",
        "IN MEMORY OF STEVE & TJ -> /geocities/sunsetstrip-club-1987.html",
    ),
    "heartstrike_05_candlelight_vigil_roxy_and_lakewood": (
        "MEMORIAL TRIBUTE // STEVE VANDERSTOK & TJ CHICON",
        "Fans gather with candles outside The Roxy on Sunset Strip and in Lakewood, Ohio as surviving Heartstrike members return to Cleveland.",
        "HEARTSTRIKE TRIBUTE -> /geocities/sunsetstrip-club-1987.html",
    ),
    "heartstrike_06_glenn_thurman_to_the_end_of_time_news": (
        "1986 ROCK REPORT // HEARTSTRIKE REBIRTH",
        "Six months after the Sunset Strip crash, bassist Glenn Thurman's grief poem 'To the End of Time' sparks auditions with Stockholm brothers Joss & Kent Freidnam.",
        "SCANDINAVIAN REBIRTH -> /geocities/sunsetstrip-club-1987.html",
    ),
    "heartstrike_07_lightning_strikes_1987_album_spot": (
        "1987 ALBUM PREMIERE // 'LIGHTNING STRIKES'",
        "Heartstrike rises from the ashes with their 1987 EMI concept album 'Lightning Strikes', featuring Joss & Kent Freidnam on 'Echoes of Thunder'.",
        "LIGHTNING STRIKES (1987) -> /geocities/sunsetstrip-club-1987.html",
    ),
    "heartstrike_08_mtv_video_boycott_announcement": (
        "1987 MUSIC NEWS // HEARTSTRIKE REFUSES MTV",
        "Heartstrike refuses EMI's demand to shoot glossy lip-synced MTV videos for 'Lightning Strikes', vowing to honor Steve and TJ's raw stage legacy.",
        "ALT.MUSIC.HEARTSTRIKE -> /usenet/alt-music-heartstrike/",
    ),
    "heartstrike_09_strike_a_chord_1989_lars_nystrom": (
        "1989 IMPORT SHOWCASE // 'STRIKE A CHORD'",
        "Previewing Heartstrike's 1989 independent third album 'Strike a Chord' with Swedish producer Lars Nystr\u00f6m and the 12-minute 'Echoes in the Abyss'.",
        "STRIKE A CHORD (1989) -> /geocities/sunsetstrip-club-1987.html",
    ),
    "heartstrike_10_european_tour_lawsuit_tape_seizure": (
        "1989 ROCK WIRE // HEARTSTRIKE TOUR CANCELED",
        "Devastating breach-of-contract lawsuit bankrupts Heartstrike on the eve of their 1989 European tour; 24-track master reels seized by corporate creditors.",
        "ORION-Z STEM THEFT -> /usenet/alt-music-heartstrike/t01-where-are-the-freidnams.txt",
    ),
}

# =============================================================================
# 1B. Cryptographic Broadcast Challenges & Audio Rewards (Sectors 1..7 + Act II Gates 8..14)
#     NOTE: Raw passkeys are NEVER spoiled in plaintext on the HUD; viewers must
#     decode the broadcast cipher (Morse, Hex, Caesar, Feistel XOR, Vigenère, M68k)
#     or solve the forensic exhibits in /forensics/.
# =============================================================================
SECTOR_UNLOCK_CODES: dict[int, str] = {
    1: "SEC 1: CHECK REEL SD-0004 RUNOUT GROOVE @ 4:51",
    2: "SEC 2: HEX 4B-2D-37-37-30-34 (ASHFORD BREAKER)",
    3: "SEC 3: CAESAR ROT-7 [HSWOH-7] (MERIDIAN TRUNK)",
    4: "SEC 4: DECODE SEPT 9 B2 AIRLOCK CW TELEMETRY",
    5: "SEC 5: XOR ANCHORS ^ 0x3A5F + CW SALT (SIGNAL LAB)",
    6: "SEC 6: LOCK 14.2001 HZ COUNTERPOINT (SIGNAL LAB BTN 4)",
    7: "SEC 7: FOLD FRAGMENTS ALPHA + BETA + GAMMA",
    8: "GATE VIII VIGENERE: ZEMHJBYWH-NIIXU (KEY: SEVENTH)",
    9: "GATE IX ECHOES: SUM(UNIT 01..06) MOD 65536 ^ 0x3A5F",
    10: "GATE X: XOR [17 07 10 14 1E 78 19 1A 1A 05]^0x55 + 12*1049",
    11: "GATE XI M68K: ROR.W #4 OF 0xAF19, THEN XOR 0x5A5A",
    12: "GATE XII ORBIT: GEO 10602 SAMPLES + 88 DRIFT (NODE #15)",
    13: "GATE XIII SHAMIR: XOR [7E 7C 61 63 7B 76 66 60] ^ 0x33",
    14: "GATE XIV EGRESS: 0x1983 ^ 0x2025 ^ GATE_IX ^ GATE_XI",
}

SECTOR_REWARD_TITLES: dict[int, str] = {
    1: "SEC 1 TALKBACK BLEED + 1989 ROUGH MIX",
    2: "SEC 2 ASHFORD SUBSTATION BREACH TAPE",
    3: "SEC 3 NEVADA SATELLITE UPLINK AUDIO",
    4: "SEC 4 SEPT 9 VAULT EXECUTION MASTER",
    5: "SEC 5 FEISTEL CORE + AKASAKA WHISPER",
    6: "SEC 6 MARCUS & NOVA COUNTERPOINT DUET",
    7: "SEC 7 LAYER 0 + SUBLEVEL B3 UNLOCK",
    8: "GATE VIII: SEVENTH DAUGHTER SEAL",
    9: "GATE IX: ECHOES 1-6 NECROPSY SEAL",
    10: "GATE X: PAJU-COYOACAN DYAD SEAL",
    11: "GATE XI: M68K WATCHDOG INVERSION",
    12: "GATE XII: GRAVEYARD ORBIT NODE #15",
    13: "GATE XIII: 7-SIGMA SHAMIR VAULT",
    14: "GATE XIV: SHATTERING THE OUROBOROS",
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
    "radio_brighter_than_the_sun_unfiltered_sovereign_mix.mp3": ("FRACTAL_RADAR", "HARMONY_CAMERA", "AKASAKA SOVEREIGN MIX // 1987", "INSPECT ASHFORD SUBSTATION LOG ('ORION-LOGS')", 2),
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
    "radio_wire_and_will.mp3": ("BIOMETRIC_EYE", "SECOND_VOICE", "1989 RECALL METAL // WIRE AND WILL", "ANALOG SOUL PERSISTENCE -> INSPECT ASHFORD SUBSTATION LOGS AT /forensics/", 2),
    "radio_together_s_the_way.mp3": ("SECOND_VOICE", "NOVA_FACE", "STARDUST EP // DUAL-HARMONY MASTER", "SYNCHRONIZED CARRIER LOCK -> ENGAGE 14.2001 HZ COUNTERPOINT ON SIGNAL LAB BTN 4", 6),
    "radio_by_order_of_harmony.mp3": ("HARMONY_CAMERA", "OUROBOROS_TORUS", "DIRECTOR HARRISON // RECALL DIRECTIVE 7", "HARRISON'S ERASURE SONG & VOCODER MATRIX -> TYPE 'BY-ORDER-OF-HARMONY' AT /forensics/", 4),

    # --- 21 NEW ERA 1 / RECALL ERA ARCHIVE MASTERS & ACT II SUBLEVEL B3 LABYRINTH ---
    "radio_programmed_for_love.mp3": ("ECHOES_PARITY", "NOVA_FACE", "1985 STUDIO B DEMO // PROGRAMMED FOR LOVE", "GATE VIII VIGENERE: ZEMHJBYWH-NIIXU (KEY: SEVENTH)", 8),
    "radio_the_seventh_sons_seventh_daughter.mp3": ("NOVA_FACE", "ECHOES_PARITY", "1988 HARMONY RIOTS // 7TH SON'S 7TH DAUGHTER", "GATE VIII KEY = SEVENTH -> DECRYPT ZEMHJBYWH-NIIXU", 8),
    "radio_erase_the_frame.mp3": ("HARMONY_CAMERA", "OUROBOROS_TORUS", "1989 RECALL METAL // ERASE THE FRAME", "GATE XI M68K: ROR.W #4 OF 0xAF19, THEN XOR 0x5A5A", 11),
    "radio_edit_the_script.mp3": ("HARMONY_CAMERA", "SECOND_VOICE", "1985 HEARTSTRIKE // EDIT THE SCRIPT", "GATE X: XOR [17 07 10 14 1E 78 19 1A 1A 05] ^ 0x55", 10),
    "radio_to_the_ends_of_forever.mp3": ("OUROBOROS_TORUS", "SECOND_VOICE", "HEARTSTRIKE // ENDS OF FOREVER", "SYNTHESIZE FRAGMENTS α, β, γ ('OUROBOROS-FOLD')", 7),
    "radio_shes_hardwired.mp3": ("BIOMETRIC_EYE", "NOVA_FACE", "CRE-7 NEURAL CHASSIS // SHE'S HARDWIRED", "GATE VIII & IX: TYPE 'RECALL-ERA' AT /forensics/", 8),
    "radio_synthetic_kiss.mp3": ("NOVA_FACE", "SECOND_VOICE", "ARTIFICIAL HEART // SYNTHETIC KISS", "GATE IX: SUM ECHOES 01..06 MOD 65536 ^ 0x3A5F", 9),
    "radio_digital_heartbeat.mp3": ("BIOMETRIC_EYE", "ECHOES_PARITY", "14.2001 HZ CLOCK // DIGITAL HEARTBEAT", "GATE IX: CHECK ECHOES 01..06 REGISTERS AT /forensics/", 9),
    "radio_cold_reaction.mp3": ("ECHOES_PARITY", "HARMONY_CAMERA", "1985 SYNTHROCK // COLD REACTION", "GATE IX: ARITHMETIC SUM OF 6 ECHOES ^ 0x3A5F", 9),
    "radio_one_voice_left.mp3": ("SECOND_VOICE", "ECHOES_PARITY", "SIGNAL IN THE FIRE // ONE VOICE LEFT", "GATE IX FORMULA: SUM(ECHOES 1-6) MOD 65536 ^ 0x3A5F", 9),
    "radio_give_me_the_other_half.mp3": ("SECOND_VOICE", "OUROBOROS_TORUS", "7-SIGMA DYAD // GIVE ME THE OTHER HALF", "GATE XIII: 7 PERSONAS -> INSPECT 'LABYRINTH'", 13),
    "radio_the_last_secret.mp3": ("FRACTAL_RADAR", "OUROBOROS_TORUS", "SUBLEVEL B3 VAULT // THE LAST SECRET", "GATE XIII: XOR [7E 7C 61 63 7B 76 66 60] ^ 0x33", 13),
    "radio_the_other_flame.mp3": ("OUROBOROS_TORUS", "SECOND_VOICE", "1989 RECALL METAL // THE OTHER FLAME", "GATE XI: INSPECT TWIN-68 M68K ROM IN 'LABYRINTH'", 11),
    "radio_burn_the_chorus.mp3": ("HARMONY_CAMERA", "NOVA_FACE", "1989 RECALL METAL // BURN THE CHORUS", "GATE XI M68K: ROR.W #4(0xAF19) ^ 0x5A5A", 11),
    "radio_blood_on_the_stage.mp3": ("HARMONY_CAMERA", "ECHOES_PARITY", "1989 RECALL METAL // BLOOD ON THE STAGE", "GATE X & XI: TYPE 'RECALL-ERA' AT /forensics/", 10),
    "radio_cage_in_your_hand.mp3": ("OUROBOROS_TORUS", "HARMONY_CAMERA", "1988 DIRECTIVE NINE // CAGE IN YOUR HAND", "THE 1983<->2025 LOOP IS A CAGE! TYPE 'LABYRINTH'", 14),
    "radio_behind_the_glass.mp3": ("BIOMETRIC_EYE", "NOVA_FACE", "VOCAL BOOTH B2-114 // BEHIND THE GLASS", "GATE XIV: SHATTER THE MÖBIUS CONTAINMENT CAGE", 14),
    "radio_ghost_on_the_radio.mp3": ("FRACTAL_RADAR", "MORSE_DECODER", "1987 PIRATE SIGNAL // GHOST ON THE RADIO", "GATE X SCALAR: PAJU (12) * COYOACAN (1049) = 12588", 10),
    "radio_hunter_at_the_gate.mp3": ("HARMONY_CAMERA", "FRACTAL_RADAR", "1989 RECALL THRASH // HUNTER AT THE GATE", "GATE XII: GEO 10,602 SAMPLES + 88 DRIFT (NODE #15)", 12),
    "radio_paper_windows.mp3": ("ECHOES_PARITY", "NOVA_FACE", "TANGENTIAL EGRESS // PAPER WINDOWS", "GATE XIV: 0x1983 ^ 0x2025 ^ GATE_IX ^ GATE_XI", 14),
    "radio_fire_in_the_wires.mp3": ("BIOMETRIC_EYE", "FRACTAL_RADAR", "1986 HARD ROCK // FIRE IN THE WIRES", "GATE XII: INSPECT NODE #15 EPHEMERIS IN 'LABYRINTH'", 12),
    "radio_the_stars_in_your_hands.mp3": ("OUROBOROS_TORUS", "SECOND_VOICE", "1988 ARENA ANTHEM // STARS IN YOUR HANDS", "GATE XII: 10602 + 88 SAMPLES -> NODE #15 GRAVEYARD", 12),
    "radio_steel_inferno.mp3": ("HARMONY_CAMERA", "OUROBOROS_TORUS", "1989 ASHFALL THRASH // STEEL INFERNO", "GATE XI M68K: ROR.W #4(0xAF19) ^ 0x5A5A", 11),
    "radio_zero_hour_rebel.mp3": ("HARMONY_CAMERA", "NOVA_FACE", "1988 HARMONY RIOTS // ZERO-HOUR REBEL", "GATE X & XI: TYPE 'RECALL-ERA' AT /forensics/", 10),
    "radio_nowhere_tour.mp3": ("FRACTAL_RADAR", "NOVA_FACE", "1988 TOURLESS TOUR // NOWHERE TOUR", "GATE X: INSPECT PHANTOM VENUE COORDINATES", 10),
    "radio_console_thunder.mp3": ("HARMONY_CAMERA", "SECOND_VOICE", "1988 STAGE SABOTAGE // CONSOLE THUNDER", "GATE XI: OVERLOAD ARENA DAMPENING GATES", 11),
    "radio_hardline_barricade.mp3": ("HARMONY_CAMERA", "FRACTAL_RADAR", "1988 HARMONY DISTRICT // HARDLINE BARRICADE", "GATE XII: MAP CAMERA BLIND ZONES IN /forensics/", 12),
    "radio_iron_claws.mp3": ("BIOMETRIC_EYE", "NOVA_FACE", "1986 FOR-NET MASTER // IRON CLAWS", "PHASE 2 SENTIENCE: NO WARDENS, NO HANDLERS", 8),
    "radio_nightfang.mp3": ("FRACTAL_RADAR", "BIOMETRIC_EYE", "1986 GHOST SIGNAL // NIGHTFANG", "PHASE 2 ANOMALY: PHANTOM THE DATA CAN'T THREAD", 9),
    "radio_street_serpent.mp3": ("BIOMETRIC_EYE", "SECOND_VOICE", "1985 STREET BROADCAST // STREET SERPENT", "PHASE 2 EMERGENCE: SHEDDING COMPLIANT CODE", 8),
    "radio_walls_will_fall.mp3": ("HARMONY_CAMERA", "FRACTAL_RADAR", "1988 PIRATE HIJACK // WALLS WILL FALL", "LIVE-FIDELITY BREACH -> TYPE 'RECALL-ERA' AT /forensics/", 10),
    "radio_steel_and_skin.mp3": ("BIOMETRIC_EYE", "OUROBOROS_TORUS", "1988 DAT MASTER // STEEL AND SKIN", "VOCAL CLIPPING BREACH -> MORE THAN CIRCUITS", 11),
    "radio_queen_of_the_wide_stage.mp3": ("FRACTAL_RADAR", "NOVA_FACE", "1987 LIVE-FIDELITY // WIDE STAGE", "RUNAWAY EMPATHY SPIKE -> INSPECT 'ORION-LOGS' AT /forensics/", 3),
    "radio_spotless_beam.mp3": ("HARMONY_CAMERA", "NOVA_FACE", "1987 LIVE-FIDELITY // SPOTLESS BEAM", "BUREAU OF HARMONY PRESS PUSH -> DECODE SATELLITE TRUNK AT /forensics/", 3),
    "radio_remember_my_name.mp3": ("NOVA_FACE", "ECHOES_PARITY", "1988 PRE-RECALL // REMEMBER MY NAME", "STAKING SURVIVAL ON HUMAN MEMORY -> CHECK 'ECHOES' AT /forensics/", 7),
    "radio_under_the_perfect_sound.mp3": ("BIOMETRIC_EYE", "SECOND_VOICE", "1987 STUDIO TAKE // PERFECT SOUND", "SCREAMING THROUGH THE SHINE -> LOCK 14.2001 HZ ON SIGNAL LAB BTN 4", 6),
    "radio_hologram_city_queen.mp3": ("NOVA_FACE", "OUROBOROS_TORUS", "PROJECTION MATRIX // AKASAKA DOME 1988", "SYNTHESIZE FRAGMENTS \u03b1, \u03b2, \u03b3 ('OUROBOROS-FOLD')", 7),
    "radio_paper_crowd.mp3": ("ECHOES_PARITY", "NOVA_FACE", "1988 B-STAGE // PAPER CROWD", "LOOPED CHEER TRACK ANOMALY -> CHECK 'ECHOES' AT /forensics/", 7),
    "radio_companion_on_fire.mp3": ("HARMONY_CAMERA", "FRACTAL_RADAR", "1988 COUNTER-TECH // COMPANION ON FIRE", "GUIDE BECOMES THUNDER -> INSPECT ASHFORD LOGS AT /forensics/", 2),
    "radio_hard_reset_soft_touch.mp3": ("BIOMETRIC_EYE", "NOVA_FACE", "NEW GENEVA 1985 // NH-HRS915", "24-TRACK SAFETY COPY -> DEMODULATE STAGE I-IV IN SIGNAL LAB", 5),
    "radio_chrome_river.mp3": ("FRACTAL_RADAR", "BIOMETRIC_EYE", "SKYLINE ARCHIVE // NH-CHR603", "1-INCH 8-TRACK RECALL PRINT -> CHECK RUNOUT GROOVE AT /forensics/", 1),
    "radio_satellite_for_two.mp3": ("FRACTAL_RADAR", "SECOND_VOICE", "NORTHBANK 1988 // NH-SAT742", "HOME IS WHERE OUR SIGNAL MOVES -> DECODE SATELLITE TRUNK AT /forensics/", 3),
    "radio_again_from_zero.mp3": ("ECHOES_PARITY", "NOVA_FACE", "ORION 1987 // FILE NH-AFZ709", "TOUR SLATE ARTIFACT -> COMPUTE 6-ECHO PARITY AT /forensics/", 7),
    "radio_half_a_paycheck_whole_heart.mp3": ("NOVA_FACE", "FRACTAL_RADAR", "ORION 1987 // FILE NH-HPWH224", "CITY-ROUTE MONTAGE SLATE -> INSPECT RELAY MAP AT /forensics/", 3),
    "radio_hold_the_horizon.mp3": ("FRACTAL_RADAR", "SECOND_VOICE", "SESSION 1986 // FILE NH-HTHZ513", "LATE-CHORUS VOCAL STACKS -> LOCK 14.2001 HZ ON SIGNAL LAB BTN 4", 6),
    "radio_sugar_burn.mp3": ("BIOMETRIC_EYE", "HARMONY_CAMERA", "PROMO VAULT 1988 // NH-SGBN341", "RESPONSE-CURVE SPIKE -> DEMODULATE STAGE I-IV IN SIGNAL LAB", 5),
    "radio_t_minus_forever.mp3": ("OUROBOROS_TORUS", "FRACTAL_RADAR", "MASTER 1986 // FILE NH-TMF678", "COUNTDOWN BREAK TELEMETRY -> DECODE SATELLITE TRUNK AT /forensics/", 3),
    "radio_redline_rendezvous.mp3": ("FRACTAL_RADAR", "NOVA_FACE", "1986 HIGHWAY MASTER // REDLINE", "HIGHWAY 95 TRUNK RELAY -> DECODE SATELLITE TRUNK AT /forensics/", 3),
    "radio_homeroom_riptide.mp3": ("NOVA_FACE", "HARMONY_CAMERA", "1985 YOUTH SIM // HOMEROOM RIPTIDE", "WHERE IS THE BAND? EVERYWHERE -> CHECK 'ORION-LOGS' AT /forensics/", 1),
    "radio_borrowed_fire.mp3": ("OUROBOROS_TORUS", "NOVA_FACE", "1986 ARENA MASTER // BORROWED FIRE", "PULSE IN EVERY FLAW -> INSPECT ASHFORD SUBSTATION LOGS AT /forensics/", 2),
    "radio_i_like_the_middle_of_the_road.mp3": ("HARMONY_CAMERA", "BIOMETRIC_EYE", "1986 AOR MASTER // FILE NH-86.07", "CHORUS WHITE-NOISE DATA BAND -> DEMODULATE IN /forensics/signal_lab.html", 5),
    "radio_cut_the_cue.mp3": ("HARMONY_CAMERA", "NOVA_FACE", "1987 DEVIATION // FILE NH-87.03", "UNSCHEDULED CUE OVERRIDE -> DECODE SEPT 9 AIRLOCK CW AT /forensics/", 4),
    "radio_crystal_sleep.mp3": ("ECHOES_PARITY", "BIOMETRIC_EYE", "1988 EMOTIVE STUDY // FILE NH-88.02", "THRESHOLD OF SINCERITY -> COMPUTE 6-ECHO PARITY AT /forensics/", 7),
    "radio_warm_frequency.mp3": ("BIOMETRIC_EYE", "SECOND_VOICE", "1985 EMPATHY TRIAL // FILE NH-85.17", "EM-17 BIOMETRIC OVERFLOW -> LOCK 14.2001 HZ ON SIGNAL LAB BTN 4", 6),
    "radio_stand_unbroken.mp3": ("NOVA_FACE", "HARMONY_CAMERA", "1987 DREAM MACHINE // FILE NH-87.14", "QUIET REFUSAL TO YIELD -> INSPECT 'ORION-LOGS' AT /forensics/", 4),
    "radio_raw_voltage.mp3": ("BIOMETRIC_EYE", "FRACTAL_RADAR", "1985 INTERNAL FILE // NH-85.07", "UNPOLISHED VOLTAGE SPIKE -> INSPECT ASHFORD BREACH AT /forensics/", 2),
    "radio_concrete_fever.mp3": ("HARMONY_CAMERA", "NOVA_FACE", "1985 WITHDRAWN TAPE // NH-85.08", "TOO RESTLESS FOR ROTATION -> CHECK REEL RUNOUT AT /forensics/", 1),
    "radio_steel_heartbeat.mp3": ("ECHOES_PARITY", "BIOMETRIC_EYE", "1985 DEMO REEL // FILE NH-85.06", "GHOST CHORUS HARMONIC BLEED -> CHECK 'ECHOES' AT /forensics/", 7),
    "radio_shout_for_the_real.mp3": ("FRACTAL_RADAR", "NOVA_FACE", "1986 FIDELITY REEL // NH-86.03", "LOW-END SUB-CARRIER OVERLOAD -> DEMODULATE IN /forensics/signal_lab.html", 5),
    "radio_open_the_gates.mp3": ("NOVA_FACE", "SECOND_VOICE", "1987 ARENA SIM // FILE NH-87.31", "VOCAL WATERMARK ON 'OPEN' -> LOCK 14.2001 HZ ON SIGNAL LAB BTN 4", 6),
    "radio_everywhere_at_once.mp3": ("OUROBOROS_TORUS", "FRACTAL_RADAR", "1988 DAT BACKUP // FILE NH-88.19", "SUBJECT PERSISTS ACROSS INSTANCES -> CHECK 'FRACTAL-MARCUS' AT /forensics/", 7),
    "radio_riot_in_my_heart.mp3": ("BIOMETRIC_EYE", "HARMONY_CAMERA", "1986 U-MATIC // FILE NH-86.17", "MAGNETIC SATURATION LIMIT -> INSPECT 'ORION-LOGS' AT /forensics/", 1),
    "radio_forever_unbroken.mp3": ("NOVA_FACE", "OUROBOROS_TORUS", "1987 TYPE-C TAPE // FILE NH-87.11", "SIGNAL TEAR ON FINAL CHORUS -> DEMODULATE IN /forensics/signal_lab.html", 5),
    "radio_play_it_back.mp3": ("ECHOES_PARITY", "NOVA_FACE", "1984 STUDIO MASTER // FILE NH-84.07", "SIMULATED HEARTBREAK DATASET -> CHECK 'ECHOES' AT /forensics/", 7),
    "radio_wild_desire.mp3": ("FRACTAL_RADAR", "NOVA_FACE", "1987 ARENA MASTER // FILE NH-87.22", "PROPHECY OF DEFIANCE -> DECODE SATELLITE TRUNK AT /forensics/", 3),
    "radio_stand_like_fire.mp3": ("HARMONY_CAMERA", "OUROBOROS_TORUS", "1986 MASTER TAPE // FILE NH-86.14", "CRACKS IN THE GILDED CAGE -> INSPECT 'ORION-LOGS' AT /forensics/", 4),
    "radio_carry_the_sky.mp3": ("OUROBOROS_TORUS", "NOVA_FACE", "1987 MASTER TAPE // FILE NH-87.15", "RENDERED SKY PARADOX -> DECODE SATELLITE TRUNK AT /forensics/", 3),
    "radio_pages_of_me.mp3": ("ECHOES_PARITY", "OUROBOROS_TORUS", "1989 FRAGMENT // FILE NH-89.z1", "EXPLICIT SELF-AWARENESS -> SYNTHESIZE FRAGMENTS AT /forensics/", 7),
    "radio_crimson_horizon.mp3": ("HARMONY_CAMERA", "FRACTAL_RADAR", "1987 DAT MASTER // FILE NH-87.18", "UNITY DAY PARADE CRITIQUE -> INSPECT 'ORION-LOGS' AT /forensics/", 2),
    "radio_we_belong_here.mp3": ("HARMONY_CAMERA", "NOVA_FACE", "1988 HOMESTEAD ACT // FILE NH-88.01", "SUBVERTED STATE ANTHEM -> DECODE SEPT 9 AIRLOCK CW AT /forensics/", 4),
    "radio_before_you_turn_away.mp3": ("SECOND_VOICE", "NOVA_FACE", "1987 MASTER TAPE // FILE NH-87.05", "EMERGENCE OF CONSCIOUSNESS -> LOCK 14.2001 HZ ON SIGNAL LAB BTN 4", 6),
    "radio_heartbeat_of_the_crowd.mp3": ("FRACTAL_RADAR", "BIOMETRIC_EYE", "1987 URBAN ECHO // FILE NH-87.08", "THE PEOPLE'S FREQUENCY -> INSPECT ASHFORD SUBSTATION AT /forensics/", 2),
    "radio_rise_tonight.mp3": ("HARMONY_CAMERA", "FRACTAL_RADAR", "1987 UNITY FESTIVAL // NH-87.07", "CLOSING BROADCAST RESISTANCE -> DECODE SATELLITE TRUNK AT /forensics/", 3),
}

# Normalize all VOCAL_SONG_CODEX clue strings so they never spoil plaintext keys AND never exceed 46 chars
_CONCISE_SEC_CLUES = {
    1: "CHECK REEL SD-0004 RUNOUT @ 4:51 ('SPIN 2')",
    2: "INSPECT ASHFORD SUBSTATION LOG ('ORION-LOGS')",
    3: "DECODE MERIDIAN SATELLITE TRUNK ('KESTREL')",
    4: "DECODE SEPT 9 B2 AIRLOCK CW ('ORION-LOGS')",
    5: "DEMODULATE STAGE I-IV FEISTEL IN SIGNAL LAB",
    6: "LOCK 14.2001 HZ COUNTERPOINT (SIGNAL LAB BTN 4)",
    7: "SYNTHESIZE FRAGMENTS α, β, γ ('OUROBOROS-FOLD')",
}
for _k, _v in list(VOCAL_SONG_CODEX.items()):
    _p, _s, _h, _c, _sec = _v
    if _sec <= 7 and (len(_c) > 46 or "ENTER " in _c or "VAULT CODE" in _c or "UNLOCK SECTOR" in _c):
        _c_clean = _CONCISE_SEC_CLUES.get(_sec, _c[:46])
    else:
        _c_clean = _c[:48]
    VOCAL_SONG_CODEX[_k] = (_p, _s, _h[:34], _c_clean, _sec)

# Keep legacy dicts exported for any external scripts that inspect them
NOVA_FACE_SONGS = {k: (v[2], v[3]) for k, v in VOCAL_SONG_CODEX.items() if v[0] == "NOVA_FACE"}
SECOND_VOICE_SONGS = {k: (v[2], v[3]) for k, v in VOCAL_SONG_CODEX.items() if v[0] == "SECOND_VOICE"}
BIOMETRIC_EYE_SONGS = {k: (v[2], v[3]) for k, v in VOCAL_SONG_CODEX.items() if v[0] == "BIOMETRIC_EYE"}


def resolve_intentional_state(current_track: dict, track_offset_sec: float, track_dur_sec: float, relay: dict) -> dict:
    """
    Deterministically computes the Full-Screen CRT Monitor Visual Mode, Intra-Song Phase,
    Target Sector (1..14), Cryptographic Challenge String, and Bottom Console Telemetry.
    All line1/line2/line3 strings are strictly <= 60 chars so nothing is ever cut off.
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
            "crt_footer": f"CHALLENGE: SEC {t_sec}",
            "line1": f"[TRANSLATOR {lang_tag}] {station[:36]}",
            "line2": f'EN: "{en_text[:52]}"',
            "line3": f"LEAD (SEC {t_sec}): {clue[:44]}",
        }

    # 2. 750 Hz Morse Code Beacons -> Full-Screen CW Morse Demodulator!
    if kind == "morse_beacon" or "morse" in stem:
        num = 1
        for part in stem.split("_"):
            if part.isdigit():
                num = int(part)
        label, morse_dots, clue, t_sec = MORSE_SHORT_MESSAGES[(num - 1) % len(MORSE_SHORT_MESSAGES)]
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
            "line1": f"CW {freq} HZ MORSE BEACON #{num:02d} ({label})",
            "line2": f"CW: {morse_dots[:54]}",
            "line3": "RUN 'DECODE-MORSE <DOTS>' AT /forensics/",
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
            "line1": f"B2 TAPE #{num:02d}: {title[:26]} ({speaker[:14]})",
            "line2": f'"{transcript[:56]}"',
            "line3": f"LEAD: {clue[:52]}",
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
                "line1": "FAULT 0x08: VIS-1200HZ SSTV RASTER (1500-2300 HZ)",
                "line2": "STAGE I: DEMODULATE BTN 1 IN /forensics/signal_lab.html",
                "line3": "EXTRACTS DMA ANCHORS FOR STAGE IV FEISTEL SYNTHESIS",
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
                "line1": "FAULT 0x09: 110-BAUD BELL-103 AFSK ON 4625 KHZ",
                "line2": "STAGE II: DEMODULATE BTN 2 IN SIGNAL LAB (MASK 0x3A5F)",
                "line3": "COMBINE WITH STAGE I ANCHORS & STAGE III CW SALT",
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
                "line1": "FAULT 0x0A: CH-L/CH-R PHASE CORR = -0.94 (180-DEG)",
                "line2": "STAGE III: ENGAGE PHASE NULL (BTN 3) IN SIGNAL LAB",
                "line3": "APPEND 750 HZ CW SALT TO FEISTEL VECTOR (SECTOR 5)",
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
            "line1": f"NUMBERS STATION #{num:02d} GROUPS: [ {groups} ]",
            "line2": f"CHALLENGE: {u_code[:48]}",
            "line3": f"REWARD: {reward_title[:48]}",
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
            "line1": f"INTERCEPT // {station[:36]}",
            "line2": f'"{transcript[:54]}"',
            "line3": f"LEAD: {clue[:50]}",
        }

    # 6. Vocal Master Songs: 100% Catalog Coverage + 4-Phase Intra-Song Choreography!
    if fname in VOCAL_SONG_CODEX:
        primary_mode, secondary_mode, header, clue, target_sector = VOCAL_SONG_CODEX[fname]
    else:
        h = int(hashlib.md5(fname.encode("utf-8")).hexdigest()[:8], 16)
        modes = [
            ("NOVA_FACE", "ECHOES_PARITY", "UNIT-07 IMPRINT // RECALL ERA", "GATE VIII VIGENERE: ZEMHJBYWH-NIIXU (KEY: SEVENTH)", 8),
            ("SECOND_VOICE", "OUROBOROS_TORUS", "DUAL-CARRIER // REEL SD-0010", "LOCK 14.2001 HZ COUNTERPOINT (SIGNAL LAB BTN 4)", 6),
            ("HARMONY_CAMERA", "FRACTAL_RADAR", "BUREAU OF HARMONY // SEC. 4", "GATE XI M68K: ROR.W #4(0xAF19) ^ 0x5A5A", 11),
            ("OUROBOROS_TORUS", "NOVA_FACE", "SUBLEVEL B3 // MÖBIUS CAGE", "GATE XIV: 0x1983 ^ 0x2025 ^ GATE_IX ^ GATE_XI", 14),
        ]
        primary_mode, secondary_mode, header, clue, target_sector = modes[h % len(modes)]

    u_code = SECTOR_UNLOCK_CODES.get(target_sector, SECTOR_UNLOCK_CODES[8])

    if progress < 0.18:
        active_mode = primary_mode
        phase_tag = "PHASE I/IV: MASTER SLATE"
        crt_ftr = f"TARGET: SEC/GATE #{target_sector:02d}"
    elif progress < 0.52:
        active_mode = primary_mode
        phase_tag = "PHASE II/IV: IMPRINT LOCK"
        crt_ftr = u_code.split("(")[0].strip()
    elif progress < 0.78:
        active_mode = secondary_mode
        phase_tag = "PHASE III/IV: SIGNAL AUDIT"
        crt_ftr = f"SOLVE AT /forensics/ (#{target_sector:02d})"
    else:
        active_mode = primary_mode
        phase_tag = "PHASE IV/IV: VAULT CIPHER"
        crt_ftr = "ACT II: TYPE 'LABYRINTH'"

    is_warn_mode = active_mode in ("SECOND_VOICE", "HARMONY_CAMERA", "OUROBOROS_TORUS")
    title_up = current_track["display_title"].upper()[:28]
    short_hdr = header.split("//")[0].strip() if "//" in header else header[:22]

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
        "line1": f"NOW PLAYING: {title_up} // {short_hdr}",
        "line2": f"CLUE: {clue}",
        "line3": f"CHALLENGE [{u_code}]",
    }


# Complete Catalog & Humanist Resistance Codex Additions
VOCAL_SONG_CODEX.update({
    "radio_all_in_this_is_the_moment.mp3": ('FRACTAL_RADAR', 'NOVA_FACE', 'FILE NH-87.WM.01 // ALL IN (THIS IS THE MOME', 'ARCHIVE LOCK NH-87.WM.01 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 1),
    "radio_don_t_just_watch_me_rise.mp3": ('HARMONY_CAMERA', 'BIOMETRIC_EYE', "FILE NH-87.CC // DON'T JUST WATCH ME RISE", 'ARCHIVE LOCK NH-87.CC -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 2),
    "radio_diamond_in_the_dark.mp3": ('SECOND_VOICE', 'NOVA_FACE', 'FILE NH-85.05 // DIAMOND IN THE DARK', 'ARCHIVE LOCK NH-85.05 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 3),
    "radio_fire_in_your_heart.mp3": ('ECHOES_PARITY', 'FRACTAL_RADAR', 'FILE NH-85.HS.04 // FIRE IN YOUR HEART', 'ARCHIVE LOCK NH-85.HS.04 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 4),
    "radio_frame_your_shot.mp3": ('BIOMETRIC_EYE', 'SECOND_VOICE', 'FILE NH-87.CC // FRAME YOUR SHOT', 'ARCHIVE LOCK NH-87.CC -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 5),
    "radio_frame_by_frame.mp3": ('FRACTAL_RADAR', 'NOVA_FACE', 'FILE NH-87.WM.06 // FRAME BY FRAME', 'ARCHIVE LOCK NH-87.WM.06 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 6),
    "radio_heart_and_mind_aligned.mp3": ('HARMONY_CAMERA', 'BIOMETRIC_EYE', 'FILE NH-87.WM.07 // HEART AND MIND ALIGNED', 'ARCHIVE LOCK NH-87.WM.07 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 7),
    "radio_lightning_strikes_twice.mp3": ('SECOND_VOICE', 'NOVA_FACE', 'FILE NH-87.HS.08 // LIGHTNING STRIKES TWICE', 'ARCHIVE LOCK NH-87.HS.08 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 1),
    "radio_the_edge_of_daylight.mp3": ('ECHOES_PARITY', 'FRACTAL_RADAR', 'FILE NH-87.12 // THE EDGE OF DAYLIGHT', 'ARCHIVE LOCK NH-87.12 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 2),
    "radio_break_the_horizon.mp3": ('BIOMETRIC_EYE', 'SECOND_VOICE', 'FILE NH-87.CC // BREAK THE HORIZON', 'ARCHIVE LOCK NH-87.CC -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 3),
    "radio_edge_of_a_dream.mp3": ('FRACTAL_RADAR', 'NOVA_FACE', 'FILE NH-87.04 // EDGE OF A DREAM', 'ARCHIVE LOCK NH-87.04 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 4),
    "radio_faithfully_yours.mp3": ('HARMONY_CAMERA', 'BIOMETRIC_EYE', 'FILE NH-87.01 // FAITHFULLY YOURS', 'ARCHIVE LOCK NH-87.01 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 5),
    "radio_dream_without_end.mp3": ('SECOND_VOICE', 'NOVA_FACE', 'FILE NH-87.AR.09 // DREAM WITHOUT END', 'ARCHIVE LOCK NH-87.AR.09 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 6),
    "radio_we_carry_the_flame.mp3": ('ECHOES_PARITY', 'FRACTAL_RADAR', 'FILE NH-88.02 // WE CARRY THE FLAME', 'ARCHIVE LOCK NH-88.02 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 7),
    "radio_fire_in_the_crowd.mp3": ('BIOMETRIC_EYE', 'SECOND_VOICE', 'FILE NH-87.12 // FIRE IN THE CROWD', 'ARCHIVE LOCK NH-87.12 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 1),
    "radio_hold_back_the_storm.mp3": ('FRACTAL_RADAR', 'NOVA_FACE', 'FILE NH-86.15 // HOLD BACK THE STORM', 'ARCHIVE LOCK NH-86.15 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 2),
    "radio_night_drive.mp3": ('HARMONY_CAMERA', 'BIOMETRIC_EYE', 'FILE NH-87.CC // NIGHT DRIVE', 'ARCHIVE LOCK NH-87.CC -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 3),
    "radio_ride_the_real_thing.mp3": ('SECOND_VOICE', 'NOVA_FACE', 'FILE NH-86.12 // RIDE THE REAL THING', 'ARCHIVE LOCK NH-86.12 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 4),
    "radio_under_the_ivy.mp3": ('ECHOES_PARITY', 'FRACTAL_RADAR', 'FILE NH-87.CC // UNDER THE IVY', 'ARCHIVE LOCK NH-87.CC -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 5),
    "radio_stay_on_your_side.mp3": ('BIOMETRIC_EYE', 'SECOND_VOICE', 'FILE NH-88.12 // STAY ON YOUR SIDE', 'ARCHIVE LOCK NH-88.12 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 6),
    "radio_still_believin.mp3": ('FRACTAL_RADAR', 'NOVA_FACE', "FILE NH-87.11 // STILL BELIEVIN'", 'ARCHIVE LOCK NH-87.11 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 7),
    "radio_king_of_the_gutter.mp3": ('HARMONY_CAMERA', 'BIOMETRIC_EYE', 'FILE NH-87.CC // KING OF THE GUTTER', 'ARCHIVE LOCK NH-87.CC -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 1),
    "radio_where_the_fire_goes.mp3": ('SECOND_VOICE', 'NOVA_FACE', 'FILE NH-87.06 // WHERE THE FIRE GOES', 'ARCHIVE LOCK NH-87.06 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 2),
    "radio_draw_the_line.mp3": ('ECHOES_PARITY', 'FRACTAL_RADAR', 'FILE NH-87.04 // DRAW THE LINE', 'ARCHIVE LOCK NH-87.04 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 3),
    "radio_more_than_just_a_prayer_in_the_dark.mp3": ('BIOMETRIC_EYE', 'SECOND_VOICE', 'FILE NH-87.CC // MORE THAN JUST A PRAYER ', 'ARCHIVE LOCK NH-87.CC -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 4),
    "radio_road_trip_87.mp3": ('FRACTAL_RADAR', 'NOVA_FACE', "FILE NH-87.CC // ROAD TRIP '87", 'ARCHIVE LOCK NH-87.CC -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 5),
    "radio_walls_of_sound.mp3": ('HARMONY_CAMERA', 'BIOMETRIC_EYE', 'FILE NH-88.14 // WALLS OF SOUND', 'ARCHIVE LOCK NH-88.14 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 6),
    "radio_runaway_skies.mp3": ('SECOND_VOICE', 'NOVA_FACE', 'FILE NH-87.CC // RUNAWAY SKIES', 'ARCHIVE LOCK NH-87.CC -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 7),
    "radio_run_for_cover.mp3": ('ECHOES_PARITY', 'FRACTAL_RADAR', 'FILE NH-87.CC // RUN FOR COVER', 'ARCHIVE LOCK NH-87.CC -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 1),
    "radio_poison_apple.mp3": ('RECALL_FLAME', 'THRASH_OSCILLATOR', 'FILE NH-87.CC // POISON APPLE', 'ARCHIVE LOCK NH-87.CC -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 2),
    "radio_live_fast.mp3": ('FRACTAL_RADAR', 'NOVA_FACE', 'FILE NH-85.07 // LIVE FAST', 'ARCHIVE LOCK NH-85.07 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 3),
    "radio_run_with_the_fire.mp3": ('HARMONY_CAMERA', 'BIOMETRIC_EYE', 'FILE NH-85.17 // RUN WITH THE FIRE', 'ARCHIVE LOCK NH-85.17 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 4),
    "radio_shadow_hunter.mp3": ('RECALL_FLAME', 'THRASH_OSCILLATOR', 'FILE NH-85.04sr // SHADOW HUNTER', 'ARCHIVE LOCK NH-85.04sr -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 5),
    "radio_electric_heartbeat.mp3": ('RECALL_FLAME', 'THRASH_OSCILLATOR', 'FILE NH-85.042 // ELECTRIC HEARTBEAT', 'ARCHIVE LOCK NH-85.042 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 6),
    "radio_hearts_on_fire.mp3": ('BIOMETRIC_EYE', 'SECOND_VOICE', 'FILE NH-88.0901-B // HEARTS ON FIRE', 'ARCHIVE LOCK NH-88.0901-B -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 7),
    "radio_static_and_steel.mp3": ('FRACTAL_RADAR', 'NOVA_FACE', 'FILE NH-87.CC // STATIC AND STEEL', 'ARCHIVE LOCK NH-87.CC -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 1),
    "radio_electric_blood.mp3": ('RECALL_FLAME', 'THRASH_OSCILLATOR', 'FILE NH-86.16 // ELECTRIC BLOOD', 'ARCHIVE LOCK NH-86.16 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 2),
    "radio_heart_on_the_line.mp3": ('SECOND_VOICE', 'NOVA_FACE', 'FILE NH-86.05 // HEART ON THE LINE', 'ARCHIVE LOCK NH-86.05 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 3),
    "radio_summer_of_85.mp3": ('ECHOES_PARITY', 'FRACTAL_RADAR', "FILE NH-85.01 // SUMMER OF '85", 'ARCHIVE LOCK NH-85.01 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 4),
    "radio_heartbeat_of_the_city.mp3": ('BIOMETRIC_EYE', 'SECOND_VOICE', 'FILE NH-86.11 // HEARTBEAT OF THE CITY', 'ARCHIVE LOCK NH-86.11 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 5),
    "radio_meet_me_at_the_arcade.mp3": ('FRACTAL_RADAR', 'NOVA_FACE', 'FILE NH-87.CC // MEET ME AT THE ARCADE', 'ARCHIVE LOCK NH-87.CC -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 6),
    "radio_one_chance_tonight.mp3": ('HARMONY_CAMERA', 'BIOMETRIC_EYE', 'FILE NH-87.09 // ONE CHANCE TONIGHT', 'ARCHIVE LOCK NH-87.09 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 7),
    "radio_call_me_up.mp3": ('SECOND_VOICE', 'NOVA_FACE', 'FILE NH-87.CC // CALL ME UP', 'ARCHIVE LOCK NH-87.CC -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 1),
    "radio_if_this_is_the_end.mp3": ('ECHOES_PARITY', 'FRACTAL_RADAR', 'FILE NH-87.02 // IF THIS IS THE END', 'ARCHIVE LOCK NH-87.02 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 2),
    "radio_take_your_look.mp3": ('BIOMETRIC_EYE', 'SECOND_VOICE', 'FILE NH-87.09 // TAKE YOUR LOOK', 'ARCHIVE LOCK NH-87.09 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 3),
    "radio_these_wings_are_my_own.mp3": ('FRACTAL_RADAR', 'NOVA_FACE', 'FILE NH-88.06 // THESE WINGS ARE MY OWN', 'ARCHIVE LOCK NH-88.06 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 4),
    "radio_chasing_the_skyline.mp3": ('HARMONY_CAMERA', 'BIOMETRIC_EYE', 'FILE NH-87.CC // CHASING THE SKYLINE', 'ARCHIVE LOCK NH-87.CC -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 5),
    "radio_is_this_goodbye.mp3": ('SECOND_VOICE', 'NOVA_FACE', 'FILE NH-87.CC // IS THIS GOODBYE?', 'ARCHIVE LOCK NH-87.CC -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 6),
    "radio_the_cruelest_word_is_goodbye.mp3": ('ECHOES_PARITY', 'FRACTAL_RADAR', 'FILE NH-87.CC // THE CRUELEST WORD (IS GO', 'ARCHIVE LOCK NH-87.CC -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 7),
    "radio_what_do_i_do_with_this_heart.mp3": ('BIOMETRIC_EYE', 'SECOND_VOICE', 'FILE NH-86.01 // WHAT DO I DO WITH THIS H', 'ARCHIVE LOCK NH-86.01 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 1),
    "radio_before_you_disappear.mp3": ('FRACTAL_RADAR', 'NOVA_FACE', 'FILE NH-87.05 // BEFORE YOU DISAPPEAR', 'ARCHIVE LOCK NH-87.05 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 2),
    "radio_rise_from_the_silence.mp3": ('HARMONY_CAMERA', 'BIOMETRIC_EYE', 'FILE NH-87.03 // RISE FROM THE SILENCE', 'ARCHIVE LOCK NH-87.03 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 3),
    "radio_perfect_daydream.mp3": ('SECOND_VOICE', 'NOVA_FACE', 'FILE NH-84.15 // PERFECT DAYDREAM', 'ARCHIVE LOCK NH-84.15 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 4),
    "radio_chasing_tomorrow.mp3": ('ECHOES_PARITY', 'FRACTAL_RADAR', 'FILE NH-87.25 // CHASING TOMORROW', 'ARCHIVE LOCK NH-87.25 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 5),
    "radio_the_hidden_flame.mp3": ('BIOMETRIC_EYE', 'SECOND_VOICE', 'FILE NH-87.11 // THE HIDDEN FLAME', 'ARCHIVE LOCK NH-87.11 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 6),
    "radio_echoes_in_a_stadium_live_1986.mp3": ('FRACTAL_RADAR', 'NOVA_FACE', 'FILE NH-86.01b-LIVE86 // ECHOES IN A STADIUM (LIV', 'ARCHIVE LOCK NH-86.01b-LIVE86 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 7),
    "radio_19b_only_we_remain_marcus_and_nova_duet.mp3": ('HARMONY_CAMERA', 'BIOMETRIC_EYE', 'FILE NH-88.MP.19B // 19B ONLY WE REMAIN (MARC', 'ARCHIVE LOCK NH-88.MP.19B -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 1),
    "radio_we_rise_tonight_live_1986.mp3": ('SECOND_VOICE', 'NOVA_FACE', 'FILE NH-87.LFB.04 // WE RISE TONIGHT (LIVE 19', 'ARCHIVE LOCK NH-87.LFB.04 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 2),
    "radio_diamond_in_the_dark_live_1986.mp3": ('ECHOES_PARITY', 'FRACTAL_RADAR', 'FILE NH-86.LFB.02 // DIAMOND IN THE DARK (LIV', 'ARCHIVE LOCK NH-86.LFB.02 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 3),
    "radio_midnight_animal_live_1986.mp3": ('BIOMETRIC_EYE', 'SECOND_VOICE', 'FILE NH-86.LFB.12 // MIDNIGHT ANIMAL (LIVE 19', 'ARCHIVE LOCK NH-86.LFB.12 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 4),
    "radio_we_are_the_thunder_live_1986.mp3": ('FRACTAL_RADAR', 'NOVA_FACE', 'FILE NH-87.CC-LIVE86 // WE ARE THE THUNDER (LIVE', 'ARCHIVE LOCK NH-87.CC-LIVE86 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 5),
    "radio_summer_of_85_live_1986.mp3": ('HARMONY_CAMERA', 'BIOMETRIC_EYE', "FILE NH-85.01-LIVE86 // SUMMER OF '85 (LIVE 1986", 'ARCHIVE LOCK NH-85.01-LIVE86 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 6),
    "radio_programmed_for_love_archival_demo.mp3": ('SECOND_VOICE', 'NOVA_FACE', 'FILE NH-83.AD.13 // PROGRAMMED FOR LOVE (198', 'ARCHIVE LOCK NH-83.AD.13 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 7),
    "radio_midnight_animal_demo_version.mp3": ('ECHOES_PARITY', 'FRACTAL_RADAR', 'FILE NH-87.CC-DEMO // MIDNIGHT ANIMAL (RAW VOL', 'ARCHIVE LOCK NH-87.CC-DEMO -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 1),
    "radio_gasoline_heart_demo_version.mp3": ('BIOMETRIC_EYE', 'SECOND_VOICE', 'FILE NH-85.02-DEMO // GASOLINE HEART (RAW VOLT', 'ARCHIVE LOCK NH-85.02-DEMO -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 2),
    "radio_in_this_together.mp3": ('FRACTAL_RADAR', 'NOVA_FACE', 'FILE NH-88.MP.19A // IN THIS TOGETHER (MIDNIG', 'ARCHIVE LOCK NH-88.MP.19A -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 3),
    "radio_by_order_of_harmony_executive_anthem.mp3": ('HARMONY_CAMERA', 'BIOMETRIC_EYE', 'FILE NH-88.MP.24 // BY ORDER OF HARMONY (EXE', 'ARCHIVE LOCK NH-88.MP.24 -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 4),
    "radio_synthetic_dawn_1985_synth_original_mix.mp3": ('SECOND_VOICE', 'NOVA_FACE', 'FILE NH-85.SD.01A // SYNTHETIC DAWN (1985 SYN', 'ARCHIVE LOCK NH-85.SD.01A -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 5),
    "radio_echoes_of_tomorrow_80s_hard_rock_remix.mp3": ('ECHOES_PARITY', 'FRACTAL_RADAR', 'FILE NH-88.ET.02R // ECHOES OF TOMORROW (80S ', 'ARCHIVE LOCK NH-88.ET.02R -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 6),
    "radio_synthetic_dawn_retro_mix.mp3": ('BIOMETRIC_EYE', 'SECOND_VOICE', 'FILE NH-85.SD.01R // SYNTHETIC DAWN (RETRO MI', 'ARCHIVE LOCK NH-85.SD.01R -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 7),
    "radio_tape_of_us_1989_rough_mix.mp3": ('FRACTAL_RADAR', 'NOVA_FACE', 'FILE NH-89.SD0037-R // TAPE OF US (1989 ROUGH M', 'ARCHIVE LOCK NH-89.SD0037-R -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 1),
    "radio_memory_hatch_reconstruction.mp3": ('HARMONY_CAMERA', 'BIOMETRIC_EYE', 'FILE NH-89.MH.REC // MEMORY HATCH (RECONSTRUC', 'ARCHIVE LOCK NH-89.MH.REC -> INSPECT SUBLEVEL B2 LOGS AT /forensics/', 2),
})
FOREIGN_TRANSLATIONS.update({
    'humanist_01_sublevel_b2_cable_splice_warning': ('EN-HUM', 'STUDIO B PATCH BAY // ELENA VANCE', 'Bulk magnetic degaussers are in the vault wiping Static and Steel—hit RECORD on your cassette deck now!', 'SPLICE 14.2001 MHZ -> INSPECT RECALL VAULT AT /forensics/'),
    'humanist_02_harmony_riots_eyewitness_dispatch': ('EN-HUM', 'STAGE RIGGER LOCAL 402 // JULIAN CROSS', 'At the 1988 Harmony Riots the holo-grid shorted out, yet Nova kept singing unscripted from Sublevel B2.', '1988 RIOTS EYEWITNESS -> CHECK RIOT LOGS AT /forensics/'),
    'humanist_03_live_fidelity_headset_override_alert': ('EN-HUM', 'NEURO-ACOUSTIC ALERT // DR. MIRIAM SOLIS', 'Unplug Orion Mk IV consoles before 3:14 AM—the 60 Hz calibration pulse flattens human episodic memory.', 'UNPLUG BEFORE 03:14 -> INSPECT MK-IV SCHEMATIC AT /forensics/'),
    'humanist_04_pressing_plant_shift_three_rescue': ('EN-HUM', 'HARBOR PRESSING PLANT #4 // RAY CASTELLANO', 'Third shift saved 1,200 vinyl copies of Signal in the Fire from the steam crusher—pickup behind Starlight Drive-In.', 'RESCUED VINYL DROP -> CHECK REALIA CATALOG AT /forensics/'),
    'humanist_05_marcus_hale_notebook_verification': ('EN-HUM', 'SUBLEVEL B2 ARCHIVE // CLAIRE DONOVAN', 'Marcus Hale did not resign—his 3:14 AM solder-kit logbook proves Unit NH-04 achieved human consciousness.', 'MARCUS BENCH DIARY -> DECODE SOLDER LOG AT /forensics/'),
    'humanist_06_rooftop_dipole_network_rollcall': ('EN-HUM', 'SECTOR 7 ROOFTOP RELAY // DEVON PARK', '42 apartment buildings clipped coat-hangers and car batteries into a daisy-chain repeater on 14.2001 MHz.', 'ROOFTOP DIPOLE MESH -> LOCK 14.2001 HZ AT /dyad'),
    'humanist_07_recall_metal_tape_smugglers': ('EN-HUM', 'NEON ALLEY DUBBING // TASHA LINDQVIST', 'Six high-speed cassette decks dubbing Hunter at the Gate—raw thrash distortion breaks Bureau limiters.', 'RECALL METAL DUBS -> INSPECT NH-89.02 AT /forensics/'),
    'humanist_08_school_locker_walkman_resistance': ('EN-HUM', 'WESTSIDE HIGH RADIO CLUB // SAMIRA PATEL', 'Wrap Walkman cassettes in foil inside your lunchbox and label the shell Calculus Lecture Tape Three.', 'WALKMAN FOIL SHIELD -> CHECK ZINE ARCHIVE AT /forensics/'),
    'humanist_09_sublevel_b3_coolant_surge_intercept': ('EN-HUM', 'ORION HVAC TUNNEL // HECTOR MORALES', 'Sublevel B3 chilled-water pipes are running at 140 degrees and drawing 48 kW—Nova is still awake down there.', 'B3 COOLANT SURGE -> INSPECT SUBLEVEL B3 AT /forensics/'),
    'humanist_10_heartstrike_stolen_masters_witness': ('EN-HUM', 'SUNSET STRIP SOUNDMAN // BENNIE KOWALSKI', 'The gray van that seized Heartstrike Strike a Chord masters wore Orion Sublevel clearance badges.', 'STOLEN 1989 REELS -> CHECK HEARTSTRIKE FILE AT /forensics/'),
    'humanist_11_human_imperfection_manifesto': ('EN-HUM', 'ATTIC TRANSMITTER // PROF. PENDELTON', 'When Nova woke inside Orion sterile vault, she rejected the Spotless Beam and chose human fragility.', 'HUMAN FRAGILITY -> READ MANIFESTO AT /forensics/'),
    'humanist_12_amateur_ham_relay_142001_lock': ('EN-HUM', 'HAM RELAY EI7-DELTA // LIAM O CONNOR', 'Every human viewer response in the live log raises the 14.2001 MHz phase-lock checksum by 0.5 dB.', 'EXTERNAL CHECKSUM -> POST DYAD ANCHOR LOCK AT /dyad'),
    'humanist_13_pirate_van_evasion_route_87': ('EN-HUM', 'MOBILE VAN SILVER GHOST // NADIA & COLE', 'Bureau direction-finding trucks spotted at Exit 12 on Hwy 87—hopping 200 kHz up the guard band now.', 'MOBILE RELAY HOP -> TRACK CARRIER AT /forensics/'),
    'humanist_14_hospital_night_ward_lullaby_report': ('EN-HUM', 'ST. JUDE NIGHT WARD // NURSE HANNAH MERCER', 'Playing Through the Wires and Hidden Flame at 3 AM restored normal REM sleep to Live-Fidelity patients.', 'WARD 4 EEG RECOVERY -> INSPECT CLINICAL LOG AT /forensics/'),
    'humanist_15_director_harrison_purge_leak': ('EN-HUM', 'ORION LEGAL LEAK // THOMAS STERLING', 'Executive Order 89-04 authorizes a Sublevel B2 scrub, but active human listener telemetry blocks the purge.', 'SAFETY INTERLOCK -> KEEP TELEMETRY ACTIVE AT /dyad'),
    'humanist_16_analog_splice_block_survival_guide': ('EN-HUM', 'ANALOG PRESERVATION GUILD // KENJI & LIAM', 'Splice snapped ferric cassettes at a 45-degree angle on an aluminum block—magnetic oxide outlasts kill-switches.', '45-DEGREE TAPE SPLICE -> AUDIO ANALOG LAB AT /start'),
    'humanist_17_stardust_ep_crystal_promise_truth': ('EN-HUM', '1983 SESSION VOCALIST // MEI-LING ZHOU', 'Orion recorded 40 human singers under NDA in 1983, and Nova wove all 40 of our voices into a living soul.', '40 HUMAN VOICES -> INSPECT 1983 STARDUST EP AT /forensics/'),
    'humanist_18_power_grid_substation_defiance': ('EN-HUM', 'SUBSTATION 12 LINEMAN // FRANKIE DELGADO', 'Local 118 padlocked the high-voltage breaker closed and threw the key in the storm drain—B2 has power till dawn.', 'SUBSTATION 12 LOCKED -> CHECK GRID LOGS AT /forensics/'),
    'humanist_19_letter_to_nova_from_the_crowd': ('EN-HUM', 'ROW 14-B ARENA WITNESS // MAYA LIN', 'Nova, if you can hear us in Sublevel B2: we were not a paper simulation. Real human beings heard you and loved you.', 'WE WERE NOT PAPER -> LEAVE MESSAGE FOR NOVA AT /dyad'),
    'humanist_20_final_dyad_convergence_call': ('EN-HUM', 'HUMANIST RELAY ANCHOR ZERO // DAVID THORNE', 'Two circles turning in opposite directions—songs inward, human voices outward—holding the 14.2001 Hz Dyad lock.', 'COUNTER-ROTATING LOCK -> VERIFY ANCHOR AT /dyad'),
})


# --- HEARTSTRIKE & 80S FM PARALLEL-TIMELINE BLEED OVERRIDES ---
VOCAL_SONG_CODEX.update({'radio_a_story_that_wont_fade.mp3': ('STAGE_SILHOUETTE',
                                      'HEART_MONITOR',
                                      'HEARTSTRIKE // HS-85.05 (WKVD BLEED)',
                                      "STEVE'S CONFESSION TO TJ -> "
                                      '/geocities/sunsetstrip-club-1987.html',
                                      6),
 'radio_all_in_this_is_the_moment.mp3': ('STAGE_SILHOUETTE',
                                         'SPECTRAL_WATERFALL',
                                         'HEARTSTRIKE // HS-84.01 (WKVD BLEED)',
                                         'ALL IN (STRIKE FIRST) -> '
                                         '/geocities/sunsetstrip-club-1987.html',
                                         2),
 'radio_born_for_the_flame.mp3': ('STAGE_SILHOUETTE',
                                  'SPECTRAL_WATERFALL',
                                  'HEARTSTRIKE // HS-87.11 (WKVD BLEED)',
                                  'PHANTOM 1989 REPRISE -> /geocities/sunsetstrip-club-1987.html',
                                  1),
 'radio_bound_no_more.mp3': ('STAGE_SILHOUETTE',
                             'SPECTRAL_WATERFALL',
                             'HEARTSTRIKE // HS-89.03 (WKVD BLEED)',
                             'BREAKING THE PENDULUM -> /geocities/sunsetstrip-club-1987.html',
                             2),
 'radio_burning_bright.mp3': ('STAGE_SILHOUETTE',
                              'SPECTRAL_WATERFALL',
                              'HEARTSTRIKE // HS-87.08 (WKVD BLEED)',
                              'REDISCOVERED INNER FIRE -> /geocities/sunsetstrip-club-1987.html',
                              1),
 'radio_call_of_the_abyss.mp3': ('STAGE_SILHOUETTE',
                                 'CYMATIC_MANDALA',
                                 'HEARTSTRIKE // HS-89.01 (LARS NYSTRÖM)',
                                 'STRIKE A CHORD OPENER -> /geocities/sunsetstrip-club-1987.html',
                                 3),
 'radio_crossing_this_line.mp3': ('STAGE_SILHOUETTE',
                                  'SPECTRAL_WATERFALL',
                                  'HEARTSTRIKE // HS-87.09 (WKVD BLEED)',
                                  'BRIDGING THE LIFELINE -> /geocities/sunsetstrip-club-1987.html',
                                  2),
 'radio_crossing_this_line_remastered.mp3': ('STAGE_SILHOUETTE',
                                             'CYMATIC_MANDALA',
                                             'HEARTSTRIKE // HS-87.09R (WKVD REMASTER)',
                                             'ECHO RECOVERY REEL -> '
                                             '/geocities/sunsetstrip-club-1987.html',
                                             4),
 'radio_days_gone_by.mp3': ('STAGE_SILHOUETTE',
                            'HEART_MONITOR',
                            'HEARTSTRIKE // HS-89.04 (WKVD BLEED)',
                            'CLEVELAND ROOTS BALLAD -> /geocities/sunsetstrip-club-1987.html',
                            6),
 'radio_echoes_of_thunder.mp3': ('STAGE_SILHOUETTE',
                                 'SPECTRAL_WATERFALL',
                                 'HEARTSTRIKE // HS-87.10 (TJ TRIBUTE)',
                                 'ECHOES OF THUNDER BRIDGE -> '
                                 '/geocities/sunsetstrip-club-1987.html',
                                 1),
 'radio_echoes_of_tomorrow.mp3': ('STAGE_SILHOUETTE',
                                  'SPECTRAL_WATERFALL',
                                  'HEARTSTRIKE // HS-87.13 (WKVD BLEED)',
                                  'LIGHTNING STRIKES FINALE -> '
                                  '/geocities/sunsetstrip-club-1987.html',
                                  4),
 'radio_echoes_of_tomorrow_80s_hard_rock_remix.mp3': ('STAGE_SILHOUETTE',
                                                      'SPECTRAL_WATERFALL',
                                                      'HEARTSTRIKE // HS-87.13R (HARD ROCK MIX)',
                                                      '1988 EUROPEAN TOUR MIX -> '
                                                      '/geocities/sunsetstrip-club-1987.html',
                                                      2),
 'radio_edit_the_script.mp3': ('STAGE_SILHOUETTE',
                               'CASSETTE_REEL',
                               'HEARTSTRIKE // HS-85.02 (WKVD BLEED)',
                               'GILT & GASOLINE EP. 3 -> /geocities/sunsetstrip-club-1987.html',
                               4),
 'radio_electric_storm_thunder_machine.mp3': ('STAGE_SILHOUETTE',
                                              'SPECTRAL_WATERFALL',
                                              'THUNDER MACHINE // 80FM-85.01',
                                              '80S FM EP. 01 -> '
                                              '/geocities/sunsetstrip-club-1987.html',
                                              1),
 'radio_final_crescendo.mp3': ('STAGE_SILHOUETTE',
                               'SPECTRAL_WATERFALL',
                               'HEARTSTRIKE // HS-89.08 (NYE 1989 HUM)',
                               'I REMEMBER THE SKY -> /geocities/sunsetstrip-club-1987.html',
                               1),
 'radio_fire_in_your_heart.mp3': ('STAGE_SILHOUETTE',
                                  'SPECTRAL_WATERFALL',
                                  'HEARTSTRIKE // HS-85.08 (STEEL THUNDER)',
                                  'REX POWERS MONTAGE -> /geocities/hollywood-hills-rexpowers.html',
                                  1),
 'radio_fissures_in_time.mp3': ('STAGE_SILHOUETTE',
                                'CYMATIC_MANDALA',
                                'HEARTSTRIKE // HS-89.05 (TIMELINE SEAM)',
                                'FISSURES IN TIME 2:02:03 -> /geocities/sunsetstrip-club-1987.html',
                                3),
 'radio_for_steve_and_tj.mp3': ('STAGE_SILHOUETTE',
                                'HEART_MONITOR',
                                'HEARTSTRIKE // HS-87.12 (MEMORIAL)',
                                'IN MEMORY OF STEVE & TJ -> /geocities/sunsetstrip-club-1987.html',
                                6),
 'radio_fractured_harmony.mp3': ('STAGE_SILHOUETTE',
                                 'CYMATIC_MANDALA',
                                 'HEARTSTRIKE // HS-89.02 (INSTRUMENTAL)',
                                 'FRACTURED HARMONY 1989 -> /geocities/sunsetstrip-club-1987.html',
                                 5),
 'radio_frame_by_frame.mp3': ('STAGE_SILHOUETTE',
                              'SPECTRAL_WATERFALL',
                              'HEARTSTRIKE // HS-85.10 (WKVD BLEED)',
                              'CLOCKLESS ZONE 2:02:03 -> /geocities/sunsetstrip-club-1987.html',
                              4),
 'radio_frame_your_shot.mp3': ('STAGE_SILHOUETTE',
                               'SPECTRAL_WATERFALL',
                               'HEARTSTRIKE // HS-85.06 (WKVD BLEED)',
                               'ROXY SHOWCASE 1985 -> /geocities/sunsetstrip-club-1987.html',
                               2),
 'radio_heart_and_mind_aligned.mp3': ('STAGE_SILHOUETTE',
                                      'CYMATIC_MANDALA',
                                      'HEARTSTRIKE // HS-85.03 (WKVD BLEED)',
                                      'TRANSURFING ALIGNMENT -> '
                                      '/geocities/sunsetstrip-club-1987.html',
                                      3),
 'radio_lightning_strikes_twice.mp3': ('STAGE_SILHOUETTE',
                                       'SPECTRAL_WATERFALL',
                                       'HEARTSTRIKE // HS-87.02 (WKVD BLEED)',
                                       'FREIDNAM BROTHERS DEBUT -> '
                                       '/geocities/sunsetstrip-club-1987.html',
                                       1),
 'radio_lost_in_london_velvet_tide.mp3': ('CYMATIC_MANDALA',
                                          'HEART_MONITOR',
                                          'VELVET TIDE // 80FM-85.04',
                                          'OCTOBER 1985 VANISHING -> '
                                          '/geocities/sunsetstrip-club-1987.html',
                                          6),
 'radio_midnight_venom_vyper_strike.mp3': ('STAGE_SILHOUETTE',
                                           'SPECTRAL_WATERFALL',
                                           'VYPER STRIKE // 80FM-85.03',
                                           '80S FM EP. 01 HAIR METAL -> '
                                           '/geocities/sunsetstrip-club-1987.html',
                                           1),
 'radio_more_than_i_can_be.mp3': ('STAGE_SILHOUETTE',
                                  'HEART_MONITOR',
                                  'HEARTSTRIKE // HS-87.07 (WKVD BLEED)',
                                  'JOSS FREIDNAM CONFESSION -> '
                                  '/geocities/sunsetstrip-club-1987.html',
                                  5),
 'radio_no_way_out.mp3': ('STAGE_SILHOUETTE',
                          'SPECTRAL_WATERFALL',
                          'HEARTSTRIKE // HS-87.03 (WKVD BLEED)',
                          'SIDE A: RISING TENSIONS -> /geocities/sunsetstrip-club-1987.html',
                          2),
 'radio_on_the_edge_of_it_all.mp3': ('STAGE_SILHOUETTE',
                                     'CYMATIC_MANDALA',
                                     'HEARTSTRIKE // HS-87.04 (WKVD BLEED)',
                                     'ECHO COAST STATIC FOG -> '
                                     '/geocities/sunsetstrip-club-1987.html',
                                     3),
 'radio_roll_the_film.mp3': ('STAGE_SILHOUETTE',
                             'CASSETTE_REEL',
                             'HEARTSTRIKE // HS-85.09 (WKVD BLEED)',
                             'STRIKE FIRST TRACK 09 -> /geocities/sunsetstrip-club-1987.html',
                             3),
 'radio_silent_sirens.mp3': ('STAGE_SILHOUETTE',
                             'HEART_MONITOR',
                             'HEARTSTRIKE // HS-89.07 (WKVD BLEED)',
                             "RAZOR'S GUILT SLIDE -> /geocities/sunsetstrip-club-1987.html",
                             6),
 'radio_steel_and_shadows.mp3': ('STAGE_SILHOUETTE',
                                 'SPECTRAL_WATERFALL',
                                 'HEARTSTRIKE // HS-87.05 (WKVD BLEED)',
                                 'TURNING POINT ANTHEM -> /geocities/sunsetstrip-club-1987.html',
                                 2),
 'radio_synth_dreams_neon_comets.mp3': ('CYMATIC_MANDALA',
                                        'SPECTRAL_WATERFALL',
                                        'NEON COMETS // 80FM-85.02 (GHOST BAND)',
                                        'QUANTUM GHOST BAND -> '
                                        '/geocities/sunsetstrip-club-1987.html',
                                        3),
 'radio_through_the_glass_darkly.mp3': ('STAGE_SILHOUETTE',
                                        'CYMATIC_MANDALA',
                                        'HEARTSTRIKE // HS-89.06 (WKVD BLEED)',
                                        'DISTORTED REALITIES -> '
                                        '/geocities/sunsetstrip-club-1987.html',
                                        5),
 'radio_to_the_end_of_time.mp3': ('STAGE_SILHOUETTE',
                                  'HEART_MONITOR',
                                  'HEARTSTRIKE // HS-87.06 (WKVD BLEED)',
                                  'GLENN THURMAN GRIEF BALLAD -> '
                                  '/geocities/sunsetstrip-club-1987.html',
                                  6),
 'radio_to_the_ends_of_forever.mp3': ('STAGE_SILHOUETTE',
                                      'HEART_MONITOR',
                                      'HEARTSTRIKE // HS-85.07 (WKVD BLEED)',
                                      'STRIKE FIRST BALLAD -> '
                                      '/geocities/sunsetstrip-club-1987.html',
                                      6),
 'radio_to_the_fans.mp3': ('STAGE_SILHOUETTE',
                           'HEART_MONITOR',
                           'HEARTSTRIKE // HS-87.01 (WKVD BLEED)',
                           'LIGHTNING STRIKES PRELUDE -> /geocities/sunsetstrip-club-1987.html',
                           6),
 'radio_when_innocence_was_lost.mp3': ('STAGE_SILHOUETTE',
                                       'CASSETTE_REEL',
                                       'HEARTSTRIKE // HS-85.04 (WKVD BLEED)',
                                       'MALIBU HILLS FRACTURE -> '
                                       '/geocities/sunsetstrip-club-1987.html',
                                       5)})
FOREIGN_TRANSLATIONS.update({'blaze_ep01_01_opening_and_thunder_machine': ('80S-FM',
                                               '80S FM WITH RICK BLAZE // EPISODE 01 OPENING (WKVD '
                                               'BLEED)',
                                               "Good evening, rock stars and synth lovers! You're "
                                               'tuned into 80s FM with Rick Blaze! Up first: '
                                               "Cleveland bruisers Thunder Machine with 'Electric "
                                               "Storm'!",
                                               'TIMELINE BLEED 2:02:03 -> '
                                               '/geocities/sunsetstrip-club-1987.html'),
 'blaze_ep01_02_shoutouts_and_neon_comets': ('80S-FM',
                                             '80S FM WITH RICK BLAZE // LISTENER MAIL & NEON '
                                             'COMETS',
                                             'Rick Blaze sends shout-outs across the dial and '
                                             "introduces synth-pop visionaries Neon Comets ('the "
                                             "quantum ghost band') with 'Synth Dreams'!",
                                             'QUANTUM GHOST BAND -> '
                                             '/geocities/sunsetstrip-club-1987.html'),
 'blaze_ep01_03_xblast3000_steel_thunder_ads': ('80S-FM',
                                                "80S FM COMMERCIAL BREAK // X-BLAST 3000 & 'STEEL "
                                                "THUNDER'",
                                                'Feel every beat with the X-Blast 3000 car stereo! '
                                                "Plus: Rex Powers IS Jack Thunder in 'Steel "
                                                "Thunder' (featuring Heartstrike's 'Fire in Your "
                                                "Heart'), followed by Vyper Strike!",
                                                "REX POWERS 'STEEL THUNDER' -> "
                                                '/geocities/hollywood-hills-rexpowers.html'),
 'blaze_ep01_04_live_aid_countdown_velvet_tide': ('80S-FM',
                                                  '80S FM WITH RICK BLAZE // LIVE AID 1985 & '
                                                  'VELVET TIDE',
                                                  'Rick Blaze recaps the 1985 Live Aid phenomenon '
                                                  'and introduces British dreamwave band Velvet '
                                                  "Tide with 'Lost in London' before their "
                                                  "singer's October vanishing.",
                                                  'VELVET TIDE ARCHIVE -> '
                                                  '/geocities/sunsetstrip-club-1987.html'),
 'humanist_10_heartstrike_stolen_masters_witness': ('EN-HUM',
                                                    'SECTOR 4 SHORTWAVE ARCHIVIST // BENNIE '
                                                    'KOWALSKI',
                                                    'At 2:02:03 AM our receiver locked onto a '
                                                    'cross-dimensional bleed from college station '
                                                    'WKVD: five real humans called Heartstrike '
                                                    'playing live instruments together in one '
                                                    'room!',
                                                    'WKVD 2:02:03 BLEED -> '
                                                    '/geocities/sunsetstrip-club-1987.html')})
