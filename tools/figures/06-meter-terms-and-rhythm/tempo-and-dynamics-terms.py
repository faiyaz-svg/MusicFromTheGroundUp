from _common import *
from _common import _text, _svg

# Rough bpm ranges for the Italian tempo words (quarter-note beat). Approximate; sources differ.
rows = [("Largo", 40, 60), ("Adagio", 66, 76), ("Andante", 76, 108),
        ("Moderato", 108, 120), ("Allegro", 120, 168), ("Presto", 168, 200)]
W, H = 620, 270
x0, sc = 120, 2.4   # px per bpm from 40
body = _text(20, 22, "Tempo words and roughly how fast they are (quarter-note beats per minute)", size=14, fill=INK, anchor="start", weight="bold")
for i, (n, a, b) in enumerate(rows):
    y = 44 + i * 32
    body += _text(20, y + 18, n, size=15, fill=INK, anchor="start", weight="bold")
    xa, xb = x0 + (a - 40) * sc, x0 + (b - 40) * sc
    body += rect(xa, y, xb - xa, 24, fill=[YELLOW, SALMON, TEAL, SKY, YELLOW, SALMON][i])
    body += _text(xa + (xb - xa) / 2, y + 17, "%d to %d" % (a, b), size=12, fill=INK)
for v in (40, 80, 120, 160, 200):
    x = x0 + (v - 40) * sc
    body += line(x, 36, x, 238, 0.8, "#bbb", "3 3")
    body += _text(x, 258, str(v), size=12, fill=LABEL)
save(_svg(W, H, "Bars showing rough bpm ranges: largo 40 to 60, adagio 66 to 76, andante 76 to 108, moderato 108 to 120, allegro 120 to 168, presto 168 to 200", body),
     STAGE + "tempo-and-dynamics-terms-tempo.svg")
print("tempo done")
