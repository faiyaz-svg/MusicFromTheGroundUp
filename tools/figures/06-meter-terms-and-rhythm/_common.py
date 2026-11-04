"""Shared bits for the stage 6 figure scripts."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from musicfigs import *  # noqa
from musicfigs import _svg, _text, INK, LABEL, YELLOW, SALMON, TEAL, SKY, BG  # noqa: F401

STAGE = "06-meter-terms-and-rhythm/"


def line(x1, y1, x2, y2, w=1.2, c=INK, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{c}" stroke-width="{w}"{d}/>\n'


def rect(x, y, w, h, fill=BG, stroke=INK, sw=1.5):
    return (f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n')


def arrow(x, y, up, c=INK, length=34):
    """A strum arrow centred on x; up=False is a down stroke."""
    y0, y1 = (y + length, y) if up else (y, y + length)
    s = line(x, y0, x, y1, 2.5, c)
    d = 7 if up else -7
    s += f'<polygon points="{x - 6:g},{y1 + d:g} {x + 6:g},{y1 + d:g} {x:g},{y1:g}" fill="{c}"/>\n'
    return s
