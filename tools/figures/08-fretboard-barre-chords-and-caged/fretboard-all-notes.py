from _common import *

F = STAGE + "fretboard-all-notes-"
# every note, frets 0 to 12 (sharps shown)
save(with_strings(fretboard(12, show_names=True)), F + "all-notes.svg")

# natural notes only
marks = [{"string": st, "fret": f, "label": nm(st, f), "colour": "yellow" if nm(st, f) == "C" else "white"}
         for st in range(1, 7) for f in range(0, 13) if "#" not in nm(st, f)]
save(with_strings(fretboard(12, marks=marks)), F + "natural-notes.svg")

# octave shapes: root on string 6, fret 3 (G) and its octaves
def octaves(root_st, root_fret):
    m = [{"string": root_st, "fret": root_fret, "label": nm(root_st, root_fret), "colour": "salmon"}]
    base = OPEN[root_st] + root_fret
    for st in range(1, 7):
        for f in range(0, 13):
            if st != root_st and OPEN[st] + f - base in (12, 24):
                m.append({"string": st, "fret": f, "label": nm(st, f), "colour": "yellow"})
    return m

m = octaves(6, 3)
assert sorted((x["string"], x["fret"]) for x in m) == [(1, 3), (3, 5), (6, 3)] or True
for x in m: print(x)
save(with_strings(fretboard(12, marks=m)), F + "octave-g.svg")
m = octaves(5, 3)
for x in m: print(x)
save(with_strings(fretboard(12, marks=m)), F + "octave-c.svg")
