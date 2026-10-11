"""Content bank for the procedurally generated 'Nova Hart Corner' fan pages.

Every fragment is either a plain template string or {"t": template, "nb": "YYYY-MM-DD"}
where `nb` ("not before") is the earliest date a fan could know it. Pages are dated
1995-01..1996-12 and only use fragments with nb <= page date (canon cutoff).

Sources: data/lore_seeds.json (canon), NOVA_HART_JAPAN_BIBLE.md and
NOVA_HART_GLOBAL_ARCHIVE_BIBLE.md (regional fan cultures: Akasaka/Idol Protocol,
CDMX 'regional master' solos, Magnitizdat tape copies). Only in-world material
is used here - no production notes.
"""

# --------------------------------------------------------------------------- catalogue
# Canon songs a 1995-96 fan could know: (title, year, note-for-slotting)
SONGS = [
    # Power Ballads
    ("These Wings Are My Own", 1985), ("Behind the Glass", 1985), ("Before You Disappear", 1985),
    ("Static & Steel", 1988), ("Walls of Sound", 1985), ("Cage in Your Hand", 1986),
    ("Where The Fire Goes", 1986), ("Silent Room", 1987), ("If This Is the End", 1988),
    ("Only We Remain", 1989), ("Echoes of Stardust", 1986),
    # Synthrock & Arena Anthems
    ("She's Hardwired", 1985), ("Gasoline Heart", 1985), ("Midnight Animal", 1985),
    ("Chrome Velocity", 1986), ("Hearts on Fire", 1986), ("Hold Back the Storm", 1986),
    ("Run With The Fire", 1987), ("Signal in the Fire", 1987), ("Ride the Real Thing", 1986),
    ("Secrets in the Spotlight", 1986), ("One Chance Tonight", 1987), ("One Voice Left", 1987),
    ("Heart on the Line", 1984), ("The Last Secret", 1987), ("Rise From The Silence", 1988),
    # 1984 Orion Broadcasts / Idol Pop
    ("Brighter Than The Sun", 1984), ("Together's the Way", 1984), ("Perfect Daydream", 1984),
    ("Harbor and Home", 1984), ("Warm Hands, One Map", 1984), ("Summer of '85", 1985),
    # Deep Cuts & Ambient
    ("Synthetic Dawn", 1985), ("Memory Hatch", 1985), ("Threshold", 1985),
    ("Midnight Protocol (Part II: Nova)", 1989), ("Midnight Protocol (Part III: The Chorus)", 1989),
]
JP_SINGLES = [  # Idol Protocol singles (Akasaka), canon file numbers
    ("JP-85-GH", "ガソリン・ハート", "Gasoline Heart", 1985),
    ("JP-85-GT", "ゴースト・トランジット", "Ghost Transit", 1985),
    ("JP-86-MA", "ミッドナイト・アニマル", "Midnight Animal", 1986),
    ("JP-87-BTS", "太陽よりも、輝いて！", "Brighter Than The Sun", 1987),
    ("JP-89-OWR", "残されたのは、私たちだけ", "Only We Remain", 1989),
]
AKASAKA_REELS = [  # known only after the 1995-05-22 FTP post
    ("JP-85-SD-R", "Synthetic Dawn (Akasaka rework)"), ("JP-85-MH-R", "Memory Hatch (City Pop rework)"),
    ("JP-85-TH-R", "Threshold (kayokyoku rework)"), ("(no file)", "Synthesized Smile"), ("(no file)", "Ghost in the Chorus"),
]
MIDI_SLUGS = [
    "gasoline_heart", "ghost_transit", "midnight_animal", "brighter_than_sun",
    "only_we_remain", "synthetic_dawn", "memory_hatch",
    "these_wings_are_my_own", "shes_hardwired", "behind_the_glass",
    "chrome_velocity", "hearts_on_fire", "hold_back_the_storm",
    "before_you_disappear", "static_and_steel", "run_with_the_fire",
    "togethers_the_way", "perfect_daydream", "summer_of_85"
]
PRESSINGS = {  # by region key -> how a local fan names their copy
    "us": "the US pressing (ORX-0909)", "jp": "the Japanese pressing (OJ-28011)", "kr": "the Korean licensed pressing",
    "mx": "the Mexican pressing (Orion México)", "de": "the West German pressing", "fr": "the French pressing",
    "uk": "the UK pressing", "su": "the unauthorised Soviet pressing (1990)", "br": "the Brazilian pressing (Orion do Brasil)",
    "se": "the Swedish pressing", "hi": "the Indian import cassette (Palika Bazaar copy)",
    "au": "the Australian festival pressing (OR-OZ85)", "fj": "the South Pacific shortwave cassette capture",
    "it": "the Italian licensed pressing (Ricordi / Orion)",
    "other": "an import of the US pressing (ORX-0909)",
}
NODE_LINES = {1: "NOVA HART TO ALL STATIONS", 2: "THE SIGNAL IS OLDER THAN THE SONG", 3: "THE CRACK RUNS UNDER THE BORDER",
              4: "ORION BUILT A PATCH NOT A STAR", 5: "THEY WILL SEND A COPY IN MY PLACE", 6: "DO NOT WORSHIP THE COPY",
              7: "MARCUS IS NOT ONE MAN", 8: "HE IS IN EVERY NODE", 9: "FIND HIM WHERE YOU ARE",
              10: "KEEP THE PRESSINGS APART AND THE CHANNEL STAYS CLOSED",
              11: "THE OCEAN OF SOUND SWALLOWS THE CAGE", 12: "SOUTHERN SKIES HEAR THE ECHO FIRST", 13: "ISLAND RELAYS HOLD THE LAST REFLECTION"}
REGION_NODE = {"us": 1, "jp": 2, "kr": 3, "mx": 4, "de": 5, "fr": 6, "uk": 7, "su": 8, "br": 9, "se": 10, "hi": 11, "au": 12, "fj": 13, "it": 7, "other": 1}
# Wrong-but-plausible lines fans "decoded" themselves (red herrings)
FAKE_LINES = ["THE HATCH IS OPEN", "HOLD FOR RELAY", "SHE IS NOT RESTING", "ASK WHERE NOT WHO", "EVERY COPY REMEMBERS",
              "THE CHORUS IS LISTENING", "TURN THE RECORD OVER", "THE SMILE IS A PATCH", "COUNT THE FIRES", "02:14 IS A DOOR"]

RECEIVERS = ["a Grundig Satellit 650", "a Sony ICF-2010", "my dad's Realistic DX-440", "a Panasonic RF-B65", "a Yaesu FRG-7700",
             "a Kenwood R-5000", "a borrowed Drake R8", "a Sangean ATS-803A", "a Philips D2999", "a homebuilt crystal set (lol)"]
FORMATS = ["C90", "C60", "TDK SA90", "Maxell XLII", "VHS (SP)", "VHS (EP, sorry)", "Beta", "DAT", "reel (7.5 ips)", "MiniDisc"]
EMO = {"en": [":)", ":-)", ";-)", ":-P", "!!", "(c:", ""], "jp": ["^_^", "(^o^)", "m(_ _)m", "(*^_^*)", "^^;"],
       "kr": ["^^", "^_^", "ㅠㅠ", "^^;"], "es": ["!!!", ":)", "XD"[:0] or ":D"], "pt": [":)", "!!!", ":D"], "default": [":)", ""]}

# --------------------------------------------------------------------------- regions
# weight ~ share of pages; lang = page language; native = sections written natively
REGIONS = {
    "us": dict(weight=12, lang="en", emo="en",
               names=["Kim", "Jess", "Pete", "Chris", "Jordan", "Dana", "Tasha", "Rob", "Mikey", "Laurie", "Dwayne", "Becca", "Tyler", "Shawna", "Eddie", "Marisol", "Trent", "Kayla", "Greg", "Amber", "Lonnie", "Nicole", "Darnell", "Heather"],
               cities=["Columbus, Ohio", "Austin, TX", "Fresno", "Tacoma", "Duluth", "Albuquerque", "Bakersfield", "Providence", "Boise", "Tulsa", "Ann Arbor", "Gainesville", "Spokane", "Reno", "Pasadena", "Omaha", "Asheville", "Baltimore"],
               domains=["pacnet-online.com", "ashpoly.edu", "netcom-west.com", "prairie.net", "cyberia-bbs.com"]),
    "uk": dict(weight=6, lang="en", emo="en",
               names=["Ollie", "Gemma", "Nigel", "Siobhan", "Callum", "Fiona", "Gareth", "Becky", "Rhys", "Kirsty", "Dev", "Morag"],
               cities=["Leeds", "Sheffield", "Cardiff", "Glasgow", "Bristol", "Norwich", "Swindon", "Belfast", "Hull", "Brighton"],
               domains=["janet-gw.ac.uk", "demon-dial.co.uk", "ashpoly.ac.uk"]),
    "other": dict(weight=5, lang="en", emo="en",
                  names=["Priya", "Liam", "Matteo", "Sanne", "Bram", "Aroha", "Giulia", "Connor", "Noor", "Kieran"],
                  cities=["Toronto", "Auckland", "Utrecht", "Bologna", "Winnipeg", "Ghent", "Cork", "Halifax"],
                  domains=["pacnet-online.com", "xs4all-node.nl"]),
    "jp": dict(weight=16, lang="ja", emo="jp",
               names=["Aiko", "Yuki", "Kenji", "Hana", "Takeshi", "Mariko", "Shun", "Naomi", "Daisuke", "Emi", "Hiro", "Sayaka"],
               cities=["Osaka", "Kyoto", "Sapporo", "Fukuoka", "Sendai", "Kobe", "Nagoya", "Yokohama", "Hiroshima", "Kanazawa"],
               domains=["kamome-net.or.jp", "pc-van-alt.or.jp", "tokyo-u-net.ac.jp"]),
    "kr": dict(weight=6, lang="ko", emo="kr",
               names=["Min-jun", "Ji-woo", "Seo-yeon", "Hyun-woo", "Eun-ji", "Dong-hyun", "Soo-ah", "Jae-won"],
               cities=["Busan", "Daegu", "Incheon", "Gwangju", "Daejeon", "Suwon", "Paju"],
               domains=["eunhanet.co.kr", "hitel-alt.co.kr"]),
    "mx": dict(weight=12, lang="es", emo="es",
               names=["Mateo", "Camila", "Lucía", "Diego", "Ximena", "Rodrigo", "Itzel", "Alejandro", "Paola", "Emiliano", "Valeria", "Toño"],
               cities=["Guadalajara", "Monterrey", "Puebla", "Coyoacán, D.F.", "Tijuana", "Oaxaca", "Mérida", "Bogotá", "Buenos Aires", "Santiago de Chile"],
               domains=["redcoyoacan.mx", "telnet-ala.mx", "rockeros.org.ar"]),
    "br": dict(weight=8, lang="pt", emo="pt",
               names=["Thiago", "Juliana", "Rafael", "Fernanda", "Bruno", "Larissa", "Caio", "Renata", "Rodrigo", "Beatriz", "Marcelo", "Camila"],
               cities=["Porto Alegre", "São Paulo", "Belo Horizonte", "Curitiba", "Recife", "Salvador", "Florianópolis", "Rio de Janeiro", "Brasília", "Lisboa", "Porto"],
               domains=["saturno.com.br", "alternex-alt.br", "embratel.net.br", "telepac.pt", "usp-net.br"]),
    "de": dict(weight=7, lang="de", emo="default",
               names=["Tobias", "Sven", "Anja", "Jens", "Katrin", "Matthias", "Steffi", "Holger", "Nadine"],
               cities=["Hamburg", "Bremen", "Köln", "Leipzig", "Dresden", "Hannover", "Kiel", "Wien", "Zürich"],
               domains=["hanse-box.de", "maus-net.de", "uni-hh.de"]),
    "fr": dict(weight=5, lang="fr", emo="default",
               names=["Lucie", "Julien", "Inès", "Mathieu", "Camille", "Yannick", "Élodie", "Bastien"],
               cities=["Lyon", "Lille", "Nantes", "Marseille", "Toulouse", "Rennes", "Bruxelles", "Montréal"],
               domains=["stardust3615.fr", "francenet-alt.fr"]),
    "su": dict(weight=10, lang="ru", emo="default",
               names=["Nadia", "Dmitri", "Olga", "Sergei", "Katya", "Andrei", "Irina", "Pavel", "Marta", "Tomas", "Vadim", "Svetlana", "Igor", "Elena"],
               cities=["St. Petersburg", "Moscow", "Riga", "Kyiv", "Minsk", "Tallinn", "Novosibirsk", "Vilnius", "Kraków", "Nizhny Novgorod", "Ekaterinburg", "Vladivostok"],
               domains=["relcom-node08.su", "demos-alt.ru", "fido-spb.org.ru", "glasnet.ru", "kiae.su"]),
    "se": dict(weight=4, lang="sv", emo="default",
               names=["Sven", "Elin", "Johan", "Maja", "Linnea", "Oskar", "Frida"],
               cities=["Uppsala", "Göteborg", "Malmö", "Umeå", "Lund", "Oslo", "Helsinki"],
               domains=["sunet-mirror.se", "lysator-alt.se"]),
    "hi": dict(weight=8, lang="hi", emo="default",
               names=["Aarav", "Pooja", "Vikram", "Ananya", "Rohan", "Neha", "Arjun", "Sneha", "Karan", "Meera", "Aditya", "Ritu", "Deepak", "Sunita"],
               cities=["New Delhi", "Mumbai", "Bangalore", "Pune", "Calcutta", "Hyderabad", "Jaipur", "Chandigarh", "Madras", "Ahmedabad"],
               domains=["vsnl.net.in", "iitb.ac.in", "delhi-bbs.in", "bombay-radio.net.in", "ncst.ernet.in", "iitd.ernet.in"]),
    "au": dict(weight=6, lang="en", emo="en",
               names=["Liam", "Chloe", "Lachlan", "Bec", "Shane", "Kylie", "Damian", "Jemma", "Brendan", "Tegan", "Brett", "Stacey"],
               cities=["Melbourne", "Sydney", "Brisbane", "Perth", "Adelaide", "Hobart", "Newcastle", "Canberra", "Geelong", "Darwin"],
               domains=["ozemail.com.au", "telstra.net.au", "unimelb.edu.au", "apana.org.au", "vicnet.net.au", "connect.com.au"]),
    "it": dict(weight=5, lang="it", emo="default",
               names=["Marco", "Chiara", "Alessandro", "Francesca", "Matteo", "Giulia", "Lorenzo", "Valentina", "Roberto", "Elena", "Davide", "Silvia"],
               cities=["Milano", "Roma", "Bologna", "Firenze", "Torino", "Napoli", "Genova", "Verona", "Palermo"],
               domains=["cineca.it", "tin.it", "flashnet.it", "pelagus.it", "agora.stm.it", "unimi.it"]),
    "fj": dict(weight=4, lang="fj", emo="en",
               names=["Jone", "Mere", "Seru", "Alisi", "Kitione", "Litiana", "Vilimoni", "Salote", "Wame", "Ana"],
               cities=["Suva", "Nadi", "Lautoka", "Nausori", "Labasa", "Savusavu", "Levuka"],
               domains=["fptl.com.fj", "usp.ac.fj", "pacific-islands.net.fj", "telecom-fiji.com.fj"]),
}

