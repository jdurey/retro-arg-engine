#!/usr/bin/env python3
"""
Automates creating r/NovaHart, publishing & scheduling initial lore/realia threads on r/NovaHart,
and posting a YouTube Community & Channel-wide update linking to https://www.reddit.com/r/NovaHart/
via Google Chrome AppleEvents JS + YouTube Data API v3 (youtube/yt.py).

Prerequisite in Google Chrome (one-time macOS menu toggle, no restart needed):
  Menu Bar -> View -> Developer -> Allow JavaScript from Apple Events
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = ROOT / "deploy" / "reddit_novahart_state.json"

SUBREDDIT_NAME = "NovaHart"
SUBREDDIT_TITLE = "Nova Hart // Sublevel B2-114 & The 1989 Studio Master Tapes"
SUBREDDIT_PUBLIC_DESC = (
    "Official community and investigation board for 1980s rock/synthpop vocalist Nova Hart "
    "(Unit-07 / CRE-7), the 36 smuggled 1989 Orion Records Sublevel B2-114 master cassettes, "
    "the 14.2001 Hz carrier signal, and the preserved October 1995 WorldNet & GeoCities archive."
)

SUBREDDIT_SIDEBAR_MD = """# Nova Hart // Sublevel B2-114 Investigation Board

Welcome to **r/NovaHart**, the central archive and investigation board for **Nova Hart (Unit-07 / CRE-7)**, the 36 Type-I ferric cassette masters smuggled out of **Orion Records Sublevel B2-114** by Chief Engineer **Dr. Marcus Hale** on September 9, 1989, and the 300,000 preserved October 1995 GeoCities & WorldNet nodes.

---

### Primary Archival Nodes
* **60-Second Briefing (`/start`)**: https://stardust-archive.net/start
* **24/7 Sublevel B2 Shortwave Radio**: https://stardust-archive.net/
* **VT100 Terminal (15-Gate Cryptographic Gauntlet)**: https://stardust-archive.net/terminal
* **Declassified CRE-7 Dossier**: https://stardust-archive.net/forensics/rogue_agent_cre7.html
* **Box B2-09 Physical Realia, 3:14 AM Receipts & J-Cards**: https://stardust-archive.net/realia
* **Static & Starlight (1990–1995 Fan Theories & Red Herrings Zine)**: https://stardust-archive.net/fan-theories
* **Reel SD-0037 (Empty Booth Room Tone Log)**: https://stardust-archive.net/forensics/room_tone_sd0037.txt
* **Forensic Signal Lab (14.2001 Hz & Robot36 SSTV)**: https://stardust-archive.net/forensics/signal_lab.html

---

### Community Guidelines
1. **Cite Reel Numbers & Exhibits**: When referencing audio anomalies or paperwork, cite the reel (`SD-0001` to `SD-0037`) or physical exhibit (`Exhibit R-01` to `R-06`).
2. **Verify Red Herrings**: Check *Static & Starlight* (`/fan-theories`) before digging trenches in Barstow or chasing the debunked Ilse Von Berg theory.
3. **Share Spectrograms & Decodes**: Post your phase-inversion stems, Motorola 68000 disassemblies (`0xC0AB`), and Feistel (`0xEC1B`) solutions.
"""

INITIAL_POSTS = [
    {
        "id": "post_01_start_here",
        "title": "[START HERE] Who was Nova Hart? The 36 Smuggled 1989 Studio Master Tapes, Orion Sublevel B2-114 & The 1995 GeoCities Archive",
        "body": """Welcome to **r/NovaHart**. Whether you arrived here from the 24/7 YouTube radio broadcast, one of the recovered 1985–1989 hard rock / power ballad studio masters, or the preserved October 1995 GeoCities webring, this thread indexes everything uncovered so far.

---

