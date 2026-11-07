from _common import *

save(strip([("F", "IV", "yellow"), ("G", "V", "salmon"), ("Em", "iii", "sky"), ("Am", "vi", "teal")],
           "The royal road in C major: F, G, Em, Am, which are IV, V, iii and vi", loop=True),
     STAGE + "the-royal-road-in-c.svg")
save(strip([("Fmaj7", "IVmaj7", "yellow"), ("G7", "V7", "salmon"), ("Em7", "iii7", "sky"), ("Am", "vi", "teal")],
           "The royal road with seventh chords in C major: Fmaj7, G7, Em7, Am", loop=True, box_w=120),
     STAGE + "the-royal-road-with-sevenths.svg")
print("the-royal-road done")
