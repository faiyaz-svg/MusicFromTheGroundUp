from _common import *
F = STAGE + "caged-scale-shapes-"
C = {0, 2, 4, 5, 7, 9, 11}
WINDOWS = {"c": (0, 4), "a": (3, 7), "g": (5, 9), "e": (8, 12), "d": (10, 14)}
for k, (lo, hi) in WINDOWS.items():
    marks = []
    for st in range(1, 7):
        for f in range(lo, hi + 1):
            n = nm(st, f)
            pc = (OPEN[st] + f) % 12
            if pc in C:
                col = "salmon" if n == "C" else ("yellow" if n in ("E", "G") else "#ffffff")
                marks.append({"string": st, "fret": f, "label": n, "colour": col})
    per = [sum(1 for m in marks if m["string"] == st) for st in range(1, 7)]
    assert per == [3] * 6, (k, per)
    svg = fretboard(hi, marks=marks, start_fret=lo)
    if lo == 0:
        svg = with_strings(svg)
    save(svg, F + f"{k}-shape.svg")
print("done")
