from _common import *

# frets string 6 -> string 1; fingers; root string
chords = {
    "a7": ("A7", ["x", 0, 2, 0, 2, 0], [None, None, 2, None, 3, None], 5),
    "d7": ("D7", ["x", "x", 0, 2, 1, 2], [None, None, None, 2, 1, 3], 4),
    "e7": ("E7", [0, 2, 0, 1, 0, 0], [None, 2, None, 1, None, None], 6),
    "b7": ("B7", ["x", 2, 1, 2, 0, 2], [None, 2, 1, 3, None, 4], 5),
}
for slug, (name, frets, fingers, root) in chords.items():
    save(chord_diagram(name, frets, fingers, highlight_root=root), STAGE + "open-seventh-chords-" + slug + ".svg")
print("sevenths done")
