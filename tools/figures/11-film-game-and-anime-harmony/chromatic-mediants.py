from _common import *

# C major (C5 E5 G5) against the target chord; the shared note is teal.
save(keyboard("C5", "C6", colours={"C5": "teal", "E5": "yellow", "G5": "yellow", "D#5": "salmon", "G#5": "salmon"},
              labels={"C5": "C", "E5": "E", "G5": "G", "D#5": "Eb", "G#5": "Ab"}),
     STAGE + "chromatic-mediants-c-to-ab.svg")
save(keyboard("B4", "A5", colours={"E5": "teal", "C5": "yellow", "G5": "yellow", "B4": "salmon", "G#5": "salmon"},
              labels={"C5": "C", "E5": "E", "G5": "G", "B4": "B", "G#5": "G#"}),
     STAGE + "chromatic-mediants-c-to-e.svg")
save(keyboard("A4", "G5", colours={"G5": "teal", "C5": "yellow", "E5": "yellow", "A#4": "salmon", "D#5": "salmon"},
              labels={"C5": "C", "E5": "E", "G5": "G", "A#4": "Bb", "D#5": "Eb"}),
     STAGE + "chromatic-mediants-c-to-eb.svg")
print("chromatic mediants done")
