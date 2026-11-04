from _common import *

# frets and fingers are listed from string 6 to string 1
chords = [
    ("Dsus2", ["x", "x", 0, 2, 3, 0], [None, None, None, 1, 3, None], 4, "dsus2"),
    ("Dsus4", ["x", "x", 0, 2, 3, 3], [None, None, None, 1, 3, 4], 4, "dsus4"),
    ("Asus2", ["x", 0, 2, 2, 0, 0], [None, None, 1, 2, None, None], 5, "asus2"),
    ("Asus4", ["x", 0, 2, 2, 3, 0], [None, None, 1, 2, 3, None], 5, "asus4"),
    ("Cadd9", ["x", 3, 2, 0, 3, 3], [None, 2, 1, None, 3, 4], 5, "cadd9"),
    ("Em7", [0, 2, 0, 0, 0, 0], [None, 2, None, None, None, None], 6, "em7"),
]
for name, frets, fingers, root, slug in chords:
    save(chord_diagram(name, frets, fingers, highlight_root=root), STAGE + f"sus-and-add9-chords-{slug}.svg")
print("sus chords done")
