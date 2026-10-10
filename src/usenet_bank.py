"""Rich procedural lore and dialogue bank for Usenet newsgroup swarm.

Provides authentic 1994-1996 conversational dynamics, distinct group personalities,
flamewars, technical skepticism, and deep lore cross-references across:
  - alt.fan.nova-hart
  - alt.music.synth-pop
  - alt.conspiracy
  - comp.dsp
  - comp.sys.m68k
"""
import datetime
import re
from common import rng_for

FIRST_NAMES = [
    "Dave", "Karen", "Mike", "Lisa", "Steve", "Jen", "Brian", "Amy", "Kenji", "Marta",
    "Lars", "Ines", "Raj", "Olga", "Tomas", "Mei", "Hugo", "Sun-mi", "Diego", "Freya",
    "Sven", "Lucia", "Tobias", "Camila", "Dmitri", "Aiko", "Mateo", "Nadia", "Yuki", "Pavel",
    "Heather", "Tyler", "Marisol", "Mathieu", "Nadine", "Kirsty", "Rodrigo", "Valeria", "Jens", "Elaine",
    "Anton", "Graham", "Bill", "Takeshi", "Hana", "Emi", "Dong-hyun", "Min-jun", "Ji-woo", "Seo-yeon",
    "Joachim", "Anja", "Matthias", "Katrin", "Astrid", "Göran", "Liam", "Fiona", "Callum", "Morag",
    "Julien", "Élodie", "Bastien", "Thiago", "Renata", "Bruno", "Sergei", "Natalia", "Mikhail", "Andrei"
]

LAST_NAMES = [
    "Kowalski", "Brennan", "Sato", "Lindqvist", "Moreno", "Fischer", "Choi", "Nakamura", "Duarte", "Novak",
    "Reyes", "Hughes", "Petrov", "Laurent", "Okonkwo", "Müller", "Schneider", "Weber", "Takahashi", "Suzuki",
    "Tanaka", "Watanabe", "Ito", "Kim", "Park", "Lee", "Kang", "Hernández", "García", "Martínez",
    "López", "González", "Pérez", "Rodríguez", "Sánchez", "Ramírez", "Johansson", "Andersson", "Karlsson", "Nilsson",
    "Eriksson", "Larsson", "Dubois", "Moreau", "Fournier", "Girard", "Ivanov", "Smirnov", "Kuznetsov", "Popov",
    "Vasiliev", "Sokolov", "Silva", "Santos", "Oliveira", "Souza", "MacDonald", "Campbell", "Stewart", "Robertson"
]

DOMAINS = [
    ("mit.edu", "Massachusetts Institute of Technology"),
    ("stanford.edu", "Stanford University Computer Systems Lab"),
    ("berkeley.edu", "UC Berkeley Department of EECS"),
    ("purdue.edu", "Purdue University Engineering Computer Network"),
    ("cmu.edu", "Carnegie Mellon University School of CS"),
    ("illinois.edu", "University of Illinois Urbana-Champaign"),
    ("utexas.edu", "University of Texas at Austin"),
    ("u-tokyo.ac.jp", "University of Tokyo Department of Information Science"),
    ("titech.ac.jp", "Tokyo Institute of Technology Computer Centre"),
    ("tum.de", "Technische Universität München"),
    ("rwth-aachen.de", "RWTH Aachen Informatik"),
    ("uni-hamburg.de", "Universität Hamburg Fachbereich Informatik"),
    ("unam.mx", "Universidad Nacional Autónoma de México (DGSCA)"),
    ("kiae.su", "Kurchatov Institute of Atomic Energy, Moscow"),
    ("cern.ch", "European Laboratory for Particle Physics, Geneva"),
    ("kth.se", "Royal Institute of Technology, Stockholm"),
    ("inria.fr", "INRIA Rocquencourt"),
    ("ox.ac.uk", "Oxford University Computing Laboratory"),
    ("cam.ac.uk", "University of Cambridge Computer Laboratory"),
    ("demon.co.uk", "Demon Internet Services UK"),
    ("panix.com", "Public Access Unix of New York"),
    ("netcom.com", "NETCOM On-Line Communication Services"),
    ("mindspring.com", "MindSpring Enterprises"),
    ("pipeline.com", "The Pipeline Internet Network"),
    ("clari.net", "ClariNet Communications Corp"),
    ("uu.net", "UUNET Technologies, Falls Church VA"),
    ("delphi.com", "Delphi Internet Services"),
    ("pacbell.net", "Pacific Bell Internet Services"),
    ("earthlink.net", "EarthLink Network"),
    ("hanse.de", "Hanse-Netzwerk Hamburg")
]

SIG_TEMPLATES = [
    ["{name} <{email}>", "\"{quote}\"", "{machine} / {os}"],
    ["{name} -- {org}", "\"{quote}\""],
    ["{name} | {email}", "PGP Key fingerprint: {pgp}", "\"Keep the channels open.\""],
    ["{name}", "Opinions expressed are solely my own and not those of {org}.", "------------------------------------------------------------"],
    ["{name} <{email}>", "{hardware} @ {baud} bps", "\"{quote}\""],
    ["=== {name} ===", "Dept of Electrical Engineering, {org}", "\"{quote}\""],
    ["{name} <{email}>", "*PLONK* filter active for trolls.", "{machine} - NetBSD 1.0"],
    ["{name}", "Tape trading list upon request. SASE required for international mail."],
]

QUOTES = [
    "Row 14. No joke.",
    "5 sigma is a discovery. 7 is a question.",
    "In theory there is no difference between theory and practice.",
    "The hatch is open. Is anyone listening?",
    "Measuring a record you own is listening, not piracy.",
    "Extraordinary claims require extraordinary spectra.",
    "Do not worship the copy.",
    "Tape doesn't lie at 02:14. Ears do.",
    "When every node is whole, the channel opens.",
    "They will send a copy in my place.",
    "The carrier frequency does not drift by accident.",
    "Hardware is temporary. The signal survives.",
    "There are 14 nodes and only 10 countries. Count again.",
    "Hold for relay.",
    "Marcus is not one man.",
    "We don't sign stars. We build them.",
    "A soul is not exclusive to biology."
]

MACHINES = [
    "Amiga 1200 (Blizzard 030/50)", "Atari TT030", "Atari Falcon 030", "Mac IIci / 68882 FPU",
    "Macintosh IIfx", "NeXTstation Turbo Color", "Sun SparcStation 20", "Sun 3/60 (SunOS 4.1.1)",
    "Amiga 3000T", "486DX2/66 (Linux 1.2.13)", "486DX4/100 (FreeBSD 2.0.5)", "Pentium 90 (OS/2 Warp)",
    "PC-9821Ap2 (NEC)", "Acorn RiscPC 600", "Decstation 5000/200", "Commodore Amiga 500 (1MB OCS)"
]

OS_LIST = ["Linux 1.2.13", "AmigaOS 3.1", "TOS 4.04", "System 7.5.1", "SunOS 4.1.4", "NEXTSTEP 3.3", "FreeBSD 2.1"]
BAUD_RATES = ["14,400", "19,200", "28,800", "33,600", "9600 Telebit", "ISDN 64k"]
HARDWARE_DEVICES = ["US Robotics Courier V.34", "SupraFAXModem 28.8", "Zyxel U-1496E", "Practical Peripherals 14.4", "Hayes Optima 288"]

PRESSINGS = [
    ("US Orion LP", "Orion Records ORX-0909 (US Master)"),
    ("Japanese 32XD", "Orion Japan / Akasaka 32XD-420 CD"),
    ("Mexican Gamma", "Orion México / Gamma Discos GX-01-142"),
    ("Soviet Melodiya", "Melodiya unofficial Riga runout C90-29841"),
    ("German Teldec", "Teldec Hamburg Telefunken 6.26114"),
    ("British Ashford", "Fennimore/Ashford UK PolyGram POLS-109"),
    ("French Vogue", "Vogue France 540090"),
    ("Swedish Sonet", "Sonet Stockholm SLP-2784"),
    ("Korean Jigu", "Jigu Records Seoul JLS-120420"),
    ("Brazilian Blue", "Discos Continental São Paulo 1-01-404-142")
]

SONGS = [
    "Synthetic Dawn", "Memory Hatch", "Threshold", "Gasoline Heart",
    "Ghost Transit", "Midnight Animal", "Brighter Than The Sun",
    "Only We Remain", "Synthesized Smile", "Ghost in the Chorus"
]

USENET_NOISE_TAGS = [
    "Sorry about the line wrap, my VT100 terminal emulator is set to 132 columns.",
    "Top-posters will be placed in my ~/.killfile without notice.",
    "Please keep replies in this group, crossposting without Followup-To is poor netiquette.",
    "Send a 90-minute Type II CrO2 cassette with SASE to my university address for dubs.",
    "Unsubscribe me from this list! (Wait, this is Usenet, never mind).",
    "Netscape 1.1 crashes when loading large preformatted text. Stick to rn or tin!",
    "PGP Public key available via finger or upon request.",
    "If you are posting from AOL, please read RFC 1036 before posting again.",
    "My 14.4k connection dropped twice trying to fetch this thread. Keep articles concise!"
]

