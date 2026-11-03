"""Shared bits for the stage 2 figure scripts."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from musicfigs import *  # noqa
from musicfigs import _parse, _svg, _text, _num_circle, _verovio, INK, LABEL, YELLOW, SALMON, TEAL, SKY, BG  # noqa: F401

STAGE = "02-two-hands-and-first-chords/"


def line(x1, y1, x2, y2, w=1.2, c=INK):
    return f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{c}" stroke-width="{w}"/>\n'


def grand(treble, bass, title):
    """Grand staff with whole notes. treble and bass are lists of the same length;
    each item is a note name like "C4" or None for a space. Built as MEI."""
    def cell(n):
        if n is None:
            return '<space dur="1"/>'
        letter, acc, octave = _parse(n)
        return f'<note pname="{letter.lower()}" oct="{octave}" dur="1"/>'
    t = "".join(cell(n) for n in treble)
    b = "".join(cell(n) for n in bass)
    mei = f'''<?xml version="1.0" encoding="UTF-8"?>
<mei xmlns="http://www.music-encoding.org/ns/mei" meiversion="5.0"><music><body><mdiv><score>
<scoreDef meter.sym="cut" meter.count="4" meter.unit="1"><staffGrp symbol="brace" bar.thru="true">
<staffDef n="1" lines="5" clef.shape="G" clef.line="2"/>
<staffDef n="2" lines="5" clef.shape="F" clef.line="4"/>
</staffGrp></scoreDef>
<section><measure right="end">
<staff n="1"><layer n="1">{t}</layer></staff>
<staff n="2"><layer n="1">{b}</layer></staff>
</measure></section></score></mdiv></body></music></mei>'''
    return _verovio(mei, title, fmt="mei")
