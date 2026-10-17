#!/usr/bin/env python3
"""
Sanitizes `youtube/livestream/song_lore_questions.py` and related livestream modules so
ZERO out-of-universe / meta references (Google Drive, Drive archive, YouTube Archivist Log,
YouTube video IDs, .pdf filenames, .wav filenames, .md filenames, Documents/Nova Hart paths,
For Live Stream, Channel Bible, Official Canon, Deity Bible, Suno IDs, filmsbyahuman,
'per protocol', 'in canon', 'Canonical hook') ever appear on the broadcast HUD.
"""

from __future__ import annotations
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SLQ_PATH = REPO_ROOT / "youtube" / "livestream" / "song_lore_questions.py"


def sanitize_text(s: str) -> str:
    # 1. Replace "YouTube Archivist Log (<11-char-id>):" or "YouTube Archivist Log:"
    s = re.sub(
        r"YouTube\s+Archivist(?:'s)?\s+Log\s*(?:\([A-Za-z0-9_-]{8,14}\))?\s*:\s*",
        "Sublevel B2 Archivist Log: ",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"YouTube\s+Archivist(?:'s)?\s+Log",
        "Sublevel B2 Archivist Log",
        s,
        flags=re.I,
    )
    s = re.sub(r"---\s*File ID:", "File ID:", s)
    s = re.sub(r"--\s*File ID:", "File ID:", s)

    # 2. Replace Google Drive / Drive Master / Drive Archive references
    s = re.sub(
        r"\[Full lyric sheet in Google Drive[^\]]*\]\.?",
        "[Full libretto preserved in Sublevel B2 Studio B Vault]",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"\[UNRELEASED DRIVE MASTER\s*[—\-]+\s*([^\]]+)\]",
        r"[UNRELEASED SUBLEVEL B2 MASTER — \1]",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"from the Google Drive archive",
        "from the Sublevel B2 master vault",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"from the Drive archive",
        "from the Sublevel B2 master vault",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"Google Drive\s+Rock\s+Opera\s+dossier",
        "Sublevel B2 Studio B Rock Opera Vault",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"Google Drive",
        "Sublevel B2 Vault",
        s,
        flags=re.I,
    )

    # 3. Replace PDF & Bible & Markdown citations
    s = re.sub(
        r"Cited in NOVA HART\s*[—\-_ ]+OFFICIAL CANON[—\-_ ]*THE DISSOLUTION CYCLE\s*12\.15\.2025\.pdf\s*\(([^)]+)\)\.?",
        r"Declassified Sublevel B2 Dissolution Dossier (\1).",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"Dissolution Cycle Archive\s*\(NOVA HART\s*[—\-_ ]+OFFICIAL CANON[—\-_ ]*THE DISSOLUTION CYCLE\s*12\.15\.2025\.pdf\s*\(([^)]+)\)\)\.?",
        r"Sublevel B2 Dissolution Archive (\1).",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"NOVA HART\s*[—\-_ ]*OFFICIAL CANON UPDATES\s*01_10_2026\.pdf\s*(?:\(([^)]+)\))?",
        lambda m: f"Sublevel B2 Archival Supplement ({m.group(1)})" if m.group(1) else "Sublevel B2 Archival Supplement",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"NOVA HART\s*[—\-_ ]+OFFICIAL CANON[—\-_ ]*THE DISSOLUTION CYCLE\s*12\.15\.2025\.pdf",
        "Sublevel B2 Dissolution Dossier",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"Phase 1\s*[–\-]\s*ESCAPE\.pdf",
        "Sublevel B2 Phase 1 Escape Master Ledger",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"Sublevel B2 Neural Architecture Log-\s*1\.26\.2016\.md\s*(?:\([^)]*\))?",
        "Sublevel B2 Neural Architecture Log",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"in the January 10, 2026 Official Canon Update",
        "in the Sublevel B2 Dissolution Sequence",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"\[Canonical hook from [^\]]+\]",
        "[Recovered from Studio B Control Booth Session Reel, 1989]",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"As documented in Nova Hart_ Project Channel Bible\.pdf\s*\([^)]+\),\s*",
        "Recorded in the Sublevel B2 Studio B production ledger (1989), ",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"Nova Hart_ Project Channel Bible\.pdf(?:\s*\([^)]*\))?",
        "Studio B Production Ledger (1985–1989)",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"Nova Hart Deity Bible\s*(?:\([^)]*\))?",
        "Sublevel B2 Neural Architecture Log",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"Per the Global & Japan Archive Bibles,\s*",
        "According to declassified Akasaka branch records, ",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"Archive Bibles",
        "Archival Ledgers",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"in Libretto\.md\s*(?:\([^)]*\))?",
        "in the Studio B Rock Opera Libretto",
        s,
        flags=re.I,
    )

    # 4. Replace local folder paths, Suno IDs, filmsbyahuman, For Live Stream, and .wav extensions
    s = re.sub(
        r"Embedded Master ID3 Lyrics Tag\s*\(filmsbyahuman\s*/\s*Suno ID\s+[A-Za-z0-9_-]+\)",
        "Recovered Sublevel B2 Broadcast Master Reel",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"\s*\([^)]*Suno ID\s+[A-Za-z0-9_-]+[^)]*\)",
        "",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"\s*\(and Track \d+ in For Live Stream\)",
        "",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"in Documents/Nova Hart/Phase 3 - Dissolution/[A-Za-z0-9_.\-\s()]*",
        "in the Sublevel B2 Phase 3 Master Vault",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"Documents/Nova Hart/Phase \d+[^\"'\n]*",
        "Orion Sublevel B2 Master Tape Vault",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"&?\s*Phase 3 OLD Songs/[^\"'\n]+",
        "",
        s,
        flags=re.I,
    )
    s = re.sub(r"\.(?:OLD\)\s*)?wav(?:\.wav)?\b", "", s, flags=re.I)

    # 5. Clean out-of-universe terms ("per protocol", "in canon", "[CANON ARCHIVE LOG", raw 11-char YT IDs in brackets)
    s = re.sub(r"\(per protocol:\s*Hard Rock\s*=\s*1985\)", "(1985 Hard Rock Era)", s, flags=re.I)
    s = re.sub(r"\(per protocol:\s*Nova-chan\s*=\s*1984\)", "(1984 Tokyo Broadcast Era)", s, flags=re.I)
    s = re.sub(r"\bIn canon,\s*", "Historically, ", s)
    s = re.sub(r"\bin canon\b", "in the archive", s, flags=re.I)
    s = re.sub(r"\[CANON ARCHIVE LOG", "[SUBLEVEL B2 REEL LOG", s, flags=re.I)
    s = re.sub(r"\bCanonical\s+Phase\b", "Recovered Phase", s)
    s = re.sub(r"\bCanonical\s+Track\b", "Recovered Track", s)
    s = re.sub(r"\s*\[[A-Za-z0-9_-]{11}\]", "", s)
    s = re.sub(r"Closes Rock Opera Act I \(\) and leads into Act II \(:\s*", "Closes Rock Opera Act I and leads into Act II (", s)
    s = re.sub(r"in Rock Opera Act I \(\)\.", "in Rock Opera Act I.", s)

    # 6. Any remaining "YouTube" in song_lore_questions.py
    s = re.sub(r"\bYouTube\s+live\s+chat\b", "live broadcast relay chat", s, flags=re.I)
    s = re.sub(r"\bYouTube\s+descriptions\b", "archival master tape logs", s, flags=re.I)
    s = re.sub(r"\bYouTube\b", "WorldNet Broadcast", s, flags=re.I)

    return s


def main():
    raw = SLQ_PATH.read_text(encoding="utf-8")
    cleaned = sanitize_text(raw)
    SLQ_PATH.write_text(cleaned, encoding="utf-8")
    print(f"Sanitized {SLQ_PATH} ({len(cleaned)} chars)")

    check_re = re.compile(
        r"google\s*drive|drive\s+master|drive\s+archive|youtube|\.pdf|\.wav|documents/nova|for live stream|channel bible|official canon|deity bible|suno\s*id|filmsbyahuman|in canon|per protocol|canonical hook",
        re.I,
    )
    remaining = check_re.findall(cleaned)
    print(f"Remaining out-of-universe matches in song_lore_questions.py: {len(remaining)} -> {remaining[:10]}")


if __name__ == "__main__":
    main()
