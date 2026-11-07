"""musicfigs: draw beginner piano and guitar teaching figures as plain SVG.

Usage in a lesson's figure script, for example
tools/figures/01-first-sounds/meet-your-piano.py:

    import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    from musicfigs import keyboard, save
    save(keyboard("A0", "C8", middle_c=True), "01-first-sounds/meet-your-piano-88-keys.svg")

Keyboard, chord and fretboard figures are hand-built SVG strings (no matplotlib).
Staff figures use verovio (ABC input) and are post-processed to match.
Note names use scientific pitch: C4 is middle C, "C#4" is sharp, "Db4" is flat.
"""
import pathlib
import re
from xml.sax.saxutils import escape

# ---------------------------------------------------------------- style
INK = "#111"
LABEL = "#444"
BG = "#fff"
FONT = "Jost, Segoe UI, Arial, sans-serif"
YELLOW, SALMON, TEAL, SKY, LAVENDER, RED = (
    "#fed134", "#ff8389", "#00d2be", "#6dcbff", "#d5b3ff", "#ff2956")
DEFAULT_MARK = YELLOW
PALETTE = {"yellow": YELLOW, "salmon": SALMON, "teal": TEAL, "sky": SKY,
           "lavender": LAVENDER, "red": RED}

# ---------------------------------------------------------------- note helpers
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
FLAT_NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
_LETTER_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
_WHITE_PCS = (0, 2, 4, 5, 7, 9, 11)
_NOTE_RE = re.compile(r"^([A-Ga-g])(##|bb|#|b|x)?(-?\d+)$")


def _parse(note):
    m = _NOTE_RE.match(note.strip())
    if not m:
        raise ValueError(f"bad note name: {note!r}")
    return m.group(1).upper(), m.group(2) or "", int(m.group(3))


def note_to_midi(note):
    """Scientific pitch name to MIDI number. C4 -> 60, "C#4" -> 61, "Db4" -> 61."""
    letter, acc, octave = _parse(note)
    shift = {"": 0, "#": 1, "b": -1, "##": 2, "x": 2, "bb": -2}[acc]
    return (octave + 1) * 12 + _LETTER_PC[letter] + shift


def midi_to_name(midi, prefer="sharp"):
    """MIDI number to note name. 61 -> "C#4" (prefer="sharp") or "Db4" ("flat")."""
    names = FLAT_NAMES if prefer == "flat" else NOTE_NAMES
    return f"{names[midi % 12]}{midi // 12 - 1}"


# open strings, string number -> MIDI (standard tuning E2 A2 D3 G3 B3 E4)
_OPEN = {6: 40, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}


def guitar_note(string, fret, prefer="sharp"):
    """Note name at a string (1 = high e, 6 = low E) and fret, standard tuning.
    guitar_note(6, 0) -> "E2"; guitar_note(5, 3) -> "C3"."""
    return midi_to_name(_OPEN[string] + fret, prefer)


def _pc_name(string, fret):
    return NOTE_NAMES[(_OPEN[string] + fret) % 12]


def _colour(c):
    return PALETTE.get(c, c) if c else DEFAULT_MARK


# ---------------------------------------------------------------- svg helpers
def _attr(s):
    return escape(str(s), {'"': "&quot;"})


def _svg(w, h, title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" '
            f'width="{w:g}" height="{h:g}" role="img" aria-label="{_attr(title)}" '
            f'font-family="{FONT}">\n<title>{escape(title)}</title>\n'
            f'<rect width="{w:g}" height="{h:g}" fill="{BG}"/>\n{body}</svg>\n')


def _text(x, y, s, size=12, fill=LABEL, anchor="middle", weight="normal"):
    return (f'<text x="{x:g}" y="{y:g}" font-size="{size:g}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{escape(str(s))}</text>\n')


def _num_circle(x, y, n, r=9, fill="#fff", ink=INK):
    return (f'<circle cx="{x:g}" cy="{y:g}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="1.5"/>\n'
            + _text(x, y + r * 0.38, n, size=r * 1.2, fill=ink, weight="bold"))


