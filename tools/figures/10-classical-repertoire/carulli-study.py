from _common import *

rows = [
 ("Carulli, Waltz Op. 241 No. 1 (bars 1 to 24)", [(1, 8, "A: C major", "played twice"), (9, 16, "B: C major, Fine", "played twice"), (17, 24, "C: A minor", "played twice")]),
]
svg, h = section_map(rows, "Section map of the Carulli waltz: bars 1 to 8, 9 to 16 and 17 to 24, each repeated, then back to the start and play to the Fine in bar 16", "carulli-study")
save(svg, FOLDER + "/carulli-study-sections.svg")
print("done")
