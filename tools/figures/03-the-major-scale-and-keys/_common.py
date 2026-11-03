"""Shared bits for the stage 3 figure scripts."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import re
from musicfigs import *  # noqa
from musicfigs import _svg, _text, _num_circle, _verovio, _text as _t, INK, LABEL, YELLOW, SALMON, TEAL, SKY, BG  # noqa: F401


def line(x1, y1, x2, y2, w=1.2, c=INK):
    return f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{c}" stroke-width="{w}"/>\n'


def rect(x, y, w, h, fill=BG, stroke=INK, sw=1.5, rx=0):
    return (f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx:g}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n')


def circle(x, y, r, fill=BG, stroke=INK, sw=1.5):
    return f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'


def widen(svg, extra_right=0, extra_body=""):
    """Add room on the right of a musicfigs SVG and draw extra elements there."""
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    w, h = float(m.group(1)), float(m.group(2))
    nw = w + extra_right
    svg = svg.replace(m.group(0), f'viewBox="0 0 {nw:g} {h:g}"', 1)
    svg = svg.replace(f'width="{w:g}" height="{h:g}"', f'width="{nw:g}" height="{h:g}"', 1)
    svg = svg.replace(f'<rect width="{w:g}" height="{h:g}"', f'<rect width="{nw:g}" height="{h:g}"', 1)
    return svg.replace("</svg>", extra_body + "</svg>")

from musicfigs import _num_circle as _nc  # noqa

def hand(x, y, thumb_side, nums, label):
    """Flat hand seen from above, palm down, fingers pointing up.
    thumb_side: -1 thumb on the left (right hand), 1 thumb on the right (left hand).
    nums: five labels from the thumb to the little finger."""
    import math
    out = []
    lens = [78, 90, 82, 62]          # index, middle, ring, little
    fw = 22
    palm_w = 4 * fw + 6
    order = range(4) if thumb_side == -1 else range(3, -1, -1)
    tips = []
    for i, k in enumerate(order):
        fx = x + 3 + i * fw
        out.append(rect(fx, y - lens[k], fw - 3, lens[k] + 6, "#fff", INK, 1.8, 10))
        tips.append((fx + (fw - 3) / 2, y - lens[k] + 14, k))
    out.append(rect(x, y, palm_w, 80, "#f4f4f4", INK, 1.8, 10))
    tx = x - 20 if thumb_side == -1 else x + palm_w + 20
    ang = 40 * thumb_side
    out.append(f'<g transform="rotate({ang} {tx:g} {y + 40})">'
               + rect(tx - 11, y + 8, 22, 62, "#fff", INK, 1.8, 11) + '</g>')
    for fx, fy, k in tips:
        out.append(_nc(fx, fy, nums[k + 1], 10, YELLOW))
    a = math.radians(ang)
    px = tx + 26 * math.sin(a)
    py = y + 40 - 26 * math.cos(a)
    out.append(_nc(px, py, nums[0], 10, YELLOW))
    out.append(_t(x + palm_w / 2, y + 100, label, size=14, fill=INK, weight="bold"))
    return "".join(out)



# ---- stage 3 helpers -------------------------------------------------------
import re as _re

_PAD, _KW = 6, 28


def key_centres(start, end):
    """x of the centre of every key (white keys, and black keys on the boundary)
    for a keyboard(start, end) figure with 16 white keys or fewer."""
    s, e = note_to_midi(start), note_to_midi(end)
    whites = [m for m in range(s, e + 1) if m % 12 in (0, 2, 4, 5, 7, 9, 11)]
    widx = {m: i for i, m in enumerate(whites)}
    out = {}
    for m in range(s, e + 1):
        if m in widx:
            out[m] = _PAD + (widx[m] + 0.5) * _KW
        elif (m - 1) in widx and (m + 1) in widx:
            out[m] = _PAD + (widx[m - 1] + 1) * _KW
    return out


def taller(svg, extra, body, extra_w=0):
    """Add `extra` pixels of height under a musicfigs SVG and draw `body` there."""
    m = _re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    w, h = float(m.group(1)), float(m.group(2))
    nw, nh = w + extra_w, h + extra
    svg = svg.replace(m.group(0), f'viewBox="0 0 {nw:g} {nh:g}"', 1)
    svg = svg.replace(f'width="{w:g}" height="{h:g}"', f'width="{nw:g}" height="{nh:g}"', 1)
    svg = svg.replace(f'<rect width="{w:g}" height="{h:g}"', f'<rect width="{nw:g}" height="{nh:g}"', 1)
    return svg.replace("</svg>", body + "</svg>")


def step_brackets(svg, start, end, notes, y0=None):
    """Draw a W or H bracket under the keyboard between each pair of neighbouring
    notes in `notes` (a scale written with sharps, e.g. ["G4", ..., "F#5", "G5"])."""
    m = _re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    h = float(m.group(2))
    cx = key_centres(start, end)
    body = ""
    for a, b in zip(notes, notes[1:]):
        ma, mb = note_to_midi(a), note_to_midi(b)
        xa, xb = cx[ma] + 3, cx[mb] - 3
        kind = "W" if mb - ma == 2 else "H"
        col = "#fed134" if kind == "H" else "#d5b3ff"
        y = h + 4
        body += (f'<path d="M{xa:g} {y - 2:g} V{y + 6:g} H{xb:g} V{y - 2:g}" fill="none" '
                 f'stroke="{INK}" stroke-width="1.5"/>\n')
        body += rect((xa + xb) / 2 - 11, y + 12, 22, 20, col, INK, 1.2)
        body += _text((xa + xb) / 2, y + 27, kind, size=13, fill=INK, weight="bold")
    return taller(svg, 44, body)
