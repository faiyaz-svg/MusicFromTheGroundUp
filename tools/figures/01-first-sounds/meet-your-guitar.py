from _common import *
from _common import _text, _svg

# 1. Parts of a steel-string acoustic guitar (front view), labelled
cx = 300
b = []
fret_ys = []
nut_y, body_top = 100, 350
# neck
b.append(rect(cx - 17, nut_y, 34, body_top - nut_y + 20, "#c9a26b", INK, 1.5))
# headstock
b.append(rect(cx - 24, 20, 48, 80, "#8a6a3b", INK, 1.5))
for i, y in enumerate((36, 58, 80)):
    b.append(circle(cx - 36, y, 6, "#b3b3b3"))
    b.append(circle(cx + 36, y, 6, "#b3b3b3"))
    b.append(line(cx - 30, y, cx - 24, y, 2))
    b.append(line(cx + 24, y, cx + 30, y, 2))
# frets
y = nut_y + 4
step = 24
for f in range(1, 13):
    y += step
    step *= 0.944
    fret_ys.append(y)
    b.append(line(cx - 17, y, cx + 17, y, 1.5, "#666"))
b.append(rect(cx - 17, nut_y - 2, 34, 6, "#fff", INK, 1.5))     # nut
for f in (3, 5, 7, 9):
    yy = (fret_ys[f - 1] + fret_ys[f - 2]) / 2
    b.append(circle(cx, yy, 3.5, "#fff", INK, 1))
yy = (fret_ys[11] + fret_ys[10]) / 2
b.append(circle(cx - 6, yy, 3.5, "#fff", INK, 1) + circle(cx + 6, yy, 3.5, "#fff", INK, 1))
# body: a closed outline built from four cubic segments on the right, mirrored on the left
SEG = [((34, -10), (82, 10), (82, 60)), ((82, 100), (58, 112), (60, 140)),
       ((62, 170), (100, 175), (100, 230)), ((100, 275), (50, 290), (0, 290))]
P = lambda sign, pt: (cx + sign * pt[0], body_top + pt[1])
path = f"M{cx + 17:g} {body_top - 14:g} "
for seg in SEG:
    path += "C" + " ".join("%g %g" % P(1, pt) for pt in seg) + " "
starts = [(17, -14)] + [seg[2] for seg in SEG[:-1]]
for i in range(3, -1, -1):
    c1, c2, _ = SEG[i]
    path += "C%g %g %g %g %g %g " % (*P(-1, c2), *P(-1, c1), *P(-1, starts[i]))
path += "Z"
b.insert(0, f'<path d="{path}" fill="#e0b97a" stroke="{INK}" stroke-width="2"/>')
# fretboard continues over the body
b.append(rect(cx - 17, body_top - 14, 34, 74, "#8a6a3b", INK, 1.5))
# soundhole, bridge, saddle, bridge pins
hole_y, bridge_y = body_top + 90, body_top + 195
b.append(circle(cx, hole_y, 32, "#222", INK, 2))
b.append(rect(cx - 45, bridge_y, 90, 20, "#5b3d1e", INK, 1.5))
b.append(line(cx - 40, bridge_y + 6, cx + 40, bridge_y + 6, 3, "#fff"))
for i in range(6):
    b.append(circle(cx - 25 + i * 10, bridge_y + 14, 2.5, "#fff", INK, 1))
for i in range(6):
    xn = cx - 12.5 + i * 5
    xb = cx - 25 + i * 10
    b.append(line(xn, nut_y + 2, xb, bridge_y + 6, 0.8 + (5 - i) * 0.25, "#555"))
# strap buttons
b.append(circle(cx, body_top + 288, 4, "#b3b3b3"))
b.append(circle(cx - 22, body_top - 14, 4, "#b3b3b3"))

def callout(x, y, tx, ty, text, anchor="start"):
    return line(x, y, tx, ty, 1, LABEL) + _text(tx + (6 if anchor == "start" else -6), ty + 4, text,
                                                size=13, fill=INK, anchor=anchor)
R, L = cx + 150, cx - 150
b.append(callout(cx + 36, 36, R, 36, "Tuners (machine heads)"))
b.append(callout(cx + 24, 26, R, 12, "Headstock"))
b.append(callout(cx + 17, nut_y + 1, R, nut_y + 12, "Nut"))
b.append(callout(cx + 17, (fret_ys[1] + fret_ys[2]) / 2, R, 150, "Neck"))
b.append(callout(cx + 17, fret_ys[3], R, 190, "Frets (the metal bars)"))
b.append(callout(cx + 3.5, (fret_ys[5] + fret_ys[6]) / 2, R, 230, "Fret marker (dot)"))
b.append(callout(cx + 17, fret_ys[9], R, 270, "Fretboard"))
b.append(callout(cx + 22, hole_y - 22, R, hole_y - 22, "Soundhole"))
b.append(callout(cx + 70, body_top + 40, R, body_top + 40, "Top (the front of the body)"))
b.append(callout(cx + 45, bridge_y + 5, R, bridge_y, "Bridge"))
b.append(callout(cx + 20, bridge_y + 6, R, bridge_y + 22, "Saddle (white strip)"))
b.append(callout(cx + 15, bridge_y + 14, R, bridge_y + 44, "Bridge pins"))
b.append(callout(cx, body_top + 288, R, body_top + 288, "Strap button (lower)"))
b.append(callout(cx - 100, body_top + 230, L, body_top + 230, "Body", "end"))
b.append(callout(cx - 22, body_top - 14, L, body_top - 14, "Strap button (upper)", "end"))
svg = _svg(cx + 340, body_top + 320, "Front view of a steel-string acoustic guitar with its parts labelled", "".join(b))
save(svg, "01-first-sounds/meet-your-guitar-parts.svg")

# 2. String names and numbers on the neck
names = {1: "E", 2: "B", 3: "G", 4: "D", 5: "A", 6: "E"}
marks = [{"string": s, "fret": 0, "label": names[s], "colour": "yellow"} for s in range(1, 7)]
fb = fretboard(4, marks=marks, inlays=True)
body = ""
for s in range(1, 7):
    body += _text(4 + 56 + 4 * 56 + 20 + 14, 20 + (s - 1) * 26 + 4, f"string {s}", size=12, fill=INK, anchor="start")
svg = widen(fb, 70, body)
save(svg, "01-first-sounds/meet-your-guitar-strings.svg")
print("meet-your-guitar done")
