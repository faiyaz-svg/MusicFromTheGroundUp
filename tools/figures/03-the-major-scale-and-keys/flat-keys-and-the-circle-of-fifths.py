import math
from _common import *
from _common import _text, _svg, _verovio

F = "03-the-major-scale-and-keys/flat-keys-and-the-circle-of-fifths-"

def sig(key, note, title, name):
    abc = f"X:1\nM:none\nL:1/1\nK:{key} clef=treble\n{note} |]\n"
    save(_verovio(abc, title), F + name + ".svg")

sig("F", "F", "The treble clef with a key signature of one flat, B flat, followed by the note F", "f-major")
sig("Bb", "B", "The treble clef with a key signature of two flats, B flat and E flat, followed by the note B flat", "bb-major")
sig("Eb", "E", "The treble clef with a key signature of three flats, B flat, E flat and A flat, followed by the note E flat", "eb-major")
sig("Cb", "c", "The treble clef with all seven flats in order: B, E, A, D, G, C, F", "order-of-flats")

# circle of fifths: major keys only
keys = [("C", "0", "yellow"), ("G", "1#", "sky"), ("D", "2#", "sky"), ("A", "3#", "sky"), ("E", "4#", "sky"),
        ("B", "5#", "sky"), ("F#/Gb", "6", "lavender"), ("Db", "5b", "salmon"), ("Ab", "4b", "salmon"),
        ("Eb", "3b", "salmon"), ("Bb", "2b", "salmon"), ("F", "1b", "salmon")]
size = 460
cx = cy = size / 2
R = 170
out = [f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#bbb" stroke-width="2"/>\n']
for i, (k, n, col) in enumerate(keys):
    a = math.radians(-90 + 30 * i)
    x, y = cx + R * math.cos(a), cy + R * math.sin(a)
    r = 34
    out.append(circle(x, y, r, PALETTE[col], INK, 1.5))
    out.append(_text(x, y - 4 if "/" in k else y + 1, k, size=17 if "/" not in k else 14, fill=INK, weight="bold"))
    lab = {"0": "no sharps or flats"}.get(n)
    count = n if n != "0" else "0"
    word = "" if n == "0" else (" sharp" if "#" in n else " flat")
    num = n.replace("#", "").replace("b", "")
    if k == "F#/Gb":
        txt = "6 sharps or 6 flats"
    elif n == "0":
        txt = "0"
    else:
        txt = f"{num} {'sharp' if '#' in n else 'flat'}{'' if num == '1' else 's'}"
    if k == "F#/Gb":
        out.append(_text(x, y + 16, "6 sharps", size=10, fill=INK))
        out.append(_text(x, y + 28, "or 6 flats", size=10, fill=INK))
    else:
        out.append(_text(x, y + 20, "none" if n == "0" else txt, size=11, fill=INK))
out.append(_text(cx, cy - 12, "Clockwise: each key starts on", size=14, fill=INK))
out.append(_text(cx, cy + 8, "the 5th note of the one before,", size=14, fill=INK))
out.append(_text(cx, cy + 28, "with one more sharp (or one less flat).", size=14, fill=INK))
save(_svg(size, size, "The circle of fifths: the twelve major keys in a circle, C at the top, sharps increasing clockwise and flats increasing anticlockwise", "".join(out)),
     F + "circle.svg")
print("flat keys done")
