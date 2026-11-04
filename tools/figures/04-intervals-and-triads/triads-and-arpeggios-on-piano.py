from _common import *

save(keyboard("C4", "G4", marks=["C4", "E4", "G4"], fingers={"C4": 1, "E4": 3, "G4": 5}),
     STAGE + "triads-and-arpeggios-on-piano-rh-c-triad.svg")
save(keyboard("C3", "G3", marks=["C3", "E3", "G3"], fingers={"C3": 5, "E3": 3, "G3": 1}),
     STAGE + "triads-and-arpeggios-on-piano-lh-c-triad.svg")
print("piano triads done")
