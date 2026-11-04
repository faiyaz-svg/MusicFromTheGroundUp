from _common import *
from _common import _text, _svg

# Strum pattern grids for one bar of 6/8: six eighth positions.
def grid(pattern, alt, _x, fname, accents=(0, 3)):
    W, H = 600, 150
    x0, step = 50, 84
    body = ""
    counts = ["1", "2", "3", "4", "5", "6"]
    for i in range(6):
        x = x0 + i * step + step / 2
        if i in accents:
            body += rect(x0 + i * step + 4, 8, step - 8, 128, fill="#fff6cc", stroke="#e0b800", sw=1)
        body += _text(x, 30, counts[i], size=20, fill=INK, weight="bold")
        p = pattern[i]
        if p == "D":
            body += arrow(x, 48, up=False, c=INK)
        elif p == "U":
            body += arrow(x, 48, up=True, c="#555")
        else:
            body += _text(x, 80, "-", size=20, fill=LABEL)
        body += _text(x, 122, p if p != "." else "", size=15, fill=INK, weight="bold")
    save(_svg(W, H, alt, body), STAGE + fname)

grid("D..D..", "Strum pattern for one bar of 6/8: down strokes on counts 1 and 4, and nothing on the others", "", "six-eight-strumming-pattern-1.svg")
grid("DDDDDD", "Strum pattern for one bar of 6/8: a down stroke on every count, 1 and 4 played louder", "", "six-eight-strumming-pattern-2.svg")
grid("D.UD.U", "Strum pattern for one bar of 6/8: down on counts 1 and 4, up on counts 3 and 6, nothing on 2 and 5", "", "six-eight-strumming-pattern-3.svg")
print("strum done")
