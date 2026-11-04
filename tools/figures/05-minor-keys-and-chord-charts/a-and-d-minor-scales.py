from _common import *

F = FOLDER + "/a-and-d-minor-scales-"
save(keyboard("A4", "A5", marks=["A4", "B4", "C5", "D5", "E5", "F5", "G5", "A5"],
              fingers={"A4": 1, "B4": 2, "C5": 3, "D5": 1, "E5": 2, "F5": 3, "G5": 4, "A5": 5}), F + "a-minor-rh.svg")
save(keyboard("A3", "A4", marks=["A3", "B3", "C4", "D4", "E4", "F4", "G4", "A4"],
              fingers={"A3": 5, "B3": 4, "C4": 3, "D4": 2, "E4": 1, "F4": 3, "G4": 2, "A4": 1}), F + "a-minor-lh.svg")
save(keyboard("D4", "D5", marks=["D4", "E4", "F4", "G4", "A4", "Bb4", "C5", "D5"],
              fingers={"D4": 1, "E4": 2, "F4": 3, "G4": 1, "A4": 2, "Bb4": 3, "C5": 4, "D5": 5}), F + "d-minor-rh.svg")
save(keyboard("D3", "D4", marks=["D3", "E3", "F3", "G3", "A3", "Bb3", "C4", "D4"],
              fingers={"D3": 5, "E3": 4, "F3": 3, "G3": 2, "A3": 1, "Bb3": 3, "C4": 2, "D4": 1}), F + "d-minor-lh.svg")
print("scales done")
