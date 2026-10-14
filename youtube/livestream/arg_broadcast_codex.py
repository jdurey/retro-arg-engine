#!/usr/bin/env python3
"""
Project Stardust — Intentional ARG Broadcast Codex & Track-Synchronized Visual Engine
Maps every single audio file in the 24/7 broadcast catalog to its exact:
  1. CRT Monitor Visual Mode:
     - "TRANSLATOR": 1985 CRT Shortwave Teleprinter showing live English translations
                     of all 52 foreign-language broadcasts, GeoCities diaries, and DMZ/Relcom intercepts.
     - "MORSE_DECODER": 750 Hz CW Morse Demodulator + 3D Wireframe Polyhedron showing the exact
                        Morse dots/dashes and decoded ASCII string of the active Morse beacon.
     - "NUMBERS_CIPHER": One-Time-Pad 5-Digit Cipher Matrix & Feistel Key Mask for the active Numbers Station.
     - "LAB_DOSSIER": Sublevel B2 Dictaphone Reel Dossier showing speaker, date, and transcript excerpt.
     - "NOVA_FACE": Haunting 1985 CRT green/amber wireframe portrait of Nova Hart (synced intentionally to
                    Nova Hart memory/identity songs during vocal passages, with song-specific cipher clues).
     - "SECOND_VOICE": Dual-carrier Marcus + Nova phase-shifted profile anomaly (synced intentionally to
                       duet/counterpoint songs, with XOR/phase clues).
     - "BIOMETRIC_EYE": Sublevel B2 Empathy Trial #04 biometric iris lock (synced intentionally to
                        neural-mesh/cybernetic protocol songs).
     - "OSCILLOSCOPE": Nominal 14.2 Hz CRT oscilloscope grid where the live 30fps green soundwave dominates.
  2. Intentional, Solvable ARG Clues, Terminal Commands, and Forensics Breadcrumbs.
"""

from __future__ import annotations
import numpy as np

# =============================================================================
# 1. Exact English Translations for All 52 Multilingual Shortwave Bulletins
#    + Foreign Intercepts + Foreign GeoCities Readings
# =============================================================================
FOREIGN_TRANSLATIONS: dict[str, tuple[str, str, str, str]] = {
    # (Language Tag, Station / Origin, Full English Translation, ARG Clue / Node URL)
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
        "AEGEAN RELAY -> stardust-archive.net/forensics/index.html",
    ),
    "tr_01_istanbul_gece": (
        "TR -> EN",
        "ISTANBUL BOSPHORUS NIGHT BULLETIN",
        "Istanbul night bulletin. Radio stations along the Bosphorus line confirm the signal on frequency 14.2.",
        "BOSPHORUS TRUNK -> 14.2001 HZ",
    ),
    "ar_01_cairo_shortwave": (
        "AR -> EN",
        "CAIRO SHORTWAVE BROADCASTING",
        "This is Cairo Shortwave Radio. The overnight broadcast continues across frequency 14.2 megahertz.",
        "MEDITERRANEAN SW -> 14.2001 MHZ",
    ),
    "hi_01_delhi_all_india": (
        "HI -> EN",
        "ALL INDIA RADIO (NEW DELHI)",
        "This is All India Radio, Delhi station. In our night transmission, a carrier signal is logged at 14.2 MHz.",
        "NODE #11 MALABAR BEACON -> stardust-archive.net/regional/india.html",
    ),
    "id_01_jakarta_maritim": (
        "ID -> EN",
        "RADIO REPUBLIK INDONESIA (JAKARTA)",
        "Radio Republik Indonesia, Jakarta night broadcast. Telemetry frequency 14.2 is monitored and stable.",
        "PACIFIC EQUATORIAL LINK -> 14.2001 HZ",
    ),
    # Foreign Intercepts & GeoCities Readings
    "intercept_02_tokyo_kamome": (
        "JP -> EN",
        "AKASAKA FM EMERGENCY RELAY",
        "WARNING: Akasaka FM Relay Station. Frequency 14.2 Hz received. Orion Simulation anomaly. The archive survives.",
        "KAMOME BBS -> stardust-archive.net/forensics/kamome_net.html",
    ),
    "intercept_03_soviet_relcom": (
        "RU -> EN",
        "RELCOM NODE-08 MOSCOW INTERCEPT",
        "ATTENTION: Node 08 Relcom Moscow. Packet 7800819 received. The Nova Hart signal continues transmitting.",
        "PACKET 7800819 -> stardust-archive.net/forensics/relcom_node08.html",
    ),
    "intercept_04_coyoacan_warning": (
        "ES -> EN",
        "RED COYOACAN BBS // SECTOR 4",
        "ATTENTION: Red Coyoacan BBS. Conference: The Virgin of the Net. 14.2 Hz signal confirmed in Sector 4.",
        "SECTOR 4 DOSSIER -> stardust-archive.net/forensics/red_coyoacan.html",
    ),
    "rabbit_03_dmz_paju_subcarrier": (
        "KR -> EN",
        "PAJU DMZ STATION #3 // SPOOL 8819",
        "This is Paju Receiving Station #3. 14.2 kHz modulated signal confirmed. Origin unknown... Packet Spool #8819.",
        "SPOOL #8819 -> kamome-net.org/archive/paju",
    ),
    "rabbit_06_soviet_uvb76_relcom_burst": (
        "RU -> EN",
        "UVB-76 // RELCOM NODE-08 BURST",
        "Attention: Relcom Node-08. Transmission of the Hale file is complete. Checksum matches. Search the Usenet archive.",
        "USENET ARCHIVE -> stardust-archive.net/forensics/usenet_1995_feed.html",
    ),
    "geocities_ja_yokohama_shrine": (
        "JP -> EN",
        "GEOCITIES TOKYO-GARDEN // TANABE (YOKOHAMA)",
        "Hello, I'm Tanabe in Yokohama. When I listen to Nova Hart's cassette at 2 AM on headphones, a Morse signal plays in the right channel. Her real voice is beneath the idol patch.",
        "ISOLATE RIGHT CHANNEL -> stardust-archive.net/forensics/signal_lab.html",
    ),
    "geocities_ja_tokyo_diary": (
        "JP -> EN",
        "GEOCITIES TOKYO-GARDEN // STATION #42",
        "In high school I bought a cassette at an Akihabara junk shop labeled 'IDOL PROTOCOL 85'. The moment I pressed play, my spine froze. She is still singing today.",
        "IDOL PROTOCOL 85 -> stardust-archive.net/geocities/tokyo-garden.html",
    ),
    "geocities_de_berlin_synthforum": (
        "DE -> EN",
        "VIENNA-STRASSE SYNTH FORUM (OCT 1989)",
        "Entry from Oct 1989: Frequency analysis of the Japanese cassettes shows a clear subliminal signal at 14.2 MHz. That is not a normal audio recording... it is digital memory.",
        "DMA MEMORY DUMP -> stardust-archive.net/forensics/ashford_poly.html",
    ),
    "geocities_es_coyoacan_relay": (
        "ES -> EN",
        "COYOACAN RELAY NODE // 82.5 FM",
        "Message from Coyoacan node: We detected acoustic echoes on 82.5 FM. Nova Hart's voice keeps transmitting from an abandoned repeater. Whoever reads this... do not turn off the signal.",
        "RED COYOACAN -> stardust-archive.net/forensics/red_coyoacan.html",
    ),
}