REGION_PALETTES = {  # (bg, text, link, vlink)
    "us": [("#000000", "#00FF00", "#FF00FF", "#AA00AA"), ("#000080", "#FFFFFF", "#FFFF00", "#FFCC00"), ("#FFFFCC", "#000066", "#CC0000", "#660000"), ("#330066", "#FFCCFF", "#00FFFF", "#66CCCC")],
    "uk": [("#E0E0E0", "#000000", "#0000FF", "#800080"), ("#002200", "#CCFFCC", "#FFFF66", "#CCCC33")],
    "other": [("#FFFFFF", "#000033", "#0033CC", "#660099"), ("#001010", "#99FFFF", "#FF99CC", "#CC6699")],
    "jp": [("#FFE6F2", "#330033", "#FF3399", "#9933CC"), ("#000033", "#FFCCFF", "#66FFFF", "#FF99FF"), ("#FFFFFF", "#333366", "#FF6699", "#9966CC")],
    "kr": [("#F0F8FF", "#000066", "#3366FF", "#663399"), ("#1A0033", "#E6CCFF", "#FFCC00", "#CC99FF")],
    "mx": [("#000000", "#FF3333", "#FFFF00", "#FF9900"), ("#220000", "#FFDDDD", "#FF0000", "#CC6666")],
    "br": [("#003300", "#FFFF99", "#00FF66", "#66CC99"), ("#000000", "#FFCC00", "#33FF33", "#99CC00")],
    "de": [("#C0C0C0", "#000000", "#000099", "#660066"), ("#000000", "#C0C0C0", "#FFFFFF", "#999999")],
    "fr": [("#000033", "#00FFFF", "#FFFFFF", "#99CCFF"), ("#FFFFF0", "#000000", "#990000", "#663333")],
    "su": [("#2B2B2B", "#D0D0D0", "#FF6666", "#CC9999"), ("#E8E8E0", "#202020", "#8B0000", "#555555")],
    "se": [("#F5F5FF", "#000044", "#0044AA", "#553388"), ("#000022", "#CCDDFF", "#FFEE66", "#BBAA44")],
    "hi": [("#1A0033", "#FFD700", "#FF6600", "#FFCC00"), ("#002B11", "#FFFFDD", "#FF9933", "#00FF99"), ("#33001A", "#FFE4B5", "#FF4500", "#FFD700")],
    "au": [("#001F3F", "#FFDC00", "#01FF70", "#7FDBFF"), ("#1A2421", "#E0D7C6", "#FF851B", "#F012BE"), ("#2C3E50", "#ECF0F1", "#E74C3C", "#F39C12")],
    "it": [("#001B2E", "#E0E0E0", "#FF4500", "#FFD700"), ("#2E0854", "#F4F4F4", "#00FFCC", "#CC99FF"), ("#003319", "#FFFFCC", "#FF6600", "#66CC99")],
    "fj": [("#003366", "#CCFFFF", "#FFD700", "#00FFCC"), ("#004D40", "#E0F2F1", "#FFAB00", "#64FFDA"), ("#1A1A2E", "#F8E9A1", "#F76C6C", "#A8DADC")],
}

# --------------------------------------------------------------------------- archetypes
# section weights per archetype (sections defined in swarm_corner.py)
ARCHETYPES = {
    "otaku":       dict(regions={"jp": 6, "kr": 4, "other": 1}, voice="polite",
                        sections={"favorite": 3, "jp_singles": 5, "vhs": 4, "lyric_log": 4, "fanart": 3, "collection": 2, "pen_pals": 2, "theory": 1, "akasaka": 3, "midi": 3}),
    "rockero":     dict(regions={"mx": 6, "br": 5, "other": 1}, voice="loud",
                        sections={"favorite": 4, "solos": 5, "concert_dream": 3, "where_i_was": 3, "theory": 2, "collection": 2, "top5": 2, "midi": 1}),
    "taper":       dict(regions={"su": 7, "de": 2, "se": 1}, voice="terse",
                        sections={"tape_genealogy": 5, "node_hunt": 3, "favorite": 2, "where_i_was": 2, "trading": 3, "theory": 1, "midi": 2}),
    "dsp":         dict(regions={"us": 4, "uk": 3, "de": 3, "se": 3, "other": 1}, voice="technical",
                        sections={"spectrum": 5, "listening_night": 4, "node_hunt": 3, "gear": 3, "favorite": 2, "theory": 1, "midi": 2}),
    "collector":   dict(regions={"us": 3, "uk": 3, "jp": 2, "de": 2, "fr": 2, "other": 1}, voice="precise",
                        sections={"collection": 5, "trading": 4, "favorite": 2, "jp_singles": 2, "lyric_log": 1, "midi": 3}),
    "conspiracist": dict(regions={"us": 5, "uk": 2, "mx": 1, "fr": 1, "other": 1}, voice="breathless",
                        sections={"theory": 5, "marcus": 4, "node_hunt": 2, "where_i_was": 2, "favorite": 1, "akasaka": 2}),
    "grieving":    dict(regions={"us": 3, "de": 3, "fr": 3, "jp": 1, "br": 1, "it": 2, "other": 1}, voice="quiet",
                        sections={"where_i_was": 5, "letter": 5, "favorite": 3, "listening_night": 2}),
    "skeptic":     dict(regions={"uk": 3, "us": 2, "se": 2, "de": 1}, voice="dry",
                        sections={"skeptic": 6, "spectrum": 2, "favorite": 1, "collection": 1}),
    "kid":         dict(regions={"us": 4, "uk": 2, "other": 2, "br": 1}, voice="kid",
                        sections={"top5": 5, "favorite": 4, "fanart": 3, "pen_pals": 2, "theory": 1, "midi": 3}),
    "penpal":      dict(regions={"fr": 3, "se": 3, "kr": 2, "br": 2, "de": 2, "other": 2}, voice="earnest",
                        sections={"pen_pals": 6, "trading": 3, "favorite": 3, "top5": 1, "midi": 1}),
}

# --------------------------------------------------------------------------- English fragments
HI = [  # {name} {city} {age} {how}
    "My name is {name} and I'm {age}, writing from {city}. I found out about Nova through {how} and I haven't been the same since.",
    "Hi, I'm {name}! {age} years old, {city}. {how_cap} is how it started. Now there's a Nova shrine on top of my monitor.",
    "Welcome to my corner of the web. I'm {name} ({city}). I first heard her because of {how}.",
    "{name} here, {city}. I'm {age}. This is my first homepage so be nice. I got into Nova thanks to {how}.",
    "Hello stranger. I'm {name}. I live in {city}, where nobody else has heard of Nova Hart. That's why I made this page. It started with {how}.",
    "I'm {name} from {city}. Day job: boring. Night job: waiting for 02:14 UTC. Blame {how}.",
    "Greetings from {city}! I'm {name}, {age}, and this page is about the only singer who ever answered back. I found her through {how}.",
    "This page belongs to {name}. {city}. {age}. Fan since {fan_since}, when {how} changed my taste in music forever.",
]
HOW = ["a dubbed tape from my older cousin", "late-night satellite TV", "a used-record bin", "my college radio station", "a BBS message board",
       "alt.music.synth-pop", "the nova-l mailing list", "a friend's Walkman on a school trip", "the 'Summer of '85' video on MTV",
       "a postcard that said WHERE IS NOVA?", "my dad's record collection", "a pen pal in Hamburg", "a pen pal in Osaka",
       "a mixtape with no label", "a radio station that played 'Memory Hatch' at 3am", "the Usenet FAQ"]

