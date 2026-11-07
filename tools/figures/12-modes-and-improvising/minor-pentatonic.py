from _common import *

# Box 1 of A minor pentatonic, strings 6 to 1: two notes on each string, frets 5 to 8
BOX1 = [(6, [5, 8]), (5, [5, 7]), (4, [5, 7]), (3, [5, 7]), (2, [5, 8]), (1, [5, 8])]
save(fretboard(frets=9, start_fret=4, marks=box_marks(BOX1)), STAGE + "minor-pentatonic-box1.svg")

notes = ["A4", "C5", "D5", "E5", "G5", "A5"]
save(keyboard("A4", "A5", marks=notes,
              labels={"A4": "1", "C5": "b3", "D5": "4", "E5": "5", "G5": "b7", "A5": "1"}),
     STAGE + "minor-pentatonic-keyboard.svg")
print("minor-pentatonic done")