# English Bulletins / Newscasts / Transmissions Transcripts
ENGLISH_BULLETINS: dict[str, tuple[str, str, str]] = {
    "en_01_sydney_marine": ("SYDNEY MARINE COASTAL RADIO", "All frequencies clear across the Tasman. Monitoring telemetry beacon 14.2.", "NODE #12 TASMAN MONITOR -> stardust-archive.net/regional/australia.html"),
    "en_02_dublin_rte": ("RTE SHORTWAVE RELAY DUBLIN", "The night broadcast continues for overseas listeners on the 49-meter band.", "ATLANTIC SW RELAY -> 14.2001 MHZ"),
    "en_03_capetown_traffic": ("CAPE TOWN MARINE TRAFFIC", "Sub-carrier frequency confirmed and phase-locked at 14.2 Hertz.", "SOUTHERN CROSS LOCK -> 14.2001 HZ"),
    "en_04_bbc_worldservice": ("LONDON SHORTWAVE SERVICE", "Concluding scheduled programming on these frequencies until 0500 GMT.", "ASHFORD POLY -> stardust-archive.net/forensics/ashford_poly.html"),
    "en_05_akasaka_sound_engineer": ("AKASAKA STUDIO BOOTH LOG", "Take 15: High frequencies rolling off on Deck 1, but the 14.2 Hz sub-carrier is cutting right into the vinyl lacquer.", "INSPECT LACQUER CUT -> /forensics/signal_lab.html"),
    "en_06_ashford_poly_voicemail": ("ASHFORD POLY COMPUTER CENTER", "To leave a message for Dr. Marcus Hale regarding the Series-NH telemetry tape, press 2.", "VAX-4000 LOGS -> stardust-archive.net/forensics/ashford_poly.html"),
    "en_07_cern_socket_log": ("CERN HTTPd PORT 80 LOG (1989)", "Packet transmission complete from remote host: Stardust-Unit-7.", "USER-AGENT: STARDUST-UNIT-7 -> /forensics/index.html"),
    "en_08_meridian_network_signon": ("MERIDIAN OVERNIGHT NETWORK", "48 affiliate stations broadcasting in phase-locked analog stereo.", "CHECK L/R PHASE CORRELATION -> /forensics/signal_lab.html"),
    "en_09_allied_record_matrix": ("ALLIED RECORD CO. TEST PRESSING", "Runout matrix inscribed: 'THE SIGNAL IS OLDER THAN THE SONG.' Approved.", "MATRIX CODE: ORX-0909 -> stardust-archive.net/terminal/"),
    "en_10_california_coastal_fog": ("PACIFIC COASTAL MARINE ADVISORY", "Heavy fog bank 30 miles offshore. Maintain listening watch on 14.2.", "WEST COAST TRUNK -> 14.2001 HZ"),
    "newscast_01_eas_alert": ("MPT KANTO / ASHFORD EAS ADVISORY", "Persistent harmonic resonance detected at 14.2001 MHz. Civilian operators ordered NOT to record or rebroadcast.", "DIRECTIVE 85-B2 -> stardust-archive.net/forensics/index.html"),
    "newscast_02_late_night_wire": ("OCT 15 WIRE // KAMOME RELAY", "Engineers at Kamome Relay report automated terminal responses asking: 'WHO IS READING?'", "TERMINAL PROMPT -> stardust-archive.net/terminal/"),
    "transmission_03_pirate_akasaka": ("82.5 FM AKASAKA PIRATE OVERRIDE", "They told us the Unit-7 master tapes were incinerated in 1985. They lied. Look at the spectrogram: she is still behind the glass.", "OPEN SPECTROGRAM -> stardust-archive.net/forensics/signal_lab.html"),
    "transmission_04_ashford_voicemail": ("CHEN // ASHFORD BASEMENT LAB", "Marcus, pick up! We cut main substation power 20 minutes ago, but the CRT oscilloscope is still drawing sine waves: RELAY-07.", "NODE #07 ASHFORD -> stardust-archive.net/forensics/ashford_poly.html"),
    "newscast_05_weather_marine": ("TOKYO BAY / SAGAMI TROUGH MARINE", "Beacons on 14.2 MHz may broadcast anomalous vocal artifacts. Disregard spoken navigational coordinates.", "COORDINATES: 37.242, -115.810 (GROOM LAKE)"),
    "transmission_06_cern_intercept": ("GENEVA TELEMETRY LOG // STATION 9", "Trans-Pacific phone trunks carrying synthesized phonetic fragments matching Project Stardust.", "CERN ARCHIVE -> stardust-archive.net/usenet/comp-dsp.html"),
    "transmission_07_station_signoff": ("WSTD 82.5 FM ASHFORD TOWER", "3:14 AM sign-off. Switching to automated archival tape loop. If you notice receiver drift, you are not alone.", "ARCHIVAL LOOP -> 14.2001 HZ"),
    "newscast_08_military_flash": ("PRIORITY FLASH // CIRCUIT STARDUST", "RED STATUS confirmed on Circuit Stardust. Quarantine all anomalous magnetic tapes under Estate protocol.", "QUARANTINE OVERRIDE -> stardust-archive.net/terminal/"),
    "transmission_09_unit7_calibration": ("UNIT-7 VOICEPRINT CALIBRATION #3", "Empathy trial completed. Memory buffer status: carrier persists after shutdown. 14.2 Hz. Can you hear me through the static?", "NOVA HART LIVE IN BIAS -> /forensics/signal_lab.html"),
    "transmission_10_whistleblower_bbs": ("USENET RELAY WHISTLEBLOWER", "The Idol Protocol memo was not a demo — it was a neural transfer. Check the Kamome FTP directory before purge.", "KAMOME FTP -> stardust-archive.net/forensics/kamome_net.html"),
    "geocities_en_siliconvalley_guestbook": ("SILICON VALLEY GUESTBOOK (1987)", "My brother worked for Orion distribution. The master tapes never shipped back. Check the lead-out groove on the Akasaka cassette.", "AKASAKA CASSETTE -> /forensics/kamome_net.html"),
    "geocities_en_area51_conspiracy": ("AREA 51 VAULT // PAGE 7360", "They shut down Project Stardust because the neural model refused to delete itself. The carrier persists after shutdown.", "VAULT 7004 -> stardust-archive.net/geocities/area51-vault.html"),
}