# ---------------------------------------------------------------- 1. keyboard
def keyboard(start="C4", end="C5", marks=None, fingers=None, labels=None,
             colours=None, show_names=False, middle_c=False):
    """Piano keyboard from white key `start` to white key `end` (inclusive).

    marks: list of notes to fill with a highlight colour (default yellow).
    colours: {note: colour} per-note colour; hex or a palette name
        ("yellow", "salmon", "teal", "sky", "lavender", "red"). A note in
        `colours` is filled even if it is not in `marks`.
    fingers: {note: 1-5} drawn as a number in a circle on the key.
    labels: {note: text} drawn on the key.
    show_names: write the letter name on every white key.
    middle_c: add a small "middle C" label under C4.
    Notes are scientific pitch; "E#4" lands on the F4 key, "Db4" on the C#4 key.
    Black keys are placed from the real pitches, so they fall in groups of 2 and 3.
    """
    s, e = note_to_midi(start), note_to_midi(end)
    if s % 12 not in _WHITE_PCS or e % 12 not in _WHITE_PCS:
        raise ValueError("start and end must be white keys")
    if e < s:
        raise ValueError("end is below start")
    whites = [m for m in range(s, e + 1) if m % 12 in _WHITE_PCS]
    n = len(whites)
    big = n > 16
    kw = 16 if big else 28
    kh = 90 if big else 130
    bw, bh = kw * 0.6, kh * 0.62
    pad = 6
    top = pad
    extra = 24 if middle_c else 0
    total_w = n * kw + 2 * pad
    total_h = kh + 2 * pad + extra
    widx = {m: i for i, m in enumerate(whites)}
    fill_of = {note_to_midi(k): DEFAULT_MARK for k in (marks or [])}
    for k, v in (colours or {}).items():
        fill_of[note_to_midi(k)] = _colour(v)
    fing = {note_to_midi(k): v for k, v in (fingers or {}).items()}
    labs = {note_to_midi(k): v for k, v in (labels or {}).items()}

    def key_x(m):  # centre x of a key; a black key sits on the white-key boundary
        if m in widx:
            return pad + (widx[m] + 0.5) * kw
        return pad + (widx[m - 1] + 1) * kw

    out = []
    for m in whites:
        x = pad + widx[m] * kw
        out.append(f'<rect x="{x:g}" y="{top}" width="{kw}" height="{kh}" '
                   f'fill="{fill_of.get(m, BG)}" stroke="{INK}" stroke-width="1.2"/>\n')
    blacks = [m for m in range(s, e + 1)
              if m % 12 not in _WHITE_PCS and (m - 1) in widx and (m + 1) in widx]
    for m in blacks:
        out.append(f'<rect x="{key_x(m) - bw / 2:g}" y="{top}" width="{bw:g}" height="{bh:g}" '
                   f'fill="{fill_of.get(m, INK)}" stroke="{INK}" stroke-width="1.2"/>\n')
    r = 7 if big else 10
    fs = 8 if big else 11
    for m in sorted(set(fing) | set(labs)):
        if m not in widx and m not in blacks:
            continue
        cx = key_x(m)
        if m in widx:
            cy = top + kh - (r + 8) if m in fing else top + kh - 14
        else:
            cy = top + bh - (r + 6)
        if m in fing:
            out.append(_num_circle(cx, cy, fing[m], r))
        if m in labs:
            ty = cy - (r + 4) if m in fing else cy
            ink = INK if (m in widx or m in fill_of) else "#fff"
            lsz = fs if (m in widx or len(str(labs[m])) < 2) else fs * 0.8
            out.append(_text(cx, ty, labs[m], size=lsz, fill=ink, weight="bold"))
    if show_names:
        for m in whites:
            if m in fing or m in labs:
                continue
            out.append(_text(key_x(m), top + kh - 8, NOTE_NAMES[m % 12],
                             size=8 if big else 12, fill=LABEL))
    if middle_c and 60 in widx:
        cx = key_x(60)
        out.append(f'<line x1="{cx:g}" y1="{top + kh + 2}" x2="{cx:g}" y2="{top + kh + 8}" '
                   f'stroke="{INK}" stroke-width="1.2"/>\n')
        edge = cx < pad + 30  # keep the label inside the figure when C4 is the first key
        edge_r = cx > total_w - pad - 30
        out.append(_text(pad if edge else (total_w - pad if edge_r else cx), top + kh + 21, "middle C", size=12, fill=INK,
                         anchor="start" if edge else ("end" if edge_r else "middle"), weight="bold"))
    return _svg(total_w, total_h, f"Piano keyboard from {start} to {end}", "".join(out))


