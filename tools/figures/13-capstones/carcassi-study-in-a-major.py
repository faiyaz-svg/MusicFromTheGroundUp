from _common import *

rows = [("Carcassi, Study in A major (bars 1 to 24)", [(1, 8, "A: tonic A", "played twice"), (9, 12, "E in the bass"), (13, 16, "Bass moves"), (17, 20, "A in the bass"), (21, 24, "Close on A")])]
svg, h = section_map(rows, "Section map of the Carcassi study: bars 1 to 8 repeated, then 9 to 24 in four groups of four bars, repeated", "carcassi-study-in-a-major")
save(svg, FOLDER + "/carcassi-study-in-a-major-sections.svg")
print("done")
