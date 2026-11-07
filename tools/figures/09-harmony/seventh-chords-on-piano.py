from _common import *

# G7 in 2nd inversion (D F G B) resolving to C (C E G C), right hand fingers 1 2 3 5.
save(keyboard("C4", "C5", colours={"D4": "yellow", "F4": "teal", "G4": "salmon", "B4": "yellow"},
              fingers={"D4": 1, "F4": 2, "G4": 3, "B4": 5}, labels={"D4": "D", "F4": "F", "G4": "G", "B4": "B"}),
     STAGE + "seventh-chords-on-piano-g7.svg")
save(keyboard("C4", "C5", colours={"C4": "salmon", "E4": "yellow", "G4": "yellow", "C5": "salmon"},
              fingers={"C4": 1, "E4": 2, "G4": 3, "C5": 5}, labels={"C4": "C", "E4": "E", "G4": "G", "C5": "C"}),
     STAGE + "seventh-chords-on-piano-c.svg")
print("seventh-chords-on-piano done")
