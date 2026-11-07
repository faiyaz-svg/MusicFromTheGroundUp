from _common import *

# Five 7th chords on C. Root salmon, 3rd and 5th yellow, 7th teal.
chords = [
    ("cmaj7", ["C4", "E4", "G4", "B4"], ["C", "E", "G", "B"]),
    ("c7", ["C4", "E4", "G4", "Bb4"], ["C", "E", "G", "Bb"]),
    ("cm7", ["C4", "Eb4", "G4", "Bb4"], ["C", "Eb", "G", "Bb"]),
    ("cm7b5", ["C4", "Eb4", "Gb4", "Bb4"], ["C", "Eb", "Gb", "Bb"]),
    ("cdim7", ["C4", "Eb4", "Gb4", "Bbb4"], ["C", "Eb", "Gb", "Bbb"]),
]
for slug, notes, names in chords:
    cols = {n: "yellow" for n in notes}
    cols[notes[0]] = "salmon"
    cols[notes[3]] = "teal"
    save(keyboard("C4", "C5", colours=cols, labels=dict(zip(notes, names))), STAGE + f"seventh-chords-{slug}.svg")
print("seventh-chords done")