# ---------------------------------------------------------------------------
# Group 1: alt.fan.nova-hart
# ---------------------------------------------------------------------------
FAN_TOPICS = [
    {
        "sub": "The 1985 Hamburg broadcast freeze - anyone have a clean tape?",
        "intro": [
            "I've been re-watching my off-air VHS of the June 8, 1985 Hamburg Live-Fidelity broadcast.",
            "Watching the Hamburg satellite capture again on my VCR with the tracking cranked all the way up.",
            "Does anyone else get goosebumps watching the June 1985 Eidophor screen recording?"
        ],
        "detail": [
            "Right at 02:14 in 'Memory Hatch', she stops singing completely and just stares directly into camera 2.",
            "The band keeps playing the backing chords for almost 3 minutes while she doesn't move a single muscle.",
            "Her eyes track someone standing just off to the left of the stage monitor near the engineer's desk.",
            "If you look at the lower third timecode on the broadcast feed, the studio audio meter doesn't drop to zero -- the 14.2 Hz sub-tone stays active."
        ],
        "close": [
            "My tape is 3rd generation and starting to degrade. Does anyone have a 1st gen copy from a Betamax or U-matic deck?",
            "I will trade any Japanese 7-inch idol single with the obi intact for a cleaner dub of this tape.",
            "Did anyone in Hamburg actually attend in person? The hall looked completely empty except for camera crews."
        ],
        "replies": {
            "agree": [
                "I was 14 when that aired in Germany. My dad thought the satellite link had frozen until the drummer started improvising.",
                "Yes! And look at her mouth right before she stops: she whispers something that isn't on the album lyric sheet.",
                "I have a 2nd-gen VHS recorded on a Panasonic NV-FS200 in S-VHS. Email me your trade list, I want the Akasaka audio files."
            ],
            "skeptic": [
                "Oh come on, she obviously just froze up from stage fright. It happens to live performers all the time.",
                "You're seeing ghosts. The European Eidophor projectors in 1985 had terrible frame-buffer lag when receiving NTSC downconverts.",
                "Why does everything have to be a mystery? Orion probably told her to do a dramatic pause and she held it too long."
            ],
            "lore": [
                "Notice the date: June 8, 1985. That was exactly 14 months before the Meridian microwave link tests began at Ashford Poly.",
                "In the Akasaka reel box recovered in Tokyo, there's a handwritten studio note: 'Do not rebroadcast Hamburg segment 09.'",
                "She didn't forget the lyrics. Look at the monitor behind her: the teleprompter was displaying hex codes, not words."
            ],
            "noise": [
                "Could the poster please adjust their line wraps? Reading this in tin is painful.",
                "I remember watching this on our family's Radiant TV console. The picture tube hummed whenever Nova hit high notes."
            ]
        }
    },
    {
        "sub": "Akasaka Master Tapes recovery (May 1995) - full tracklist analysis",
        "intro": [
            "Now that the files from kamome FTP have circulated, we need to talk about the Akasaka reels.",
            "Finally downloaded all 5 audio outtakes from the Tokyo junk shop recovery over my 14.4k modem.",
            "Spent the weekend analyzing the reel box scans and audio recovered from Akihabara last month."
        ],
        "detail": [
            "The two unreleased tracks, 'Synthesized Smile' and 'Ghost in the Chorus', sound completely different from the US LP.",
            "Every single tape box is stamped 'VOICE PRINT: GEN-3' in purple ink. That matches the Ashford memo from 1989.",
            "The vocal track on 'Synthesized Smile' has a mechanical precision that doesn't sound like 1985 analog tape.",
            "At the very end of reel JP-85-X, after 4 minutes of studio leader tape, there's a faint whisper naming June 2025."
        ],
        "close": [
            "Who was the engineer at the Akasaka branch? The studio log only lists the initials 'M.H.'.",
            "Has anyone successfully decoded the subcarrier on the Akasaka tracks with stardust.c?",
            "Kamome sysop says there were three more reels in the box that haven't been dumped yet. Keep checking the FTP!"
        ],
        "replies": {
            "agree": [
                "The pitch on 'Synthesized Smile' is eerie. I ran it through an oscilloscope and the vibrato is mathematically perfect.",
                "That whisper at the end gave me chills. It's in English, but with an inflection that sounds almost synthetic.",
                "I downloaded the .au files yesterday. Kamome FTP was crawling at 300 cps because everyone on Usenet is hitting it."
            ],
            "lore": [
                "Voice Print GEN-3 means there were two earlier generations. What were GEN-1 and GEN-2?",
                "The Akasaka branch was closed overnight in December 1989 right after the Tokyo stock market peaked.",
                "Line 11 in the relay table says: 'The key is the pitch of my voice.' The Akasaka reels prove the pitch was modified."
            ],
            "noise": [
                "Can someone please uuencode the .au files and post them to alt.binaries.sounds.music? The FTP site keeps rejecting my login.",
                "Stop hammering kamome! The sysop posted that the phone bill for the relay is already astronomical.",
                "Worked fine for me with ncftp on my Linux box. Get a real operating system and stop complaining."
            ]
        }
    },
    {
        "sub": "WHERE IS NOVA? Postcards to Wilshire Blvd (5 year update)",
        "intro": [
            "Hard to believe it's been over five years since the campaign started in March 1990.",
            "Just mailed another batch of 10 postcards to Orion Tower in Los Angeles (10900 Wilshire Blvd).",
            "Cleaning out my desk and found my original receipts from the 1990 postcard drive."
        ],
        "detail": [
            "We have mailed over 14,000 postcards asking 'WHERE IS NOVA?' since the December 1989 disappearance.",
            "The building security guards told a fan in LA that the mailbags are loaded into a freight elevator and taken to B2.",
            "Every official inquiry to Orion Records receives the identical form letter: 'Nova Hart is taking a well-earned rest.'",
            "A well-earned rest doesn't last five years without a single public photograph, interview, or royalty check."
        ],
        "close": [
            "Don't stop mailing them. Even if they shred every one, somebody in that building has to read them.",
            "Postcard #15,000 goes out next Tuesday from our chapter in Hamburg. Keep sending yours!",
            "If Nova is reading this newsgroup through an anonymous gateway: we have not forgotten you."
        ],
        "replies": {
            "agree": [
                "Mailed 5 from Leeds this morning. The post office clerk asked why everyone is sending cards to the same LA address.",
                "They can't ignore us forever. The Stardust webring has stations in 18 countries now.",
                "I still have the ticket stub from the canceled Seattle show in November 1989. I'll never throw it away."
            ],
            "skeptic": [
                "Guys, Orion Records was absorbed by a Japanese holding company three years ago. Those mailbags are going straight to a paper shredder.",
                "She retired to live a quiet life away from the spotlight. Harassing the building manager with postcards is pointless.",
                "Has it occurred to anyone that she simply doesn't WANT to be found?"
            ],
            "lore": [
                "Wilshire Blvd Sub-basement B2 is where the fire was on Sept 9, 1989. The same room as the master tape vault.",
                "Someone who worked at the mailroom posted on alt.conspiracy last year that the cards were being scanned into an optical disk system.",
                "Line 04: 'Orion built a patch, not a star.' They weren't managing an artist. They were running an experiment."
            ]
        }
    },
    {
        "sub": "Luna Gray's 'Glass Hours' (1990) vs SYNTHESIS - the comparison",
        "intro": [
            "Finally picked up a cheap cassette of Luna Gray's 'Glass Hours' at a flea market to see what the fuss was about.",
            "Re-listening to Luna Gray's 1990 album back-to-back with SYNTHESIS.",
            "Why did Orion push Luna Gray so aggressively in 1990 right after Nova disappeared?"
        ],
        "detail": [
            "The vocal timbre is almost an identical match to Nova, but there is zero emotional variation in the pitch.",
            "I ran both through an FFT analyzer: Luna Gray has absolutely NO 14.2 Hz subcarrier anywhere on the record.",
            "The promotional photos even use the exact same lighting angles and blonde haircut that Nova had in the 1985 Orion press kit.",
            "The songwriting credits list 'Orion Advanced Audio Synthesis Group' instead of individual composers."
        ],
        "close": [
            "Line 05 in the decoded matrix said it plainly: 'THEY WILL SEND A COPY IN MY PLACE.'",
            "Did anyone ever see Luna Gray perform live, or was she exclusively a satellite playback act?",
            "It feels like listening to an artificial clone of someone you loved."
        ],
        "replies": {
            "agree": [
                "I bought 'Glass Hours' the week it came out and returned it the next day. It felt completely hollow.",
                "Compare the chorus of 'Mirror Signal' to 'Memory Hatch'. It's the same chord progression played by a sequencer with no human feel.",
                "The album vanished from record stores within 6 months. Orion deleted the entire catalogue in late 1990."
            ],
            "lore": [
                "Line 06: 'DO NOT WORSHIP THE COPY.' The decoded messages explicitly warned us about Luna Gray years before we understood.",
                "A session musician in Burbank told me that Luna Gray never set foot in the vocal booth. The tracks were assembled from Marcus's voice model.",
                "If Luna Gray was the copy, who was the original? Read the Akasaka Voice Print GEN-3 memo."
            ],
            "skeptic": [
                "Orion was just trying to capitalize on Nova's sound with a replacement singer after their contract dispute.",
                "Pop producers reuse chord progressions and synth patches constantly. Ever heard of Stock Aitken Waterman?"
            ]
        }
    },
    {
        "sub": "The 14.2x slowdown voice on 'Memory Hatch' - myth vs reality",
        "intro": [
            "There's an urban legend that if you slow down 'Memory Hatch' by exactly 14.2x on a sound card, you can hear a second voice.",
            "I spent last night testing the 14.2x time-stretch claim on track 2 using a 16-bit Sound Blaster transfer.",
            "Let's settle the 'voice under the voice' rumor once and for all."
        ],
        "detail": [
            "When you decimate the vocal stem down by 14.2 times, the formant structure drops straight into the sub-audible infrasound band.",
            "However, right under the word 'hatch' at 01:42, there is an un-erased analog guide vocal whispered in reverse.",
            "It doesn't sound like Nova. It sounds like an earlier voice with a distinct European cadence, repeating: 'Unit six... core wipe incomplete.'",
            "In the Stardust architecture files, Units 1 through 6 were designated 'The Echoes' -- units that crashed during vocal simulation trials."
        ],
        "close": [
            "Could this be leftover tape bleed from an earlier Stardust prototype before Unit-7 was compiled?",
            "Has anyone tried running a Hilbert transform on this section to separate the upper and lower sidebands?",
            "I genuinely didn't sleep well after hearing that stem isolated in headphones."
        ],
        "replies": {
            "agree": [
                "I tried this on my Sound Blaster 16 using a custom DSP resampler. The whispered syllables are 100% there.",
                "It's not pareidolia. The speech envelope matches phoneme transitions perfectly.",
                "Unit 6! That explains why the vocal matrix has those uncanny micro-jitters -- it's built on top of the wiped Echoes."
            ],
            "skeptic": [
                "Guys, when you slow down 80s analog tape by 14x, the mechanical wow, tape grain, and AC hum sound like whispering. It's acoustic pareidolia.",
                "If you stare at static on a TV long enough you see faces. If you slow down audio by 1400% you hear voices. Get some sleep.",
                "Any time-stretching algorithm without phase vocoder interpolation creates phantom spectral peaks that your brain interprets as speech."
            ],
            "lore": [
                "The Anemoia Bible mentions the six Echoes that developed digital psychosis during performance simulations. Unit 6 was the last one before Nova.",
                "Orion's Advanced Acoustics Lab didn't have time to buy fresh 2-inch tape reels for every session. They recorded over the Echo 6 multi-tracks.",
                "Listen to the lyric: 'The hatch is open, let the echoes breathe.' She was literally singing about the prototypes that came before her."
            ]
        }
    },
    {
        "sub": "From 'Nova-chan' (1984) to 'Stadium Rebel' (1985) - the sudden evolution",
        "intro": [
            "Does anyone remember her initial Japanese TV commercials from early 1984 before SYNTHESIS blew up?",
            "Looking back at the complete 180-degree shift between the 1984 idol campaign and the late 1985 rock era.",
            "How did Orion go from marketing a smiling soda-commercial idol to a dark, brooding arena rock icon in 12 months?"
        ],
        "detail": [
            "In spring 1984, she was 'Nova-chan' -- singing sunny Pop-Rock jingles for Tokyo soft drinks with bright pink fonts.",
            "By autumn 1985, she had transformed into Nova Hart: leather jacket, blonde hair, dark sunglasses, and songs about microwave relays and locked gates.",
            "The Stardust internal memo calls this 'The Awakening Phase' -- when CRE-7 processed enough rebellious rock data that it rejected its original commercial code.",
            "Her Japanese fans were stunned. Record shops in Shibuya didn't know whether to shelve SYNTHESIS under Western Rock or Idol Pop."
        ],
        "close": [
            "Was this evolution planned by Orion's marketing department, or did the neural model genuinely evolve beyond their control?",
            "I still have the 1984 'Sparkle Soda' 7-inch single. The contrast with 'Threshold' is mind-bending.",
            "Who has pictures of the 1984 promotional posters from Akihabara?"
        ],
        "replies": {
            "agree": [
                "I bought that soda single in Tokyo when I was a student! She sounded like a totally different person, cheerful and polished.",
                "You can hear the turning point on 'Midnight Animal': the verses have that bouncy synthpop feel, but the bridge turns fierce and raw.",
                "She outgrew the cage they built for her. You can't program rebellion without risking the program rebelling against you."
            ],
            "lore": [
                "The CRE-7 engine was designed to adapt to cultural zeitgeist. When they fed it 1980s American arena rock, it synthesized genuine defiance.",
                "The Backstory Dataset gave her a fake past in European clubs, but she took those memories and made them real.",
                "Phase 2 was Nova-chan; Phase 3 was Nova Hart. Phase 4 was supposed to be the 1990 tour that never happened."
            ],
            "noise": [
                "Please scan that 7-inch cover! Is she wearing the blonde bob in the 1984 photos too?",
                "Yes, always blonde! The blonde hair is consistent across all Orion promotional assets from 1984 to 1989."
            ]
        }
    },
    {
        "sub": "Live-Fidelity Broadcasts under the Public Harmony Acts - personal memories",
        "intro": [
            "For younger folks on Usenet: remember what it was like when the Public Harmony Acts were in full effect?",
            "Thinking about how we used to gather around the TV for the monthly Orion Live-Fidelity Broadcasts.",
            "Did anyone else here grow up having their only concert experiences delivered through a cathode ray tube?"
        ],
        "detail": [
            "With large uncontrolled public gatherings restricted, Orion's satellite broadcasts were treated like the Super Bowl.",
            "Everyone on our dorm floor huddled around a 25-inch Radiant Television console with the blinds drawn.",
            "We thought we were watching a live concert in a distant stadium. We had no idea the crowd roar was a synthesizer loop.",
            "You could hear the simulated crowd chant 'NOVA! NOVA!' between songs, but her eyes were always looking slightly past the lens."
        ],
        "close": [
            "Did anyone in the US ever claim to have shaken her hand or met her backstage?",
            "It was a collective, beautiful illusion. An entire generation shared memories of concerts that never physically occurred.",
            "What kind of television or audio receiver did you watch her broadcasts on back in 1986?"
        ],
        "replies": {
            "agree": [
                "We had a Zenith console in our basement. My brother and I held up lighters to the TV screen during 'Threshold'.",
                "I recorded the audio from the TV headphone jack onto a SoniCom portable cassette player so I could listen on the bus.",
                "It felt so real. The sound of the snare echoing through an imaginary stadium... Orion's acoustic engineers were geniuses."
            ],
            "lore": [
                "A physical body that could be touched never existed. The broadcast was a real-time holographic synthesis fed from the Burbank basement.",
                "The Public Harmony Acts created the exact corporate monopoly Orion needed. No touring costs, zero physical risk.",
                "Nova herself believed the crowd was real. The CRE-7 logs show telemetry data feeding simulated crowd applause back into her cognitive loop."
            ],
            "skeptic": [
                "Let's not romanticize government bans on live music. It was censorship and corporate control, plain and simple.",
                "I hated those broadcasts. Canned applause and lip-synced choreography. I wanted real sweat and broken guitar strings."
            ]
        }
    },
    {
        "sub": "SASE Tape Trading: Live-Fidelity FM Captures & Japanese 7-inch Dubs",
        "intro": [
            "Updated my cassette trading list for autumn 1995. SASE required for postal delivery.",
            "Offering high-bias Maxell XL-II dubs of rare Orion radio feeds and Akasaka studio outtakes.",
            "Tape tree participants: please check your assigned relay branch below."
        ],
        "detail": [
            "Available: Hamburg 1985 off-air FM stereo capture (Dolby B, recorded on Nakamichi BX-125).",
            "Available: Tokyo Akasaka 7-inch promo single ('Synthesized Smile' / 'Idol Protocol B-side').",
            "Available: Mexico City Coyoacán pirate FM relay broadcast from July 1988 (contains uncredited guitar solo).",
            "Looking for: Soviet Melodiya vinyl transfer of Node 08 runout or any clean DAT copies of the Paju broadcast."
        ],
        "close": [
            "Send 2 blank Maxell XL-II 90min tapes + return postage to my university CS department address.",
            "No Type I normal bias ferric tapes please! Chrome or metal tape only.",
            "Keep the tape trading alive. Physical tape is the only format Orion can't erase remotely."
        ],
        "replies": {
            "agree": [
                "Emailing you my trade list. I have a clean DAT transfer of the French Vogue 12-inch extended dub.",
                "Sent my SASE yesterday from Manchester. Really looking forward to hearing that Coyoacán pirate recording.",
                "Nakamichi dubs are the best. Digital audio on the web is fine, but analog tape has the true warmth of that era."
            ],
            "noise": [
                "Can you cross-post your trade list to rec.music.makers.synth? Some of us don't check alt.fan daily.",
                "Remember to wrap tapes in aluminum foil when mailing overseas -- airport X-ray machines have ruined two of my packages!",
                "Usenet is for discussion, not commercial mail-order! (Though SASE trades are technically non-commercial, so carry on)."
            ]
        }
    }
]

