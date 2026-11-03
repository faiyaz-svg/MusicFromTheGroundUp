"""Tests for anki/build_decks.py.

Run from the repo root:

    .venv/Scripts/python anki/test_build_decks.py
"""

import contextlib
import io
import json
import sqlite3
import sys
import tempfile
import unittest
import zipfile
from contextlib import closing
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import genanki  # noqa: E402

import build_decks as bd  # noqa: E402
from build_decks import MathError, convert_math  # noqa: E402

HEADER = "id\tfront\tback\ttags\n"


def open_collection(apkg: bytes) -> sqlite3.Connection:
    with zipfile.ZipFile(io.BytesIO(apkg)) as zf:
        db = zf.read("collection.anki2")
    conn = sqlite3.connect(":memory:")
    conn.deserialize(db)
    return conn


class ConvertMathTest(unittest.TestCase):
    def test_no_math_is_unchanged(self):
        self.assertEqual(convert_math("Plain text, no math."), "Plain text, no math.")

    def test_inline(self):
        self.assertEqual(convert_math("$x^2$"), r"\(x^2\)")

    def test_several_inline_spans(self):
        self.assertEqual(
            convert_math("If $a = 1$ and $b = 2$, then $a + b = 3$."),
            r"If \(a = 1\) and \(b = 2\), then \(a + b = 3\).")

    def test_punctuation_next_to_math(self):
        self.assertEqual(convert_math("($x$), $y$; $z$. $-3$!"),
                         r"(\(x\)), \(y\); \(z\). \(-3\)!")

    def test_adjacent_spans(self):
        self.assertEqual(convert_math("$a$$b$"), r"\(a\)\(b\)")

    def test_money(self):
        self.assertEqual(convert_math(r"It costs \$5, or \$12.50 (with tax)."),
                         "It costs $5, or $12.50 (with tax).")

    def test_money_and_math_together(self):
        self.assertEqual(convert_math(r"Pay \$5 for each of $n$ items: \$$5n$ in total."),
                         r"Pay $5 for each of \(n\) items: $\(5n\) in total.")

    def test_escaped_dollar_inside_math_stays_escaped(self):
        self.assertEqual(convert_math(r"$\$5 + x$"), r"\(\$5 + x\)")

    def test_display(self):
        self.assertEqual(convert_math("Sum: $$a + b$$ done"), r"Sum: \[a + b\] done")

    def test_display_then_inline(self):
        self.assertEqual(convert_math("$$x = 1$$ so $x$ is odd"),
                         r"\[x = 1\] so \(x\) is odd")

    def test_display_with_aligned(self):
        src = r"$$\begin{aligned} a &= b \\ c &= d \end{aligned}$$"
        self.assertEqual(convert_math(src),
                         r"\[\begin{aligned} a &amp;= b \\ c &amp;= d \end{aligned}\]")

    def test_html_special_characters_inside_math_are_escaped(self):
        self.assertEqual(convert_math("$a < b > c$"), r"\(a &lt; b &gt; c\)")

    def test_html_outside_math_is_kept(self):
        self.assertEqual(convert_math("Line one<br>$x$ and <code>0x1F</code>"),
                         r"Line one<br>\(x\) and <code>0x1F</code>")

    def test_other_backslashes_are_kept(self):
        self.assertEqual(convert_math(r"$\frac{1}{2}$ and a \ b"),
                         r"\(\frac{1}{2}\) and a \ b")

    def test_escaped_backslash_before_dollar_inside_math(self):
        # \\ is a LaTeX line break, so the $ after it closes the math.
        self.assertEqual(convert_math(r"$a \\$"), r"\(a \\\)")

    def test_unclosed_inline(self):
        with self.assertRaisesRegex(MathError, "column 1 is never closed"):
            convert_math("$x + 1")

    def test_odd_number_of_dollars(self):
        with self.assertRaisesRegex(MathError, "column 9 is never closed"):
            convert_math("$x$ and $y")

    def test_escaped_dollar_cannot_close_math(self):
        with self.assertRaises(MathError):
            convert_math(r"$x\$")

    def test_unclosed_display(self):
        with self.assertRaisesRegex(MathError, r"\$\$ at column 3 is never closed"):
            convert_math("a $$x + 1")

    def test_single_dollar_inside_display(self):
        with self.assertRaisesRegex(MathError, "single"):
            convert_math("$$a $ b$$")

    def test_empty_math(self):
        for src in ("$ $", "$$$$", "a $$ $$ b"):
            with self.subTest(src=src), self.assertRaisesRegex(MathError, "empty"):
                convert_math(src)


