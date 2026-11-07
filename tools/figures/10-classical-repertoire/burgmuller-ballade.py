from _common import *

rows = [
 ("Ballade (bars 1 to 96)", [(1, 30, "C minor theme"), (31, 56, "C major, dolce", "bars 31 to 46 twice"), (57, 86, "C minor theme returns, pp"), (87, 96, "Ending")]),
]
svg, h = section_map(rows, "Section map of the Ballade by bar number", "burgmuller-ballade")
save(svg, FOLDER + "/burgmuller-ballade-sections.svg")
print("done")
