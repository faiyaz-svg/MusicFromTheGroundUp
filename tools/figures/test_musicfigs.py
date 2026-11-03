import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import re
import tempfile
import unittest
import xml.etree.ElementTree as ET

import musicfigs as mf


def parse(svg):
    return ET.fromstring(svg)


class Helpers(unittest.TestCase):
    def test_note_to_midi(self):
        self.assertEqual(mf.note_to_midi("C4"), 60)
        self.assertEqual(mf.note_to_midi("C#4"), 61)
        self.assertEqual(mf.note_to_midi("Db4"), 61)
        self.assertEqual(mf.note_to_midi("A0"), 21)
        self.assertEqual(mf.note_to_midi("C8"), 108)
        self.assertEqual(mf.note_to_midi("E#4"), mf.note_to_midi("F4"))
        self.assertEqual(mf.note_to_midi("Cb4"), mf.note_to_midi("B3"))

    def test_midi_to_name(self):
        self.assertEqual(mf.midi_to_name(61), "C#4")
        self.assertEqual(mf.midi_to_name(61, prefer="flat"), "Db4")
        self.assertEqual(mf.midi_to_name(60), "C4")
        self.assertEqual(mf.midi_to_name(21), "A0")

    def test_guitar_note(self):
        self.assertEqual(mf.note_to_midi(mf.guitar_note(6, 0)), 40)
        self.assertEqual(mf.guitar_note(6, 0), "E2")
        self.assertEqual(mf.note_to_midi(mf.guitar_note(1, 0)), 64)
        self.assertEqual(mf.guitar_note(1, 0), "E4")
        self.assertEqual(mf.guitar_note(5, 3), "C3")
        self.assertEqual(mf.guitar_note(2, 1), "C4")


class Keyboard(unittest.TestCase):
    def black_xs(self, svg):
        root = parse(svg)
        ns = "{http://www.w3.org/2000/svg}"
        rects = [r for r in root.iter(ns + "rect") if r.get("fill") == "#111"]
        return sorted(float(r.get("x")) + float(r.get("width")) / 2 for r in rects)

    def test_black_key_count_and_groups(self):
        xs = self.black_xs(mf.keyboard("C4", "B4"))
        self.assertEqual(len(xs), 5)
        gaps = [round(b - a) for a, b in zip(xs, xs[1:])]
        # groups of 2 then 3: gap, big gap, gap, gap
        self.assertEqual(gaps[1] > gaps[0] and gaps[0] == gaps[2] == gaps[3], True)

    def test_88_keys(self):
        svg = mf.keyboard("A0", "C8", middle_c=True)
        self.assertEqual(len(self.black_xs(svg)), 36)
        self.assertIn("middle C", svg)

    def test_sharp_is_black_and_e_sharp_is_f(self):
        a = mf.keyboard("C4", "C5", marks=["C#4"])
        self.assertIn('fill="#fed134"', a)
        root = parse(a)
        ns = "{http://www.w3.org/2000/svg}"
        marked = [r for r in root.iter(ns + "rect") if r.get("fill") == "#fed134"]
        self.assertEqual(len(marked), 1)
        self.assertEqual(float(marked[0].get("height")) < 100, True)  # short = black key
        # E#4 fills the same white key as F4
        e = mf.keyboard("C4", "C5", marks=["E#4"])
        f = mf.keyboard("C4", "C5", marks=["F4"])
        self.assertEqual(e.replace("E#4", "F4"), f.replace("E#4", "F4"))
        self.assertEqual(mf.keyboard("C4", "C5", marks=["Db4"]), a)

    def test_options_parse(self):
        parse(mf.keyboard("C4", "C5", marks=["C4"], fingers={"C4": 1, "D4": 2},
                          labels={"E4": "Mi"}, colours={"G4": "teal"},
                          show_names=True, middle_c=True))

    def test_bad_start(self):
        with self.assertRaises(ValueError):
            mf.keyboard("C#4", "C5")


class Guitar(unittest.TestCase):
    def test_chord_parses(self):
        parse(mf.chord_diagram("Em", [0, 2, 2, 0, 0, 0], [None, 2, 3, None, None, None]))
        parse(mf.chord_diagram("F", [1, 3, 3, 2, 1, 1], [1, 3, 4, 2, 1, 1], barre=(1, 6, 1)))
        svg = mf.chord_diagram("Bm", ["x", 2, 4, 4, 3, 2], barre=(2, 5, 1), base_fret=2)
        parse(svg)
        self.assertIn("2fr", svg)

    def test_chord_low_e_on_left(self):
        svg = mf.chord_diagram("G", [3, 2, 0, 0, 0, 3])
        root = parse(svg)
        ns = "{http://www.w3.org/2000/svg}"
        dots = sorted(float(c.get("cx")) for c in root.iter(ns + "circle")
                      if c.get("fill") == "#111")
        # frets 3 and 2 on string 6 and 5 are leftmost; fret 3 on string 1 rightmost
        self.assertEqual(len(dots), 3)
        self.assertLess(dots[0], dots[1])
        self.assertLess(dots[1], dots[2])

    def test_fretboard(self):
        marks = [{"string": 1, "fret": 0, "label": "E", "colour": "teal"},
                 {"string": 6, "fret": 12, "label": "E"}]
        svg = mf.fretboard(12, marks=marks, show_names=True, highlight_strings=[3])
        parse(svg)
        parse(mf.fretboard(7, start_fret=5))


class Staff(unittest.TestCase):
    def test_staff(self):
        for args in (("C4",), ("F3", "bass"), ("A5",), ("A2", "bass"), ("C6",),
                     ("F#4",), ("Bb3", "bass")):
            svg = mf.staff_note(*args)
            root = parse(svg)
            self.assertTrue(root.get("viewBox"))
            self.assertEqual(root.get("role"), "img")

    def test_grand(self):
        parse(mf.staff_note_grand("C4"))
        parse(mf.staff_note_grand("G2"))


class Save(unittest.TestCase):
    def test_save(self):
        old = mf.FIG_ROOT
        with tempfile.TemporaryDirectory() as d:
            mf.FIG_ROOT = pathlib.Path(d)
            try:
                p = mf.save(mf.keyboard(), "a/b/k.svg")
                data = p.read_bytes()
                self.assertNotIn(b"\r", data)
                parse(data.decode())
            finally:
                mf.FIG_ROOT = old


if __name__ == "__main__":
    unittest.main()
