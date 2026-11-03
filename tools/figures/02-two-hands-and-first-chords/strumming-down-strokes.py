from _common import *
from _common import _verovio, _text, _svg

# A chord chart row: four bars, each with a chord name and four rhythm slashes.
bars = ["Em", "Em", "A", "A"]
bw, h = 130, 90
w = 20 + bw * 4 + 20
body = ""
x0, y0 = 20, 30
body += line(x0, y0, x0, y0 + 50, 2)
for i, c in enumerate(bars):
    x = x0 + i * bw
    body += _text(x + 8, y0 - 6, c, size=18, fill=INK, anchor="start", weight="bold")
    body += line(x + bw, y0, x + bw, y0 + 50, 2)
    for b in range(4):
        sx = x + 18 + b * 28
        body += line(sx, y0 + 40, sx + 16, y0 + 10, 3)
    if i % 2 == 0:
        pass
body += line(x0, y0 + 25, x0 + bw * 4, y0 + 25, 0.0001, "#fff")
body += _text(x0 + bw * 2, y0 + 78, "Four slashes in each bar: strum a down stroke on every beat", size=13, fill=LABEL)
save(_svg(w, 120, "A chord chart: four bars of 4/4. Bars 1 and 2 are Em, bars 3 and 4 are A, with four slashes in each bar", body),
     STAGE + "strumming-down-strokes-chart.svg")
print("strum done")