class DeckNamingTest(unittest.TestCase):
    def test_deck_names(self):
        self.assertEqual(bd.deck_name("06-cs-math"), "Math From the Ground Up::06 CS math")
        self.assertEqual(bd.deck_name("02-middle-school"),
                         "Math From the Ground Up::02 Middle school")
        self.assertEqual(bd.deck_name("99-extra"), "Math From the Ground Up::99-extra")

    def test_deck_ids_are_stable_and_in_range(self):
        ids = {stem: bd.deck_id(stem) for stem in bd.FOLDER_TITLES}
        for value in ids.values():
            self.assertTrue((1 << 30) <= value < (1 << 31))
        self.assertEqual(len(set(ids.values())), len(ids))
        self.assertEqual(bd.deck_id("06-cs-math"), bd.deck_id("06-cs-math"))
        self.assertTrue((1 << 30) <= bd.MODEL_ID < (1 << 31))


class ReadCardsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, body, name="06-cs-math.tsv", header=HEADER):
        path = self.dir / name
        path.write_text(header + body, encoding="utf-8", newline="\n")
        return path

    def errors_for(self, body, **kwargs):
        _, errors = bd.read_cards(self.write(body, **kwargs))
        return errors

    def test_valid_file(self):
        cards, errors = bd.read_cards(self.write(
            "a-one\tWhat is $2^3$?\t8\tpowers-of-two\n"
            "\n"
            "# a comment line\n"
            "a-two\tCost?\t\\$5\t\n"))
        self.assertEqual(errors, [])
        self.assertEqual([c.id for c in cards], ["a-one", "a-two"])
        self.assertEqual(cards[0].front, r"What is \(2^3\)?")
        self.assertEqual(cards[0].tags, ["powers-of-two", "06-cs-math"])
        self.assertEqual(cards[1].back, "$5")
        self.assertEqual(cards[1].tags, ["06-cs-math"])
        self.assertEqual(cards[1].line, 5)

    def test_quotes_are_ordinary_characters(self):
        cards, errors = bd.read_cards(self.write('q\tWhat is "base"?\tThe "radix".\t\n'))
        self.assertEqual(errors, [])
        self.assertEqual(cards[0].front, 'What is "base"?')

    def test_byte_order_mark_is_accepted(self):
        path = self.dir / "bom.tsv"
        path.write_text(HEADER + "a\tb\tc\t\n", encoding="utf-8-sig")
        self.assertEqual(bd.read_cards(path)[1], [])

    def test_bad_header(self):
        errors = self.errors_for("a\tb\tc\t\n", header="id\tquestion\tanswer\ttags\n")
        self.assertEqual(len(errors), 1)
        self.assertIn("06-cs-math.tsv:1: header", errors[0])

    def test_duplicate_id(self):
        errors = self.errors_for("same\tA\tB\t\nother\tC\tD\t\nsame\tE\tF\t\n")
        self.assertEqual(len(errors), 1)
        self.assertIn(":4: duplicate id 'same' (first used on line 2)", errors[0])

    def test_empty_front_and_back(self):
        errors = self.errors_for("a\t\tB\t\nb\tA\t  \t\n")
        self.assertEqual(len(errors), 2)
        self.assertIn(":2: front is empty", errors[0])
        self.assertIn(":3: back is empty", errors[1])

    def test_wrong_column_count(self):
        errors = self.errors_for("a\tA\tB\nb\tA\tB\tt\textra\n")
        self.assertEqual(len(errors), 2)
        self.assertIn(":2: expected 4 tab-separated columns", errors[0])
        self.assertIn("found 3", errors[0])
        self.assertIn(":3: expected 4", errors[1])
        self.assertIn("found 5", errors[1])

    def test_unbalanced_dollar(self):
        errors = self.errors_for("ok\tA\tB\t\nbad\tWhat is $x?\tB\t\nm\tA\tCosts $5\t\n")
        self.assertEqual(len(errors), 2)
        self.assertIn("06-cs-math.tsv:3: front: $ at column 9 is never closed", errors[0])
        self.assertIn("06-cs-math.tsv:4: back:", errors[1])

    def test_bad_id(self):
        errors = self.errors_for("Bad Id\tA\tB\t\n")
        self.assertEqual(len(errors), 1)
        self.assertIn("must be a lowercase slug", errors[0])

    def test_bad_tag(self):
        errors = self.errors_for("a\tA\tB\tok bad,tag\n")
        self.assertEqual(len(errors), 1)
        self.assertIn("tag 'bad,tag'", errors[0])

    def test_invalid_html_outside_math(self):
        errors = self.errors_for("a\tIs 3 < 5 and 7 > 2?\tYes\t\n")
        self.assertEqual(len(errors), 1)
        self.assertIn("invalid HTML", errors[0])
        self.assertEqual(self.errors_for("a\tIs $3 < 5$ and $7 > 2$?\tYes\t\n"), [])


