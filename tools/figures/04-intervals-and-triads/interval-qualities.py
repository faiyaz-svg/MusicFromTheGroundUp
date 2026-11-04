from _common import *

# half steps above C4 -> (name, colour)
names = ["P1", "m2", "M2", "m3", "M3", "P4", "TT", "P5", "m6", "M6", "m7", "M7", "P8"]
notes = ["C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5"]
col = {"P": "teal", "M": "yellow", "m": "salmon", "T": "sky"}
labels = {n: nm for n, nm in zip(notes, names)}
colours = {n: col[nm[0]] for n, nm in zip(notes, names)}
save(keyboard("C4", "C5", labels=labels, colours=colours),
     STAGE + "interval-qualities-above-c.svg")
print("interval-qualities done")
