from _common import *

# frets and fingers are listed from string 6 to string 1
open_chords = [
    ("Cmaj7", ["x", 3, 2, 0, 0, 0], [None, 3, 2, None, None, None], 5, "cmaj7"),
    ("Am7", ["x", 0, 2, 0, 1, 0], [None, None, 2, None, 1, None], 5, "am7"),
    ("Fmaj7", ["x", "x", 3, 2, 1, 0], [None, None, 3, 2, 1, None], 4, "fmaj7"),
    ("G7", [3, 2, 0, 0, 0, 1], [3, 2, None, None, None, 1], 6, "g7"),
]
for name, frets, fingers, root, slug in open_chords:
    save(chord_diagram(name, frets, fingers, highlight_root=root), STAGE + f"maj7-and-min7-barre-shapes-{slug}.svg")

# movable shapes with the root on string 5, drawn as C chords at fret 3
moving = [
    ("Cmaj7", ["x", 3, 5, 4, 5, 3], [None, 1, 3, 2, 4, 1], "cmaj7-fret3"),
    ("Cm7", ["x", 3, 5, 3, 4, 3], [None, 1, 3, 1, 2, 1], "cm7-fret3"),
    ("C7", ["x", 3, 5, 3, 5, 3], [None, 1, 3, 1, 4, 1], "c7-fret3"),
]
for name, frets, fingers, slug in moving:
    save(chord_diagram(name, frets, fingers, barre=(3, 5, 1), base_fret=3, highlight_root=5),
         STAGE + f"maj7-and-min7-barre-shapes-{slug}.svg")

# root on string 6, drawn as F chords at fret 1
low = [
    ("F7", [1, 3, 1, 2, 1, 1], [1, 3, 1, 2, 1, 1], "f7-fret1"),
    ("Fm7", [1, 3, 1, 1, 1, 1], [1, 3, 1, 1, 1, 1], "fm7-fret1"),
]
for name, frets, fingers, slug in low:
    save(chord_diagram(name, frets, fingers, barre=(1, 6, 1), highlight_root=6),
         STAGE + f"maj7-and-min7-barre-shapes-{slug}.svg")
print("maj7 shapes done")
