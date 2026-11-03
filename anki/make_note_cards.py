"""Generate the note-reading deck: one card per note on the treble and bass staff.

Writes the staff images to anki/media/ (mfgu-note-<clef>-<note>.svg) and the
cards to anki/cards/00-note-reading.tsv. Run from the repo root, then build:

    .venv/Scripts/python anki/make_note_cards.py
    .venv/Scripts/python anki/build_decks.py

The ranges match the note flashcards on the site: treble A3 to C6 and bass
C2 to E4, natural notes only, so ledger lines above and below each staff are
included.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools" / "figures"))
from musicfigs import staff_note  # noqa: E402

MEDIA = ROOT / "anki" / "media"
CARDS = ROOT / "anki" / "cards" / "00-note-reading.tsv"
LETTERS = "CDEFGAB"


def naturals(low: str, high: str) -> list[str]:
    def index(note: str) -> int:
        return int(note[1:]) * 7 + LETTERS.index(note[0])

    return [f"{LETTERS[i % 7]}{i // 7}" for i in range(index(low), index(high) + 1)]


def describe(note: str) -> str:
    extra = {"C4": " (middle C)", "G4": " (the treble clef curls around this line)", "F3": " (the bass clef's dots sit around this line)"}
    return note + extra.get(note, "")


def main() -> None:
    MEDIA.mkdir(parents=True, exist_ok=True)
    rows = ["id\tfront\tback\ttags"]
    for clef, low, high in (("treble", "A3", "C6"), ("bass", "C2", "E4")):
        for note in naturals(low, high):
            name = f"mfgu-note-{clef}-{note}.svg"
            (MEDIA / name).write_text(staff_note(note, clef=clef), encoding="utf-8", newline="\n")
            rows.append(
                f"note-{clef}-{note.lower()}\t<img src=\"{name}\"><br>Which note is this ({clef} clef)?"
                f"\t{describe(note)}\tnote-reading {clef}"
            )
    CARDS.write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(rows) - 1} cards -> {CARDS.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
