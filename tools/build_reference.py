"""Regenerate the glossary and common-mistakes pages from the lessons.

Reads tools/lessons.yml (reading order), then for every lesson file that exists:
  - glossary: the "- **Term**: definition" items in the "## Key terms" section.
    The first lesson to define a term wins; later lessons are listed after it.
  - common mistakes: the paragraphs of the "## Common mistakes" section, grouped
    by stage and lesson.

Only the text between <!-- generated:start --> and <!-- generated:end --> in
docs/reference/glossary.md and common-mistakes.md is replaced, so the pages'
introductions are kept. With --tracked, only lessons committed to git count.
Run from the repo root:  .venv/Scripts/python tools/build_reference.py [--tracked]
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REF = DOCS / "reference"
START, END = "<!-- generated:start -->", "<!-- generated:end -->"
TERM = re.compile(r"^- \*\*(.+?)\*\*(.*?):\s+(.+)$")


def lessons():
    """Yield (stage title, lesson title, path relative to docs/)."""
    data = yaml.safe_load((ROOT / "tools" / "lessons.yml").read_text(encoding="utf-8"))
    for f in data["folders"]:
        for i, entry in enumerate(f["lessons"], 1):
            yield f["title"], entry[1], f"{f['folder']}/{i:02d}-{entry[0]}.md"


def tracked() -> set[str]:
    out = subprocess.run(["git", "ls-files", "docs"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return {line.removeprefix("docs/") for line in out.splitlines()}


def section(text: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}\s*$", text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    n = re.search(r"^## |^Next: ", rest, re.M)
    return rest[: n.start()] if n else rest


def rel(path: str) -> str:
    return os.path.relpath(DOCS / path, REF).replace("\\", "/")


def fix_links(text: str, lesson_path: str) -> str:
    """Rewrite relative links in a lesson's text so they work from docs/reference/."""
    base = (DOCS / lesson_path).parent

    def repl(m: re.Match) -> str:
        target = m.group(2)
        if re.match(r"[a-z]+:|#", target):
            return m.group(0)
        path, _, anchor = target.partition("#")
        new = os.path.relpath((base / path).resolve(), REF.resolve()).replace("\\", "/")
        return f"[{m.group(1)}]({new}{'#' + anchor if anchor else ''})"

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", repl, text)
    return re.sub(r"<!-- link: [^>]+ -->", "", text)


def replace_generated(path: Path, generated: str) -> None:
    text = path.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise SystemExit(f"{path} has no {START} ... {END} block")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    path.write_text(f"{head}{START}\n\n{generated.strip()}\n\n{END}{tail}", encoding="utf-8", newline="\n")


def main() -> None:
    only = tracked() if "--tracked" in sys.argv else None
    terms: dict[str, dict] = {}
    mistakes: list[tuple[str, str, str, list[str]]] = []
    for stage, title, path in lessons():
        file = DOCS / path
        if not file.is_file() or (only is not None and path not in only):
            continue
        text = file.read_text(encoding="utf-8")
        for line in section(text, "Key terms").splitlines():
            m = TERM.match(line.strip())
            if not m:
                continue
            term, extra, definition = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
            key = term.lower()
            if key in terms:
                terms[key]["also"].append((title, path))
                continue
            terms[key] = {"term": term, "extra": extra, "def": fix_links(definition, path),
                          "title": title, "path": path, "also": []}
        pars = [p.strip() for p in re.split(r"\n\s*\n", section(text, "Common mistakes")) if p.strip()]
        if pars:
            mistakes.append((stage, title, path, [fix_links(p, path) for p in pars]))

    out = []
    letter = ""
    for key in sorted(terms, key=lambda k: re.sub(r"[^a-z0-9#]", "", k)):
        t = terms[key]
        first = re.sub(r"[^A-Za-z]", "", t["term"])[:1].upper() or "#"
        if first != letter:
            letter = first
            out += ["", f"## {letter}", ""]
        extra = f" {t['extra']}" if t["extra"] else ""
        also = "".join(f", [{a}]({rel(p)})" for a, p in t["also"][:3])
        out.append(f"- **{t['term']}**{extra}: {t['def']} ([{t['title']}]({rel(t['path'])}){also})")
    replace_generated(REF / "glossary.md", "\n".join(out))

    out = []
    current = ""
    for stage, title, path, pars in mistakes:
        if stage != current:
            current = stage
            out += ["", f"## {stage}", ""]
        out += [f"### [{title}]({rel(path)})", ""]
        for p in pars:
            out += [p, ""]
    replace_generated(REF / "common-mistakes.md", "\n".join(out))
    n_m = sum(len(p) for *_, p in mistakes)
    print(f"glossary: {len(terms)} terms; common mistakes: {n_m} from {len(mistakes)} lessons")


if __name__ == "__main__":
    main()
