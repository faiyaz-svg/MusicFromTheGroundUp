from _common import *
from _common import _text

F = "03-the-major-scale-and-keys/whole-and-half-steps-"

# 1. C4 to C5 with both names on every black key, and three step brackets
svg = keyboard("C4", "C5")
cx = key_centres("C4", "C5")
head = ""
for sharp, flat, m in (("C#", "Db", 61), ("D#", "Eb", 63), ("F#", "Gb", 66), ("G#", "Ab", 68), ("A#", "Bb", 70)):
    head += _text(cx[m], 20, sharp, size=12, fill=INK, weight="bold")
    head += _text(cx[m], 36, flat, size=12, fill=INK, weight="bold")
# move the keyboard down by 46 and put the names above it
svg = svg.replace("</svg>", "</svg>")
import re
m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
w, h = float(m.group(1)), float(m.group(2))
body = svg.split("\n", 3)[3].rsplit("</svg>", 1)[0]
body = body.replace(f'<rect width="{w:g}" height="{h:g}" fill="#fff"/>\n', "", 1)
new_h = h + 46
head_svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {new_h:g}" width="{w:g}" height="{new_h:g}" '
            f'role="img" aria-label="Piano keyboard from C4 to C5 with the sharp and flat name of each black key above it" '
            f'font-family="{FONT}">\n<title>Piano keyboard from C4 to C5 with the sharp and flat name of each black key above it</title>\n'
            f'<rect width="{w:g}" height="{new_h:g}" fill="#fff"/>\n' + head
            + f'<g transform="translate(0 46)">\n{body}</g>\n</svg>\n')
save(head_svg, F + "black-key-names.svg")

# 2. Half steps and whole steps: three pairs on one row, under a full octave
k = keyboard("C4", "C5", colours={"C4": "yellow", "C#4": "yellow", "E4": "yellow", "F4": "yellow",
                                   "G4": "teal", "A4": "teal"}, marks=["C4", "C#4", "E4", "F4", "G4", "A4"])
cxs = key_centres("C4", "C5")
def br(a, b, label, y=142):
    xa, xb = cxs[note_to_midi(a)] - 6, cxs[note_to_midi(b)] + 6
    s = f'<path d="M{xa:g} {y - 2:g} V{y + 6:g} H{xb:g} V{y - 2:g}" fill="none" stroke="{INK}" stroke-width="1.5"/>\n'
    s += _text((xa + xb) / 2, y + 24, label, size=10, fill=INK, weight="bold")
    return s
brackets = br("C4", "C#4", "half step") + br("E4", "F4", "half step") + br("G4", "A4", "whole step")
save(taller(k, 44, brackets), F + "half-and-whole.svg")

# 3. Half steps on the guitar: string 1, frets 0 to 5
names = ["E", "F", "F#", "G", "G#", "A"]
marks = [{"string": 1, "fret": f, "label": n, "colour": "yellow" if "#" not in n else "lavender"}
         for f, n in enumerate(names)]
fb = fretboard(5, marks=marks, highlight_strings=[1], inlays=True)
save(fb, F + "string-1.svg")
print("whole-and-half-steps done")
