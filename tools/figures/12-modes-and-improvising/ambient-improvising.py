from _common import *

notes = ["C4", "D4", "E4", "G4", "A4"]
save(keyboard("C4", "C5", marks=notes, labels={n: n[0] for n in notes}),
     STAGE + "ambient-improvising-five-notes.svg")
print("ambient-improvising done")
