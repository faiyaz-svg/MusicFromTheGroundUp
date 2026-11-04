from _common import *
from _common import _svg, _text

names = {6: "E", 5: "A", 4: "D", 3: "G", 2: "B", 1: "E"}
fing = {6: "p", 5: "p", 4: "p", 3: "i", 2: "m", 1: "a"}
w, h = 420, 250
out = []
for k, s in enumerate([1, 2, 3, 4, 5, 6]):
    y = 40 + k * 34
    out.append(line(110, y, 330, y, 1 + (s - 1) * 0.6))
    out.append(_text(70, y + 5, f"string {s}", size=14, fill=INK, anchor="end"))
    out.append(_text(100, y + 5, names[s], size=14, fill=LABEL, anchor="end"))
    colour = {"p": SALMON, "i": YELLOW, "m": SKY, "a": TEAL}[fing[s]]
    out.append(circle(360, y, 14, colour))
    out.append(_text(360, y + 6, fing[s], size=17, fill=INK, weight="bold"))
out.append(_text(360, 20, "finger", size=12, fill=LABEL))
out.append(_text(215, 238, "p thumb, i index, m middle, a ring", size=13, fill=LABEL))
save(_svg(w, h, "The six strings with the picking-hand finger for each: the thumb p plays strings 6, 5 and 4, i plays string 3, m plays string 2, a plays string 1",
          "".join(out)), FOLDER + "/fingerpicking-basics-fingers.svg")
print("pick done")
