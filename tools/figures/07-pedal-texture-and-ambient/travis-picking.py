from _common import *
from _common import _text, _svg, _num_circle

# Travis pattern on C: thumb on beats (strings 5 and 4), fingers on the "&"s (strings 3 and 2).
cols = ["1", "&", "2", "&", "3", "&", "4", "&"]
x0, dx = 90, 46
rows = {  # string -> {column: letter}
    1: {}, 2: {3: "m", 7: "m"}, 3: {1: "i", 5: "i"},
    4: {2: "p", 6: "p"}, 5: {0: "p", 4: "p"}, 6: {},
}
top, dy = 50, 26
body = _text(20, 22, "Travis pattern on C (picking hand letters)", size=14, fill=INK, anchor="start", weight="bold")
for i, c in enumerate(cols):
    body += _text(x0 + i * dx, top - 8, c, size=13, fill=INK, weight="bold")
for s in range(1, 7):
    y = top + (s - 1) * dy + 14
    body += line(x0 - 24, y, x0 + 7 * dx + 24, y, 1.2, "#999")
    body += _text(34, y + 4, f"string {s}", size=11, anchor="middle")
    for col, letter in rows[s].items():
        body += _num_circle(x0 + col * dx, y, letter, r=10, fill=(TEAL if letter == "p" else YELLOW))
h = top + 6 * dy + 40
body += _text(20, h - 12, "Thumb (p) on the beats, alternating strings 5 and 4. Fingers i and m on the &s.", size=11, anchor="start")
save(_svg(x0 + 7 * dx + 40, h, "Travis picking pattern on a C chord: thumb on strings 5 and 4 on the beats, index on string 3 and middle on string 2 on the ands", body),
     STAGE + "travis-picking-pattern.svg")
print("travis done")
