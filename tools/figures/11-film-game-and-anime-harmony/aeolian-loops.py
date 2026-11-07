from _common import *

save(strip([("Am", "i", "teal"), ("F", "VI", "yellow"), ("G", "VII", "salmon")],
           "The Aeolian loop in A minor: Am, F, G, which are i, VI and VII", loop=True),
     STAGE + "aeolian-loops-three-chord.svg")
save(strip([("Am", "i", "teal"), ("F", "VI", "yellow"), ("C", "III", "sky"), ("G", "VII", "salmon")],
           "The four-chord Aeolian loop in A minor: Am, F, C, G, which are i, VI, III and VII", loop=True),
     STAGE + "aeolian-loops-four-chord.svg")
print("aeolian-loops done")
