from _common import *

rows = [("Schumann, Traumerei (pickup, then bars 1 to 24)", [(1, 8, "First part", "two phrases of 4 bars"), (9, 16, "Middle part", "turns away, climbs"), (17, 24, "Opening returns", "new ending")])]
svg, h = section_map(rows, "Section map of Traumerei: bars 1 to 8, 9 to 16 and 17 to 24", "schumann-traumerei")
save(svg, FOLDER + "/schumann-traumerei-sections.svg")
print("done")