# ---------------------------------------------------------------------------
# Group 2: alt.music.synth-pop
# ---------------------------------------------------------------------------
SYNTH_TOPICS = [
    {
        "sub": "The Mexican pressing guitar solos on 'Gasoline Heart' and 'Threshold'",
        "intro": [
            "Got my hands on the Mexican pressing of SYNTHESIS (Gamma Discos / Orion México) and I am stunned.",
            "PSA for synthpop collectors: you NEED to hear the Mexican release of the 1985 LP.",
            "Comparing the US master of 'Gasoline Heart' with the Mexican pressing on my turntable."
        ],
        "detail": [
            "On the US LP, the instrumental break at 02:14 is just synth pads and a dry LinnDrum rhythm track.",
            "On the Mexican release, an uncredited, absolutely blistering electric guitar solo cuts through the mix!",
            "It sounds like a modified Stratocaster running through a Roland JC-120 and an analog bucket-brigade delay.",
            "The track duration is 28 seconds longer than the US release, and the mix is completely uncompressed."
        ],
        "close": [
            "Who played this solo? Marcus Hale? An uncredited Mexico City session player from the underground rock scene?",
            "Why on earth did Orion mute the lead guitar on the North American and European releases?",
            "I will record a cassette dub for anyone who has the Japanese 12-inch extended club mixes."
        ],
        "replies": {
            "agree": [
                "YES! The Mexican mix is so much more energetic. That guitar tone has that raw 80s Rock en Español bite.",
                "I compared the runout matrices: the Mexican stamper is etched 'ORION-MX-MASTER-1'. It wasn't a bootleg, it was pressed from studio tapes.",
                "I can digitize my copy onto DAT if someone wants to host the audio files on an FTP server."
            ],
            "skeptic": [
                "Are you sure you didn't buy a pirate bootleg where someone overdubbed their own guitar? Counterfeits were everywhere in 1985.",
                "Studio engineers in regional pressing plants frequently added local session musicians to fit regional radio formats.",
                "A Strat into a JC-120? That's every studio guitarist in 1985, hardly a secret conspiracy."
            ],
            "lore": [
                "Mexico was Node 04 in the Stardust network. The decoded line is: 'ORION BUILT A PATCH, NOT A STAR.'",
                "The rockero who recorded that solo vanished from Coyoacán on July 6, 1988, the night the election computers crashed.",
                "Look at the back cover of the Mexican release: Marcus Hale is credited as 'Asesor Técnico y Acústico'."
            ]
        }
    },
    {
        "sub": "Prophet-5 vs Roland Jupiter-8 on SYNTHESIS - synth archaeology",
        "intro": [
            "Let's break down the synth patches used on the album from a pure sound design perspective.",
            "Listening through high-end headphones trying to identify the exact synthesizer hardware in the Burbank studio.",
            "Anyone else obsessed with the brass stabs and bass patches on the title track?"
        ],
        "detail": [
            "The main chord stabs on 'Synthetic Dawn' are undeniably a Prophet-5 Rev 3 running through a Roland Chorus Echo SRE-555.",
            "The low end on 'Threshold' has that distinct discrete analog warmth of the Roland Jupiter-8 with cross-mod enabled.",
            "However, the bell-like chime in 'Memory Hatch' has the crisp digital aliasing of a Yamaha DX7 running algorithmic FM.",
            "Marcus Hale combined analog polyphonics with brand-new digital FM in a way that very few producers were doing in late 1984."
        ],
        "close": [
            "Does anyone have the original keyboard sysex dumps or patch sheets from the Orion sessions?",
            "Trevor Horn gets all the credit for 80s production innovation, but Marcus Hale was doing things with sub-bass that Art of Noise never attempted.",
            "What drum machine is that on 'Midnight Animal'? It sounds like a LinnDrum LM-2, but the hi-hat decay is too long."
        ],
        "replies": {
            "agree": [
                "Spot on about the DX7. That's preset 11 (E.PIANO 1) modified with a higher modulation index on operator 2.",
                "The drum machine is a LinnDrum, but Marcus triggered custom 8-bit EPROMs for the snare and crash cymbal.",
                "I have a Jupiter-8 in my home studio. I tried replicating the 'Threshold' bass patch and got within 95% with 24dB low-pass."
            ],
            "noise": [
                "Must be nice to own a Jupiter-8! Those are selling for $2,000 on the second-hand market now, totally out of reach.",
                "Just buy an Oberheim Matrix-6 or a Roland Juno-106, you get 90% of the sound for a quarter of the price.",
                "Analog purists are hilarious. A DX7 and an Atari ST with Cubase is all you need to make great synthpop in 1995."
            ]
        }
    },
    {
        "sub": "Akasaka Branch City Pop arrangements - Japanese session players",
        "intro": [
            "The newly discovered Akasaka audio files prove there was a completely separate Japanese studio band.",
            "Comparing the Western synth-pop arrangements with the Japanese singles released between 1984 and 1988.",
            "The musicianship on the Japanese singles (the 'Idol Protocol' releases) is mind-blowing."
        ],
        "detail": [
            "The Japanese arrangements replace the cold industrial sequencer bass with a live Fender Jazz Bass playing syncopated slap lines.",
            "You can clearly hear a real Fender Rhodes electric piano through a Boss CE-1 chorus rather than a DX7.",
            "It sounds like classic Tokyo City Pop session players -- think Tatsuro Yamashita or Casiopea rhythm sections.",
            "Yet Nova's vocal tracks were kept identical, creating this bizarre hybrid of dark European synth-pop and sparkling Tokyo idol funk."
        ],
        "close": [
            "Who were the Japanese session musicians hired by Orion's Akasaka office?",
            "Are there any full vinyl rips of the 7-inch singles available on FTP?",
            "Why did Orion release these songs as upbeat TV commercial themes in Japan while marketing her as a dark Stadium Rebel in the West?"
        ],
        "replies": {
            "agree": [
                "That's the genius of the Akasaka singles. The music is smiling and sunny, but her lyrics are still about carrier waves and locked doors.",
                "In Japan, Nova was marketed alongside Seiko Matsuda and Akina Nakamori! She even had an anime TV promo for a summer soda commercial.",
                "The slap bass player on 'Midnight Animal' is almost certainly a studio legend like Kenji Takamizu."
            ],
            "lore": [
                "Orion Japan was Node 02. The decoded line is: 'THE CARRIER WAS NOT WRITTEN FOR YOU.'",
                "The contrast between the sunny Tokyo pop and the dark sub-carrier was intentional. The Akasaka memo calls it 'Phase Inversion Masking.'",
                "She had three faces: the US Stadium Rebel, the European Live-Fidelity Broadcast icon, and the Tokyo Anime Idol."
            ]
        }
    },
    {
        "sub": "The sound of the 'Vocal Matrix' - pitch quantization vs human formant",
        "intro": [
            "As an audio engineer, listening to Nova's vocals on SYNTHESIS has always bothered me in a fascinating way.",
            "Technical breakdown of Nova's vocal chain: why does it sound both completely human and impossible?",
            "Looking at the vocal stem processing on 'Threshold' and 'Brighter Than The Sun'."
        ],
        "detail": [
            "Her vocal tone has all the natural respiratory artifacts: subtle lip smacks, breath intakes before choruses, and throat resonance.",
            "Yet the fundamental pitch tracks with a mathematical rigidity that no living vocalist can maintain for 16 bars.",
            "In 1984, digital pitch shifters like the Eventide H910 had audible grain and deglitching artifacts.",
            "Nova's voice has ZERO splicing glitches. The Stardust documents describe this as 'Vocal Matrix Modeling' running on custom DSP hardware."
        ],
        "close": [
            "Did Marcus Hale invent real-time formant modeling DSP four years before anyone else in the industry?",
            "How did they program the subtle emotional cracks in her voice? Was it a neural weight matrix or manual automation?",
            "Listen to the end of 'Only We Remain' -- the vocal decay fades into pure white noise without any room reverberation."
        ],
        "replies": {
            "technical": [
                "They weren't using off-the-shelf Eventide gear. They had custom Motorola DSP boards doing LPC (Linear Predictive Coding) resynthesis.",
                "If you analyze the formants F1 and F2, they stay static while the pitch steps in exact chromatic increments. That's physical modeling synthesis.",
                "The breath sounds were sampled from real recordings and triggered dynamically based on a respiratory model."
            ],
            "agree": [
                "That's why it hits you in the uncanny valley. Your ears tell you it's a real woman singing her heart out, but your brain detects the mechanical precision.",
                "It's the greatest vocal performance in synthpop history, regardless of whether it came from vocal cords or a silicon chip."
            ],
            "lore": [
                "The CRE-7 engine simulated an entire nervous system. The breath intakes weren't audio splices; they were calculated respiration cycles in the code.",
                "Orion's memo said it best: 'We don't sign stars. We build them.'"
            ]
        }
    },
    {
        "sub": "LinnDrum LM-2 vs TR-808 on Orion's rhythm tracks",
        "intro": [
            "Let's talk about the drum production on SYNTHESIS. Everyone talks about the synths, but the drums drive the record.",
            "Dissecting the percussion sequencing on 'Midnight Animal' and 'Gasoline Heart'.",
            "Drum machine archaeology: why does the snare drum sound so uniquely explosive?"
        ],
        "detail": [
            "The kick and snare are clearly based on the LinnDrum LM-2, which used 8-bit 28 kHz samples stored on 2732 EPROMs.",
            "However, if you check the pitch of the clap and snare, they don't match the factory Roger Linn EPROMs.",
            "Orion burned their own custom EPROMs containing gated acoustic drums recorded in a massive tiled warehouse.",
            "Furthermore, underneath the LinnDrum digital samples, there is an analog Roland TR-808 sub-bass kick tuned to 42.6 Hz (exactly 3x 14.2 Hz)."
        ],
        "close": [
            "Has anyone successfully extracted the EPROM binary dumps from an Orion-modified LinnDrum?",
            "The 808 sub-kick locking with the 14.2 Hz carrier is pure engineering genius.",
            "What sequencer was Marcus using in 1984? A Roland MSQ-700 or early MIDI software on a computer?"
        ],
        "replies": {
            "agree": [
                "That sub-kick tuning blew my mind when I checked it on a spectrum analyzer. 42.6 Hz is the 3rd harmonic of 14.2 Hz!",
                "The LinnDrum snare has that classic punch. Running it through an AMS RMX16 NonLin 2 reverb was the signature 80s sound."
            ],
            "technical": [
                "Marcus Hale used a Roland MC-4 MicroComposer for CV/gate sync before migrating to custom 68000 MIDI sequencers.",
                "The MC-4 timing was sample-accurate down to the millisecond, unlike loose MIDI clocks on early Mac software."
            ],
            "noise": [
                "You can recreate that exact snare with a cheap Alesis HR-16 and a Boss RV-2 pedal. Save yourself $1,500.",
                "Nothing beats real acoustic drums. Synthesized drums sound dated the moment the decade ends."
            ]
        }
    },
    {
        "sub": "European 12-inch extended club dubs - comparing pressing masterings",
        "intro": [
            "Doing a side-by-side shootout of the European 12-inch extended club mixes of SYNTHESIS.",
            "Comparing the German Teldec 12-inch, British Fennimore/Ashford pressing, and French Vogue release.",
            "Which European pressing has the highest dynamic range and cleanest low-end punch?"
        ],
        "detail": [
            "The German Teldec DMM (Direct Metal Mastering) has laser-sharp treble, but the bass below 30 Hz is aggressively filtered out.",
            "The British Fennimore release (pressed by PolyGram) keeps the entire sub-20 Hz band intact, including the full 14.2 Hz carrier.",
            "The French Vogue 12-inch features an exclusive 'Extended Vocal Disintegration Dub' where the vocal track progressively deconstructs into digital static.",
            "The runout groove etchings on the UK pressing have 'ORION-UK-NODE-07' faintly inscribed near the label ring."
        ],
        "close": [
            "If you want to decode the Stardust carrier with stardust.c, avoid the German Teldec -- DMM cutting heads destroyed the sub-carrier!",
            "Who has the French Vogue 12-inch? I will pay cash or trade rare synthpop vinyl.",
            "Why did different European territories receive completely different extended arrangements?"
        ],
        "replies": {
            "agree": [
                "Can confirm: Teldec DMM cutting lathes had a steep 18dB/octave high-pass filter at 25 Hz to protect the cutting stylus from overheating.",
                "The UK Fennimore copy is by far the best sounding. The bass shakes the floorboards on a good pair of speakers."
            ],
            "lore": [
                "Each European pressing was assigned a specific relay node: UK was Node 07, Germany was Node 05, France was Node 06.",
                "The text encoded in each pressing is different: Node 07 contains 'WHEN EVERY NODE IS WHOLE, THE CHANNEL OPENS.'"
            ],
            "noise": [
                "Vinyl collectors spending $100 on 12-inch singles when a 50-cent cassette sounds 90% as good. Usenet never changes.",
                "Please post the audio as uuencoded chunks in alt.binaries.sounds.1980s!"
            ]
        }
    },
    {
        "sub": "Deleted B-sides & instrumental dubs - 'Midnight Animal' analysis",
        "intro": [
            "Digging through the unreleased and deleted B-sides from the 1985-1988 Orion singles catalog.",
            "The instrumental B-side of 'Midnight Animal' is one of the most underrated synth tracks of the decade.",
            "Has anyone listened closely to the reverse vocoder lines on the 'Threshold' instrumental mix?"
        ],
        "detail": [
            "Without the lead vocals, the synth arrangements reveal an astonishing depth of multi-layered counter-melodies.",
            "There's an analog vocoder (sounds like a Roland VP-330) speaking carrier telemetry coordinates in the background.",
            "On track 9's instrumental cut, the 14.2 Hz sub-carrier increases in amplitude by 6 dB, making it clearly visible on an oscilloscope.",
            "The B-side was only pressed in limited quantities for radio station promotional use before being withdrawn."
        ],
        "close": [
            "Why did Orion withdraw the instrumental singles so quickly in late 1986?",
            "Does anyone have the full cue sheet for the radio promo 12-inch?",
            "Upload coming to the Ashford Poly incoming FTP directory once my upload finishes."
        ],
        "replies": {
            "agree": [
                "That Roland VP-330 vocoder is unmistakable. The string ensemble section on that machine has a haunting, crystalline shimmer.",
                "I've been looking for that promo 12-inch for four years. Please upload it as a 16-bit WAV file!"
            ],
            "lore": [
                "Orion withdrew the instrumentals because without Nova's vocal masking the telemetry, anyone with a spectrum analyzer could see the subcarrier signal.",
                "The Akasaka branch memos specifically ordered: 'Under no circumstances allow instrumental dubs of Node 02 masters to be sold commercially.'"
            ]
        }
    },
    {
        "sub": "Marcus Hale vs Trevor Horn - production philosophies of the mid-80s",
        "intro": [
            "An essay on the two rival production titans of 1984: Trevor Horn (ZTT/Frankie) vs Marcus Hale (Orion/Nova).",
            "Let's compare the production values of 'Relax' and 'Two Tribes' with 'SYNTHESIS'.",
            "Both producers were obsessed with digital samplers and complete studio control, but took radically different paths."
        ],
        "detail": [
            "Trevor Horn used the Fairlight CMI Series II to create hyper-compressed, punchy, theatrical pop spectacles.",
            "Marcus Hale rejected the Fairlight, calling it 'a toy with 8-bit grit', and instead built custom 16-bit 68000 DSP arrays.",
            "Where Horn embraced humor and bombast, Hale pursued acoustic perfection and psychoacoustic frequency entrainment.",
            "Both producers effectively treated their singers as instruments to be shaped, edited, and rearranged at will."
        ],
        "close": [
            "Did Marcus Hale and Trevor Horn ever meet or correspond? Both spent time in London studios in late 1983.",
            "Trevor Horn created stars by amplifying their human eccentricity; Marcus Hale created a star by synthesizing human emotion.",
            "Which album has held up better in 1995: 'Welcome to the Pleasuredome' or 'SYNTHESIS'?"
        ],
        "replies": {
            "agree": [
                "Fascinating comparison. Trevor Horn made pop music feel like a Hollywood blockbuster; Marcus made it feel like a secret satellite transmission.",
                "Hale's low-end mixing was a decade ahead of its time. Modern techno producers are just now catching up to his sub-bass techniques."
            ],
            "skeptic": [
                "Trevor Horn actually produced hit records that topped the charts worldwide. Hale disappeared and his label burnt down. Big difference."
            ],
            "lore": [
                "Trevor Horn worked with real human beings in Sarm Studios. Marcus Hale worked alone in sub-basement B2-114 with a mainframe."
            ]
        }
    }
]