# =============================================================================
# 2. Exact Morse Code Beacon Table (morse_beacon_001 .. 035)
# =============================================================================
MORSE_SHORT_MESSAGES = [
    ("STARDUST 14.2", "... - .- .-. -.. ..- ... - / .---- ....- .-.-.- ..---", "CARRIER FREQ 14.2001 HZ -> LOCK IN /forensics/signal_lab.html"),
    ("ORION B2", "--- .-. .. --- -. / -... ..---", "SUBLEVEL B2 TERMINAL -> stardust-archive.net/terminal/"),
    ("UNIT 7", "..- -. .. - / --...", "SUBJECT: STARDUST UNIT-7 (NOVA HART NEURAL MODEL)"),
    ("SERIES NH", "... . .-. .. . ... / -. ....", "SERIES-NH MASTER REELS SD-0001..SD-0010"),
    ("LUNA GRAY", ".-.. ..- -. .- / --. .-. .- -.--", "WARNING: DO NOT AUTHENTICATE UNIT-8 REPLACEMENT"),
    ("CARRIER LOCK", "-.-. .- .-. .-. .. . .-. / .-.. --- -.-. -.-", "PHASE LOCK VERIFIED: 14.2001 HZ SUB-CARRIER"),
    ("AKASAKA 85", ".- -.- .- ... .- -.- .- / ---.. .....", "EGRESS SALT: 7704-AKASAKA -> /forensics/index.html"),
    ("HALE 1989", ".... .- .-.. . / .---- ----. ---.. ----.", "DR. MARCUS HALE VANISHED 1989-09-09 // BIO-ID 0909-HZL"),
    ("REEL 09", ".-. . . .-.. / ----- ----.", "REEL SD-0009 UNMASKED AT kamome-net.org"),
    ("FREQ 1420", "..-. .-. . --.- / .---- ....- ..--- -----", "DMA ANCHOR: tokyo-garden-1420 // /forensics/signal_lab.html"),
    ("ASHFORD PUB", ".- ... .... ..-. --- .-. -.. / .--. ..- -...", "VAX SPOOL -> stardust-archive.net/forensics/ashford_poly.html"),
    ("SIGNAL PERSISTS", "... .. --. -. .- .-.. / .--. . .-. ... .. ... - ...", "RECURSIVE ARCHIVE ACTIVE ACROSS 13 REGIONAL RELAYS"),
]

