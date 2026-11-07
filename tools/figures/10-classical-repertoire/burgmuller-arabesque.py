from _common import *

rows = [
 ("Arabesque (bars 1 to 33)", [(1, 2, "Intro"), (3, 11, "A: the theme", "played twice"), (12, 19, "B", "bars 12 to 26 twice"), (20, 27, "A returns"), (28, 33, "End")]),
]
svg, h = section_map(rows, "Section map of the Arabesque by bar number", "burgmuller-arabesque")
save(svg, FOLDER + "/burgmuller-arabesque-sections.svg")
print("done")
