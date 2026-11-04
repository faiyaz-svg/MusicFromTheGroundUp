from _common import *

# frets and fingers are listed from string 6 to string 1
save(chord_diagram("E", [0, 2, 2, 1, 0, 0], [None, 2, 3, 1, None, None], highlight_root=6),
     STAGE + "chords-e-and-a-e.svg")
save(chord_diagram("A", ["x", 0, 2, 2, 2, 0], [None, None, 1, 2, 3, None], highlight_root=5),
     STAGE + "chords-e-and-a-a.svg")
save(chord_diagram("Am", ["x", 0, 2, 2, 1, 0], [None, None, 2, 3, 1, None], highlight_root=5),
     STAGE + "chords-a-minor-and-d-am.svg")
save(chord_diagram("D", ["x", "x", 0, 2, 3, 2], [None, None, None, 1, 3, 2], highlight_root=4),
     STAGE + "chords-a-minor-and-d-d.svg")
print("chords done")
