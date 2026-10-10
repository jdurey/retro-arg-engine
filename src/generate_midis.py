"""Generates authentic 1990s multi-track Standard MIDI (.mid) files for Nova Hart songs.

Creates:
  assets/midi/gasoline_heart.mid    (132 BPM - J-Rock / City Pop Anthem)
  assets/midi/ghost_transit.mid     (84 BPM - Atmospheric DX7 Ballad)
  assets/midi/midnight_animal.mid   (118 BPM - Funky Slap Bass City Pop)
  assets/midi/brighter_than_sun.mid (126 BPM - Sparkling 80s Idol Pop)
  assets/midi/only_we_remain.mid    (72 BPM - Dramatic Kayokyoku Strings Ballad)
  assets/midi/synthetic_dawn.mid    (116 BPM - Dark Industrial Synthwave)
  assets/midi/memory_hatch.mid      (104 BPM - Sophisti-Pop Vibraphone & Rhodes)
"""
import os
from midi_engine import MidiFile, MidiTrack

QN = 480  # Ticks per quarter note (standard division)


def add_drum_pattern(track, pattern_type, start_beat, bars=4):
    """Adds authentic General MIDI drum patterns on Channel 9 (10)."""
    ch = 9
    for b in range(bars):
        bar_start = int((start_beat + b * 4) * QN)
        
        if pattern_type == "rock_driving":  # Gasoline Heart
            # Kick on 1, 3, and 3-and
            track.note(ch, 36, 110, bar_start + 0, QN // 2)
            track.note(ch, 36, 95, bar_start + int(2.5 * QN), QN // 2)
            track.note(ch, 36, 110, bar_start + 2 * QN, QN // 2)
            # Snare on 2 and 4
            track.note(ch, 38, 115, bar_start + 1 * QN, QN // 2)
            track.note(ch, 38, 120, bar_start + 3 * QN, QN // 2)
            # Closed Hat 8th notes
            for h in range(8):
                track.note(ch, 42, 85 if h % 2 == 0 else 65, bar_start + int(h * 0.5 * QN), QN // 4)
            # Crash on bar 0 downbeat
            if b == 0:
                track.note(ch, 49, 115, bar_start, QN)

        elif pattern_type == "ballad_slow":  # Ghost Transit / Only We Remain
            # Kick on 1 and 3-and
            track.note(ch, 35, 95, bar_start + 0, QN // 2)
            track.note(ch, 35, 80, bar_start + int(2.5 * QN), QN // 2)
            # Side stick / soft snare on 2 and 4
            track.note(ch, 37, 90, bar_start + 1 * QN, QN // 2)
            track.note(ch, 37, 95, bar_start + 3 * QN, QN // 2)
            # Ride cymbal 8th notes
            for h in range(8):
                track.note(ch, 51, 75 if h % 2 == 0 else 55, bar_start + int(h * 0.5 * QN), QN // 2)
            if b == 0:
                track.note(ch, 49, 90, bar_start, QN)

        elif pattern_type == "disco_funk":  # Midnight Animal
            # Four on the floor kick
            for k in range(4):
                track.note(ch, 36, 105, bar_start + k * QN, QN // 2)
            # Snare on 2 and 4
            track.note(ch, 38, 110, bar_start + 1 * QN, QN // 2)
            track.note(ch, 38, 115, bar_start + 3 * QN, QN // 2)
            # Open hat on off-beats
            for o in range(4):
                track.note(ch, 42, 80, bar_start + o * QN, QN // 4)
                track.note(ch, 46, 95, bar_start + int((o + 0.5) * QN), QN // 4)

        elif pattern_type == "idol_pop":  # Brighter Than The Sun
            # Pop dance kick on 1, 2-and, 3
            track.note(ch, 36, 110, bar_start + 0, QN // 2)
            track.note(ch, 36, 90, bar_start + int(1.5 * QN), QN // 2)
            track.note(ch, 36, 105, bar_start + 2 * QN, QN // 2)
            # Snare on 2 and 4
            track.note(ch, 40, 115, bar_start + 1 * QN, QN // 2)
            track.note(ch, 40, 115, bar_start + 3 * QN, QN // 2)
            # 16th note closed hats
            for h in range(16):
                track.note(ch, 42, 80 if h % 4 == 0 else 60, bar_start + int(h * 0.25 * QN), QN // 8)
            # Tambourine on 8ths
            for t in range(8):
                track.note(ch, 54, 75, bar_start + int(t * 0.5 * QN), QN // 4)

        elif pattern_type == "synth_industrial":  # Synthetic Dawn
            # Heavy electronic kick on 1, 2-and, 3
            track.note(ch, 36, 120, bar_start + 0, QN // 2)
            track.note(ch, 36, 100, bar_start + int(1.5 * QN), QN // 2)
            track.note(ch, 36, 115, bar_start + 2 * QN, QN // 2)
            # Gated electronic snare on 2 and 4
            track.note(ch, 40, 120, bar_start + 1 * QN, QN // 2)
            track.note(ch, 40, 127, bar_start + 3 * QN, QN // 2)
            for h in range(8):
                track.note(ch, 42, 80, bar_start + int(h * 0.5 * QN), QN // 4)


# -----------------------------------------------------------------------------
# 1. Gasoline Heart (ガソリン・ハート) - 132 BPM E Minor / A Minor
# -----------------------------------------------------------------------------
def make_gasoline_heart():
    mf = MidiFile(division=QN)
    
    # Track 0: Conductor
    t0 = MidiTrack("Conductor")
    t0.set_tempo(132, 0)
    t0.copyright("(c) 1985 Orion Records / Sequenced by Rick D. (Stardust Webring)")
    t0.marker("Intro", 0)
    t0.marker("Verse 1", int(8 * 4 * QN))
    t0.marker("Chorus", int(16 * 4 * QN))
    mf.add_track(t0)

    # Track 1: Lead Vocal (Synth Lead 81 Sawtooth)
    t1 = MidiTrack("Nova Lead Vocal")
    t1.program_change(0, 81, 0)
    t1.control_change(0, 7, 105, 0)  # Volume
    
    # Verse melody (starts at bar 8)
    melody_verse = [
        # Bar 8-9: "Kousaten no mukou..."
        (32.0, 1.0, 64), (33.0, 0.5, 67), (33.5, 1.5, 69), (35.0, 1.0, 71),
        (36.0, 0.5, 69), (36.5, 0.5, 67), (37.0, 2.0, 64),
        # Bar 10-11
        (40.0, 1.0, 64), (41.0, 0.5, 67), (41.5, 1.5, 69), (43.0, 1.0, 71),
        (44.0, 0.5, 72), (44.5, 0.5, 71), (45.0, 2.5, 69),
        # Bar 12-15: Pre-chorus climb
        (48.0, 0.5, 71), (48.5, 0.5, 72), (49.0, 1.0, 74), (50.0, 2.0, 76),
        (52.0, 0.5, 74), (52.5, 0.5, 72), (53.0, 1.0, 71), (54.0, 2.0, 69),
        (56.0, 1.0, 71), (57.0, 1.0, 74), (58.0, 3.0, 76),
    ]
    # Chorus melody (starts at bar 16: "GASOLINE HEART!")
    melody_chorus = [
        # Bar 16-17: High hook
        (64.0, 1.5, 76), (65.5, 0.5, 79), (66.0, 2.0, 81),
        (68.0, 1.0, 79), (69.0, 1.0, 76), (70.0, 2.0, 74),
        # Bar 18-19: Answer
        (72.0, 1.5, 76), (73.5, 0.5, 79), (74.0, 2.0, 81),
        (76.0, 1.0, 83), (77.0, 1.0, 81), (78.0, 2.5, 76),
        # Bar 20-23: Big vocal resolution
        (80.0, 1.0, 79), (81.0, 1.0, 76), (82.0, 1.0, 74), (83.0, 1.0, 72),
        (84.0, 0.5, 71), (84.5, 0.5, 69), (85.0, 2.0, 67), (87.0, 1.0, 69),
        (88.0, 4.0, 64),
    ]
    for beat, dur, pitch in melody_verse + melody_chorus:
        t1.note(0, pitch, 105, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Track 2: Rhythm Chords (DX7 Electric Piano 4)
    t2 = MidiTrack("DX7 E.Piano / Chords")
    t2.program_change(1, 4, 0)
    t2.control_change(1, 7, 90, 0)
    chords = [
        # Intro: Em7 -> Cmaj7 -> Am7 -> Bm7
        ([64, 67, 71, 74], 4), ([60, 64, 67, 71], 4), ([57, 60, 64, 67], 4), ([59, 62, 66, 69], 4),
        ([64, 67, 71, 74], 4), ([60, 64, 67, 71], 4), ([57, 60, 64, 67], 4), ([59, 62, 66, 71], 4),
    ] * 3  # Intro + Verse + Chorus
    curr_beat = 0.0
    for chord_notes, dur_beats in chords:
        # Syncopated comping on beat 0, 1.5, 2.5
        for stab in (0.0, 1.5, 2.5):
            t2.chord(1, chord_notes, 85, int((curr_beat + stab) * QN), int(0.9 * QN))
        curr_beat += dur_beats
    mf.add_track(t2)

    # Track 3: Slap Bass (36)
    t3 = MidiTrack("Slap Bass")
    t3.program_change(2, 36, 0)
    t3.control_change(2, 7, 100, 0)
    bass_roots = [40, 36, 33, 35, 40, 36, 33, 35] * 3  # E, C, A, B
    for idx, root in enumerate(bass_roots):
        b_start = idx * 4
        # Slap root + octave pop
        t3.note(2, root, 105, int((b_start + 0.0) * QN), int(0.7 * QN))
        t3.note(2, root + 12, 115, int((b_start + 1.5) * QN), int(0.5 * QN))
        t3.note(2, root, 100, int((b_start + 2.0) * QN), int(0.7 * QN))
        t3.note(2, root + 7, 95, int((b_start + 3.0) * QN), int(0.5 * QN))
        t3.note(2, root + 12, 110, int((b_start + 3.5) * QN), int(0.5 * QN))
    mf.add_track(t3)

    # Track 4: Synth Brass (62)
    t4 = MidiTrack("Synth Brass Stabs")
    t4.program_change(3, 62, 0)
    t4.control_change(3, 7, 95, 0)
    for b in range(16, 24):  # Chorus brass stabs
        st_start = b * 4
        t4.chord(3, [64, 67, 72], 100, int((st_start + 1.5) * QN), int(0.6 * QN))
        t4.chord(3, [64, 67, 72], 105, int((st_start + 2.5) * QN), int(0.6 * QN))
    mf.add_track(t4)

    # Track 5: Drums (Channel 10)
    t5 = MidiTrack("LinnDrum Kit")
    for b_chunk in range(0, 24, 4):
        add_drum_pattern(t5, "rock_driving", b_chunk, bars=4)
    mf.add_track(t5)
    
    return mf


# -----------------------------------------------------------------------------
# 2. Ghost Transit (ゴースト・トランジット) - 84 BPM D Minor / F Major
# -----------------------------------------------------------------------------
def make_ghost_transit():
    mf = MidiFile(division=QN)
    
    t0 = MidiTrack("Conductor")
    t0.set_tempo(84, 0)
    t0.copyright("(c) 1985 Orion Records / Sequenced by Yuki Tanabe (Kamome-Net)")
    t0.marker("Shortwave Intro", 0)
    t0.marker("Ballad Verse", int(4 * 4 * QN))
    t0.marker("Chorus", int(12 * 4 * QN))
    mf.add_track(t0)

    # Vocal (Flute / Warm Lead 73)
    t1 = MidiTrack("Nova Vocal (Flute/Lead)")
    t1.program_change(0, 73, 0)
    t1.control_change(0, 7, 100, 0)
    melody = [
        # Verse (Bar 4-7: "Yoru no ressha wa...")
        (16.0, 1.5, 62), (17.5, 0.5, 65), (18.0, 2.0, 67),
        (20.0, 1.0, 69), (21.0, 1.0, 67), (22.0, 2.0, 65),
        (24.0, 1.5, 62), (25.5, 0.5, 65), (26.0, 2.0, 67),
        (28.0, 1.0, 69), (29.0, 1.0, 72), (30.0, 2.5, 74),
        # Pre-chorus (Bar 8-11)
        (32.0, 1.5, 74), (33.5, 0.5, 72), (34.0, 1.0, 70), (35.0, 2.0, 69),
        (36.0, 1.5, 67), (37.5, 0.5, 69), (38.0, 1.0, 70), (39.0, 2.0, 72),
        (40.0, 1.0, 74), (41.0, 1.0, 76), (42.0, 2.0, 77), (44.0, 4.0, 76),
        # Chorus (Bar 12-19: "GHOST TRANSIT...")
        (48.0, 2.0, 77), (50.0, 1.0, 76), (51.0, 1.0, 74),
        (52.0, 2.0, 72), (54.0, 1.0, 70), (55.0, 1.0, 69),
        (56.0, 2.5, 70), (58.5, 0.5, 72), (59.0, 1.5, 74),
        (61.0, 1.0, 72), (62.0, 2.0, 69), (64.0, 4.0, 62),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 100, int(beat * QN), int(dur * QN * 0.96))
    mf.add_track(t1)

    # Rhodes & Piano (4)
    t2 = MidiTrack("DX7 Rhodes & Piano")
    t2.program_change(1, 4, 0)
    chords = [
        ([50, 57, 62, 65], 4), ([46, 53, 58, 62], 4), ([43, 50, 55, 58], 4), ([45, 52, 57, 60], 4)
    ] * 5
    curr_beat = 0.0
    for chord_notes, dur_beats in chords:
        for arp_idx, p in enumerate(chord_notes):
            t2.note(1, p, 80, int((curr_beat + arp_idx * 0.5) * QN), int(3.5 * QN))
        curr_beat += dur_beats
    mf.add_track(t2)

    # Strings Pad (48)
    t3 = MidiTrack("Synth String Ensemble")
    t3.program_change(2, 48, 0)
    t3.control_change(2, 7, 75, 0)
    curr_beat = 0.0
    for chord_notes, dur_beats in chords:
        t3.chord(2, [p + 12 for p in chord_notes[:3]], 70, int(curr_beat * QN), int(dur_beats * QN))
        curr_beat += dur_beats
    mf.add_track(t3)

    # Fretless Bass (35)
    t4 = MidiTrack("Fretless Bass")
    t4.program_change(3, 35, 0)
    roots = [38, 34, 31, 33] * 5  # D, Bb, G, A
    for idx, r in enumerate(roots):
        b_pos = idx * 4
        t4.note(3, r, 95, int((b_pos + 0.0) * QN), int(2.5 * QN))
        t4.note(3, r + 7, 85, int((b_pos + 2.5) * QN), int(1.2 * QN))
    mf.add_track(t4)

    # Drums (Channel 10)
    t5 = MidiTrack("Ballad Percussion")
    for b_chunk in range(0, 20, 4):
        add_drum_pattern(t5, "ballad_slow", b_chunk, bars=4)
    mf.add_track(t5)
    
    return mf


# -----------------------------------------------------------------------------
# 3. Midnight Animal (ミッドナイト・アニマル) - 118 BPM C Minor / Funk
# -----------------------------------------------------------------------------
def make_midnight_animal():
    mf = MidiFile(division=QN)
    
    t0 = MidiTrack("Conductor")
    t0.set_tempo(118, 0)
    t0.copyright("(c) 1986 Orion Records / Sequenced by Aiko (Tokyo-Garden-1420)")
    t0.marker("Slap Bass Intro", 0)
    t0.marker("Funk Verse", int(4 * 4 * QN))
    t0.marker("Brass Chorus", int(12 * 4 * QN))
    mf.add_track(t0)

    # Lead Vocal / Synth Lead (81)
    t1 = MidiTrack("Vocal Melody")
    t1.program_change(0, 81, 0)
    melody = [
        # Verse (Bar 4-7: "Mayonaka no machi...")
        (16.0, 0.5, 60), (16.5, 0.5, 63), (17.0, 1.0, 65), (18.5, 0.5, 67),
        (19.0, 1.0, 65), (20.0, 1.5, 63), (21.5, 0.5, 60),
        (24.0, 0.5, 60), (24.5, 0.5, 63), (25.0, 1.0, 65), (26.5, 0.5, 67),
        (27.0, 1.0, 70), (28.0, 2.0, 72),
        # Chorus (Bar 12-19: "MIDNIGHT ANIMAL!")
        (48.0, 1.0, 72), (49.0, 0.5, 75), (49.5, 1.5, 77), (51.5, 0.5, 75),
        (52.0, 1.5, 72), (54.0, 1.5, 70), (55.5, 0.5, 67),
        (56.0, 1.0, 72), (57.0, 0.5, 75), (57.5, 1.5, 77), (59.0, 1.0, 79),
        (60.0, 2.0, 77), (62.0, 2.0, 72),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 105, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Synth Brass (62)
    t2 = MidiTrack("Synth Brass Section")
    t2.program_change(1, 62, 0)
    t2.control_change(1, 7, 95, 0)
    for b in range(0, 20):
        b_pos = b * 4
        # Funky brass stabs on beat 1.5 and 3.5
        t2.chord(1, [63, 67, 72], 100, int((b_pos + 1.5) * QN), int(0.4 * QN))
        t2.chord(1, [63, 67, 72], 110, int((b_pos + 3.5) * QN), int(0.4 * QN))
    mf.add_track(t2)

    # Clavinet / E.Piano (7)
    t3 = MidiTrack("Clavinet Funk Comp")
    t3.program_change(2, 7, 0)
    t3.control_change(2, 7, 90, 0)
    for b in range(0, 20):
        b_pos = b * 4
        for sixteenth in [0, 2, 3, 5, 7, 8, 10, 11, 14]:
            t3.note(2, 60, 85, int((b_pos + sixteenth * 0.25) * QN), int(0.2 * QN))
    mf.add_track(t3)

    # Slap Bass (37)
    t4 = MidiTrack("Slap Bass (Octaves)")
    t4.program_change(3, 37, 0)
    for b in range(0, 20):
        b_pos = b * 4
        # C minor funk groove
        t4.note(3, 36, 110, int((b_pos + 0.0) * QN), int(0.4 * QN))
        t4.note(3, 48, 120, int((b_pos + 0.5) * QN), int(0.4 * QN))
        t4.note(3, 36, 95, int((b_pos + 1.5) * QN), int(0.4 * QN))
        t4.note(3, 46, 105, int((b_pos + 2.0) * QN), int(0.4 * QN))
        t4.note(3, 48, 115, int((b_pos + 2.5) * QN), int(0.4 * QN))
        t4.note(3, 39, 100, int((b_pos + 3.25) * QN), int(0.4 * QN))
        t4.note(3, 41, 105, int((b_pos + 3.75) * QN), int(0.4 * QN))
    mf.add_track(t4)

    # Drums (Channel 10)
    t5 = MidiTrack("Disco Funk Kit")
    for b_chunk in range(0, 20, 4):
        add_drum_pattern(t5, "disco_funk", b_chunk, bars=4)
    mf.add_track(t5)
    
    return mf


# -----------------------------------------------------------------------------
# 4. Brighter Than The Sun (太陽よりも、輝いて！) - 126 BPM F Major / Idol Pop
# -----------------------------------------------------------------------------
def make_brighter_than_sun():
    mf = MidiFile(division=QN)
    
    t0 = MidiTrack("Conductor")
    t0.set_tempo(126, 0)
    t0.copyright("(c) 1987 Orion Records / Sequenced for The Stardust Webring")
    t0.marker("Bell Intro", 0)
    t0.marker("Idol Verse", int(4 * 4 * QN))
    t0.marker("Sparkling Chorus", int(12 * 4 * QN))
    mf.add_track(t0)

    # Vocal (Acoustic Piano / Bright Lead 0)
    t1 = MidiTrack("Idol Vocal")
    t1.program_change(0, 0, 0)
    t1.control_change(0, 7, 105, 0)
    melody = [
        # Verse (Bar 4-7: "Taiyou yori mo...")
        (16.0, 1.0, 65), (17.0, 1.0, 69), (18.0, 1.5, 72), (19.5, 0.5, 74),
        (20.0, 2.0, 72), (22.0, 1.0, 69), (23.0, 1.0, 67),
        (24.0, 1.0, 65), (25.0, 1.0, 69), (26.0, 1.5, 72), (27.5, 0.5, 76),
        (28.0, 2.0, 74), (30.0, 2.0, 72),
        # Pre-chorus (Bar 8-11)
        (32.0, 1.0, 70), (33.0, 1.0, 72), (34.0, 1.5, 74), (35.5, 0.5, 76),
        (36.0, 2.0, 74), (38.0, 1.0, 72), (39.0, 1.0, 70),
        (40.0, 1.0, 72), (41.0, 1.0, 74), (42.0, 2.0, 76), (44.0, 4.0, 77),
        # Chorus (Bar 12-19: "Kagayaite!")
        (48.0, 1.5, 77), (49.5, 0.5, 79), (50.0, 2.0, 81),
        (52.0, 1.0, 79), (53.0, 1.0, 77), (54.0, 2.0, 76),
        (56.0, 1.5, 74), (57.5, 0.5, 76), (58.0, 2.0, 77),
        (60.0, 1.0, 76), (61.0, 1.0, 74), (62.0, 2.0, 72),
        (64.0, 4.0, 65),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 105, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Bells / Crystal (98)
    t2 = MidiTrack("Twinkling Bells")
    t2.program_change(1, 98, 0)
    t2.control_change(1, 7, 85, 0)
    for b in range(0, 20):
        b_pos = b * 4
        # 16th note arpeggios
        for s, p in enumerate([77, 81, 84, 89, 84, 81]):
            t2.note(1, p, 80, int((b_pos + s * 0.5) * QN), int(0.4 * QN))
    mf.add_track(t2)

    # Chords (Electric Piano 4)
    t3 = MidiTrack("E.Piano Chords")
    t3.program_change(2, 4, 0)
    chords = [
        ([53, 60, 65, 69], 4), ([50, 57, 62, 65], 4), ([46, 53, 58, 62], 4), ([48, 55, 60, 64], 4)
    ] * 5
    curr_beat = 0.0
    for chord_notes, dur_beats in chords:
        for stab in (0.0, 1.5, 2.5):
            t3.chord(2, chord_notes, 85, int((curr_beat + stab) * QN), int(0.8 * QN))
        curr_beat += dur_beats
    mf.add_track(t3)

    # Synth Bass (38)
    t4 = MidiTrack("Synth Bass")
    t4.program_change(3, 38, 0)
    roots = [41, 38, 34, 36] * 5  # F, D, Bb, C
    for idx, r in enumerate(roots):
        b_pos = idx * 4
        for eighth in range(8):
            t4.note(3, r, 95 if eighth % 2 == 0 else 80, int((b_pos + eighth * 0.5) * QN), int(0.4 * QN))
    mf.add_track(t4)

    # Drums (Channel 10)
    t5 = MidiTrack("Pop Idol Drums")
    for b_chunk in range(0, 20, 4):
        add_drum_pattern(t5, "idol_pop", b_chunk, bars=4)
    mf.add_track(t5)
    
    return mf


# -----------------------------------------------------------------------------
# 5. Only We Remain (残されたのは、私たちだけ) - 72 BPM G Minor / Kayokyoku Ballad
# -----------------------------------------------------------------------------
def make_only_we_remain():
    mf = MidiFile(division=QN)
    
    t0 = MidiTrack("Conductor")
    t0.set_tempo(72, 0)
    t0.copyright("(c) 1989 Orion Records / Sequenced for The Stardust Webring")
    t0.marker("Piano Solo", 0)
    t0.marker("Dramatic Verse", int(4 * 4 * QN))
    t0.marker("Grand Chorus", int(12 * 4 * QN))
    mf.add_track(t0)

    # Lead Violin / Solo Strings (40)
    t1 = MidiTrack("Nova Solo Violin")
    t1.program_change(0, 40, 0)
    t1.control_change(0, 7, 105, 0)
    melody = [
        # Verse (Bar 4-7)
        (16.0, 1.5, 55), (17.5, 0.5, 58), (18.0, 2.0, 62),
        (20.0, 1.0, 65), (21.0, 1.0, 63), (22.0, 2.0, 62),
        (24.0, 1.5, 58), (25.5, 0.5, 62), (26.0, 2.0, 65),
        (28.0, 1.0, 67), (29.0, 1.0, 69), (30.0, 2.5, 70),
        # Pre-chorus (Bar 8-11: Crescendo)
        (32.0, 1.5, 70), (33.5, 0.5, 69), (34.0, 1.0, 67), (35.0, 2.0, 65),
        (36.0, 1.5, 63), (37.5, 0.5, 65), (38.0, 1.0, 67), (39.0, 2.0, 69),
        (40.0, 1.0, 70), (41.0, 1.0, 72), (42.0, 2.0, 74), (44.0, 4.0, 72),
        # Chorus (Bar 12-19: "NOKOSARETA NO WA...")
        (48.0, 2.0, 74), (50.0, 1.0, 72), (51.0, 1.0, 70),
        (52.0, 2.0, 69), (54.0, 1.0, 67), (55.0, 1.0, 65),
        (56.0, 2.5, 67), (58.5, 0.5, 69), (59.0, 1.5, 70),
        (61.0, 1.0, 69), (62.0, 2.0, 67), (64.0, 4.0, 55),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 100, int(beat * QN), int(dur * QN * 0.96))
    mf.add_track(t1)

    # Grand Piano (0)
    t2 = MidiTrack("Acoustic Grand Piano")
    t2.program_change(1, 0, 0)
    chords = [
        ([43, 50, 55, 58], 4), ([39, 46, 51, 55], 4), ([36, 43, 48, 51], 4), ([38, 45, 50, 53], 4)
    ] * 5
    curr_beat = 0.0
    for chord_notes, dur_beats in chords:
        for arp_idx, p in enumerate(chord_notes):
            t2.note(1, p, 85, int((curr_beat + arp_idx * 0.5) * QN), int(3.5 * QN))
        curr_beat += dur_beats
    mf.add_track(t2)

    # String Ensemble (48)
    t3 = MidiTrack("String Orchestra")
    t3.program_change(2, 48, 0)
    t3.control_change(2, 7, 85, 0)
    curr_beat = 0.0
    for chord_notes, dur_beats in chords:
        t3.chord(2, [p + 12 for p in chord_notes], 75, int(curr_beat * QN), int(dur_beats * QN))
        curr_beat += dur_beats
    mf.add_track(t3)

    # Acoustic Bass (32)
    t4 = MidiTrack("Acoustic Bass")
    t4.program_change(3, 32, 0)
    roots = [31, 27, 24, 26] * 5  # G, Eb, C, D
    for idx, r in enumerate(roots):
        b_pos = idx * 4
        t4.note(3, r, 95, int((b_pos + 0.0) * QN), int(3.5 * QN))
    mf.add_track(t4)

    # Timpani & Percussion (Channel 10)
    t5 = MidiTrack("Timpani & Ballad Drums")
    for b_chunk in range(0, 20, 4):
        add_drum_pattern(t5, "ballad_slow", b_chunk, bars=4)
    mf.add_track(t5)
    
    return mf


# -----------------------------------------------------------------------------
# 6. Synthetic Dawn - 116 BPM A Minor / Industrial Synthpop
# -----------------------------------------------------------------------------
def make_synthetic_dawn():
    mf = MidiFile(division=QN)
    
    t0 = MidiTrack("Conductor")
    t0.set_tempo(116, 0)
    t0.copyright("(c) 1985 Orion Records / SYNTHESIS Track 01")
    t0.marker("Industrial Intro", 0)
    t0.marker("Main Synth Theme", int(4 * 4 * QN))
    mf.add_track(t0)

    # Square Wave Lead (80)
    t1 = MidiTrack("Square Wave Lead")
    t1.program_change(0, 80, 0)
    melody = [
        # Bar 4-7: Driving industrial hook
        (16.0, 1.0, 69), (17.0, 0.5, 72), (17.5, 0.5, 71), (18.0, 1.0, 69),
        (19.0, 1.0, 67), (20.0, 2.0, 69),
        (24.0, 1.0, 69), (25.0, 0.5, 72), (25.5, 0.5, 74), (26.0, 1.0, 76),
        (27.0, 1.0, 74), (28.0, 2.0, 72),
        # Bar 8-11: Second phrase
        (32.0, 1.0, 76), (33.0, 0.5, 79), (33.5, 0.5, 77), (34.0, 1.0, 76),
        (35.0, 1.0, 72), (36.0, 2.0, 74),
        (40.0, 1.0, 72), (41.0, 1.0, 71), (42.0, 1.0, 69), (43.0, 1.0, 67),
        (44.0, 4.0, 69),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 110, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Dark Synth Strings (50)
    t2 = MidiTrack("Synth Strings Pad")
    t2.program_change(1, 50, 0)
    chords = [([45, 52, 57, 60], 4), ([41, 48, 53, 57], 4), ([48, 55, 60, 64], 4), ([43, 50, 55, 59], 4)] * 3
    curr_beat = 0.0
    for chord_notes, dur_beats in chords:
        t2.chord(1, chord_notes, 80, int(curr_beat * QN), int(dur_beats * QN))
        curr_beat += dur_beats
    mf.add_track(t2)

    # 16th note Synth Bass (39)
    t3 = MidiTrack("Sequencer Synth Bass")
    t3.program_change(2, 39, 0)
    roots = [33, 29, 36, 31] * 3  # A, F, C, G
    for idx, r in enumerate(roots):
        b_pos = idx * 4
        for sixteenth in range(16):
            pitch = r if sixteenth % 4 != 2 else r + 12
            t3.note(2, pitch, 95 if sixteenth % 4 == 0 else 75, int((b_pos + sixteenth * 0.25) * QN), int(0.2 * QN))
    mf.add_track(t3)

    # Drums (Channel 10)
    t4 = MidiTrack("LinnDrum Electronic")
    for b_chunk in range(0, 12, 4):
        add_drum_pattern(t4, "synth_industrial", b_chunk, bars=4)
    mf.add_track(t4)
    
    return mf


# -----------------------------------------------------------------------------
# 7. Memory Hatch - 104 BPM B Minor / Sophisti-Pop
# -----------------------------------------------------------------------------
def make_memory_hatch():
    mf = MidiFile(division=QN)
    
    t0 = MidiTrack("Conductor")
    t0.set_tempo(104, 0)
    t0.copyright("(c) 1985 Orion Records / SYNTHESIS Track 09")
    t0.marker("Rhodes Intro", 0)
    t0.marker("Vibraphone Theme", int(4 * 4 * QN))
    mf.add_track(t0)

    # Vibraphone (11)
    t1 = MidiTrack("Vibraphone Melody")
    t1.program_change(0, 11, 0)
    t1.control_change(0, 7, 105, 0)
    melody = [
        # Bar 4-7: Breezy, sophisticated theme
        (16.0, 1.5, 71), (17.5, 0.5, 74), (18.0, 1.0, 76), (19.0, 1.0, 74),
        (20.0, 2.0, 71), (22.0, 1.0, 69), (23.0, 1.0, 67),
        (24.0, 1.5, 71), (25.5, 0.5, 74), (26.0, 1.0, 78), (27.0, 1.0, 76),
        (28.0, 2.0, 74), (30.0, 2.0, 71),
        # Bar 8-11: Resolution
        (32.0, 1.0, 69), (33.0, 1.0, 71), (34.0, 1.5, 74), (35.5, 0.5, 76),
        (36.0, 2.0, 74), (38.0, 1.0, 71), (39.0, 1.0, 69),
        (40.0, 1.0, 67), (41.0, 1.0, 69), (42.0, 2.0, 71), (44.0, 4.0, 59),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 100, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Fender Rhodes (4)
    t2 = MidiTrack("Fender Rhodes E.Piano")
    t2.program_change(1, 4, 0)
    chords = [([47, 54, 59, 62], 4), ([43, 50, 55, 59], 4), ([40, 47, 52, 55], 4), ([42, 49, 54, 58], 4)] * 3
    curr_beat = 0.0
    for chord_notes, dur_beats in chords:
        for stab in (0.0, 1.5, 2.5):
            t2.chord(1, chord_notes, 85, int((curr_beat + stab) * QN), int(0.9 * QN))
        curr_beat += dur_beats
    mf.add_track(t2)

    # Electric Finger Bass (33)
    t3 = MidiTrack("Finger Bass")
    t3.program_change(2, 33, 0)
    roots = [35, 31, 28, 30] * 3  # B, G, E, F#
    for idx, r in enumerate(roots):
        b_pos = idx * 4
        t3.note(2, r, 95, int((b_pos + 0.0) * QN), int(1.2 * QN))
        t3.note(2, r + 7, 85, int((b_pos + 1.5) * QN), int(0.8 * QN))
        t3.note(2, r, 90, int((b_pos + 2.5) * QN), int(1.0 * QN))
        t3.note(2, r + 12, 100, int((b_pos + 3.5) * QN), int(0.5 * QN))
    mf.add_track(t3)

    # Smooth Drums (Channel 10)
    t4 = MidiTrack("City Pop Drums")
    for b_chunk in range(0, 12, 4):
        add_drum_pattern(t4, "disco_funk", b_chunk, bars=4)
    mf.add_track(t4)
    
    return mf


# -----------------------------------------------------------------------------
# Main Generator Runner
# -----------------------------------------------------------------------------
SONGS = [
    ("gasoline_heart.mid", "Gasoline Heart (ガソリン・ハート)", make_gasoline_heart),
    ("ghost_transit.mid", "Ghost Transit (ゴースト・トランジット)", make_ghost_transit),
    ("midnight_animal.mid", "Midnight Animal (ミッドナイト・アニマル)", make_midnight_animal),
    ("brighter_than_sun.mid", "Brighter Than The Sun (太陽よりも、輝いて！)", make_brighter_than_sun),
    ("only_we_remain.mid", "Only We Remain (残されたのは、私たちだけ)", make_only_we_remain),
    ("synthetic_dawn.mid", "Synthetic Dawn (Akasaka Mix)", make_synthetic_dawn),
    ("memory_hatch.mid", "Memory Hatch (Sophisti-Pop)", make_memory_hatch),
]


def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(root_dir, "assets", "midi")
    os.makedirs(out_dir, exist_ok=True)
    
    print("\nGenerating authentic 1990s Nova Hart MIDI tracks...")
    manifest = []
    for fname, title, fn in SONGS:
        dest = os.path.join(out_dir, fname)
        mf = fn()
        mf.write(dest)
        sz = os.path.getsize(dest)
        print(f"  ✓ {fname:<26} ({sz:>5d} bytes) - {title}")
        manifest.append((fname, title, sz))
        
    print(f"\nGenerated {len(manifest)} MIDI tracks in {out_dir}")


if __name__ == "__main__":
    main()
