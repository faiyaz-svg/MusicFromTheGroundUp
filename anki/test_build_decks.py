"""Tests for anki/build_decks.py. Run: .venv/Scripts/python -m unittest anki.test_build_decks"""

from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_decks as bd  # noqa: E402

SVG = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10"/></svg>'


class DeckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.cards = self.dir / "cards"
        self.media = self.dir / "media"
        self.out = self.dir / "out"
        self.cards.mkdir()
        self.media.mkdir()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, name: str, rows: list[str]) -> Path:
        path = self.cards / name
        path.write_text("\n".join(rows) + "\n", encoding="utf-8")
        return path

    def test_header_is_optional(self) -> None:
        with_header = self.write("a.tsv", ["id\tfront\tback\ttags", "c1\tMiddle C?\tC4\tnotes"])
        without = self.write("b.tsv", ["c1\tMiddle C?\tC4\tnotes"])
        for path in (with_header, without):
            cards, errors = bd.read_cards(path, self.media)
            self.assertEqual(errors, [])
            self.assertEqual([c.id for c in cards], ["c1"])

    def test_errors_are_reported(self) -> None:
        path = self.write("a.tsv", [
            "c1\tfront\tback\tt",
            "c1\tfront\tback\tt",
            "Bad_Id\tfront\tback\tt",
            "c2\tonly three\tcolumns",
            'c3\t<img src="mfgu-missing.svg">\tback\tt',
            'c4\t<img src="noprefix.svg">\tback\tt',
        ])
        cards, errors = bd.read_cards(path, self.media)
        text = "\n".join(errors)
        self.assertIn("duplicate id", text)
        self.assertIn("lowercase slug", text)
        self.assertIn("4 tab-separated columns", text)
        self.assertIn("is not in", text)
        self.assertIn("must be a bare file name", text)
        self.assertEqual([c.id for c in cards], ["c1"])

    def test_images_go_into_the_package(self) -> None:
        (self.media / "mfgu-c4.svg").write_bytes(SVG)
        path = self.write("a.tsv", ['c1\t<img src="mfgu-c4.svg">\tC4 (middle C)\tnotes'])
        cards, errors = bd.read_cards(path, self.media)
        self.assertEqual(errors, [])
        data = bd.build_apkg("a", cards, 1_700_000_000, self.media)
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            media = json.loads(zf.read("media"))
            self.assertEqual(media, {"0": "mfgu-c4.svg"})
            self.assertEqual(zf.read("0"), SVG)

    def test_rebuild_is_byte_identical(self) -> None:
        path = self.write("a.tsv", ["c1\tfront\tback\tt"])
        cards, _ = bd.read_cards(path, self.media)
        self.out.mkdir()
        target = self.out / "a.apkg"
        self.assertTrue(bd.write_deck("a", cards, target, now=1_700_000_000, media_dir=self.media))
        first = target.read_bytes()
        self.assertFalse(bd.write_deck("a", cards, target, now=1_800_000_000, media_dir=self.media))
        self.assertEqual(target.read_bytes(), first)

    def test_ids_are_stable(self) -> None:
        self.assertEqual(bd.deck_id("01-first-sounds"), bd.deck_id("01-first-sounds"))
        self.assertNotEqual(bd.deck_id("01-first-sounds"), bd.deck_id("09-harmony"))
        self.assertTrue((1 << 30) <= bd.deck_id("01-first-sounds") < (1 << 31))


if __name__ == "__main__":
    unittest.main()