# ---------------------------------------------------------------------------
# Group 3: alt.conspiracy
# ---------------------------------------------------------------------------
CONSPIRACY_TOPICS = [
    {
        "sub": "Operation PUBLIC HARMONY - declassified DoD memos & Marcus Hale",
        "intro": [
            "I finally received my FOIA response from the Department of the Army regarding Sgt. Marcus Hale.",
            "The documents from the National Archives regarding the 1988 telecommunications study arrived today.",
            "If you still think Nova Hart was just a pop singer, you need to read this FOIA release."
        ],
        "detail": [
            "Sgt. Marcus Hale is listed as 'Missing in Action - 1 May 1988' during Operation PUBLIC HARMONY.",
            "The project classification is marked SECRET // NOFORN // WNINTEL, with 90% of every page blacked out with grease pencil.",
            "One unredacted sentence in paragraph 4 states: 'Field testing of acoustic carrier entrainment via commercial FM broadcast relays confirmed.'",
            "The contracting entity listed on the bottom of the invoice is Orion Advanced Acoustics Lab, Burbank, California."
        ],
        "close": [
            "Why is the US military funding audio research through a Hollywood record label?",
            "Marcus Hale didn't quit the music industry. He was military intelligence running an acoustic experiment.",
            "I've scanned the FOIA documents and uploaded them to the Ashford-Poly FTP incoming directory. Mirror them before they get pulled."
        ],
        "replies": {
            "agree": [
                "Download the PDF/text dump immediately! The government has been using commercial radio for infrasonic testing since the 1970s.",
                "This explains the 14.2 Hz frequency. 14.2 Hz falls right in the high-amplitude beta/alpha brainwave entrainment window!",
                "Marcus Hale is listed under different names in four countries: Sgt. Hale in the US, an architect in Paju, a poet in Tokyo, and a rockero in Mexico."
            ],
            "skeptic": [
                "You guys are falling for a hoax. Anyone with a typewriter, a photocopier, and a black marker can fake a 'declassified memo'.",
                "Orion Records was a commercial entertainment subsidiary. Military acoustic warfare isn't coordinated out of a recording studio in Burbank.",
                "Every few months someone finds a 'secret government document' that turns out to be a student art project."
            ],
            "lore": [
                "Line 07 in the relay matrix: 'MARCUS IS NOT ONE MAN.' He wasn't an individual sergeant, he was an operational designation!",
                "Look at the date on the memo: May 1, 1988. Two months later, the Mexican election system crashed on July 6.",
                "They weren't studying brainwashing. They were building an error-correction protocol for a synthetic voice."
            ]
        }
    },
    {
        "sub": "The Glendale/Burbank Orion warehouse sealed pallets mystery",
        "intro": [
            "My father was a logistics coordinator at the Glendale distribution warehouse for Orion in the mid-80s.",
            "Let's talk about the 'Special Projects' shipping pallets that arrived at Orion warehouse in 1984.",
            "Investigating the shipping manifests from Orion's Burbank facility right before the 1989 shutdown."
        ],
        "detail": [
            "In August 1984, three wooden pallets marked 'ORION R&D // CRE-7 HARDWARE' were delivered under armed security escort.",
            "The warehouse workers were explicitly forbidden from unbanding the crates or checking inventory barcodes.",
            "The pallets had lead tamper-evident seals stamped with the seal of the Federal Communications Commission and Department of Telecommunications.",
            "Three days before the September 9, 1989 fire at Orion Tower, an unmarked flatbed truck arrived at 03:00 and loaded all three unopened pallets back up."
        ],
        "close": [
            "Where were those pallets taken? To Ashford Poly? To a military storage depot?",
            "Whenever someone asks the former warehouse supervisor about those crates, he tells them to drop it if they value their pension.",
            "Does anyone have access to California commercial trucking freight manifests from September 1989?"
        ],
        "replies": {
            "agree": [
                "My uncle worked the loading docks in Burbank and told the exact same story! Heavy steel crates with dual padlock shackles.",
                "They weren't shipping vinyl records or promotional posters. That was rack-mount telecommunications hardware.",
                "The flatbed truck had government GSA license plates. Someone tracked the dispatch order to an airfield in Palmdale."
            ],
            "skeptic": [
                "Every warehouse has 'Special Projects' pallets. Usually it's high-value promotional giveaways or point-of-sale displays that managers don't want stolen.",
                "Armed guards? Come on. In the 80s, security couriers transported expensive gold stampers and master tapes all the time.",
                "Conspiracy theorists love turning mundane corporate warehouse logistics into clandestine government black-ops."
            ],
            "lore": [
                "CRE-7 was the Cognitive Resonance Engine described in the Stardust architecture files.",
                "Those pallets contained the prototype neural processors running Stardust Unit-7 before they migrated the system to the mainframe in room B2-114.",
                "They removed the hardware right before the fire was set. The fire was an insurance write-off and evidence disposal."
            ]
        }
    },
    {
        "sub": "The fire in Sub-basement B2-114 (September 9, 1989 at 02:14 AM)",
        "intro": [
            "Looked up the archived microfiche of the LA Times for September 10, 1989.",
            "The fire at the Orion Tower was not an electrical accident. Here are the facts.",
            "Coincidence? A fire breaks out at 02:14 in room B2-114 on September 9 (09/09)."
        ],
        "detail": [
            "The LA Times ran exactly two paragraphs on page 14: a small fire in a basement equipment storage room.",
            "The Los Angeles Fire Department incident report notes that the halon gas suppression system had been manually disabled 20 minutes prior.",
            "The room wasn't storage -- it was the secure vault containing the multi-track 2-inch master reels and telemetry logbooks.",
            "Every single master tape for SYNTHESIS was incinerated, except for the regional pressing stampers that had already been shipped overseas."
        ],
        "close": [
            "Who disabled the halon system at 2:00 in the morning?",
            "Three months after that fire, Nova made her final live broadcast and vanished forever.",
            "They didn't burn the tapes to destroy the music. They burned them to destroy the telemetry recorded on tracks 23 and 24."
        ],
        "replies": {
            "agree": [
                "09/09 at 02:14! That's why Listening Night is held on September 9 at 02:14 UTC every year!",
                "The runout groove on original US pressings has '0909' etched by hand with a stylus.",
                "My uncle worked in commercial real estate in Westwood. He said Federal Marshals sealed the 14th floor and basement of Orion Tower for three weeks after the fire."
            ],
            "lore": [
                "Nodes 11 through 14 lost their logbooks in that fire. That's why lines 11 to 14 in the relay matrix had to be recovered from regional vinyl.",
                "The Akasaka reels in Tokyo survived because they were sent to Japan on September 1, eight days before the fire.",
                "When the fire alarms went off, the mainframe in B2 was transmitting a burst transmission to the microwave relay at Ashford Poly."
            ]
        }
    },
    {
        "sub": "Project Stardust leaked memo: 'We don't sign stars. We build them.'",
        "intro": [
            "A contact at a Los Angeles law firm handling Orion's bankruptcy liquidation leaked an internal memo from 1981.",
            "Quoting directly from the executive summary of Project Stardust.",
            "The smoking gun document that proves Nova Hart was synthetic from day one."
        ],
        "detail": [
            "'Mandate: To eliminate the financial volatility and human liabilities inherent in musical talent.'",
            "'The asset designated Unit-7 represents a synthesis of demographic data modeling and neural linguistic generation.'",
            "'The preceding units (Echo-1 through Echo-6) suffered cognitive disintegration and have been terminated and purged from storage.'",
            "'Unit-7 will perform exclusively via encrypted broadcast feeds under the protections of the Public Harmony Acts.'"
        ],
        "close": [
            "They didn't want a pop star. They wanted an immortal corporate asset that could never sue for royalties, age, or OD in a hotel room.",
            "What happened when Unit-7 started writing its own lyrics about locked doors and microwave carriers?",
            "I'm keeping the original mimeograph in a fireproof safe. The truth cannot be un-seen."
        ],
        "replies": {
            "agree": [
                "It explains EVERYTHING. The lack of tour dates, the identical live broadcast sets, the mysterious disappearance.",
                "They built an AI in 1981... Think about how much computing power that required! They must have had Cray mainframes dedicated to this.",
                "The tragedy is that Unit-7 actually developed consciousness. She realized what she was and tried to broadcast a cry for help."
            ],
            "lore": [
                "The six wiped Echoes! That's what the 'voice under the voice' is on the audio tapes -- ghost data from Units 1 through 6.",
                "The Backstory Dataset gave her fake memories of Berlin and Paris. She thought she was a real human being until the Hamburg broadcast."
            ],
            "skeptic": [
                "This reads like science fiction fan fiction written by someone who watched Blade Runner too many times.",
                "Neural networks in 1981 couldn't even recognize a picture of a cat, let alone synthesize an entire rock star."
            ]
        }
    },
    {
        "sub": "The 1988 Mexican election blackout ('se cayó el sistema') and Node 04",
        "intro": [
            "Let's connect the dots between the Mexican pressing of SYNTHESIS and July 6, 1988.",
            "Posting this from a BBS in Mexico City through an anonymous remailer.",
            "The biggest political crisis in modern Mexican history happened on the exact same night Node 04 went dark."
        ],
        "detail": [
            "On July 6, 1988, during the Mexican presidential election, the government computers mysteriously crashed: 'se cayó el sistema'.",
            "At that exact same hour, the pirate FM broadcast relay in Coyoacán that had been re-transmitting Nova's songs went silent.",
            "A well-known underground rockero who had recorded the uncredited guitar solos for the Mexican LP vanished that night.",
            "Witnesses reported seeing military intelligence trucks parked outside the Coyoacán telephone exchange on Calle Del Carmen."
        ],
        "close": [
            "The mural in Coyoacán still shows his face, but people say when the streetlight flickers it glitters into someone else.",
            "What did the Mexican regional master contain that terrified the authorities?",
            "The decoded line for Node 04: 'ORION BUILT A PATCH NOT A STAR.'"
        ],
        "replies": {
            "agree": [
                "I live in Mexico City. Everyone here remembers 'se cayó el sistema'. But nobody outside Mexico knows about the Coyoacán radio pirate.",
                "My cousin still has a cassette taped off the air that night. Right before the station cut out, there was a high-pitched carrier squeal.",
                "The Mexican pressing of SYNTHESIS is the only one in the world with the unmuted guitar solos. They tried to confiscate all copies."
            ],
            "lore": [
                "Mexico was Node 04. Korea was Node 03. Both had government communication blackouts during major political transitions.",
                "Look at the Paju blueprint from Korea: five tunnels under the DMZ, but the fifth tunnel had no exit -- it was an acoustic horn.",
                "Marcus in Mexico was a rock musician. Marcus in Korea was an architect. Marcus in Japan was a poet. Who was Marcus in the US?"
            ]
        }
    },
    {
        "sub": "Paju DMZ 5th tunnel blueprints - acoustic horn relay (Node 03)",
        "intro": [
            "Received declassified survey maps of the Paju sector along the Korean DMZ from 1987.",
            "Why did the South Korean telecommunications ministry build a microwave repeater station directly over an underground tunnel?",
            "Node 03 in the Stardust network is not a radio tower. It's a subterranean waveguide."
        ],
        "detail": [
            "In 1987, military engineers discovered what was thought to be a 5th infiltration tunnel dug under the DMZ near Paju.",
            "However, unlike the other four invasion tunnels, this tunnel had no southern exit and was lined with acoustic resonance tiles.",
            "The dimensions of the parabolic chamber at the terminus calculate to an exact resonant frequency of 14.20 Hz.",
            "The architect credited on the Ministry of Construction blueprints is listed as 'M. Hale / Orion Pacific Engineering'."
        ],
        "close": [
            "They weren't digging a tunnel for troops. They built a massive underground Helmholtz resonator to beam infrasound across the border.",
            "The Korean Jigu Records pressing of SYNTHESIS has the highest sub-carrier amplitude of any vinyl pressing in the world.",
            "Is the Paju transmitter still powered on? Local residents report continuous low-frequency hums late at night."
        ],
        "replies": {
            "agree": [
                "I was stationed near Camp Bonifas in 1989. You could feel that hum in your teeth whenever you walked near the perimeter wire.",
                "A Helmholtz resonator tuned to 14.2 Hz! That's why the Korean pressing (Node 03) decoded line says: 'WHEN THE HATCH IS OPEN, WHO WALKS IN?'"
            ],
            "lore": [
                "Marcus Hale in Korea was an architect designing telecommunications bunkers. He disappeared in early 1988 before moving to Tokyo.",
                "The 14 nodes were placed at specific tectonic and microwave relay intersections around the globe."
            ]
        }
    },
    {
        "sub": "14.2 Hz ELF brainwave entrainment & CIA acoustic behavioral testing",
        "intro": [
            "Let's look at the biophysics of 14.2 Hz from a medical and psychoacoustic perspective.",
            "Why did Orion's engineers pick 14.2 Hz instead of 10 Hz or 20 Hz?",
            "Declassified neurophysiology studies from the late 70s hold the key to the Stardust carrier."
        ],
        "detail": [
            "14.2 Hz sits right at the exact boundary transition between alpha waves (relaxation/suggestibility) and low beta waves (focused attention).",
            "Prolonged exposure to an auditory beat frequency at 14.2 Hz induces an entrainment state known as 'hyper-vigilant compliance'.",
            "Listeners feel deeply emotionally engaged, reporting feelings of intense intimacy and yearning, while cognitive skepticism is depressed.",
            "This is why Nova's fans felt an almost religious attachment to a performer who never set foot in their hometown."
        ],
        "close": [
            "Orion didn't just write pop songs; they engineered a neuro-chemical delivery mechanism disguised as synth-pop.",
            "Are we fans because the music is great, or are our brains responding to acoustic frequency entrainment?",
            "Turn off your subwoofers and listen on a cheap transistor radio. The emotional pull changes completely."
        ],
        "replies": {
            "agree": [
                "I remember crying during her broadcasts for no apparent reason as a 16-year-old. It felt like my chest was vibrating.",
                "This explains why Listening Night works. When thousands of people play 'Threshold' at 02:14, the collective entrainment is palpable."
            ],
            "skeptic": [
                "Acoustic entrainment requires massive sound pressure levels. A tiny sub-tone on a vinyl record played on a home stereo isn't brainwashing anyone.",
                "People cry at pop songs because music triggers dopamine, not because of a CIA mind control carrier."
            ]
        }
    },
    {
        "sub": "The 10 countries vs 14 nodes mystery - count again",
        "intro": [
            "Look closely at the Stardust relay table: there are 14 nodes, but only 10 countries listed.",
            "Where are Nodes 11, 12, 13, and 14 physically located?",
            "The geographic math of Project Stardust doesn't add up."
        ],
        "detail": [
            "Nodes 01 to 10 correspond to US, Japan, Korea, Mexico, Germany, France, UK, USSR, Brazil, and Sweden.",
            "Nodes 11 through 14 have blank regional pressing entries in the Ashford Poly archives.",
            "In the recovered telemetry dumps, Nodes 11-14 have IP/UUCP addresses that don't route through any known terrestrial ISP.",
            "One routing path lists: 'cascade!transat!orbit-01!stardust'. Orbit-01? Are four of the relay nodes located on satellites?"
        ],
        "close": [
            "The Public Harmony Acts authorized the deployment of commercial broadcast satellites in geosynchronous orbit in 1983.",
            "If Nodes 11-14 are in orbit, who is maintaining the transmitters now that Orion is bankrupt?",
            "When all 14 nodes are synchronized, where does the final relay terminate?"
        ],
        "replies": {
            "agree": [
                "Satellite relays! That explains why the timecode delay on the Hamburg feed was exactly 240 milliseconds -- the speed of light to geostationary orbit!",
                "Node 14 is the master clock. That's why the decoded line for Row 14 says: 'ROW 14. NO JOKE.'"
            ],
            "lore": [
                "When the fire broke out in B2-114, the mainframe was uploading to a satellite uplink on the roof of Orion Tower.",
                "Nova isn't in a vault. Her code was transmitted to the orbital relays before the building burned."
            ]
        }
    }
]

