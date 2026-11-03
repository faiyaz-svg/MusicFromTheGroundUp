from _common import *

F = "03-the-major-scale-and-keys/the-major-scale-"
deg = lambda notes: {n: str(i + 1) for i, n in enumerate(notes)}

c = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]
k = keyboard("C4", "C5", marks=c, labels=deg(c))
save(step_brackets(k, "C4", "C5", c), F + "c-major.svg")

g = ["G4", "A4", "B4", "C5", "D5", "E5", "F#5", "G5"]
k = keyboard("G4", "G5", marks=g, labels=deg(g))
save(step_brackets(k, "G4", "G5", g), F + "g-major.svg")
print("major scale done")
