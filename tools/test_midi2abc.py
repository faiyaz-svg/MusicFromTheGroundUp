"""Tests for midi2abc.py, built on tiny MIDI files written here (no files needed).

Run:  py -m unittest tools/test_midi2abc.py   (from the repository root)
"""
import io
import os
import struct
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import midi2abc  # noqa: E402

PPQ = 96  # ticks per quarter note in the test files


def vlq(n):
    out = [n & 0x7F]
    n >>= 7
    while n:
        out.append((n & 0x7F) | 0x80)
        n >>= 7
    return bytes(reversed(out))


def track(events):
    """events: list of (tick, bytes). Returns a track chunk."""
    events = sorted(events, key=lambda e: e[0])
    data = b""
    last = 0
    for tick, msg in events:
        data += vlq(tick - last) + msg
        last = tick
    data += vlq(0) + b"\xff\x2f\x00"
    return b"MTrk" + struct.pack(">I", len(data)) + data


def notes_track(notes):
    """notes: list of (start_quarters, length_quarters, midi_pitch)."""
    ev = []
    for start, length, pitch in notes:
        ev.append((int(start * PPQ), bytes([0x90, pitch, 80])))
        ev.append((int((start + length) * PPQ), bytes([0x80, pitch, 0])))
    return track(ev)


