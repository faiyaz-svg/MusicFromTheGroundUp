from _common import *

rows = [("Chopin, Prelude in B minor (bars 1 to 26)", [(1, 8, "Two phrases"), (9, 12, "Opening, then C natural"), (13, 20, "Middle: C natural, then B and A#"), (21, 26, "Opening again and the end")])]
svg, h = section_map(rows, "Section map of the B minor prelude: bars 1 to 8, 9 to 12, 13 to 20 and 21 to 26", "chopin-prelude-in-b-minor")
save(svg, FOLDER + "/chopin-prelude-in-b-minor-sections.svg")
print("done")
