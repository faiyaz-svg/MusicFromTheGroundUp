from _common import *
from _common import _text

F = "03-the-major-scale-and-keys/notes-on-strings-6-and-5-"
s6 = {0: "E", 1: "F", 3: "G", 5: "A", 7: "B", 8: "C", 10: "D", 12: "E"}
s5 = {0: "A", 2: "B", 3: "C", 5: "D", 7: "E", 8: "F", 10: "G", 12: "A"}
marks = []
for f, n in s6.items():
    marks.append({"string": 6, "fret": f, "label": n, "colour": "yellow"})
for f, n in s5.items():
    marks.append({"string": 5, "fret": f, "label": n, "colour": "lavender"})
fb = fretboard(12, marks=marks, highlight_strings=[5, 6])
body = _text(14, 20 + 4 * 26 + 4, "5", size=12, fill=INK, weight="bold") + _text(14, 20 + 5 * 26 + 4, "6", size=12, fill=INK, weight="bold")
save(widen(fb, 0, body), F + "natural-notes.svg")

# the 5th-fret rule: fret 5 of one string equals the open string next to it
marks = [
    {"string": 6, "fret": 5, "label": "A", "colour": "yellow"},
    {"string": 5, "fret": 0, "label": "A", "colour": "yellow"},
    {"string": 5, "fret": 5, "label": "D", "colour": "lavender"},
    {"string": 4, "fret": 0, "label": "D", "colour": "lavender"},
]
fb = fretboard(5, marks=marks, highlight_strings=[4, 5, 6])
save(fb, F + "fifth-fret.svg")
print("strings done")
