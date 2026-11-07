from _common import *
from _common import _text, _svg

def strip(y, title, letters, w=60):
    out = [_text(16, y + 12, title, size=13, fill=INK, anchor="start", weight="bold")]
    x = 16
    for k, (ltr, fill) in enumerate(letters):
        out.append(rect(x, y + 22, w, 40, fill, INK, 1.5))
        out.append(_text(x + w / 2, y + 48, ltr, size=16, fill=INK, weight="bold"))
        x += w
    return "".join(out)

Y, S, T, B, L = YELLOW, SKY, TEAL, SALMON, LAVENDER
rows = [
 ("Binary: A B (each half repeated)", [("A", Y), ("B", S)]),
 ("Ternary: A B A", [("A", Y), ("B", S), ("A", Y)]),
 ("Rondo: A B A C A", [("A", Y), ("B", S), ("A", Y), ("C", T), ("A", Y)]),
 ("Theme and variations", [("A", Y), ("A1", S), ("A2", T), ("A3", B)]),
 ("Verse and chorus", [("V", S), ("C", Y), ("V", S), ("C", Y)]),
]
body = "".join(strip(8 + i * 76, t, l) for i, (t, l) in enumerate(rows))
h = 8 + len(rows) * 76
save(_svg(640, h, "Five forms drawn as strips of coloured boxes: binary AB, ternary ABA, rondo ABACA, theme and variations, and verse and chorus", body), FOLDER + "/phrases-and-form-forms.svg")
print("done")
