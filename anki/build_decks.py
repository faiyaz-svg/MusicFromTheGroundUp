"""Build Anki decks from the card files in anki/cards/.

Each anki/cards/<stem>.tsv becomes docs/downloads/anki/<stem>.apkg, one deck
per book folder. Run it from the repo root:

    .venv/Scripts/python anki/build_decks.py

File format (see anki/README.md for the full rules):

- UTF-8, tab-separated, header row exactly: id<TAB>front<TAB>back<TAB>tags
- Every row has exactly 4 columns. A field can't contain a tab or a newline:
  write <br> for a line break. Quotes are ordinary characters.
- Blank lines and lines starting with # are skipped.
- Math is written as in the book: $...$ inline, $$...$$ display, and \\$ for a
  literal dollar sign. The build converts math to \\(...\\) and \\[...\\],
  which Anki's MathJax renders.

The build checks every file first and writes nothing if any file has an error.
Each error is printed as path:line: message, and the exit code is 1.

Re-importing an updated deck updates the cards in place, because each note's
GUID comes from the file stem and the card id. Anki only updates a note when
the file's copy is newer, so a deck whose content changed gets the current
time as its timestamp. A deck whose content did not change keeps its previous
timestamp, so rebuilding it gives a byte-identical file.

Needs Python 3.11 or later (sqlite3 serialize) and genanki 0.13.1.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import io
import itertools
import json
import re
import sqlite3
import sys
import time
import zipfile
from contextlib import closing
from dataclasses import dataclass, field
from pathlib import Path

import genanki

ROOT = Path(__file__).resolve().parent.parent
CARDS_DIR = ROOT / "anki" / "cards"
OUT_DIR = ROOT / "docs" / "downloads" / "anki"

BOOK_TITLE = "Math From the Ground Up"

# Readable deck titles for the book folders. Other stems are used as they are.
FOLDER_TITLES = {
    "00-start-here": "00 Start here",
    "01-elementary": "01 Elementary",
    "02-middle-school": "02 Middle school",
    "03-high-school": "03 High school",
    "04-proofs-and-logic": "04 Proofs and logic",
    "05-university-core": "05 University core",
    "06-cs-math": "06 CS math",
    "07-economics-math": "07 Economics math",
    "08-financial-math": "08 Financial math",
    "reference": "Reference",
}

# The note type is shared by every deck. Its ID must never change: Anki uses it
# to recognise the note type when a deck is imported again.
MODEL_ID = 1_581_934_517
MODEL_NAME = "Math From the Ground Up (basic)"

HEADER = ["id", "front", "back", "tags"]
ID_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
TAG_RE = re.compile(r"[A-Za-z0-9_-]+(?:::[A-Za-z0-9_-]+)*")

QUESTION_TEMPLATE = '<div class="front">{{Front}}</div>'
ANSWER_TEMPLATE = (
    "{{FrontSide}}\n"
    '<hr id="answer">\n'
    '<div class="back">{{Back}}</div>\n'
    '{{#Source}}<div class="source">{{Source}}</div>{{/Source}}'
)

CARD_CSS = """\
.card {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
  font-size: 20px;
  line-height: 1.5;
  text-align: left;
  color: #1f2328;
  background-color: #fbfbf8;
}
.front, .back, .source, hr#answer {
  max-width: 36em;
  margin-left: auto;
  margin-right: auto;
}
hr#answer {
  border: none;
  border-top: 1px solid #d0d0cc;
  margin-top: 1em;
  margin-bottom: 1em;
}
.source {
  margin-top: 1.5em;
  font-size: 14px;
  color: #66665f;
}
code {
  font-family: ui-monospace, "Cascadia Mono", Consolas, "Liberation Mono",
    monospace;
  font-size: 0.9em;
}
.card.nightMode, .card.night_mode, .nightMode .card, .night_mode .card {
  color: #e6e6e3;
  background-color: #1e1f22;
}
.nightMode hr#answer, .night_mode hr#answer {
  border-top-color: #46484c;
}
.nightMode .source, .night_mode .source {
  color: #a3a39d;
}
"""

# Fixed zip entry date, so identical content gives identical bytes.
ZIP_DATE = (1980, 1, 1, 0, 0, 0)


class MathError(ValueError):
    """A field has unbalanced or empty math delimiters."""


@dataclass
class Card:
    line: int
    id: str
    front: str  # already converted for Anki
    back: str
    tags: list[str] = field(default_factory=list)


# Math conversion


def _find_close(text: str, start: int, display: bool) -> int:
    """Return the index of the delimiter that closes math opened before `start`.

    A backslash escapes the next character, so \\$ inside math is a dollar sign
    and does not close it. Raises MathError if there is no closing delimiter.
    """
    i = start
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "$":
            if not display:
                return i
            if text.startswith("$$", i):
                return i
            raise MathError(
                f"single $ inside $$...$$ at column {i + 1} "
                "(write \\$ for a dollar sign)"
            )
        i += 1
    delim = "$$" if display else "$"
    raise MathError(f"{delim} at column {start - len(delim) + 1} is never closed")


def convert_math(text: str) -> str:
    """Convert book-style math to the delimiters Anki's MathJax uses.

    $$...$$ becomes \\[...\\] and $...$ becomes \\(...\\). Outside math, \\$
    becomes a literal $. Inside math, \\$ stays as it is (MathJax shows it as a
    dollar sign), and <, > and & are escaped for HTML, so write them directly.
    Raises MathError for unbalanced or empty math.
    """
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c == "\\" and i + 1 < n:
            nxt = text[i + 1]
            out.append("$" if nxt == "$" else c + nxt)
            i += 2
        elif c == "$":
            display = text.startswith("$$", i)
            width = 2 if display else 1
            start = i + width
            end = _find_close(text, start, display)
            body = text[start:end]
            if not body.strip():
                raise MathError(f"empty math at column {i + 1}")
            opener, closer = (r"\[", r"\]") if display else (r"\(", r"\)")
            out.append(opener + html.escape(body, quote=False) + closer)
            i = end + width
        else:
            out.append(c)
            i += 1
    return "".join(out)


# Reading and checking card files


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def folder_title(stem: str) -> str:
    return FOLDER_TITLES.get(stem, stem)


def deck_name(stem: str) -> str:
    return f"{BOOK_TITLE}::{folder_title(stem)}"


def deck_id(stem: str) -> int:
    """A stable deck ID in the range [2**30, 2**31), from the SHA-1 of the stem."""
    h = int(hashlib.sha1(stem.encode("utf-8")).hexdigest()[:8], 16)
    return (1 << 30) + h % (1 << 30)


def read_cards(path: Path) -> tuple[list[Card], list[str]]:
    """Read and check one card file. Returns (cards, errors)."""
    where = display_path(path)
    cards: list[Card] = []
    errors: list[str] = []
    first_line: dict[str, int] = {}

    try:
        raw = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        return [], [f"{where}: not valid UTF-8 ({exc})"]

    reader = csv.reader(io.StringIO(raw, newline=""), delimiter="\t",
                        quoting=csv.QUOTE_NONE)
    header = next(reader, None)
    if header != HEADER:
        return [], [f"{where}:1: header must be id, front, back, tags "
                    f"separated by tabs; found {header!r}"]

    for row in reader:
        line = reader.line_num
        if not row or (len(row) == 1 and not row[0].strip()):
            continue
        if row[0].startswith("#"):
            continue
        loc = f"{where}:{line}"
        if len(row) != 4:
            errors.append(f"{loc}: expected 4 tab-separated columns "
                          f"(id, front, back, tags), found {len(row)}")
            continue

        card_id, front, back, tags = (col.strip() for col in row)
        row_ok = True

        if not ID_RE.fullmatch(card_id):
            errors.append(f"{loc}: id {card_id!r} must be a lowercase slug "
                          "such as bases-hex-digit-values")
            row_ok = False
        elif card_id in first_line:
            errors.append(f"{loc}: duplicate id {card_id!r} "
                          f"(first used on line {first_line[card_id]})")
            row_ok = False
        else:
            first_line[card_id] = line

        converted = {}
        for name, value in (("front", front), ("back", back)):
            if not value:
                errors.append(f"{loc}: {name} is empty")
                row_ok = False
                continue
            try:
                converted[name] = convert_math(value)
            except MathError as exc:
                errors.append(f"{loc}: {name}: {exc}")
                row_ok = False
                continue
            bad_tags = genanki.Note._find_invalid_html_tags_in_field(converted[name])
            if bad_tags:
                errors.append(f"{loc}: {name}: invalid HTML {' '.join(bad_tags)!r} "
                              "(outside math, write < as &lt;)")
                row_ok = False

        tag_list = tags.split()
        for tag in tag_list:
            if not TAG_RE.fullmatch(tag):
                errors.append(f"{loc}: tag {tag!r} may only use letters, digits, "
                              "- and _ (and :: for nested tags)")
                row_ok = False

        if row_ok:
            all_tags = list(dict.fromkeys(tag_list + [path.stem]))
            cards.append(Card(line, card_id, converted["front"],
                              converted["back"], all_tags))

    return cards, errors


# Building packages


def make_model() -> genanki.Model:
    return genanki.Model(
        MODEL_ID,
        MODEL_NAME,
        fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Source"}],
        templates=[{"name": "Card 1", "qfmt": QUESTION_TEMPLATE,
                    "afmt": ANSWER_TEMPLATE}],
        css=CARD_CSS,
    )


def make_deck(stem: str, cards: list[Card]) -> genanki.Deck:
    title = folder_title(stem)
    deck = genanki.Deck(
        deck_id(stem),
        deck_name(stem),
        description=f"Flashcards for {title} in {BOOK_TITLE}.",
    )
    model = make_model()
    for position, card in enumerate(cards):
        deck.add_note(genanki.Note(
            model=model,
            fields=[card.front, card.back, title],
            tags=card.tags,
            guid=genanki.guid_for(stem, card.id),
            due=position,  # new cards come up in file order
        ))
    return deck


def build_apkg(stem: str, cards: list[Card], timestamp: int) -> bytes:
    """Return the .apkg file contents for one deck."""
    package = genanki.Package(make_deck(stem, cards))
    with closing(sqlite3.connect(":memory:")) as conn:
        cursor = conn.cursor()
        package.write_to_db(cursor, timestamp, itertools.count(timestamp * 1000))
        conn.commit()
        db_bytes = conn.serialize()

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, data in (("collection.anki2", db_bytes), ("media", b"{}")):
            info = zipfile.ZipInfo(name, date_time=ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 0
            info.external_attr = 0
            zf.writestr(info, data)
    return buf.getvalue()


def previous_timestamp(apkg: bytes) -> int | None:
    """Read the build timestamp from an .apkg this script wrote, or None."""
    try:
        with zipfile.ZipFile(io.BytesIO(apkg)) as zf:
            db_bytes = zf.read("collection.anki2")
        with closing(sqlite3.connect(":memory:")) as conn:
            conn.deserialize(db_bytes)
            (models_json,) = conn.execute("SELECT models FROM col").fetchone()
        return int(json.loads(models_json)[str(MODEL_ID)]["mod"])
    except Exception:
        return None


def write_deck(stem: str, cards: list[Card], out_path: Path,
               now: int | None = None) -> bool:
    """Write one deck. Returns True if the file changed, False if it didn't.

    If the existing file was built from the same content, it is left alone
    (rebuilding with its old timestamp gives the same bytes). Otherwise the
    deck gets the current time, so Anki treats its notes as newer.
    """
    old = out_path.read_bytes() if out_path.exists() else None
    if old is not None:
        old_ts = previous_timestamp(old)
        if old_ts is not None and build_apkg(stem, cards, old_ts) == old:
            return False
    timestamp = int(time.time()) if now is None else now
    out_path.write_bytes(build_apkg(stem, cards, timestamp))
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build docs/downloads/anki/<stem>.apkg from anki/cards/<stem>.tsv.")
    parser.add_argument("--cards", type=Path, default=CARDS_DIR,
                        help="folder of .tsv card files (default: anki/cards)")
    parser.add_argument("--out", type=Path, default=OUT_DIR,
                        help="output folder (default: docs/downloads/anki)")
    args = parser.parse_args(argv)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")

    paths = sorted(args.cards.glob("*.tsv"))
    if not paths:
        print(f"No .tsv files in {display_path(args.cards)}", file=sys.stderr)
        return 1

    decks: list[tuple[str, list[Card]]] = []
    errors: list[str] = []
    for path in paths:
        cards, file_errors = read_cards(path)
        errors.extend(file_errors)
        decks.append((path.stem, cards))

    if errors:
        for message in errors:
            print(message, file=sys.stderr)
        print(f"{len(errors)} error(s); no decks written.", file=sys.stderr)
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    for stem, cards in decks:
        if not cards:
            print(f"{stem}: no cards, skipped")
            continue
        out_path = args.out / f"{stem}.apkg"
        changed = write_deck(stem, cards, out_path)
        status = "" if changed else " (unchanged)"
        print(f"{deck_name(stem)}: {len(cards)} cards -> "
              f"{display_path(out_path)}{status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
