"""Style and template check for lesson pages (the STYLE.md self-check, as a script).

Run from the repo root:
  .venv/Scripts/python tools/lint.py docs/01-first-sounds           every lesson in a stage
  .venv/Scripts/python tools/lint.py docs/01-first-sounds/02-meet-your-piano.md

It reports banned words, em dashes, curly quotes, Unicode sharps and flats,
emoji, Title Case headings, bold-label bullets, missing template sections, a
practice routine whose minutes don't add up to 30, and the prose word count.
Some hits are false positives (a word in a quotation, a name); read each one.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BANNED = re.compile(
    r"\b(delve|tapestry|testament|pivotal|underscores?|underscored|intricat\w*|meticulous\w*|showcas\w*|"
    r"garner\w*|bolster\w*|interplay|vibrant|multifaceted|realms?|groundbreaking|renowned|nestled|"
    r"seamless\w*|commendable|noteworthy|invaluable|transformative|unparalleled|unveil\w*|harness\w*|"
    r"elucidat\w*|burgeoning|foster\w*|leverag\w*|quietly|deep dive|boasts?|journey|unlock\w*|elevat\w*|"
    r"key (?:role|factor|takeaway|insight|concept)s?|"
    r"serves? as|stands? as|functions? as|important to note|worth noting|worth mentioning|in summary|"
    r"in conclusion|to sum up|not only|let'?s dive|let'?s unpack|clearly|obviously|it is easy|"
    r"simply|trivially|great question|i hope this helps|"
    r"timeless|beloved|iconic|masterpiece|breathtaking|hauntingly|game-changing|supercharge\w*|revolutioni[sz]e)\b",
    re.I,
)
SPARING = re.compile(
    r"\b(crucial|vital|essential|comprehensive|notably|additionally|moreover|furthermore|consequently|"
    r"ultimately|enhance\w*|valuable|insights?|remarkable|nuanced|significant|robust|powerful|lush|"
    r"just|master(?:ed|ing|s)?)\b",
    re.I,
)
# Words allowed to keep a capital in a heading (besides the first word).
HEADING_OK = {
    "I", "II", "III", "IV", "V", "VI", "VII", "V7", "I7", "IV7", "RCM", "MIDI", "ABC", "CAGED", "VS", "Code",
    "Anki", "YouTube", "JustinGuitar", "Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian",
    "Locrian", "Travis", "Alberti", "Picardy", "Mario", "Bach", "Petzold", "Türk", "Gurlitt", "Schumann",
    "Burgmüller", "Tchaikovsky", "Clementi", "Chopin", "Debussy", "Grieg", "Satie", "Giuliani", "Carulli",
    "Sor", "Carcassi", "Aguado", "Tárrega", "Gymnopédie", "Arietta", "Adelita", "Opus", "Op.", "No.",
    "Example", "Minuet", "Prelude", "Sonatina", "Arabesque", "Ballade", "Melody", "Soldiers'", "March",
    "Old", "French", "Song", "Happy", "Farmer", "Little", "Shepherd", "RH", "LH", "Hz", "Em", "Am", "Dm",
}
CHORDISH = re.compile(r"^[A-G](#|b)?(m|maj7|maj|m7|7|dim|aug|sus2|sus4|add9|5|6|9)?[0-9]?[,.:;)]?$")
SECTIONS = ["## Practice routine", "## Move on when", "## Key terms"]
TAG = re.compile(r'<span class="tag tag-(piano|guitar|theory|reading|ear|improvise|other)">')


def prose_words(text: str) -> int:
    text = re.sub(r"^```.*?^```", "", text, flags=re.S | re.M)
    lines = [ln for ln in text.splitlines() if not ln.lstrip().startswith("|")]
    text = "\n".join(lines)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return len(re.findall(r"[A-Za-z0-9#']+", text))


def practice_minutes(text: str) -> list[int]:
    totals = []
    for block in re.findall(r'<div class="practice" markdown>(.*?)</div>', text, flags=re.S):
        mins = 0
        for row in block.splitlines():
            m = re.match(r"^\|\s*(\d+)\s*\|", row)
            if m:
                mins += int(m.group(1))
        totals.append(mins)
    return totals


def check(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    issues = []
    in_code = False
    section = ""
    for no, line in enumerate(text.splitlines(), 1):
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if "—" in line:
            issues.append(f"{no}: em dash")
        if re.search(r"–", line) and not re.search(r"\d–\d", line):
            issues.append(f"{no}: en dash outside a numeric range")
        if re.search("[“”‘’]", line):
            issues.append(f"{no}: curly quote")
        if re.search("[♯♭♮]", line):
            issues.append(f"{no}: Unicode sharp/flat/natural (write # and b)")
        if re.search("[\U0001F300-\U0001FAFF☀-➿]", line):
            issues.append(f"{no}: emoji or symbol")
        prose = re.sub(r"`[^`]*`", "", line)
        for m in BANNED.finditer(prose):
            issues.append(f"{no}: banned '{m.group(0)}'")
        for m in SPARING.finditer(prose):
            if m.group(0).lower().startswith("master") and "master volume" in prose.lower():
                continue
            issues.append(f"{no}: use rarely '{m.group(0)}'")
        if line.startswith("## "):
            section = line.strip()
        # The key terms list is the one place where "- **Term**: ..." is the format.
        if section != "## Key terms" and (
            re.match(r"^\s*[-*] \*\*[^*]+:\*\*", line) or re.match(r"^\s*[-*] \*\*[^*]+\*\*:", line)
        ):
            issues.append(f"{no}: bold label bullet")
        if re.match(r"^#{2,6} ", line):
            words = re.sub(r"[()\[\]]", " ", line.lstrip("#")).split()
            caps = [
                w for w in words[1:]
                if w[:1].isupper() and w not in HEADING_OK and not CHORDISH.match(w) and not w[:1].isdigit()
            ]
            if caps:
                issues.append(f"{no}: Title Case? {line.strip()}")
        if re.search(r"\bmeasures?\b", prose, re.I) and "also called a measure" not in prose:
            issues.append(f"{no}: 'measure' (the book says 'bar')")
    if text.count("<details") != text.count("</details>"):
        issues.append("unbalanced <details>")
    if len(re.findall(r"<div ", text)) != text.count("</div>"):
        issues.append("unbalanced <div>")
    # Template checks apply to lessons: files in a stage folder (01-... to 13-...) other than index.md.
    if path.name != "index.md" and re.match(r"(0[1-9]|1[0-3])-", path.parent.name):
        if not TAG.search(text):
            issues.append("missing the area tag line under the title")
        if "After this lesson you can" not in text:
            issues.append("missing 'After this lesson you can'")
        if "Before this:" not in text:
            issues.append("missing 'Before this:'")
        for s in SECTIONS:
            if s not in text:
                issues.append(f"missing section '{s}'")
        if not re.search(r"^Next: ", text, re.M):
            issues.append("missing 'Next:' link")
        for total in practice_minutes(text):
            if total != 30:
                issues.append(f"practice routine adds up to {total} minutes, not 30")
        words = prose_words(text)
        if words > 1500:
            issues.append(f"{words} words of prose (cap 1500)")
        elif words < 500:
            issues.append(f"{words} words of prose (short?)")
    return issues


def main() -> None:
    paths = []
    for arg in sys.argv[1:] or ["docs"]:
        p = Path(arg)
        paths += sorted(p.rglob("*.md")) if p.is_dir() else [p]
    total = 0
    for path in paths:
        if "my-music" in path.parts or path.name == "style-sample.md":
            continue
        found = check(path)
        total += len(found)
        print(f"== {path}: {len(found)} issue(s)")
        for item in found[:40]:
            print("   ", item)
    print(f"{total} issue(s) in {len(paths)} file(s)")


if __name__ == "__main__":
    main()
