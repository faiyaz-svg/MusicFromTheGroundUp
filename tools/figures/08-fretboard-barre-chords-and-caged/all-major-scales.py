from _common import *
F = STAGE + "all-major-scales-"
def sc(notes, fing, start, end, name):
    save(keyboard(start, end, marks=notes, fingers=dict(zip(notes, fing))), F + name)
sc(["F4", "G4", "A4", "Bb4", "C5", "D5", "E5", "F5"], [1, 2, 3, 4, 1, 2, 3, 4], "F4", "F5", "f-rh.svg")
sc(["B3", "C#4", "D#4", "E4", "F#4", "G#4", "A#4", "B4"], [4, 3, 2, 1, 4, 3, 2, 1], "B3", "B4", "b-lh.svg")
sc(["F#4", "G#4", "A#4", "B4", "C#5", "D#5", "E#5", "F#5"], [2, 3, 4, 1, 2, 3, 1, 2], "F4", "G5", "fsharp-rh.svg")
sc(["F#3", "G#3", "A#3", "B3", "C#4", "D#4", "E#4", "F#4"], [4, 3, 2, 1, 3, 2, 1, 4], "F3", "G4", "fsharp-lh.svg")
print("done")
