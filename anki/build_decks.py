"""Build Anki decks from the card files in anki/cards/.

Each anki/cards/<stem>.tsv becomes docs/downloads/anki/<stem>.apkg, one deck
per stage (plus generated decks such as note reading). Run it from the repo root:

    .venv/Scripts/python anki/build_decks.py

File format:

- UTF-8, tab-separated, 4 columns: id<TAB>front<TAB>back<TAB>tags. A first row
  exactly "id front back tags" is a header and is skipped.
- A field can't contain a tab or a newline: write <br> for a line break.
- Blank lines and lines starting with # are skipped.
- Images: write <img src="mfgu-....svg"> in a field. The file must be in
  anki/media/ and its name must start with "mfgu-" (Anki keeps every deck's
  media in one folder, so the prefix keeps names from clashing). The build
  puts each image into the package.

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
MEDIA_DIR = ROOT / "anki" / "media"
OUT_DIR = ROOT / "docs" / "downloads" / "anki"

BOOK_TITLE = "Music From the Ground Up"

# Readable deck titles. Other stems are used as they are.
FOLDER_TITLES = {
    "00-note-reading": "00 Note reading",
    "01-first-sounds": "01 First sounds",
    "02-two-hands-and-first-chords": "02 Two hands and first chords",
    "03-the-major-scale-and-keys": "03 The major scale and keys",
    "04-intervals-and-triads": "04 Intervals and triads",
    "05-minor-keys-and-chord-charts": "05 Minor keys and chord charts",
    "06-meter-terms-and-rhythm": "06 Meter, terms and rhythm",
    "07-pedal-texture-and-ambient": "07 Pedal, texture and ambient",
    "08-fretboard-barre-chords-and-caged": "08 Fretboard, barre chords and CAGED",
    "09-harmony": "09 Harmony",
    "10-classical-repertoire": "10 Classical repertoire",
    "11-film-game-and-anime-harmony": "11 Film, game and anime harmony",
    "12-modes-and-improvising": "12 Modes and improvising",
    "13-capstones": "13 Capstones",
}

# The note type is shared by every deck. Its ID must never change: Anki uses it
# to recognise the note type when a deck is imported again.
MODEL_ID = 1_729_403_611
MODEL_NAME = "Music From the Ground Up (basic)"

HEADER = ["id", "front", "back", "tags"]
ID_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
TAG_RE = re.compile(r"[A-Za-z0-9_-]+(?:::[A-Za-z0-9_-]+)*")
IMG_RE = re.compile(r'<img\s+src="([^"]+)"\s*/?>')

QUESTION_TEMPLATE = '<div class="front">{{Front}}</div>'
ANSWER_TEMPLATE = (
    "{{FrontSide}}\n"
    '<hr id="answer">\n'
    '<div class="back">{{Back}}</div>\n'
    '{{#Source}}<div class="source">{{Source}}</div>{{/Source}}'
)

CARD_CSS = """\
.card {
  font-family: Jost, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
  font-size: 20px;
  line-height: 1.5;
  text-align: center;
  color: #111;
  background-color: #fff;
}
.front, .back, .source, hr#answer {
  max-width: 36em;
  margin-left: auto;
  margin-right: auto;
}
.front img, .back img {
  max-width: 100%;
  height: auto;
  background: #fff;
}
hr#answer {
  border: none;
  border-top: 2px solid #111;
  margin-top: 1em;
  margin-bottom: 1em;
}
.source {
  margin-top: 1.5em;
  font-size: 14px;
  color: #4d4d4d;
}
.card.nightMode, .card.night_mode, .nightMode .card, .night_mode .card {
  color: #eee;
  background-color: #1e1e1e;
}
.nightMode hr#answer, .night_mode hr#answer {
  border-top-color: #858585;
}
.nightMode .source, .night_mode .source {
  color: #b3b3b3;
}
"""

# Fixed zip entry date, so identical content gives identical bytes.
ZIP_DATE = (1980, 1, 1, 0, 0, 0)


@dataclass
class Card:
    line: int
    id: str
    front: str
    back: str
    tags: list[str] = field(default_factory=list)
    media: list[str] = field(default_factory=list)


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
    h = int(hashlib.sha1(("music:" + stem).encode("utf-8")).hexdigest()[:8], 16)
    return (1 << 30) + h % (1 << 30)


def read_cards(path: Path, media_dir: Path = MEDIA_DIR) -> tuple[list[Card], list[str]]:
    """Read and check one card file. Returns (cards, errors)."""
    where = display_path(path)
    cards: list[Card] = []
    errors: list[str] = []
    first_line: dict[str, int] = {}

    try:
        raw = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        return [], [f"{where}: not valid UTF-8 ({exc})"]

    reader = csv.reader(io.StringIO(raw, newline=""), delimiter="\t", quoting=csv.QUOTE_NONE)
    for row in reader:
        line = reader.line_num
        if not row or (len(row) == 1 and not row[0].strip()):
            continue
        if row[0].startswith("#") or (line == 1 and [c.strip() for c in row] == HEADER):
            continue
        loc = f"{where}:{line}"
        if len(row) != 4:
            errors.append(f"{loc}: expected 4 tab-separated columns (id, front, back, tags), found {len(row)}")
            continue

        card_id, front, back, tags = (col.strip() for col in row)
        row_ok = True

        if not ID_RE.fullmatch(card_id):
            errors.append(f"{loc}: id {card_id!r} must be a lowercase slug such as s1-staff-middle-c")
            row_ok = False
        elif card_id in first_line:
            errors.append(f"{loc}: duplicate id {card_id!r} (first used on line {first_line[card_id]})")
            row_ok = False
        else:
            first_line[card_id] = line

        media: list[str] = []
        for name, value in (("front", front), ("back", back)):
            if not value:
                errors.append(f"{loc}: {name} is empty")
                row_ok = False
                continue
            bad_tags = genanki.Note._find_invalid_html_tags_in_field(value)
            if bad_tags:
                errors.append(f"{loc}: {name}: invalid HTML {' '.join(bad_tags)!r} (write < as &lt;)")
                row_ok = False
            for src in IMG_RE.findall(value):
                if not src.startswith("mfgu-") or "/" in src:
                    errors.append(f"{loc}: image {src!r} must be a bare file name starting with mfgu-")
                    row_ok = False
                elif not (media_dir / src).is_file():
                    errors.append(f"{loc}: image {src!r} is not in {display_path(media_dir)}")
                    row_ok = False
                else:
                    media.append(src)

        tag_list = tags.split()
        for tag in tag_list:
            if not TAG_RE.fullmatch(tag):
                errors.append(f"{loc}: tag {tag!r} may only use letters, digits, - and _ (and :: for nested tags)")
                row_ok = False

        if row_ok:
            all_tags = list(dict.fromkeys(tag_list + [path.stem]))
            cards.append(Card(line, card_id, front, back, all_tags, media))

    return cards, errors


def make_model() -> genanki.Model:
    return genanki.Model(
        MODEL_ID,
        MODEL_NAME,
        fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Source"}],
        templates=[{"name": "Card 1", "qfmt": QUESTION_TEMPLATE, "afmt": ANSWER_TEMPLATE}],
        css=CARD_CSS,
    )


def make_deck(stem: str, cards: list[Card]) -> genanki.Deck:
    title = folder_title(stem)
    deck = genanki.Deck(deck_id(stem), deck_name(stem), description=f"Flashcards for {title} in {BOOK_TITLE}.")
    model = make_model()
    for position, card in enumerate(cards):
        deck.add_note(genanki.Note(
            model=model,
            fields=[card.front, card.back, title],
            tags=card.tags,
            guid=genanki.guid_for("music", stem, card.id),
            due=position,  # new cards come up in file order
        ))
    return deck


def build_apkg(stem: str, cards: list[Card], timestamp: int, media_dir: Path = MEDIA_DIR) -> bytes:
    """Return the .apkg file contents for one deck, with its images."""
    package = genanki.Package(make_deck(stem, cards))
    with closing(sqlite3.connect(":memory:")) as conn:
        cursor = conn.cursor()
        package.write_to_db(cursor, timestamp, itertools.count(timestamp * 1000))
        conn.commit()
        db_bytes = conn.serialize()

    media_names = sorted({name for card in cards for name in card.media})
    media_map = {str(i): name for i, name in enumerate(media_names)}
    entries = [("collection.anki2", db_bytes)]
    entries += [(str(i), (media_dir / name).read_bytes()) for i, name in enumerate(media_names)]
    entries.append(("media", json.dumps(media_map, sort_keys=True).encode("utf-8")))

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, data in entries:
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


def write_deck(stem: str, cards: list[Card], out_path: Path, now: int | None = None,
               media_dir: Path = MEDIA_DIR) -> bool:
    """Write one deck. Returns True if the file changed, False if it didn't."""
    old = out_path.read_bytes() if out_path.exists() else None
    if old is not None:
        old_ts = previous_timestamp(old)
        if old_ts is not None and build_apkg(stem, cards, old_ts, media_dir) == old:
            return False
    timestamp = int(time.time()) if now is None else now
    out_path.write_bytes(build_apkg(stem, cards, timestamp, media_dir))
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build docs/downloads/anki/<stem>.apkg from anki/cards/<stem>.tsv.")
    parser.add_argument("--cards", type=Path, default=CARDS_DIR, help="folder of .tsv card files")
    parser.add_argument("--media", type=Path, default=MEDIA_DIR, help="folder of card images")
    parser.add_argument("--out", type=Path, default=OUT_DIR, help="output folder")
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
        cards, file_errors = read_cards(path, args.media)
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
        changed = write_deck(stem, cards, out_path, media_dir=args.media)
        status = "" if changed else " (unchanged)"
        images = len({m for c in cards for m in c.media})
        print(f"{deck_name(stem)}: {len(cards)} cards, {images} images -> {display_path(out_path)}{status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
