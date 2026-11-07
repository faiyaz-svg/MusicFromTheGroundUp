from _common import *

# A minor pentatonic boxes. Boxes 4 and 5 are drawn in the low position
# (the same shapes sit 12 frets higher, at frets 12 to 15 and 14 to 17).
BOXES = {
    1: ([(6, [5, 8]), (5, [5, 7]), (4, [5, 7]), (3, [5, 7]), (2, [5, 8]), (1, [5, 8])], 4, 9),
    2: ([(6, [8, 10]), (5, [7, 10]), (4, [7, 10]), (3, [7, 9]), (2, [8, 10]), (1, [8, 10])], 6, 11),
    3: ([(6, [10, 12]), (5, [10, 12]), (4, [10, 12]), (3, [9, 12]), (2, [10, 13]), (1, [10, 12])], 8, 14),
    4: ([(6, [0, 3]), (5, [0, 3]), (4, [0, 2]), (3, [0, 2]), (2, [1, 3]), (1, [0, 3])], 0, 5),
    5: ([(6, [3, 5]), (5, [3, 5]), (4, [2, 5]), (3, [2, 5]), (2, [3, 5]), (1, [3, 5])], 0, 6),
}
for n, (box, start, end) in BOXES.items():
    # check every mark is a note of A minor pentatonic
    for string, frets in box:
        for f in frets:
            assert note_to_midi(guitar_note(string, f)) % 12 in A_MINOR_PENT, (n, string, f)
    save(fretboard(frets=end, start_fret=start, marks=box_marks(box)), STAGE + f"pentatonic-boxes-box{n}.svg")

# the whole neck, frets 0 to 15, every note of A minor pentatonic
allm = []
for s in range(1, 7):
    for f in range(0, 16):
        if note_to_midi(guitar_note(s, f)) % 12 in A_MINOR_PENT:
            allm.append((s, f))
marks = []
for s, f in allm:
    name = guitar_note(s, f)[:-1]
    marks.append({"string": s, "fret": f, "label": name, "colour": "salmon" if name == "A" else "yellow"})
save(fretboard(frets=15, marks=marks), STAGE + "pentatonic-boxes-neck.svg")
print("pentatonic-boxes done")
