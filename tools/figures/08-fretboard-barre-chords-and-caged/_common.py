"""Shared bits for the stage 8 figure scripts."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from musicfigs import *  # noqa
from musicfigs import _svg, _text, _pc_name, INK, LABEL, YELLOW, SALMON, TEAL, SKY, BG  # noqa: F401

STAGE = "08-fretboard-barre-chords-and-caged/"
OPEN = {6: 40, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}
NN = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def nm(st, f):
    return NN[(OPEN[st] + f) % 12]


def string_labels(svg_body_x=14, top=20, sp=26, strings=(1, 2, 3, 4, 5, 6)):
    return "".join(_text(svg_body_x, top + (st - 1) * sp + 4, str(st), size=12, fill=INK, weight="bold")
                   for st in strings)


def with_strings(svg):
    """Add string numbers on the left of a fretboard svg that starts at the nut."""
    return svg.replace("</svg>", string_labels() + "</svg>")
