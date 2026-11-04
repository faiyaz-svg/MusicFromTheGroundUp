"""Shared bits for the stage 4 figure scripts."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from musicfigs import *  # noqa
from musicfigs import _svg, _text, INK, LABEL, YELLOW, SALMON, TEAL, SKY, BG  # noqa: F401

STAGE = "04-intervals-and-triads/"
