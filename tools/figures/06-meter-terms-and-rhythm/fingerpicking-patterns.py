from _common import *
from _common import _text, _svg

STR = {6: "E", 5: "A", 4: "D", 3: "G", 2: "B", 1: "e"}
# Which finger plays which string: p on 6-4, i on 3, m on 2, a on 1.
W, H = 520, 260
body = _text(20, 24, "Picking hand: which finger plays which string", size=15, fill=INK, anchor="start", weight="bold")
fing = {6: "p", 5: "p", 4: "p", 3: "i", 2: "m", 1: "a"}
col = {"p": YELLOW, "i": SALMON, "m": TEAL, "a": SKY}
for k, s in enumerate((1, 2, 3, 4, 5, 6)):
    y = 56 + k * 30
    body += line(120, y, 440, y, 1 + (s - 1) * 0.4, "#555")
    body += _text(30, y + 5, "string %d (%s)" % (s, STR[s]), size=14, fill=INK, anchor="start")
    f = fing[s]
    body += (f'<circle cx="470" cy="{y}" r="13" fill="{col[f]}" stroke="{INK}" stroke-width="1.5"/>\n'
             + _text(470, y + 5, f, size=15, fill=INK, weight="bold"))
body += _text(280, 250, "Thumb p: strings 6, 5, 4. Index i: 3. Middle m: 2. Ring a: 1.", size=13, fill=LABEL)
save(_svg(W, H, "The six strings with the picking finger for each: p on strings 6, 5 and 4, i on string 3, m on string 2, a on string 1", body),
     STAGE + "fingerpicking-patterns-fingers.svg")

save(chord_diagram("Am", ["x", 0, 2, 2, 1, 0], [None, None, 2, 3, 1, None], highlight_root=5), STAGE + "fingerpicking-patterns-am.svg")
save(chord_diagram("C", ["x", 3, 2, 0, 1, 0], [None, 3, 2, None, 1, None], highlight_root=5), STAGE + "fingerpicking-patterns-c.svg")
save(chord_diagram("G", [3, 2, 0, 0, 0, 3], [2, 1, None, None, None, 3], highlight_root=6), STAGE + "fingerpicking-patterns-g.svg")
print("fp done")
