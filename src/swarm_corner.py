"""Procedural generator for authentic 1995-1996 GeoCities 'Nova Hart Corner' fan pages.

Implements the Nova Hart Corner Expansion Plan:
- 10 distinct regional fan archetypes (Otaku, Rockero, Magnitizdat Taper, DSP Nerd, Collector, Conspiracist, Grieving Fan, Skeptic, Kid, Pen-pal Seeker)
- Canon-aware temporal consistency (every fragment has 'not_before' checked against the page date)
- 4 distinct retro layout designs (Classic Shrine, 2-Column Sidebar, Monospace Zine/Terminal, Webring Station Hub)
- Diverse, richly styled sections with slot-filling
- 16 custom authentic retro 90s badges and icons
- 4-tier clue distribution (Common, Uncommon, Rare BIO-ID, Legendary)
- Output manifest generation for private site_clues.json
"""
import os
import random
import re
from common import esc, rng_for
import swarm_bank as sb

HOODS = [
    "SiliconValley/Lab", "Hollywood/Hills", "SunsetStrip/Club", "Area51/Vault", "Tokyo/Garden", "Athens/Forum",
    "Paris/LeftBank", "CapeCanaveral/Lab", "Heartland/Plains", "SoHo/Studio", "Vienna/Strasse", "Colosseum/Field",
    "TimesSquare/Arcade", "Nashville/Opry", "RainForest/Canopy", "Pentagon/Quarters", "BourbonStreet/Delta", "EnchantedForest/Glade"
]

LAYOUTS = ["shrine", "two_column", "terminal", "hub"]

BADGE_LIST = [
    "netscape_now", "hfn_badge", "listening_night", "node_hunter", "tape_trader",
    "stardust_webring", "orion_records_badge", "warning_glitch", "geocities_badge", "view_640"
]

def parse_date(date_str):
    parts = [int(p) for p in date_str.split("-")]
    return parts[0], parts[1], parts[2]

def is_available(fragment, page_date):
    if isinstance(fragment, dict):
        nb = fragment.get("nb")
        if nb and nb > page_date:
            return False
    return True

def get_text(fragment):
    if isinstance(fragment, dict):
        return fragment.get("t", "")
    return str(fragment)

def apply_voice(text, voice_type, r):
    cfg = sb.VOICE.get(voice_type, {})
    caps_prob = cfg.get("caps", 0.0)
    bang_prob = cfg.get("bang", 0.0)
    typo_prob = cfg.get("typo", 0.0)
    
    words = text.split(" ")
    out_words = []
    for w in words:
        if r.random() < caps_prob and len(w) > 3:
            w = w.upper()
        if r.random() < typo_prob and len(w) > 4:
            # swap two adjacent letters
            idx = r.randint(1, len(w) - 2)
            w = w[:idx] + w[idx+1] + w[idx] + w[idx+2:]
        out_words.append(w)
    res = " ".join(out_words)
    if r.random() < bang_prob and not res.endswith("!"):
        res += "!" * r.randint(1, 3)
    tails = cfg.get("tail")
    if tails and r.random() < 0.35:
        res += " " + r.choice(tails)
    return res

