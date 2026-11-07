"""Shared bits for the stage 9 figure scripts."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from musicfigs import *  # noqa
from musicfigs import _svg, _text, _num_circle, INK, LABEL, YELLOW, SALMON, TEAL, SKY, LAVENDER, BG  # noqa: F401

STAGE = "09-harmony/"
