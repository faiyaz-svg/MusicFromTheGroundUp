from _common import *

save(keyboard("A4", "A5", fingers={"A4": 1, "C5": 2, "E5": 3, "A5": 5},
              labels={"A4": "A", "C5": "C", "E5": "E", "A5": "A"}, marks=["A4", "C5", "E5", "A5"]),
     STAGE + "arpeggio-prelude-am-shape.svg")
save(strip([("Am", "i", "teal"), ("F", "VI", "yellow"), ("C", "III", "sky"), ("G", "VII", "salmon")],
           "Bars 1 to 4 of Far Tower: Am, F, C, G, one chord per bar", loop=True),
     STAGE + "arpeggio-prelude-bars-1-to-4.svg")
print("arpeggio prelude done")
