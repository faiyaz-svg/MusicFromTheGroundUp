from _common import *

for slug, notes, fing, labs in [
    ("c-root", ["C4", "E4", "G4"], {"C4": 1, "E4": 3, "G4": 5}, {}),
    ("f-second", ["C4", "F4", "A4"], {"C4": 1, "F4": 2, "A4": 5}, {}),
    ("g-first", ["B3", "D4", "G4"], {"B3": 1, "D4": 2, "G4": 5}, {}),
]:
    save(keyboard("B3", "A4", marks=notes, fingers=fing), STAGE + "inversions-on-piano-" + slug + ".svg")
print("inversions piano done")