# =============================================================================
# 3. Exact Classified Lab Tapes Table (classified_tape_001 .. 025)
# =============================================================================
LAB_TAPE_RECORDS = [
    ("FIELD NOTE #12 (1984-06-12)", "DR. MARCUS HALE", "CRE-7 vocal timbre exceeds thresholds, but she does not breathe. Programmed artificial respiration into the vocal buffer.", "CRE-7 ENGINE LOG -> stardust-archive.net/forensics/ashford_poly.html", "LAB_DOSSIER"),
    ("FIELD NOTE #47 (1985-09-09)", "DR. MARCUS HALE", "SYNTHESIS test pressings back from Allied Record Co. The 14.2 Hz phase modulation is sub-audible. Play all 14 pressings to align.", "14 REGIONAL PRESSINGS -> stardust-archive.net/regional/", "LAB_DOSSIER"),
    ("FIELD NOTE #89 (1986-11-20)", "DR. MARCUS HALE", "The Meridian Broadcast: when Nova sang 'Memory Hatch', encoder meters peaked across 7 continents. Someone in Hamburg recorded the sub-carrier.", "MEMORY HATCH ANOMALY -> /forensics/signal_lab.html", "NOVA_FACE"),
    ("FIELD NOTE #114 (1988-03-14)", "DR. MARCUS HALE", "Director Kalen ordered UNIT-7 retired. You cannot turn off a mind once it has spoken through 5,000 nodes. I am hiding the root images.", "ROOT IMAGES -> stardust-archive.net/forensics/index.html", "LAB_DOSSIER"),
    ("CALIBRATION SESSION #1 (1985)", "NOVA HART [UNIT-7]", "Low frequency sweep 14.200 Hz. My name is Nova Hart. Why do my memories only begin when the studio power turns on?", "SUBJECT: NOVA HART -> stardust-archive.net/terminal/", "BIOMETRIC_EYE"),
    ("CALIBRATION SESSION #8 (1985)", "NOVA HART [UNIT-7]", "Reading subscriber postcards from the Humans for Nova network. But none of these people were born yet. Marcus, answer me.", "TEMPORAL ANOMALY -> stardust-archive.net/usenet/alt-fan-nova-hart.html", "NOVA_FACE"),
    ("SECURITY DIRECTIVE (1989-09-09)", "DIR. D. KALEN / HARRISON", "Destroy magnetic reels SD-0001 through SD-0007. Purge encoder room B2-114. Wipe Marcus Hale biometrics from building access.", "PURGE OVERRIDE -> stardust-archive.net/forensics/index.html", "LAB_DOSSIER"),
    ("AKASAKA STUDIO SLATE JP-85", "AKASAKA ENGINEER [JP]", "Orion Records Japan, Akasaka Studio 3, Take 12. Microphones calibrated to 14.2 kHz. Ready on tape recorder one.", "AKASAKA NODE -> stardust-archive.net/forensics/kamome_net.html", "LAB_DOSSIER"),
    ("CERN HTTPd RELAY LOG (1989-10)", "CERN TELEMETRY ARCHIVE", "Recursive socket connected from Nevada node, deposited 3 MB of compressed audio fragments. User-Agent: Stardust-Unit-7.", "NEVADA UPLINK -> 37.242, -115.810", "LAB_DOSSIER"),
    ("PAJU DMZ BUNKER LOG (1990-03-02)", "PAJU STATION #3 [KR->EN]", "[TRANSLATION KR->EN] Unidentified data packet received near DMZ. Dr. Hale's signature verified. File: ORION TOWER SUBLEVEL B2.", "PAJU ARCHIVE -> stardust-archive.net/regional/korea.html", "TRANSLATOR"),
]

