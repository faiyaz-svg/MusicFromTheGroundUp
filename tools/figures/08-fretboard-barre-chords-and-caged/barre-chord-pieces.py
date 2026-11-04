from _common import *
F = STAGE + "barre-chord-pieces-"
save(chord_diagram("F#m", [2, 4, 4, 2, 2, 2], [1, 3, 4, 1, 1, 1], barre=(2, 6, 1), base_fret=2, highlight_root=6), F + "fsharp-m.svg")
save(chord_diagram("Gm", [3, 5, 5, 3, 3, 3], [1, 3, 4, 1, 1, 1], barre=(3, 6, 1), base_fret=3, highlight_root=6), F + "gm.svg")
print("done")
save(chord_diagram("F (small)", ["x", "x", 3, 2, 1, 1], [None, None, 3, 2, 1, 1], barre=(1, 2, 1), highlight_root=4), F + "f-small.svg")