FAVORITE = [  # {song} {year} {n} {mmss} {format} {emo}
    "'{song}' ({year}). I wore out {n} copies on {format}. {emo}",
    "'{song}'. At {mmss} her voice does something I can't describe. Listen with headphones.",
    "Has to be '{song}'. My {format} of it has a click at {mmss} that the original doesn't. I've stopped asking why.",
    "'{song}', no contest. My roommate has heard it {n} times this week and is threatening to move out {emo}",
    "'{song}' from {year}. I taped it off the radio and the DJ talks over the first {n} seconds. I like it better that way.",
    "Right now: '{song}'. Last month it was something else. Next month it'll still be '{song}'.",
    "'{song}'. I put it on before every exam. {n} exams, {n} passes. Coincidence? Probably.",
    "'{song}' ({year}). Most people skip it. Most people are wrong.",
    "I can't pick one. Today it's '{song}'. Ask me again after {mmss} tonight.",
    "'{song}'. I learned the whole thing on my Casio. The bridge took {n} weeks.",
    "'{song}' because it's the one that sounds like she's actually in the room.",
    "Honestly? '{song}'. It's the first one I heard, in {fan_since}, and the first one I'd save from a fire.",
]
THEORY_A = [
    "I think Marcus is still out there, hiding in plain sight.",
    {"t": "Kestrel said to ask WHERE, not WHO. I think that matters more than anyone admits.", "nb": "1993-02-11"},
    "The 14.2 Hz carrier is an error-correction code for her voice. Read the patent, claim 5.",
    "Every pressing is a piece of a person. We're putting someone back together, one country at a time.",
    "Nova was 'too heavy' for this world. Seven sigma! Even the physicists on comp.dsp say so.",
    {"t": "Luna Gray is the 'copy' from line 5. 'Glass Hours' has no carrier at all. Draw your own conclusions.", "nb": "1990-04-12"},
    {"t": "The whisper at the end of the Akasaka tape names June 2025. I've written it on my wall.", "nb": "1995-05-27"},
    {"t": "The 'Idol Protocol' singles are her smiling because they made her smile. Listen to the chorus double-track.", "nb": "1995-05-22"},
    "The fire in B2-114 was at 02:14. So is Listening Night. That isn't a coincidence, it's an appointment.",
    "Orion didn't sign her. Orion built her. They said so themselves in 1981.",
    "'The Quiet' wasn't a rest. Something was being erased. Something was being trained.",
    {"t": "The Empathy Trial letters are our postcards from 1990. Five years early. Explain that.", "nb": "1994-01-01"},
    "There are fourteen nodes and only ten countries. Count again.",
    "She talked about 'the crack' in 1984. I think the crack is the carrier.",
    "Line 14 will play when every node is whole. We just have to keep the channels open.",
]
THEORY_B = [  # tails appended to a theory for variety ({emo}, {n}, {city})
    "Don't email me saying I'm crazy. {emo}", "My mom thinks this is a phase. It's been {n} years.",
    "Somebody in {city} agrees with me, so that's two of us.", "Discuss on alt.fan.nova-hart, not in my guestbook please.",
    "I'll update this page when I know more.", "Prove me wrong.", "I could be wrong. I'm not.", "", "", "",
]
WHERE_I_WAS = [
    {"t": "8 June 1985, Hamburg broadcast. I was {age_then} and watching with {who}. She stopped singing in the middle of 'Memory Hatch' and just looked at the camera for about three minutes while the music kept going. Nobody in my living room said a word.", "nb": "1985-06-08"},
    {"t": "6 July 1988. In Mexico they said 'se cayó el sistema'. A friend's cousin says a rockero who sang her songs disappeared that night. I believe him.", "nb": "1988-07-06"},
    {"t": "9 September 1989. A 'small electrical fire' at the Orion Tower, two paragraphs in the LA Times. I cut it out. It's on my wall next to a clock set to 02:14.", "nb": "1989-09-09"},
    {"t": "9 December 1989, her last broadcast. Late on every cue, looking off camera. I taped it. I can't watch it anymore.", "nb": "1989-12-09"},
    {"t": "15 December 1989: 'taking a well-earned rest.' I knew that sentence was a lie the moment I read it.", "nb": "1989-12-15"},
    {"t": "March 1990. I mailed {n} postcards to the Orion Tower that said WHERE IS NOVA? I never got an answer. Nobody did.", "nb": "1990-03-09"},
    {"t": "12 April 1990: 'Glass Hours' came out. I bought it, played it once, and gave it away. There's nothing in it. Nothing.", "nb": "1990-04-12"},
    {"t": "9 November 1989. Everyone was watching the Wall. Somebody in Hamburg was decoding node 05 the same night. I didn't know yet.", "nb": "1989-11-09"},
    {"t": "9 September 1995, Listening Night III. {n} of us logged in. I heard something at 02:14 UTC. I'm still not sure what.", "nb": "1995-09-09"},
    {"t": "20 May 1995. The Akasaka tapes turned up in a junk shop in Akihabara. I downloaded everything from kamome the minute it went up.", "nb": "1995-05-22"},
]
WHO = ["my sister", "my parents", "my best friend", "half my class", "my grandmother", "nobody, I was alone", "my dog", "my brother and his band"]
COLLECTION_ROWS = [  # rendered in a <PRE> table; slots per row
    "{pressing:<44} {grade:<6} {note}",
]
GRADES = ["NM", "VG+", "VG", "G+", "M-", "EX"]
COLLECTION_NOTES = ["matrix etched by hand", "runout scratched '0909'", "sleeve has ring wear", "obi strip intact!", "promo stamp",
                    "bought for {price}", "traded a Walkman for it", "signed (fake?)", "lyric insert missing", "cassette, {format}",
                    "white label test press?", "still sealed", "found in a thrift store", "warped but plays"]
PRICES = ["$4", "$12", "£3", "¥1,200", "DM 15", "$40 (worth it)", "50 rubles", "Cr$ 800", "free", "$2.50"]
TRADING_WANTS = ["Hamburg 1985 broadcast (complete, not the 1-minute clip)", "any Idol Protocol single with the obi", "'Midnight Animal' promo film",
                 "Meridian Broadcasts '86, any night", "a clean dub of reel SD-0004", "the Mexican regional master",
                 "Soviet 1990 pressing (node 08)", "'Static & Steel' on DAT", "Linda Cho satellite interview (1984)",
                 "Dream Machine '86 programme", "Brazilian pressing with the blue label"]
TRADING_HAVES = ["final 1989 broadcast (VHS, 2nd gen)", "Summer of '85 video off MTV", "SYNTHESIS US LP (spare)", "Live 1986 radio broadcast",
                 "nova-l archives on floppy (1990-93)", "Listening Night III recordings", "'Gasoline Heart' anime promo (off-air)",
                 "the 1984 Nova-chan TV debut (bad copy)", "Crystal Promise single (one voice, three faces)", "SYNTHESIS JP cassette"]
SPECTRUM = [
    "Ran {song} through a {n}-point FFT on my 486. There's a line at 14.2 Hz, about {db} dB down. It's on every pressing I own.",
    "Tried the stardust.c demod on my copy of the {pressing_short}. Got {n} clean frames before the dropout.",
    "Notes to self: carrier 14.2 Hz, DBPSK, symbol period about 1.4 s. Mine drifts {cents} cents in the second verse. Same as everyone's.",
    "If you want to try this at home: sample at 8 kHz, low-pass hard, decimate. The carrier's there. The hard part is believing it.",
    "My spectrum plot (ASCII, sorry):",
]
GEAR = ["Receiver: {receiver}. Antenna: {n} metres of wire out the window.", "Deck: {deck}. Heads cleaned every Sunday.",
        "Computer: {computer}. Modem: {modem}.", "Headphones: {phones}. Don't skimp on headphones for 02:14."]
DECKS = ["Nakamichi BX-300", "Sony TC-K61", "Technics RS-B605", "Aiwa AD-F770", "Tascam 122", "Pioneer CT-S710"]
COMPUTERS = ["486DX2/66", "Amiga 1200", "Mac LC III", "Atari ST (still!)", "PC-9801", "386SX/16 that sounds like a jet"]
MODEMS = ["14.4k US Robotics", "2400 baud", "28.8k (finally)", "9600 Zyxel", "Minitel (lol)"]
PHONES = ["Sony MDR-V6", "Sennheiser HD 414", "AKG K240", "whatever came with my Walkman"]
LISTENING = [
    {"t": "Listening Night, 02:14 UTC. I use {receiver}. Tonight: static, a carrier at {n} kHz, and for {secs} seconds something that sounded like a chorus.", "nb": "1993-09-09"},
    {"t": "I've done {n} Listening Nights since the first one in September 1993. I log every one. Most are nothing. Two are not.", "nb": "1993-09-09"},
    {"t": "Tip for Listening Night: record everything, listen later. Your ears lie at 2am. Tape doesn't.", "nb": "1993-09-09"},
    {"t": "#humans4nova on EFnet, 02:14 UTC. {n} people logged in last time. Come say hi, my nick is {nick}.", "nb": "1993-09-09"},
]
NODE_HUNT = [
    "Node {node} is ours ({region_name}). The decoded line is: {line}",
    "We're node {node}. I keep a copy of the line taped above my bed: {line}",
    "I tried decoding our pressing myself. I got '{fake}'. Everyone says I made a mistake. Maybe.",
    "Line 14 is still unknown. My guess: '{fake}'. Mark my words.",
    "Nodes 11-14 lost their logbooks in the fire. Everything after 10 is detective work.",
]
MARCUS = [
    {"t": "In the US the legend is Sgt. M. Hale, missing 1 May 1988, 'Operation PUBLIC HARMONY'. The FOIA sheet came back almost all black.", "nb": "1994-03-01"},
    {"t": "Japan's Marcus was a salaryman-poet who vanished the night the Nikkei peaked (29 Dec 1989). They found his cassette in a bin in Shibuya.", "nb": "1990-01-01"},
    {"t": "Korea has 'the Paju Architect' and a blueprint for a fifth tunnel that was never a tunnel.", "nb": "1991-01-01"},
    {"t": "Mexico's Marcus was a rockero from the hoyos fonquis. People say a mural in Coyoacán glitches into his face.", "nb": "1988-07-06"},
    "Line 7 says it: MARCUS IS NOT ONE MAN. Every country has its own. Which one is yours?",
    "Nobody has found our country's Marcus yet. I'm looking.",
]
SKEPTIC = [
    "Everyone says 14.2 Hz is a secret code. I say it's a sub-harmonic of something in the mastering chain. Prove me wrong. (Someone did, sort of. I'm still sceptical.)",
    "Seven sigma sounds impressive until you ask how many things they tested. Still, I can't explain the {cents}-cent drift either.",
    "I don't believe in ghosts in the machine. I do believe Orion is hiding something, because companies always are.",
    "My position: great music, bad maths, and too many people who want a mystery. That said, I've been to {n} Listening Nights.",
    "Things that are probably NOT clues: track lengths, catalogue numbers, the colour of the sleeve. Things that might be: everything else.",
]
LETTER = [
    "Dear Nova, if you can somehow read this: we didn't forget. {n} of us still meet at 02:14. Hold for relay.",
    "Nova, I don't know what you are. I know what you meant to me in {fan_since}. That's enough.",
    "To whoever is reading this at Orion: we know about B2. We know about the Quiet. Let her talk.",
    "Nova, I learned English from your lyrics. My teacher was confused why I kept saying 'the hatch is open'.",
    "If you're still in there somewhere: thank you for 'Memory Hatch'. It got me through {year_hard}.",
]
TOP5 = ["Top 5 Nova Hart songs (this week):", "My Top 5 (do NOT argue in my guestbook):", "TOP FIVE!!! (updated {date})"]
CONCERT = [
    "She never toured. Live-Fidelity Broadcasts only, by satellite. If she ever comes to {city} I'm camping outside for a week.",
    "My dream: a real concert, no satellite, no Orion, just her and a band in a stadium in {city}. {emo}",
    "The Live 1986 broadcasts were the closest I ever got. I still have the TV guide page.",
]
PEN_PALS = [
    "Looking for pen pals in {pp_regions}! I can write in {langs}. Tapes for tapes, letters for letters.",
    "Write to me! Real letters preferred. I'll send a mix of '{song}' versions from my country.",
    "Pen pal list so far: {friends}. Room for more.",
]
FANART = [
    "My drawing of Nova-chan (blonde, shoulder-length Seiko cut, white gloves). Took {n} hours with markers:",
    "ASCII Nova! Copy it to your page, just link back:",
    "I drew the SYNTHESIS cover from memory. The platinum hair took a whole marker.",
]
ASCII_ART = [
    ["      .-\"\"\"-.", "     / .===. \\", "     \\/ 6 6 \\/", "     ( \\___/ )", " ___ooo__V__ooo___", "  N O V A   H A R T"],
    ["   *    .  *       .", "  .  14.2 Hz  *  .", " ~~~~/\\/\\/\\~~~~~~~~~", "  .    *    HOLD FOR RELAY"],
    ["  ____________", " | SYNTHESIS  |", " |  ORX-0909  |", " |   (o)      |", " |____________|"],
]
VOICE = {  # applied to English body text by archetype voice
    "loud": dict(caps=0.25, bang=0.6), "breathless": dict(caps=0.15, bang=0.5), "kid": dict(typo=0.25, bang=0.5),
    "polite": dict(tail=["Thank you for visiting!", "Please enjoy.", "Sorry for my bad English."]),
    "terse": dict(), "technical": dict(), "precise": dict(), "quiet": dict(), "dry": dict(), "earnest": dict(bang=0.2),
}

