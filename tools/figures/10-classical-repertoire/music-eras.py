from _common import *
from _common import _text, _svg

W, H = 700, 285
x0, x1 = 30, 670
y0, y1 = 1600, 2000
def X(y): return x0 + (y - y0) / (y1 - y0) * (x1 - x0)
eras = [("Baroque", 1600, 1750, YELLOW), ("Classical", 1750, 1820, SKY),
        ("Romantic", 1820, 1900, TEAL), ("20th century", 1900, 2000, SALMON)]
out = []
for nm, a, b, c in eras:
    out.append(rect(X(a), 70, X(b) - X(a), 56, c, INK, 1.5))
    out.append(_text((X(a) + X(b)) / 2, 94, nm, size=13 if b - a > 60 else 12, fill=INK, weight="bold"))
    out.append(_text((X(a) + X(b)) / 2, 112, f"{a}-{b}", size=11, fill=INK))
for yr in range(1600, 2001, 50):
    out.append(line(X(yr), 126, X(yr), 134, 1.2))
    out.append(_text(X(yr), 148, str(yr), size=11, fill=LABEL))
# pieces from the book (composer's years)
marks = [("Petzold", 1677, 1733, 175), ("Clementi", 1752, 1832, 197), ("Sor", 1778, 1839, 219),
         ("Schumann", 1810, 1856, 241), ("Burgmüller", 1806, 1874, 263)]
for nm, a, b, y in marks:
    out.append(line(X(a), y, X(b), y, 5, INK))
    out.append(_text(X(a) - 6 if nm != "Schumann" else X(a) - 6, y + 4, nm, size=11, fill=INK, anchor="end"))
out.append(_text(350, 30, "Eras of classical music, with the lifespans of some composers in this book", size=13, fill=INK, weight="bold"))
save(_svg(W, H, "Timeline from 1600 to 2000: Baroque 1600 to 1750, Classical 1750 to 1820, Romantic 1820 to 1900, 20th century 1900 to 2000, with bars for the lifespans of Petzold, Clementi, Sor, Schumann and Burgm\u00fcller",
          "".join(out)), FOLDER + "/music-eras-timeline.svg")
print("done")
