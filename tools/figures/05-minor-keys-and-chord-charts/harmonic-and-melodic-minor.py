from _common import *

F = FOLDER + "/harmonic-and-melodic-minor-"
save(step_strip(list("ABCDEF") + ["G#", "A"], ["W", "H", "W", "W", "H", "W+H", "H"],
                "The A harmonic minor scale: A, B, C, D, E, F, G#, A with the steps between the notes",
                fills={6: SALMON}, caption="Only the 7th note changes (G#, salmon). F to G# is a step of 3 half steps."),
     F + "a-harmonic-steps.svg")
save(step_strip(list("ABCDE") + ["F#", "G#", "A"], ["W", "H", "W", "W", "W", "W", "H"],
                "The A melodic minor scale going up: A, B, C, D, E, F#, G#, A with the steps between the notes",
                fills={5: SALMON, 6: SALMON}, caption="Going up, the 6th and 7th notes are raised (F# and G#). Going down, use the natural minor."),
     F + "a-melodic-steps.svg")
save(keyboard("A4", "A5", marks=["A4", "B4", "C5", "D5", "E5", "F5", "A5"], colours={"G#5": "salmon"},
              labels={"G#5": "7"}), F + "a-harmonic-keyboard.svg")
save(keyboard("A4", "A5", marks=["A4", "B4", "C5", "D5", "E5", "A5"], colours={"F#5": "salmon", "G#5": "salmon"},
              labels={"F#5": "6", "G#5": "7"}), F + "a-melodic-keyboard.svg")
print("harmonic-melodic done")
