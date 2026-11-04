from _common import *
import re

TITLE = "Neck of a guitar, frets 1 to 5, with a capo clamped across all six strings just behind fret 2"
svg = fretboard(frets=5, marks=[])
cx = 56 + 56 * 1.5 + 10
body = (rect(cx - 9, 8, 18, 150, SALMON, INK, 1.5)
        + f'<text transform="rotate(-90 {cx:g} 83)" x="{cx:g}" y="88" font-size="12" text-anchor="middle" fill="{INK}" font-weight="bold">capo</text>\n')
svg = svg.replace("</svg>", body + "</svg>")
svg = re.sub(r'aria-label="[^"]*"', f'aria-label="{TITLE}"', svg, count=1)
svg = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", svg, count=1)
save(svg, FOLDER + "/capo-and-moving-shapes-capo-fret-2.svg")
print("capo done")
