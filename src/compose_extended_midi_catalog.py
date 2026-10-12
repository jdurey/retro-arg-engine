"""Composes 11 new authentic 1980s multi-track MIDI compositions for Project Stardust.
Brings the total catalog of original procedural MIDI tracks from 19 to 30.

Tracks composed:
 20. neon_corridor_88.mid         - 128 BPM Outrun / Neon Highway Synthwave (D Minor)
 21. tokyo_twilight_express.mid   - 112 BPM City Pop Funk / Slap Bass & Fender Rhodes (A Dorian)
 22. orion_subroutine_142.mid     - 136 BPM Cyberpunk Industrial 16th Sequencer (C Minor)
 23. signal_fading_in_the_fog.mid - 78 BPM Lush DX7 Ballad / Synth Strings & Flute (G Minor)
 24. analog_heartbeat_1984.mid    - 122 BPM Sparkling Idol Pop / DX7 Bells & Chorus (F Major)
 25. cybernetic_vow.mid           - 140 BPM Fast Italo-Disco / Saw Lead & Brass (B Minor)
 26. whispers_at_midnight.mid     - 92 BPM Sophisti-Pop / Vibraphone & 9th Chords (E Major)
 27. kamome_packet_radio.mid      - 118 BPM Chiptune-Synth Hybrid / Square Wave & LinnDrum (A Minor)
 28. satellite_intercept_89.mid   - 105 BPM Dark Ambient Synth / FM Bell & Sub Bass (D Minor)
 29. stardust_memory_reprise.mid  - 70 BPM Grand Kayokyoku Emotional Finale / Strings & Grand Piano (C Minor)
 30. electric_mirage.mid          - 126 BPM Dream Pop / Lush Detuned Pads & Lead (Eb Major)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from midi_engine import MidiFile, MidiTrack

QN = 480


def add_drum_pattern(track, pattern_type, start_beat, bars=4):
    ch = 9
    for b in range(bars):
        bar_start = int((start_beat + b * 4) * QN)
        if pattern_type == "outrun":
            for k in (0, 1.5, 2, 3.5):
                track.note(ch, 36, 115, bar_start + int(k * QN), QN // 2)
            track.note(ch, 40, 125, bar_start + 1 * QN, QN // 2)
            track.note(ch, 40, 125, bar_start + 3 * QN, QN // 2)
            for s in range(16):
                track.note(ch, 42, 85 if s % 2 == 0 else 65, bar_start + int(s * 0.25 * QN), QN // 8)
            if b % 2 == 0:
                track.note(ch, 49, 110, bar_start, QN)
        elif pattern_type == "funk":
            for k in range(4):
                track.note(ch, 36, 105, bar_start + k * QN, QN // 2)
            track.note(ch, 38, 110, bar_start + 1 * QN, QN // 2)
            track.note(ch, 38, 115, bar_start + 3 * QN, QN // 2)
            for o in range(4):
                track.note(ch, 42, 80, bar_start + o * QN, QN // 4)
                track.note(ch, 46, 95, bar_start + int((o + 0.5) * QN), QN // 4)
        elif pattern_type == "ballad":
            track.note(ch, 35, 95, bar_start + 0, QN // 2)
            track.note(ch, 35, 80, bar_start + int(2.5 * QN), QN // 2)
            track.note(ch, 37, 90, bar_start + 1 * QN, QN // 2)
            track.note(ch, 37, 95, bar_start + 3 * QN, QN // 2)
            for h in range(8):
                track.note(ch, 51, 75 if h % 2 == 0 else 55, bar_start + int(h * 0.5 * QN), QN // 2)
            if b == 0:
                track.note(ch, 49, 90, bar_start, QN)
        elif pattern_type == "pop":
            track.note(ch, 36, 110, bar_start + 0, QN // 2)
            track.note(ch, 36, 90, bar_start + int(1.5 * QN), QN // 2)
            track.note(ch, 36, 105, bar_start + 2 * QN, QN // 2)
            track.note(ch, 40, 115, bar_start + 1 * QN, QN // 2)
            track.note(ch, 40, 115, bar_start + 3 * QN, QN // 2)
            for h in range(16):
                track.note(ch, 42, 80 if h % 4 == 0 else 60, bar_start + int(h * 0.25 * QN), QN // 8)
        elif pattern_type == "italo":
            for k in range(4):
                track.note(ch, 36, 120, bar_start + k * QN, QN // 2)
            track.note(ch, 38, 120, bar_start + 1 * QN, QN // 2)
            track.note(ch, 38, 125, bar_start + 3 * QN, QN // 2)
            for s in range(16):
                track.note(ch, 42, 90 if s % 2 == 0 else 70, bar_start + int(s * 0.25 * QN), QN // 8)
            track.note(ch, 49, 110, bar_start, QN)
        else: # smooth / ambient
            track.note(ch, 35, 80, bar_start + 0, QN)
            track.note(ch, 38, 85, bar_start + 2 * QN, QN)
            for h in range(4):
                track.note(ch, 42, 60, bar_start + h * QN, QN // 4)


# 20. Neon Corridor '88 (128 BPM, D Minor)
def make_neon_corridor():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(128, 0)
    t0.copyright("(c) 1988 Orion Records / Stardust Webring")
    mf.add_track(t0)

    # Lead Synth
    t1 = MidiTrack("Neon Lead Synth")
    t1.program_change(0, 81, 0)
    melody = [
        (0.0, 1.0, 62), (1.0, 0.5, 65), (1.5, 0.5, 67), (2.0, 1.0, 69), (3.0, 1.0, 72),
        (4.0, 1.5, 74), (5.5, 0.5, 72), (6.0, 2.0, 69),
        (8.0, 1.0, 62), (9.0, 0.5, 65), (9.5, 0.5, 67), (10.0, 1.0, 69), (11.0, 1.0, 74),
        (12.0, 2.0, 76), (14.0, 2.0, 74),
        (16.0, 1.5, 77), (17.5, 0.5, 76), (18.0, 1.0, 74), (19.0, 1.0, 72),
        (20.0, 2.0, 69), (22.0, 2.0, 72), (24.0, 4.0, 62),
    ] * 2
    curr = 0.0
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 105, int((curr + beat) * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Chords
    t2 = MidiTrack("Synth Brass & Pads")
    t2.program_change(1, 62, 0)
    chords = [([50, 57, 62, 65], 4), ([46, 53, 58, 62], 4), ([43, 50, 55, 58], 4), ([45, 52, 57, 60], 4)] * 4
    b_curr = 0.0
    for ch_notes, dur in chords:
        t2.chord(1, ch_notes, 85, int(b_curr * QN), int(dur * QN * 0.9))
        b_curr += dur
    mf.add_track(t2)

    # 16th Bass
    t3 = MidiTrack("Outrun Synth Bass")
    t3.program_change(2, 38, 0)
    roots = [38, 34, 31, 33] * 4
    for idx, r in enumerate(roots):
        b_pos = idx * 4
        for s in range(16):
            p = r if s % 4 != 2 else r + 12
            t3.note(2, p, 100 if s % 4 == 0 else 80, int((b_pos + s * 0.25) * QN), int(0.2 * QN))
    mf.add_track(t3)

    # Drums
    t4 = MidiTrack("LinnDrum Outrun")
    for b in range(0, 16, 4):
        add_drum_pattern(t4, "outrun", b, bars=4)
    mf.add_track(t4)
    return mf


# 21. Tokyo Twilight Express (112 BPM, A Dorian)
def make_tokyo_twilight():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(112, 0)
    t0.copyright("(c) 1986 Orion Records / Kamome-Net")
    mf.add_track(t0)

    # Rhodes Melody
    t1 = MidiTrack("DX7 Rhodes & Vibraphone")
    t1.program_change(0, 4, 0)
    melody = [
        (0.0, 1.0, 69), (1.0, 0.5, 72), (1.5, 0.5, 74), (2.0, 1.5, 76), (3.5, 0.5, 74),
        (4.0, 2.0, 72), (6.0, 2.0, 69),
        (8.0, 1.0, 69), (9.0, 0.5, 71), (9.5, 0.5, 72), (10.0, 1.5, 74), (11.5, 0.5, 76),
        (12.0, 2.0, 77), (14.0, 2.0, 76),
    ] * 2
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 100, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Funk Clavinet
    t2 = MidiTrack("Clavinet Comp")
    t2.program_change(1, 7, 0)
    for b in range(16):
        for s in (0, 1.5, 2.5, 3.5):
            t2.chord(1, [60, 64, 69], 80, int((b * 4 + s) * QN), int(0.3 * QN))
    mf.add_track(t2)

    # Slap Bass
    t3 = MidiTrack("City Pop Slap Bass")
    t3.program_change(2, 36, 0)
    for b in range(16):
        b_pos = b * 4
        t3.note(2, 33, 110, int((b_pos + 0.0) * QN), int(0.4 * QN))
        t3.note(2, 45, 120, int((b_pos + 0.5) * QN), int(0.4 * QN))
        t3.note(2, 33, 95, int((b_pos + 1.5) * QN), int(0.4 * QN))
        t3.note(2, 43, 105, int((b_pos + 2.0) * QN), int(0.4 * QN))
        t3.note(2, 45, 115, int((b_pos + 2.5) * QN), int(0.4 * QN))
    mf.add_track(t3)

    # Drums
    t4 = MidiTrack("Funk Drums")
    for b in range(0, 16, 4):
        add_drum_pattern(t4, "funk", b, bars=4)
    mf.add_track(t4)
    return mf


# 22. Orion Subroutine 142 (136 BPM, C Minor)
def make_orion_subroutine():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(136, 0)
    t0.copyright("(c) 1989 Orion Records Research Dept")
    mf.add_track(t0)

    # Cyber Lead
    t1 = MidiTrack("Square Wave Lead")
    t1.program_change(0, 80, 0)
    melody = [
        (0.0, 0.5, 72), (0.5, 0.5, 75), (1.0, 1.0, 74), (2.0, 1.0, 72),
        (3.0, 0.5, 75), (3.5, 0.5, 77), (4.0, 2.0, 79),
        (6.0, 1.0, 77), (7.0, 1.0, 75), (8.0, 2.0, 74),
        (10.0, 1.0, 75), (11.0, 1.0, 74), (12.0, 4.0, 72),
    ] * 2
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 105, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # 16th Sequencer Bass
    t2 = MidiTrack("Sequencer Bass")
    t2.program_change(1, 39, 0)
    for b in range(16):
        b_pos = b * 4
        for s in range(16):
            p = 36 if s % 4 != 2 else 48
            t2.note(1, p, 100 if s % 4 == 0 else 80, int((b_pos + s * 0.25) * QN), int(0.2 * QN))
    mf.add_track(t2)

    # Industrial Drums
    t3 = MidiTrack("Industrial Kit")
    for b in range(0, 16, 4):
        add_drum_pattern(t3, "outrun", b, bars=4)
    mf.add_track(t3)
    return mf


# 23. Signal Fading in the Fog (78 BPM, G Minor)
def make_signal_fading():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(78, 0)
    t0.copyright("(c) 1985 Orion Records / Akasaka Studio")
    mf.add_track(t0)

    # Flute / Solo Synth
    t1 = MidiTrack("Warm Flute Lead")
    t1.program_change(0, 73, 0)
    melody = [
        (0.0, 2.0, 67), (2.0, 1.0, 70), (3.0, 1.0, 69), (4.0, 3.0, 67),
        (8.0, 2.0, 70), (10.0, 1.0, 72), (11.0, 1.0, 74), (12.0, 4.0, 75),
        (16.0, 2.0, 74), (18.0, 1.0, 72), (19.0, 1.0, 70), (20.0, 3.0, 69),
        (24.0, 4.0, 67),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 95, int(beat * QN), int(dur * QN * 0.98))
    mf.add_track(t1)

    # Strings Ensemble
    t2 = MidiTrack("Strings Pad")
    t2.program_change(1, 48, 0)
    chords = [([43, 50, 55, 58], 4), ([39, 46, 51, 55], 4), ([41, 48, 53, 57], 4), ([43, 50, 55, 58], 4)] * 2
    b_curr = 0.0
    for ch_notes, dur in chords:
        t2.chord(1, ch_notes, 75, int(b_curr * QN), int(dur * QN))
        b_curr += dur
    mf.add_track(t2)

    # Fretless Bass
    t3 = MidiTrack("Fretless Bass")
    t3.program_change(2, 35, 0)
    roots = [31, 27, 29, 31] * 2
    for idx, r in enumerate(roots):
        b_pos = idx * 4
        t3.note(2, r, 90, int((b_pos + 0.0) * QN), int(2.5 * QN))
        t3.note(2, r + 7, 80, int((b_pos + 2.5) * QN), int(1.2 * QN))
    mf.add_track(t3)

    # Ballad Drums
    t4 = MidiTrack("Soft Ballad Drums")
    for b in range(0, 8, 4):
        add_drum_pattern(t4, "ballad", b, bars=4)
    mf.add_track(t4)
    return mf


# 24. Analog Heartbeat 1984 (122 BPM, F Major)
def make_analog_heartbeat():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(122, 0)
    t0.copyright("(c) 1984 Orion Records Idol Division")
    mf.add_track(t0)

    # Crystal Bells Lead
    t1 = MidiTrack("Idol Bells & Lead")
    t1.program_change(0, 98, 0)
    melody = [
        (0.0, 1.0, 65), (1.0, 1.0, 69), (2.0, 1.5, 72), (3.5, 0.5, 74),
        (4.0, 2.0, 72), (6.0, 2.0, 69),
        (8.0, 1.0, 65), (9.0, 1.0, 69), (10.0, 1.5, 72), (11.5, 0.5, 76),
        (12.0, 2.0, 74), (14.0, 2.0, 72),
        (16.0, 1.5, 77), (17.5, 0.5, 79), (18.0, 2.0, 81), (20.0, 2.0, 77),
        (22.0, 2.0, 74), (24.0, 4.0, 65),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 105, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Electric Piano Chords
    t2 = MidiTrack("DX7 E.Piano")
    t2.program_change(1, 4, 0)
    chords = [([53, 60, 65, 69], 4), ([50, 57, 62, 65], 4), ([46, 53, 58, 62], 4), ([48, 55, 60, 64], 4)] * 2
    b_curr = 0.0
    for ch_notes, dur in chords:
        for s in (0.0, 1.5, 2.5):
            t2.chord(1, ch_notes, 85, int((b_curr + s) * QN), int(0.8 * QN))
        b_curr += dur
    mf.add_track(t2)

    # Synth Bass
    t3 = MidiTrack("Punchy Synth Bass")
    t3.program_change(2, 38, 0)
    roots = [41, 38, 34, 36] * 2
    for idx, r in enumerate(roots):
        b_pos = idx * 4
        for e in range(8):
            t3.note(2, r, 95 if e % 2 == 0 else 80, int((b_pos + e * 0.5) * QN), int(0.4 * QN))
    mf.add_track(t3)

    # Pop Drums
    t4 = MidiTrack("Idol Pop Kit")
    for b in range(0, 8, 4):
        add_drum_pattern(t4, "pop", b, bars=4)
    mf.add_track(t4)
    return mf


# 25. Cybernetic Vow (140 BPM, B Minor)
def make_cybernetic_vow():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(140, 0)
    t0.copyright("(c) 1987 Orion Euro-Synthwave")
    mf.add_track(t0)

    # High Saw Lead
    t1 = MidiTrack("Sawtooth Lead")
    t1.program_change(0, 81, 0)
    melody = [
        (0.0, 1.5, 71), (1.5, 0.5, 74), (2.0, 2.0, 76), (4.0, 2.0, 74), (6.0, 2.0, 71),
        (8.0, 1.5, 71), (9.5, 0.5, 74), (10.0, 2.0, 78), (12.0, 2.0, 76), (14.0, 2.0, 74),
        (16.0, 2.0, 79), (18.0, 2.0, 78), (20.0, 2.0, 76), (22.0, 2.0, 74),
        (24.0, 4.0, 71),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 110, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Brass Stabs
    t2 = MidiTrack("Synth Brass")
    t2.program_change(1, 62, 0)
    for b in range(8):
        b_pos = b * 4
        t2.chord(1, [59, 62, 66, 71], 100, int((b_pos + 1.5) * QN), int(0.4 * QN))
        t2.chord(1, [59, 62, 66, 71], 110, int((b_pos + 3.5) * QN), int(0.4 * QN))
    mf.add_track(t2)

    # Fast 16th Bass
    t3 = MidiTrack("Italo Bass")
    t3.program_change(2, 38, 0)
    roots = [35, 31, 33, 35] * 2
    for idx, r in enumerate(roots):
        b_pos = idx * 4
        for s in range(16):
            p = r if s % 2 == 0 else r + 12
            t3.note(2, p, 100 if s % 4 == 0 else 85, int((b_pos + s * 0.25) * QN), int(0.2 * QN))
    mf.add_track(t3)

    # Italo Drums
    t4 = MidiTrack("Italo Disco Kit")
    for b in range(0, 8, 4):
        add_drum_pattern(t4, "italo", b, bars=4)
    mf.add_track(t4)
    return mf


# 26. Whispers at Midnight (92 BPM, E Major)
def make_whispers_at_midnight():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(92, 0)
    t0.copyright("(c) 1985 Orion Records / Akasaka Late Night")
    mf.add_track(t0)

    # Vibraphone
    t1 = MidiTrack("Vibraphone")
    t1.program_change(0, 11, 0)
    melody = [
        (0.0, 1.5, 64), (1.5, 0.5, 68), (2.0, 1.0, 71), (3.0, 1.0, 73),
        (4.0, 2.0, 71), (6.0, 2.0, 68),
        (8.0, 1.5, 64), (9.5, 0.5, 68), (10.0, 1.0, 71), (11.0, 1.0, 75),
        (12.0, 2.0, 73), (14.0, 2.0, 71),
        (16.0, 4.0, 64),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 100, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Jazz Rhodes
    t2 = MidiTrack("Rhodes 9th Chords")
    t2.program_change(1, 4, 0)
    chords = [([52, 59, 63, 66], 4), ([49, 56, 61, 64], 4), ([47, 54, 59, 63], 4), ([45, 52, 57, 61], 4)]
    b_curr = 0.0
    for ch_notes, dur in chords:
        t2.chord(1, ch_notes, 80, int(b_curr * QN), int(dur * QN * 0.9))
        b_curr += dur
    mf.add_track(t2)

    # Finger Bass
    t3 = MidiTrack("Finger Bass")
    t3.program_change(2, 33, 0)
    roots = [28, 25, 23, 21]
    for idx, r in enumerate(roots):
        b_pos = idx * 4
        t3.note(2, r, 90, int(b_pos * QN), int(2.0 * QN))
        t3.note(2, r + 7, 80, int((b_pos + 2.5) * QN), int(1.0 * QN))
    mf.add_track(t3)

    # Smooth Drums
    t4 = MidiTrack("Smooth Kit")
    add_drum_pattern(t4, "ballad", 0, bars=4)
    mf.add_track(t4)
    return mf


# 27. Kamome Packet Radio (118 BPM, A Minor)
def make_kamome_packet_radio():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(118, 0)
    t0.copyright("(c) 1986 Kamome-Net Telemetry")
    mf.add_track(t0)

    # Square Chiptune Lead
    t1 = MidiTrack("Square Wave Lead")
    t1.program_change(0, 80, 0)
    melody = [
        (0.0, 0.5, 69), (0.5, 0.5, 72), (1.0, 1.0, 71), (2.0, 1.0, 69), (3.0, 1.0, 67),
        (4.0, 1.5, 69), (5.5, 0.5, 72), (6.0, 2.0, 74),
        (8.0, 0.5, 76), (8.5, 0.5, 74), (9.0, 1.0, 72), (10.0, 1.0, 71), (11.0, 1.0, 69),
        (12.0, 4.0, 69),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 105, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Fast Arpeggio
    t2 = MidiTrack("Chiptune Arp")
    t2.program_change(1, 80, 0)
    arp_notes = [69, 72, 76, 81]
    for b in range(16):
        for s in range(4):
            t2.note(1, arp_notes[(b * 4 + s) % 4], 80, int((b + s * 0.25) * QN), int(0.2 * QN))
    mf.add_track(t2)

    # Bass
    t3 = MidiTrack("Synth Bass")
    t3.program_change(2, 38, 0)
    for b in range(4):
        b_pos = b * 4
        for s in range(8):
            t3.note(2, 33, 95 if s % 2 == 0 else 75, int((b_pos + s * 0.5) * QN), int(0.4 * QN))
    mf.add_track(t3)

    # Drums
    t4 = MidiTrack("LinnDrum")
    add_drum_pattern(t4, "outrun", 0, bars=4)
    mf.add_track(t4)
    return mf


# 28. Satellite Intercept '89 (105 BPM, D Minor)
def make_satellite_intercept():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(105, 0)
    t0.copyright("(c) 1989 Classified Telemetry")
    mf.add_track(t0)

    # FM Bell Lead
    t1 = MidiTrack("FM Bells")
    t1.program_change(0, 98, 0)
    melody = [
        (0.0, 2.0, 74), (2.0, 1.0, 77), (3.0, 1.0, 76), (4.0, 3.0, 74),
        (8.0, 2.0, 70), (10.0, 1.0, 72), (11.0, 1.0, 74), (12.0, 4.0, 69),
        (16.0, 4.0, 62),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 100, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Dark Pad
    t2 = MidiTrack("Dark Synth Pad")
    t2.program_change(1, 50, 0)
    chords = [([50, 57, 62, 65], 4), ([46, 53, 58, 62], 4), ([43, 50, 55, 58], 4), ([45, 52, 57, 60], 4)]
    b_curr = 0.0
    for ch_notes, dur in chords:
        t2.chord(1, ch_notes, 75, int(b_curr * QN), int(dur * QN))
        b_curr += dur
    mf.add_track(t2)

    # Sub Bass
    t3 = MidiTrack("Sub Bass")
    t3.program_change(2, 38, 0)
    roots = [26, 22, 19, 21]
    for idx, r in enumerate(roots):
        t3.note(2, r, 100, int(idx * 4 * QN), int(3.8 * QN))
    mf.add_track(t3)

    # Drums
    t4 = MidiTrack("Ambient Drums")
    add_drum_pattern(t4, "ballad", 0, bars=4)
    mf.add_track(t4)
    return mf


# 29. Stardust Memory Reprise (70 BPM, C Minor)
def make_stardust_memory_reprise():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(70, 0)
    t0.copyright("(c) 1989 Orion Records Grand Finale")
    mf.add_track(t0)

    # Solo Violin / Flute
    t1 = MidiTrack("Solo Violin")
    t1.program_change(0, 40, 0)
    melody = [
        (0.0, 2.0, 60), (2.0, 1.0, 63), (3.0, 1.0, 67), (4.0, 3.0, 70), (7.0, 1.0, 72),
        (8.0, 2.0, 75), (10.0, 1.0, 74), (11.0, 1.0, 72), (12.0, 4.0, 74),
        (16.0, 2.0, 72), (18.0, 1.0, 70), (19.0, 1.0, 67), (20.0, 3.0, 63), (23.0, 1.0, 62),
        (24.0, 6.0, 60),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 105, int(beat * QN), int(dur * QN * 0.98))
    mf.add_track(t1)

    # Acoustic Grand Piano
    t2 = MidiTrack("Grand Piano")
    t2.program_change(1, 0, 0)
    chords = [([48, 55, 60, 63], 4), ([44, 51, 56, 60], 4), ([41, 48, 53, 56], 4), ([43, 50, 55, 58], 4)] * 2
    b_curr = 0.0
    for ch_notes, dur in chords:
        for a_idx, p in enumerate(ch_notes):
            t2.note(1, p, 85, int((b_curr + a_idx * 0.5) * QN), int(3.5 * QN))
        b_curr += dur
    mf.add_track(t2)

    # String Orchestra
    t3 = MidiTrack("Orchestral Strings")
    t3.program_change(2, 48, 0)
    b_curr = 0.0
    for ch_notes, dur in chords:
        t3.chord(2, [p + 12 for p in ch_notes], 75, int(b_curr * QN), int(dur * QN))
        b_curr += dur
    mf.add_track(t3)

    # Acoustic Bass
    t4 = MidiTrack("Acoustic Bass")
    t4.program_change(3, 32, 0)
    roots = [36, 32, 29, 31] * 2
    for idx, r in enumerate(roots):
        t4.note(3, r, 95, int(idx * 4 * QN), int(3.5 * QN))
    mf.add_track(t4)

    # Ballad Timpani
    t5 = MidiTrack("Timpani & Drums")
    add_drum_pattern(t5, "ballad", 0, bars=4)
    add_drum_pattern(t5, "ballad", 4, bars=4)
    mf.add_track(t5)
    return mf


# 30. Electric Mirage (126 BPM, Eb Major)
def make_electric_mirage():
    mf = MidiFile(division=QN)
    t0 = MidiTrack("Conductor")
    t0.set_tempo(126, 0)
    t0.copyright("(c) 1985 Orion Records Dream Pop")
    mf.add_track(t0)

    # Lead Synth
    t1 = MidiTrack("Dream Lead")
    t1.program_change(0, 81, 0)
    melody = [
        (0.0, 1.0, 63), (1.0, 0.5, 67), (1.5, 0.5, 70), (2.0, 1.5, 72), (3.5, 0.5, 70),
        (4.0, 2.0, 67), (6.0, 2.0, 63),
        (8.0, 1.0, 63), (9.0, 0.5, 67), (9.5, 0.5, 70), (10.0, 1.5, 75), (11.5, 0.5, 74),
        (12.0, 2.0, 72), (14.0, 2.0, 70),
        (16.0, 4.0, 63),
    ]
    for beat, dur, pitch in melody:
        t1.note(0, pitch, 105, int(beat * QN), int(dur * QN * 0.95))
    mf.add_track(t1)

    # Chorus E.Piano
    t2 = MidiTrack("Chorus E.Piano")
    t2.program_change(1, 4, 0)
    chords = [([51, 58, 63, 67], 4), ([48, 55, 60, 63], 4), ([44, 51, 56, 60], 4), ([46, 53, 58, 62], 4)]
    b_curr = 0.0
    for ch_notes, dur in chords:
        for s in (0.0, 1.5, 2.5):
            t2.chord(1, ch_notes, 85, int((b_curr + s) * QN), int(0.8 * QN))
        b_curr += dur
    mf.add_track(t2)

    # Synth Bass
    t3 = MidiTrack("Synth Bass")
    t3.program_change(2, 38, 0)
    roots = [39, 36, 32, 34]
    for idx, r in enumerate(roots):
        b_pos = idx * 4
        for e in range(8):
            t3.note(2, r, 95 if e % 2 == 0 else 80, int((b_pos + e * 0.5) * QN), int(0.4 * QN))
    mf.add_track(t3)

    # Drums
    t4 = MidiTrack("Dream Pop Kit")
    add_drum_pattern(t4, "pop", 0, bars=4)
    mf.add_track(t4)
    return mf


NEW_COMPOSITIONS = [
    ("neon_corridor_88", "Neon Corridor '88 (ネオン・コリドー)", make_neon_corridor),
    ("tokyo_twilight_express", "Tokyo Twilight Express (トワイライト・エキスプレス)", make_tokyo_twilight),
    ("orion_subroutine_142", "Orion Subroutine 142 (サブルーチン142)", make_orion_subroutine),
    ("signal_fading_in_the_fog", "Signal Fading in the Fog (霧の中の信号)", make_signal_fading),
    ("analog_heartbeat_1984", "Analog Heartbeat 1984 (アナログ・ハートビート)", make_analog_heartbeat),
    ("cybernetic_vow", "Cybernetic Vow (サイバネティックの誓い)", make_cybernetic_vow),
    ("whispers_at_midnight", "Whispers at Midnight (真夜中の囁き)", make_whispers_at_midnight),
    ("kamome_packet_radio", "Kamome Packet Radio (かもめパケットラジオ)", make_kamome_packet_radio),
    ("satellite_intercept_89", "Satellite Intercept '89 (衛星通信傍受)", make_satellite_intercept),
    ("stardust_memory_reprise", "Stardust Memory Reprise (スターダスト・メモリー)", make_stardust_memory_reprise),
    ("electric_mirage", "Electric Mirage (エレクトリック・ミラージュ)", make_electric_mirage),
]


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dirs = [
        os.path.join(root, "assets", "midi"),
        os.path.join(root, "site", "assets", "midi"),
        os.path.join(root, "site", "ftp", "kamome", "midi"),
    ]
    for d in target_dirs:
        os.makedirs(d, exist_ok=True)

    print(f"Generating 11 Extended MIDI Tracks (Catalog expansion to 30 tracks)...")
    for slug, title, fn in NEW_COMPOSITIONS:
        mf = fn()
        for d in target_dirs:
            path = os.path.join(d, f"{slug}.mid")
            mf.write(path)
        sz = os.path.getsize(os.path.join(target_dirs[0], f"{slug}.mid"))
        print(f"  ✓ {slug:<28} ({sz:>5d} B) - {title}")

    print("Successfully expanded MIDI catalog to 30 compositions!")


if __name__ == "__main__":
    main()