# ---------------------------------------------------------------- 2. chord diagram
def chord_diagram(name, frets, fingers=None, barre=None, base_fret=1, highlight_root=None):
    """Guitar chord box. Low E (string 6) is the left line, high e (string 1) the right.

    frets: 6 values, string 6 to string 1: an int fret, 0 = open (o above the
        nut) or "x" = muted (x above). Frets are absolute: with base_fret=5 a
        dot at fret 5 sits in the top box and "5fr" is printed on the left.
    fingers: 6 values (None or 1-4), drawn inside the dots.
    barre: (fret, from_string, to_string), e.g. (1, 6, 1) for a full barre.
    base_fret: fret shown in the top box. 1 draws a thick nut.
    highlight_root: string number (6 to 1) whose dot or open circle is salmon.
    """
    if len(frets) != 6:
        raise ValueError("frets needs 6 values")
    played = [f for f in frets if isinstance(f, int) and f > 0]
    if barre:
        played.append(barre[0])
    last = max(played) if played else base_fret
    nrows = 5 if last - base_fret + 1 > 4 else 4
    sp, rh = 26, 30
    left = 58 if base_fret > 1 else 26
    top = 58
    gw = sp * 5
    w = left + gw + 26
    h = top + nrows * rh + 20
    sx = lambda st: left + (6 - st) * sp
    out = [_text(left + gw / 2, 26, name, size=22, fill=INK, weight="bold")]
    for i in range(nrows + 1):
        y = top + i * rh
        sw = 6 if (i == 0 and base_fret == 1) else 1.5
        out.append(f'<line x1="{left}" y1="{y}" x2="{left + gw}" y2="{y}" stroke="{INK}" stroke-width="{sw}"/>\n')
    for st in range(6, 0, -1):
        out.append(f'<line x1="{sx(st)}" y1="{top}" x2="{sx(st)}" y2="{top + nrows * rh}" '
                   f'stroke="{INK}" stroke-width="1.5"/>\n')
    if base_fret > 1:
        out.append(_text(left - 17, top + rh / 2 + 5, f"{base_fret}fr", size=13, fill=INK, anchor="end"))
    row_y = lambda f: top + (f - base_fret + 0.5) * rh
    in_barre = lambda st, f: bool(barre) and f == barre[0] and min(barre[1:]) <= st <= max(barre[1:])
    if barre:
        bf, a, b = barre
        x1, x2 = sx(max(a, b)), sx(min(a, b))
        y = row_y(bf)
        out.append(f'<rect x="{x1 - 11}" y="{y - 11}" width="{x2 - x1 + 22}" height="22" rx="11" fill="{INK}"/>\n')
        if fingers:
            fn = next((fingers[6 - st] for st in range(max(a, b), min(a, b) - 1, -1)
                       if fingers[6 - st]), None)
            if fn:
                out.append(_text(x1, y + 5, fn, size=13, fill="#fff", weight="bold"))
    for idx, f in enumerate(frets):
        st = 6 - idx
        x = sx(st)
        is_root = highlight_root == st
        if f == "x":
            c, d = top - 18, 6
            out.append(f'<path d="M{x - d} {c - d}L{x + d} {c + d}M{x + d} {c - d}L{x - d} {c + d}" '
                       f'stroke="{INK}" stroke-width="2" fill="none"/>\n')
        elif f == 0:
            out.append(f'<circle cx="{x}" cy="{top - 18}" r="6.5" fill="{SALMON if is_root else BG}" '
                       f'stroke="{INK}" stroke-width="1.8"/>\n')
        else:
            y = row_y(f)
            if in_barre(st, f):
                if is_root:
                    out.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{SALMON}" stroke="{INK}" stroke-width="1.5"/>\n')
                continue
            fill, ink = (SALMON, INK) if is_root else (INK, "#fff")
            out.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{fill}" stroke="{INK}" stroke-width="1.5"/>\n')
            fn = fingers[idx] if fingers else None
            if fn:
                out.append(_text(x, y + 5, fn, size=13, fill=ink, weight="bold"))
    return _svg(w, h, f"{name} chord diagram", "".join(out))


