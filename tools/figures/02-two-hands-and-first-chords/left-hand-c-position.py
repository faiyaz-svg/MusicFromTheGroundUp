from _common import *
from _common import _verovio, _text, _svg

F = STAGE + "left-hand-c-position-"
save(keyboard("C3", "G3", marks=["C3", "D3", "E3", "F3", "G3"],
              fingers={"C3": 5, "D3": 4, "E3": 3, "F3": 2, "G3": 1}, show_names=True),
     F + "lh-c-position.svg")

abc = """X:1
M:none
L:1/1
K:C clef=bass
w: C3 D3 E3 F3 G3
C, D, E, F, G, |]
"""
save(_verovio(abc, "The notes C3, D3, E3, F3 and G3 on the bass staff"), F + "notes-c3-to-g3.svg")
print("lh c done")
