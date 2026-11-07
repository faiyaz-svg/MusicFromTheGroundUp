from _common import *
from _common import _text, _svg

# Side view of the picking finger, looking along the strings from the bridge end.
W, H = 640, 250
out = []
def panel(x0, title, rest):
    o = [_text(x0 + 140, 24, title, size=15, fill=INK, weight="bold")]
    # strings drawn as dots in a row (cross-section), sound board line below
    sx = [x0 + 70, x0 + 140, x0 + 210]
    for i, x in enumerate(sx):
        o.append(circle(x, 110, 7, INK, INK))
    o.append(line(x0 + 20, 190, x0 + 260, 190, 3))
    o.append(_text(x0 + 140, 210, "guitar top", size=12, anchor="middle"))
    o.append(_text(sx[1] - 10, 130, "plucked string", size=12, fill=INK, anchor="end"))
    o.append(_text(sx[2], 130, "next string", size=12, fill=LABEL))
    # fingertip before the stroke
    o.append(rect(sx[1] - 12, 38, 24, 40, YELLOW, INK, 1.5, 10))
    o.append(_text(sx[1] + 38, 62, "finger", size=12, fill=LABEL, anchor="start"))
    if rest:
        # finger ends resting on the next string
        o.append(line(sx[1], 78, sx[2] - 6, 100, 2.5, RED))
        o.append(f'<path d="M{sx[2]-6:g} 100 l-9 -2 l5 -8 z" fill="{RED}"/>\n')
        o.append(_text(x0 + 140, 160, "ends on the next string", size=12, fill=INK))
    else:
        # finger curls up and over, never touching the next string
        o.append(f'<path d="M{sx[1]:g} 78 Q{sx[1]+4:g} 150 {sx[1]+40:g} 150" fill="none" stroke="{RED}" stroke-width="2.5"/>\n')
        o.append(f'<path d="M{sx[1]+40:g} 150 l-9 -6 l0 12 z" fill="{RED}"/>\n')
        o.append(_text(x0 + 200, 170, "curls past the next string", size=12, fill=INK))
    return "".join(o)
out.append(panel(0, "Free stroke", False))
out.append(panel(320, "Rest stroke", True))
save(_svg(W, H, "Two diagrams of the picking finger seen from the end of the strings. In a free stroke the finger plucks and curls past the next string without touching it. In a rest stroke the finger plucks and comes to rest on the next string.",
          "".join(out)), FOLDER + "/fingerstyle-posture-and-studies-strokes.svg")
print("done")