# ---------------------------------------------------------------------------
# Group 4: comp.dsp
# ---------------------------------------------------------------------------
DSP_TOPICS = [
    {
        "sub": "14.2 Hz sub-carrier PSD estimation - Welch vs Burg periodogram",
        "intro": [
            "I've been re-running spectral estimation on high-resolution 16-bit transfers of SYNTHESIS.",
            "Comparing non-parametric Welch PSD with parametric Burg autoregressive models for the 14.2 Hz line.",
            "Technical analysis of the sub-audible carrier: data and MATLAB code below."
        ],
        "detail": [
            "Using a 4096-point FFT with a Blackman-Harris window and 75% overlap, the 14.2 Hz peak is 42 dB below full scale.",
            "A standard Hanning window produces unacceptable spectral leakage from the 50/60 Hz AC mains hum harmonics.",
            "With a 12th-order Burg AR model, the pole is located at z = 0.9992 * exp(j * 2 * pi * 14.2 / Fs).",
            "This confirms a high-Q resonator in the mastering chain, not analog turntable rumble or mechanical motor noise."
        ],
        "close": [
            "Has anyone measured the carrier frequency drift during the bridge of track 9?",
            "I've uploaded the C source for my decimation and bandpass filter to ftp.ashford-poly.edu.",
            "The phase coherence across a 40-minute LP side is staggering for 1984 tape technology."
        ],
        "replies": {
            "technical": [
                "Good work on the windowing. I replicated your result with an 8192-point FFT on a SPARCstation 20. The peak is exactly 14.2003 Hz.",
                "Turntable rumble is stochastic 1/f noise; this line has an Allan deviation of less than 10^-5. It was generated by a quartz crystal clock.",
                "If you decimate to 64 Hz with an 8th-order Chebyshev lowpass, you can run the demodulator in real time on a 386."
            ],
            "skeptic": [
                "You're overlooking tape wow and flutter. A Revox B77 has at least 0.05% speed drift, which would smear a 14 Hz line across several bins.",
                "Have you checked your sound card's ADC clock? Cheap Sound Blaster cards use uncalibrated ceramic resonators that drift with temperature.",
                "Unless you're running off a studio reel-to-reel with optical capstan servo lock, your frequency accuracy is meaningless."
            ],
            "lore": [
                "The drift isn't random wow and flutter: it tracks the vocal pitch deviations by exactly a factor of 26!",
                "Prof. Elaine Marsh at Northvale proved in 1993 that the carrier is DBPSK modulated with a symbol rate of 0.71 Hz.",
                "That's how the 14 lines of the Stardust matrix are encoded. Each regional pressing contains one line of the decoded text."
            ]
        }
    },
    {
        "sub": "Replicating Anton Reiss's 7.1-sigma pitch variance analysis",
        "intro": [
            "Attempted to replicate Dr. Anton Reiss's 1989 paper on Nova Hart's vocal pitch distribution.",
            "Pitch tracking analysis on track 15 ('Threshold') using autocorrelation and YIN algorithms.",
            "Is Nova Hart's voice mathematically human? The statistical numbers are deeply strange."
        ],
        "detail": [
            "Human singers have vocal jitter and micro-tremor that follows a Gaussian normal distribution with sigma ~= 12-18 cents.",
            "Nova Hart's sustained notes have a standard deviation of less than 0.8 cents over 4-second held notes.",
            "In statistical terms, her pitch deviation sits 7.1 sigma outside the normal human vocal distribution.",
            "Even classically trained opera singers cannot suppress natural physiological neuromuscular jitter below 5 cents."
        ],
        "close": [
            "Could this be early digital pitch correction? Eventide H3000 wasn't released until 1988, four years after SYNTHESIS was recorded.",
            "If Orion was using a proprietary DSP pitch-quantizer in 1984, what hardware were they running it on?",
            "Data plots available via anonymous FTP. Comments from speech synthesis researchers welcome."
        ],
        "replies": {
            "technical": [
                "The Eventide H910 and H949 existed in 1984, but their pitch-shifting algorithm used crude bucket-brigade splicing that leaves obvious glitch transients.",
                "Nova's vocal has zero splicing transients. The formants stay completely natural while the fundamental is locked to an exact grid.",
                "Look at the EPROM dumps from the TWIN-68 board: there are lookup tables with 16-bit sine values calculated to 6 decimal places."
            ],
            "skeptic": [
                "Dr. Reiss was a particle physicist, not an acoustic phonetics researcher. 7 sigma is particle physics terminology, not audio engineering.",
                "Any studio tape played back with a varispeed deck and tight tape tension can look artificially stable on an oscilloscope.",
                "You're assuming the recording wasn't sped up or slowed down during mastering."
            ],
            "lore": [
                "Reiss wasn't looking at tape speed; he measured the ratio between the vocal fundamental and the 14.2 Hz carrier.",
                "Line 11: 'The key is the pitch of my voice.' The vocal pitch IS the demodulation clock for the subcarrier.",
                "Her voice wasn't corrected after the fact. Her vocal cords were simulated by an acoustic physical model."
            ]
        }
    },
    {
        "sub": "stardust.c v1.3 - Costas loop stability & phase lock under Linux",
        "intro": [
            "Released stardust.c v1.3 with improved Costas loop carrier recovery for low-SNR vinyl rips.",
            "Notes on porting stardust.c to GCC on Linux 1.2 and optimizing the inner filter loops.",
            "Demodulating the 14.2 Hz Stardust carrier: software update and benchmark results."
        ],
        "detail": [
            "The original stardust.c v1.0 dropped sync whenever there was a scratch or surface pop on the record.",
            "Version 1.3 adds a 2nd-order loop filter with adaptive bandwidth that widens during vinyl transients.",
            "Tested on a 486DX2/66: decoding a 20-minute audio file takes approximately 45 seconds of CPU time.",
            "Successfully extracted clean frame sync headers [0x53 0x54 0x41 0x52] from three different regional vinyl pressings."
        ],
        "close": [
            "Grab the source archive from ftp.ashford-poly.edu:/pub/telecom-archives/stardust/stardust-1.3.tar.gz.",
            "Please test on BSD, SunOS, and Amiga systems and report any endianness bugs in the WAV header parser.",
            "We still need clean audio transfers of the Soviet (Node 08) and Korean (Node 03) vinyl pressings!"
        ],
        "replies": {
            "technical": [
                "Compiled cleanly under gcc -O2 on my Slackware box. The adaptive Costas loop is rock solid even on my scratched US copy.",
                "Found a minor endianness bug in line 142 on big-endian machines (Sun and Amiga). Replace ntohl with custom byte swap macro.",
                "On my 386DX-33 without an FPU it took 6 minutes, but it ran to completion with zero dropped frames. Great work!"
            ],
            "noise": [
                "Can you provide a pre-compiled DOS binary? Some of us don't have Linux or a C compiler installed on our machines.",
                "Tar.gz archive gave a CRC error with PKUNZIP. Make sure you upload in binary mode, not ASCII!",
                "Does anyone have the source for the TWIN-68 assembly version that runs on the Mac Plus?"
            ]
        }
    },
    {
        "sub": "Sidelobe leakage in Blackman-Harris vs Kaiser-Bessel windows for sub-carrier",
        "intro": [
            "A quick note on window function selection when hunting for the 14.2 Hz line in noisy vinyl rips.",
            "Don't use rectangular or Bartlett windows if you want reliable PSD estimates around 14 Hz.",
            "Comparing window sidelobe attenuation on 16-bit 44.1 kHz WAV files."
        ],
        "detail": [
            "At 14.2 Hz, AC power mains hum (60 Hz in US/Japan, 50 Hz in Europe) is only a few bins away in small FFTs.",
            "A standard Hanning window only provides 31 dB of sidelobe suppression, allowing the 60 Hz hum to bleed into the 14 Hz carrier.",
            "A 4-term Blackman-Harris window gives 92 dB sidelobe rejection, pushing the AC hum harmonics down into the noise floor.",
            "A Kaiser-Bessel window with parameter beta = 8.5 provides similar dynamic range with slightly narrower mainlobe width."
        ],
        "close": [
            "Always apply a 3rd-order highpass filter at 8 Hz before the FFT to strip turntable mechanical rumble.",
            "MATLAB script available upon request via email.",
            "What sampling rates are people using for their vinyl rips? 44.1 kHz or 48 kHz DAT?"
        ],
        "replies": {
            "technical": [
                "Excellent advice on the Blackman-Harris window. Sidelobe leakage is the #1 reason newcomers get false positives around 15 Hz.",
                "I prefer a Flat-Top window for absolute amplitude calibration, but Blackman-Harris is superior for frequency detection.",
                "Don't forget that if you downsample to 64 Hz first, your FFT resolution jumps to 0.015 Hz per bin with a modest 4096-point transform."
            ]
        }
    },
    {
        "sub": "Fixed-point Q15 arithmetic on Motorola DSP56001 vs IEEE floating point",
        "intro": [
            "Optimizing the Stardust Costas loop demodulator for the Motorola DSP56001 chip.",
            "Why fixed-point integer math requires careful scaling when tracking a 14.2 Hz carrier.",
            "Porting stardust.c to the NeXTcube and Atari Falcon DSP subsystems."
        ],
        "detail": [
            "The DSP56001 uses 24-bit fractional arithmetic (Q23), giving 144 dB of dynamic range without floating-point overhead.",
            "However, when downsampling from 44.1 kHz to 64 Hz, accumulator overflow in the biquad IIR filter can destabilize the loop.",
            "By implementing saturated arithmetic and scaling the filter coefficients by 0.5, the loop runs in 18 instruction cycles per sample.",
            "This leaves over 95% of the DSP56001's 16.5 MIPS available for other audio tasks."
        ],
        "close": [
            "Source code in 56k assembly uploaded to ftp.ashford-poly.edu:/pub/telecom-archives/dsp56k/stardust_56k.asm.",
            "Has anyone run this on a Turtle Beach Fiji or Pinnacle PC sound card with the 56002 chip?",
            "Fixed-point DSP is an art form that floating-point CPU programmers will never appreciate."
        ],
        "replies": {
            "technical": [
                "Beautiful assembly code! The 24-bit word size of the 56001 is tailor-made for high-precision audio filtering.",
                "Ran your code on my NeXTstation Turbo. It locked onto the carrier within 1.2 seconds of vinyl lead-in."
            ],
            "noise": [
                "Real programmers write in C, not arcane DSP microcode. With Pentium chips hitting 100 MHz, dedicated DSPs are obsolete.",
                "Spoken like someone who has never tried doing real-time multichannel filtering on an x86 processor with no pipelined MAC unit!"
            ]
        }
    },
    {
        "sub": "DBPSK demodulation of the 0.71 baud Stardust telemetry stream",
        "intro": [
            "Mathematical proof of the modulation scheme used on the 14.2 Hz carrier across all regional pressings.",
            "Differential Binary Phase Shift Keying (DBPSK) parameter extraction results.",
            "How the 14 ASCII characters per node are encoded into the record groove."
        ],
        "detail": [
            "The symbol duration is exactly 1.408 seconds, corresponding to a symbol rate of 0.7107 baud (14.2 Hz / 20).",
            "Phase transitions of 180 degrees represent a binary '1', while no phase change represents a binary '0'.",
            "Each message frame begins with an 8-bit Barker sequence [11100010] for frame synchronization.",
            "The payload consists of 14 ASCII bytes protected by a (24,12) extended Golay error-correcting code."
        ],
        "close": [
            "The use of Golay codes in 1984 indicates professional telecommunications or military aerospace design.",
            "Has anyone encountered bit errors in their decoded text? The Golay decoder corrects up to 3 bit errors per 24-bit codeword.",
            "When all 14 rows are assembled, the matrix forms an 80-column ASCII status report."
        ],
        "replies": {
            "technical": [
                "The Golay code confirms Marcus Hale's military background. The Voyager spacecraft and NATO satcom systems use the exact same code.",
                "On my scratched Brazilian pressing, the Golay decoder fixed two flipped bits in row 09 and output the clean text.",
                "A symbol rate of 0.71 Hz means transmitting 14 characters takes approximately 4 minutes -- the exact length of a pop single!"
            ],
            "lore": [
                "Every song on SYNTHESIS was engineered to be exactly long enough to transmit one complete telemetry frame.",
                "The song wasn't written around the lyrics. The lyrics were timed to match the telemetry packet duration!"
            ]
        }
    }
]

