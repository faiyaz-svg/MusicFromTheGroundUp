from _common import *
from _common import _text, _svg, _num_circle

body = _text(210, 26, "The three pedals, seen from the player's seat", size=15, fill=INK, weight="bold")
pedals = [
    ("Left", "Soft (una corda)", "Quieter, softer tone", LAVENDER, 60),
    ("Middle", "Sostenuto", "Holds only the notes already down", SKY, 180),
    ("Right", "Damper (sustain)", "Lifts all the dampers", TEAL, 300),
]
for pos, name, what, col, x in pedals:
    body += rect(x, 70, 100, 60, col)
    body += rect(x + 10, 130, 80, 26, "#ddd", r=4)
    body += _text(x + 50, 56, pos, size=13, fill=INK, weight="bold")
    body += _text(x + 50, 108, name.split(" (")[0], size=13, fill=INK, weight="bold")
    body += _text(x + 50, 186, name, size=12, fill=INK, weight="bold")
    words = what.split(" ")
    mid = len(words) // 2 if len(what) > 22 else len(words)
    body += _text(x + 50, 204, " ".join(words[:mid]), size=11)
    if mid < len(words):
        body += _text(x + 50, 219, " ".join(words[mid:]), size=11)
body += _text(210, 252, "Some digital pianos assign these differently: check your manual.", size=11)
save(_svg(460, 270, "Three piano pedals from left to right: soft, sostenuto and damper", body),
     STAGE + "half-pedal-una-corda-and-sostenuto-pedals.svg")
print("pedals done")
