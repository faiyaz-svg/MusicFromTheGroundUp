from _common import *

chords = [
    ("Am", ["x", 0, 2, 2, 1, 0], [None, None, 2, 3, 1, None], 5, "am"),
    ("Dm", ["x", "x", 0, 2, 3, 1], [None, None, None, 2, 3, 1], 4, "dm"),
    ("E", [0, 2, 2, 1, 0, 0], [None, 2, 3, 1, None, None], 6, "e"),
]
for name, frets, fingers, root, slug in chords:
    save(chord_diagram(name, frets, fingers, highlight_root=root), STAGE + f"minor-key-progressions-{slug}.svg")
save(chord_diagram("F", [1, 3, 3, 2, 1, 1], [1, 3, 4, 2, 1, 1], barre=(1, 6, 1), highlight_root=6),
     STAGE + "minor-key-progressions-f.svg")
print("minor-key-progressions done")
