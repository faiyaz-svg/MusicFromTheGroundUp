from _common import *

# frets and fingers run from string 6 to string 1
shapes = [
    ("Fmaj7", ["x", "x", 3, 2, 1, 0], [None, None, 3, 2, 1, None], 4, None, "fmaj7"),
    ("G7", [3, 2, 0, 0, 0, 1], [3, 2, None, None, None, 1], 6, None, "g7"),
    ("Em7", [0, 2, 0, 0, 0, 0], [None, 2, None, None, None, None], 6, None, "em7"),
    ("Am", ["x", 0, 2, 2, 1, 0], [None, None, 2, 3, 1, None], 5, None, "am"),
    ("Cmaj7", ["x", 3, 2, 0, 0, 0], [None, 3, 2, None, None, None], 5, None, "cmaj7"),
    ("D7", ["x", "x", 0, 2, 1, 2], [None, None, None, 2, 1, 3], 4, None, "d7"),
    ("Bm7", ["x", 2, 4, 2, 3, 2], [None, 1, 3, 1, 2, 1], 5, (2, 5, 1), "bm7"),
]
for name, frets, fingers, root, barre, slug in shapes:
    base_fret = 2 if barre else 1
    save(chord_diagram(name, frets, fingers, barre=barre, base_fret=base_fret, highlight_root=root),
         STAGE + f"royal-road-on-guitar-{slug}.svg")
print("royal-road-on-guitar done")
