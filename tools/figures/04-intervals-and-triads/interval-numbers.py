from _common import *

labels = {n: str(i + 1) for i, n in enumerate(["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"])}
save(keyboard("C4", "C5", marks=["C4"], colours={"C4": "salmon"}, labels=labels),
     STAGE + "interval-numbers-counting-from-c.svg")
print("interval-numbers done")