class BuildTest(unittest.TestCase):
    TSV = (HEADER
           + "c-one\tWhat is $2^{10}$?\t1024\tpowers-of-two\n"
           + "c-two\tShow a sum.\t$$1 + 1 = 2$$\t\n"
           + "c-three\tPrice?\t\\$3\t\n")

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.cards_dir = self.dir / "cards"
        self.out_dir = self.dir / "out"
        self.cards_dir.mkdir()
        (self.cards_dir / "06-cs-math.tsv").write_text(self.TSV, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def run_main(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = bd.main(["--cards", str(self.cards_dir), "--out", str(self.out_dir)])
        return code, out.getvalue(), err.getvalue()

    def test_package_contents(self):
        cards, _ = bd.read_cards(self.cards_dir / "06-cs-math.tsv")
        apkg = bd.build_apkg("06-cs-math", cards, 1_700_000_000)
        with closing(open_collection(apkg)) as conn:
            notes = conn.execute("SELECT guid, flds, tags FROM notes ORDER BY id").fetchall()
            decks = json.loads(conn.execute("SELECT decks FROM col").fetchone()[0])
            models = json.loads(conn.execute("SELECT models FROM col").fetchone()[0])
            card_rows = conn.execute("SELECT did, due FROM cards ORDER BY id").fetchall()
        self.assertEqual([n[0] for n in notes],
                         [genanki.guid_for("06-cs-math", i) for i in ("c-one", "c-two", "c-three")])
        fields = [n[1].split("\x1f") for n in notes]
        self.assertEqual(fields[0], [r"What is \(2^{10}\)?", "1024", "06 CS math"])
        self.assertEqual(fields[1][1], r"\[1 + 1 = 2\]")
        self.assertEqual(fields[2][1], "$3")
        self.assertEqual(notes[0][2].split(), ["powers-of-two", "06-cs-math"])
        deck = decks[str(bd.deck_id("06-cs-math"))]
        self.assertEqual(deck["name"], "Math From the Ground Up::06 CS math")
        model = models[str(bd.MODEL_ID)]
        self.assertEqual(model["name"], "Math From the Ground Up (basic)")
        self.assertEqual([f["name"] for f in model["flds"]], ["Front", "Back", "Source"])
        self.assertEqual(card_rows, [(bd.deck_id("06-cs-math"), i) for i in range(3)])

    def test_same_input_gives_same_bytes(self):
        cards, _ = bd.read_cards(self.cards_dir / "06-cs-math.tsv")
        self.assertEqual(bd.build_apkg("06-cs-math", cards, 1_700_000_000),
                         bd.build_apkg("06-cs-math", cards, 1_700_000_000))

    def test_write_deck_keeps_timestamp_until_content_changes(self):
        path = self.out_dir / "deck.apkg"
        self.out_dir.mkdir()
        cards, _ = bd.read_cards(self.cards_dir / "06-cs-math.tsv")
        self.assertTrue(bd.write_deck("06-cs-math", cards, path, now=1_700_000_000))
        first = path.read_bytes()
        self.assertFalse(bd.write_deck("06-cs-math", cards, path, now=1_800_000_000))
        self.assertEqual(path.read_bytes(), first)
        self.assertEqual(bd.previous_timestamp(first), 1_700_000_000)

        cards[0].back = "1024 (exactly)"
        self.assertTrue(bd.write_deck("06-cs-math", cards, path, now=1_800_000_000))
        self.assertEqual(bd.previous_timestamp(path.read_bytes()), 1_800_000_000)

    def test_main_builds_and_rebuilds(self):
        code, out, err = self.run_main()
        # stderr may hold a DeprecationWarning from genanki's cached_property
        # dependency (Python 3.14), so only check that no build error appears.
        self.assertEqual(code, 0)
        self.assertNotIn("error", err)
        self.assertIn("Math From the Ground Up::06 CS math: 3 cards ->", out)
        first = (self.out_dir / "06-cs-math.apkg").read_bytes()
        code, out, _ = self.run_main()
        self.assertEqual(code, 0)
        self.assertIn("(unchanged)", out)
        self.assertEqual((self.out_dir / "06-cs-math.apkg").read_bytes(), first)

    def test_main_reports_errors_and_writes_nothing(self):
        (self.cards_dir / "05-university-core.tsv").write_text(
            HEADER + "x\tWhat is $x?\tB\t\nx\tA\tB\t\n", encoding="utf-8")
        code, out, err = self.run_main()
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("05-university-core.tsv:2: front: $ at column 9 is never closed", err)
        self.assertIn("05-university-core.tsv:3: duplicate id 'x'", err)
        self.assertIn("2 error(s); no decks written.", err)
        self.assertFalse(self.out_dir.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