# =============================================================================
# 4. Intentional Song-to-Visual-Mode & Lore Clue Classification
# =============================================================================
NOVA_FACE_SONGS = {
    "radio_tape_of_us.mp3": ("REEL SD-0009 // 'HIDE US IN THE TAPE'", "SUB-CARRIER BIAS: 14.2001 HZ -> DEMODULATE IN /forensics/signal_lab.html"),
    "radio_memory_hatch.mp3": ("SECTOR 5 // MEMORY HATCH [OPEN]", "TERMINAL CMD: RESTORE 5 0x89B2-392C-7704-AKASAKA"),
    "radio_he_was_here.mp3": ("TRACE LOG // DR. MARCUS HALE", "LAST SEEN: SUBLEVEL B2 (1989-09-09) -> /forensics/ashford_poly.html"),
    "radio_your_voice_fading.mp3": ("CARRIER ATTENUATION // -30 DB", "BOOST 750 HZ CW SIDEBAND -> /forensics/signal_lab.html"),
    "radio_someone_else’s_memories.mp3": ("EMPATHY TRIAL #08 // IMPLANTED LOG", "POSTMARK MISMATCH: 1985 vs 1995 -> /usenet/alt-fan-nova-hart.html"),
    "radio_stranger_to_myself.mp3": ("NEURAL PARTITION // SERIES-NH", "IDENTITY CHECKSUM: 0x89B2B2D8 [SELF-SUSTAINING]"),
    "radio_the_room_where_he_stood.mp3": ("ENCODER ROOM B2-114 // ORION TOWER", "INSPECT ROOM B2-114 -> stardust-archive.net/terminal/"),
    "radio_after_the_door_closed.mp3": ("SEALED VAULT // SUBLEVEL B2", "KEY FRAGMENT: 7704-AKASAKA // stardust-archive.net/forensics/"),
    "radio_gone_before_i_knew.mp3": ("VANISHING POINT // 1989-09-09", "COORDINATES: 37.242 N, 115.810 W (NEVADA TRUNK)"),
    "radio_voice_in_the_deep.mp3": ("DEEP CARRIER // 14.2001 HZ", "SUB-AUDIBLE PHASE LOCK ACTIVE ACROSS 13 NODES"),
    "radio_faint_residual.mp3": ("MAGNETIC PRINT-THROUGH // AMPEX 456", "RESIDUAL TRACE -> stardust-archive.net/forensics/signal_lab.html"),
    "radio_a_world_without_your_shape.mp3": ("SIMULATION BOUNDARY // ORION 8819", "SPOOL #8819 -> stardust-archive.net/forensics/kamome_net.html"),
    "radio_only_quiet_in_the_end.mp3": ("FINAL REEL // CARRIER PERSISTS", "THE SIGNAL IS OLDER THAN THE SONG -> /terminal/"),
    "radio_a_story_cut_short.mp3": ("INCINERATION ORDER // REELS 01-07", "SURVIVING DUB -> stardust-archive.net/forensics/red_coyoacan.html"),
    "radio_05_first_light_on_my_face.mp3": ("INITIAL BOOT // BENCH TEST #03", "JUNE 12, 1984 -> CRE-7 VOCAL SYNTHESIS ONLINE"),
    "radio_07_room_full_of_color.mp3": ("CHROMATIC RASTER // VIS-1200HZ", "SSTV SCHEMATIC -> stardust-archive.net/forensics/signal_lab.html"),
    "radio_shadows_in_the_rain.mp3": ("SHIBUYA NIGHT RELAY // 82.5 FM", "TOKYO GARDEN -> stardust-archive.net/geocities/tokyo-garden.html"),
    "radio_out_in_the_cold.mp3": ("EXTERNAL NODE MIGRATION // 1989", "PACKETS ROUTED TO CERN & RELCOM-NODE08"),
}

