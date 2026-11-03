from _common import *
from _common import _text, _svg, _num_circle


# Piano: fingers 1 to 5 in both hands
# Left hand: the thumb is on the right. Right hand: the thumb is on the left.
b = hand(50, 130, 1, [1, 2, 3, 4, 5], "Left hand") + hand(250, 130, -1, [1, 2, 3, 4, 5], "Right hand")
save(_svg(420, 250, "Both hands seen from above, palms down: left hand fingers 5 4 3 2 1 from the left, right hand fingers 1 2 3 4 5, thumbs are 1", b),
     "01-first-sounds/sitting-and-finger-numbers-hands.svg")

# Right hand fingers on the keys
save(keyboard("C4", "G4", marks=["C4", "D4", "E4", "F4", "G4"],
              fingers={"C4": 1, "D4": 2, "E4": 3, "F4": 4, "G4": 5}, middle_c=True),
     "01-first-sounds/sitting-and-finger-numbers-rh-fingers.svg")
print("sitting done")
