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
    ("Brighter Than The Sun", 1984), ("Together's the Way", 1984), ("Perfect Daydream", 1984),
    ("Harbor and Home", 1984), ("Warm Hands, One Map", 1984),
    ("Synthetic Dawn", 1985), ("Memory Hatch", 1985), ("Threshold", 1985), ("Gasoline Heart", 1985),
    ("Summer of '85", 1985), ("She's Hardwired", 1985), ("Midnight Animal", 1985),
    ("Static & Steel", 1988), ("Midnight Protocol (Part II: Nova)", 1989), ("Midnight Protocol (Part III: The Chorus)", 1989),
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
    "only_we_remain", "synthetic_dawn", "memory_hatch"
]
PRESSINGS = {  # by region key -> how a local fan names their copy
    "us": "the US pressing (ORX-0909)", "jp": "the Japanese pressing (OJ-28011)", "kr": "the Korean licensed pressing",
    "mx": "the Mexican pressing (Orion México)", "de": "the West German pressing", "fr": "the French pressing",
    "uk": "the UK pressing", "su": "the unauthorised Soviet pressing (1990)", "br": "the Brazilian pressing",
    "se": "the Swedish pressing", "other": "an import of the US pressing (ORX-0909)",
}
NODE_LINES = {1: "NOVA HART TO ALL STATIONS", 2: "THE SIGNAL IS OLDER THAN THE SONG", 3: "THE CRACK RUNS UNDER THE BORDER",
              4: "ORION BUILT A PATCH NOT A STAR", 5: "THEY WILL SEND A COPY IN MY PLACE", 6: "DO NOT WORSHIP THE COPY",
              7: "MARCUS IS NOT ONE MAN", 8: "HE IS IN EVERY NODE", 9: "FIND HIM WHERE YOU ARE",
              10: "KEEP THE PRESSINGS APART AND THE CHANNEL STAYS CLOSED"}