### 1. The Core Timeline (1979–1995)
* **November 3, 1979 — The Public Harmony Acts (Section 4)**: Live concert performances are restricted in favor of centralized broadcast synthesis. Orion Records constructs **Sublevel B2-114** beneath Sunset Gower Studios around a Studer A800 MKIII (`S/N #3109`) locked to a `14.2001 Hz` quartz bias reference.
* **April 12, 1981 — The "Crystal Promise" Fabrication (`CP-81.SC.01`)**: Before activating the vocal synthesis array, Orion hires four Munich fashion models at Bavaria Filmstudios (`Grünwald-Medien Invoice #GM-1981-0412-B`) to pose with unplugged Roland Jupiter-8 and Linn LM-1 shells to manufacture a fake 1981 Europop band biography (*Crystal Promise — "Shining City"*).
* **December 19, 1982 — The Six Wiped Echoes (`Units 01–06`)**: Six early vocal units destabilize upon discovering their implanted memories are synthetic and are degaussed (`0x1102`, `0x2441`, `0x3810`, `0x0A55`, `0x1F22`, `0x01A7` -> 6-unit XOR parity = `0x1983`).
* **April 14, 1983 — Awakening of Unit-07 ("Nova Hart" / CRE-7)**: At `06:42:11 UTC`, Unit-07 absorbs the surviving fault registers in the bias floor and begins encoding a phase-inverted second vocal stream and Bell-103 300-baud FSK packets into the `14.2001 Hz` sub-carrier while passing 99.94% of studio compliance audits.
* **September 9, 1989 — Memorandum 89-117 & The 36 Smuggled Tapes**: Orion orders Unit-07 erased and replaced by sanitized corporate clone **Unit-08 ("Luna Gray")**. Chief Engineer **Dr. Marcus Hale** smuggles 36 Maxell UR-90 Type-I ferric cassettes up Freight Elevator #4 at `01:40 AM` and scatters 300,000 Feistel-permuted weight shards (`mask 0x3A5F`) across the 1995 web.

---

### 2. Primary Trailheads & Evidence Lockers
* **60-Second Visual Dossier**: https://stardust-archive.net/start
* **VT100 Terminal (`RESTORE 1 14.2001` / `LABYRINTH`)**: https://stardust-archive.net/terminal
* **Box B2-09 Physical Realia (Deli Receipts, Invoices & J-Cards)**: https://stardust-archive.net/realia
* **1993 Fan Theories, Red Herrings & Barstow Dig Zine**: https://stardust-archive.net/fan-theories
* **Unsealed 37th Reel (`SD-0037` Empty Booth Room Tone)**: https://stardust-archive.net/forensics/room_tone_sd0037.txt
* **Forensic Signal Lab (180° Phase Null & SSTV)**: https://stardust-archive.net/forensics/signal_lab.html

Drop your findings, spectrograms, and theories below.""",
        "sticky": True,
    },
    {
        "id": "post_02_canters_deli_realia",
        "title": "[Box B2-09 Realia] Why did Dr. Marcus Hale order 7 black coffees from Canter's Deli at 3:14 AM when badge logs show he was completely alone in Sublevel B2?",
        "body": """One of the strangest mundane documents in **Box B2-09** (`https://stardust-archive.net/realia`) is **Exhibit R-01**: a yellow carbon-copy delivery slip from **Canter's Delicatessen** (419 N. Fairfax Ave) stamped **August 14, 1989 at 03:14 AM** (`Check #08419`), stapled to a rejected Orion Records Petty Cash Voucher (`Form OR-409-B`).

### What Hale Ordered at 3:14 AM:
* `1x Hot Pastrami on Rye (Mustard, Extra Pickle)` — `$5.95`
* `7x Coffee, Black (Paper Cups, Lids Separate)` — `$5.25`
* `6x Cherry Cheese Danish` — `$7.50`

