from _common import *

rows = [("Bach, Bourree in E minor (pickup, then bars 1 to 24)", [(1, 7, "First half", "played twice"), (8, 24, "Second half", "played twice")])]
svg, h = section_map(rows, "Section map of the bourree: first half to bar 7, second half from bar 8 to bar 24, each played twice", "bach-for-guitar")
save(svg, FOLDER + "/bach-for-guitar-sections.svg")
print("done")
