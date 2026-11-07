from _common import *

save(keyboard("F4", "C5", colours={"F4": "teal", "A4": "yellow", "C5": "teal"}, labels={"F4": "F", "A4": "A", "C5": "C"}),
     STAGE + "minor-iv-and-the-picardy-third-f-major.svg")
save(keyboard("F4", "C5", colours={"F4": "teal", "G#4": "salmon", "C5": "teal"}, labels={"F4": "F", "G#4": "Ab", "C5": "C"}),
     STAGE + "minor-iv-and-the-picardy-third-f-minor.svg")
save(chord_diagram("Fm", [1, 3, 3, 1, 1, 1], [1, 3, 4, 1, 1, 1], barre=(1, 6, 1), highlight_root=6),
     STAGE + "minor-iv-and-the-picardy-third-fm.svg")
save(chord_diagram("E", [0, 2, 2, 1, 0, 0], [None, 2, 3, 1, None, None], highlight_root=6),
     STAGE + "minor-iv-and-the-picardy-third-e.svg")
print("minor iv done")
