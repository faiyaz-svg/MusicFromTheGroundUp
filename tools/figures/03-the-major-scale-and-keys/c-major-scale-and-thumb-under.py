from _common import *

F = "03-the-major-scale-and-keys/c-major-scale-and-thumb-under-"
rh = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]
save(keyboard("C4", "C5", marks=rh, fingers=dict(zip(rh, [1, 2, 3, 1, 2, 3, 4, 5]))), F + "rh.svg")
lh = ["C3", "D3", "E3", "F3", "G3", "A3", "B3", "C4"]
save(keyboard("C3", "C4", marks=lh, fingers=dict(zip(lh, [5, 4, 3, 2, 1, 3, 2, 1]))), F + "lh.svg")
print("c scale done")
