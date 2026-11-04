from _common import *
F = STAGE + "e-shape-barre-chords-"
# frets and fingers are listed from string 6 to string 1
save(chord_diagram("F", [1, 3, 3, 2, 1, 1], [1, 3, 4, 2, 1, 1], barre=(1, 6, 1), highlight_root=6), F + "f.svg")
save(chord_diagram("Fm", [1, 3, 3, 1, 1, 1], [1, 3, 4, 1, 1, 1], barre=(1, 6, 1), highlight_root=6), F + "fm.svg")
save(chord_diagram("G", [3, 5, 5, 4, 3, 3], [1, 3, 4, 2, 1, 1], barre=(3, 6, 1), base_fret=3, highlight_root=6), F + "g.svg")
save(chord_diagram("Gm", [3, 5, 5, 3, 3, 3], [1, 3, 4, 1, 1, 1], barre=(3, 6, 1), base_fret=3, highlight_root=6), F + "gm.svg")
# the open E and Em for comparison
save(chord_diagram("E", [0, 2, 2, 1, 0, 0], [None, 2, 3, 1, None, None], highlight_root=6), F + "e.svg")
save(chord_diagram("Em", [0, 2, 2, 0, 0, 0], [None, 2, 3, None, None, None], highlight_root=6), F + "em.svg")
# the partial barre steps
save(chord_diagram("Step 1", ["x", "x", "x", "x", 1, 1], [None] * 4 + [1, 1], barre=(1, 2, 1), highlight_root=None), F + "step-1.svg")
save(chord_diagram("Step 2", ["x", "x", 2, 1, 1, 1], [None, None, 2, 1, 1, 1], barre=(1, 4, 1)), F + "step-2.svg")
print("done")
