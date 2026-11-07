from _common import *

rows = [
 ("Etude No. 1 (bars 1 to 43)", [(1, 8, "Runs down"), (9, 10, "Scale up and down"), (11, 16, "Sharps"), (17, 20, "Back in C"), (21, 28, "Pairs of notes"), (29, 36, "Bass and chord notes"), (37, 39, "Scales"), (40, 43, "Opening and end")]),
]
svg, h = section_map(rows, "Section map of Carcassi Etude No. 1 by bar number", "carcassi-op-60")
save(svg, FOLDER + "/carcassi-op-60-sections.svg")
print("done")
