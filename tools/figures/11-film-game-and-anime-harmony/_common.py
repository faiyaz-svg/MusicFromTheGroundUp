"""Shared bits for the stage 11 figure scripts."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from musicfigs import *  # noqa
from musicfigs import _svg, _text, INK, LABEL, YELLOW, SALMON, TEAL, SKY, LAVENDER, BG, PALETTE  # noqa: F401

STAGE = "11-film-game-and-anime-harmony/"


def strip(items, title, loop=False, box_w=110, gap=26, notes=None):
    """A row of chord boxes with the Roman numeral under each box and arrows between them.

    items: list of (chord name, numeral, colour name or hex).
    loop: draw a dashed return line under the row from the last box to the first.
    notes: optional list of small captions under the numerals (same length as items).
    """
    n = len(items)
    pad = 20
    w = pad * 2 + n * box_w + (n - 1) * gap
    top = 20
    box_h = 64
    text_bottom = top + box_h + (52 if notes else 32)
    h = text_bottom + (34 if loop else 14)
    body = ""
    for i, (name, numeral, col) in enumerate(items):
        x = pad + i * (box_w + gap)
        fill = PALETTE.get(col, col)
        body += (f'<rect x="{x}" y="{top}" width="{box_w}" height="{box_h}" fill="{fill}" '
                 f'stroke="{INK}" stroke-width="2"/>\n')
        body += _text(x + box_w / 2, top + box_h / 2 + 9, name, size=26, fill=INK, weight="bold")
        body += _text(x + box_w / 2, top + box_h + 26, numeral, size=20, fill=INK, weight="bold")
        if notes:
            body += _text(x + box_w / 2, top + box_h + 46, notes[i], size=13, fill=LABEL)
        if i < n - 1:
            ax = x + box_w + 3
            ay = top + box_h / 2
            body += (f'<line x1="{ax}" y1="{ay}" x2="{ax + gap - 9}" y2="{ay}" stroke="{INK}" stroke-width="2"/>\n'
                     f'<polygon points="{ax + gap - 3},{ay} {ax + gap - 11},{ay - 5} {ax + gap - 11},{ay + 5}" fill="{INK}"/>\n')
    if loop:
        y = h - 10
        x1 = pad + box_w / 2
        x2 = pad + (n - 1) * (box_w + gap) + box_w / 2
        base = text_bottom - 4
        body += (f'<polyline points="{x2},{base} {x2},{y} {x1},{y} {x1},{base + 2}" fill="none" stroke="{LABEL}" '
                 f'stroke-width="1.5" stroke-dasharray="5 4"/>\n'
                 f'<polygon points="{x1},{base - 4} {x1 - 5},{base + 4} {x1 + 5},{base + 4}" fill="{LABEL}"/>\n')
        body += _text((x1 + x2) / 2, y - 5, "repeat", size=13, fill=LABEL)
    return _svg(w, h, title, body)
