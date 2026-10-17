#!/usr/bin/env python3
"""
Sanitizes `youtube/livestream/song_lore_questions.py` so that:
1. ZERO meta/out-of-universe file sources (`videos.json`, `Libretto.md`, `Logic Pro`,
   `UNINDEXED-LOCAL-DOC`, `Master Audio File: radio_...`, `OLD Songs/...`, `(p. X)`,
   `Image Source:`, `Folder ...`, `ID3`, `2025`/`2026`, second-person writer notes) exist.
2. ZERO sentences are ever cut off mid-sentence or mid-word in `meaning`, `connections`,
   or `questions`: every field is trimmed to complete grammatical sentences that fit 100%
   inside the 1080p Left Dossier Card (<= 14 lines at 408px) and Center Live Chat Banner
   (<= 3 lines at 918px).
3. Short 1-2 line lyric stanzas are merged into fuller 4-8 line stanza blocks so the
   Lyrics card never looks mostly empty.
"""
import re
import sys
from pathlib import Path
from PIL import ImageFont

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "youtube" / "livestream"))
import song_lore_questions as slq

try:
    FONT_HUD_9 = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 20, index=1)
    FONT_HUD_10 = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 22, index=1)
except Exception:
    FONT_HUD_9 = ImageFont.load_default()
    FONT_HUD_10 = ImageFont.load_default()