def make_midi(tracks, sig=(4, 4), key=(0, 0), bpm=100):
    meta = [
        (0, b"\xff\x51\x03" + (60000000 // bpm).to_bytes(3, "big")),
        (0, b"\xff\x58\x04" + bytes([sig[0], {2: 1, 4: 2, 8: 3}[sig[1]], 24, 8])),
        (0, b"\xff\x59\x02" + bytes([key[0] & 0xFF, key[1]])),
    ]
    chunks = [track(meta)] + tracks
    head = b"MThd" + struct.pack(">IHHH", 6, 1, len(chunks), PPQ)
    return midi2abc.MidiFile(head + b"".join(chunks))


def body_lines(text):
    return [l for l in text.splitlines() if l and not l[0] in "XTCMLQKV%"]


class Convert(unittest.TestCase):
    def test_single_voice(self):
        # bar 1: C5 D5 E5(half); bar 2: C5 whole
        midi = make_midi([notes_track([(0, 1, 72), (1, 1, 74), (2, 2, 76), (4, 4, 72)])])
        text = midi2abc.convert(midi, title="T", composer="C").text
        self.assertIn("M:4/4", text)
        self.assertIn("L:1/8", text)
        self.assertIn("Q:1/4=100", text)
        self.assertIn("K:C clef=treble", text)
        self.assertEqual(body_lines(text), ["c2 d2 e4 | c8 |]"])

    def test_piano_two_staves_and_chord(self):
        rh = notes_track([(0, 4, 72), (0, 4, 76), (0, 4, 79)])
        lh = notes_track([(0, 4, 48)])
        text = midi2abc.convert(make_midi([rh, lh])).text
        self.assertIn("%%score {RH LH}", text)
        self.assertIn("V:RH clef=treble", text)
        self.assertIn("V:LH clef=bass", text)
        self.assertIn("[ceg]8 |]", text)
        self.assertIn("C,8 |]", text)

    def test_spelling_follows_key(self):
        # G#4 in A minor, Bb4 in F major, F#4 in G major (already in the key signature)
        am = make_midi([notes_track([(0, 4, 68)])], key=(0, 1))
        self.assertIn("^G8", midi2abc.convert(am).text)
        f = make_midi([notes_track([(0, 4, 70)])], key=(-1, 0))
        self.assertIn("B8", midi2abc.convert(f).text)
        self.assertNotIn("_B", midi2abc.convert(f).text)
        g = make_midi([notes_track([(0, 4, 66)])], key=(1, 0))
        self.assertIn("F8", midi2abc.convert(g).text)
        # outside the key: B-flat in C major is spelled as a flat when asked
        c = make_midi([notes_track([(0, 4, 70)])])
        self.assertIn("_B8", midi2abc.convert(c, spell={10: ("B", -1)}).text)

    def test_key_override(self):
        midi = make_midi([notes_track([(0, 4, 66)])], key=(0, 0))
        self.assertIn("K:G", midi2abc.convert(midi, key="G").text)

    def test_tie_over_bar_line(self):
        # a half note starting on beat 4 crosses the bar line
        midi = make_midi([notes_track([(0, 3, 72), (3, 2, 74), (5, 3, 72)])])
        text = midi2abc.convert(midi).text
        self.assertEqual(body_lines(text), ["c6 d2- | d2 c6 |]"])

    def test_rests_and_beaming(self):
        midi = make_midi([notes_track([(1, 0.5, 72), (1.5, 0.5, 74), (3, 1, 72)])])
        lines = body_lines(midi2abc.convert(midi).text)
        self.assertEqual(lines, ["z2 cd z2 c2 |]"])

    def test_pickup(self):
        midi = make_midi([notes_track([(0, 1, 67), (1, 4, 72)])])
        text = midi2abc.convert(midi, pickup="1/4").text
        self.assertEqual(body_lines(text), ["G2 | c8 |]"])

    def test_repeat_signs_and_unfolded_repeat(self):
        bar = [(0, 1, 72), (1, 1, 74), (2, 2, 76)]
        once = notes_track(bar + [(4, 4, 72)])
        text = midi2abc.convert(make_midi([once]), sign_repeats=[(1, 1)]).text
        self.assertEqual(body_lines(text), ["|: c2 d2 e4 :| c8 |]"])
        twice = notes_track(bar + [(4 + s, l, p) for s, l, p in bar] + [(8, 4, 72)])
        text = midi2abc.convert(make_midi([twice]), repeats=[(1, 1)]).text
        self.assertEqual(body_lines(text), ["|: c2 d2 e4 :| c8 |]"])

    def test_unfolded_repeat_must_be_identical(self):
        notes = [(0, 4, 72), (4, 4, 74)]
        with self.assertRaises(midi2abc.ConvertError):
            midi2abc.convert(make_midi([notes_track(notes)]), repeats=[(1, 1)])

    def test_two_voices_in_one_staff(self):
        # melody quarter notes over a held half-note chord
        t = notes_track([(0, 1, 79), (1, 1, 81), (2, 2, 79), (1, 3, 64), (1, 3, 67)])
        piece = midi2abc.convert(make_midi([t]))
        self.assertEqual(len(piece.staves[0]), 2)

    def test_marks_file(self):
        import tempfile
        midi = make_midi([notes_track([(0, 1, 72), (1, 1, 74), (2, 2, 76)])])
        with tempfile.NamedTemporaryFile("w", suffix=".marks", delete=False, encoding="utf-8") as f:
            f.write('Melody 1 0 !p!\nMelody 1 0 (\nMelody 1 1/4 <)\nMelody 1 1/2 =76:Fb\n')
            path = f.name
        try:
            text = midi2abc.convert(midi, marks_path=path).text
        finally:
            os.unlink(path)
        self.assertEqual(body_lines(text), ["!p!(c2 d2) _f4 |]"])

    def test_grace_note_is_dropped_and_time_returned(self):
        # G (1 beat) with a short grace note stealing the end, then C
        ev = [(0, 1, 67), (0.9, 0.1, 71), (1, 1, 72)]
        midi = make_midi([notes_track(ev)])
        self.assertEqual(body_lines(midi2abc.convert(midi).text), ["G2 c2 z4 |]"])


class Check(unittest.TestCase):
    def setUp(self):
        self.midi = make_midi([notes_track([(0, 1, 72), (1, 1, 74), (2, 2, 76), (4, 4, 72)])])
        self.abc = midi2abc.convert(self.midi).text

    def run_check(self, abc):
        out = io.StringIO()
        return midi2abc.check(abc, self.midi, out=out), out.getvalue()

    def test_round_trip_matches(self):
        rc, out = self.run_check(self.abc)
        self.assertEqual(rc, 0, out)

    def test_wrong_pitch_is_reported(self):
        rc, out = self.run_check(self.abc.replace("d2", "e2"))
        self.assertEqual(rc, 1)
        self.assertIn("MISMATCH", out)

    def test_wrong_length_is_reported(self):
        rc, out = self.run_check(self.abc.replace("e4", "e2"))
        self.assertEqual(rc, 1)

    def test_accidentals_and_bar_state(self):
        midi = make_midi([notes_track([(0, 1, 68), (1, 1, 68), (2, 1, 69), (3, 1, 68), (4, 4, 68)])], key=(0, 1))
        abc = midi2abc.convert(midi).text
        self.assertIn("^G2 G2", abc)  # the accidental carries through the bar
        out = io.StringIO()
        self.assertEqual(midi2abc.check(abc, midi, out=out), 0, out.getvalue())

    def test_triplet(self):
        t = notes_track([(0, 1 / 3, 72), (1 / 3, 1 / 3, 74), (2 / 3, 1 / 3, 76), (1, 3, 72)])
        midi = make_midi([t])
        abc = midi2abc.convert(midi).text
        self.assertIn("(3c2d2e2", abc)
        out = io.StringIO()
        self.assertEqual(midi2abc.check(abc, midi, out=out), 0, out.getvalue())


class ReadMidi(unittest.TestCase):
    def test_header_values(self):
        midi = make_midi([notes_track([(0, 1, 60)])], sig=(3, 4), key=(-2, 0), bpm=90)
        self.assertEqual(midi.timesig, (3, 4))
        self.assertEqual(midi.keysig, (-2, False))
        self.assertEqual(midi.ppq, PPQ)
        self.assertEqual(round(60000000 / midi.tempo), 90)

    def test_rejects_non_midi(self):
        with self.assertRaises(midi2abc.ConvertError):
            midi2abc.MidiFile(b"not a midi file at all")


if __name__ == "__main__":
    unittest.main()