def make_title(archetype, reg_key, name, city, r):
    titles_en = [
        f"{name}'s Nova Hart Corner",
        f"★ {name}'s Stardust Shrine ★",
        f"The 14.2 Hz Station - {name} ({city})",
        f"{name}'s Tape Exchange // NOVA HART",
        f"Where Is Nova? - {name}'s GeoCities Page",
        f"{name}'s SYNTHESIS Archive",
        f"Project Stardust Fan Hub - Station {r.randint(100, 999)}",
        f"{name}'s Retro Wave & Nova Hart Sanctuary",
    ]
    if reg_key == "jp":
        titles_jp = [
            f"★ {name}のノバ・ハート部屋 ★",
            f"{name}のアイドル・プロトコル研究所",
            f"赤坂リール研究室 ({name}'s Page)",
            f"{name}のノバちゃん応援ステーション！",
            f"Stardust 14.2Hz - {name} ({city})",
            f"{name}'s Nova-chan Fan Sanctuary ^_^",
        ]
        return r.choice(titles_jp)
    elif reg_key == "kr":
        titles_kr = [
            f"{name}의 노바 하트 팬페이지 ^^",
            f"은하넷 {name}의 음악 보관소",
            f"{name}의 14.2 Hz 스타더스트 룸",
            f"노바 하트 & 신스팝 연구 ({name})",
        ]
        return r.choice(titles_kr)
    elif reg_key in ("mx", "es"):
        titles_es = [
            f"La Bóveda de {name} - ROCK EN ESPAÑOL & NOVA HART",
            f"El Rincón de {name} // 14.2 Hz",
            f"Página de {name}: Solos de Orion México !!!",
            f"Santuario de Nova Hart - {name} ({city})",
            f"ORION MÉXICO // {name}'s Home",
        ]
        return r.choice(titles_es)
    elif reg_key == "pt":
        titles_pt = [
            f"Espaço de {name}: O Sinal de Nova Hart",
            f"Página de {name} - Fã de 1985 !!!",
            f"Rede Saturno: O Rincón de {name}",
            f"{name}'s Nova Hart Sanctuary (Porto Alegre)",
        ]
        return r.choice(titles_pt)
    elif reg_key == "de":
        titles_de = [
            f"{name}'s Nova Hart Archiv ({city})",
            f"SYNTH.GER - {name}'s Fanseite",
            f"Knoten 05 // {name}'s Stardust Page",
            f"{name}'s Speicher - 14.2 Hz",
        ]
        return r.choice(titles_de)
    elif reg_key == "ru":
        titles_ru = [
            f"Страница {name}: Магнитиздат и Нова Харт",
            f"Узел 08 - Архив {name}",
            f"{name} / Сигнал 14.2 Гц ({city})",
            f"Коллекция {name}: Катушки и Кассеты",
        ]
        return r.choice(titles_ru)
    elif reg_key == "fr":
        titles_fr = [
            f"Le Temple de Nova - Page de {name}",
            f"Station 3615 de {name} ({city})",
            f"{name}'s Synth-Wave & Nova Hart",
        ]
        return r.choice(titles_fr)
    elif reg_key == "sv":
        titles_sv = [
            f"{name}'s Nova Hart-sida ({city})",
            f"{name}'s Stardust Arkiv (Uppsala/Sweden)",
            f"Nod 10 // {name}'s Webbsida",
        ]
        return r.choice(titles_sv)
    return r.choice(titles_en)

