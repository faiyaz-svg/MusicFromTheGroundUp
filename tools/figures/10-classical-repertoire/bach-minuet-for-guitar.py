from _common import *

rows = [
 ("Minuet in G, guitar (bars 1 to 32)", [(1, 8, "A1", "played twice"), (9, 16, "A2", "played twice"), (17, 24, "B1", "played twice"), (25, 32, "B2", "played twice")]),
]
svg, h = section_map(rows, "Section map of the Minuet in G for guitar by bar number", "bach-minuet-for-guitar")
save(svg, FOLDER + "/bach-minuet-for-guitar-sections.svg")
print("done")