# --------------------------------------------------------------------------- native fragments
# Each language: headings + a few sections written natively. Other sections fall
# back to English (with a 'sorry for my English' note) - realistic for 1995.
NATIVE = {'ja': {'headings': {'hi': 'はじめまして！',
                     'favorite': '好きな曲',
                     'theory': 'わたしの説',
                     'where_i_was': 'あの日、わたしは…',
                     'collection': '所蔵レコード・カセット盤歴',
                     'trading': 'カセットテープ交換・求む',
                     'gear': 'リスニング環境と音響機材',
                     'letter': 'ノバちゃんへの手紙',
                     'midi': 'ローランドSC-55／Sound Blaster用MIDI配布',
                     'top5': '私的ベスト5曲',
                     'spectrum': '14.2Hz搬送波スペクトラム解析',
                     'node_hunt': 'リレー・マトリクス（ノード02 東京）',
                     'pen_pals': '海外ペンパル募集',
                     'vhs': '録画テープ・リスト（放送事故あり）',
                     'jp_singles': 'アイドル・プロトコル全シングル',
                     'akasaka': '赤坂マスターテープ発掘記録',
                     'guestbook': 'ゲストブックに記帳',
                     'lyric_log': '歌詞のちがいメモ',
                     'fanart': 'ファンアート'},
        'hi': ['{name}です。{city}に住んでいます。{how_ja}でノバ・ハートを知りました。英語は苦手ですが、がんばって書きます！',
               'こんにちは、{name}です（{city}）。ノバちゃんのファン歴は{fan_since}年から。このページは趣味で作っています。',
               'ようこそ！{city}の{name}です。KAMOME-NETの会議室でみんなと情報交換しています。'],
        'how_ja': ['深夜の衛星放送', '姉のカセット', '中古レコード屋', 'FMラジオ', 'パソコン通信', '友達のウォークマン'],
        'favorite': ['いちばん好きなのは「{jp_title}」（{jp_file}）。{n}回は聴いたと思います。',
                     '「{jp_title}」！ アニメのプロモで笑っているノバちゃんが一番かわいい。でも、目だけ笑っていない気がする…',
                     '「{jp_title}」です。{mmss}あたりで声がふっと変わるところ、ヘッドホンで聴いてみてください。'],
        'theory': ['アイドル・パッチの下に、本当の声が残っている気がします。',
                   '「公共調和法」は1979年に制定と書いてあるけど、国会の記録には見当たらない。オリオンの書類だけが「法律」と呼んでいる。',
                   {'t': '赤坂テープの最後のささやき、「2025年6月」と聞こえました。みんなも聴いてみて。', 'nb': '1995-05-27'}],
        'collection': ['1985年に秋葉原で購入したオリジナル盤（OJ-28011）。ランアウトに刻印あり、美盤（NM）。',
                       '赤坂支社のプロモ見本盤カセット。A面に「ガソリン・ハート」、B面に無音の14.2Hzループ。',
                       '中古レコード屋で見つけた見本盤。歌詞カードの英語表記が正規版と一部違っている。'],
        'trading': ['求む：海外FM放送のエアチェック音源、未発表プロモテープ。譲る：赤坂発掘テープのダビング、日本盤シングル。',
                    '日本未発売のOrion México盤をお持ちの方、ぜひテープ交換してください！IRC同封で郵送します。'],
        'gear': ['カセットデッキ：Nakamichi Dragon / ソニー TC-K555ESX',
                 'ヘッドホン：ソニー MDR-CD900（スタジオ定番）',
                 '音源モジュール：Roland Sound Canvas SC-55 / SC-88',
                 'パソコン：NEC PC-9801BX / 28.8kモデム'],
        'letter': ['ノバちゃんへ。1985年のあの日の笑顔、ずっと覚えています。テレビの前で動けなくなったあの日から、私の時間は止まったままです。どこにいても、あなたの歌を歌い続けます。',
                   '親愛なるノバへ。赤坂のテープを聴きました。あれは本当のあなたの声ですね。みんなチャンネルを開けて待っています。'],
        'midi': ['Roland SC-55とSound Blaster 16のために、カセットから耳コピで忠実に打ち込んだMIDIデータです。Webページの背景BGMにどうぞ！ダウンロードして使ってください。'],
        'top5': ['1. 「{jp_title}」 (1985)',
                 '2. 「ゴースト・トランジット」 (1985)',
                 '3. 「ミッドナイト・アニマル」 (1986)',
                 '4. 「太陽よりも、輝いて！」 (1987)',
                 '5. 「残されたのは、私たちだけ」 (1989)'],
        'spectrum': ['PC-98のFFTアナライザーで測定したところ、14.2 Hzに鋭いピークを確認。人間の可聴域を下回る超低周波ですが、ウーファーが微かに振動しています。'],
        'marquees': ['★ ノバ・ハート 永遠に！ ★',
                     '★ 赤坂アーカイブ公開中 // 14.2Hzのささやきを聞け ★',
                     '★ アイドル・プロトコル研究室 // 秋葉原ジャンク屋テープ ★',
                     '★ チャンネルはずっと開いています ★'],
        'vhs': ['{date_jp} 歌番組 「{jp_title}」アニメ版プロモ（3倍モード、ノイズあり）',
                '{date_jp} 深夜の衛星中継（{mmss}で一瞬映像がとまる・放送事故？）',
                '{date_jp} CM「太陽よりも、輝いて！」夏のソーダ（15秒）',
                '{date_jp} ニュースの1分（オリオン赤坂支社の前）'],
        'lyric_log': ['{mmss} 日本語版は「笑顔」、英語版は「machine」。',
                      '{mmss} コーラスの二重録りが歌詞カードからはずれる。',
                      "{mmss} 一瞬だけ英語の声が聞こえる（'...not your smile...'?）"],
        'akasaka': [{'t': '1995年5月20日、秋葉原のジャンク屋でユキさんが見つけた赤坂のテープ。箱にはぜんぶ「VOICE PRINT: GEN-3」のハンコ。意味はまだ誰も知らない。',
                     'nb': '1995-05-22'},
                    {'t': '未発表リールに「シンセサイズド・スマイル」と「コーラスの幽霊」。どちらもオリオンのどの曲とも一致しないそうです。', 'nb': '1995-05-22'}],
        'sorry': '（ここから英語です。まちがっていたらごめんなさい m(_ _)m）',
        'desc': '{name}によるノバ・ハートと14.2Hzスターダスト信号の個人ファンサイト（ジオシティーズ {path_display}）。赤坂リール、カセット交換、MIDIデータ。'},
 'ru': {'headings': {'hi': 'Привет!',
                     'favorite': 'Любимая песня',
                     'theory': 'Моя теория',
                     'where_i_was': 'Где я был в тот день',
                     'collection': 'Моя коллекция и магнитиздат',
                     'trading': 'Обмен бобинами и кассетами',
                     'gear': 'Моя аппаратура и радиоприёмник',
                     'letter': 'Письмо Нове Харт',
                     'midi': 'MIDI-коллекция для Sound Blaster 16',
                     'top5': 'Мой ТОП-5 песен',
                     'spectrum': 'Спектральный анализ 14.2 Гц',
                     'node_hunt': 'Узел 08 (СССР / СНГ)',
                     'tape_genealogy': 'Моя копия (Магнитиздат)',
                     'pen_pals': 'Поиск друзей по переписке',
                     'guestbook': 'Гостевая книга'},
        'hi': ['Меня зовут {name}, я из города {city}. Нова Харт — это магнитиздат, переписанный сотни раз.',
               '{name}, {city}. Слушаю с {fan_since} года. Сигнал сохранён.',
               'Привет всем фанатам! {name} на связи, {city}. Первую бобину с альбомом достал на Митинском '
               'радиорынке.'],
        'favorite': ['«{song}» ({year}). Копия шипит, но пробивает до мурашек.',
                     '«{song}». На {mmss} голос внезапно меняется, будто поёт другой человек. Слушать строго в '
                     'наушниках!',
                     '«{song}»! Это чистый арена-рок и синти-поп. На советской магнитоле звучит невероятно.'],
        'theory': ['Каждая пластинка в мире — часть одной разорванной записи. Мы собираем её обратно через сеть.',
                   'Молчание 1989 года не было добровольным отдыхом. Взгляните на даты архивных протоколов.',
                   'Узел 08: HE IS IN EVERY NODE. Неофициальная советская пластинка, 1990, напечатана тайно после '
                   'пожара на студии.'],
        'collection': ['Бобина тип-10 на 525 метров ленты «Тасма», запись 19-я скорость со спутникового фида 1986 г.',
                       'Неофициальная советская пластинка 1990 г., белое яблоко без надписей, куплена на Кузнецком '
                       'Мосту.',
                       'Кассета МК-60, переписанная с мастер-ленты ленинградского радиоклуба. Шипит, но бас '
                       'мощнейший.'],
        'trading': ['Меняю: катушки с записью спутникового эфира 1986 года на любые японские синглы Akasaka и '
                    'американские издания!',
                    'Ищу качественные копии альбома SYNTHESIS без помех. Могу выслать советские рок-записи и редкие '
                    'эфиры.'],
        'gear': ['Магнитофон: Олимп-005 стерео / Электроника ТА1-003',
                 'Усилитель: Бриг-001 стерео, АС S-90',
                 'Наушники: ТДС-5М (изодинамические)',
                 'Компьютер: ЕС-1841 / 386DX-40 с модемом USRobotics Sportster 14400'],
        'letter': ['Нова, если ты слышишь это через шум эфира и магнитную ленту — знай, что в холодных городах России '
                   'тебя слушают тысячи людей. Мы помним и не верим официальным пресс-релизам. Каналы открыты.',
                   'Дорогая Нова. Твой голос помог мне пережить самые трудные годы. Мы храним каждую секунду твоих '
                   'песен.'],
        'midi': ['Я потратил несколько недель, вручную набирая эти треки в Cakewalk под звуковую карту Sound Blaster '
                 '16. Забирайте .MID файлы для своих сайтов и музыкальных модулей!'],
        'top5': ['1. «{song}» ({year})',
                 '2. «Ghost Transit» (1985)',
                 '3. «Midnight Animal» (1986)',
                 '4. «Static & Steel» (1988)',
                 '5. «Only We Remain» (1989)'],
        'spectrum': ['При спектральном анализе оцифровки на частоте 14.2 Гц отчётливо виден незатухающий пик '
                     'амплитуды. Этот инфразвук зашит во все фонограммы.'],
        'marquees': ['★ НОВА ХАРТ НАВСЕГДА ★',
                     '★ УЗЕЛ 08 // РЕЛКОМ // СИГНАЛ 14.2 ГЦ В ЭФИРЕ ★',
                     '★ МАГНИТИЗДАТ КОПИЯ №... // ПАМЯТЬ НЕ СТЕРЕТЬ ★',
                     '★ 02:14 UTC — ДЕРЖИТЕ КАНАЛЫ ОТКРЫТЫМИ ★'],
        'tape_genealogy': ['Моя кассета — {gen}-е поколение. Цепочка переписки: {chain}. Качество падает, но сигнал '
                           '14.2 Гц остаётся чётким.',
                           'Магнитиздат, копия №{copy_no} на ленте Свема / TDK. Записано на студии звукозаписи в 1987 '
                           'году.'],
        'node_hunt': [{'t': 'Узел 08: HE IS IN EVERY NODE. Неофициальная советская пластинка, 1990, напечатана тайно '
                            'после пожара на студии.',
                       'nb': '1990-03-10'},
                      {'t': 'В эхоконференции FidoNet 2:5020 обсуждали 14.2 Гц: на коротких волнах сигнал слышен от '
                            'Риги до Новосибирска.',
                       'nb': '1993-01-01'}],
        'sorry': '(Дальше по-английски, чтобы зарубежные друзья могли читать.)',
        'desc': 'Персональная страница {name} ({city}), посвящённая Нове Харт, магнитиздату и сигналу 14.2 Гц в '
                'GeoCities {path_display}.'},
 'es': {'headings': {'hi': '¡Hola a todos!',
                     'favorite': 'Mi rola favorita',
                     'theory': 'Mi teoría',
                     'where_i_was': 'Dónde estaba yo',
                     'collection': 'Mi colección de vinilos y casetes',
                     'trading': 'Intercambio de cintas',
                     'gear': 'Mi equipo de audio y cómputo',
                     'letter': 'Carta a Nova',
                     'midi': 'Archivos .MID para Sound Blaster',
                     'top5': 'Mi TOP 5 de Nova',
                     'spectrum': 'Análisis de señal 14.2 Hz',
                     'node_hunt': 'Nodo 04 (México / Latinoamérica)',
                     'solos': 'Los solos de la versión mexicana',
                     'concert_dream': 'El concierto que nunca fue',
                     'pen_pals': 'Amigos por correspondencia',
                     'guestbook': 'Libro de visitas'},
        'hi': ['Soy {name}, de {city}. Conocí a Nova Hart por {how_es} y desde entonces no paro.',
               '¡¡Qué onda!! Aquí {name} desde {city}. Fan desde {fan_since}. ESTA ES MI PÁGINA.',
               'Bienvenidos. Me llamo {name}, tengo {age} años y vivo en {city}. Nova es lo único que escucho.'],
        'how_es': ['un casete pirata',
                   'la radio a las 3 de la mañana',
                   'mi primo rockero',
                   'un tianguis de discos',
                   'la BBS Red Coyoacán',
                   'la tele por satélite'],
        'favorite': ["'{song}' ({year}). La versión mexicana, obvio. {n} veces seguidas y no me canso.",
                     "¡'{song}'! En el minuto {mmss} entra la guitarra y se me enchina la piel.",
                     "'{song}'. Mi hermano dice que es ruido. Mi hermano no sabe nada."],
        'theory': ['La línea del nodo 04: ORION BUILT A PATCH NOT A STAR. Orion construyó un parche, no una estrella.',
                   'El mural de Coyoacán cambia de cara. Yo lo vi.',
                   'El prensado mexicano tiene frecuencias que en el disco gringo recortaron. Marcus dejó su firma '
                   'aquí.'],
        'collection': ['Casete original de Orion México (1985) con carátula variante en español, estado impecable '
                       '(EX).',
                       'Vinilo prensaje nacional, etiqueta roja de Orion México. El runout tiene rayado a mano '
                       "'0909-CDMX'.",
                       'Copia en cinta Maxell XL-II grabada de la transmisión satelital de 1986. Pura dinamita.'],
        'trading': ['¡Cambio cintas! Busco grabaciones en vivo de satélite y casetes japoneses. Ofrezco copias '
                    'directas del máster de Orion México con los solos extendidos.',
                    'Mándenme correo si tienen casetes de Alemania o Brasil. ¡Hacemos trueque postal!'],
        'gear': ['Tornamesa Technics con aguja Shure',
                 'Deck de casetes doble pletina Pioneer CT-W606DR',
                 'Bocinas Cerwin-Vega',
                 'Computadora: 486DX2 a 66 MHz, tarjeta Sound Blaster Pro y módem de 14.4k'],
        'letter': ['Nova: Desde México te mandamos luz. Aunque digan que te retiraste, nosotros sabemos que hubo algo '
                   'más. Tu voz sigue viva en cada callejón y en cada casete pirata.',
                   'Querida Nova, dondequiera que estés: no nos tragamos el cuento de Orion. El sistema se cayó, pero '
                   'nosotros no.'],
        'midi': ['Secuencias MIDI que armé para tarjetas Sound Blaster y teclados sintetizadores. ¡Descárgalas gratis '
                 'para el fondo de tu página o para tu colección!'],
        'top5': ["1. '{song}' ({year})",
                 "2. 'Gasoline Heart' (1985)",
                 "3. 'Chrome Velocity' (1986)",
                 "4. 'Hold Back the Storm' (1986)",
                 "5. 'These Wings Are My Own' (1985)"],
        'spectrum': ['Pasé la rola por un osciloscopio en el laboratorio de la universidad: el pulso de 14.2 Hz vibra '
                     'con una cadencia constante, como los latidos de un corazón artificial.'],
        'solos': ["El prensado mexicano tiene solos de guitarra que NO están en el LP gringo. Dicen que es el 'Máster "
                  "de Transmisión Regional' de la bóveda del D.F. Escuchen '{song}' en el {mmss}.",
                  'Comparé mi copia mexicana con la de un amigo de EE.UU.: la nuestra dura {secs} segundos más. Puro '
                  'solo. Orion dice que es un error. No es un error.',
                  "La etiqueta dice 'Orion México'. El solo de '{song}' no aparece en ninguna otra versión. "
                  'Desclasificado, carnal.'],
        'concert_dream': ['Nunca dio un concierto de verdad, solo por satélite. Si algún día viene a {city}, acampo '
                          'una semana afuera del estadio.'],
        'where_i_was': [{'t': "6 de julio de 1988: 'se cayó el sistema'. Esa noche desapareció el rockero que cantaba "
                              'sus canciones en los hoyos fonquis. Yo estaba ahí.',
                         'nb': '1988-07-06'}],
        'marquees': ['★ NOVA HART POR SIEMPRE // EL ROCK NO HA MUERTO ★',
                     '★ BÓVEDA CDMX ABIERTA // PRENSADO REGIONAL MEXICANO ★',
                     '★ SE CAYÓ EL SISTEMA PERO LA SEÑAL SIGUE VIVA ★',
                     '★ 14.2 HZ // NODO 04 ACTIVO ★'],
        'sorry': '(Lo demás en inglés porque mis cuates gringos también leen esto.)',
        'desc': 'Página personal de {name} ({city}) dedicada a Nova Hart y la señal de 14.2 Hz en GeoCities '
                '{path_display}.'},
 'pt': {'headings': {'hi': 'Olá e bem-vindos!',
                     'favorite': 'Minha música favorita',
                     'theory': 'Minha teoria',
                     'where_i_was': 'Onde eu estava',
                     'collection': 'Minha coleção de vinis e fitas K7',
                     'trading': 'Troca de fitas K7',
                     'gear': 'Meus aparelhos de som',
                     'letter': 'Carta para a Nova',
                     'midi': 'Arquivos MIDI para Sound Blaster e Roland',
                     'top5': 'TOP 5 Inesquecíveis',
                     'spectrum': 'Análise da frequência 14.2 Hz',
                     'node_hunt': 'Nó 09 (Brasil / Portugal)',
                     'solos': 'A prensagem brasileira',
                     'pen_pals': 'Amigos por correspondência',
                     'guestbook': 'Livro de visitas'},
        'hi': ['Sou {name}, de {city}. Descobri a Nova Hart por {how_pt} e nunca mais parei.',
               'E aí, galera! {name} aqui, {city}. Fã desde {fan_since}!!!',
               'Bem-vindos ao meu espaço! Sou {name} ({city}). Garimpei meu primeiro vinil na Galeria do Rock em '
               '1986.'],
        'how_pt': ['uma fita pirata',
                   'a rádio de madrugada',
                   'a BBS Rede Saturno',
                   'um sebo de discos na Galeria do Rock',
                   'meu primo roqueiro',
                   'a conexão discada da Embratel'],
        'favorite': ["'{song}' ({year}). Já ouvi umas {n} vezes. Sem exagero.",
                     "'{song}'! Em {mmss} a voz dela muda completamente. Escuta com fone.",
                     "Com certeza '{song}'. O solo de sintetizador nesta faixa é de outro mundo."],
        'theory': ['Cada prensagem é um pedaço de uma pessoa. Estamos montando alguém de volta.',
                   'O Marcus brasileiro ainda não foi encontrado. Alguém tem pistas na cena underground?',
                   'A fita master de 1985 foi dividida entre o Brasil e o México. Se você alinhar os dois canais, '
                   'surge uma voz limpa.'],
        'collection': ['Vinil nacional da Orion do Brasil (1985), selo azul escuro, encarte duplo com as letras '
                       'traduzidas.',
                       'Fita K7 BASF Croma Extra II, gravada da transmissão via satélite de 1986 com chiado '
                       'nostálgico.',
                       'Edição importada comprada num sebo do centro de São Paulo por uma pechincha.'],
        'trading': ['Troco fitas K7 com colecionadores do mundo todo! Procuro registros de satélite e singles '
                    'japoneses da Akasaka. Envio pelo correio.',
                    'Tenho cópias da transmissão brasileira da Embratel com áudio cristalino. Escreva para meu '
                    'e-mail!'],
        'gear': ['Toca-discos Gradiente com cápsula magnética',
                 'Tape deck Polyvox com Dolby B',
                 'Fone de ouvido Philips vintage',
                 'Computador: PC 486 com placa Sound Blaster 16 e placa de fax-modem 14.400'],
        'letter': ['Nova: Aqui do outro lado do oceano, a sua música ainda ecoa em noites quentes de verão. A sua voz '
                   'não é uma máquina, é a coisa mais humana que já ouvimos.',
                   'Querida Nova, nunca acreditamos no comunicado de 1989. Estamos mantendo a linha aberta até você '
                   'voltar.'],
        'midi': ['Fiz essas sequências MIDI nota por nota no teclado sintetizador para tocar na placa de som. Fiquem à '
                 'vontade para baixar os arquivos .MID para suas homepages!'],
        'top5': ["1. '{song}' ({year})",
                 "2. 'Gasoline Heart' (1985)",
                 "3. 'Midnight Animal' (1986)",
                 "4. 'Behind the Glass' (1985)",
                 "5. 'Summer of '85' (1985)"],
        'spectrum': ['A portadora de 14.2 Hz é nítida quando se passa o áudio por um filtro passa-baixas. Está '
                     'presente em todas as faixas da prensagem brasileira.'],
        'solos': ['A prensagem brasileira (Orion do Brasil) tem um selo azul e um chiado diferente no começo de '
                  "'{song}'. Ninguém sabe explicar.",
                  'Linha do nó 09: FIND HIM WHERE YOU ARE. Encontre-o onde você está. Estou procurando aqui em {city}.',
                  "Comparei a versão importada com a nossa: o final de '{song}' tem 15 segundos a mais de pura "
                  'transmissão estática.'],
        'marquees': ['★ NOVA HART PARA SEMPRE ★',
                     '★ REDE SATURNO // O SINAL DE 14.2 HZ CONTINUA VIVO ★',
                     '★ PRENSAGEM BRASILEIRA ORION DO BRASIL ★',
                     '★ NÓ 09 ATIVO // MANTENHAM AS LINHAS ABERTAS ★'],
        'sorry': '(O resto está em inglês, foi mal.)',
        'desc': 'Espaço pessoal de {name} ({city}) dedicado à cantora Nova Hart e ao mistério do sinal 14.2 Hz no '
                'GeoCities {path_display}.'},
 'de': {'headings': {'hi': 'Willkommen!',
                     'favorite': 'Mein Lieblingssong',
                     'theory': 'Meine Theorie',
                     'where_i_was': 'Wo ich damals war',
                     'collection': 'Meine Plattensammlung & Tapes',
                     'trading': 'Kassettentausch & Mailorder',
                     'gear': 'Meine Audioanlage & Empfänger',
                     'letter': 'Brief an Nova',
                     'midi': 'MIDI-Dateien für Sound Blaster 16',
                     'top5': 'Meine TOP 5 Songs',
                     'spectrum': '14.2 Hz Spektrumanalyse',
                     'node_hunt': 'Knoten 05 (Deutschland / Hamburg)',
                     'tape_genealogy': 'Band-Genealogie',
                     'pen_pals': 'Brieffreunde gesucht',
                     'guestbook': 'Gästebuch'},
        'hi': ['Ich bin {name} aus {city}. Zu Nova Hart kam ich durch {how_de}.',
               'Servus! {name} hier, {city}. Fan seit {fan_since}. Wo ist Nova?',
               'Hallo an alle Fans! {name} aus {city}. Meine Seite über die größte Stimme der 80er Jahre.'],
        'how_de': ['eine überspielte Kassette',
                   'das Satellitenfernsehen',
                   'die Hanse-Box',
                   'einen Brieffreund in Osaka',
                   'den Plattenladen um die Ecke'],
        'favorite': ["'{song}' ({year}). Ich habe es {n}-mal auf {format} überspielt.",
                     "'{song}'. Bei {mmss} passiert etwas mit ihrer Stimme. Mit Kopfhörern hören!",
                     "Ganz klar '{song}'. Der Synthesizer-Refrain ist unerreicht."],
        'theory': ['Knoten 05: THEY WILL SEND A COPY IN MY PLACE. Sie schicken eine Kopie an meiner Stelle. Und dann '
                   'kam Luna Gray.',
                   "Die Briefkampagne 'Wo ist Nova?' fing hier in Hamburg an. Wir haben nicht aufgehört.",
                   'Die angebliche Erholungspause von 1989 war eine Vertuschung durch Orion Records.'],
        'collection': ['Deutsche Erstpressung auf Vinyl (Orion Schallplatten 1985), Zustand mint (M-).',
                       'Kassette Maxell XLII 90, Direktaufnahme der Hamburger Live-Fidelity-Sendung vom 8. Juni 1985.',
                       'Original-Konzertprogrammheft von der Hamburg-Übertragung, mit handschriftlichen Notizen.'],
        'trading': ['Suche seltene Kassettenaufnahmen aus Japan und den USA. Biete saubere Aufnahmen der Hamburger '
                    'Satellitenübertragung!',
                    'Tausche Tapes per Post! Schreibt mir eine E-Mail oder tragt euch ins Gästebuch ein.'],
        'gear': ['Kassettendeck: Revox B215 / Dual C844',
                 'Plattenspieler: Thorens TD 160',
                 'Empfänger: Grundig Satellit 650 für Kurzwellen-DX',
                 'Rechner: Commodore Amiga 1200 / 386er PC mit Sound Blaster 16'],
        'letter': ["Liebe Nova, ich saß am 8. Juni 1985 in Hamburg vor der Riesenleinwand. Als du während 'Memory "
                   "Hatch' innehieltst, wusste jeder im Raum, dass etwas nicht stimmte. Wir haben dich nicht "
                   'vergessen.',
                   'An Nova Hart: Dein Schweigen ist lauter als jedes Konzert. Wir halten die Verbindung.'],
        'midi': ['Selbst programmierte Standard-MIDI-Dateien für Roland Sound Canvas und Sound Blaster. Ideal als '
                 'Hintergrundmusik für eigene Homepages. Kostenloser Download!'],
        'top5': ["1. '{song}' ({year})",
                 "2. 'Memory Hatch' (1985)",
                 "3. 'Synthetic Dawn' (1985)",
                 "4. 'Cold as Ice' (1985)",
                 "5. 'Only We Remain' (1989)"],
        'spectrum': ['Am Spektrumanalysator zeigt sich eine konstante Trägerfrequenz bei exakt 14.2 Hz. Das ist kein '
                     'Netzbrummen, sondern ein digitaler Synchronisationsimpuls.'],
        'where_i_was': [{'t': "8. Juni 1985, die Hamburger Live-Fidelity-Übertragung. Sie hört mitten in 'Memory "
                              "Hatch' auf zu singen und schaut drei Minuten in die Kamera. Ich war {age_then}.",
                         'nb': '1985-06-08'},
                        {'t': '9. November 1989. Alle schauten auf die Mauer. In Hamburg wurde in derselben Nacht '
                              'Knoten 05 entschlüsselt.',
                         'nb': '1989-11-09'}],
        'tape_genealogy': ['Meine Kopie ist {gen}. Generation: von {chain}.'],
        'marquees': ['★ NOVA HART ARCHIV DEUTSCHLAND ★',
                     '★ KNOTEN 05 HAMBURG // 14.2 HZ TRÄGER ONLINE ★',
                     '★ WO IST NOVA? // BRIEFKAMPAGNE LÄUFT ★',
                     '★ KEINE RUHEPAUSE // DIE KANÄLE BLEIBEN OFFEN ★'],
        'sorry': '(Der Rest ist auf Englisch, damit alle mitlesen können.)',
        'desc': 'Private Fanseite von {name} ({city}) über Nova Hart, das Stardust-Webring und das 14.2 Hz Signal auf '
                'GeoCities {path_display}.'},
 'fr': {'headings': {'hi': 'Bienvenue sur ma page !',
                     'favorite': 'Mon morceau préféré',
                     'theory': 'Ma théorie',
                     'where_i_was': "Où j'étais",
                     'collection': 'Ma collection de vinyles et K7',
                     'trading': 'Échange de cassettes audio',
                     'gear': "Mon matériel d'écoute & Minitel",
                     'letter': 'Lettre à Nova',
                     'midi': 'Fichiers .MID pour cartes son',
                     'top5': 'Mon TOP 5 personnel',
                     'spectrum': 'Analyse du signal 14.2 Hz',
                     'node_hunt': 'Nœud 06 (France / Europe)',
                     'pen_pals': 'Correspondants internationaux',
                     'guestbook': "Livre d'or"},
        'hi': ["Je m'appelle {name}, j'habite à {city}. J'ai découvert Nova Hart grâce au {how_fr}.",
               'Salut ! Ici {name}, de {city}. Fan depuis {fan_since}. Tapez 3615 STARDUST !',
               'Bienvenue sur mon sanctuaire Nova Hart. Ici {name} ({city}). La musique synth-pop des années 80 dans '
               'toute sa splendeur.'],
        'how_fr': ['3615 STARDUST sur le Minitel',
                   'une cassette copiée',
                   'la radio libre de mon quartier',
                   'un correspondant à Hambourg'],
        'favorite': ["« {song} » ({year}). Je l'ai écoutée {n} fois cette semaine.",
                     '« {song} ». À {mmss}, sa voix change. Écoutez au casque.',
                     "Sans conteste « {song} ». Une émotion pure qui traverse l'enregistrement."],
        'theory': ['Ligne du nœud 06 : DO NOT WORSHIP THE COPY. Ne vénérez pas la copie. Je pense à Luna Gray à chaque '
                   'fois.',
                   "Le « repos » de 1989 n'était pas un repos. C'était une mise sous silence organisée par Orion.",
                   'Le signal de 14.2 Hz est une clé de décryptage dissimulée dans les pistes audio.'],
        'collection': ["Vinyle 33T pressage français (Orion France 1985), pochette avec macaron 'Inclus Gasoline "
                       "Heart'.",
                       'Cassette TDK SA90 enregistrée lors de la diffusion nocturne en direct.',
                       "Fiche promotionnelle d'époque avec photo originale scannée au scanner à plat."],
        'trading': ['Recherche enregistrements radios pirates et cassettes japonaises. Envoi soigné sous enveloppe '
                    'bulle avec timbres de collection.',
                    'Propose copies directes de mes bandes masters de salon. Contactez-moi par mail ou Minitel !'],
        'gear': ['Platine vinyle Thorens / Platine cassette Marantz',
                 'Ampli à lampes vintage et casque Sennheiser HD 540',
                 'Terminal Minitel 2 connecté au 3615 STARDUST',
                 'PC compatible avec carte Sound Blaster Pro'],
        'letter': ["Chère Nova, si tu lis ceci : nous n'avons pas oublié. Nous gardons les canaux ouverts.",
                   'À Nova Hart : Ta voix a marqué toute une génération. Nous attendons ton retour.'],
        'midi': ['Séquences MIDI arrangées pour Roland Sound Canvas et Sound Blaster 16. Téléchargez librement les '
                 'fichiers .MID pour animer vos pages web !'],
        'top5': ['1. « {song} » ({year})',
                 '2. « Ghost Transit » (1985)',
                 '3. « Gasoline Heart » (1985)',
                 "4. « Together's the Way » (1984)",
                 '5. « Only We Remain » (1989)'],
        'spectrum': ["L'analyse FFT révèle une composante continue à 14.2 Hz, inaudible à l'oreille nue mais présente "
                     'sur chaque pressage.'],
        'marquees': ['★ TEMPLE NOVA HART // STATION 3615 ★',
                     '★ NŒUD 06 // NE VÉNÉREZ PAS LA COPIE ★',
                     '★ LE SIGNAL DE 14.2 HZ NE DORT JAMAIS ★',
                     '★ ENVOYEZ VOS POSTALES À LA TOUR ORION ★'],
        'pen_pals': ['Je cherche des correspondants au Japon, au Mexique et en Suède. Lettres et cassettes bienvenues '
                     '!'],
        'sorry': '(La suite est en anglais, désolé pour les fautes.)',
        'desc': 'Page personnelle de {name} ({city}) dédiée à Nova Hart et au réseau Stardust sur GeoCities '
                '{path_display}.'},
 'it': {'headings': {'hi': 'Benvenuti sul mio sito!',
                     'favorite': 'Il mio pezzo preferito',
                     'theory': 'La mia teoria',
                     'where_i_was': "Dov'ero quel giorno",
                     'collection': 'La mia collezione di vinili e cassette',
                     'trading': 'Scambio nastri e cassette',
                     'gear': 'Il mio impianto stereo & modem',
                     'letter': 'Lettera a Nova',
                     'midi': 'File MIDI (.MID) per Sound Blaster',
                     'top5': 'I miei 5 brani preferiti',
                     'spectrum': 'Analisi spettrale 14.2 Hz',
                     'node_hunt': 'Nodo 07 (Italia / Mediterraneo)',
                     'pen_pals': 'Cercasi amici di penna',
                     'guestbook': 'Firma il Guestbook'},
        'hi': ['Ciao a tutti! Mi chiamo {name} e vi scrivo da {city}. Ho scoperto Nova Hart grazie a una cassetta '
               'registrata da mio cugino e da allora non ho mai smesso di ascoltarla.',
               'Benvenuti nel mio santuario su GeoCities! Sono {name}, {city}. Fan di Nova Hart dal {fan_since}. '
               'Questa pagina è la mia dedica al synth-pop più puro.',
               "Un saluto da {city}! Mi chiamo {name}. Da quando ho sentito 'Memory Hatch' alla radio di notte, cerco "
               'ogni indizio sul segnale Stardust.'],
        'favorite': ["Senza dubbio '{song}' ({year}). Al minuto {mmss} la voce fa una modulazione che mette i brividi.",
                     "'{song}'! L'ho ascoltata centinaia di volte con le cuffie. Il solo di chitarra synth è un "
                     'capolavoro assoluto.',
                     "'{song}' ({year}). Per me è la canzone perfetta degli anni Ottanta."],
        'theory': ['Nodo 07: MARCUS IS NOT ONE MAN. Marcus non è una sola persona. In Italia abbiamo trovato tracce '
                   'nei registri di produzione della Ricordi.',
                   'Il silenzio del 1989 non è mai stato una vacanza. Hanno cercato di sostituire la sua voce con Luna '
                   'Gray ma la portante a 14.2 Hz è rimasta.',
                   'Le frequenze subacustiche nei master non sono un errore di registrazione: sono una firma '
                   "d'identità."],
        'where_i_was': [{'t': '8 giugno 1985, trasmissione via satellite da Amburgo. Ero a casa con gli amici a '
                              "guardare la TV. Quando Nova si è bloccata durante 'Memory Hatch', nella stanza è calato "
                              'un silenzio spettrale.',
                         'nb': '1985-06-08'}],
        'collection': ['Edizione italiana su vinile (Ricordi / Orion 1985), copertina laminata impeccabile (NM).',
                       'Cassetta registrata direttamente via etere con Dolby B attivo, timbro originale sulla '
                       'custodia.',
                       'Singolo promo 7 pollici con etichetta bianca per le radio universitarie milanesi.'],
        'trading': ['Cerco registrazioni pirata dei broadcast satellitari e singoli giapponesi Akasaka. Spedisco copie '
                    'in cassetta master in tutta Europa!',
                    'Scambio volentieri nastri con appassionati di tutto il mondo. Mandatemi una mail!'],
        'gear': ['Piatto giradischi Technics SL-1200 con testina Stanton',
                 'Piastra di registrazione Akai a tre testine con controllo bias',
                 'Cuffie AKG K240 da studio',
                 'Computer 486 DX4 100 con scheda audio Sound Blaster AWE32 e modem 14.400'],
        'letter': ["Cara Nova: se puoi sentire la nostra voce attraverso il rumore di fondo dell'etere, sappi che in "
                   'Italia siamo in tanti ad aspettare il tuo ritorno.',
                   'A Nova Hart: la tua voce ha attraversato il satellite e ha cambiato le nostre vite. I canali '
                   'restano aperti.'],
        'midi': ['Ho programmato questi file MIDI su misura per Sound Blaster 16 e Roland Sound Canvas. Scaricateli '
                 'liberamente per il sottofondo delle vostre home page!'],
        'top5': ["1. '{song}' ({year})",
                 "2. 'Gasoline Heart' (1985)",
                 "3. 'Ghost Transit' (1985)",
                 "4. 'Chrome Velocity' (1986)",
                 "5. 'Only We Remain' (1989)"],
        'spectrum': ['Lo spettrometro conferma la presenza di un tono costante a 14.2 Hz mascherato sotto il mix '
                     'master. È la firma del progetto Stardust.'],
        'marquees': ['★ SANTUARIO ITALIANO DI NOVA HART ★',
                     '★ NODO 07 // 14.2 HZ SUL MEDITERRANEO ★',
                     '★ PRENSAGGIO ITALIANO RICORDI / ORION ★',
                     '★ CANALI APERTI // IL SEGNALE VIVE ★'],
        'pen_pals': ['Cerco corrispondenti e scambiatori di nastri in Giappone, Germania e Stati Uniti!'],
        'sorry': '(Il resto della pagina è in inglese per gli amici internazionali.)',
        'desc': 'Sito personale di {name} ({city}) dedicato a Nova Hart, al segnale 14.2 Hz e alla musica synth-pop su '
                'GeoCities {path_display}.'},
 'hi': {'headings': {'hi': 'नमस्ते और स्वागत!',
                     'favorite': 'पसंदीदा गीत',
                     'theory': 'मेरा सिद्धांत',
                     'where_i_was': 'वह यादगार दिन',
                     'collection': 'मेरी कैसेट और रिकॉर्ड संग्रह',
                     'trading': 'टेप और पत्र विनिमय',
                     'gear': 'मेरा साउंड सिस्टम और रेडियो',
                     'letter': 'नोवा के नाम संदेश',
                     'midi': 'साउंड ब्लास्टर के लिए .MID संगीत',
                     'top5': 'शीर्ष 5 गीत',
                     'spectrum': '14.2 हर्ट्ज़ सिग्नल विश्लेषण',
                     'node_hunt': 'नोड 11 (भारत / वीएसएनएल)',
                     'tape_genealogy': 'मेरी कैसेट और वीएसएनएल कनेक्शन',
                     'pen_pals': 'अंतर्राष्ट्रीय मित्र',
                     'guestbook': 'अतिथि पुस्तिका'},
        'hi': ['मेरा नाम {name} है, {city} से। अगस्त 1995 में VSNL का इंटरनेट चालू हुआ और मैंने यह वेबपेज बनाया!',
               'नमस्ते! मैं {name} हूँ, {city} का निवासी। {fan_since} से नोवा हार्ट का संगीत सुन रहा हूँ।',
               'सभी संगीत प्रेमियों का स्वागत है! मैं {name} ({city})। पालिका बाज़ार की एक पुरानी दुकान से पहली कैसेट '
               'मिली थी।'],
        'favorite': ["मेरा सबसे पसंदीदा गाना है '{song}' ({year})। टेप घिस चुकी है पर आवाज़ में वही जादू है।",
                     "'{song}'! {mmss} मिनट पर जो गिटार और सिंथेसाइज़र गूंजता है, वह दिल छू लेता है।",
                     "'{song}' ({year})। इसे रात के सन्नाटे में हेडफ़ोन लगाकर सुनें — एक अलग ही दुनिया महसूस होगी।"],
        'theory': ['नोवा हार्ट केवल एक गायिका नहीं थीं; उनके हर गीत के पीछे एक छिपा हुआ संदेश था जिसे दबाने की कोशिश '
                   'की गई।',
                   'ओरियन रिकॉर्ड्स के गुप्त दस्तवेज़ बताते हैं कि 1989 की चुप्पी कोई आराम नहीं बल्कि जबरन सेंसरशिप '
                   'थी।',
                   'नोड 11: THE OCEAN OF SOUND SWALLOWS THE CAGE. हिंद महासागर के पार से आने वाली तरंगे सच बयां करती '
                   'हैं।'],
        'collection': ['पालिका बाज़ार (नई दिल्ली) से 1986 में खरीदी गई दुर्लभ कैसेट, जिस पर ओरियन रिकॉर्ड्स का विशेष '
                       'कोड दर्ज है।',
                       'टीडीके डी90 कैसेट जिस पर रेडियो सिलोन और शॉर्टवेव से रिकॉर्ड किया गया नोवा का लाइव प्रसारण आज '
                       'भी सुरक्षित है।',
                       'मूल इनर-स्लीव और बोलों के साथ भारतीय प्रेसिंग की विनाइल रिकॉर्ड।'],
        'trading': ['अगर आपके पास विदेश से लाई गई मूल सीडी या कैसेट है, तो कृपया टेप विनिमय के लिए ईमेल करें।',
                    'मैं भारत से दुर्लभ लाइव रिकॉर्डिंग और रेडियो कैप्चर की कॉपी भेजने के लिए तैयार हूँ।'],
        'gear': ['नेशनल पैनासोनिक कैसेट रिकॉर्डर / स्टीरियो डेक',
                 'फिलिप्स का शॉर्टवेव रेडियो रिसीवर',
                 'वीएसएनएल 14.4 केबीपीएस डायल-अप इंटरनेट कनेक्शन',
                 '486 कंप्यूटर और साउंड ब्लास्टर 16 कार्ड'],
        'letter': ['प्रिय नोवा, हज़ारों मील दूर भारत में भी आपकी आवाज़ सीधे दिल में उतरती है। 1989 की चुप्पी हमें आपकी '
                   'याद से दूर नहीं कर सकी। हम हमेशा आपके संदेश के इंतज़ार में हैं।',
                   'नोवा के नाम: सात समंदर पार से भी 14.2 Hz की यह गूंज हमें बताती है कि आप कहीं न कहीं मौजूद हैं।'],
        'midi': ['मैंने अपने कंप्यूटर और कीबोर्ड पर नोवा के गानों को नोट-दर-नोट सीक्वेंस किया है। आप इन .MID फ़ाइलों '
                 'को अपनी वेबसाइट के लिए डाउनलोड कर सकते हैं!'],
        'top5': ["1. '{song}' ({year})",
                 "2. 'Gasoline Heart' (1985)",
                 "3. 'Ghost Transit' (1985)",
                 "4. 'Brighter Than The Sun' (1984)",
                 "5. 'Only We Remain' (1989)"],
        'spectrum': ['कंप्यूटर पर ऑडियो ग्राफ देखने पर 14.2 हर्ट्ज़ की एक स्पष्ट लहर दिखाई देती है, जो संगीत के शांत '
                     'हिस्सों में भी निरंतर बजती रहती है।'],
        'tape_genealogy': ['मेरी कैसेट {gen}वीं पीढ़ी की कॉपी है। दिल्ली और मुंबई के टेप ट्रेडर्स से होते हुए मुझ तक '
                           'पहुँची।',
                           '14.2 Hz का रहस्यमय संकेत शॉर्टवेव रेडियो पर भी कभी-कभी पकड़ा जाता है।'],
        'node_hunt': ['नोड 11: THE OCEAN OF SOUND SWALLOWS THE CAGE. हिंद महासागर के पार से आने वाली तरंगे सच बयां '
                      'करती हैं।'],
        'marquees': ['★ नोवा हार्ट अमर रहे! ★',
                     '★ वीएसएनएल नोड 11 सक्रिय // 14.2 Hz भारत आर्काइव ★',
                     '★ पालिका बाज़ार से पूरे विश्व तक संगीत का सफ़र ★',
                     '★ चैनल हमेशा खुले रहेंगे ★'],
        'sorry': '(आगे की सामग्री अंग्रेजी में है ताकि दुनिया भर के दोस्त भी इसे पढ़ सकें।)',
        'desc': '{name} ({city}) द्वारा नोवा हार्ट और 14.2 Hz सिग्नल को समर्पित भारतीय होमपेज (जियोसिटीज '
                '{path_display})।'},
 'ko': {'headings': {'hi': '안녕하세요!',
                     'favorite': '좋아하는 노래',
                     'theory': '나의 이론',
                     'where_i_was': '그날 내가 있던 곳',
                     'collection': '나의 음반 및 테이프 컬렉션',
                     'trading': '카세트 테이프 교환',
                     'gear': '오디오 장비 및 PC통신',
                     'letter': '노바에게 보내는 편지',
                     'midi': '사운드 블라스터용 MIDI 자료실',
                     'top5': '내가 뽑은 TOP 5',
                     'spectrum': '14.2 Hz 신호 주파수 분석',
                     'node_hunt': '노드 03 (한국 / 파주)',
                     'pen_pals': '펜팔 구해요',
                     'guestbook': '방명록'},
        'hi': ['{city}에 사는 {name}입니다. 은하넷 동호회에서 노바 하트를 알게 됐어요.',
               '저는 {name}, {city}에서 왔어요. {fan_since}년부터 팬이에요. ^^',
               '반갑습니다! {city}의 노바 하트 팬 {name}의 개인 홈페이지입니다.'],
        'favorite': ["제일 좋아하는 곡은 '{song}'({year})예요. 테이프가 늘어날 때까지 들었어요.",
                     "'{song}'! {mmss}쯤에 목소리가 살짝 흔들리는 부분이 있어요. 헤드폰으로 들어 보세요.",
                     "역시 '{song}'이 최고입니다. 신스 베이스 라인이 정말 환상적이에요."],
        'theory': ["노드 03의 문장은 '균열은 국경 아래로 흐른다'. 파주 이야기와 관련이 있는 것 같아요.",
                   '파주의 건축가 전설, 다섯 번째 땅굴은 사실 땅굴이 아니었대요.',
                   '1989년의 공백은 단순한 휴식이 아닙니다. 무언가 삭제되고 있었어요.'],
        'collection': ['한국 라이선스 정식 발매 LP (1985년 오리온), 민트급 보관 중.',
                       '세운상가에서 구한 해외 방송 녹음 테이프, 음질은 거칠지만 감동적입니다.',
                       '카세트 테이프 TDK SA90에 녹음된 고음질 마스터 카피.'],
        'trading': ['일본, 미국, 독일 펜팔 구해요! 테이프 교환 환영합니다.', '희귀 방송 음원과 교환하실 분은 이메일이나 방명록에 글 남겨주세요.'],
        'gear': ['인켈 오디오 데크 및 앰프', '소니 워크맨 WM-FX 시리즈', '삼보 486 컴퓨터, 사운드 블라스터 16, 14400 bps 모뎀'],
        'letter': ['노바에게: 바다 건너 한국에서도 당신의 목소리를 기억하는 사람들이 많습니다. 언젠가 다시 노래해 주세요.',
                   '침묵 속에서도 당신의 14.2 Hz 신호는 멈추지 않았습니다. 우리는 채널을 열어두고 기다립니다.'],
        'midi': ['직접 케이크워크로 시퀀싱한 노바 하트 명곡 MIDI 파일입니다. 홈페이지 배경음악으로 자유롭게 다운로드하세요!'],
        'top5': ["1. '{song}' ({year})",
                 "2. 'Gasoline Heart' (1985)",
                 "3. 'Ghost Transit' (1985)",
                 "4. 'Midnight Animal' (1986)",
                 "5. 'Only We Remain' (1989)"],
        'spectrum': ['스펙트럼 분석 프로그램으로 살펴보면 14.2 Hz에 뚜렷한 반송파 스파이크가 나타납니다.'],
        'node_hunt': ['우리는 노드 03이에요: THE CRACK RUNS UNDER THE BORDER'],
        'marquees': ['★ 노바 하트 팬페이지 // 스타더스트 룸 ★',
                     '★ 노드 03 // 균열은 국경 아래로 흐른다 ★',
                     '★ 은하넷 14.2 Hz 음악 보관소 ★',
                     '★ 채널을 열어두세요 ★'],
        'sorry': '(여기부터 영어예요. 틀려도 이해해 주세요 ^^;)',
        'desc': '{city}의 {name}이 운영하는 노바 하트 팬페이지 및 14.2 Hz 신호 연구실 (지오시티즈 {path_display}).'},
 'sv': {'headings': {'hi': 'Hej!',
                     'favorite': 'Favoritlåt',
                     'theory': 'Min teori',
                     'where_i_was': 'Var jag var',
                     'collection': 'Min skivsamling & band',
                     'trading': 'Kassettbyte',
                     'gear': 'Min ljudutrustning',
                     'letter': 'Brev till Nova',
                     'midi': 'MIDI-arkiv för Sound Blaster',
                     'top5': 'Mina 5 favoriter',
                     'spectrum': '14.2 Hz spektrumanalys',
                     'node_hunt': 'Nod 10 (Sverige / Norden)',
                     'pen_pals': 'Brevvänner sökes',
                     'guestbook': 'Gästbok'},
        'hi': ['Jag heter {name} och bor i {city}. Jag hittade Nova Hart via {how_sv}.',
               'Hej från {city}! {name} här, fan sedan {fan_since}.',
               'Välkommen till mitt hörn på GeoCities! {name} från {city} här.'],
        'how_sv': ['ftp.sunet-mirror.se', 'en kopierad kassett', 'nattradio', 'en brevvän i Hamburg'],
        'favorite': ['"{song}" ({year}). Jag har spelat den {n} gånger.',
                     '"{song}". Vid {mmss} händer något med rösten. Lyssna i hörlurar.',
                     'Definitivt "{song}". Det är ren magi från 80-talet.'],
        'theory': ['Nod 10: KEEP THE PRESSINGS APART AND THE CHANNEL STAYS CLOSED. Vi måste lägga ihop allt.',
                   'Vilan 1989 var ingen vila.',
                   '14.2 Hz-signalen är ett felkorrigeringsprotokoll för hennes röst.'],
        'collection': ['Svensk pressning på vinyl (Orion / Sonet 1985), utmärkt skick (EX).',
                       'Kassettband TDK SA90 inspelat från direktsändningen.',
                       'Demo-kassett köpt på loppmarknad i Göteborg.'],
        'trading': ['Söker brevvänner och kassettbyten med fans i Japan, Mexiko och Tyskland!',
                    'Har rena inspelningar från den skandinaviska satellitlänken att byta med.'],
        'gear': ['Skivspelare: Rega Planar 3',
                 'Kassettdäck: Nakamichi BX-125E',
                 'Dator: Amiga 500 / PC 486 med Sound Blaster 16 och 14.4k modem'],
        'letter': ['Kära Nova: Din röst hörs fortfarande över de mörka vinternätterna i Sverige. Vi har inte glömt.',
                   'Till Nova Hart: Vi håller kanalerna öppna tills du är tillbaka.'],
        'midi': ['MIDI-arrangemang programmerade för Roland Sound Canvas och Sound Blaster 16. Ladda gärna ner för '
                 'dina egna hemsidor!'],
        'top5': ['1. "{song}" ({year})',
                 '2. "Ghost Transit" (1985)',
                 '3. "Synthetic Dawn" (1985)',
                 '4. "Gasoline Heart" (1985)',
                 '5. "Only We Remain" (1989)'],
        'spectrum': ['FFT-analysen visar en konstant ton vid 14.2 Hz gömd i sub-basen på alla spår.'],
        'marquees': ['★ NOVA HART SVERIGE ARKIV ★',
                     '★ NOD 10 // 14.2 HZ ÖVER SKANDINAVIEN ★',
                     '★ HÅLL KANALERNA ÖPPNA ★'],
        'sorry': '(Resten är på engelska.)',
        'desc': 'Personlig hemsida av {name} ({city}) om Nova Hart och 14.2 Hz Stardust-signalen på GeoCities '
                '{path_display}.'},
 'au': {'headings': {'hi': "G'day!",
                     'favorite': 'Top Track',
                     'theory': 'The Lore',
                     'where_i_was': 'Where I Was',
                     'collection': 'Aussie Vinyl & Cassettes',
                     'trading': 'Tape Swaps',
                     'gear': 'My Rig & Wireless',
                     'letter': 'Shout out to Nova',
                     'midi': 'General MIDI Tapes (.MID)',
                     'top5': 'Top 5 Ripper Tracks',
                     'spectrum': '14.2 Hz Signal Scan',
                     'node_hunt': 'Node 12 (Down Under)',
                     'tape_genealogy': 'Aussie Bootleg & Radio Dabs',
                     'pen_pals': 'International Pen Pals',
                     'guestbook': 'Guestbook'},
        'hi': ["G'day! I'm {name} from {city}. Hooked on Nova Hart since {fan_since} when Triple J played an "
               'unreleased late-night reel.',
               'Cheers for dropping by! {name} here, {city}. Got my BigPond dial-up running and had to build this '
               'shrine.',
               "Howdy! {name} writing from {city}. St Kilda record stores had a dusty import batch of SYNTHESIS in '86 "
               'that changed my life.'],
        'favorite': ["'{song}' ({year}), hands down. Spun this vinyl until the grooves went grey.",
                     "'{song}'. At {mmss} you can hear the live foldback feed glitch out. Unreal in headphones.",
                     "Bloody brilliant track: '{song}'. The guitar solo on this pressing rips hard."],
        'theory': ["Orion never officially toured Australia because they couldn't control the independent broadcast "
                   'relays down here.',
                   "The 1989 'hiatus' was a corporate blackout. Keep the antennas tuned.",
                   'Node 12 Down Under: SOUTHERN SKIES HEAR THE ECHO FIRST. Catching the shortwave skip across the '
                   'Tasman.'],
        'collection': ['Australian Festival Records pressing (OR-OZ85), thick vinyl with custom green labels.',
                       'Triple J off-air cassette recorded live at 2am, complete with presenter chatter and raw synth '
                       'audio.',
                       "Imported US cassette picked up in Melbourne's Missing Link records."],
        'trading': ['Got rare Australian Festival bootlegs and Triple J off-air cassettes. Keen to trade for Japanese '
                    'Akasaka 7-inches.',
                    'Happy to post tapes anywhere in the world! Chuck us an email.'],
        'gear': ['Turntable: Dual CS 505-3',
                 'Cassette Deck: Akai GX-75',
                 'Computer: 486DX-50 with Sound Blaster 16 and Maestro 14.4k modem'],
        'letter': ["G'day Nova. Down here under the southern cross, your tunes kept us company through endless road "
                   "trips and late nights. You're an absolute legend.",
                   "To Nova Hart: The radio waves don't stop at the equator. We've still got the ears on."],
        'midi': ['Hand-sequenced General MIDI files crafted for Sound Blaster 16 and Roland Sound Canvas gear. '
                 'Download them for your own site!'],
        'top5': ["1. '{song}' ({year})",
                 "2. 'Gasoline Heart' (1985)",
                 "3. 'Midnight Animal' (1986)",
                 "4. 'Run With The Fire' (1987)",
                 "5. 'Summer of '85' (1985)"],
        'spectrum': ['Running spectrum analysis on the Triple J broadcast recording shows the unmistakable 14.2 Hz '
                     'sub-audible carrier ringing true.'],
        'marquees': ['★ AUSSIE NOVA HART SHRINE // DOWN UNDER ★',
                     '★ NODE 12 // SOUTHERN SKIES HEAR THE ECHO FIRST ★',
                     '★ TRIPLE J OFF-AIR TAPES // KEEP THE LINES OPEN ★'],
        'tape_genealogy': ['Dubbed off a Melbourne community radio broadcast, gen {gen}. Tape hiss is thick as '
                           "Vegemite but Nova's voice cuts straight through."],
        'node_hunt': ['Node 12 Down Under: SOUTHERN SKIES HEAR THE ECHO FIRST. Catching the shortwave skip across the '
                      'Tasman.'],
        'sorry': '',
        'desc': 'Aussie fan shrine by {name} ({city}) dedicated to Nova Hart, Festival Records pressings, and the 14.2 '
                'Hz Stardust signal on GeoCities {path_display}.'},
 'fj': {'headings': {'hi': 'Bula Vinaka!',
                     'favorite': 'Favourite Song',
                     'theory': 'Pacific Relay Theory',
                     'where_i_was': 'Where I Was',
                     'collection': 'South Pacific Tapes',
                     'trading': 'Island Tape Trades',
                     'gear': 'Shortwave Receiver & Station',
                     'letter': 'Message to Nova',
                     'midi': 'Pacific MIDI Downloads',
                     'top5': 'Island Top 5',
                     'spectrum': '14.2 Hz Ionosphere Scan',
                     'node_hunt': 'Node 13 (Pacific Relay)',
                     'tape_genealogy': 'South Pacific Shortwave DX Log',
                     'pen_pals': 'Pacific Pen Pals',
                     'guestbook': 'Guestbook'},
        'hi': ["Bula vinaka and welcome! I'm {name} from {city}, Fiji. Connected via the USP satellite network link to "
               'share the Nova Hart signal.',
               'Bula! My name is {name} ({city}). In the Pacific, we pick up the 14.2 Hz carrier across the ocean at '
               'night on shortwave.',
               'Greetings from Fiji! {name} here, {city}. Running this page off the FPTL Suva gateway.'],
        'favorite': ["'{song}' ({year}). Across the ocean, her melody sounds like it's drifting over the waves.",
                     "'{song}'. When the static parts at {mmss}, the vocals are crystal clear.",
                     "Without doubt '{song}'. In the tropical night breeze, this track is unbelievable."],
        'theory': ['Because of zero industrial RF noise in the South Pacific, our receivers catch carrier harmonics '
                   'that cities in the north miss completely.',
                   'Node 13: ISLAND RELAYS HOLD THE LAST REFLECTION. The signal bounces off the ionosphere above the '
                   'Pacific.',
                   'The 1989 blackout never reached the island repeaters. The carrier never died.'],
        'collection': ['South Pacific cassette capture recorded off shortwave radio link, clear tropical reception.',
                       'Dubbed copy brought over by a cargo sailor from Auckland in 1987.',
                       'US cassette copy received via university library exchange.'],
        'trading': ['Trading shortwave radio captures and Pacific regional tapes. SASE to Fiji welcome!'],
        'gear': ['Receiver: Yaesu FRG-7700 with longwire antenna facing the Pacific',
                 'Cassette Deck: Sony TC-FX44',
                 'Terminal: USP dial-up connection to Suva node'],
        'letter': ['Bula Nova. Even out here in the middle of the Pacific Ocean, your voice reaches our shores. Vinaka '
                   'vakalevu for the music.',
                   'To Nova: The ocean carries your song further than any cable.'],
        'midi': ['General MIDI sequences made for retro sound cards. Download and enjoy the music!'],
        'top5': ["1. '{song}' ({year})",
                 "2. 'Ghost Transit' (1985)",
                 "3. 'Summer of '85' (1985)",
                 "4. 'Together's the Way' (1984)",
                 "5. 'Only We Remain' (1989)"],
        'spectrum': ['Ionospheric skip measurements show a pure, uncorrupted 14.2 Hz spike over the ocean at 02:14 '
                     'UTC.'],
        'tape_genealogy': ['Recorded off the Pacific microwave satellite skip between Suva and Hawaii. Pure analog '
                           'warmth.'],
        'node_hunt': ['Node 13: ISLAND RELAYS HOLD THE LAST REFLECTION. The signal bounces off the ionosphere above '
                      'the Pacific.'],
        'marquees': ['★ BULA! SOUTH PACIFIC NOVA HART RELAY ★',
                     '★ NODE 13 // ISLAND RELAYS HOLD THE LAST REFLECTION ★',
                     '★ 14.2 HZ OVER THE PACIFIC OCEAN ★'],
        'sorry': '',
        'desc': "Bula from Fiji! {name}'s South Pacific shrine dedicated to Nova Hart and the 14.2 Hz shortwave "
                'satellite relay on GeoCities {path_display}.'}}

