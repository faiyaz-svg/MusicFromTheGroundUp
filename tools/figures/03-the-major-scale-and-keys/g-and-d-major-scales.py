from _common import *

F = "03-the-major-scale-and-keys/g-and-d-major-scales-"
fr = [1, 2, 3, 1, 2, 3, 4, 5]
fl = [5, 4, 3, 2, 1, 3, 2, 1]
g_rh = ["G4", "A4", "B4", "C5", "D5", "E5", "F#5", "G5"]
save(keyboard("G4", "G5", marks=g_rh, fingers=dict(zip(g_rh, fr))), F + "g-rh.svg")
g_lh = ["G3", "A3", "B3", "C4", "D4", "E4", "F#4", "G4"]
save(keyboard("G3", "G4", marks=g_lh, fingers=dict(zip(g_lh, fl))), F + "g-lh.svg")
d_rh = ["D4", "E4", "F#4", "G4", "A4", "B4", "C#5", "D5"]
save(keyboard("D4", "D5", marks=d_rh, fingers=dict(zip(d_rh, fr))), F + "d-rh.svg")
d_lh = ["D3", "E3", "F#3", "G3", "A3", "B3", "C#4", "D4"]
save(keyboard("D3", "D4", marks=d_lh, fingers=dict(zip(d_lh, fl))), F + "d-lh.svg")
print("g d done")