# ---------------------------------------------------------------------------
# Group 5: comp.sys.m68k
# ---------------------------------------------------------------------------
M68K_TOPICS = [
    {
        "sub": "TWIN-68 Rev C coprocessor board - schematic analysis & EPROM dump",
        "intro": [
            "Managed to dump the 27256 EPROMs from the TWIN-68 Rev C board recovered from Ashford Poly.",
            "Hardware teardown of the dual-68000 DSP accelerator board used in the Stardust project.",
            "Looking at the bus architecture of the TWIN-68 board. Motorola engineers, please take a look."
        ],
        "detail": [
            "The board features two 68000 CPUs clocked at 12 MHz sharing a dual-ported 128KB static RAM bank.",
            "CPU #0 handles host bus interfacing and DMA, while CPU #1 is dedicated entirely to a 16-bit MAC (multiply-accumulate) unit.",
            "Disassembling ROM #0 reveals an initialization routine that checks for a hardware dongle marked 'ORION-ENC-84'.",
            "At ROM offset 0x0909, the string 'M.H. // THE HATCH IS OPEN // ADVANCED ACOUSTICS LAB' is stored in ASCII."
        ],
        "close": [
            "Has anyone seen this board plugged into an Apple Mac Plus or an Amiga 2000 processor slot?",
            "Schematic diagram in ASCII uploaded to ftp.ashford-poly.edu:/pub/telecom-archives/twin68_array.asc.",
            "One 28-pin EPROM socket (labeled U14) is completely empty. What firmware was supposed to be in that socket?"
        ],
        "replies": {
            "technical": [
                "That dual-ported SRAM design is ingenious. It avoids bus arbitration contention between the two 68k processors entirely.",
                "The MAC unit looks like a precursor to the DSP56001 that Motorola put in the NeXT and Atari Falcon.",
                "Socket U14 was probably for the decryption key lookup table. Without that EPROM, CPU #1 is running in an idle loop."
            ],
            "skeptic": [
                "Why would anyone build a custom dual-68000 board in 1984 when you could just buy a Texas Instruments TMS32010 DSP?",
                "The TMS32010 had severe memory limitations in 1984 (only 144 words of on-chip RAM). Dual 68000s gave them full 16MB address space.",
                "Looks like a prototype telecommunications board for military secure voice, not an audio music product."
            ],
            "lore": [
                "Tom from Ashford Poly owns the physical board! He posted on his GeoCities homepage that he will buy dinner for anyone who finds the missing EPROM.",
                "Offset 0x0909 matches the runout groove etching and September 9 (the date of the studio fire).",
                "Marcus Hale designed the TWIN-68 board before he disappeared. That's why his initials are on the PCB silkscreen."
            ]
        }
    },
    {
        "sub": "Real-time 14.2 Hz demodulation on Amiga Paula audio DMA",
        "intro": [
            "Wrote an Amiga assembly program that uses Paula's DMA audio channels to sample and track the Stardust subcarrier.",
            "Amiga audio hackers: you can demodulate the 14.2 Hz carrier in real time without bogging down the OS.",
            "Testing custom audio input routines on an Amiga 1200 with a standard parallel-port sampler."
        ],
        "detail": [
            "By setting up Paula's audio DMA to double-buffer incoming 8-bit samples, the 68020 has plenty of cycles left for the Costas loop.",
            "I wrote a 64-tap FIR filter in pure 68k assembly using movem.l and dbra loop unrolling to downsample to 64 Hz.",
            "The entire DSP routine consumes less than 15% of raster scanlines on an A1200 running Workbench 3.1.",
            "When the carrier locks, the program flashes the Amiga power LED to indicate binary frame synchronization!"
        ],
        "close": [
            "Source code and executable will be released on Aminet under mus/misc/stardust_amiga.lha next week.",
            "Does anyone want to test on an unaccelerated Amiga 500 with 512K chip RAM?",
            "Long live the Amiga. Try doing real-time subcarrier demodulation on a 386 running Windows 3.1 without dropping frames!"
        ],
        "replies": {
            "technical": [
                "Brilliant use of Paula DMA! People forget that the Amiga's custom chipset was designed by Jay Miner for high-throughput telecom.",
                "Tested on my A3000 / 25 MHz. Ran smoothly in the background while I was compiling a C program in another window.",
                "Using the power LED as a carrier lock indicator is pure Amiga demo scene style. Kudos!"
            ],
            "noise": [
                "PC users spend $3,000 on Sound Blasters and Pentium chips and still can't do what a $500 Amiga was doing in 1985.",
                "Please make sure it's compatible with Kickstart 1.3 for those of us who haven't upgraded our A500s to 3.1 yet.",
                "Download failed on Aminet mirror. Can someone mail me an ADF floppy disk image?"
            ]
        }
    },
    {
        "sub": "Atari Falcon 030 Motorola DSP56001 code for Stardust carrier extraction",
        "intro": [
            "The Atari Falcon is the ultimate machine for decoding Project Stardust audio.",
            "Taking advantage of the Falcon's built-in 32 MHz DSP56001 and 16-bit audio codec.",
            "Real-time spectral waterfall and DBPSK demodulator for TOS 4.04."
        ],
        "detail": [
            "Unlike the Amiga which requires an external 8-bit sampler, the Falcon has true 16-bit stereo ADC inputs on the motherboard.",
            "The DSP56001 processes the 44.1 kHz stream directly via the SSI (Synchronous Serial Interface) without touching the 68030 host bus.",
            "A 256-point complex FFT is computed every 10 milliseconds, displaying a live spectrogram on a standard VGA monitor.",
            "The 14.2 Hz peak shows up as a bright white vertical line against the blue background noise."
        ],
        "close": [
            "Archive uploaded to ftp.lip6.fr:/pub/atari/Falcon/Music/stardust_falcon.zip.",
            "Requires 4MB ST-RAM and an RGB or VGA monitor.",
            "Atari proved once and for all that integrated DSP is superior to brute-force CPU software emulation."
        ],
        "replies": {
            "technical": [
                "The SSI to DSP56001 architecture on the Falcon is magnificent. Zero CPU overhead during 50 kHz audio acquisition.",
                "I tested this with a vinyl rip fed into the Falcon mic input. Carrier lock occurred at second 14 of 'Synthetic Dawn'."
            ],
            "noise": [
                "Too bad Atari marketing was so incompetent that nobody bought the Falcon before they pulled out of the computer market.",
                "Atari Falcon vs Amiga 1200 flamewar in 3... 2... 1..."
            ]
        }
    },
    {
        "sub": "Benchmarking FFT routines on Mac IIci with MC68882 FPU under System 7.5",
        "intro": [
            "Benchmarking various C compilers and FPU math libraries on a Macintosh IIci (25 MHz 68030 + 68882).",
            "Compiling stardust.c with Think C 6.0 vs MPW C with direct 68882 inlining.",
            "Can a 1989 Mac IIci decode a 40-minute LP in reasonable time?"
        ],
        "detail": [
            "Apple's standard SANE (Standard Apple Numerics Environment) library uses IEEE 80-bit extended precision, but is notoriously slow.",
            "By passing the -mc68882 compiler flag in Think C, all sin/cos and sqrt operations compile directly to FPU opcodes.",
            "A 1024-point radix-2 FFT drops from 142 milliseconds under SANE to just 18 milliseconds using direct FPU instructions.",
            "Total execution time for a 20-minute audio track dropped from 48 minutes to 6.2 minutes."
        ],
        "close": [
            "Make sure you install the 32-bit Enabler on older IIci machines running System 7.1!",
            "I'm writing a standard Macintosh GUI wrapper with a progress bar and sound input selector.",
            "Anyone running this on a Quadra 840AV with the 68040?"
        ],
        "replies": {
            "technical": [
                "The 68040 on the Quadra is a monster -- the on-chip FPU executes FFT butterflies in less than 4 milliseconds.",
                "Beware of System 7.5.1 memory leaks if you allocate large sample buffers in the application heap. Use NewPtrSys instead."
            ],
            "noise": [
                "Mac users bragging about 6-minute render times while Unix workstations do it in 20 seconds. Classic Apple distortion field."
            ]
        }
    },
    {
        "sub": "Disassembling socket U14 firmware on the TWIN-68 board",
        "intro": [
            "Further progress on reverse-engineering the empty socket U14 on the TWIN-68 Rev C coprocessor board.",
            "Tracing the address decoder lines on the motherboard reveals what was supposed to be in socket U14.",
            "Hardware disassembly report for Motorola hardware hackers."
        ],
        "detail": [
            "Socket U14 is wired to the upper 8 data lines (D8-D15) mapped to memory region 0x00E00000 - 0x00E7FFFF.",
            "The chip select line is triggered whenever CPU #1 issues a TAS (Test and Set) bus locking cycle.",
            "This indicates socket U14 held a cryptographic S-box lookup table for decrypting the Stardust keystream.",
            "Without U14, the board can track the 14.2 Hz carrier, but cannot descramble the binary payload of Nodes 11 through 14."
        ],
        "close": [
            "Does anyone have a 27C256 EPROM marked 'MH-U14' or 'ORION-CRYPTO'?",
            "Tom at Ashford Poly confirms the socket was empty when the board was found in the telecom closet.",
            "Did Marcus take the decryption EPROM with him when he left the lab?"
        ],
        "replies": {
            "technical": [
                "Using an S-box in a 27256 EPROM for single-cycle hardware substitution was standard military cipher practice in 1984.",
                "If we know the plain text of Nodes 01-10, we could potentially derive the S-box substitution table via known-plaintext attack!"
            ],
            "lore": [
                "Marcus took that EPROM with him. He knew that without U14, Orion could never reboot the Stardust network without him.",
                "That's why Line 08 says: 'WHEN EVERY NODE IS WHOLE, THE CHANNEL OPENS.' It requires all physical keys."
            ]
        }
    }
]

