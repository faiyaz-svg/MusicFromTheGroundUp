from _common import *

save(keyboard("D2", "D4", marks=["D2", "A2", "D3"],
              colours={"D2": "salmon", "A2": "yellow", "D3": "teal"},
              fingers={"D2": 5, "A2": 2, "D3": 1},
              labels={"D2": "D", "A2": "A", "D3": "D"}),
     STAGE + "left-hand-patterns-d-and-a.svg")
print("left-hand-patterns done")
