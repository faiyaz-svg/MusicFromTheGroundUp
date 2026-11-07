from _common import *

rows = [
 ("Lesson 1 (bars 1 to 16)", [(1, 8, "First half", "played twice"), (9, 16, "Second half", "played twice")]),
 ("Lesson 2 (bars 1 to 40)", [(1, 8, "Tune"), (9, 16, "Tune again"), (17, 24, "Second tune"), (25, 32, "Third tune"), (33, 40, "Closing")]),
]
svg, h = section_map(rows, "Section maps of Sor Lessons 1 and 2 by bar number", "sor-op-60")
save(svg, FOLDER + "/sor-op-60-sections.svg")
print("done")
