from _common import *
from _common import _text

F = "03-the-major-scale-and-keys/reading-notation-on-guitar-"
nat = {6: {0: "E", 1: "F", 3: "G"}, 5: {0: "A", 2: "B", 3: "C"}, 4: {0: "D", 2: "E", 3: "F"},
       3: {0: "G", 2: "A", 4: "B"}, 2: {0: "B", 1: "C", 3: "D"}, 1: {0: "E", 1: "F", 3: "G"}}
marks = [{"string": s, "fret": f, "label": n, "colour": "yellow"} for s, d in nat.items() for f, n in d.items()]
fb = fretboard(4, marks=marks)
body = "".join(_text(14, 20 + (s - 1) * 26 + 4, str(s), size=12, fill=INK, weight="bold") for s in range(1, 7))
save(widen(fb, 0, body), F + "first-position.svg")
print("guitar notation done")