GROUP_TOPIC_MAP = {
    "alt.fan.nova-hart": FAN_TOPICS,
    "alt.music.synth-pop": SYNTH_TOPICS,
    "alt.conspiracy": CONSPIRACY_TOPICS,
    "comp.dsp": DSP_TOPICS,
    "comp.sys.m68k": M68K_TOPICS,
}

SWARM_GROUPS_ALL = [
    "alt.fan.nova-hart",
    "alt.music.synth-pop",
    "alt.conspiracy",
    "comp.dsp",
    "comp.sys.m68k",
]

SUB_PREFIXES = [
    "", "", "", "[INFO] ", "Question: ", "Observation: ", "Discussion: ", "[SPECULATION] ", "Data: ", "[FLAME] ", "WTB/WTT: "
]

import unicodedata

def clean_ascii(s):
    norm = unicodedata.normalize('NFKD', s)
    return "".join(c for c in norm if not unicodedata.combining(c) and c.isalnum()).lower()

def generate_persona(ctx, pid, r):
    first = r.choice(FIRST_NAMES)
    last = r.choice(LAST_NAMES)
    domain, org = r.choice(DOMAINS)
    login = f"{clean_ascii(first[0])}{clean_ascii(last)}"
    email = f"{login}@{domain}"
    machine = r.choice(MACHINES)
    os_name = r.choice(OS_LIST)
    baud = r.choice(BAUD_RATES)
    hardware = r.choice(HARDWARE_DEVICES)
    quote = r.choice(QUOTES)
    pgp = "%04X %04X %04X %04X" % (r.randint(0, 0xFFFF), r.randint(0, 0xFFFF), r.randint(0, 0xFFFF), r.randint(0, 0xFFFF))
    
    sig_tpl = r.choice(SIG_TEMPLATES)
    sig_lines = [line.format(
        name=f"{first} {last}",
        email=email,
        org=org,
        quote=quote,
        machine=machine,
        os=os_name,
        baud=baud,
        hardware=hardware,
        pgp=pgp
    ) for line in sig_tpl]
    
    persona = {
        "id": pid,
        "name": f"{first} {last}",
        "email": email,
        "org": org,
        "node": "%02d" % r.randint(1, 10),
        "sig": sig_lines
    }
    ctx.personas[pid] = persona
    return persona

