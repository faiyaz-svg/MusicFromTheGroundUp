from _common import *

rows = [
 ("Study 1 (bars 0 to 33)", [(0, 7, "Opening"), (8, 13, "Key of G"), (14, 21, "Climb"), (22, 24, "Opening back"), (25, 31, "Way home"), (32, 33, "End")]),
 ("Study 2 (bars 0 to 35)", [(0, 8, "Tune"), (9, 15, "Away and back"), (16, 19, "Two-bar phrases"), (20, 23, "Chords"), (24, 32, "Six-note patterns"), (33, 35, "End")]),
 ("Study 3 (bars 0 to 32)", [(0, 8, "First part"), (9, 15, "An octave higher"), (16, 23, "Middle part"), (24, 32, "Closing part")]),
]
svg, h = section_map(rows, "Section maps of Giuliani studies 1, 2 and 3 by bar number", "giuliani-right-hand-studies")
save(svg, FOLDER + "/giuliani-right-hand-studies-sections.svg")
print("done")
