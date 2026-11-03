from _common import *
from _common import _text, _svg

# Fretting hand (left hand for a right-handed player): fingers 1 to 4 and the thumb T
b = hand(60, 130, 1, ["T", 1, 2, 3, 4], "Fretting hand (left)")
save(_svg(240, 250, "Left hand seen from above: thumb T, index finger 1, middle 2, ring 3, little 4", b),
     "01-first-sounds/holding-tuning-and-the-pick-fretting-hand.svg")

# Where to press: close behind the fret wire (on the nut side of the wire)
fw = 120
x0, y0 = 40, 40
b = []
b.append(rect(x0, y0, 3 * fw, 60, "#e0b97a", INK, 1.5))
for i in range(1, 4):
    b.append(line(x0 + i * fw, y0, x0 + i * fw, y0 + 60, 5, "#888"))
b.append(line(x0, y0 + 30, x0 + 3 * fw, y0 + 30, 2))
b.append(rect(x0 - 6, y0 - 4, 6, 68, INK, INK, 1))
# three separate examples in the three fret spaces
b.append(circle(x0 + fw * 0.3, y0 + 30, 13, "#ff8389"))
b.append(circle(x0 + fw * 1.82, y0 + 30, 13, "#00d2be"))
b.append(circle(x0 + fw * 3.0, y0 + 30, 13, "#ff8389"))
b.append(_text(x0 + fw * 0.3, y0 + 95, "too far back", size=12, fill=INK))
b.append(_text(x0 + fw * 1.82, y0 + 95, "close behind the fret", size=12, fill=INK, weight="bold"))
b.append(_text(x0 + fw * 3.0, y0 + 95, "on the wire", size=12, fill=INK))
b.append(_text(x0 - 3, y0 - 10, "nut", size=12, fill=LABEL, anchor="middle"))
for i in range(1, 4):
    b.append(_text(x0 + i * fw, y0 - 10, f"fret {i}", size=12, fill=LABEL))
save(_svg(x0 * 2 + 3 * fw, 150, "Top view of a string over frets 1 to 3: a finger too far back, just behind fret 2, and on the fret wire of fret 3", "".join(b)),
     "01-first-sounds/holding-tuning-and-the-pick-fret-position.svg")
print("holding done")
