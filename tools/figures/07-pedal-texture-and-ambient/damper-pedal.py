from _common import *
from _common import _text, _svg, _num_circle

# Three ways to see pedal marks: Ped. and *, pairs, and the line.
body = ""
body += _text(20, 28, "Pedal marks", size=16, fill=INK, anchor="start", weight="bold")
# row 1: one span
y = 70
body += _text(20, y, "Ped. and *", size=13, anchor="start")
body += _text(150, y, "Ped.", size=15, fill=INK, anchor="start", weight="bold")
body += line(190, y - 5, 420, y - 5, 1.5, "#888")
body += _text(430, y, "*", size=20, fill=INK, anchor="start", weight="bold")
body += _text(150, y + 22, "press", size=11, anchor="start")
body += _text(410, y + 22, "lift", size=11, anchor="start")
# row 2: two spans in a row
y = 130
body += _text(20, y, "Two spans", size=13, anchor="start")
xs = [150, 290]
for x in xs:
    body += _text(x, y, "Ped.", size=15, fill=INK, anchor="start", weight="bold")
    body += line(x + 40, y - 5, x + 100, y - 5, 1.5, "#888")
    body += _text(x + 108, y, "*", size=20, fill=INK, anchor="start", weight="bold")
# row 3: line form with a change
y = 190
body += _text(20, y, "Line form", size=13, anchor="start")
body += line(150, y - 14, 150, y - 2, 2)
body += line(150, y - 2, 270, y - 2, 2)
body += line(270, y - 2, 280, y - 14, 2)
body += line(280, y - 14, 290, y - 2, 2)
body += line(290, y - 2, 420, y - 2, 2)
body += line(420, y - 2, 420, y - 14, 2)
body += _text(150, y + 22, "press", size=11, anchor="start")
body += _text(246, y + 22, "change (lift and press)", size=11, anchor="start")
body += _text(398, y + 22, "lift", size=11, anchor="start")
save(_svg(480, 230, "Pedal marks: Ped. and an asterisk, two spans in a row, and the line form with a change", body),
     STAGE + "damper-pedal-marks.svg")
print("damper-pedal done")
