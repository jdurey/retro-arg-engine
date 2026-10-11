"""One-time export of the frozen v2 phrase bank (src/swarm_bank.py + builder UI
strings) into data/bank_v3/*.json, the editable bank used by the JS edge
generator (deploy/swarm/).  src/swarm_bank.py stays untouched so the 5,039
legacy static pages remain byte-identical.

Usage: python3 scripts/export_bank_v3.py   (refuses to overwrite unless --force)
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import swarm_bank as sb  # noqa: E402
import swarm_corner as sc  # noqa: E402
import geocities_builder as gb  # noqa: E402

OUT = os.path.join(ROOT, "data", "bank_v3")

# make_title() keyed some regions by language code, so br/su/se silently fell
# back to English titles in v2.  v3 keys titles by region.
TITLES = {
    "jp": ["★ {name}のノバ・ハート部屋 ★", "{name}のアイドル・プロトコル研究所", "赤坂リール研究室 ({name}'s Page)",
           "{name}のノバちゃん応援ステーション！", "Stardust 14.2Hz - {name} ({city})", "{name}'s Nova-chan Fan Sanctuary ^_^"],
    "kr": ["{name}의 노바 하트 팬페이지 ^^", "은하넷 {name}의 음악 보관소", "{name}의 14.2 Hz 스타더스트 룸", "노바 하트 & 신스팝 연구 ({name})"],
    "mx": ["La Bóveda de {name} - ROCK EN ESPAÑOL & NOVA HART", "El Rincón de {name} // 14.2 Hz",
           "Página de {name}: Solos de Orion México !!!", "Santuario de Nova Hart - {name} ({city})", "ORION MÉXICO // {name}'s Home"],
    "br": ["Espaço de {name}: O Sinal de Nova Hart", "Página de {name} - Fã de 1985 !!!", "Rede Saturno: O Cantinho de {name}",
           "{name}'s Nova Hart Sanctuary ({city})"],
    "de": ["{name}'s Nova Hart Archiv ({city})", "SYNTH.GER - {name}'s Fanseite", "Knoten 05 // {name}'s Stardust Page", "{name}'s Speicher - 14.2 Hz"],
    "su": ["Страница {name}: Магнитиздат и Нова Харт", "Узел 08 - Архив {name}", "{name} / Сигнал 14.2 Гц ({city})",
           "Коллекция {name}: Катушки и Кассеты"],
    "fr": ["Le Temple de Nova - Page de {name}", "Station 3615 de {name} ({city})", "{name}'s Synth-Wave & Nova Hart"],
    "se": ["{name}'s Nova Hart-sida ({city})", "{name}'s Stardust Arkiv", "Nod 10 // {name}'s Webbsida"],
    "hi": ["★ {name} का नोवा हार्ट कॉर्नर ({city}) ★", "वीएसएनएल नोड 11 - {name} का वेबपेज", "14.2 Hz भारत आर्काइव - {name}",
           "{name}'s Nova Hart Sanctuary ({city})", "पालिका बाज़ार टेप संग्रह // {name}"],
    "au": ["★ {name}'s Aussie Nova Hart Shrine ({city}) ★", "Node 12 Down Under - {name}'s GeoCities Hub",
           "{name}'s BigPond 14.2 Hz Listening Post", "Triple J Off-Air Tapes // {name} ({city})", "{name}'s Aussie Tape Exchange & Shrine"],
    "it": ["★ Il Santuario di {name} - Nova Hart Italia ★", "Nodo 07 Milano/Roma - {name}'s Stardust Page", "{name}'s Synth-Pop Archive ({city})",
           "La Stazione 14.2 Hz di {name} // Ricordi Master", "Spazio di {name} // Fan di Nova Hart dal 1985", "{name}'s Italian Cassette Exchange // {city}"],
    "fj": ["★ {name}'s Pacific Island Relay // {city} ★", "Bula! {name}'s South Pacific Nova Hart Page",
           "USP Satellite Station 13 - {name} ({city})", "Suva Shortwave DX Hub - {name}"],
}
TITLES_EN = ["{name}'s Nova Hart Corner", "★ {name}'s Stardust Shrine ★", "The 14.2 Hz Station - {name} ({city})",
             "{name}'s Tape Exchange // NOVA HART", "Where Is Nova? - {name}'s GeoCities Page", "{name}'s SYNTHESIS Archive",
             "Project Stardust Fan Hub - Station {station}", "{name}'s Retro Wave & Nova Hart Sanctuary"]
MARQUEES_EN = ["~ hold for relay ~", "welcome to station #{station} !!", "★ NOVA HART 4EVER ★", "the hatch is open",
               "14.2 Hz -- THE CARRIER SURVIVES", "Akasaka Branch Archive // Online", "Where is Nova? Postcards to LA!",
               "02:14 UTC -- KEEP THE CHANNELS OPEN", "Orion Records Advanced Acoustics Lab -- declassified?",
               "Seiko Cut / 80s Idol Pop Forever", "El rock no ha muerto // Bóveda CDMX", "Магнитиздат копия №{copy_no}"]

# Link tokens resolved to site paths (urlmap.publicUrl maps them to hosts).
LINK_POOL = [
    ("alt.fan.nova-hart archive", "usenet/alt-fan-nova-hart/index.html"),
    ("alt.music.synth-pop", "usenet/alt-music-synth-pop/index.html"),
    ("Anonymous FTP Archive: Ashford-Poly", "ftp/ashford-poly/index.html"),
    ("Anonymous FTP Archive: Kamome Net", "ftp/kamome/index.html"),
    ("Regional Node 01: Northvale Gopher (USA)", "regional/01-usa/index.html"),
    ("Regional Node 02: Kamome BBS (Japan)", "regional/02-japan/index.html"),
    ("Regional Node 04: Red Coyoacán (Mexico)", "regional/04-mexico/index.html"),
    ("Regional Node 08: Relcom Node 08 (USSR)", "regional/08-ussr/index.html"),
    ("Regional Node 11: VSNL Gateway (India)", "regional/11-india/index.html"),
    ("Regional Node 12: OzEmail Node (Australia)", "regional/12-australia/index.html"),
    ("Regional Node 13: USP Pacific Relay (Fiji)", "regional/13-fiji/index.html"),
    ("Tokyo Garden #1420 - Akasaka Shrine", "geocities/tokyo-garden-1420.html"),
    ("Silicon Valley Lab #1984 - DSP Lab", "geocities/siliconvalley-lab-1984.html"),
    ("Athens Forum #3317 - Fourier Lab", "geocities/athens-forum-3317.html"),
    ("Paris Left Bank #0142", "geocities/paris-leftbank-0142.html"),
]
THREAD_LINKS = [("comp.dsp - 14.2 Hz spectral discussion", "t01-spectral-line"),
                ("alt.conspiracy - Kestrel's testimony", "t03-kestrel"),
                ("Akasaka Tapes Recovery (May 1995)", "t14-akasaka")]


def dump(rel, obj):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def main():
    if os.path.exists(os.path.join(OUT, "base.json")) and "--force" not in sys.argv:
        sys.exit("data/bank_v3 already exists; it is now hand/LLM-edited. Re-run with --force to clobber.")
    lore = json.load(open(os.path.join(ROOT, "data", "lore_seeds.json"), encoding="utf-8"))
    tgroup = {t["id"]: t["group"] for t in lore["usenet_threads"]}
    links = [{"t": t, "p": p} for t, p in LINK_POOL]
    for t, tid in THREAD_LINKS:
        links.append({"t": t, "p": "usenet/%s/%s.txt" % (tgroup[tid].replace(".", "-"), tid)})

    base = {
        "songs": sb.SONGS, "jp_singles": sb.JP_SINGLES, "midi_slugs": sb.MIDI_SLUGS,
        "node_lines": {str(k): v for k, v in sb.NODE_LINES.items()}, "fake_lines": sb.FAKE_LINES,
        "receivers": sb.RECEIVERS, "formats": sb.FORMATS, "emo": sb.EMO, "archetypes": sb.ARCHETYPES, "voice": sb.VOICE,
        "who": sb.WHO, "grades": sb.GRADES, "prices": sb.PRICES, "decks": sb.DECKS, "computers": sb.COMPUTERS,
        "modems": sb.MODEMS, "phones": sb.PHONES, "ascii_art": sb.ASCII_ART,
        "badges": sc.BADGE_LIST, "hood_themes": gb.HOOD_THEMES, "links": links,
        "titles_en": TITLES_EN, "marquees_en": MARQUEES_EN,
        "en": {
            "hi": sb.HI, "how": sb.HOW, "favorite": sb.FAVORITE, "theory_a": sb.THEORY_A, "theory_b": sb.THEORY_B,
            "where_i_was": sb.WHERE_I_WAS, "collection_notes": sb.COLLECTION_NOTES, "trading_wants": sb.TRADING_WANTS,
            "trading_haves": sb.TRADING_HAVES, "spectrum": sb.SPECTRUM, "gear": sb.GEAR, "listening": sb.LISTENING,
            "node_hunt": sb.NODE_HUNT, "marcus": sb.MARCUS, "skeptic": sb.SKEPTIC, "letter": sb.LETTER, "top5": sb.TOP5,
            "concert": sb.CONCERT, "pen_pals": sb.PEN_PALS, "fanart": sb.FANART,
        },
    }
    dump("base.json", base)

    for key, reg in sb.REGIONS.items():
        r = dict(reg)
        r["palettes"] = sb.REGION_PALETTES.get(key, sb.REGION_PALETTES["us"])
        r["pressing"] = sb.PRESSINGS.get(key, sb.PRESSINGS["us"])
        r["node"] = sb.REGION_NODE.get(key, 1)
        r["titles"] = TITLES.get(key, [])
        if key in sb.NATIVE and reg.get("lang") not in sb.NATIVE:
            r["native"] = sb.NATIVE[key]  # e.g. Australian English
        dump("regions/%s.json" % key, r)

    for lang in sorted(set(r["lang"] for r in sb.REGIONS.values())):
        dump("lang/%s.json" % lang, {
            "native": sb.NATIVE.get(lang, {}),
            "ui": gb.UI_LANGS.get(lang, {}),
            "info": gb.LANG_INFO.get(lang, gb.LANG_INFO["en"]),
        })
    print("exported to", OUT)


if __name__ == "__main__":
    main()