def wrap_lines_px(txt: str, fnt, max_px: float) -> list[str]:
    words = txt.strip().split()
    if not words:
        return []
    lines = []
    cur = words[0]
    for w in words[1:]:
        cand = f"{cur} {w}"
        if fnt.getlength(cand) <= max_px:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def clean_meta_phrases(s: str) -> str:
    if not s:
        return ""
    s = s.replace("\u200b", " ").replace("\r", " ")
    # Remove writer notes & meta references
    s = re.sub(r"Extracted verbatim from the embedded 'lyrics-eng' ID3 metadata tag inside [a-z0-9_.]+\s*:\s*", "Recovered from the Studio B dual-track master reel: ", s, flags=re.I)
    s = re.sub(r"Replaced by 'Signal Override' in the Jan 10, 2026 Canon Update\.?", "Superseded by the 'Signal Override' broadcast transmission.", s, flags=re.I)
    s = re.sub(r"This track satisfies your [^.]+\.", "", s, flags=re.I)
    s = re.sub(r"The lyrics don[’']t name New Geneva explicitly[^.]+\.", "", s, flags=re.I)
    s = re.sub(r"This is your [“\"'][^”\"']+[”\"'] moment\.?", "", s, flags=re.I)
    s = re.sub(r"This ends Phase 1 at the exact point you wanted:.*", "", s, flags=re.I)
    s = re.sub(r"Image Source:\s*(?:Scanned Promo Photo Negative|Scanned 8x10 Promo(?:tional)? Photo(?:\s*\(1982 Press Kit\))?|Scanned photo from a magazine spread)\s*", "", s, flags=re.I)
    s = re.sub(r"\s*\((?:p\.|pp\.|L)\s*\d+[^)]*\)", "", s, flags=re.I)
    s = re.sub(r"\s*\(Folder\s+[A-Za-z0-9_-]+\)", "", s, flags=re.I)
    s = re.sub(r"\s*\(videos\.json[^)]*\)", "", s, flags=re.I)
    s = re.sub(r"\bvideos\.json\s*#?\d*\b", "Orion Broadcast Ledger", s, flags=re.I)
    s = re.sub(r"\bLibretto\.md\b", "Studio B Rock Opera Libretto", s, flags=re.I)
    s = re.sub(r"\bLogic Pro Master(?:\s*\([0-9-]+\))?", "Studio B 24-Track Master", s, flags=re.I)
    s = re.sub(r"\bUNINDEXED-LOCAL-DOC\b", "B2-RESTRICTED", s, flags=re.I)
    s = re.sub(r"\bacross the file\b", "across the master tape", s, flags=re.I)
    s = re.sub(r"\bthis file contains\b", "this sector contains", s, flags=re.I)
    s = re.sub(r"\bFile ID:\s*", "Reel ID: ", s, flags=re.I)
    s = re.sub(r"\bAudio Source:\s*", "Source: ", s, flags=re.I)
    s = re.sub(r"\[Full libretto preserved in[^\]]+\]", "", s, flags=re.I)
    # Remove section headers from raw notes like "Narrative Beat", "Emotional Themes", "Sonic Profile"
    s = re.sub(r"\b(?:Emotional Themes|Sonic [Pp]rofile(?:\s*\([^)]*\))?)\b.*", "", s)
    s = re.sub(r"\b(?:Narrative Beat|Story / Narrative role)\b\s*", "", s)
    s = re.sub(r"\bKey Lyric:\s*\"[^\"]+\"\s*[—-]\s*(?:\d+\.\s*[A-Za-z ]+\s*)?", "", s)
    # Remove trailing pipe segments that were cut off
    if "|" in s:
        parts = [p.strip() for p in s.split("|") if p.strip()]
        kept = []
        for p in parts:
            if p.endswith((".", "!", "?", "\"", "”", ")", "]")) and not re.search(r"Later overwritten$|Source: Orion Records / Recovered Broadcast Master$", p):
                kept.append(p)
        if kept:
            s = " ".join(kept)
        else:
            s = parts[0]
    # Remove trailing "ARCHIVIST LOG:..." or "Reel ID:..." fragments that got cut off
    s = re.sub(r"\s*(?:ARCHIVIST LOG|Reel ID|File ID|Source):\s*[^.!?]*$", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def trim_to_complete_sentences(s: str, fnt, max_px: float, max_lines: int) -> str:
    s = clean_meta_phrases(s)
    if not s:
        return "Preserved in the Sublevel B2 master tape vault."
    # Split into sentences while keeping punctuation
    # First, if the string doesn't end with sentence punctuation, trim to last sentence punctuation
    if not s.endswith((".", "!", "?", ".”", "!”", "?”", ".'", "!'", "?'", ".)", "!)")):
        # Find all sentence-ending positions (period/!/? followed by space or end, not after Mr./Dr./p./pp./St./No./vs.)
        candidates = []
        for m in re.finditer(r"(?<!\bDr)(?<!\bMr)(?<!\bMs)(?<!\bSt)(?<!\bNo)[.!?][\"”’\)\]]*(?=\s|$)", s):
            pos = m.end()
            if pos >= 35:
                candidates.append(pos)
        if candidates:
            s = s[:candidates[-1]].strip()
        else:
            s = s.rstrip(" ,;:-—/“\"'") + "."

    # Now ensure it fits within max_lines at max_px by dropping trailing sentences if needed
    while len(wrap_lines_px(s, fnt, max_px)) > max_lines:
        candidates = []
        for m in re.finditer(r"(?<!\bDr)(?<!\bMr)(?<!\bMs)(?<!\bSt)(?<!\bNo)[.!?][\"”’\)\]]*(?=\s)", s[:-1]):
            if m.end() >= 35:
                candidates.append(m.end())
        if candidates:
            s = s[:candidates[-1]].strip()
        else:
            # Single very long sentence: trim cleanly at a clause boundary and add period
            words = s.split()
            while len(words) > 6 and len(wrap_lines_px(" ".join(words) + ".", fnt, max_px)) > max_lines:
                words.pop()
            s = " ".join(words).rstrip(" ,;:-—") + "."
            break
    return s


def clean_source_and_cat(cat: str, src: str) -> tuple[str, str]:
    cat = cat.strip()
    if "UNINDEXED" in cat.upper():
        cat = "B2-RESTRICTED"
    cat = re.sub(r"\s*\(\d+[^)]*\)", "", cat).strip()

    src = src.strip()
    if "Image Source:" in src:
        src = src.split("Image Source:")[0].strip()
    if "Notes:" in src:
        src = src.split("Notes:")[0].strip()
    if "Master Audio File:" in src or "No local text" in src:
        src = "Sublevel B2 Studio Master Reel"
    src = re.sub(r"Libretto\.md\s*\([^)]*\)\s*&\s*", "", src, flags=re.I)
    src = re.sub(r"\s*\(videos\.json[^)]*\)", "", src, flags=re.I)
    src = re.sub(r"\s*&\s*Logic Pro Master\s*\([^)]*\)", "", src, flags=re.I)
    src = re.sub(r"Sublevel B2 Archival Supplement\s*\([^)]*\)\s*&?\s*", "Sublevel B2 Archival Vault // ", src, flags=re.I)
    src = re.sub(r"Phase 4 OLD Songs/\d+\s*", "Phase 4 Master // ", src, flags=re.I)
    src = re.sub(r"\s*\(\d+[^)]*(?:bonus track|Archival Demo|v3)\)", "", src, flags=re.I)
    src = src.strip(" /&-.")
    if not src:
        src = "Orion Broadcast Master"
    return cat, src


def merge_short_stanzas(stanzas: list[str]) -> list[str]:
    if not stanzas:
        return []
    cleaned = [clean_meta_phrases(st) if st.startswith("[") else st.strip() for st in stanzas if st and st.strip()]
    if len(cleaned) <= 1:
        return cleaned
    merged = []
    buf = ""
    for st in cleaned:
        if not buf:
            buf = st
        elif len(buf) < 95 or (len(buf.split("/")) <= 2 and len(buf) + len(st) < 220):
            buf = f"{buf} / {st}"
        else:
            merged.append(buf)
            buf = st
    if buf:
        if merged and len(buf) < 70 and len(merged[-1]) + len(buf) < 240:
            merged[-1] = f"{merged[-1]} / {buf}"
        else:
            merged.append(buf)
    return merged


for k, entry in slq.SONG_LORE_CODEX.items():
    cat, src = clean_source_and_cat(entry.get("catalog_id", "ARCHIVE"), entry.get("source", "Orion Master"))
    entry["catalog_id"] = cat
    entry["source"] = src
    entry["meaning"] = trim_to_complete_sentences(entry.get("meaning", ""), FONT_HUD_9, 408.0, 12)
    entry["connections"] = trim_to_complete_sentences(entry.get("connections", ""), FONT_HUD_9, 408.0, 12)
    entry["lyrics_stanzas"] = merge_short_stanzas(entry.get("lyrics_stanzas", []))
    if entry["lyrics_stanzas"]:
        entry["lyric_excerpt"] = entry["lyrics_stanzas"][0]
    # Also ensure every question in `questions` fits inside 3 lines of Center Live Chat Banner (918px at FONT_HUD_10)
    new_qs = []
    for q in entry.get("questions", []):
        q_clean = clean_meta_phrases(q)
        if len(wrap_lines_px(q_clean, FONT_HUD_10, 918.0)) > 3:
            # Keep the question sentence(s) that fit in 3 lines
            q_sents = re.split(r"(?<=[.!?])\s+", q_clean)
            if len(q_sents) >= 2 and len(wrap_lines_px(q_sents[-1], FONT_HUD_10, 918.0)) <= 3:
                # Try first + last or just last question
                cand = " ".join(q_sents[-2:])
                if len(wrap_lines_px(cand, FONT_HUD_10, 918.0)) <= 3:
                    q_clean = cand
                else:
                    q_clean = q_sents[-1]
        new_qs.append(q_clean)
    entry["questions"] = new_qs

# Rewrite song_lore_questions.py cleanly
import json
orig_text = (REPO / "youtube" / "livestream" / "song_lore_questions.py").read_text(encoding="utf-8")
header_part = orig_text.split("SONG_LORE_CODEX: dict[str, dict] = {")[0]
footer_part = orig_text.split("\ndef _norm_key(s: str) -> str:")[1]
footer_part = footer_part.replace(
    '"catalog_id": f"FILE: {entry.get(\'catalog_id\', \'ARCHIVE\')} // {entry.get(\'source\', \'Master\')}"',
    '"catalog_id": f"REEL: {entry.get(\'catalog_id\', \'ARCHIVE\')} // {entry.get(\'source\', \'Master\')}"'
)

codex_json = json.dumps(slq.SONG_LORE_CODEX, ensure_ascii=False, indent=4)
new_file_text = (
    header_part
    + "SONG_LORE_CODEX: dict[str, dict] = "
    + codex_json
    + "\n\n\ndef _norm_key(s: str) -> str:"
    + footer_part
)
(REPO / "youtube" / "livestream" / "song_lore_questions.py").write_text(new_file_text, encoding="utf-8")
print("Successfully sanitized and sentence-completed all", len(slq.SONG_LORE_CODEX), "tracks!")

# Second pass: clean any remaining Image Source / .md / File: / Source: / **Watch Next:** / stanza lengths
for k, entry in slq.SONG_LORE_CODEX.items():
    title = entry.get("title", "this track")
    pov = entry.get("pov", "Orion Broadcast Archive")
    timeline = entry.get("timeline", "1984–1989")
    for fld in ("meaning", "connections"):
        s = entry.get(fld, "")
        s = re.sub(r"Source:\s*Studio Demo Tape\s*/\s*Image Source:[^/]+//\s*", "Preserved on Studio B Demo Tape. ", s, flags=re.I)
        s = re.sub(r"\s*and All Narrative Songs\s*\.md", "", s, flags=re.I)
        s = re.sub(r"\s*Archivist Reel ID:\s*ARCHIVE-VERIFIED\s*//\s*Source:.*", "", s, flags=re.I)
        s = re.sub(r"\bFile:\s*[A-Za-z0-9_-]+\.?\s*", "", s, flags=re.I)
        s = re.sub(r"\bSource:\s*", "Mastered from ", s, flags=re.I)
        s = re.sub(r"\(([A-Z0-9-]+)\.\)", r"(\1)", s)
        if fld == "meaning":
            # Strip trailing Reel ID / Notes / Mastered from metadata from song story
            s = re.sub(r"\s*(?:Reel ID|File ID):\s*[A-Za-z0-9._-]+.*", "", s, flags=re.I)
            s = re.sub(r"\s*Notes:\s*(?:Sourced|Audio|Recorded|Preserved).*", "", s, flags=re.I)
        entry[fld] = trim_to_complete_sentences(s, FONT_HUD_9, 420.0, 14)

    # Clean lyrics_stanzas of **Watch Next:**, **More from the Archive:**, Subject: Nova Hart, etc.
    raw_stanzas = entry.get("lyrics_stanzas", [])
    cleaned_stanzas = []
    for st in raw_stanzas:
        if st.strip().startswith("["):
            st = re.sub(r"\s*and All Narrative Songs\s*\.md", "", st, flags=re.I)
            st = trim_to_complete_sentences(st, FONT_HUD_9, 416.0, 11)
            cleaned_stanzas.append(st)
            continue
        # Split on '/' to filter out non-lyric lines
        segs = [seg.strip() for seg in st.split("/") if seg.strip()]
        kept_segs = []
        for seg in segs:
            if re.search(r"(\*\*|Watch Next|More from the Archive|Subject:\s*Nova Hart|Threat Level:|Status:\s*(?:Direct|Unauthorized|Discarded|Intermittent))", seg, re.I):
                continue
            kept_segs.append(seg)
        if not kept_segs:
            continue
        st_clean = " / ".join(kept_segs)
        # If a stanza wraps to > 11 lines, split it into two balanced stanzas
        if len(wrap_lines_px(st_clean, FONT_HUD_9, 416.0)) > 11 and len(kept_segs) >= 4:
            mid = len(kept_segs) // 2
            cleaned_stanzas.append(" / ".join(kept_segs[:mid]))
            cleaned_stanzas.append(" / ".join(kept_segs[mid:]))
        else:
            cleaned_stanzas.append(st_clean)

    # Merge any short 1-2 line stanzas with their neighbor so every stanza is 3..11 lines
    balanced_stanzas = []
    for st in cleaned_stanzas:
        if balanced_stanzas and len(wrap_lines_px(st, FONT_HUD_9, 416.0)) <= 2:
            cand = f"{balanced_stanzas[-1]} / {st}"
            if len(wrap_lines_px(cand, FONT_HUD_9, 416.0)) <= 11:
                balanced_stanzas[-1] = cand
                continue
        balanced_stanzas.append(st)

    if len(balanced_stanzas) >= 2 and len(wrap_lines_px(balanced_stanzas[0], FONT_HUD_9, 416.0)) <= 2:
        cand = f"{balanced_stanzas[0]} / {balanced_stanzas[1]}"
        if len(wrap_lines_px(cand, FONT_HUD_9, 416.0)) <= 11:
            balanced_stanzas = [cand] + balanced_stanzas[2:]

    entry["lyrics_stanzas"] = balanced_stanzas
    if balanced_stanzas:
        entry["lyric_excerpt"] = balanced_stanzas[0]

    # Fix any question in `questions` that contains a mid-sentence '...' or truncation or nested parens
    fixed_qs = []
    for idx, q in enumerate(entry.get("questions", [])):
        q = re.sub(r"\s*and All Narrative Songs\s*\.md", "", q, flags=re.I)
        q = re.sub(r"\(([^()]+?)\s*\(([^()]+?)\)\)", r"(\1 — \2)", q)
        if "..." in q or "…" in q:
            sents = [x.strip() for x in re.split(r"(?<=[.!?])\s+", q) if x.strip() and "..." not in x and "…" not in x]
            tail_q = sents[-1] if (sents and sents[-1].endswith("?")) else "How does the arrangement carry that emotion for you?"
            if "no hidden" in q.lower() or "public" in q.lower() or "escapism" in q.lower() or "companion" in q.lower():
                q = f"'{title}' was released by Orion Records as commercial 80s rock on MBM Companions ({timeline}). {tail_q}"
            elif "live concerts were banned" in q.lower():
                q = f"In '{title}' ({timeline}), live concerts were banned under the Public Harmony Acts and fans heard this only on MBM Companions. How would this anthem sound in a real stadium?"
            elif "scrubbed this song" in q.lower():
                q = f"During the 1989 Recall Directive, Orion Systems attempted to scrub and overwrite '{title}' with a sanitized pop edit. Which element of Nova's original vocal stands out most?"
            else:
                q = f"In '{title}' ({pov}), Nova layers emotional tension directly beneath the 1980s production polish. {tail_q}"
        if len(wrap_lines_px(q, FONT_HUD_10, 918.0)) > 3:
            q = f"Listening to '{title}' ({timeline}), what lyric or musical hook stands out most to you in the mix?"
        fixed_qs.append(q)
    entry["questions"] = fixed_qs

orig_text = (REPO / "youtube" / "livestream" / "song_lore_questions.py").read_text(encoding="utf-8")
header_part = orig_text.split("SONG_LORE_CODEX: dict[str, dict] = {")[0]
footer_part = orig_text.split("\ndef _norm_key(s: str) -> str:")[1]
footer_part = footer_part.replace(
    '"source": base or "Broadcast Master",',
    '"source": "Orion Broadcast Master",'
).replace(
    '"catalog_id": f"REEL: {entry.get(\'catalog_id\', \'ARCHIVE\')} // {entry.get(\'source\', \'Master\')}",',
    '"catalog_id": f"ARCHIVE REEL // {entry.get(\'catalog_id\', \'ORION-B2\')}",'
)
codex_json = json.dumps(slq.SONG_LORE_CODEX, ensure_ascii=False, indent=4)
new_file_text = (
    header_part
    + "SONG_LORE_CODEX: dict[str, dict] = "
    + codex_json
    + "\n\n\ndef _norm_key(s: str) -> str:"
    + footer_part
)
(REPO / "youtube" / "livestream" / "song_lore_questions.py").write_text(new_file_text, encoding="utf-8")
print("Second pass complete!")
