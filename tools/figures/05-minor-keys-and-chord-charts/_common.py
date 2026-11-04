"""Shared bits for the stage 5 figure scripts."""
import sys, pathlib, math
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from musicfigs import *  # noqa
from musicfigs import _svg, _text, _num_circle, INK, LABEL, YELLOW, SALMON, TEAL, SKY, LAVENDER, RED, BG  # noqa: F401

FOLDER = "05-minor-keys-and-chord-charts"


def line(x1, y1, x2, y2, w=1.5, c=INK):
    return f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{c}" stroke-width="{w}"/>\n'


def rect(x, y, w, h, fill=BG, stroke=INK, sw=1.5):
    return (f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n')


def circle(x, y, r, fill=BG, stroke=INK, sw=1.5):
    return f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'


def step_strip(notes, steps, title, fills=None, caption=None):
    """A row of note circles with W / H labels between them.
    notes: list of note names; steps: list of 'W', 'H' or 'W+H' (len(notes) - 1).
    fills: {index: colour} for circles to colour."""
    n = len(notes)
    gap = 78
    left = 40
    w = left * 2 + gap * (n - 1)
    h = 110 if caption else 90
    out = []
    y = 40
    for i in range(n - 1):
        x1, x2 = left + i * gap, left + (i + 1) * gap
        out.append(line(x1, y, x2, y, 2))
        lab = steps[i]
        wide = lab == "W+H"
        bx = (x1 + x2) / 2
        out.append(rect(bx - (19 if wide else 12), y + 22, 38 if wide else 24, 22, "#f4f4f4", INK, 1))
        out.append(_text(bx, y + 38, lab, size=13, fill=INK, weight="bold"))
    for i, nm in enumerate(notes):
        x = left + i * gap
        out.append(circle(x, y, 19, (fills or {}).get(i, BG)))
        out.append(_text(x, y + 5, nm, size=15, fill=INK, weight="bold"))
        out.append(_text(x, y - 27, str(i + 1), size=12, fill=LABEL))
    if caption:
        out.append(_text(w / 2, h - 8, caption, size=13, fill=LABEL))
    return _svg(w, h, title, "".join(out))


def chart_svg(bars, title, per_row=4, start_repeat=False, end_repeat=False, caption=None, beats=4):
    """Chord chart. bars: list of bars; each bar is a string (one chord for the bar),
    a list of (beat_index, chord) pairs like [(0,'C'),(2,'G')], or '%' (repeat the bar)."""
    bw, bh = 150, 72
    left = 30
    rows = [bars[i:i + per_row] for i in range(0, len(bars), per_row)]
    w = left * 2 + bw * per_row
    top = 14
    h = top + len(rows) * (bh + 14) + (26 if caption else 6)
    out = []
    for r, row in enumerate(rows):
        y = top + r * (bh + 14)
        for c in range(len(row) + 1):
            x = left + c * bw
            thick = (c == 0 and r == 0 and start_repeat) or (c == len(row) and r == len(rows) - 1 and end_repeat)
            out.append(line(x, y, x, y + bh, 4 if thick else 1.6))
        for c, bar in enumerate(row):
            x = left + c * bw
            if bar == "%":
                out.append(line(x + bw / 2 - 14, y + bh / 2 + 10, x + bw / 2 + 14, y + bh / 2 - 10, 4))
                out.append(circle(x + bw / 2 - 14, y + bh / 2 - 8, 4, INK, INK, 1))
                out.append(circle(x + bw / 2 + 14, y + bh / 2 + 8, 4, INK, INK, 1))
                continue
            chords = [(0, bar)] if isinstance(bar, str) else bar
            for beat, name in chords:
                out.append(_text(x + 12 + beat * (bw - 20) / beats, y + 26, name, size=22, fill=INK, anchor="start", weight="bold"))
            for b in range(beats):
                sx = x + 16 + b * (bw - 24) / beats
                out.append(line(sx, y + bh - 12, sx + 14, y + bh - 34, 2.4))
    # repeat dots
    for r, row in enumerate(rows):
        y = top + r * (bh + 14)
        if r == 0 and start_repeat:
            x = left
            out.append(circle(x + 12, y + bh / 2 - 8, 3.5, INK, INK, 1))
            out.append(circle(x + 12, y + bh / 2 + 8, 3.5, INK, INK, 1))
            out.append(line(x + 4, y, x + 4, y + bh, 1.6))
        if r == len(rows) - 1 and end_repeat:
            x = left + len(row) * bw
            out.append(circle(x - 12, y + bh / 2 - 8, 3.5, INK, INK, 1))
            out.append(circle(x - 12, y + bh / 2 + 8, 3.5, INK, INK, 1))
            out.append(line(x - 4, y, x - 4, y + bh, 1.6))
    if caption:
        out.append(_text(w / 2, h - 8, caption, size=13, fill=LABEL))
    return _svg(w, h, title, "".join(out))


def circle_of_fifths(title):
    cx = cy = 270
    w = h = 540
    majors = ["C", "G", "D", "A", "E", "B", "F#/Gb", "Db", "Ab", "Eb", "Bb", "F"]
    minors = ["Am", "Em", "Bm", "F#m", "C#m", "G#m", "D#m/Ebm", "Bbm", "Fm", "Cm", "Gm", "Dm"]
    sigs = ["0", "1#", "2#", "3#", "4#", "5#", "6# or 6b", "5b", "4b", "3b", "2b", "1b"]
    out = [circle(cx, cy, 250, "#fff", INK, 1.5), circle(cx, cy, 170, SKY, INK, 1.5), circle(cx, cy, 95, "#fff", INK, 1.5)]
    for i in range(12):
        a = math.radians(i * 30 - 90)
        a2 = math.radians(i * 30 - 75)
        out.append(line(cx + 95 * math.cos(a2), cy + 95 * math.sin(a2), cx + 250 * math.cos(a2), cy + 250 * math.sin(a2), 1, "#999"))
        out.append(_text(cx + 212 * math.cos(a), cy + 212 * math.sin(a) + 7, majors[i], size=22 if len(majors[i]) < 4 else 17, fill=INK, weight="bold"))
        out.append(_text(cx + 132 * math.cos(a), cy + 132 * math.sin(a) + 6, minors[i], size=18 if len(minors[i]) < 4 else 13, fill=INK, weight="bold"))
        out.append(_text(cx + 70 * math.cos(a), cy + 70 * math.sin(a) + 5, sigs[i], size=12 if len(sigs[i]) < 4 else 10, fill=LABEL))
    return _svg(w, h, title, "".join(out))


def strum_grid(pattern, title, counts=None):
    """16 slots (one bar of sixteenths). pattern: list of 16 of 'D', 'U', '-' (hand moves, no strum), 'x' (chuck)."""
    n = len(pattern)
    cw = 40
    left = 20
    w = left * 2 + cw * n
    h = 118
    counts = counts or ["1", "e", "&", "a"] * (n // 4)
    out = []
    for i, (p, c) in enumerate(zip(pattern, counts)):
        x = left + i * cw + cw / 2
        beat = i % 4 == 0
        out.append(_text(x, 24, c, size=17 if beat else 14, fill=INK if beat else LABEL, weight="bold" if beat else "normal"))
        if i % 4 == 0 and i:
            out.append(line(left + i * cw, 8, left + i * cw, 104, 1, "#bbb"))
        if p == "D":
            out.append(f'<polygon points="{x-9:g},62 {x+9:g},62 {x:g},82" fill="{INK}"/>' + line(x, 40, x, 64, 3))
            out.append(_text(x, 100, "D", size=14, fill=INK, weight="bold"))
        elif p == "U":
            out.append(f'<polygon points="{x-9:g},58 {x+9:g},58 {x:g},38" fill="{INK}"/>' + line(x, 56, x, 80, 3))
            out.append(_text(x, 100, "U", size=14, fill=INK, weight="bold"))
        elif p == "x":
            out.append(rect(x - 11, 42, 22, 22, YELLOW, INK, 1.5))
            out.append(_text(x, 59, "x", size=16, fill=INK, weight="bold"))
            out.append(_text(x, 100, "chuck", size=11, fill=INK))
        else:
            out.append(circle(x, 60, 3, "#bbb", "#bbb", 1))
    return _svg(w, h, title, "".join(out))
