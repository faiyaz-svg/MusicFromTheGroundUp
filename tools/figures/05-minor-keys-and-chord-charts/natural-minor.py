from _common import *

F = FOLDER + "/natural-minor-"
save(step_strip(list("ABCDEFGA"), ["W", "H", "W", "W", "H", "W", "W"],
                "The A natural minor scale: A, B, C, D, E, F, G, A with the step between each pair of notes",
                fills={2: SALMON, 5: SALMON, 6: SALMON},
                caption="Degrees 3, 6 and 7 (salmon) are a half step lower than in A major."), F + "a-minor-steps.svg")
save(keyboard("A4", "A5", marks=["A4", "B4", "C5", "D5", "E5", "F5", "G5", "A5"],
              labels={"A4": "1", "B4": "2", "C5": "3", "D5": "4", "E5": "5", "F5": "6", "G5": "7", "A5": "8"}),
     F + "a-minor-keyboard.svg")
print("natural-minor done")
