"""Shared bits for the stage 10 figure scripts."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from musicfigs import *  # noqa
from musicfigs import _svg, _text, INK, LABEL, YELLOW, SALMON, TEAL, SKY, LAVENDER, RED, BG  # noqa: F401

FOLDER = "10-classical-repertoire"
FILLS = [YELLOW, SKY, TEAL, SALMON]


def line(x1, y1, x2, y2, w=1.5, c=INK, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{c}" stroke-width="{w}"{d}/>\n'


def rect(x, y, w, h, fill=BG, stroke=INK, sw=1.5, rx=0):
    return (f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx:g}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n')


def circle(x, y, r, fill=BG, stroke=INK, sw=1.5):
    return f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'


def _wrap(s, width_px, size=12):
    per = max(4, int(width_px / (size * 0.52)))
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= per:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:3]


def section_map(rows, alt, name, W=640, min_w=70):
    """rows: list of (row title, [(first_bar, last_bar, name, note), ...]).
    Each section is a box, wide in proportion to its bars (at least min_w).
    note is optional text such as 'played twice'."""
    left, right = 16, 16
    avail = W - left - right
    out, y = [], 12
    for title, secs in rows:
        out.append(_text(left, y + 12, title, size=13, fill=INK, anchor="start", weight="bold"))
        y += 22
        total = sum(e - s + 1 for s, e, *_ in secs)
        widths = [(e - s + 1) / total * avail for s, e, *_ in secs]
        small = [i for i, w in enumerate(widths) if w < min_w]
        if small:
            rest = avail - min_w * len(small)
            big_total = sum(w for i, w in enumerate(widths) if i not in small)
            widths = [min_w if i in small else w / big_total * rest for i, w in enumerate(widths)]
        x = left
        for k, ((s, e, nm, *note), w) in enumerate(zip(secs, widths)):
            out.append(rect(x, y, w, 52, FILLS[k % len(FILLS)], INK, 1.5))
            lines = _wrap(nm, w - 8)
            ty = y + 22 - 7 * (len(lines) - 1)
            for ln in lines:
                out.append(_text(x + w / 2, ty, ln, size=12, fill=INK, weight="bold"))
                ty += 14
            rng = f"bar {s}" if s == e else f"bars {s}-{e}"
            out.append(_text(x + w / 2, y + 68, rng, size=11, fill=LABEL))
            if note and note[0]:
                out.append(_text(x + w / 2, y + 81, note[0], size=11, fill=LABEL))
            x += w
        y += 96
    h = y + 4
    return _svg(W, h, alt, "".join(out)), h
