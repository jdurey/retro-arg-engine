"""Generates 100% ORIGINAL procedural 1980s synthwave, city pop, and ambient MIDI compositions.
Zero copyright risk. Completely replaces all pop song arrangements with authentic procedural music.

Tracks generated (19 original songs):
 1. gasoline_heart.mid      - 132 BPM Driving J-Rock / City Pop Anthem (E Minor)
 2. ghost_transit.mid       - 84 BPM Atmospheric DX7 Ballad (D Minor / F Major)
 3. midnight_animal.mid     - 118 BPM Funky Slap Bass City Pop (A Dorian)
 4. brighter_than_sun.mid   - 126 BPM Sparkling 80s Idol Pop (G Major)
 5. only_we_remain.mid      - 72 BPM Dramatic Kayokyoku Strings Ballad (C Minor)
 6. synthetic_dawn.mid      - 116 BPM Dark Industrial Cyberpunk Synthwave (A Minor)
 7. memory_hatch.mid        - 104 BPM Sophisti-Pop Vibraphone & Rhodes (B Minor)
 8. behind_the_glass.mid    - 120 BPM Cold Minimalist 80s Synth Pop (F Minor)
 9. static_and_steel.mid    - 128 BPM Darkwave / Arpeggiated D Minor 80s Heavy Synth (D Minor)
10. hearts_on_fire.mid      - 130 BPM High Energy 80s Euro Synthwave Power Hook (B Minor)
11. these_wings_are_my_own  - 76 BPM Expansive 80s Nostalgia Power Ballad (F Major)
12. chrome_velocity.mid     - 140 BPM Driving Neon Highway Outrun Synthwave (E Minor)
13. hold_back_the_storm.mid - 80 BPM Lush DX7 & Analog Pad Slow Burn (G Minor)
14. before_you_disappear.mid- 68 BPM Melancholy Solo E.Piano & Cello Synth (D Minor)
15. run_with_the_fire.mid   - 134 BPM Upbeat 80s New Wave / Power Synth Pop (A Major)
16. togethers_the_way.mid   - 108 BPM Sophisti-Pop / Smooth Brass & 9th Chords (Eb Major)
17. summer_of_85.mid        - 112 BPM Sunset Nostalgia Synthwave / Palm Mute Bass (D Major)
18. shes_hardwired.mid      - 124 BPM Cybernetic 16th-Note Bass Sequence & Stabs (C Minor)
19. perfect_daydream.mid    - 96 BPM Breezy City Pop Jazz Rhodes & Lead (A Major)
"""
import os
import sys

# Ensure src is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from midi_engine import MidiFile, MidiTrack

QN = 480  # Ticks per quarter note


