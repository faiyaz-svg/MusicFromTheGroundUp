from _common import *
from _common import _verovio, _text, _svg

F = STAGE + "g-and-f-positions-"
rh = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
lh = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}


def pos(start_w, notes_w, hand):
    fing = {n: (rh if hand == "rh" else lh)[i + 1] for i, n in enumerate(notes_w)}
    return keyboard(notes_w[0], notes_w[-1], marks=notes_w, fingers=fing, show_names=True)


save(pos(0, ["G4", "A4", "B4", "C5", "D5"], "rh"), F + "rh-g-position.svg")
save(pos(0, ["G2", "A2", "B2", "C3", "D3"], "lh"), F + "lh-g-position.svg")
save(pos(0, ["F4", "G4", "A4", "B4", "C5"], "rh"), F + "rh-f-position.svg")
save(pos(0, ["F2", "G2", "A2", "B2", "C3"], "lh"), F + "lh-f-position.svg")

save(grand(["G4", "A4", "B4", "C5", "D5"], ["G2", "A2", "B2", "C3", "D3"],
           "G position on the grand staff. Right hand G4 to D5 in the treble staff, left hand G2 to D3 in the bass staff"),
     F + "g-position-staff.svg")
save(grand(["F4", "G4", "A4", "B4", "C5"], ["F2", "G2", "A2", "B2", "C3"],
           "F position on the grand staff. Right hand F4 to C5 in the treble staff, left hand F2 to C3 in the bass staff"),
     F + "f-position-staff.svg")
print("positions done")
