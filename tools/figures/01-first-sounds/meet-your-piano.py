from _common import *
from _common import _text, _svg

# 1. The 88 keys with middle C marked
save(keyboard("A0", "C8", marks=["C4"], middle_c=True), "01-first-sounds/meet-your-piano-88-keys.svg")

# 2. Groups of two and three black keys
two = {"C#4": "salmon", "D#4": "salmon", "C#5": "salmon", "D#5": "salmon"}
three = {n: "teal" for n in ("F#4", "G#4", "A#4", "F#5", "G#5", "A#5")}
save(keyboard("C4", "B5", colours={**two, **three}),
     "01-first-sounds/meet-your-piano-black-key-groups.svg")

# 3. Parts of a digital piano (front view); ox moves the piano right to leave room for labels
ox = 150

def callout(x, y, tx, ty, text, anchor="start"):
    return line(x, y, tx, ty, 1, LABEL) + _text(tx + (6 if anchor == "start" else -6), ty + 4, text,
                                                size=13, fill=INK, anchor=anchor)

b = []
b.append(rect(ox + 60, 70, 520, 120, "#e6e6e6", INK, 2))         # body
b.append(rect(ox + 160, 28, 320, 42, "#fff", INK, 2))            # music desk
b.append(rect(ox + 70, 120, 500, 62, "#fff", INK, 1.5))          # keys
n = 21
for i in range(n):
    b.append(line(ox + 70 + i * 500 / n, 120, ox + 70 + i * 500 / n, 182, 1))
for i in range(n - 1):
    if i % 7 in (0, 1, 3, 4, 5):
        b.append(rect(ox + 70 + (i + 0.68) * 500 / n, 120, 500 / n * 0.64, 38, INK, INK, 1))
b.append(rect(ox + 70, 78, 120, 34, "#fed134", INK, 1.5))        # control panel
b.append(rect(ox + 200, 78, 44, 34, "#fff", INK, 1.5))           # headphone jack
b.append(rect(ox + 120, 190, 14, 100, "#e6e6e6", INK, 2))        # legs
b.append(rect(ox + 506, 190, 14, 100, "#e6e6e6", INK, 2))
b.append(rect(ox + 240, 270, 160, 14, "#e6e6e6", INK, 2))        # pedal unit
for x in (275, 320, 365):
    b.append(rect(ox + x - 12, 286, 24, 18, "#b3b3b3", INK, 1.5))
r = ox + 600
b.append(callout(ox + 480, 49, r, 49, "Music desk"))
b.append(callout(ox + 244, 95, r, 95, "Headphone jack"))
b.append(callout(ox + 570, 150, r, 150, "Keys"))
b.append(callout(ox + 520, 240, r, 240, "Leg"))
b.append(callout(ox + 400, 277, r, 277, "Pedal unit"))
b.append(callout(ox + 70, 95, ox - 6, 95, "Control panel", "end"))
b.append(_text(ox - 12, 113, "volume, sounds,", size=11, anchor="end"))
b.append(_text(ox - 12, 127, "metronome", size=11, anchor="end"))
svg = _svg(ox + 730, 320, "Front view of a digital piano: music desk, control panel, headphone jack, keys, legs and pedal unit", "".join(b))
save(svg, "01-first-sounds/meet-your-piano-parts.svg")

# 4. The three pedals
b = []
names = [("Soft", "left pedal (una corda)"), ("Sostenuto", "middle pedal"), ("Damper", "right pedal (sustain)")]
for i, (n1, n2) in enumerate(names):
    x = 20 + i * 175
    b.append(rect(x, 20, 130, 36, "#b3b3b3", INK, 2, 4))
    b.append(_text(x + 65, 84, n1, size=16, fill=INK, weight="bold"))
    b.append(_text(x + 65, 104, n2, size=12, fill=LABEL))
save(_svg(540, 120, "The three piano pedals from left to right: soft, sostenuto and damper", "".join(b)),
     "01-first-sounds/meet-your-piano-pedals.svg")
print("meet-your-piano done")
