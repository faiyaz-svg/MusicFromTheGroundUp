from _common import *

for slug, name, notes, labs in [
    ("c-major", "C major triad", ["C4", "E4", "G4"], {"C4": "C", "E4": "E", "G4": "G"}),
    ("c-minor", "C minor triad", ["C4", "Eb4", "G4"], {"C4": "C", "Eb4": "Eb", "G4": "G"}),
    ("c-diminished", "C diminished triad", ["C4", "Eb4", "Gb4"], {"C4": "C", "Eb4": "Eb", "Gb4": "Gb"}),
    ("c-augmented", "C augmented triad", ["C4", "E4", "G#4"], {"C4": "C", "E4": "E", "G#4": "G#"}),
]:
    save(keyboard("C4", "G4", colours={n: ("salmon" if n == "C4" else "yellow") for n in notes}, labels=labs),
         STAGE + "triads-" + slug + ".svg")
print("triads done")
