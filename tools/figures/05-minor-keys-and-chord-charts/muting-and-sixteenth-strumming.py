from _common import *

F = FOLDER + "/muting-and-sixteenth-strumming-"
P1 = ["D", "U"] * 8
P2 = ["D", "-", "D", "U"] * 4
P3 = ["D", "-", "D", "U", "x", "-", "D", "U", "D", "-", "D", "U", "x", "-", "D", "U"]
save(strum_grid(P1, "Pattern 1: down-up on every sixteenth note, 16 strokes in a bar"), F + "pattern-1.svg")
save(strum_grid(P2, "Pattern 2: down on each beat, down on the and, up on the a, with the e left out"), F + "pattern-2.svg")
save(strum_grid(P3, "Pattern 3: pattern 2 with a chuck on beats 2 and 4"), F + "pattern-3.svg")
print("strum done")
