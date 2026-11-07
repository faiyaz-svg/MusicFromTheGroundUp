from _common import *

rows = [("Satie, Gymnopedie No. 1 (bars 1 to 47)", [(1, 4, "Introduction"), (5, 12, "Melody, long F#"), (13, 20, "Melody again, new end"), (21, 31, "Contrast, naturals"), (32, 39, "First ending", "then back to bar 1"), (40, 47, "Second ending", "last time")])]
svg, h = section_map(rows, "Section map of the Gymnopedie: introduction, two melody parts, a contrasting part and two endings", "satie-gymnopedie-1")
save(svg, FOLDER + "/satie-gymnopedie-1-sections.svg")
print("done")
