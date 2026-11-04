from _common import *
F = STAGE + "fretboard-reading-"
for name, lo, hi in (("5th", 5, 8), ("7th", 7, 10)):
    marks = [{"string": st, "fret": f, "label": nm(st, f), "colour": "yellow"}
             for st in range(1, 7) for f in range(lo, hi + 1) if "#" not in nm(st, f)]
    save(fretboard(hi, marks=marks, start_fret=lo), F + f"position-{name}.svg")
print("done")
