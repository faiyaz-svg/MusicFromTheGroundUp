from _common import *

# The I, IV and V triads of C major, root in salmon.
for slug, notes in [("i", ["C4", "E4", "G4"]), ("iv", ["F4", "A4", "C5"]), ("v", ["G4", "B4", "D5"])]:
    cols = {n: ("salmon" if k == 0 else "yellow") for k, n in enumerate(notes)}
    labs = {n: n[:-1] for n in notes}
    save(keyboard("C4", "E5", colours=cols, labels=labs), STAGE + f"roman-numerals-c-{slug}.svg")
print("roman-numerals done")