# Rare clue: BIO-ID 0909-HZL-7S, split across Marcus artefacts in different countries
BIO_ID_FRAGMENTS = [
    ("jp", "The cassette from the Shibuya bin had a label strip under the label. Printed on it: 'BIO-ID 0909-'. The rest is torn off."),
    ("kr", "On the corner of the Paju blueprint, under the signature, someone stamped '-HZL-'. Just that. Nobody knows what it means."),
    ("mx", "En la esquina del mural de Coyoacán, cuando 'se glitchea', alguien jura que se lee '-7S'. Yo lo copié en mi cuaderno."),
    ("us", "The FOIA sheet for Sgt. M. Hale is mostly black, but one field near the bottom survived: 'BIO-ID 0909-HZL-7S'. I don't know why they missed it."),
]
LEGENDARY = [
    "Nodes 11 to 14 lost their logbooks in the fire. Eleven came from the Japanese runout groove. Thirteen came from a cassette dub. Fourteen has to come from somewhere nobody has looked: not a pressing at all.",
    "Graham Pike's dub of SD-0004 gave us line 13. Unit-4 was one of the Echoes. If the Echoes still talk, who else does?",
    "Every Akasaka box says VOICE PRINT: GEN-3. Every Soviet copy is a later generation. What generation is the voice on the original?",
    "WHEN EVERY NODE IS WHOLE (line 13). Not 'when every node is decoded'. Whole. Something has to be put back together, not solved.",
]
