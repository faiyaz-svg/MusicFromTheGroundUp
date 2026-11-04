from _common import *

# Cadd9 spread wide: C2 and G2 in the left hand, D3 above them, E4 in the right hand.
svg = keyboard("C2", "C5", marks=["C2", "G2", "D3", "E4"],
               colours={"C2": "salmon", "G2": "yellow", "D3": "teal", "E4": "sky"},
               labels={"C2": "C", "G2": "G", "D3": "D", "E4": "E"})
save(svg, STAGE + "ambient-piano-cadd9-wide.svg")
print("ambient-piano done")