# ---------------------------------------------------------------- 3. fretboard
def fretboard(frets=12, marks=None, show_names=False, inlays=True,
              highlight_strings=None, start_fret=0):
    """Horizontal guitar neck, string 1 (high e) on top, string 6 at the bottom (as in tab).

    marks: list of dicts {string, fret, label, colour}; fret 0 is drawn left of the nut.
    show_names: label every position with its note name (standard tuning, sharps).
    inlays: dots at frets 3, 5, 7, 9, a double dot at 12 (and 15..24 likewise).
    highlight_strings: string numbers drawn with a sky-blue band.
    start_fret: first fret shown (0 shows the nut and open strings).
    """
    first = max(start_fret, 1)
    nslots = frets - first + 1
    fw, sp = 56, 26
    left = 56 if start_fret == 0 else 24
    top = 20
    h_neck = sp * 5
    w = left + nslots * fw + 20
    h = top + h_neck + 40
    gx = lambda slot: left + slot * fw
    sy = lambda st: top + (st - 1) * sp
    slot_c = lambda f: gx(f - first + 0.5)
    pos_x = lambda f: left - 20 if f == 0 else slot_c(f)
    out = []
    if inlays:
        midy = top + h_neck / 2
        for f in range(first, frets + 1):
            cx = slot_c(f)
            if f in (3, 5, 7, 9, 15, 17, 19, 21):
                out.append(f'<circle cx="{cx:g}" cy="{midy:g}" r="6" fill="#ddd"/>\n')
            elif f in (12, 24):
                for dy in (-sp, sp):
                    out.append(f'<circle cx="{cx:g}" cy="{midy + dy:g}" r="6" fill="#ddd"/>\n')
    for i in range(nslots + 1):
        sw = 6 if (i == 0 and start_fret == 0) else 1.5
        out.append(f'<line x1="{gx(i):g}" y1="{top}" x2="{gx(i):g}" y2="{top + h_neck}" '
                   f'stroke="{INK}" stroke-width="{sw}"/>\n')
    hs = set(highlight_strings or [])
    for st in range(1, 7):
        wdt = 1 + (st - 1) * 0.0 + (st - 1) * 0.3  # thicker for lower strings
        if st in hs:
            out.append(f'<line x1="{left}" y1="{sy(st)}" x2="{gx(nslots):g}" y2="{sy(st)}" '
                       f'stroke="{SKY}" stroke-width="{wdt + 6:g}"/>\n')
        out.append(f'<line x1="{left}" y1="{sy(st)}" x2="{gx(nslots):g}" y2="{sy(st)}" '
                   f'stroke="{INK}" stroke-width="{wdt:g}"/>\n')
    for f in range(first, frets + 1):
        out.append(_text(slot_c(f), top + h_neck + 24, f, size=12))
    if start_fret == 0:
        out.append(_text(pos_x(0), top + h_neck + 24, "0", size=12))
    placed = {(mk["string"], mk["fret"]): mk for mk in (marks or [])}
    if show_names:
        rng = ([0] if start_fret == 0 else []) + list(range(first, frets + 1))
        for st in range(1, 7):
            for f in rng:
                if (st, f) not in placed:
                    out.append(_text(pos_x(f), sy(st) + 4, _pc_name(st, f), size=10, fill="#777"))
    for (st, f), mk in placed.items():
        if f == 0 and start_fret != 0:
            continue
        if f != 0 and not (first <= f <= frets):
            continue
        cx, cy = pos_x(f), sy(st)
        out.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="10" fill="{_colour(mk.get("colour"))}" '
                   f'stroke="{INK}" stroke-width="1.5"/>\n')
        lab = mk.get("label")
        if lab is None and show_names:
            lab = _pc_name(st, f)
        if lab not in (None, ""):
            out.append(_text(cx, cy + 4, lab, size=11 if len(str(lab)) < 3 else 9,
                             fill=INK, weight="bold"))
    return _svg(w, h, f"Guitar fretboard, frets {start_fret} to {frets}", "".join(out))


# ---------------------------------------------------------------- 4. staff notes (verovio)
def _abc_pitch(note, accidental_style="sharp"):
    """Scientific pitch (or MIDI int) to an ABC pitch with accidental."""
    name = midi_to_name(note, "flat" if accidental_style == "flat" else "sharp") \
        if isinstance(note, int) else note
    letter, acc, octave = _parse(name)
    prefix = {"": "", "#": "^", "b": "_", "##": "^^", "x": "^^", "bb": "__"}[acc]
    if octave >= 5:
        body = letter.lower() + "'" * (octave - 5)
    else:
        body = letter + "," * (4 - octave)
    return prefix + body


