from _common import *

F = FOLDER + "/broken-chord-accompaniment-"
save(keyboard("C3", "E4", marks=["C3", "G3", "C4"], colours={"C3": "salmon"},
              labels={"C3": "1", "G3": "5", "C4": "8"}), F + "c-1-5-8.svg")
save(keyboard("C3", "E4", marks=["C3", "G3", "E4"], colours={"C3": "salmon"},
              labels={"C3": "1", "G3": "5", "E4": "10"}), F + "c-1-5-10.svg")
print("broken done")