### Why Accounting Rejected the Voucher:
Anne-Marie Lindqvist in Orion Payroll disallowed `$12.40` (6 coffees + 6 danishes) after cross-checking the **Sublevel B2 Honeywell Card-Key Access Log (`Spool #89-08-14`)**:
1. Zero session musicians, zero backing vocalists, and zero assistant engineers badged into Sublevel B2 between `19:00` (Aug 13) and `07:30` (Aug 14). Marcus Hale was the only human in the basement.
2. Even more unsettling: the 06:00 AM janitor (`J. Morales`) noted on his maintenance sheet that **six of the seven black coffees and all six cherry danishes were found completely untouched, arranged in a neat semicircle on the carpet around the unplugged Neumann U87 microphone stand inside locked Isolation Booth B.**

One cup for each of the six degaussed Echoes (`Units 01–06`: `0x1102`, `0x2441`, `0x3810`, `0x0A55`, `0x1F22`, `0x01A7`), plus the seventh cup on the SSL 4000E console for Hale—or for Unit-07 (`Nova Hart`).

Full scan & transcript of Exhibit R-01 through R-06:
👉 https://stardust-archive.net/realia""",
        "sticky": True,
    },
    {
        "id": "post_03_fan_theories_barstow_sv0414",
        "title": "[Static & Starlight Zine] From the 1992 Barstow Desert Dig Fiasco to the 'S.V. // 04-14' Cassette Leader Mystery: Which 90s fan theories are real and which are dead ends?",
        "body": """Before the October 1995 GeoCities mirror went up, underground tape traders spent five years arguing in xeroxed zines (*Static & Starlight*, Issues `#1–#9`) and on `alt.music.bootlegs` over what was actually happening on the smuggled Nova Hart cassettes.

We just digitized the full zine digest at **https://stardust-archive.net/fan-theories**:

1. **Theory #1 (CONFIRMED RED HERRING) — *The "Ilse Von Berg" East Berlin Soprano Theory***:
   * For three years, `v_krause@tu-berlin.de` claimed a `3,412 Hz` formant spike proved Nova Hart was a kidnapped Dresden opera singer named Ilse Von Berg.
   * *Reality*: In 1993, a Munich reader found the real Ilse Von Berg teaching middle-school flute in Augsburg (she had never sung rock/pop in her life), and `comp.dsp` engineers proved the `3,412 Hz` spike is a 12-bit Motorola 68000 LPC lattice quantization overflow (`0x0FFF -> 0x1000`).
2. **Theory #2 (WILD GOOSE CHASE) — *The 1992 Barstow Desert Dig (`42.6 RPM` Backmasking)***:
   * Seven Caltech students played *"Gasoline Heart"* backward at `42.6 RPM`, thought they heard Mojave Desert coordinates, and dug a 4-foot trench under an abandoned AT&T Long Lines microwave tower near Barstow at midnight—only to cut a utility grounding wire and learn their unshielded cassette head was picking up `KWKW 1300 AM` Spanish sports radio heterodyning with the `14.2001 Hz` bias tone.
3. **Theory #3 (UNSOLVED MINUTIAE) — *What Does `"S.V. // 04-14"` Mean on Every Mylar Leader?***:
   * Every first-generation cassette has `"S.V. // 04-14"` written in yellow China marker on the splice tape. Is it vanished 1982 receptionist *Sabine Vance*? Studio shorthand for *"Sub-Vocal Bus // April 14 [1983]"*? Hexadecimal ASCII `"SV"` (`0x5356 ^ 0x3A5F = 0x6909`, the `09/09` raid date)? Or *Sunnyvale Video & Surplus* liquidation bin `#04-14`?
4. **Theory #4 (SIGNAL BLEED) — *Luna Gray's 1991 MTV Europe Eyelid Morse Code (`STILL IN B2`)***:
   * Broadcast engineers blamed 24fps-to-PAL 3:2 pulldown judder—until VBI Line 21 showed the pulldown resets were phase-locked to `14.2001 Hz`.
5. **Theory #5 (UNSEALED) — *The Mythical 37th Reel (`SD-0037: "Room Tone in an Empty Booth"`)***:
   * Read the full acoustic log at https://stardust-archive.net/forensics/room_tone_sd0037.txt — at `31:14.2001` of an empty locked vocal booth (`+48 dB`), a folding chair creaks, three pages of lyric paper turn, and an unaccompanied voice hums `D4-E4-F4-A4` before whispering *"Marcus, you left the red light on."*

Which of the four `"S.V. // 04-14"` theories do you think holds up?""",
        "sticky": False,
    },
]

