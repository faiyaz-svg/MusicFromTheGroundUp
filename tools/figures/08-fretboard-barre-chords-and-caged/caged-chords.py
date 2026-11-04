from _common import *
F = STAGE + "caged-chords-"
# open shapes (string 6 to string 1)
SHAPES = {
    "C": ([ "x", 3, 2, 0, 1, 0], [None, 3, 2, None, 1, None], 5),
    "A": ([ "x", 0, 2, 2, 2, 0], [None, None, 1, 2, 3, None], 5),
    "G": ([3, 2, 0, 0, 0, 3], [2, 1, None, None, None, 3], 6),
    "E": ([0, 2, 2, 1, 0, 0], [None, 2, 3, 1, None, None], 6),
    "D": ["x", "x", 0, 2, 3, 2],
}
OPENROOT = {"C": 0, "A": 9, "G": 7, "E": 4, "D": 2}
shapes = {
    "C": ["x", 3, 2, 0, 1, 0],
    "A": ["x", 0, 2, 2, 2, 0],
    "G": [3, 2, 0, 0, 0, 3],
    "E": [0, 2, 2, 1, 0, 0],
    "D": ["x", "x", 0, 2, 3, 2],
}
rootstr = {"C": 5, "A": 5, "G": 6, "E": 6, "D": 4}
fing = {
    "C": [None, 3, 2, None, 1, None],
    "A": [None, None, 1, 2, 3, None],
    "G": [2, 1, None, None, None, 3],
    "E": [None, 2, 3, 1, None, None],
    "D": [None, None, None, 1, 3, 2],
}

def moved(shape, n):
    return [f if f == "x" else f + n for f in shape]

def base_for(frets):
    nums = [f for f in frets if f != "x"]
    return max(1, min(x for x in nums if x > 0) if min(nums) > 0 else 1) if False else None

def draw(name, key, frets, fingers, rs, fname, n=0):
    nums = [f for f in frets if f != "x"]
    lo = min(nums)
    base = 1 if lo <= 1 else lo
    barre = None
    if n > 0:
        if key == "A":
            barre, fingers = (n, 5, 1), [None, 1, 3, 3, 3, 1]
        elif key == "E":
            barre, fingers = (n, 6, 1), [1, 3, 4, 2, 1, 1]
        elif key == "G":
            barre, fingers = (n, 4, 2), [3, 2, 1, 1, 1, 4]
        elif key == "D":
            fingers = None
    save(chord_diagram(name, frets, fingers, barre=barre, base_fret=base, highlight_root=rs), fname)

def spell(target):
    return (NN.index(target) )

def caged_set(root):
    t = NN.index(root)
    res = {}
    for k in "CAGED":
        n = (t - OPENROOT[k]) % 12
        res[k] = (moved(shapes[k], n), n)
    return res

if __name__ == "__main__":
    out = caged_set("C")
    for k in "CAGED":
        fr, n = out[k]
        print("C", k, fr, n)
        draw(f"C ({k} shape)", k, fr, fing[k], rootstr[k], F + f"c-{k.lower()}-shape.svg", n)
    out = caged_set("G")
    for k in "CAGED":
        print("G", k, out[k])

    # the five forms of C major on one neck
    cols = {"C": "yellow", "A": "salmon", "G": "teal", "E": "sky", "D": "lavender"}
    out = caged_set("C")
    marks = {}
    for k in "CAGED":
        fr, n = out[k]
        for i, f in enumerate(fr):
            if f == "x":
                continue
            st = 6 - i
            marks[(st, f)] = {"string": st, "fret": f, "label": nm(st, f), "colour": cols[k]}
            assert nm(st, f) in ("C", "E", "G")
    svg = fretboard(15, marks=list(marks.values()))
    body = string_labels()
    save(svg.replace("</svg>", body + "</svg>"), F + "c-five-places.svg")
