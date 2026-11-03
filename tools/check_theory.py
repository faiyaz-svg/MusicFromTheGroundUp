"""Check music facts stated in the lessons: chord spellings, scale spellings,
key signatures and intervals.

Run from the repo root:
  .venv/Scripts/python tools/check_theory.py              all of docs/
  .venv/Scripts/python tools/check_theory.py docs/04-intervals-and-triads

It looks for statements written in the book's standard forms (see the brief):
  chords:     "C major: C, E, G"   "Am is A, C, E"   "G7: G, B, D, F"
  scales:     "the D major scale: D, E, F#, G, A, B, C#, D"
  keys:       "D major has two sharps"   "Eb major has 3 flats (Bb, Eb, Ab)"
  intervals:  "C up to E is a major 3rd"   "from A to C is a minor third"
and also table rows whose first cell names a chord or scale and whose second
cell lists the notes. Each one is recomputed and compared, letters included
(F# and Gb are different spellings, so "D major: D, Gb, A" is reported).

Import it for the helpers: spell_chord("F#m7"), spell_scale("Bb", "major"),
key_signature("A", "minor"), interval_name("C", "Eb").
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

LETTERS = "CDEFGAB"
NATURAL = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
ACC = {"": 0, "#": 1, "##": 2, "x": 2, "b": -1, "bb": -2}

# Chord qualities: intervals above the root as (letter steps, semitones).
CHORDS = {
    "": [(0, 0), (2, 4), (4, 7)],
    "m": [(0, 0), (2, 3), (4, 7)],
    "dim": [(0, 0), (2, 3), (4, 6)],
    "aug": [(0, 0), (2, 4), (4, 8)],
    "+": [(0, 0), (2, 4), (4, 8)],
    "5": [(0, 0), (4, 7)],
    "sus2": [(0, 0), (1, 2), (4, 7)],
    "sus4": [(0, 0), (3, 5), (4, 7)],
    "add9": [(0, 0), (2, 4), (4, 7), (1, 14)],
    "madd9": [(0, 0), (2, 3), (4, 7), (1, 14)],
    "6": [(0, 0), (2, 4), (4, 7), (5, 9)],
    "m6": [(0, 0), (2, 3), (4, 7), (5, 9)],
    "7": [(0, 0), (2, 4), (4, 7), (6, 10)],
    "maj7": [(0, 0), (2, 4), (4, 7), (6, 11)],
    "m7": [(0, 0), (2, 3), (4, 7), (6, 10)],
    "m7b5": [(0, 0), (2, 3), (4, 6), (6, 10)],
    "dim7": [(0, 0), (2, 3), (4, 6), (6, 9)],
    "mmaj7": [(0, 0), (2, 3), (4, 7), (6, 11)],
    "9": [(0, 0), (2, 4), (4, 7), (6, 10), (1, 14)],
    "maj9": [(0, 0), (2, 4), (4, 7), (6, 11), (1, 14)],
    "m9": [(0, 0), (2, 3), (4, 7), (6, 10), (1, 14)],
    "7sus4": [(0, 0), (3, 5), (4, 7), (6, 10)],
}
QUALITY_WORDS = {
    "major": "", "minor": "m", "diminished": "dim", "augmented": "aug", "dominant 7th": "7",
    "dominant seventh": "7", "major 7th": "maj7", "major seventh": "maj7", "minor 7th": "m7",
    "minor seventh": "m7", "half-diminished": "m7b5", "diminished 7th": "dim7", "diminished seventh": "dim7",
}
SCALES = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "natural minor": [0, 2, 3, 5, 7, 8, 10],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "harmonic minor": [0, 2, 3, 5, 7, 8, 11],
    "melodic minor": [0, 2, 3, 5, 7, 9, 11],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "aeolian": [0, 2, 3, 5, 7, 8, 10],
    "locrian": [0, 1, 3, 5, 6, 8, 10],
    "ionian": [0, 2, 4, 5, 7, 9, 11],
}
PENTATONIC = {"major pentatonic": ([0, 1, 2, 4, 5], [0, 2, 4, 7, 9]), "minor pentatonic": ([0, 2, 3, 4, 6], [0, 3, 5, 7, 10])}
ORDINAL = {
    "unison": 1, "1st": 1, "2nd": 2, "second": 2, "3rd": 3, "third": 3, "4th": 4, "fourth": 4, "5th": 5,
    "fifth": 5, "6th": 6, "sixth": 6, "7th": 7, "seventh": 7, "octave": 8, "8th": 8,
}
WORD_NUM = {"no": 0, "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7}

NOTE = r"[A-G](?:##|bb|#|b|x)?"
NOTE_LIST = rf"{NOTE}(?:\s*(?:,|and|-)\s*(?:and\s+)?{NOTE})+"


def parse_note(name: str) -> tuple[int, int]:
    """'F#' -> (letter index 3, pitch class 6)."""
    letter, acc = name[0], name[1:]
    return LETTERS.index(letter), (NATURAL[letter] + ACC[acc]) % 12


def name_note(letter_index: int, pc: int) -> str:
    letter = LETTERS[letter_index % 7]
    diff = (pc - NATURAL[letter]) % 12
    if diff > 6:
        diff -= 12
    acc = {0: "", 1: "#", 2: "##", -1: "b", -2: "bb"}.get(diff)
    if acc is None:
        raise ValueError(f"can't spell pitch class {pc} on {letter}")
    return letter + acc


def spell_chord(symbol: str) -> list[str]:
    m = re.fullmatch(rf"({NOTE})(.*?)(?:/({NOTE}))?", symbol)
    if not m or m.group(2) not in CHORDS:
        raise ValueError(f"unknown chord {symbol}")
    li, pc = parse_note(m.group(1))
    notes = [name_note(li + steps, pc + semis) for steps, semis in CHORDS[m.group(2)]]
    if m.group(3):
        bass = m.group(3)
        notes = [bass] + [n for n in notes if n != bass]
    return notes


def spell_scale(tonic: str, kind: str) -> list[str]:
    li, pc = parse_note(tonic)
    kind = kind.lower()
    if kind in PENTATONIC:
        steps, semis = PENTATONIC[kind]
        return [name_note(li + s, pc + t) for s, t in zip(steps, semis)]
    return [name_note(li + i, pc + s) for i, s in enumerate(SCALES[kind])]


def key_signature(tonic: str, mode: str) -> tuple[int, str]:
    """(count, 'sharp' or 'flat') for a major or minor key."""
    notes = spell_scale(tonic, "major" if mode == "major" else "natural minor")
    sharps = sum(n.count("#") for n in notes)
    flats = sum(n.count("b") for n in notes)
    return (sharps, "sharp") if sharps else (flats, "flat")


def interval_name(low: str, high: str) -> str:
    l1, p1 = parse_note(low)
    l2, p2 = parse_note(high)
    number = (l2 - l1) % 7 + 1
    semis = (p2 - p1) % 12
    perfect = {1: 0, 4: 5, 5: 7}
    major = {2: 2, 3: 4, 6: 9, 7: 11}
    if number in perfect:
        d = semis - perfect[number]
        if number == 1 and d < 0:
            d += 12
        quality = {0: "perfect", 1: "augmented", -1: "diminished"}.get(d, "?")
    else:
        d = semis - major[number]
        if d < -6:
            d += 12
        quality = {0: "major", -1: "minor", 1: "augmented", -2: "diminished"}.get(d, "?")
    return f"{quality} {number}"


def same_list(said: list[str], expected: list[str]) -> bool:
    # Allow the scale to repeat its first note at the top.
    if len(said) == len(expected) + 1 and said[-1] == said[0]:
        said = said[:-1]
    return said == expected


def notes_in(text: str) -> list[str]:
    return re.findall(NOTE, text)


def check_text(path: Path) -> list[str]:
    issues = []
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^```.*?^```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S | re.M)
    for no, line in enumerate(text.splitlines(), 1):
        plain = re.sub(r"[`*]", "", line)

        for m in re.finditer(
            rf"\b(?:the\s+)?({NOTE})\s*((?:major|minor|natural minor|harmonic minor|melodic minor|dorian|phrygian|lydian|"
            rf"mixolydian|aeolian|locrian|ionian|major pentatonic|minor pentatonic))\s+scale\s*(?:is|has the notes|uses|:)\s*({NOTE_LIST})",
            plain, re.I,
        ):
            tonic, kind, listed = m.group(1), m.group(2), notes_in(m.group(3))
            try:
                expected = spell_scale(tonic, kind)
            except (ValueError, KeyError):
                continue
            if not same_list(listed, expected):
                issues.append(f"{no}: {tonic} {kind} scale is {' '.join(expected)}, text says {' '.join(listed)}")

        for m in re.finditer(
            rf"(?<![A-Za-z#])({NOTE})(m7b5|maj7|maj9|mmaj7|madd9|dim7|7sus4|sus2|sus4|add9|dim|aug|m7|m9|m6|m|7|9|6|5)?"
            rf"(?:\s+(major|minor|diminished|augmented|dominant 7th|dominant seventh|major 7th|major seventh|minor 7th|minor seventh|diminished 7th))?"
            rf"(?:\s+(?:chord|triad))?\s*(?::|=|is spelled|is made of|has the notes|uses the notes)\s*({NOTE_LIST})",
            plain,
        ):
            root, suffix, word, listed = m.group(1), m.group(2) or "", m.group(3), notes_in(m.group(4))
            if word:
                if suffix:
                    continue
                suffix = QUALITY_WORDS[word.lower()]
            if re.search(r"scale|key", plain[max(0, m.start() - 25):m.start() + len(root) + 25], re.I) and not word and not suffix:
                continue
            try:
                expected = spell_chord(root + suffix)
            except ValueError:
                continue
            if len(listed) != len(expected):
                continue
            if listed != expected:
                issues.append(f"{no}: {root}{suffix} is {', '.join(expected)}, text says {', '.join(listed)}")

        for m in re.finditer(
            rf"\b({NOTE})\s+(major|minor)\s+has\s+(\d|no|zero|one|two|three|four|five|six|seven)\s+(sharps?|flats?)",
            plain, re.I,
        ):
            tonic, mode, count, kind = m.group(1), m.group(2).lower(), m.group(3).lower(), m.group(4).lower()
            n = int(count) if count.isdigit() else WORD_NUM[count]
            try:
                want_n, want_kind = key_signature(tonic, mode)
            except ValueError:
                continue
            if n != want_n or (n and not kind.startswith(want_kind)):
                issues.append(f"{no}: {tonic} {mode} has {want_n} {want_kind}(s), text says {n} {kind}")

        for m in re.finditer(
            rf"(?:from\s+)?\b({NOTE})\s+(?:up\s+)?to\s+(?:the\s+)?({NOTE})(?:\s+above)?\s+is\s+an?\s+"
            rf"(major|minor|perfect|augmented|diminished)\s+(unison|1st|2nd|second|3rd|third|4th|fourth|5th|fifth|6th|sixth|7th|seventh|octave|8th)",
            plain, re.I,
        ):
            low, high, quality, num = m.group(1), m.group(2), m.group(3).lower(), ORDINAL[m.group(4).lower()]
            if num == 8:
                continue
            got = interval_name(low, high)
            if got != f"{quality} {num}":
                issues.append(f"{no}: {low} up to {high} is a {got}, text says {quality} {num}")

        cells = [c.strip() for c in plain.strip().strip("|").split("|")] if plain.lstrip().startswith("|") else []
        if len(cells) >= 2:
            listed = notes_in(cells[1])
            name = cells[0]
            if len(listed) >= 3 and re.fullmatch(r"[A-G A-Za-z0-9#,\s]+", cells[1]) and len(cells[1].split()) <= 9:
                m = re.fullmatch(rf"({NOTE})\s*(major|natural minor|harmonic minor|melodic minor|minor|major pentatonic|minor pentatonic)(?: scale)?", name, re.I)
                if m and "scale" in plain.lower() + name.lower():
                    expected = spell_scale(m.group(1), m.group(2))
                    if not same_list(listed, expected):
                        issues.append(f"{no}: table: {name} is {' '.join(expected)}, row says {' '.join(listed)}")
                m = re.fullmatch(rf"({NOTE})(m7b5|maj7|maj9|mmaj7|madd9|dim7|7sus4|sus2|sus4|add9|dim|aug|m7|m9|m6|m|7|9|6|5)?(?: chord)?", name)
                if m:
                    try:
                        expected = spell_chord(m.group(1) + (m.group(2) or ""))
                    except ValueError:
                        expected = None
                    if expected and len(listed) == len(expected) and listed != expected:
                        issues.append(f"{no}: table: {name} is {', '.join(expected)}, row says {', '.join(listed)}")
    return issues


def self_test() -> None:
    assert spell_chord("C") == ["C", "E", "G"]
    assert spell_chord("F#m7") == ["F#", "A", "C#", "E"]
    assert spell_chord("Bb7") == ["Bb", "D", "F", "Ab"]
    assert spell_chord("Bdim") == ["B", "D", "F"]
    assert spell_chord("Cadd9") == ["C", "E", "G", "D"]
    assert spell_chord("C/E") == ["E", "C", "G"]
    assert spell_scale("F#", "major") == ["F#", "G#", "A#", "B", "C#", "D#", "E#"]
    assert spell_scale("A", "harmonic minor") == ["A", "B", "C", "D", "E", "F", "G#"]
    assert spell_scale("A", "minor pentatonic") == ["A", "C", "D", "E", "G"]
    assert key_signature("Eb", "major") == (3, "flat")
    assert key_signature("E", "minor") == (1, "sharp")
    assert key_signature("C", "major")[0] == 0
    assert interval_name("C", "E") == "major 3"
    assert interval_name("A", "C") == "minor 3"
    assert interval_name("B", "F") == "diminished 5"
    assert interval_name("F", "B") == "augmented 4"
    assert interval_name("E", "C") == "minor 6"


def main() -> None:
    self_test()
    paths = []
    for arg in sys.argv[1:] or ["docs"]:
        p = Path(arg)
        paths += sorted(p.rglob("*.md")) if p.is_dir() else [p]
    total = 0
    for path in paths:
        if "my-music" in path.parts:
            continue
        for issue in check_text(path):
            total += 1
            print(f"{path}:{issue}")
    print(f"theory check: {len(paths)} file(s), {total} problem(s)")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