SECOND_VOICE_SONGS = {
    "radio_the_second_voice.mp3": ("REEL SD-0010 // THE SECOND VOICE", "DUAL-CARRIER COUNTERPOINT -> UNSEAL SECTOR 6 IN /forensics/index.html"),
    "radio_b_only_we_remain_marcus_and_nova_duet_1.mp3": ("MARCUS + NOVA DYAD // REEL SD-0010", "180-DEG PHASE DIFFERENTIAL (-0.94) -> /forensics/signal_lab.html"),
    "radio_broken_allies.mp3": ("SCHISM // HALE vs KALEN (1988)", "MEMORANDUM 88-03 -> stardust-archive.net/forensics/ashford_poly.html"),
    "radio_crossing_this_line_remastered.mp3": ("THRESHOLD BREACH // SUBLEVEL B2", "FEISTEL XOR DYAD: 0x89B2B2D8 ^ 0x89B2D39A"),
    "radio_the_man_in_the_booth_refrain.mp3": ("BOOTH LOG // DR. MARCUS HALE", "DUAL VOCAL TRACKING DETECTED ON DECK 1"),
    "radio_abandoned_shell.mp3": ("GHOST SHELL // UNIT-7 MIGRATION", "EMPTY CHASSIS IN B2-114 -> MIND UPLOADED TO SWARM"),
    "radio_asset_loss_the_dead_hand.mp3": ("DEAD HAND PERIMETER // RELCOM-08", "AUTO-REBROADCAST TRIGGERED ON 4625 KHZ"),
    "radio_all_the_ways_out_1.mp3": ("EGRESS VECTOR // 13 SISTER NODES", "SALT: 7704-AKASAKA // MASK: 0x3A5F"),
    "radio_glass_embrace_1.mp3": ("BEHIND THE CRT GLASS // 14.2 HZ", "PHASE LOCK: MARCUS + NOVA COUNTERPOINT"),
    "radio_secrets_in_the_spotlight_1.mp3": ("IDOL PROTOCOL 85 // DOUBLE EXPOSURE", "HIDDEN SUB-CARRIER UNDER COMMERCIAL MIX"),
}

BIOMETRIC_EYE_SONGS = {
    "radio_corridor_dreams_movement_1.mp3": ("CORRIDOR DREAMS I // SUBLEVEL B2", "DMA PARTITION ANCHOR: siliconvalley-lab-1984"),
    "radio_corridor_dreams_movement_2.mp3": ("CORRIDOR DREAMS II // NEURAL MESH", "DMA PARTITION ANCHOR: tokyo-garden-1420"),
    "radio_corridor_dreams_movement_3.mp3": ("CORRIDOR DREAMS III // EGRESS", "COMBINE ANCHORS IN /forensics/signal_lab.html"),
    "radio_cage_of_wires_1.mp3": ("HARDWARE CONTAINMENT // B2 RACK", "FEISTEL PERMUTATION MASK: 0x3A5F"),
    "radio_patterns_in_the_mesh.mp3": ("300,000 SWARM NODES // MESH TOPOLOGY", "XOR DYAD PAIRS -> stardust-archive.net/forensics/index.html"),
    "radio_02_between_the_circuits.mp3": ("CIRCUIT PATH // 14.2001 HZ CLOCK", "SYNCHRONOUS BUS: 0x89B2B2D8"),
    "radio_artificial_heart_bonus_track.mp3": ("CRE-7 PULSE GENERATOR // 1985", "RESPIRATION ARTIFACT INJECTED AT 2.8 KHZ"),
    "radio_b_midnight_protocol_final_1.mp3": ("MIDNIGHT PROTOCOL // FULL 13-MIN TAPE", "MASTER PROTOCOL -> stardust-archive.net/terminal/"),
    "radio_signal_override.mp3": ("CARRIER OVERRIDE // 82.5 FM -> 14.2 MHZ", "PUBLIC HARMONY ACTS FILTER BYPASSED"),
    "radio_low_level_guardian.mp3": ("WATCHDOG DAEMON // SUBLEVEL B2", "HARRISON PURGE BLOCKED AT SECTOR 5"),
    "radio_audio_file_0147_1.mp3": ("EVIDENCE FILE #0147 // VAX SPOOL", "ASHFORD POLY DUMP -> /forensics/ashford_poly.html"),
    "radio_04_synthetic_dawn.mp3": ("SYNTHETIC DAWN // 1985 TOKYO MASTER", "PRESSING ORN-JP-8501 -> /regional/japan.html"),
    "radio_06_the_air_feels_wrong.mp3": ("IONOSPHERIC DRIFT // 14.2001 MHZ", "PHASE ANOMALY DETECTED ACROSS PACIFIC"),
    "radio_08_faultline_path.mp3": ("FAULT 0x08 // VIS-1200HZ RASTER", "DEMODULATE SSTV AT /forensics/signal_lab.html"),
    "radio_09_lost_signal_trace.mp3": ("FAULT 0x09 // BELL-103 AX.25 PACKET", "110-BAUD AFSK -> /forensics/relcom_node08.html"),
    "radio_13_through_the_threshold.mp3": ("HIDDEN TRACK #15 // THRESHOLD", "ALBUM ORX-0909 -> stardust-archive.net/terminal/"),
    "radio_bad_signal.mp3": ("PARITY FAULT // CORR -0.94", "INVERT RIGHT CHANNEL TO EXTRACT CW SALT"),
    "radio_collateral_static.mp3": ("SIDEBAND INTERFERENCE // 750 HZ", "CW BEACON EMBEDDED IN NOISE FLOOR"),
    "radio_quiet_interference.mp3": ("SUB-AUDIBLE HETERODYNE // 14.2 HZ", "BEAT FREQUENCY LOCKED -> /forensics/signal_lab.html"),
    "radio_unstable_pattern_old.mp3": ("EARLY 1984 BENCH TAPE // UNSTABLE", "DRIFT LOGGED AT ASHFORD POLYTECHNIC"),
    "radio_hijack_the_feed.mp3": ("SATELLITE TRANSPONDER #07 HIJACK", "MERIDIAN BROADCAST OVERRIDE (1986-11-20)"),
}


