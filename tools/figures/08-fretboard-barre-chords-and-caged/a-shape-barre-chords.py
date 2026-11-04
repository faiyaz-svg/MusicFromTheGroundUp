from _common import *
F = STAGE + "a-shape-barre-chords-"
save(chord_diagram("B", ["x", 2, 4, 4, 4, 2], [None, 1, 3, 3, 3, 1], barre=(2, 5, 1), base_fret=2, highlight_root=5), F + "b.svg")
save(chord_diagram("Bm", ["x", 2, 4, 4, 3, 2], [None, 1, 3, 4, 2, 1], barre=(2, 5, 1), base_fret=2, highlight_root=5), F + "bm.svg")
save(chord_diagram("Bb", ["x", 1, 3, 3, 3, 1], [None, 1, 3, 3, 3, 1], barre=(1, 5, 1), highlight_root=5), F + "bb.svg")
save(chord_diagram("Bbm", ["x", 1, 3, 3, 2, 1], [None, 1, 3, 4, 2, 1], barre=(1, 5, 1), highlight_root=5), F + "bbm.svg")
save(chord_diagram("C", ["x", 3, 5, 5, 5, 3], [None, 1, 3, 3, 3, 1], barre=(3, 5, 1), base_fret=3, highlight_root=5), F + "c-fret-3.svg")
save(chord_diagram("A", ["x", 0, 2, 2, 2, 0], [None, None, 1, 2, 3, None], highlight_root=5), F + "a.svg")
print("done")
