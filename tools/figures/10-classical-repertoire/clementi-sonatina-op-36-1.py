from _common import *

rows = [
 ("Sonatina in C, first movement (bars 1 to 38)", [(1, 15, "Exposition", "played twice"), (16, 23, "Development", "bars 16 to 38"), (24, 38, "Recapitulation")]),
 ("Inside the exposition", [(1, 4, "First theme"), (5, 8, "Theme again, to G"), (9, 15, "Runs in G major")]),
]
svg, h = section_map(rows, "Section map of the Clementi Sonatina first movement: exposition bars 1 to 15, development 16 to 23, recapitulation 24 to 38", "clementi-sonatina-op-36-1")
save(svg, FOLDER + "/clementi-sonatina-op-36-1-sections.svg")
print("done")
