from _common import *
from _common import _verovio, _text, _svg

F = STAGE + "bass-clef-and-grand-staff-"

abc = """X:1
M:none
L:1/1
K:C clef=bass
w: C3 D3 E3 F3 G3 A3 B3 C4
C, D, E, F, G, A, B, C |]
"""
save(_verovio(abc, "The notes C3, D3, E3, F3, G3, A3, B3 and C4 on the bass staff, with C4 on a ledger line above the staff"),
     F + "notes-c3-to-c4.svg")

save(grand([None, "E4", "C4", None], ["C3", None, None, "G3"], "The grand staff: treble staff above, bass staff below, joined by a brace. C3 and G3 are in the bass staff, C4 and E4 in the treble staff"),
     F + "grand-staff.svg")

save(grand(["C4"], ["C4"], "Middle C written twice: on a ledger line below the treble staff, and on a ledger line above the bass staff"),
     F + "middle-c-twice.svg")

save(keyboard("C3", "C4", marks=["C4"], show_names=True, middle_c=True),
     F + "keyboard-c3-to-c4.svg")
print("bass clef done")