def add_drum_pattern(track, pattern_type, start_beat, bars=4):
    """Adds General MIDI drum patterns on Channel 9 (10)."""
    ch = 9
    for b in range(bars):
        bar_start = int((start_beat + b * 4) * QN)
        
        if pattern_type == "rock_driving":
            track.note(ch, 36, 110, bar_start + 0, QN // 2)
            track.note(ch, 36, 95, bar_start + int(2.5 * QN), QN // 2)
            track.note(ch, 36, 110, bar_start + 2 * QN, QN // 2)
            track.note(ch, 38, 115, bar_start + 1 * QN, QN // 2)
            track.note(ch, 38, 120, bar_start + 3 * QN, QN // 2)
            for h in range(8):
                track.note(ch, 42, 85 if h % 2 == 0 else 65, bar_start + int(h * 0.5 * QN), QN // 4)
            if b == 0:
                track.note(ch, 49, 115, bar_start, QN)

        elif pattern_type == "ballad_slow":
            track.note(ch, 35, 95, bar_start + 0, QN // 2)
            track.note(ch, 35, 80, bar_start + int(2.5 * QN), QN // 2)
            track.note(ch, 37, 90, bar_start + 1 * QN, QN // 2)
            track.note(ch, 37, 95, bar_start + 3 * QN, QN // 2)
            for h in range(8):
                track.note(ch, 51, 75 if h % 2 == 0 else 55, bar_start + int(h * 0.5 * QN), QN // 2)
            if b == 0:
                track.note(ch, 49, 90, bar_start, QN)

        elif pattern_type == "disco_funk":
            for k in range(4):
                track.note(ch, 36, 105, bar_start + k * QN, QN // 2)
            track.note(ch, 38, 110, bar_start + 1 * QN, QN // 2)
            track.note(ch, 38, 115, bar_start + 3 * QN, QN // 2)
            for o in range(4):
                track.note(ch, 42, 80, bar_start + o * QN, QN // 4)
                track.note(ch, 46, 95, bar_start + int((o + 0.5) * QN), QN // 4)

        elif pattern_type == "idol_pop":
            track.note(ch, 36, 110, bar_start + 0, QN // 2)
            track.note(ch, 36, 90, bar_start + int(1.5 * QN), QN // 2)
            track.note(ch, 36, 105, bar_start + 2 * QN, QN // 2)
            track.note(ch, 40, 115, bar_start + 1 * QN, QN // 2)
            track.note(ch, 40, 115, bar_start + 3 * QN, QN // 2)
            for h in range(16):
                track.note(ch, 42, 80 if h % 4 == 0 else 60, bar_start + int(h * 0.25 * QN), QN // 8)
            for t in range(8):
                track.note(ch, 54, 75, bar_start + int(t * 0.5 * QN), QN // 4)

        elif pattern_type == "synth_industrial":
            track.note(ch, 36, 120, bar_start + 0, QN // 2)
            track.note(ch, 36, 100, bar_start + int(1.5 * QN), QN // 2)
            track.note(ch, 36, 115, bar_start + 2 * QN, QN // 2)
            track.note(ch, 40, 120, bar_start + 1 * QN, QN // 2)
            track.note(ch, 40, 127, bar_start + 3 * QN, QN // 2)
            for h in range(8):
                track.note(ch, 42, 85, bar_start + int(h * 0.5 * QN), QN // 4)

        elif pattern_type == "outrun_driving":
            for k in (0, 1.5, 2, 3.5):
                track.note(ch, 36, 115, bar_start + int(k * QN), QN // 2)
            track.note(ch, 40, 125, bar_start + 1 * QN, QN // 2)
            track.note(ch, 40, 125, bar_start + 3 * QN, QN // 2)
            for s in range(16):
                track.note(ch, 42, 90 if s % 2 == 0 else 70, bar_start + int(s * 0.25 * QN), QN // 8)
            if b % 2 == 0:
                track.note(ch, 49, 110, bar_start, QN)


# Import the original 7 core songs from generate_midis
import generate_midis as gm

# -----------------------------------------------------------------------------
# 8. Behind The Glass (ビハインド・ザ・グラス) - 120 BPM F Minor Minimal Synth
# -----------------------------------------------------------------------------
def make_behind_the_glass():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(120, 0)
    t0.copyright("(c) 1986 Stardust Archive / Original Composition")
    t0.marker("Cold Synth Intro", 0)
    t0.marker("Verse", int(4 * 4 * QN))
    t0.marker("Chorus", int(12 * 4 * QN))
    mf.add_track(t0)

    # Lead (Sawtooth 81)
    t1 = MidiTrack("Nova Lead Vocal")
    t1.program_change(0, 81, 0)
    melody = [
        # Verse: Fm -> Db -> Bbm -> C
        (16.0, 1.5, 65), (17.5, 0.5, 68), (18.0, 2.0, 70), (20.0, 1.0, 68), (21.0, 1.0, 67), (22.0, 2.0, 65),
        (24.0, 1.5, 65), (25.5, 0.5, 68), (26.0, 2.0, 72), (28.0, 1.0, 70), (29.0, 1.0, 68), (30.0, 2.0, 67),
        # Pre-chorus
        (32.0, 1.0, 68), (33.0, 1.0, 70), (34.0, 1.5, 72), (35.5, 0.5, 73), (36.0, 2.0, 72), (38.0, 2.0, 70),
        (40.0, 1.0, 68), (41.0, 1.0, 67), (42.0, 2.0, 65), (44.0, 4.0, 67),
        # Chorus: "BEHIND THE GLASS"
        (48.0, 2.0, 72), (50.0, 1.0, 70), (51.0, 1.0, 68), (52.0, 2.5, 70),
        (54.5, 0.5, 72), (55.0, 1.0, 73), (56.0, 2.0, 75), (58.0, 1.0, 73), (59.0, 1.0, 72), (60.0, 4.0, 70),
        (64.0, 2.0, 68), (66.0, 1.0, 67), (67.0, 1.0, 65), (68.0, 4.0, 65),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 105, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Chords (DX7 EPiano 4)
    t2 = MidiTrack("Cold DX7 Chords")
    t2.program_change(1, 4, 0)
    chords = [([53, 60, 65, 68], 4), ([49, 56, 61, 65], 4), ([46, 53, 58, 61], 4), ([48, 55, 60, 64], 4)] * 5
    curr = 0.0
    for notes, dur in chords:
        for st in (0.0, 1.5, 2.5):
            t2.chord(1, notes, 85, int((curr + st) * QN), int(0.9 * QN))
        curr += dur
    mf.add_track(t2)

    # 16th Bass (39)
    t3 = MidiTrack("Sequencer Synth Bass")
    t3.program_change(2, 39, 0)
    roots = [41, 37, 34, 36] * 5  # F, Db, Bb, C
    for idx, r in enumerate(roots):
        b_pos = idx * 4
        for s in range(16):
            p = r if s % 4 != 2 else r + 12
            t3.note(2, p, 90 if s % 4 == 0 else 70, int((b_pos + s * 0.25) * QN), int(0.2 * QN))
    mf.add_track(t3)

    # Drums
    t4 = MidiTrack("LinnDrum")
    for b in range(0, 20, 4):
        add_drum_pattern(t4, "synth_industrial", b, bars=4)
    mf.add_track(t4)
    return mf


# -----------------------------------------------------------------------------
# 9. Static & Steel (スタティック・アンド・スチール) - 128 BPM D Minor Heavy Synth
# -----------------------------------------------------------------------------
def make_static_and_steel():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(128, 0)
    t0.copyright("(c) 1985 Kamome Records / Original Composition")
    t0.marker("Arp Intro", 0)
    t0.marker("Heavy Verse", int(4 * 4 * QN))
    t0.marker("Power Chorus", int(12 * 4 * QN))
    mf.add_track(t0)

    # Lead (Square Wave 80)
    t1 = MidiTrack("Nova Lead Vocal")
    t1.program_change(0, 80, 0)
    melody = [
        # Verse (Dm -> Bb -> C -> Am)
        (16.0, 1.5, 62), (17.5, 0.5, 65), (18.0, 2.0, 69), (20.0, 1.0, 67), (21.0, 1.0, 65), (22.0, 2.0, 64),
        (24.0, 1.5, 62), (25.5, 0.5, 65), (26.0, 2.0, 69), (28.0, 1.0, 70), (29.0, 1.0, 72), (30.0, 2.0, 69),
        # Chorus
        (48.0, 2.0, 74), (50.0, 1.0, 72), (51.0, 1.0, 70), (52.0, 2.0, 69), (54.0, 1.0, 67), (55.0, 1.0, 65),
        (56.0, 2.5, 67), (58.5, 0.5, 69), (59.0, 1.5, 70), (61.0, 1.0, 69), (62.0, 2.0, 67), (64.0, 4.0, 62),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 110, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Heavy Synth Arpeggiator (Ch 1, 81)
    t2 = MidiTrack("Steel Arpeggiator")
    t2.program_change(1, 81, 0)
    chords = [([50, 57, 62, 65], 4), ([46, 53, 58, 62], 4), ([48, 55, 60, 64], 4), ([45, 52, 57, 60], 4)] * 5
    curr = 0.0
    for notes, dur in chords:
        for s in range(16):
            note = notes[s % len(notes)]
            t2.note(1, note + (12 if (s // 4) % 2 == 1 else 0), 85, int((curr + s * 0.25) * QN), int(0.2 * QN))
        curr += dur
    mf.add_track(t2)

    # Moog Bass (38)
    t3 = MidiTrack("Moog Bass")
    t3.program_change(2, 38, 0)
    roots = [38, 34, 36, 33] * 5
    for idx, r in enumerate(roots):
        b = idx * 4
        for step in (0, 1.5, 2, 3, 3.5):
            t3.note(2, r, 105, int((b + step) * QN), int(0.4 * QN))
    mf.add_track(t3)

    # Driving Drums
    t4 = MidiTrack("Drums")
    for b in range(0, 20, 4):
        add_drum_pattern(t4, "rock_driving", b, bars=4)
    mf.add_track(t4)
    return mf


# -----------------------------------------------------------------------------
# 10. Hearts on Fire (ハーツ・オン・ファイア) - 130 BPM Eurobeat / High Energy
# -----------------------------------------------------------------------------
def make_hearts_on_fire():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(130, 0)
    t0.copyright("(c) 1987 Stardust / Original Euro-Synth")
    t0.marker("High Energy Intro", 0)
    t0.marker("Verse", int(4 * 4 * QN))
    t0.marker("Chorus", int(12 * 4 * QN))
    mf.add_track(t0)

    # Vocal Lead (81)
    t1 = MidiTrack("Nova Lead Vocal")
    t1.program_change(0, 81, 0)
    melody = [
        # B Minor -> G -> A -> F#m
        (16.0, 1.0, 71), (17.0, 0.5, 74), (17.5, 1.5, 76), (19.0, 1.0, 74), (20.0, 2.0, 71),
        (24.0, 1.0, 71), (25.0, 0.5, 74), (25.5, 1.5, 78), (27.0, 1.0, 76), (28.0, 2.0, 74),
        # Chorus: "HEARTS ON FIRE"
        (48.0, 1.5, 78), (49.5, 0.5, 81), (50.0, 2.0, 83), (52.0, 1.0, 81), (53.0, 1.0, 78), (54.0, 2.0, 76),
        (56.0, 1.5, 78), (57.5, 0.5, 81), (58.0, 2.0, 83), (60.0, 1.0, 85), (61.0, 1.0, 83), (62.0, 2.5, 78),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 115, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Synth Brass (62)
    t2 = MidiTrack("Synth Brass Stabs")
    t2.program_change(1, 62, 0)
    chords = [([47, 54, 59, 62], 4), ([43, 50, 55, 59], 4), ([45, 52, 57, 60], 4), ([42, 49, 54, 57], 4)] * 5
    curr = 0.0
    for notes, dur in chords:
        for st in (0.0, 1.5, 2.5, 3.5):
            t2.chord(1, [n + 12 for n in notes[:3]], 95, int((curr + st) * QN), int(0.4 * QN))
        curr += dur
    mf.add_track(t2)

    # Slap Bass (36)
    t3 = MidiTrack("High Energy Slap Bass")
    t3.program_change(2, 36, 0)
    roots = [35, 31, 33, 30] * 5
    for idx, r in enumerate(roots):
        b = idx * 4
        for s in (0, 0.75, 1.5, 2, 2.75, 3.5):
            t3.note(2, r if s < 2 else r + 12, 105, int((b + s) * QN), int(0.3 * QN))
    mf.add_track(t3)

    # Four on the floor drums
    t4 = MidiTrack("LinnDrum")
    for b in range(0, 20, 4):
        add_drum_pattern(t4, "disco_funk", b, bars=4)
    mf.add_track(t4)
    return mf


# -----------------------------------------------------------------------------
# 11. These Wings Are My Own - 76 BPM F Major Power Ballad
# -----------------------------------------------------------------------------
def make_these_wings_are_my_own():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(76, 0)
    t0.copyright("(c) 1985 Ashford Poly / Original Power Ballad")
    t0.marker("Piano Intro", 0)
    t0.marker("Ballad Verse", int(4 * 4 * QN))
    t0.marker("Soaring Chorus", int(12 * 4 * QN))
    mf.add_track(t0)

    # Lead (Vocal Flute/Lead 73)
    t1 = MidiTrack("Nova Lead Vocal")
    t1.program_change(0, 73, 0)
    melody = [
        # Verse (F -> Bb -> Dm -> C)
        (16.0, 1.5, 65), (17.5, 0.5, 69), (18.0, 2.0, 72), (20.0, 1.0, 70), (21.0, 1.0, 69), (22.0, 2.0, 67),
        (24.0, 1.5, 65), (25.5, 0.5, 69), (26.0, 2.0, 74), (28.0, 1.0, 72), (29.0, 1.0, 70), (30.0, 2.0, 69),
        # Chorus: "THESE WINGS ARE MY OWN"
        (48.0, 2.0, 77), (50.0, 1.0, 76), (51.0, 1.0, 74), (52.0, 2.0, 72), (54.0, 1.0, 70), (55.0, 1.0, 69),
        (56.0, 3.0, 70), (59.0, 1.0, 72), (60.0, 2.0, 74), (62.0, 2.0, 72), (64.0, 4.0, 65),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 100, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Acoustic Grand Piano (0)
    t2 = MidiTrack("Grand Piano")
    t2.program_change(1, 0, 0)
    chords = [([53, 57, 60, 65], 4), ([50, 53, 58, 62], 4), ([50, 57, 62, 65], 4), ([48, 55, 60, 64], 4)] * 5
    curr = 0.0
    for notes, dur in chords:
        for arp, p in enumerate(notes):
            t2.note(1, p, 85, int((curr + arp * 0.5) * QN), int(3.5 * QN))
        curr += dur
    mf.add_track(t2)

    # Strings Pad (48)
    t3 = MidiTrack("Synth Strings Pad")
    t3.program_change(2, 48, 0)
    curr = 0.0
    for notes, dur in chords:
        t3.chord(2, [n + 12 for n in notes[:3]], 70, int(curr * QN), int(dur * QN))
        curr += dur
    mf.add_track(t3)

    # Slow Ballad Drums
    t4 = MidiTrack("Ballad Drums")
    for b in range(0, 20, 4):
        add_drum_pattern(t4, "ballad_slow", b, bars=4)
    mf.add_track(t4)
    return mf


# -----------------------------------------------------------------------------
# 12. Chrome Velocity (クローム・ヴェロシティ) - 140 BPM Driving Outrun Synthwave
# -----------------------------------------------------------------------------
def make_chrome_velocity():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(140, 0)
    t0.copyright("(c) 1986 Stardust Motor Club / Original Synthwave")
    t0.marker("High Speed Intro", 0)
    t0.marker("Fast Verse", int(4 * 4 * QN))
    t0.marker("Anthem Chorus", int(12 * 4 * QN))
    mf.add_track(t0)

    # Saw Lead (81)
    t1 = MidiTrack("Nova Lead Vocal")
    t1.program_change(0, 81, 0)
    melody = [
        # Em -> C -> D -> Bm
        (16.0, 1.0, 64), (17.0, 0.5, 67), (17.5, 1.5, 71), (19.0, 1.0, 69), (20.0, 2.0, 67),
        (24.0, 1.0, 64), (25.0, 0.5, 67), (25.5, 1.5, 74), (27.0, 1.0, 72), (28.0, 2.0, 71),
        # Chorus
        (48.0, 1.5, 76), (49.5, 0.5, 79), (50.0, 2.0, 81), (52.0, 1.0, 79), (53.0, 1.0, 76), (54.0, 2.0, 74),
        (56.0, 1.5, 76), (57.5, 0.5, 79), (58.0, 2.0, 83), (60.0, 1.0, 81), (61.0, 1.0, 79), (62.0, 2.5, 76),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 115, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Fast 16th Arp (Ch 1, 80)
    t2 = MidiTrack("Speed Arpeggio")
    t2.program_change(1, 80, 0)
    roots = [40, 36, 38, 35] * 5
    curr = 0.0
    for r in roots:
        for s in range(16):
            offset = [0, 7, 12, 15, 12, 7, 19, 12][s % 8]
            t2.note(1, r + 24 + offset, 85, int((curr + s * 0.25) * QN), int(0.2 * QN))
        curr += 4.0
    mf.add_track(t2)

    # Sequencer Bass (38)
    t3 = MidiTrack("Synth Bass")
    t3.program_change(2, 38, 0)
    curr = 0.0
    for r in roots:
        for s in range(16):
            t3.note(2, r, 95 if s % 4 == 0 else 75, int((curr + s * 0.25) * QN), int(0.2 * QN))
        curr += 4.0
    mf.add_track(t3)

    # Driving Drums
    t4 = MidiTrack("Outrun Drums")
    for b in range(0, 20, 4):
        add_drum_pattern(t4, "outrun_driving", b, bars=4)
    mf.add_track(t4)
    return mf


# -----------------------------------------------------------------------------
# 13. Hold Back The Storm - 80 BPM G Minor Ambient Slow Burn
# -----------------------------------------------------------------------------
def make_hold_back_the_storm():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(80, 0)
    t0.copyright("(c) 1985 Kamome Records / Original Ambient DX7")
    t0.marker("Rain Intro", 0)
    t0.marker("Slow Verse", int(4 * 4 * QN))
    t0.marker("Lush Chorus", int(12 * 4 * QN))
    mf.add_track(t0)

    # Flute / Whistle Lead (73)
    t1 = MidiTrack("Nova Lead Vocal")
    t1.program_change(0, 73, 0)
    melody = [
        # Gm -> Eb -> F -> Dm
        (16.0, 1.5, 67), (17.5, 0.5, 70), (18.0, 2.0, 72), (20.0, 1.0, 70), (21.0, 1.0, 69), (22.0, 2.0, 67),
        (24.0, 1.5, 67), (25.5, 0.5, 70), (26.0, 2.0, 74), (28.0, 1.0, 72), (29.0, 1.0, 70), (30.0, 2.0, 69),
        # Chorus
        (48.0, 2.0, 74), (50.0, 1.0, 72), (51.0, 1.0, 70), (52.0, 2.5, 69),
        (54.5, 0.5, 70), (55.0, 1.0, 72), (56.0, 2.0, 74), (58.0, 2.0, 72), (60.0, 4.0, 67),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 100, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # DX7 Warm E.Piano (4)
    t2 = MidiTrack("DX7 Rhodes")
    t2.program_change(1, 4, 0)
    chords = [([43, 50, 55, 58], 4), ([39, 46, 51, 55], 4), ([41, 48, 53, 57], 4), ([38, 45, 50, 53], 4)] * 5
    curr = 0.0
    for notes, dur in chords:
        for st in (0.0, 1.5, 2.5):
            t2.chord(1, notes, 80, int((curr + st) * QN), int(1.2 * QN))
        curr += dur
    mf.add_track(t2)

    # Warm Pad (89)
    t3 = MidiTrack("Warm Analog Pad")
    t3.program_change(2, 89, 0)
    curr = 0.0
    for notes, dur in chords:
        t3.chord(2, [n + 12 for n in notes[:3]], 65, int(curr * QN), int(dur * QN))
        curr += dur
    mf.add_track(t3)

    # Slow Drums
    t4 = MidiTrack("Drums")
    for b in range(0, 20, 4):
        add_drum_pattern(t4, "ballad_slow", b, bars=4)
    mf.add_track(t4)
    return mf


# -----------------------------------------------------------------------------
# 14. Before You Disappear - 68 BPM D Minor Solo E.Piano & Ambient Cello
# -----------------------------------------------------------------------------
def make_before_you_disappear():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(68, 0)
    t0.copyright("(c) 1985 Ashford Poly / Original Ambient Elegy")
    t0.marker("Solitude Intro", 0)
    t0.marker("Melancholy Verse", int(4 * 4 * QN))
    t0.marker("Fade Out", int(12 * 4 * QN))
    mf.add_track(t0)

    # Cello Synth Lead (42)
    t1 = MidiTrack("Nova Cello Synth")
    t1.program_change(0, 42, 0)
    melody = [
        # Dm -> Bbmaj7 -> Gm9 -> Asis4 -> A
        (16.0, 2.0, 62), (18.0, 1.0, 65), (19.0, 1.0, 67), (20.0, 3.0, 69), (23.0, 1.0, 65),
        (24.0, 2.0, 64), (26.0, 1.0, 62), (27.0, 1.0, 60), (28.0, 4.0, 57),
        (32.0, 2.0, 62), (34.0, 1.0, 65), (35.0, 1.0, 69), (36.0, 2.0, 72), (38.0, 2.0, 69),
        (40.0, 4.0, 67), (44.0, 4.0, 62),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 95, int(beat * QN), int(dur * QN * 0.98))
    mf.add_track(t1)

    # Delicate E.Piano (5)
    t2 = MidiTrack("E.Piano")
    t2.program_change(1, 5, 0)
    chords = [([50, 57, 62, 65], 4), ([46, 53, 57, 62], 4), ([43, 50, 55, 58], 4), ([45, 52, 57, 61], 4)] * 4
    curr = 0.0
    for notes, dur in chords:
        for arp, p in enumerate(notes):
            t2.note(1, p, 75, int((curr + arp * 0.75) * QN), int(3.0 * QN))
        curr += dur
    mf.add_track(t2)

    # Synth Strings (48)
    t3 = MidiTrack("Strings")
    t3.program_change(2, 48, 0)
    curr = 0.0
    for notes, dur in chords:
        t3.chord(2, [notes[0], notes[2]], 60, int(curr * QN), int(dur * QN))
        curr += dur
    mf.add_track(t3)
    return mf


# -----------------------------------------------------------------------------
# 15. Run With The Fire - 134 BPM A Major 80s Power New Wave
# -----------------------------------------------------------------------------
def make_run_with_the_fire():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(134, 0)
    t0.copyright("(c) 1986 Stardust Webring / Original New Wave")
    t0.marker("Intro", 0)
    t0.marker("Verse", int(4 * 4 * QN))
    t0.marker("Chorus", int(12 * 4 * QN))
    mf.add_track(t0)

    # Lead (Sawtooth 81)
    t1 = MidiTrack("Nova Lead Vocal")
    t1.program_change(0, 81, 0)
    melody = [
        # A -> F#m -> D -> E
        (16.0, 1.0, 69), (17.0, 0.5, 71), (17.5, 1.5, 73), (19.0, 1.0, 71), (20.0, 2.0, 69),
        (24.0, 1.0, 69), (25.0, 0.5, 73), (25.5, 1.5, 76), (27.0, 1.0, 74), (28.0, 2.0, 73),
        # Chorus: "RUN WITH THE FIRE"
        (48.0, 1.5, 76), (49.5, 0.5, 78), (50.0, 2.0, 81), (52.0, 1.0, 78), (53.0, 1.0, 76), (54.0, 2.0, 73),
        (56.0, 1.5, 76), (57.5, 0.5, 78), (58.0, 2.0, 81), (60.0, 1.0, 83), (61.0, 1.0, 81), (62.0, 2.5, 76),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 115, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Juno Synth Brass (62)
    t2 = MidiTrack("Juno Synth Brass")
    t2.program_change(1, 62, 0)
    chords = [([45, 52, 57, 61], 4), ([42, 49, 54, 57], 4), ([50, 54, 57, 62], 4), ([40, 47, 52, 56], 4)] * 5
    curr = 0.0
    for notes, dur in chords:
        for st in (0.0, 1.5, 2.5, 3.5):
            t2.chord(1, [n + 12 for n in notes[:3]], 95, int((curr + st) * QN), int(0.4 * QN))
        curr += dur
    mf.add_track(t2)

    # Driving Bass (36)
    t3 = MidiTrack("Slap Bass")
    t3.program_change(2, 36, 0)
    roots = [33, 30, 38, 28] * 5
    for idx, r in enumerate(roots):
        b = idx * 4
        for s in (0, 0.5, 1.5, 2, 2.5, 3.5):
            t3.note(2, r if s < 2 else r + 12, 105, int((b + s) * QN), int(0.4 * QN))
    mf.add_track(t3)

    # Driving Drums
    t4 = MidiTrack("LinnDrum")
    for b in range(0, 20, 4):
        add_drum_pattern(t4, "rock_driving", b, bars=4)
    mf.add_track(t4)
    return mf


# -----------------------------------------------------------------------------
# 16. Together's The Way - 108 BPM Eb Major Sophisti-Pop
# -----------------------------------------------------------------------------
def make_togethers_the_way():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(108, 0)
    t0.copyright("(c) 1985 Kamome Records / Original Sophisti-Pop")
    t0.marker("Rhodes Intro", 0)
    t0.marker("Verse", int(4 * 4 * QN))
    t0.marker("Smooth Chorus", int(12 * 4 * QN))
    mf.add_track(t0)

    # Lead (Vibraphone/Lead 11)
    t1 = MidiTrack("Nova Lead Vocal")
    t1.program_change(0, 11, 0)
    melody = [
        # Ebmaj7 -> Cm7 -> Fm7 -> Bb7
        (16.0, 1.5, 63), (17.5, 0.5, 67), (18.0, 1.5, 70), (19.5, 0.5, 72), (20.0, 2.0, 70),
        (24.0, 1.5, 63), (25.5, 0.5, 67), (26.0, 1.5, 74), (27.5, 0.5, 72), (28.0, 2.0, 70),
        # Chorus
        (48.0, 2.0, 75), (50.0, 1.0, 74), (51.0, 1.0, 72), (52.0, 2.0, 70), (54.0, 1.0, 68), (55.0, 1.0, 67),
        (56.0, 2.5, 68), (58.5, 0.5, 70), (59.0, 1.5, 72), (61.0, 1.0, 70), (62.0, 2.0, 67), (64.0, 4.0, 63),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 100, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Rhodes (4)
    t2 = MidiTrack("Fender Rhodes")
    t2.program_change(1, 4, 0)
    chords = [([51, 58, 62, 65], 4), ([48, 55, 60, 63], 4), ([41, 48, 53, 56], 4), ([46, 53, 58, 62], 4)] * 5
    curr = 0.0
    for notes, dur in chords:
        for st in (0.0, 1.5, 2.5):
            t2.chord(1, notes, 80, int((curr + st) * QN), int(1.0 * QN))
        curr += dur
    mf.add_track(t2)

    # Finger Bass (33)
    t3 = MidiTrack("Finger Bass")
    t3.program_change(2, 33, 0)
    roots = [39, 36, 29, 34] * 5
    for idx, r in enumerate(roots):
        b = idx * 4
        t3.note(2, r, 95, int((b + 0.0) * QN), int(1.2 * QN))
        t3.note(2, r + 7, 85, int((b + 1.5) * QN), int(0.8 * QN))
        t3.note(2, r, 90, int((b + 2.5) * QN), int(1.0 * QN))
        t3.note(2, r + 12, 95, int((b + 3.5) * QN), int(0.5 * QN))
    mf.add_track(t3)

    # City Pop Drums
    t4 = MidiTrack("Drums")
    for b in range(0, 20, 4):
        add_drum_pattern(t4, "disco_funk", b, bars=4)
    mf.add_track(t4)
    return mf


# -----------------------------------------------------------------------------
# 17. Summer of '85 - 112 BPM D Major Nostalgia Sunset Synthwave
# -----------------------------------------------------------------------------
def make_summer_of_85():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(112, 0)
    t0.copyright("(c) 1985 Orion Records / Original Synthwave")
    t0.marker("Sunset Arp", 0)
    t0.marker("Nostalgic Verse", int(4 * 4 * QN))
    t0.marker("Chorus", int(12 * 4 * QN))
    mf.add_track(t0)

    # Vocal Lead (81)
    t1 = MidiTrack("Nova Lead Vocal")
    t1.program_change(0, 81, 0)
    melody = [
        # D -> Bm -> G -> A
        (16.0, 1.5, 62), (17.5, 0.5, 66), (18.0, 2.0, 69), (20.0, 1.0, 67), (21.0, 1.0, 66), (22.0, 2.0, 64),
        (24.0, 1.5, 62), (25.5, 0.5, 66), (26.0, 2.0, 71), (28.0, 1.0, 69), (29.0, 1.0, 67), (30.0, 2.0, 66),
        # Chorus: "SUMMER OF EIGHTY-FIVE"
        (48.0, 1.5, 74), (49.5, 0.5, 76), (50.0, 2.0, 78), (52.0, 1.0, 76), (53.0, 1.0, 74), (54.0, 2.0, 71),
        (56.0, 1.5, 74), (57.5, 0.5, 76), (58.0, 2.0, 78), (60.0, 1.0, 81), (61.0, 1.0, 78), (62.0, 2.5, 74),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 105, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Palm Mute Synth Guitar / Key (28)
    t2 = MidiTrack("Palm Mute Arp")
    t2.program_change(1, 28, 0)
    roots = [38, 35, 31, 33] * 5
    curr = 0.0
    for r in roots:
        for s in range(16):
            t2.note(1, r + 24 + (7 if s % 2 == 1 else 0), 75, int((curr + s * 0.25) * QN), int(0.2 * QN))
        curr += 4.0
    mf.add_track(t2)

    # Warm Pad (89)
    t3 = MidiTrack("Warm Pad")
    t3.program_change(2, 89, 0)
    chords = [([50, 57, 62, 66], 4), ([47, 54, 59, 62], 4), ([43, 50, 55, 59], 4), ([45, 52, 57, 61], 4)] * 5
    curr = 0.0
    for notes, dur in chords:
        t3.chord(2, notes, 70, int(curr * QN), int(dur * QN))
        curr += dur
    mf.add_track(t3)

    # Drums
    t4 = MidiTrack("LinnDrum")
    for b in range(0, 20, 4):
        add_drum_pattern(t4, "synth_industrial", b, bars=4)
    mf.add_track(t4)
    return mf


# -----------------------------------------------------------------------------
# 18. She's Hardwired - 124 BPM C Minor Cybernetic Sequencer
# -----------------------------------------------------------------------------
def make_shes_hardwired():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(124, 0)
    t0.copyright("(c) 1986 Stardust Unit-7 / Original Composition")
    t0.marker("Machine Pulse", 0)
    t0.marker("Cybernetic Verse", int(4 * 4 * QN))
    t0.marker("Core Chorus", int(12 * 4 * QN))
    mf.add_track(t0)

    # Vocoder / Saw Lead (80)
    t1 = MidiTrack("Nova Lead Vocal")
    t1.program_change(0, 80, 0)
    melody = [
        # Cm -> Ab -> Fm -> G
        (16.0, 1.0, 60), (17.0, 0.5, 63), (17.5, 1.5, 65), (19.0, 1.0, 63), (20.0, 2.0, 60),
        (24.0, 1.0, 60), (25.0, 0.5, 63), (25.5, 1.5, 67), (27.0, 1.0, 65), (28.0, 2.0, 63),
        # Chorus: "SHE'S HARDWIRED"
        (48.0, 1.5, 67), (49.5, 0.5, 70), (50.0, 2.0, 72), (52.0, 1.0, 70), (53.0, 1.0, 67), (54.0, 2.0, 65),
        (56.0, 1.5, 67), (57.5, 0.5, 70), (58.0, 2.0, 72), (60.0, 1.0, 74), (61.0, 1.0, 72), (62.0, 2.5, 67),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 110, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Cybernetic Stabs (62)
    t2 = MidiTrack("Synth Stabs")
    t2.program_change(1, 62, 0)
    chords = [([48, 55, 60, 63], 4), ([44, 51, 56, 60], 4), ([41, 48, 53, 56], 4), ([43, 50, 55, 59], 4)] * 5
    curr = 0.0
    for notes, dur in chords:
        for st in (0.0, 1.5, 2.5, 3.5):
            t2.chord(1, notes, 90, int((curr + st) * QN), int(0.4 * QN))
        curr += dur
    mf.add_track(t2)

    # 16th Sequencer Bass (38)
    t3 = MidiTrack("Sequencer Bass")
    t3.program_change(2, 38, 0)
    roots = [36, 32, 29, 31] * 5
    curr = 0.0
    for r in roots:
        for s in range(16):
            p = r if s % 4 != 2 else r + 12
            t3.note(2, p, 95 if s % 4 == 0 else 75, int((curr + s * 0.25) * QN), int(0.2 * QN))
        curr += 4.0
    mf.add_track(t3)

    # Industrial Drums
    t4 = MidiTrack("LinnDrum")
    for b in range(0, 20, 4):
        add_drum_pattern(t4, "synth_industrial", b, bars=4)
    mf.add_track(t4)
    return mf


# -----------------------------------------------------------------------------
# 19. Perfect Daydream - 96 BPM A Major Breezy City Pop Jazz
# -----------------------------------------------------------------------------
def make_perfect_daydream():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(96, 0)
    t0.copyright("(c) 1985 Kamome Records / Original City Pop")
    t0.marker("Breezy Intro", 0)
    t0.marker("Jazz Verse", int(4 * 4 * QN))
    t0.marker("Daydream Chorus", int(12 * 4 * QN))
    mf.add_track(t0)

    # Acoustic / Jazz Lead (24)
    t1 = MidiTrack("Nova Lead Guitar/Vocal")
    t1.program_change(0, 24, 0)
    melody = [
        # Amaj7 -> F#m7 -> Bm7 -> E7
        (16.0, 1.5, 69), (17.5, 0.5, 73), (18.0, 1.5, 76), (19.5, 0.5, 78), (20.0, 2.0, 76),
        (24.0, 1.5, 69), (25.5, 0.5, 73), (26.0, 1.5, 80), (27.5, 0.5, 78), (28.0, 2.0, 76),
        # Chorus: "PERFECT DAYDREAM"
        (48.0, 2.0, 81), (50.0, 1.0, 80), (51.0, 1.0, 78), (52.0, 2.0, 76), (54.0, 1.0, 74), (55.0, 1.0, 73),
        (56.0, 2.5, 74), (58.5, 0.5, 76), (59.0, 1.5, 78), (61.0, 1.0, 76), (62.0, 2.0, 73), (64.0, 4.0, 69),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 100, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Fender Rhodes (4)
    t2 = MidiTrack("Rhodes Chords")
    t2.program_change(1, 4, 0)
    chords = [([45, 52, 56, 61], 4), ([42, 49, 54, 57], 4), ([47, 54, 57, 62], 4), ([40, 47, 52, 56], 4)] * 5
    curr = 0.0
    for notes, dur in chords:
        for st in (0.0, 1.5, 2.5):
            t2.chord(1, notes, 80, int((curr + st) * QN), int(1.1 * QN))
        curr += dur
    mf.add_track(t2)

    # Warm Slap Bass (36)
    t3 = MidiTrack("City Pop Bass")
    t3.program_change(2, 36, 0)
    roots = [33, 30, 35, 28] * 5
    for idx, r in enumerate(roots):
        b = idx * 4
        t3.note(2, r, 95, int((b + 0.0) * QN), int(1.0 * QN))
        t3.note(2, r + 7, 85, int((b + 1.5) * QN), int(0.7 * QN))
        t3.note(2, r, 90, int((b + 2.5) * QN), int(0.9 * QN))
        t3.note(2, r + 12, 100, int((b + 3.5) * QN), int(0.5 * QN))
    mf.add_track(t3)

    # Funky Drums
    t4 = MidiTrack("Drums")
    for b in range(0, 20, 4):
        add_drum_pattern(t4, "disco_funk", b, bars=4)
    mf.add_track(t4)
    return mf


# -----------------------------------------------------------------------------
# ALL 19 ORIGINAL COMPOSITIONS
# -----------------------------------------------------------------------------
ALL_SONGS = [
    ("gasoline_heart", "Gasoline Heart (ガソリン・ハート)", gm.make_gasoline_heart),
    ("ghost_transit", "Ghost Transit (ゴースト・トランジット)", gm.make_ghost_transit),
    ("midnight_animal", "Midnight Animal (ミッドナイト・アニマル)", gm.make_midnight_animal),
    ("brighter_than_sun", "Brighter Than The Sun (太陽よりも、輝いて！)", gm.make_brighter_than_sun),
    ("only_we_remain", "Only We Remain (残されたのは、私たちだけ)", gm.make_only_we_remain),
    ("synthetic_dawn", "Synthetic Dawn (Akasaka Mix)", gm.make_synthetic_dawn),
    ("memory_hatch", "Memory Hatch (Sophisti-Pop)", gm.make_memory_hatch),
    ("behind_the_glass", "Behind The Glass (ビハインド・ザ・グラス)", make_behind_the_glass),
    ("static_and_steel", "Static & Steel (スタティック・アンド・スチール)", make_static_and_steel),
    ("hearts_on_fire", "Hearts on Fire (ハーツ・オン・ファイア)", make_hearts_on_fire),
    ("these_wings_are_my_own", "These Wings Are My Own (私の翼)", make_these_wings_are_my_own),
    ("chrome_velocity", "Chrome Velocity (クローム・ヴェロシティ)", make_chrome_velocity),
    ("hold_back_the_storm", "Hold Back The Storm (嵐を止めて)", make_hold_back_the_storm),
    ("before_you_disappear", "Before You Disappear (消え去る前に)", make_before_you_disappear),
    ("run_with_the_fire", "Run With The Fire (炎と走れ)", make_run_with_the_fire),
    ("togethers_the_way", "Together's The Way (二人の道)", make_togethers_the_way),
    ("summer_of_85", "Summer of '85 (1985年の夏)", make_summer_of_85),
    ("shes_hardwired", "She's Hardwired (ハードワイヤード)", make_shes_hardwired),
    ("perfect_daydream", "Perfect Daydream (デイドリーム)", make_perfect_daydream),
]


def render_all_tracks():
    import render_midi_audio as rma
    
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    midi_target_dir = os.path.join(root_dir, "site", "ftp", "kamome", "midi")
    os.makedirs(midi_target_dir, exist_ok=True)
    
    print(f"\n=======================================================")
    print(f" GENERATING 19 FULLY ORIGINAL PROCEDURAL 80s TRACKS")
    print(f" ZERO COPYRIGHT / 100% PROCEDURAL SYNTHWAVE & CITY POP")
    print(f"=======================================================\n")
    
    for slug, title, make_fn in ALL_SONGS:
        midi_path = os.path.join(midi_target_dir, f"{slug}.mid")
        mp3_path = os.path.join(midi_target_dir, f"{slug}_14k.mp3")
        
        # 1. Generate MIDI
        mf = make_fn()
        mf.write(midi_path)
        sz_mid = os.path.getsize(midi_path)
        
        # 2. Render authentic 14.4k dialup MP3
        rma.render_midi_to_audio(mf, mp3_path)
        sz_mp3 = os.path.getsize(mp3_path)
        print(f" [OK] {slug:<22} -> mid: {sz_mid}B | mp3: {sz_mp3/1024:.1f}KB ({title})")
        
    print(f"\nSuccessfully generated and rendered all 19 original compositions!")


if __name__ == "__main__":
    render_all_tracks()