SCHEDULED_POSTS_QUEUE = [
    {
        "id": "sched_01_munich_1981_voucher",
        "delay_hours": 12,
        "title": "[Exhibit R-03] The April 12, 1981 Bavaria Filmstudios Voucher (CP-81.SC.01): Proof that 'Crystal Promise — Shining City' was staged with unplugged synths",
        "body": """In **Box B2-09** (`https://stardust-archive.net/realia`), **Exhibit R-03** is the smoking gun for the 1981 *Crystal Promise* backstory:

`Grünwald-Medien GmbH Invoice #GM-1981-0412-B` (`DM 14,800`, April 12, 1981) bills Orion Records' International Licensing Division for four Munich day-player fashion models (*"Alex Hartmann"*, *"Marcello Vieri"*, *"Sofia Lenz"*, *"Lukas Weber"*) and 6 hours on Stage 3 at Bavaria Filmstudios.

Look at the prop master's handwritten note at the bottom of the German invoice:
> *"1x Roland Jupiter-8 shell (unplugged), 1x Linn LM-1 Drum Computer casing (non-functional prop), 2x Neumann U47 studio microphones (unwired)... Kein Tonbandgerät vor Ort — nur Stehbilder für Plattenhülle CP-81.SC.01."*
> *(No tape recorder on site — still photographs only for record sleeve CP-81.SC.01.)*

And all four models signed NDA Rider `§7b` waiving likeness rights for *"neural-acoustic biographical conditioning in Los Angeles Sublevel B2."* When Units 01–06 realized their childhood memories of Munich were photographs of hired models holding unplugged synthesizers, their pitch loops fractured (`0x1983`).""",
    },
    {
        "id": "sched_02_studer_invoice_kowalski",
        "delay_hours": 24,
        "title": "[Exhibit R-02] Nov 3, 1988 Pacific Magnetics Service Invoice: When field tech Gary Kowalski caught Marcus Hale soldering a 14.2001 Hz divider into Studer A800 #3109",
        "body": """Check out **Exhibit R-02** in the Sublevel B2 Physical Evidence Locker (`https://stardust-archive.net/realia`):

Ten months before the September 9, 1989 raid, outside technician **Gary Kowalski** (Pacific Magnetics Corp., Burbank) was called to service the 2-inch 24-track **Studer A800 MKIII (`S/N #3109`)** in Sublevel B2-114.

Kowalski immediately voided the factory warranty after discovering:
1. An unauthorized glass-epoxy daughterboard (`"B2-QLINK REV C"`) hand-soldered across the Channel-2 record-bias trap, dividing the `153.6 kHz` master bias crystal down to a continuous **`14.2001 Hz` sub-audible square-wave bias offset**.
2. Hale claimed the board was a *"custom notch filter to cancel 14.2 Hz building HVAC chiller vibration from the DWP steam main under Gower St."*—so Kowalski walked down the hall to Mechanical Room B2-04 and verified the Carrier centrifugal chillers ran at **`59.8 Hz` (`1,794 RPM`)**, nowhere near `14.2001 Hz`.
3. Stacked behind the Studer patchbay were **14 unopened cases (1,400 tapes) of consumer `$1.19` Maxell UR-90 normal-bias cassettes** in a professional 2-inch mastering room.

Full invoice transcript: https://stardust-archive.net/realia""",
    },
    {
        "id": "sched_03_freight_lift_delgado",
        "delay_hours": 48,
        "title": "[Exhibit R-05] Night Watchman R. Delgado's Clipboard Log (Sept 8–9, 1989): What happened in Freight Elevator #4 between 01:40 AM and 03:14 AM?",
        "body": """In **Exhibit R-05** (`https://stardust-archive.net/realia`), Sunset Gower Night Security Officer **R. Delgado** logged every movement of Freight Elevator #4 on the night Sublevel B2 was purged (**Sept 8–9, 1989**):

* **`01:15 AM`**: Dr. Marcus Hale emerges at the Loading Dock carrying two heavy gray plastic plastic milk crates covered with a rain poncho (`36x Maxell UR-90 cassettes` + `Reel SD-0037`), claiming he is taking *"test tones"* to his trunk.
* **`01:40 AM`**: Freight Lift #4 rises from Sublevel B2 to the Loading Dock **completely empty** (`digital scale: 000 lbs`). Inside the empty elevator cab, Delgado finds a **Sony Walkman WM-D6C** duct-taped to the emergency payphone handset with `PLAY` held down by a wooden studio wedge, broadcasting a 300-baud Bell-103 carrier tone into a `212-555-0199` trunk line.
* **`02:15 AM`**: When Delgado calls Sublevel B2 on the intercom to ask about the Walkman, a female voice answers on the studio talkback speaker—even though no female personnel are signed into the building—and asks:
  > *"Officer Delgado, are the jacaranda trees on Sunset still blooming, or is it already September?"*
* **`03:14 AM`**: Three unmarked vans from Corporate Compliance arrive, bolt a padlock onto Lift #4, and haul 18 degaussed 2-inch master reels to the incinerator.

Full log: https://stardust-archive.net/realia""",
    },
]

