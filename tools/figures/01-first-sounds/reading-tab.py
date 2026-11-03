from _common import *
from _common import _text

grey = "#ddd"
marks = []
names = {(1, 0): "E", (1, 1): "F", (1, 2): "", (1, 3): "G", (2, 0): "B", (2, 1): "C", (2, 2): "", (2, 3): "D"}
for (s, f), n in names.items():
    marks.append({"string": s, "fret": f, "label": n, "colour": grey if n == "" else "yellow"})
fb = fretboard(3, marks=marks, highlight_strings=[1, 2], inlays=False)
body = "".join(_text(4 + 56 + 3 * 56 + 6, 20 + (s - 1) * 26 + 4, f"string {s}", size=12, fill=INK, anchor="start")
               for s in (1, 2))
save(widen(fb, 70, body), "01-first-sounds/reading-tab-strings-1-and-2.svg")
print("tab done")
