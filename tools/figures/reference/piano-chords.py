"""Keyboard figures for the piano chord chart: C, F, G and Am triads."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from musicfigs import keyboard, save

F = "reference/piano-chords-"
chords = [
    ("c", ["C4", "E4", "G4"]),
    ("f", ["F4", "A4", "C5"]),
    ("g", ["G4", "B4", "D5"]),
    ("am", ["A4", "C5", "E5"]),
]
for slug, notes in chords:
    save(keyboard("C4", "G5", marks=notes, colours={notes[0]: "salmon"},
                  fingers=dict(zip(notes, (1, 3, 5))), show_names=True), F + slug + ".svg")
print("piano chords done")
