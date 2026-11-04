from _common import *

save(chord_diagram("E5", [0, 2, 2, "x", "x", "x"], [None, 1, 2, None, None, None], highlight_root=6),
     STAGE + "power-chords-e5.svg")
save(chord_diagram("A5", [5, 7, 7, "x", "x", "x"], [1, 3, 4, None, None, None], base_fret=5, highlight_root=6),
     STAGE + "power-chords-a5.svg")
save(chord_diagram("G5", [3, 5, 5, "x", "x", "x"], [1, 3, 4, None, None, None], base_fret=3, highlight_root=6),
     STAGE + "power-chords-g5.svg")
print("power chords done")
