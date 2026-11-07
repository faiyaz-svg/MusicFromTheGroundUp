from _common import *

# F Lydian with left-hand open fifths F and G under it
notes = ["F4", "G4", "A4", "B4", "C5", "D5", "E5", "F5"]
save(keyboard("F4", "F5", marks=notes, labels={n: str(i + 1) for i, n in enumerate(notes)},
              colours={"B4": "salmon"}), STAGE + "lydian-wonder-f-lydian.svg")
# The I and II chords in F Lydian: F A C and G B D
save(keyboard("F4", "D5", marks=["F4", "A4", "C5", "G4", "B4", "D5"],
              colours={"F4": "teal", "A4": "teal", "C5": "teal", "G4": "yellow", "B4": "salmon", "D5": "yellow"},
              labels={"F4": "F", "A4": "A", "C5": "C", "G4": "G", "B4": "B", "D5": "D"}),
     STAGE + "lydian-wonder-chords.svg")
print("lydian-wonder done")