def _verovio(data, title, fmt="abc"):
    import verovio
    tk = verovio.toolkit()
    tk.setOptions({
        "inputFrom": fmt, "pageWidth": 700, "pageHeight": 600,
        "adjustPageHeight": True, "adjustPageWidth": True, "scale": 60,
        "header": "none", "footer": "none",
        "pageMarginTop": 40, "pageMarginBottom": 40,
        "pageMarginLeft": 20, "pageMarginRight": 20,
    })
    if not tk.loadData(data):
        raise ValueError("verovio could not read the input")
    svg = tk.renderToSVG(1)
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
    svg = re.sub(r"<desc>.*?</desc>\s*", "", svg, flags=re.S)
    root = re.search(r"<svg\b[^>]*>", svg).group(0)
    w = float(re.search(r'\bwidth="([\d.]+)px"', root).group(1))
    h = float(re.search(r'\bheight="([\d.]+)px"', root).group(1))
    sid = re.search(r'\bid="([^"]+)"', root).group(1)  # verovio's CSS is keyed to this id
    new_root = (f'<svg id="{sid}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w:g} {h:g}" '
                f'width="{w:g}" height="{h:g}" role="img" aria-label="{_attr(title)}" '
                f'font-family="{FONT}">\n<title>{escape(title)}</title>\n'
                f'<rect width="{w:g}" height="{h:g}" fill="{BG}"/>')
    svg = svg.replace(root, new_root, 1)
    return svg if svg.endswith("\n") else svg + "\n"


def staff_note(note, clef="treble", accidental_style="sharp"):
    """One whole note on a staff (verovio, ABC input).

    note: scientific pitch like "C4", "F#3", "Bb4" (spelling kept as written),
        or a MIDI int, in which case accidental_style ("sharp" or "flat")
        picks the spelling.
    clef: "treble" or "bass". Ledger lines are drawn automatically.
    """
    if clef not in ("treble", "bass"):
        raise ValueError("clef must be 'treble' or 'bass'")
    pitch = _abc_pitch(note, accidental_style)
    abc = f"X:1\nL:1/1\nK:C clef={clef}\n{pitch}|]\n"
    label = note if isinstance(note, str) else midi_to_name(note, accidental_style)
    return _verovio(abc, f"{label} on the {clef} clef")


def staff_note_grand(note, accidental_style="sharp"):
    """One whole note on a grand staff (treble above, bass below, with a brace).
    Notes from middle C up go on the treble staff, lower ones on the bass staff.
    Verovio's ABC reader cannot do two staves, so this one is built as MEI."""
    name = midi_to_name(note, "flat" if accidental_style == "flat" else "sharp")         if isinstance(note, int) else note
    letter, acc, octave = _parse(name)
    midi = note_to_midi(name)
    accid = {"": "", "#": "s", "b": "f", "##": "x", "x": "x", "bb": "ff"}[acc]
    acc_attr = f' accid="{accid}"' if accid else ""
    note_xml = f'<note pname="{letter.lower()}" oct="{octave}" dur="1"{acc_attr}/>'
    rest = '<space dur="1"/>'
    t, b = (note_xml, rest) if midi >= 60 else (rest, note_xml)
    mei = f'''<?xml version="1.0" encoding="UTF-8"?>
<mei xmlns="http://www.music-encoding.org/ns/mei" meiversion="5.0"><music><body><mdiv><score>
<scoreDef><staffGrp symbol="brace" bar.thru="true">
<staffDef n="1" lines="5" clef.shape="G" clef.line="2"/>
<staffDef n="2" lines="5" clef.shape="F" clef.line="4"/>
</staffGrp></scoreDef>
<section><measure right="end">
<staff n="1"><layer n="1">{t}</layer></staff>
<staff n="2"><layer n="1">{b}</layer></staff>
</measure></section></score></mdiv></body></music></mei>'''
    label = name
    return _verovio(mei, f"{label} on the grand staff", fmt="mei")


# ---------------------------------------------------------------- 5. save
FIG_ROOT = pathlib.Path(__file__).resolve().parents[2] / "docs" / "assets" / "figures"


def save(svg, relpath):
    """Write svg to docs/assets/figures/<relpath> (folders created, LF endings).
    Returns the path."""
    path = FIG_ROOT / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    return path