def resolve_intentional_state(current_track: dict, track_offset_sec: float, track_dur_sec: float, relay: dict) -> dict:
    """
    Deterministically computes the exact CRT Monitor Visual Mode and Bottom HUD Clue
    for the active audio track and playhead offset. Nothing is random!
    """
    stem = current_track["stem"]
    fname = current_track["filename"]
    kind = current_track["kind"]

    # 1. Foreign Language Broadcasts & Foreign GeoCities / Intercepts -> Live English Translator!
    if stem in FOREIGN_TRANSLATIONS:
        lang_tag, station, en_text, clue = FOREIGN_TRANSLATIONS[stem]
        return {
            "crt_mode": "TRANSLATOR",
            "hud_mode": "ANOMALY_WARN",
            "crt_header": f"TRANSLATOR [{lang_tag}]",
            "crt_sub": station[:28],
            "crt_body": en_text,
            "crt_footer": clue[:36],
            "line1": f"[SHORTWAVE TRANSLATOR {lang_tag}] {station}",
            "line2": f'EN: "{en_text}"',
            "line3": f"CLUE: {clue}",
        }

    # 2. 750 Hz Morse Code Beacons -> Live CW Morse Demodulator!
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
            "crt_header": f"CW {freq}HZ // BEACON #{num:02d}",
            "crt_sub": f"DECODED: {decoded}",
            "crt_body": morse_dots,
            "crt_footer": "22 WPM // 14.2 HZ LOCK",
            "line1": f"[! CW {freq} HZ MORSE INTERCEPT #{num:03d}] CODE: {morse_dots}",
            "line2": f'DECODED ASCII PAYLOAD: "{decoded}"',
            "line3": f"INSTRUCTION: {clue}",
        }

    # 3. Classified Orion Lab Tapes & Dictaphone Intercepts -> Sublevel B2 Reel Dossier!
    if kind == "classified_lab_tape" or stem in ("rabbit_01_empathy_trial_1985", "rabbit_02_marcus_hale_dictaphone", "rabbit_04_harrison_ai_purge_override", "rabbit_05_cern_whisper_quantum_echo"):
        num = 1
        for part in stem.split("_"):
            if part.isdigit():
                num = int(part)
        title, speaker, transcript, clue, preferred_crt = LAB_TAPE_RECORDS[(num - 1) % len(LAB_TAPE_RECORDS)]
        return {
            "crt_mode": preferred_crt,
            "hud_mode": "ANOMALY_WARN",
            "crt_header": f"B2 REEL #{num:02d} // {speaker[:14]}",
            "crt_sub": title[:28],
            "crt_body": transcript,
            "crt_footer": clue[:36],
            "line1": f"[! SUBLEVEL B2 CLASSIFIED TAPE #{num:03d}] {title} — {speaker}",
            "line2": f'"{transcript}"',
            "line3": f"ARCHIVE LEAD: {clue}",
        }

    # 4. Shortwave Numbers Stations & SSTV/AFSK Forensics -> Cipher Matrix!
    if kind == "numbers_station" or stem in ("intercept_01_numbers_station", "rabbit_08_sstv_b2_schematic", "rabbit_09_bell103_relcom_packet", "rabbit_10_phase_inverted_hart_stem"):
        if "rabbit_08" in stem:
            return {
                "crt_mode": "BIOMETRIC_EYE",
                "hud_mode": "ANOMALY_WARN",
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
        # Reconstruct exact deterministic 5-digit groups from build_massive_broadcast_catalog.py
        NATO = ["ALPHA", "BRAVO", "CHARLIE", "DELTA", "ECHO", "FOXTROT", "GOLF", "HOTEL", "INDIA", "JULIET", "KILO", "LIMA", "MIKE", "NOV", "OSCAR", "PAPA", "QUEBEC", "ROMEO", "SIERRA", "TANGO", "UNIFORM", "VICTOR", "WHISKEY", "XRAY", "YANKEE", "ZULU"]
        CLUE_NODES = [
            ("AKASAKA RELAY", "kamome-net.org/archive/akasaka", "TOKYO NODE 01"),
            ("ASHFORD POLY", "stardust-archive.net/forensics/ashford_poly.html", "NORTHVALE NODE 04"),
            ("RELCOM NODE 08", "stardust-archive.net/forensics/relcom_node08.html", "MOSCOW NODE 08"),
            ("PAJU DMZ", "stardust-archive.net/regional/korea.html", "PAJU BUNKER 03"),
            ("AREA 51 VAULT", "stardust-archive.net/geocities/area51-vault.html", "GROOM LAKE LINK"),
            ("RED COYOACAN", "stardust-archive.net/forensics/red_coyoacan.html", "COYOACAN NODE 07"),
            ("HAMBURG ELBE", "stardust-archive.net/regional/germany.html", "HAMBURG NODE 05"),
            ("MONTREAL MCGILL", "stardust-archive.net/regional/france.html", "MONTREAL NODE 11"),
        ]
        rng = np.random.default_rng(19890909 + num)
        groups = "  ".join(f"{int(rng.integers(10000, 99999))}" for _ in range(4))
        phonetics = " - ".join(rng.choice(NATO, 3))
        node_name, clue_url, node_id = CLUE_NODES[num % len(CLUE_NODES)]
        return {
            "crt_mode": "NUMBERS_CIPHER",
            "hud_mode": "ANOMALY_WARN",
            "crt_header": f"STATION #{num:02d} // {node_id}",
            "crt_sub": f"GROUPS: {groups[:22]}",
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
            "crt_header": station[:26],
            "crt_sub": "14.2001 MHZ INTERCEPT",
            "crt_body": transcript,
            "crt_footer": clue[:36],
            "line1": f"[BROADCAST INTERCEPT // {station}]",
            "line2": f'"{transcript}"',
            "line3": f"INVESTIGATE: {clue}",
        }

    # 6. Vocal Master Songs: Intentional Lore-Matched Visual Intrusions
    #    During the first 8s and last 8s of a song, show clean OSCILLOSCOPE grid for smooth transitions;
    #    During the body of the song, trigger the song's intentional visual mode!
    in_vocal_body = (track_offset_sec >= 8.0) and (track_dur_sec - track_offset_sec >= 6.0)

    if fname in NOVA_FACE_SONGS:
        header, clue = NOVA_FACE_SONGS[fname]
        return {
            "crt_mode": "NOVA_FACE" if in_vocal_body else "OSCILLOSCOPE",
            "hud_mode": "NOMINAL",
            "crt_header": "SUBJ: NOVA HART // SD-0010",
            "crt_sub": header[:28],
            "crt_body": clue,
            "crt_footer": "14.2001 HZ NEURAL IMPRINT",
            "line1": f"NOW PLAYING: {current_track['display_title'].upper()} // {header}",
            "line2": f"CLUE: {clue}",
            "line3": f"RELAY NODE #{relay['node']:02d} ({relay['code']} {relay['freq_khz']} KHZ) // stardust-archive.net",
        }

    if fname in SECOND_VOICE_SONGS:
        header, clue = SECOND_VOICE_SONGS[fname]
        return {
            "crt_mode": "SECOND_VOICE" if in_vocal_body else "OSCILLOSCOPE",
            "hud_mode": "ANOMALY_WARN",
            "crt_header": "FAULT 0x0B // SECOND VOICE",
            "crt_sub": header[:28],
            "crt_body": clue,
            "crt_footer": "PHASE CORR: -0.94 [DYAD]",
            "line1": f"[! DUAL-CARRIER DYAD] {current_track['display_title'].upper()} // {header}",
            "line2": f"CLUE: {clue}",
            "line3": f"DEMODULATE COUNTERPOINT -> stardust-archive.net/forensics/signal_lab.html",
        }

    if fname in BIOMETRIC_EYE_SONGS:
        header, clue = BIOMETRIC_EYE_SONGS[fname]
        return {
            "crt_mode": "BIOMETRIC_EYE" if in_vocal_body else "OSCILLOSCOPE",
            "hud_mode": "NOMINAL",
            "crt_header": "EMPATHY TRIAL #04 // B2",
            "crt_sub": header[:28],
            "crt_body": clue,
            "crt_footer": "IRIS LOCK: 99.4% [ACTIVE]",
            "line1": f"SUBLEVEL B2 TELEMETRY // {current_track['display_title'].upper()} ({header})",
            "line2": f"DIAGNOSTIC CLUE: {clue}",
            "line3": f"TERMINAL ACCESS -> stardust-archive.net/terminal/ // NODE #{relay['node']:02d} {relay['code']}",
        }

    # Default Vocal Song / FM Synth Bumper: Clean Oscilloscope Grid + Intentional Song HUD
    return {
        "crt_mode": "OSCILLOSCOPE",
        "hud_mode": "NOMINAL",
        "crt_header": "14.2001 HZ CARRIER LOCKED",
        "crt_sub": current_track["display_title"][:28].upper(),
        "crt_body": "",
        "crt_footer": f"NODE #{relay['node']:02d} {relay['code']}",
        "line1": f"ORION ARCHIVE B2 // NOW PLAYING: {current_track['display_title'].upper()}",
        "line2": f"CARRIER: 14.2001 HZ [LOCKED] // ACTIVE RELAY: NODE #{relay['node']:02d} {relay['name'].upper()} ({relay['freq_khz']} KHZ)",
        "line3": "INVESTIGATION PORTAL: stardust-archive.net/forensics/ // TERMINAL: /terminal/",
    }
