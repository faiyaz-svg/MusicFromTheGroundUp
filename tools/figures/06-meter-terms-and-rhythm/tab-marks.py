from _common import *
from _common import _text, _svg

# Six-line tab strips showing one mark each. items: (string, fret text, x)
def strip(items, w, title, alt, fname, labels):
    H = 190
    x0 = 60
    body = ""
    for s in range(1, 7):
        y = 40 + (s - 1) * 20
        body += line(x0, y, w - 20, y, 1, "#555")
    body += line(x0, 40, x0, 140, 2)
    body += _text(20, 95, "TAB", size=13, fill=INK, weight="bold")
    for (string, txt, x) in items:
        y = 40 + (string - 1) * 20
        body += f'<rect x="{x - 12:g}" y="{y - 9:g}" width="24" height="18" fill="#fff"/>\n'
        body += _text(x, y + 5, txt, size=14, fill=INK, weight="bold")
    for (x, t) in labels:
        body += _text(x, 168, t, size=13, fill=LABEL)
    save(_svg(w, H, alt, body), STAGE + fname)

# hammer-on and pull-off: 0h2, 2p0 on string 3; 5h7 on string 2
strip([(3, "0", 110), (3, "h", 150), (3, "2", 190), (3, "2", 290), (3, "p", 330), (3, "0", 370),
       (2, "5", 470), (2, "h", 510), (2, "7", 550)], 620, "", 
      "Tab with three marks: 0 h 2 on string 3 is a hammer-on, 2 p 0 on string 3 is a pull-off, 5 h 7 on string 2 is a hammer-on",
      "tab-marks-h-p.svg", [(150, "hammer-on"), (330, "pull-off"), (510, "hammer-on")])

# slide and bend: 5/7, 7\5 on string 1; 7b8 on string 2
strip([(1, "5", 110), (1, "/", 150), (1, "7", 190), (1, "7", 290), (1, "\\", 330), (1, "5", 370),
       (2, "7", 470), (2, "b", 510), (2, "8", 550)], 620, "",
      "Tab with three marks: 5 / 7 on string 1 is a slide up, 7 backslash 5 on string 1 is a slide down, 7 b 8 on string 2 is a bend up a half step",
      "tab-marks-slide-bend.svg", [(150, "slide up"), (330, "slide down"), (510, "bend")])
print("tab marks done")
