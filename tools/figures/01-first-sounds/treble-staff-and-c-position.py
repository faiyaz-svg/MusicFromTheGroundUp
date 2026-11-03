from _common import *
from _common import _verovio

F = "01-first-sounds/treble-staff-and-c-position-"
abc = """X:1
M:none
L:1/1
K:C clef=treble
w: C4 D4 E4 F4 G4
C D E F G |]
"""
save(_verovio(abc, "The notes C4, D4, E4, F4 and G4 on the treble staff, with C4 on a ledger line below the staff"),
     F + "notes-c4-to-g4.svg")

save(keyboard("C4", "G4", marks=["C4", "D4", "E4", "F4", "G4"],
              fingers={"C4": 1, "D4": 2, "E4": 3, "F4": 4, "G4": 5}, show_names=False, middle_c=True),
     F + "c-position.svg")
print("staff done")
