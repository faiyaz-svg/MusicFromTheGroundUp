from _common import *

save(chord_diagram("E", [0, 2, 2, 1, 0, 0], [None, 2, 3, 1, None, None], highlight_root=6),
     STAGE + "hero-theme-on-guitar-e.svg")
save(chord_diagram("C", ["x", 3, 2, 0, 1, 0], [None, 3, 2, None, 1, None], highlight_root=5),
     STAGE + "hero-theme-on-guitar-c.svg")
save(strip([("E5", "i", "teal"), ("G5", "III", "sky"), ("A5", "iv", "yellow"), ("B5", "v", "salmon")],
           "Bars 1 to 4 of The Long Climb: E5, G5, A5, B5", loop=True),
     STAGE + "hero-theme-on-guitar-bars-1-to-4.svg")
print("hero theme done")
