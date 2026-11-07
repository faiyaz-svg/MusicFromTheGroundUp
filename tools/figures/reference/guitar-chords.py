"""Chord diagrams for the guitar chord shapes page.
Frets and fingers are listed from string 6 to string 1."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from musicfigs import chord_diagram, save

F = "reference/guitar-chords-"
X = "x"
N = None

# (name, frets, fingers, root string, slug)
open_chords = [
    ("E", [0, 2, 2, 1, 0, 0], [N, 2, 3, 1, N, N], 6, "e"),
    ("Em", [0, 2, 2, 0, 0, 0], [N, 2, 3, N, N, N], 6, "em"),
    ("A", [X, 0, 2, 2, 2, 0], [N, N, 1, 2, 3, N], 5, "a"),
    ("Am", [X, 0, 2, 2, 1, 0], [N, N, 2, 3, 1, N], 5, "am"),
    ("D", [X, X, 0, 2, 3, 2], [N, N, N, 1, 3, 2], 4, "d"),
    ("Dm", [X, X, 0, 2, 3, 1], [N, N, N, 2, 3, 1], 4, "dm"),
    ("C", [X, 3, 2, 0, 1, 0], [N, 3, 2, N, 1, N], 5, "c"),
    ("G", [3, 2, 0, 0, 0, 3], [3, 2, N, N, N, 4], 6, "g"),
    ("A7", [X, 0, 2, 0, 2, 0], [N, N, 2, N, 3, N], 5, "a7"),
    ("D7", [X, X, 0, 2, 1, 2], [N, N, N, 2, 1, 3], 4, "d7"),
    ("E7", [0, 2, 0, 1, 0, 0], [N, 2, N, 1, N, N], 6, "e7"),
    ("B7", [X, 2, 1, 2, 0, 2], [N, 2, 1, 3, N, 4], 5, "b7"),
    ("Cmaj7", [X, 3, 2, 0, 0, 0], [N, 3, 2, N, N, N], 5, "cmaj7"),
    ("Am7", [X, 0, 2, 0, 1, 0], [N, N, 2, N, 1, N], 5, "am7"),
    ("Fmaj7", [X, X, 3, 2, 1, 0], [N, N, 3, 2, 1, N], 4, "fmaj7"),
    ("Dsus2", [X, X, 0, 2, 3, 0], [N, N, N, 1, 3, N], 4, "dsus2"),
    ("Dsus4", [X, X, 0, 2, 3, 3], [N, N, N, 1, 3, 4], 4, "dsus4"),
    ("Asus2", [X, 0, 2, 2, 0, 0], [N, N, 1, 2, N, N], 5, "asus2"),
    ("Asus4", [X, 0, 2, 2, 3, 0], [N, N, 1, 2, 3, N], 5, "asus4"),
    ("Cadd9", [X, 3, 2, 0, 3, 3], [N, 2, 1, N, 3, 4], 5, "cadd9"),
    ("Em7", [0, 2, 0, 0, 0, 0], [N, 2, N, N, N, N], 6, "em7"),
]
for name, frets, fingers, root, slug in open_chords:
    save(chord_diagram(name, frets, fingers, highlight_root=root), F + slug + ".svg")

# power chords: root on string 6 (E5, G5, A5) and on string 5 (A5 open-position, D5)
save(chord_diagram("E5", [0, 2, 2, X, X, X], [N, 1, 2, N, N, N], highlight_root=6), F + "e5.svg")
save(chord_diagram("G5", [3, 5, 5, X, X, X], [1, 3, 4, N, N, N], base_fret=3, highlight_root=6), F + "g5.svg")
save(chord_diagram("A5", [5, 7, 7, X, X, X], [1, 3, 4, N, N, N], base_fret=5, highlight_root=6), F + "a5.svg")
save(chord_diagram("D5", [X, 5, 7, 7, X, X], [N, 1, 3, 4, N, N], base_fret=5, highlight_root=5), F + "d5.svg")

# E-shape movable shapes, drawn as F chords at fret 1 (root on string 6)
e_shapes = [
    ("F", [1, 3, 3, 2, 1, 1], [1, 3, 4, 2, 1, 1], (1, 6, 1), "e-shape-major"),
    ("Fm", [1, 3, 3, 1, 1, 1], [1, 3, 4, 1, 1, 1], (1, 6, 1), "e-shape-minor"),
    ("F7", [1, 3, 1, 2, 1, 1], [1, 3, 1, 2, 1, 1], (1, 6, 1), "e-shape-7"),
    ("Fm7", [1, 3, 1, 1, 1, 1], [1, 3, 1, 1, 1, 1], (1, 6, 1), "e-shape-m7"),
    ("Fmaj7", [1, X, 2, 2, 1, X], [1, N, 3, 4, 2, N], None, "e-shape-maj7"),
]
for name, frets, fingers, barre, slug in e_shapes:
    save(chord_diagram(name, frets, fingers, barre=barre, highlight_root=6), F + slug + ".svg")

# A-shape movable shapes, drawn as C chords at fret 3 (root on string 5)
a_shapes = [
    ("C", [X, 3, 5, 5, 5, 3], [N, 1, 3, 3, 3, 1], "a-shape-major"),
    ("Cm", [X, 3, 5, 5, 4, 3], [N, 1, 3, 4, 2, 1], "a-shape-minor"),
    ("C7", [X, 3, 5, 3, 5, 3], [N, 1, 3, 1, 4, 1], "a-shape-7"),
    ("Cm7", [X, 3, 5, 3, 4, 3], [N, 1, 3, 1, 2, 1], "a-shape-m7"),
    ("Cmaj7", [X, 3, 5, 4, 5, 3], [N, 1, 3, 2, 4, 1], "a-shape-maj7"),
]
for name, frets, fingers, slug in a_shapes:
    save(chord_diagram(name, frets, fingers, barre=(3, 5, 1), base_fret=3, highlight_root=5), F + slug + ".svg")
print("guitar chords done")