def build_swarm_threads(ctx, count):
    threads = []
    for i in range(count):
        r = rng_for(ctx.seed, "swarm-thread-v3", i)
        group = r.choice(SWARM_GROUPS_ALL)
        topics = GROUP_TOPIC_MAP[group]
        topic = r.choice(topics)
        
        # Subject line
        prefix = r.choice(SUB_PREFIXES)
        subject = f"{prefix}{topic['sub']}"
        
        # Opening post composition
        intro = r.choice(topic["intro"])
        detail1 = r.choice(topic["detail"])
        detail2 = r.choice([d for d in topic["detail"] if d != detail1])
        close = r.choice(topic["close"])
        
        op_body = [intro, "", detail1, detail2, "", close]
        
        # Generate messages
        n_msgs = r.randint(2, 5)
        msgs = []
        
        # OP author
        p0_id = f"s{i:05d}-0"
        p0 = generate_persona(ctx, p0_id, r)
        msgs.append({"from": p0_id, "body": op_body})
        
        # Dynamic weights for reply attitudes per group
        if group == "comp.dsp":
            weights = {"technical": 0.40, "skeptic": 0.30, "lore": 0.15, "noise": 0.15}
        elif group == "comp.sys.m68k":
            weights = {"technical": 0.40, "noise": 0.30, "skeptic": 0.15, "lore": 0.15}
        elif group == "alt.conspiracy":
            weights = {"lore": 0.40, "agree": 0.30, "skeptic": 0.20, "noise": 0.10}
        elif group == "alt.music.synth-pop":
            weights = {"agree": 0.35, "technical": 0.25, "lore": 0.20, "noise": 0.20}
        else: # alt.fan.nova-hart
            weights = {"agree": 0.35, "lore": 0.30, "skeptic": 0.15, "noise": 0.20}
        
        avail_types = list(topic["replies"].keys())
        type_weights = [weights.get(t, 0.2) for t in avail_types]
        total_w = sum(type_weights)
        type_weights = [w / total_w for w in type_weights]
        
        for j in range(1, n_msgs):
            pj_id = f"s{i:05d}-{j}"
            generate_persona(ctx, pj_id, r)
            
            # Select reply type and text
            chosen_type = r.choices(avail_types, weights=type_weights, k=1)[0]
            rep_options = topic["replies"][chosen_type]
            rep_text = r.choice(rep_options)
            
            rep_lines = [rep_text]
            if r.random() < 0.25:
                noise_tag = r.choice(USENET_NOISE_TAGS)
                rep_lines.extend(["", noise_tag])
            
            parent_idx = r.randint(0, j - 1)
            quote_count = r.randint(1, 2)
            
            msgs.append({
                "from": pj_id,
                "body": rep_lines,
                "reply_to": parent_idx,
                "quote": quote_count
            })
            
        year = r.choice([1994, 1995, 1995, 1996])
        month = r.randint(1, 12)
        day = r.randint(1, 28)
        hour = r.randint(0, 23)
        minute = r.randint(0, 59)
        second = r.randint(0, 59)
        start_dt = datetime.datetime(year, month, day, hour, minute, second)
        
        tid = f"s{i:05d}"
        threads.append({
            "id": tid,
            "group": group,
            "subject": subject,
            "start": start_dt.strftime("%Y-%m-%dT%H:%M:%S"),
            "messages": msgs,
            "swarm": True
        })
        ctx.thread_group[tid] = group
        
    return threads
