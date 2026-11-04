from _common import *

for slug, notes, labs in [
    ("root", ["C4", "E4", "G4"], {"C4": "C", "E4": "E", "G4": "G"}),
    ("first", ["E4", "G4", "C5"], {"E4": "E", "G4": "G", "C5": "C"}),
    ("second", ["G4", "C5", "E5"], {"G4": "G", "C5": "C", "E5": "E"}),
]:
    save(keyboard("C4", "E5", colours={n: ("salmon" if n.startswith("C") else "yellow") for n in notes}, labels=labs),
         STAGE + "inversions-c-" + slug + ".svg")
save(chord_diagram("C/E", [0, 3, 2, 0, 1, 0], [None, 3, 2, None, 1, None], highlight_root=6),
     STAGE + "inversions-c-over-e.svg")
print("inversions done")
