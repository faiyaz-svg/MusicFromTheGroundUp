from _common import *

rows = [
 ("Petite piece No. 1 (bars 1 to 48)", [(1, 8, "A", "played twice"), (9, 16, "A answer, Fine", "played twice"), (17, 32, "F major", "played twice"), (33, 48, "Wandering, then F returns", "played twice")]),
]
svg, h = section_map(rows, "Section map of the Aguado Petite piece No. 1 by bar number", "aguado-study")
save(svg, FOLDER + "/aguado-study-sections.svg")
print("done")
