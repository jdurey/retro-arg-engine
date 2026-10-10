"""Standard MIDI File (SMF Format 1) generator in pure Python.

No external dependencies. Generates spec-compliant multi-track MIDI files
with conductor track, instrument patches, notes, markers, and percussion.
"""
import struct

def encode_vlq(val):
    """Encodes an integer into MIDI variable-length quantity bytes."""
    if val < 0:
        val = 0
    buf = [val & 0x7F]
    val >>= 7
    while val > 0:
        buf.append(0x80 | (val & 0x7F))
        val >>= 7
    buf.reverse()
    return bytes(buf)


class MidiTrack:
    def __init__(self, name=""):
        self.name = name
        self.events = []  # List of tuples: (tick, raw_bytes)
        if name:
            name_bytes = name.encode("ascii", "replace")
            self.events.append((0, b"\xFF\x03" + encode_vlq(len(name_bytes)) + name_bytes))

    def set_tempo(self, bpm, tick=0):
        """Sets tempo in beats per minute."""
        us_per_qn = int(60_000_000 / bpm)
        self.events.append((tick, b"\xFF\x51\x03" + struct.pack(">I", us_per_qn)[1:]))

    def set_time_signature(self, numerator=4, denominator=4, tick=0):
        """Sets time signature (e.g. 4/4)."""
        denom_pow = 2  # 2^2 = 4
        if denominator == 8:
            denom_pow = 3
        elif denominator == 2:
            denom_pow = 1
        self.events.append((tick, b"\xFF\x58\x04" + bytes([numerator, denom_pow, 24, 8])))

    def marker(self, text, tick=0):
        """Adds a section marker or cue."""
        text_bytes = text.encode("ascii", "replace")
        self.events.append((tick, b"\xFF\x06" + encode_vlq(len(text_bytes)) + text_bytes))

    def text(self, text, tick=0):
        """Adds a general text event."""
        text_bytes = text.encode("ascii", "replace")
        self.events.append((tick, b"\xFF\x01" + encode_vlq(len(text_bytes)) + text_bytes))

    def copyright(self, text, tick=0):
        """Adds a copyright notice."""
        text_bytes = text.encode("ascii", "replace")
        self.events.append((tick, b"\xFF\x02" + encode_vlq(len(text_bytes)) + text_bytes))

    def program_change(self, channel, program, tick=0):
        """Selects General MIDI instrument patch (0-127)."""
        self.events.append((tick, bytes([0xC0 | (channel & 0x0F), program & 0x7F])))

    def control_change(self, channel, controller, value, tick=0):
        """Sets MIDI control change (e.g. 7=Volume, 10=Pan, 91=Reverb)."""
        self.events.append((tick, bytes([0xB0 | (channel & 0x0F), controller & 0x7F, value & 0x7F])))

    def pitch_wheel(self, channel, value=8192, tick=0):
        """Sets pitch wheel (0-16383, 8192=center)."""
        lsb = value & 0x7F
        msb = (value >> 7) & 0x7F
        self.events.append((tick, bytes([0xE0 | (channel & 0x0F), lsb, msb])))

    def note_on(self, channel, pitch, velocity=100, tick=0):
        self.events.append((tick, bytes([0x90 | (channel & 0x0F), pitch & 0x7F, velocity & 0x7F])))

    def note_off(self, channel, pitch, tick=0):
        self.events.append((tick, bytes([0x80 | (channel & 0x0F), pitch & 0x7F, 0])))

    def note(self, channel, pitch, velocity, start_tick, dur_ticks):
        """Convenience method to schedule Note On and Note Off."""
        self.note_on(channel, pitch, velocity, start_tick)
        self.note_off(channel, pitch, start_tick + dur_ticks)

    def chord(self, channel, pitches, velocity, start_tick, dur_ticks):
        """Plays multiple notes simultaneously."""
        for p in pitches:
            self.note(channel, p, velocity, start_tick, dur_ticks)

    def build(self):
        """Assembles and returns MTrk chunk bytes with delta-times."""
        # Sort events by tick (stable sort maintains order of simultaneous events)
        sorted_evs = sorted(self.events, key=lambda x: x[0])
        track_bytes = bytearray()
        last_tick = 0
        for tick, ev_bytes in sorted_evs:
            delta = tick - last_tick
            track_bytes += encode_vlq(delta) + ev_bytes
            last_tick = tick
        # End of Track meta event
        track_bytes += encode_vlq(0) + b"\xFF\x2F\x00"
        return b"MTrk" + struct.pack(">I", len(track_bytes)) + bytes(track_bytes)


class MidiFile:
    def __init__(self, division=480):
        self.division = division  # Ticks per quarter note
        self.tracks = []

    def add_track(self, track):
        self.tracks.append(track)

    def write(self, path):
        """Writes Standard MIDI File Format 1 to disk."""
        header = b"MThd" + struct.pack(">IHHH", 6, 1, len(self.tracks), self.division)
        with open(path, "wb") as f:
            f.write(header)
            for t in self.tracks:
                f.write(t.build())