def generate_swarm_homepage(ctx, i, total_swarm=5000):
    r = rng_for(ctx.seed, "swarm-geo-v2", i)
    hood = r.choice(HOODS)
    num = r.randint(1000, 9999)
    slug = f"{hood.replace('/', '-').lower()}-{num}"
    path_display = f"{hood}/{num}"
    
    # Pick Region
    reg_keys = list(sb.REGIONS.keys())
    reg_weights = [sb.REGIONS[k]["weight"] for k in reg_keys]
    reg_key = r.choices(reg_keys, weights=reg_weights, k=1)[0]
    reg = sb.REGIONS[reg_key]
    
    # Pick Archetype fitting region
    arch_keys = list(sb.ARCHETYPES.keys())
    arch_weights = []
    for ak in arch_keys:
        w = sb.ARCHETYPES[ak]["regions"].get(reg_key, sb.ARCHETYPES[ak]["regions"].get("other", 1))
        arch_weights.append(w)
    arch_key = r.choices(arch_keys, weights=arch_weights, k=1)[0]
    arch = sb.ARCHETYPES[arch_key]
    
    name = r.choice(reg["names"])
    city = r.choice(reg["cities"])
    domain = r.choice(reg["domains"])
    email_clean = re.sub(r'[^a-z0-9]', '', name.lower())
    email = f"{email_clean}{num}@{domain}"
    
    # Palette & Layout
    palette_list = sb.REGION_PALETTES.get(reg_key, sb.REGION_PALETTES["us"])
    bg, text, link, vlink = r.choice(palette_list)
    layout = r.choice(LAYOUTS)
    
    # Date in 1995-1996
    year = r.choice([1995, 1996])
    month = r.randint(1, 12)
    # If 1995, ensure realistic spread
    day = r.randint(1, 28)
    page_date = f"{year}-{month:02d}-{day:02d}"
    
    # Slot values for formatting
    age = r.randint(15, 34)
    age_then = max(7, age - (year - 1985))
    fan_since = r.choice([1984, 1985, 1985, 1985, 1986, 1987, 1988, 1989, 1990])
    song_tuple = r.choice(sb.SONGS)
    song_name, song_year = song_tuple[0], song_tuple[1]
    jp_sing = r.choice(sb.JP_SINGLES)
    jp_file, jp_title, jp_en, jp_year = jp_sing[0], jp_sing[1], jp_sing[2], jp_sing[3]
    emo = r.choice(sb.EMO.get(reg.get("emo", "default"), sb.EMO["default"]))
    how_choice = r.choice(sb.HOW)
    
    slot_vars = {
        "name": name, "city": city, "age": age, "age_then": age_then,
        "fan_since": fan_since, "how": how_choice, "how_cap": how_choice.capitalize(),
        "song": song_name, "year": song_year, "format": r.choice(sb.FORMATS),
        "n": r.randint(2, 45), "mmss": f"{r.randint(1, 4)}:{r.randint(10, 59):02d}",
        "secs": r.randint(4, 52), "cents": r.randint(12, 48), "db": r.randint(35, 68),
        "emo": emo, "receiver": r.choice(sb.RECEIVERS), "deck": r.choice(sb.DECKS),
        "computer": r.choice(sb.COMPUTERS), "modem": r.choice(sb.MODEMS),
        "phones": r.choice(sb.PHONES), "price": r.choice(sb.PRICES),
        "grade": r.choice(sb.GRADES), "nick": f"{name.lower()}{r.randint(10, 99)}",
        "date": page_date, "year_hard": r.choice([1989, 1990, 1991, 1992, 1993]),
        "jp_file": jp_file, "jp_title": jp_title, "jp_en": jp_en,
        "pressing": sb.PRESSINGS.get(reg_key, sb.PRESSINGS["us"]),
        "pressing_short": reg_key.upper(),
        "node": sb.REGION_NODE.get(reg_key, 1),
        "region_name": reg_key.upper(),
        "line": sb.NODE_LINES.get(sb.REGION_NODE.get(reg_key, 1), "HOLD FOR RELAY"),
        "fake": r.choice(sb.FAKE_LINES),
        "pp_regions": r.choice(["Japan & Mexico", "Europe & USA", "Brazil & Russia", "Scandinavia & Asia", "everywhere"]),
        "langs": r.choice(["English & Spanish", "English & German", "English & French", "English & Japanese (learning!)", "English & Russian"]),
        "friends": f"{r.choice(['Sven', 'Lucia', 'Kenji', 'Dmitri', 'Ines'])} and {r.choice(['Aiko', 'Mateo', 'Nadia', 'Tobias', 'Camila'])}",
        "who": r.choice(sb.WHO),
        "gen": r.randint(3, 7),
        "copy_no": r.randint(100, 999),
        "chain": r.choice(["Riga -> Moscow -> St. Petersburg", "Berlin -> Warsaw -> Kyiv", "Vladivostok -> Khabarovsk", "Tallinn -> Leningrad"]),
        "date_jp": f"199{r.randint(4, 6)}年{r.randint(1, 12)}月",
    }
    
    # Title & Marquee
    title = make_title(arch_key, reg_key, name, city, r)
    marquees = [
        "~ hold for relay ~", "welcome to station #%d !!" % i, "★ NOVA HART 4EVER ★",
        "the hatch is open", "14.2 Hz -- THE CARRIER SURVIVES", "Akasaka Branch Archive // Online",
        "Where is Nova? Postcards to LA!", "02:14 UTC -- KEEP THE CHANNELS OPEN",
        "Orion Records Advanced Acoustics Lab -- declassified?", "Seiko Cut / 80s Idol Pop Forever",
        "El rock no ha muerto // Bóveda CDMX", "Магнитиздат копия №%d" % r.randint(100, 999)
    ]
    marquee = r.choice(marquees)
    
    # Clue Assignment
    # Common (85%), Uncommon (12%), Rare BIO-ID (~2.5%), Legendary (~0.5%)
    clue_roll = r.random()
    clue_record = None
    assigned_clue_text = None
    assigned_clue_type = None
    
    if clue_roll < 0.005: # Legendary (~25 pages)
        assigned_clue_type = "legendary"
        assigned_clue_text = r.choice(sb.LEGENDARY)
        clue_record = {"slug": slug, "tier": "legendary", "text": assigned_clue_text, "region": reg_key}
    elif clue_roll < 0.030: # Rare BIO-ID (~125 pages)
        assigned_clue_type = "rare_bio_id"
        matching_bio = [b[1] for b in sb.BIO_ID_FRAGMENTS if b[0] == reg_key]
        if not matching_bio:
            matching_bio = [b[1] for b in sb.BIO_ID_FRAGMENTS]
        assigned_clue_text = r.choice(matching_bio)
        clue_record = {"slug": slug, "tier": "rare_bio_id", "text": assigned_clue_text, "region": reg_key}
    elif clue_roll < 0.150: # Uncommon (~600 pages)
        assigned_clue_type = "uncommon_node"
        node_num = sb.REGION_NODE.get(reg_key, 1)
        node_line = sb.NODE_LINES.get(node_num, "HOLD FOR RELAY")
        assigned_clue_text = f"Decoded relay matrix (Node {node_num:02d} / {reg_key.upper()}): '{node_line}'."
        clue_record = {"slug": slug, "tier": "uncommon_node", "text": assigned_clue_text, "region": reg_key}
    
    # Build Sections
    # Determine which sections this archetype desires
    desired_secs = arch.get("sections", {})
    available_sec_types = list(desired_secs.keys())
    # Pick 4 to 7 sections
    sec_count = r.randint(4, min(7, len(available_sec_types)))
    weights = [desired_secs[k] for k in available_sec_types]
    chosen_sec_types = ["hi"] # Always start with Hi/Intro
    
    # Sample without replacement
    remaining_types = list(available_sec_types)
    remaining_weights = list(weights)
    for _ in range(sec_count):
        if not remaining_types:
            break
        picked = r.choices(remaining_types, weights=remaining_weights, k=1)[0]
        chosen_sec_types.append(picked)
        idx = remaining_types.index(picked)
        remaining_types.pop(idx)
        remaining_weights.pop(idx)
        
    native_data = sb.NATIVE.get(reg_key) if reg_key in sb.NATIVE else None
    
    sections = []
    
    for stype in chosen_sec_types:
        heading = stype.replace("_", " ").title()
        p_list = []
        list_items = None
        pre_lines = None
        badge_row = None
        
        if stype == "hi":
            if native_data and "hi" in native_data and r.random() < 0.85:
                heading = native_data.get("headings", {}).get("hi", "Hi!")
                raw_hi = r.choice(native_data["hi"])
                if "how_" + reg_key in native_data:
                    slot_vars["how_" + reg_key] = r.choice(native_data["how_" + reg_key])
                p_list.append(raw_hi.format(**slot_vars))
                if r.random() < 0.5:
                    p_list.append(native_data.get("sorry", "(Sorry for my English)"))
            else:
                raw_hi = r.choice(sb.HI)
                hi_text = raw_hi.format(**slot_vars)
                p_list.append(apply_voice(hi_text, arch.get("voice", "polite"), r))
                
        elif stype == "favorite":
            if native_data and "favorite" in native_data and r.random() < 0.80:
                heading = native_data.get("headings", {}).get("favorite", "Favorite Song")
                raw_fav = r.choice(native_data["favorite"])
                p_list.append(raw_fav.format(**slot_vars))
            else:
                raw_fav = r.choice(sb.FAVORITE)
                fav_text = raw_fav.format(**slot_vars)
                p_list.append(apply_voice(fav_text, arch.get("voice", "polite"), r))
                
        elif stype == "theory":
            heading = "My Theory"
            if native_data and "theory" in native_data and r.random() < 0.70:
                heading = native_data.get("headings", {}).get("theory", "My Theory")
                cand = [c for c in native_data["theory"] if is_available(c, page_date)]
                if cand:
                    p_list.append(get_text(r.choice(cand)).format(**slot_vars))
            if not p_list:
                cand = [c for c in sb.THEORY_A if is_available(c, page_date)]
                t_a = get_text(r.choice(cand)).format(**slot_vars)
                t_b = r.choice(sb.THEORY_B).format(**slot_vars)
                comb = f"{t_a} {t_b}".strip()
                p_list.append(apply_voice(comb, arch.get("voice", "conspiracist"), r))
                
        elif stype == "where_i_was":
            heading = "Where I Was"
            if native_data and "where_i_was" in native_data and r.random() < 0.75:
                cand = [c for c in native_data["where_i_was"] if is_available(c, page_date)]
                if cand:
                    heading = native_data.get("headings", {}).get("where_i_was", "Where I Was")
                    p_list.append(get_text(r.choice(cand)).format(**slot_vars))
            if not p_list:
                cand = [c for c in sb.WHERE_I_WAS if is_available(c, page_date)]
                p_list.append(get_text(r.choice(cand)).format(**slot_vars))
                
        elif stype == "collection":
            heading = "My Collection & Pressing Log"
            p_list.append(f"My physical collection of Nova Hart records and tapes as of {page_date}:")
            pre_lines = [
                "PRESSING / EDITION                         GRADE  NOTES",
                "------------------------------------------ ------ --------------------------"
            ]
            rows_num = r.randint(2, 5)
            for _ in range(rows_num):
                press_key = r.choice(list(sb.PRESSINGS.keys()))
                press_name = sb.PRESSINGS[press_key].replace("the ", "")[:42]
                gr = r.choice(sb.GRADES)
                note_templ = r.choice(sb.COLLECTION_NOTES)
                note_str = note_templ.format(**slot_vars)
                pre_lines.append(f"{press_name:<42} {gr:<6} {note_str}")
                
        elif stype == "trading":
            heading = "Tape Trading & Mail Order"
            p_list.append("Looking for audio and video trades! SASE or IRC required for international tape mail.")
            p_list.append("<b>WANTS:</b>")
            list_items = [r.choice(sb.TRADING_WANTS) for _ in range(r.randint(2, 4))]
            # We can put HAVES in a paragraph
            haves = ", ".join(r.sample(sb.TRADING_HAVES, k=min(3, len(sb.TRADING_HAVES))))
            p_list.append(f"<b>HAVES TO TRADE:</b> {haves}.")
            
        elif stype == "jp_singles":
            heading = "Orion Records Japan: Idol Protocol Singles"
            if native_data and "jp_singles" in native_data:
                heading = native_data["headings"].get("jp_singles", heading)
            p_list.append("Chronological 7-inch & Cassette Single Releases (Akasaka Branch, 1985-1989):")
            pre_lines = [
                "CATALOGUE   YEAR  JAPANESE TITLE                ENGLISH TITLE",
                "----------- ----  ----------------------------  ------------------------"
            ]
            for s in sb.JP_SINGLES:
                pre_lines.append(f"{s[0]:<11} {s[3]}  {s[1]:<28}  {s[2]}")
                
        elif stype == "solos":
            heading = "The Mexican Pressing Guitar Solos"
            if native_data and "solos" in native_data:
                heading = native_data["headings"].get("solos", heading)
                p_list.append(r.choice(native_data["solos"]).format(**slot_vars))
            else:
                p_list.append(f"The Mexican pressing (Orion México) contains uncredited guitar solos on '{song_name}' that are completely muted on the US release. At {slot_vars['mmss']}, Marcus or the studio band lets loose!")
                
        elif stype == "tape_genealogy":
            heading = "Magnitizdat Tape Genealogy"
            if native_data and "tape_genealogy" in native_data:
                heading = native_data["headings"].get("tape_genealogy", heading)
                p_list.append(r.choice(native_data["tape_genealogy"]).format(**slot_vars))
            else:
                p_list.append(f"My cassette copy is generation #{slot_vars['gen']} dubbed from {slot_vars['chain']}. Even through tape hiss and wow/flutter, the 14.2 Hz pulse registers on the VU meter.")
                
        elif stype == "spectrum":
            heading = "14.2 Hz Signal Analysis & DSP"
            p_list.append(r.choice(sb.SPECTRUM).format(**slot_vars))
            pre_lines = [
                " Frequency (Hz) | Level (dB) | Spectral Density [FFT 4096]",
                "----------------+------------+--------------------------------",
                "  10.0 Hz       |  -64 dB    | *",
                "  14.2 Hz [PEAK]|  -42 dB    | ************************** [CARRIER]",
                "  18.5 Hz       |  -68 dB    | *",
                "  50/60 Hz      |  -52 dB    | ******* [MAINS HUM]",
            ]
            
        elif stype == "node_hunt":
            heading = f"Relay Matrix // Node {slot_vars['node']:02d}"
            if native_data and "node_hunt" in native_data:
                cand = [c for c in native_data["node_hunt"] if is_available(c, page_date)]
                if cand:
                    heading = native_data["headings"].get("node_hunt", heading)
                    p_list.append(get_text(r.choice(cand)).format(**slot_vars))
            if not p_list:
                p_list.append(r.choice(sb.NODE_HUNT).format(**slot_vars))
                
        elif stype == "marcus":
            heading = "Who Was Marcus Hale?"
            cand = [c for c in sb.MARCUS if is_available(c, page_date)]
            p_list.append(get_text(r.choice(cand)).format(**slot_vars))
            
        elif stype == "listening_night":
            heading = "Listening Night 02:14 UTC Log"
            cand = [c for c in sb.LISTENING if is_available(c, page_date)]
            p_list.append(get_text(r.choice(cand)).format(**slot_vars))
            
        elif stype == "gear":
            heading = "My Listening Post & Audio Gear"
            list_items = [g.format(**slot_vars) for g in r.sample(sb.GEAR, k=min(3, len(sb.GEAR)))]
            
        elif stype == "skeptic":
            heading = "A Sceptic's Counter-Argument"
            p_list.append(r.choice(sb.SKEPTIC).format(**slot_vars))
            
        elif stype == "letter":
            heading = "Letter to Nova"
            p_list.append(r.choice(sb.LETTER).format(**slot_vars))
            
        elif stype == "top5":
            heading = r.choice(sb.TOP5).format(**slot_vars)
            chosen_songs = r.sample(sb.SONGS, k=5)
            list_items = [f"{idx+1}. '{s[0]}' ({s[1]})" for idx, s in enumerate(chosen_songs)]
            
        elif stype == "vhs":
            heading = "VHS Off-Air Recording Log"
            if native_data and "vhs" in native_data:
                heading = native_data["headings"].get("vhs", heading)
                list_items = [v.format(**slot_vars) for v in r.sample(native_data["vhs"], k=min(3, len(native_data["vhs"])))]
            else:
                list_items = [
                    f"1985-06-08 Hamburg broadcast 'Memory Hatch' freeze (tape degradation: heavy)",
                    f"1986-10-12 Meridian Broadcast live satellite capture (clean audio, some dropout)",
                    f"1989-12-09 Final broadcast recording (Nova looks off camera at {slot_vars['mmss']})"
                ]
                
        elif stype == "lyric_log":
            heading = "Lyric Discrepancy & Translation Anomalies"
            if native_data and "lyric_log" in native_data:
                heading = native_data["headings"].get("lyric_log", heading)
                list_items = [ll.format(**slot_vars) for ll in r.sample(native_data["lyric_log"], k=min(2, len(native_data["lyric_log"])))]
            else:
                list_items = [
                    f"At {slot_vars['mmss']}: US lyric says 'dream', regional master vocal take clearly says 'machine'.",
                    f"The chorus double-track drifts away from the official lyric sheet by half a beat."
                ]
                
        elif stype == "akasaka":
            heading = "The Akasaka Master Tapes (Recovered May 1995)"
            cand = [c for c in (native_data.get("akasaka", []) if native_data else []) if is_available(c, page_date)]
            if cand:
                p_list.append(get_text(r.choice(cand)).format(**slot_vars))
            else:
                p_list.append("The unreleased Akasaka reel box contains 'Synthesized Smile' and 'Ghost in the Chorus'. Every box is stamped 'VOICE PRINT: GEN-3'.")
                
        elif stype == "fanart":
            heading = "Nova-chan Fan Art & ASCII"
            p_list.append(r.choice(sb.FANART).format(**slot_vars))
            pre_lines = r.choice(sb.ASCII_ART)
            
        elif stype == "concert_dream":
            heading = "Live Concert Dream"
            p_list.append(r.choice(sb.CONCERT).format(**slot_vars))
            
        elif stype == "pen_pals":
            heading = "International Pen-Pals Wanted"
            p_list.append(r.choice(sb.PEN_PALS).format(**slot_vars))
            
        sec_obj = {"h": heading}
        if p_list:
            sec_obj["p"] = p_list
        if list_items:
            sec_obj["list"] = list_items
        if pre_lines:
            sec_obj["pre"] = pre_lines
        sections.append(sec_obj)

    # Inject Assigned Clue (if any) into an appropriate section or a dedicated note
    if assigned_clue_text:
        sections.append({
            "h": "Secret Note // Decrypted Transmission",
            "p": [f"<b>[INTERCEPT / RECOVERED DATA]:</b> {assigned_clue_text}"]
        })
        
    # Badge Row (Pick 2-4 authentic 88x31 badges)
    badge_picks = r.sample(BADGE_LIST, k=r.randint(2, 4))
    
    # Links
    links = [
        {"t": "Rick's Nova Hart Shrine (ring home)", "u": "geo:hollywood-hills-4127"},
        {"t": "GeoCities Homestead Directory", "u": "geo:index"},
    ]
    # Add random thematic links
    thematic_pool = [
        {"t": "alt.fan.nova-hart archive", "u": "usenetgroup:alt.fan.nova-hart"},
        {"t": "alt.music.synth-pop", "u": "usenetgroup:alt.music.synth-pop"},
        {"t": "comp.dsp - 14.2 Hz spectral discussion", "u": "usenet:t01-spectral-line"},
        {"t": "alt.conspiracy - Kestrel's testimony", "u": "usenet:t03-kestrel"},
        {"t": "Akasaka Tapes Recovery (May 1995)", "u": "usenet:t14-akasaka"},
        {"t": "Anonymous FTP Archive: Ashford-Poly", "u": "ftp:ashford-poly/index.html"},
        {"t": "Anonymous FTP Archive: Kamome Net", "u": "ftp:kamome/index.html"},
        {"t": "Regional Node 01: Northvale Gopher (USA)", "u": "regional:01-usa"},
        {"t": "Regional Node 02: Kamome BBS (Japan)", "u": "regional:02-japan"},
        {"t": "Regional Node 04: Red Coyoacán (Mexico)", "u": "regional:04-mexico"},
        {"t": "Regional Node 08: Relcom Node 08 (USSR)", "u": "regional:08-ussr"},
        {"t": "Tokyo Garden #1420 - Akasaka Shrine", "u": "geo:tokyo-garden-1420"},
        {"t": "Silicon Valley Lab #1984 - DSP Lab", "u": "geo:siliconvalley-lab-1984"},
    ]
    chosen_thematics = r.sample(thematic_pool, k=r.randint(2, 4))
    links.extend(chosen_thematics)
    
    hp = {
        "slug": slug,
        "path_display": path_display,
        "title": title,
        "bg": bg,
        "text": text,
        "link": link,
        "vlink": vlink,
        "counter": r.randint(14, 18940),
        "updated": page_date,
        "lang": reg.get("lang", "en"),
        "layout": layout,
        "marquee": marquee,
        "badges": badge_picks,
        "sections": sections,
        "links": links,
    }
    owner = {"email": email}
    return hp, owner, clue_record
