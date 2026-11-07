from _common import *

# The four chords of the C major cadence, right hand fingers 1 3 5.
for slug, notes, lab in [
    ("i", ["C4", "E4", "G4"], "C major"),
    ("iv", ["C4", "F4", "A4"], "F major"),
    ("v", ["B3", "D4", "G4"], "G major"),
]:
    save(keyboard("B3", "C5", colours={n: "yellow" for n in notes},
                  fingers=dict(zip(notes, [1, 3, 5])), labels={n: n[:-1] for n in notes}),
         STAGE + f"cadences-at-the-piano-{slug}.svg")
print("cadences-at-the-piano done")
