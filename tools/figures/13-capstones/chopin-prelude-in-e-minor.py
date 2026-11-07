from _common import *

rows = [("Chopin, Prelude in E minor (pickup, then bars 1 to 25)", [(1, 12, "First statement, melody falls from B", "bars 1 to 11, climb in 12"), (13, 15, "Theme returns, p"), (16, 19, "Climax and stretto, f in bar 17"), (20, 25, "Fade, fermatas in 23 and 25")])]
svg, h = section_map(rows, "Section map of the E minor prelude: bars 1 to 12, 13 to 15, 16 to 19 and 20 to 25", "chopin-prelude-in-e-minor")
save(svg, FOLDER + "/chopin-prelude-in-e-minor-sections.svg")
print("done")
