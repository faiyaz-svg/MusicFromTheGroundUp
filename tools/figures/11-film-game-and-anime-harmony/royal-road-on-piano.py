from _common import *

# Right-hand voicings above the left-hand root.
voicings = [
    ("fmaj7", {"A4": 1, "C5": 3, "E5": 5}, {"A4": "A", "C5": "C", "E5": "E"}),
    ("g7", {"B4": 1, "D5": 3, "F5": 5}, {"B4": "B", "D5": "D", "F5": "F"}),
    ("em7", {"B4": 1, "D5": 3, "G5": 5}, {"B4": "B", "D5": "D", "G5": "G"}),
]
for slug, fingers, labels in voicings:
    save(keyboard("A4", "G5", marks=list(fingers), fingers=fingers, labels=labels),
         STAGE + f"royal-road-on-piano-{slug}.svg")
print("royal-road-on-piano done")
