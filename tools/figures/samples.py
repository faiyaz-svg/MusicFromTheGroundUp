"""Write one sample of each musicfigs function to docs/assets/figures/_samples/."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from musicfigs import (keyboard, chord_diagram, fretboard, staff_note,
                       staff_note_grand, save, guitar_note)

D = "_samples/"
save(keyboard("C4", "C5", marks=["C4", "D4", "E4", "F4", "G4"],
              fingers={"C4": 1, "D4": 2, "E4": 3, "F4": 4, "G4": 5},
              show_names=True, middle_c=True), D + "keyboard-rh-fingers.svg")
save(keyboard("A0", "C8", middle_c=True), D + "keyboard-88.svg")
save(chord_diagram("Em", [0, 2, 2, 0, 0, 0], [None, 2, 3, None, None, None],
                   highlight_root=6), D + "chord-em.svg")
save(chord_diagram("C", ["x", 3, 2, 0, 1, 0], [None, 3, 2, None, 1, None],
                   highlight_root=5), D + "chord-c.svg")
save(chord_diagram("F", [1, 3, 3, 2, 1, 1], [1, 3, 4, 2, 1, 1], barre=(1, 6, 1)),
     D + "chord-f.svg")
save(chord_diagram("Bm", ["x", 2, 4, 4, 3, 2], [None, 1, 3, 4, 2, 1], barre=(2, 5, 1),
                   base_fret=2), D + "chord-bm.svg")
marks = []
for s in range(1, 7):
    for f in range(0, 13):
        n = guitar_note(s, f)[:-1]
        if len(n) == 1:  # natural notes = C major scale
            marks.append({"string": s, "fret": f, "label": n,
                          "colour": "salmon" if n == "C" else "yellow"})
save(fretboard(12, marks=marks), D + "fretboard-c-major.svg")
save(fretboard(5, show_names=True), D + "fretboard-names.svg")
save(staff_note("C4"), D + "staff-c4-treble.svg")
save(staff_note("F3", clef="bass"), D + "staff-f3-bass.svg")
save(staff_note("A5"), D + "staff-a5-ledger.svg")
save(staff_note("Bb3", clef="bass"), D + "staff-bb3-bass.svg")
save(staff_note_grand("C4"), D + "staff-grand-c4.svg")
print("samples written")
