"""Shared bits for the stage 12 figure scripts."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from musicfigs import *  # noqa
from musicfigs import _svg, _text, INK, LABEL, YELLOW, SALMON, TEAL, SKY, LAVENDER, RED, BG  # noqa: F401

STAGE = "12-modes-and-improvising/"

# A minor pentatonic: pitch classes A C D E G
A_MINOR_PENT = {9, 0, 2, 4, 7}


def box_marks(box, root_pc=9):
    """Marks for a pentatonic box: dicts for musicfigs.fretboard. box is a list of 6
    (string, [frets]) pairs. Roots (A) are salmon, other notes yellow."""
    marks = []
    for string, frets in box:
        for f in frets:
            name = guitar_note(string, f)[:-1]
            marks.append({"string": string, "fret": f, "label": name,
                          "colour": "salmon" if name == "A" else "yellow"})
    return marks
