from _common import *

F = "01-first-sounds/pitch-and-the-musical-alphabet-"
# Every C marked, so C sits just left of each group of two black keys
cs = {f"C{o}": "yellow" for o in range(1, 8)}
labs = {f"C{o}": f"C{o}" for o in range(1, 8)}
labs["C8"] = "C8"
save(keyboard("A0", "C8", colours={**cs, "C8": "yellow"}, labels=labs), F + "octaves.svg")

# One octave of white keys with their letter names, middle C marked
save(keyboard("C4", "C5", marks=["C4", "C5"], show_names=True, middle_c=True), F + "white-key-names.svg")

# C marked left of each pair of black keys, two octaves close up
save(keyboard("C4", "B5", marks=["C4", "C5"], labels={"C4": "C", "C5": "C"}), F + "find-c.svg")
print("pitch done")
