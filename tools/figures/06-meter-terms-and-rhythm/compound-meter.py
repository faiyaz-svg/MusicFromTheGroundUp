from _common import *
from _common import _text, _svg

# Two bars of eighth notes: 3/4 (simple) against 6/8 (compound), same six eighths.
W, H = 640, 250
body = ""
x0, step = 70, 80
def row(y, title, groups, labels, beatlabels):
    s = _text(20, y - 24, title, size=15, fill=INK, anchor="start", weight="bold")
    for i in range(6):
        x = x0 + i * step
        s += rect(x, y, step - 8, 34, fill=YELLOW if i in groups else BG)
        s += _text(x + (step - 8) / 2, y + 23, labels[i], size=16, fill=INK, weight="bold")
    return s
# 3/4: three beats, each split in two (1 & 2 & 3 &)
body += row(50, "3/4: three beats, each split in two", {0, 2, 4}, ["1", "&", "2", "&", "3", "&"], None)
for b in range(3):
    xa = x0 + b * 2 * step
    body += f'<path d="M{xa:g} 96 V104 H{xa + 2 * step - 8:g} V96" fill="none" stroke="{INK}" stroke-width="1.5"/>\n'
    body += _text(xa + step - 4, 124, "beat " + str(b + 1) + " (quarter note)", size=12, fill=LABEL)
# 6/8: two beats, each split in three (1 2 3 4 5 6)
body += row(170, "6/8: two beats, each split in three", {0, 3}, ["1", "2", "3", "4", "5", "6"], None)
for b in range(2):
    xa = x0 + b * 3 * step
    body += f'<path d="M{xa:g} 216 V224 H{xa + 3 * step - 8:g} V216" fill="none" stroke="{INK}" stroke-width="1.5"/>\n'
    body += _text(xa + 1.5 * step - 4, 244, "beat " + str(b + 1) + " (dotted quarter note)", size=12, fill=LABEL)
H = 256
save(_svg(W, H, "Six eighth notes grouped in twos for 3/4 (three beats) and in threes for 6/8 (two beats), with the beat starts shaded", body),
     STAGE + "compound-meter-grouping.svg")
print("compound done")
