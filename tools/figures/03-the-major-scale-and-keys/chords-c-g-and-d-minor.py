from _common import *

F = "03-the-major-scale-and-keys/chords-c-g-and-d-minor-"
save(chord_diagram("C", ["x", 3, 2, 0, 1, 0], [None, 3, 2, None, 1, None], highlight_root=5), F + "c.svg")
save(chord_diagram("G", [3, 2, 0, 0, 0, 3], [3, 2, None, None, None, 4], highlight_root=6), F + "g.svg")
save(chord_diagram("Dm", ["x", "x", 0, 2, 3, 1], [None, None, None, 2, 3, 1], highlight_root=4), F + "dm.svg")
print("chords done")
