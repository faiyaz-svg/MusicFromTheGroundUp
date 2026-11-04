"""Shared bits for the stage 7 figure scripts."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from musicfigs import *  # noqa
from musicfigs import _svg, _text, _num_circle, INK, LABEL, YELLOW, SALMON, TEAL, SKY, LAVENDER, BG  # noqa: F401

STAGE = "07-pedal-texture-and-ambient/"


def line(x1, y1, x2, y2, w=1.5, c=INK):
    return f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{c}" stroke-width="{w}"/>\n'


def rect(x, y, w, h, fill="#fff", stroke=INK, sw=1.5, r=6):
    return (f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n')
