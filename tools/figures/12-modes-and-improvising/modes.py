from _common import *

# The seven white-key modes: (file, start, end, characteristic note)
MODES = [
    ("ionian", "C4", "C5", None),
    ("dorian", "D4", "D5", "B4"),
    ("phrygian", "E4", "E5", "F4"),
    ("lydian", "F4", "F5", "B4"),
    ("mixolydian", "G4", "G5", "F5"),
    ("aeolian", "A4", "A5", "F5"),
    ("locrian", "B4", "B5", "F5"),
]
WHITE = ["C", "D", "E", "F", "G", "A", "B"]


def scale_notes(start):
    i = WHITE.index(start[0])
    octave = int(start[1:])
    out = []
    for k in range(8):
        letter = WHITE[(i + k) % 7]
        o = octave + (i + k) // 7
        out.append(f"{letter}{o}")
    return out


for name, start, end, char in MODES:
    notes = scale_notes(start)
    assert notes[-1] == end, (name, notes)
    labels = {n: str(i + 1) for i, n in enumerate(notes)}
    colours = {char: "salmon"} if char else {}
    save(keyboard(start, end, marks=notes, labels=labels, colours=colours),
         STAGE + f"modes-{start[0].lower()}-{name}.svg")

# C Lydian: the one black key
notes = ["C4", "D4", "E4", "F#4", "G4", "A4", "B4", "C5"]
save(keyboard("C4", "C5", marks=notes, labels={n: str(i + 1) for i, n in enumerate(notes)},
              colours={"F#4": "salmon"}), STAGE + "modes-c-lydian-sharp-four.svg")
print("modes done")