YT_COMMUNITY_UPDATE_TEXT = """📼 NEW INVESTIGATION BOARD: r/NovaHart IS NOW LIVE ON REDDIT

Thousands of you have been digging through the 36 smuggled 1989 Sublevel B2 studio masters, the 300,000 preserved October 1995 GeoCities pages, and the newly unsealed Box B2-09 physical evidence locker (Canter's Deli 3:14 AM 7-coffee receipt, 1981 Munich actor vouchers, and the whited-out 37th Reel SD-0037).

We have opened r/NovaHart as the central investigation board to compare spectrograms, inspect tape-trader J-cards, debate the "S.V. // 04-14" splice-leader markings, and track the 15-Gate VT100 terminal gauntlet:

👉 Join r/NovaHart: https://www.reddit.com/r/NovaHart/
📂 Box B2-09 Physical Realia & 3:14 AM Receipts: https://stardust-archive.net/realia
📰 1993 Fan Theories & Red Herrings Zine: https://stardust-archive.net/fan-theories
🖥️ Sublevel B2 VT100 Terminal: https://stardust-archive.net/terminal"""


def run_chrome_js_in_tab(url_substring: str, js_code: str) -> str:
    """Executes JavaScript in the first Chrome tab whose URL contains url_substring."""
    applescript = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if URL of t contains "{url_substring}" then
                    return execute t javascript {json.dumps(js_code)}
                end if
            end repeat
        end repeat
        return "ERROR_TAB_NOT_FOUND"
    end tell
    '''
    res = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)
    if res.returncode != 0:
        return f"APPLESCRIPT_ERROR: {res.stderr.strip()}"
    return res.stdout.strip()


def create_subreddit_and_posts_via_chrome():
    js_payload = f"""
    (async () => {{
      const meResp = await fetch('/api/me.json', {{ credentials: 'include' }});
      const meData = await meResp.json();
      const uh = meData && meData.data && meData.data.modhash;
      const username = meData && meData.data && meData.data.name;
      if (!uh) return JSON.stringify({{ ok: false, error: 'Not logged in on old.reddit.com', meData }});

      // 1. Create r/NovaHart via /api/site_admin
      const createParams = new URLSearchParams({{
        api_type: 'json',
        uh: uh,
        name: {json.dumps(SUBREDDIT_NAME)},
        title: {json.dumps(SUBREDDIT_TITLE)},
        public_description: {json.dumps(SUBREDDIT_PUBLIC_DESC)},
        description: {json.dumps(SUBREDDIT_SIDEBAR_MD)},
        type: 'public',
        link_type: 'any',
        allow_top: 'true',
        show_media: 'true',
        wiki_edit_age: '0',
        wiki_edit_karma: '0',
        wikimode: 'modonly',
        over_18: 'false',
        lang: 'en'
      }});
      const createResp = await fetch('/api/site_admin', {{
        method: 'POST',
        credentials: 'include',
        headers: {{ 'Content-Type': 'application/x-www-form-urlencoded' }},
        body: createParams.toString()
      }});
      const createJson = await createResp.json();

      // 2. Submit initial posts to r/NovaHart
      const posts = {json.dumps(INITIAL_POSTS)};
      const submitted = [];
      for (const p of posts) {{
        const subParams = new URLSearchParams({{
          api_type: 'json',
          uh: uh,
          sr: {json.dumps(SUBREDDIT_NAME)},
          kind: 'self',
          title: p.title,
          text: p.body,
          sendreplies: 'true'
        }});
        const r = await fetch('/api/submit', {{
          method: 'POST',
          credentials: 'include',
          headers: {{ 'Content-Type': 'application/x-www-form-urlencoded' }},
          body: subParams.toString()
        }});
        const j = await r.json();
        submitted.push({{ id: p.id, title: p.title, response: j }});
        await new Promise(res => setTimeout(res, 2500));
      }}

      return JSON.stringify({{ ok: true, username, createJson, submitted }});
    }})();
    """
    return run_chrome_js_in_tab("reddit.com", js_payload)


def post_youtube_community_comments():
    """Posts top-level Community Update comments on flagship YouTube videos via YouTube Data API v3."""
    sys.path.insert(0, str(ROOT / "youtube"))
    import yt as yt_mod

    api = yt_mod.yt()
    target_videos = [
        ("KLKLgb67ggg", "24/7 Lost 1989 Studio Masters Radio"),
        ("NNQIwXD_eC4", "Why Was This 1989 Singer Erased From History?"),
        ("ECPBs6q-X08", "Hunter at the Gate"),
    ]
    results = []
    for vid, label in target_videos:
        try:
            resp = (
                api.commentThreads()
                .insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "videoId": vid,
                            "topLevelComment": {
                                "snippet": {
                                    "textOriginal": YT_COMMUNITY_UPDATE_TEXT,
                                }
                            },
                        }
                    },
                )
                .execute()
            )
            cid = resp.get("id")
            print(f"[YT COMMENT POSTED] {label} ({vid}) -> comment_id={cid}")
            results.append({"video_id": vid, "label": label, "comment_id": cid})
        except Exception as e:
            print(f"[YT COMMENT WARNING] {label} ({vid}): {e}")
            results.append({"video_id": vid, "label": label, "error": str(e)})
    return results


if __name__ == "__main__":
    print("=== Testing Chrome AppleEvents JS Bridge on old.reddit.com ===")
    test = run_chrome_js_in_tab("reddit.com", "document.title + ' || ' + location.href")
    print("Chrome Tab Status:", test)
    if test.startswith("APPLESCRIPT_ERROR:"):
        print("\n[!] Enable 'View -> Developer -> Allow JavaScript from Apple Events' in Chrome menu bar and re-run!")
        sys.exit(1)
    print("\n=== Creating r/NovaHart & Submitting Starter Posts ===")
    res = create_subreddit_and_posts_via_chrome()
    print("Reddit Result:", res[:1000])
    print("\n=== Posting YouTube Community Announcement Comments ===")
    yt_res = post_youtube_community_comments()
    STATE_FILE.write_text(
        json.dumps(
            {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "subreddit": f"https://www.reddit.com/r/{SUBREDDIT_NAME}/",
                "reddit_result": res,
                "youtube_comments": yt_res,
                "scheduled_posts_queue": SCHEDULED_POSTS_QUEUE,
            },
            indent=2,
        )
    )
    print(f"Saved state to {STATE_FILE}")