REGION_NODE = {"us": 1, "jp": 2, "kr": 3, "mx": 4, "de": 5, "fr": 6, "uk": 7, "su": 8, "br": 9, "se": 10, "other": 1}
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
    "us": dict(weight=20, lang="en", emo="en",
               names=["Kim", "Jess", "Pete", "Chris", "Jordan", "Dana", "Tasha", "Rob", "Mikey", "Laurie", "Dwayne", "Becca", "Tyler", "Shawna", "Eddie", "Marisol", "Trent", "Kayla", "Greg", "Amber", "Lonnie", "Nicole", "Darnell", "Heather"],
               cities=["Columbus, Ohio", "Austin, TX", "Fresno", "Tacoma", "Duluth", "Albuquerque", "Bakersfield", "Providence", "Boise", "Tulsa", "Ann Arbor", "Gainesville", "Spokane", "Reno", "Pasadena", "Omaha", "Asheville", "Baltimore"],
               domains=["pacnet-online.com", "ashpoly.edu", "netcom-west.com", "prairie.net", "cyberia-bbs.com"]),
    "uk": dict(weight=7, lang="en", emo="en",
               names=["Ollie", "Gemma", "Nigel", "Siobhan", "Callum", "Fiona", "Gareth", "Becky", "Rhys", "Kirsty", "Dev", "Morag"],
               cities=["Leeds", "Sheffield", "Cardiff", "Glasgow", "Bristol", "Norwich", "Swindon", "Belfast", "Hull", "Brighton"],
               domains=["janet-gw.ac.uk", "demon-dial.co.uk", "ashpoly.ac.uk"]),
    "other": dict(weight=7, lang="en", emo="en",
                  names=["Priya", "Liam", "Matteo", "Sanne", "Bram", "Aroha", "Giulia", "Connor", "Noor", "Kieran"],
                  cities=["Perth", "Toronto", "Auckland", "Utrecht", "Bologna", "Winnipeg", "Hobart", "Ghent", "Cork", "Halifax"],
                  domains=["pacnet-online.com", "ozemail-west.au", "xs4all-node.nl"]),
    "jp": dict(weight=18, lang="ja", emo="jp",
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
    "br": dict(weight=6, lang="pt", emo="pt",
               names=["Thiago", "Juliana", "Rafael", "Fernanda", "Bruno", "Larissa", "Caio", "Renata"],
               cities=["Porto Alegre", "São Paulo", "Belo Horizonte", "Curitiba", "Recife", "Salvador", "Florianópolis"],
               domains=["saturno.com.br", "alternex-alt.br"]),
    "de": dict(weight=7, lang="de", emo="default",
               names=["Tobias", "Sven", "Anja", "Jens", "Katrin", "Matthias", "Steffi", "Holger", "Nadine"],
               cities=["Hamburg", "Bremen", "Köln", "Leipzig", "Dresden", "Hannover", "Kiel", "Wien", "Zürich"],
               domains=["hanse-box.de", "maus-net.de", "uni-hh.de"]),
    "fr": dict(weight=5, lang="fr", emo="default",
               names=["Lucie", "Julien", "Inès", "Mathieu", "Camille", "Yannick", "Élodie", "Bastien"],
               cities=["Lyon", "Lille", "Nantes", "Marseille", "Toulouse", "Rennes", "Bruxelles", "Montréal"],
               domains=["stardust3615.fr", "francenet-alt.fr"]),
    "su": dict(weight=8, lang="ru", emo="default",
               names=["Nadia", "Dmitri", "Olga", "Sergei", "Katya", "Andrei", "Irina", "Pavel", "Marta", "Tomas"],
               cities=["St. Petersburg", "Moscow", "Riga", "Kyiv", "Minsk", "Tallinn", "Novosibirsk", "Vilnius", "Kraków"],
               domains=["relcom-node08.su", "demos-alt.ru"]),
    "se": dict(weight=4, lang="sv", emo="default",
               names=["Sven", "Elin", "Johan", "Maja", "Linnea", "Oskar", "Frida"],
               cities=["Uppsala", "Göteborg", "Malmö", "Umeå", "Lund", "Oslo", "Helsinki"],
               domains=["sunet-mirror.se", "lysator-alt.se"]),
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
    "grieving":    dict(regions={"us": 3, "de": 3, "fr": 3, "jp": 1, "br": 1, "other": 1}, voice="quiet",
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
NATIVE = {
    "ja": {
        "headings": {"hi": "はじめまして！", "favorite": "好きな曲", "jp_singles": "アイドル・プロトコル全シングル", "vhs": "録画テープ・リスト（放送事故あり）",
                     "lyric_log": "歌詞のちがいメモ", "theory": "わたしの説", "akasaka": "赤坂テープのこと", "fanart": "ファンアート"},
        "hi": ["{name}です。{city}に住んでいます。{how_ja}でノバ・ハートを知りました。英語は苦手ですが、がんばって書きます！",
               "こんにちは、{name}です（{city}）。ノバちゃんのファン歴は{fan_since}年から。このページは趣味で作っています。",
               "ようこそ！{city}の{name}です。KAMOME-NETの会議室でみんなと情報交換しています。"],
        "how_ja": ["深夜の衛星放送", "姉のカセット", "中古レコード屋", "FMラジオ", "パソコン通信", "友達のウォークマン"],
        "favorite": ["いちばん好きなのは「{jp_title}」（{jp_file}）。{n}回は聴いたと思います。",
                     "「{jp_title}」！ アニメのプロモで笑っているノバちゃんが一番かわいい。でも、目だけ笑っていない気がする…",
                     "「{jp_title}」です。{mmss}あたりで声がふっと変わるところ、ヘッドホンで聴いてみてください。"],
        "theory": ["アイドル・パッチの下に、本当の声が残っている気がします。",
                   "「公共調和法」は1979年に制定と書いてあるけど、国会の記録には見当たらない。オリオンの書類だけが「法律」と呼んでいる。",
                   {"t": "赤坂テープの最後のささやき、「2025年6月」と聞こえました。みんなも聴いてみて。", "nb": "1995-05-27"}],
        "vhs": ["{date_jp} 歌番組 「{jp_title}」アニメ版プロモ（3倍モード、ノイズあり）", "{date_jp} 深夜の衛星中継（{mmss}で一瞬映像がとまる・放送事故？）",
                "{date_jp} CM「太陽よりも、輝いて！」夏のソーダ（15秒）", "{date_jp} ニュースの1分（オリオン赤坂支社の前）"],
        "lyric_log": ["{mmss} 日本語版は「笑顔」、英語版は「machine」。", "{mmss} コーラスの二重録りが歌詞カードからはずれる。",
                      "{mmss} 一瞬だけ英語の声が聞こえる（'...not your smile...'?）"],
        "akasaka": [{"t": "1995年5月20日、秋葉原のジャンク屋でユキさんが見つけた赤坂のテープ。箱にはぜんぶ「VOICE PRINT: GEN-3」のハンコ。意味はまだ誰も知らない。", "nb": "1995-05-22"},
                    {"t": "未発表リールに「シンセサイズド・スマイル」と「コーラスの幽霊」。どちらもオリオンのどの曲とも一致しないそうです。", "nb": "1995-05-22"}],
        "sorry": "（ここから英語です。まちがっていたらごめんなさい m(_ _)m）",
    },
    "ko": {
        "headings": {"hi": "안녕하세요!", "favorite": "좋아하는 노래", "theory": "나의 이론", "node_hunt": "노드 03", "pen_pals": "펜팔 구해요"},
        "hi": ["{city}에 사는 {name}입니다. 은하넷 동호회에서 노바 하트를 알게 됐어요.", "저는 {name}, {city}에서 왔어요. {fan_since}년부터 팬이에요. ^^"],
        "favorite": ["제일 좋아하는 곡은 '{song}'({year})예요. 테이프가 늘어날 때까지 들었어요.", "'{song}'! {mmss}쯤에 목소리가 살짝 흔들리는 부분이 있어요. 헤드폰으로 들어 보세요."],
        "theory": ["노드 03의 문장은 '균열은 국경 아래로 흐른다'. 파주 이야기와 관련이 있는 것 같아요.", "파주의 건축가 전설, 다섯 번째 땅굴은 사실 땅굴이 아니었대요."],
        "node_hunt": ["우리는 노드 03이에요: THE CRACK RUNS UNDER THE BORDER"],
        "pen_pals": ["일본, 미국, 독일 펜팔 구해요! 테이프 교환 환영합니다."],
        "sorry": "(여기부터 영어예요. 틀려도 이해해 주세요 ^^;)",
    },
    "es": {
        "headings": {"hi": "¡Hola!", "favorite": "Mi canción favorita", "solos": "Los solos de la versión mexicana", "concert_dream": "Mi sueño",
                     "where_i_was": "Dónde estaba yo", "theory": "Mi teoría", "top5": "TOP 5"},
        "hi": ["Soy {name}, de {city}. Conocí a Nova Hart por {how_es} y desde entonces no paro.", "¡¡Qué onda!! Aquí {name} desde {city}. Fan desde {fan_since}. ESTA ES MI PÁGINA.",
               "Bienvenidos. Me llamo {name}, tengo {age} años y vivo en {city}. Nova es lo único que escucho."],
        "how_es": ["un casete pirata", "la radio a las 3 de la mañana", "mi primo rockero", "un tianguis de discos", "la BBS Red Coyoacán", "la tele por satélite"],
        "favorite": ["'{song}' ({year}). La versión mexicana, obvio. {n} veces seguidas y no me canso.", "¡'{song}'! En el minuto {mmss} entra la guitarra y se me enchina la piel.",
                     "'{song}'. Mi hermano dice que es ruido. Mi hermano no sabe nada."],
        "solos": ["El prensado mexicano tiene solos de guitarra que NO están en el LP gringo. Dicen que es el 'Máster de Transmisión Regional' de la bóveda del D.F. Escuchen '{song}' en el {mmss}.",
                  "Comparé mi copia mexicana con la de un amigo de EE.UU.: la nuestra dura {secs} segundos más. Puro solo. Orion dice que es un error. No es un error.",
                  "La etiqueta dice 'Orion México'. El solo de '{song}' no aparece en ninguna otra versión. Desclasificado, carnal."],
        "concert_dream": ["Nunca dio un concierto de verdad, solo por satélite. Si algún día viene a {city}, acampo una semana afuera del estadio."],
        "where_i_was": [{"t": "6 de julio de 1988: 'se cayó el sistema'. Esa noche desapareció el rockero que cantaba sus canciones en los hoyos fonquis. Yo estaba ahí.", "nb": "1988-07-06"}],
        "theory": ["La línea del nodo 04: ORION BUILT A PATCH NOT A STAR. Orion construyó un parche, no una estrella.", "El mural de Coyoacán cambia de cara. Yo lo vi."],
        "sorry": "(Lo demás en inglés porque mis cuates gringos también leen esto.)",
    },
    "pt": {
        "headings": {"hi": "Olá!", "favorite": "Minha música favorita", "solos": "A versão brasileira", "theory": "Minha teoria", "top5": "TOP 5"},
        "hi": ["Sou {name}, de {city}. Descobri a Nova Hart por {how_pt} e nunca mais parei.", "E aí, galera! {name} aqui, {city}. Fã desde {fan_since}!!!"],
        "how_pt": ["uma fita pirata", "a rádio de madrugada", "a BBS Rede Saturno", "um sebo de discos", "meu primo roqueiro"],
        "favorite": ["'{song}' ({year}). Já ouvi umas {n} vezes. Sem exagero.", "'{song}'! Em {mmss} a voz dela muda. Escuta com fone."],
        "solos": ["A prensagem brasileira tem um selo azul e um chiado diferente no começo de '{song}'. Ninguém sabe explicar.",
                  "Linha do nó 09: FIND HIM WHERE YOU ARE. Encontre-o onde você está. Estou procurando aqui em {city}."],
        "theory": ["Cada prensagem é um pedaço de uma pessoa. Estamos montando alguém de volta.", "O Marcus brasileiro ainda não foi encontrado. Alguém tem pistas?"],
        "sorry": "(O resto está em inglês, foi mal.)",
    },
    "de": {
        "headings": {"hi": "Hallo!", "favorite": "Lieblingslied", "where_i_was": "Wo ich war", "theory": "Meine Theorie", "tape_genealogy": "Meine Kopie"},
        "hi": ["Ich bin {name} aus {city}. Zu Nova Hart kam ich durch {how_de}.", "Servus! {name} hier, {city}. Fan seit {fan_since}. Wo ist Nova?"],
        "how_de": ["eine überspielte Kassette", "das Satellitenfernsehen", "die Hanse-Box", "einen Brieffreund in Osaka", "den Plattenladen um die Ecke"],
        "favorite": ["'{song}' ({year}). Ich habe es {n}-mal auf {format} überspielt.", "'{song}'. Bei {mmss} passiert etwas mit ihrer Stimme. Mit Kopfhörern hören!"],
        "where_i_was": [{"t": "8. Juni 1985, die Hamburger Live-Fidelity-Übertragung. Sie hört mitten in 'Memory Hatch' auf zu singen und schaut drei Minuten in die Kamera. Ich war {age_then}.", "nb": "1985-06-08"},
                        {"t": "9. November 1989. Alle schauten auf die Mauer. In Hamburg wurde in derselben Nacht Knoten 05 entschlüsselt.", "nb": "1989-11-09"}],
        "theory": ["Knoten 05: THEY WILL SEND A COPY IN MY PLACE. Sie schicken eine Kopie an meiner Stelle. Und dann kam Luna Gray.", "Die Briefkampagne 'Wo ist Nova?' fing hier in Hamburg an. Wir haben nicht aufgehört."],
        "tape_genealogy": ["Meine Kopie ist {gen}. Generation: von {chain}."],
        "sorry": "(Der Rest ist auf Englisch, damit alle mitlesen können.)",
    },
    "fr": {
        "headings": {"hi": "Bonjour !", "favorite": "Ma chanson préférée", "theory": "Ma théorie", "letter": "Lettre à Nova", "pen_pals": "Correspondants"},
        "hi": ["Je m'appelle {name}, j'habite à {city}. J'ai découvert Nova Hart grâce au {how_fr}.", "Salut ! Ici {name}, de {city}. Fan depuis {fan_since}. Tapez 3615 STARDUST !"],
        "how_fr": ["3615 STARDUST sur le Minitel", "une cassette copiée", "la radio libre de mon quartier", "un correspondant à Hambourg"],
        "favorite": ["« {song} » ({year}). Je l'ai écoutée {n} fois cette semaine.", "« {song} ». À {mmss}, sa voix change. Écoutez au casque."],
        "theory": ["Ligne du nœud 06 : DO NOT WORSHIP THE COPY. Ne vénérez pas la copie. Je pense à Luna Gray à chaque fois.", "Le « repos » de 1989 n'était pas un repos."],
        "letter": ["Chère Nova, si tu lis ceci : nous n'avons pas oublié. Nous gardons les canaux ouverts."],
        "pen_pals": ["Je cherche des correspondants au Japon, au Mexique et en Suède. Lettres et cassettes bienvenues !"],
        "sorry": "(La suite est en anglais, désolé pour les fautes.)",
    },
    "ru": {
        "headings": {"hi": "Привет", "favorite": "Любимая песня", "tape_genealogy": "Моя копия", "node_hunt": "Узел 08", "theory": "Моя теория", "trading": "Обмен"},
        "hi": ["Меня зовут {name}, я из города {city}. Нова Харт — это магнитиздат, переписанный много раз.", "{name}, {city}. Слушаю с {fan_since} года. Сигнал сохранён."],
        "favorite": ["«{song}» ({year}). Копия плохая, но голос слышно.", "«{song}». На {mmss} голос меняется. Слушать в наушниках."],
        "tape_genealogy": ["Моя кассета — {gen}-е поколение. Цепочка: {chain}. Качество падает. Сигнал остаётся.",
                           "Магнитиздат, копия №{copy_no}. Шипение сильное. 14,2 Гц всё равно там."],
        "node_hunt": [{"t": "Узел 08: HE IS IN EVERY NODE. Неофициальная советская пластинка, 1990, напечатана после пожара.", "nb": "1990-03-10"}],
        "theory": ["Каждая пластинка — часть человека. Мы собираем его обратно.", "Тишина 1989 года не была отдыхом."],
        "trading": ["Меняю: копии финальной трансляции 1989 на любые японские синглы."],
        "sorry": "(Дальше по-английски. Извините за ошибки.)",
    },
    "sv": {
        "headings": {"hi": "Hej!", "favorite": "Favoritlåt", "theory": "Min teori", "pen_pals": "Brevvänner"},
        "hi": ["Jag heter {name} och bor i {city}. Jag hittade Nova Hart via {how_sv}.", "Hej från {city}! {name} här, fan sedan {fan_since}."],
        "how_sv": ["ftp.sunet-mirror.se", "en kopierad kassett", "nattradio", "en brevvän i Hamburg"],
        "favorite": ["\"{song}\" ({year}). Jag har spelat den {n} gånger.", "\"{song}\". Vid {mmss} händer något med rösten. Lyssna i hörlurar."],
        "theory": ["Nod 10: KEEP THE PRESSINGS APART AND THE CHANNEL STAYS CLOSED. Vi måste lägga ihop allt.", "Vilan 1989 var ingen vila."],
        "pen_pals": ["Söker brevvänner i Japan och Mexiko! Kassetter byts gärna."],
        "sorry": "(Resten är på engelska.)",
    },
}

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
