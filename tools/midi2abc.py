#!/usr/bin/env python3
"""midi2abc: turn a standard MIDI file into ABC 2.1 notation (pure Python, no packages).

Built for the practice players in this book. It reads a type 0 or type 1 MIDI
file (for example a Mutopia download, or the reader's own file) and writes an
ABC tune that abcjs can draw and play.

What it does
  * Header: T:, C:, M: (from the time signature), L:1/8 or L:1/16 (chosen from
    the shortest note), Q: (from the tempo), K: (from the key signature).
  * Notes, rests, chords ([CEG]), ties across bar lines, and bar lines every bar
    (4 bars to a line by default, closing with |]).
  * One voice per MIDI track. Two note tracks become a piano score:
        %%score {RH LH}, V:RH clef=treble, V:LH clef=bass
    A staff whose notes cannot share one rhythm (a melody over held chords) is
    split into two voices (RH and RH2) so that every voice is monophonic or a
    plain chord line. Use --split NAME to force this for a staff.
  * Spelling comes from the key: sharp keys get sharps, flat keys get flats, a
    minor key gets its raised leading tone (G# in A minor). Notes outside the
    key that are white keys on the piano are written as naturals. Override
    with --spell 1=Db,6=Gb (pitch class to name) or per note in a marks file.
  * Grace notes: MIDI plays them as very short notes that steal time from the
    note before. Notes shorter than a 32nd are dropped and the note before gets
    its time back (the ABC does not write the grace note).
  * Repeats: MIDI usually plays every repeat out. Tell the converter which bars
    are the duplicate, and it writes |: and :| (and [1 [2) instead, after
    checking that the duplicate is identical:
        --repeat S:B        bars S..S+B-1 are played twice in a row
        --volta S:B:E1:E2   body of B bars, E1 bars of first ending, body again,
                            E2 bars of second ending
    Bar numbers here are MIDI bar numbers (the pickup bar is bar 0, the first
    full bar is bar 1). Repeat the option for more than one repeat.
    If the MIDI plays each repeat only once, add the signs without dropping
    any bars: --sign-repeat S:B and --sign-volta S:B:E1:E2 (endings follow
    the body one after the other).

Guitar: --guitar writes clef=treble-8 with every note an octave above the sound
(as printed guitar music), --options 'tab=guitar sound=nylon' adds the book's
%%opts line, --floor 40 lifts notes below the low E string by an octave, and --merge-tracks puts several MIDI tracks (for example the two
staves of a lute score) on one staff. --check understands the octave shift.

Key changes: --key-change BAR:KEY (MIDI bar number, repeatable) writes an inline
[K:C] at that bar and spells the following notes in the new key.

Marks file (--marks FILE): details that MIDI loses (slurs, staccato dots,
dynamics, text, fermatas, spelling). One mark per line:
        VOICE BAR OFFSET TEXT
    BAR is the notated bar number (after repeats are folded; pickup is 0).
    OFFSET is the position in the bar as a fraction of a whole note: 0, 1/4,
    3/8. TEXT goes in front of the note or rest that starts there, for example
    !p!   "^Allegro"   (   .   !fermata!. A TEXT that starts with < goes after
    the note instead (<) closes a slur); for a note that runs over a bar line
    (written as tied pieces) < goes after the last piece and << after the first. A TEXT that starts with = sets the
    spelling of one pitch there: =61:Db. Lines starting with # are comments.

Check mode: --check TUNE.abc FILE.mid reads the ABC back (repeats unfolded, ties
joined) and compares every note (pitch, start, length, per staff) with the MIDI.
It exits with 1 and lists differences when they do not match.

Usage
    py tools/midi2abc.py piece.mid -o piece.abc --title "Minuet" --composer "Anon (1700-1750)"
    py tools/midi2abc.py piece.mid --key G --pickup 1/8 --repeat 1:16
    py tools/midi2abc.py --check piece.abc piece.mid

Limits: durations must be plain or dotted notes, or triplets of three equal notes, and
timing is snapped to 1/96 of a whole note. Written for LilyPond-style, exactly
timed MIDI; a loosely played file needs a coarser snap (see --snap).
"""

import argparse
import re
import struct
import sys
from fractions import Fraction

UNIT = 96  # grid units in a whole note (1/32 = 3 units, a triplet 8th = 8)
VALID = [96, 72, 48, 36, 24, 18, 12, 9, 6, 3]  # notatable lengths in units
LETTERS = "CDEFGAB"
STEP = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
SHARP_ORDER = "FCGDAEB"
FLAT_ORDER = "BEADGCF"
MAJOR_FIFTHS = {"C": 0, "G": 1, "D": 2, "A": 3, "E": 4, "B": 5, "F#": 6, "C#": 7,
                "F": -1, "Bb": -2, "Eb": -3, "Ab": -4, "Db": -5, "Gb": -6, "Cb": -7}
MINOR_FIFTHS = {"A": 0, "E": 1, "B": 2, "F#": 3, "C#": 4, "G#": 5, "D#": 6, "A#": 7,
                "D": -1, "G": -2, "C": -3, "F": -4, "Bb": -5, "Eb": -6, "Ab": -7}


class ConvertError(Exception):
    pass


# ---------------------------------------------------------------- MIDI reading

def _vlq(data, i):
    value = 0
    while True:
        b = data[i]
        i += 1
        value = (value << 7) | (b & 0x7F)
        if not b & 0x80:
            return value, i


class MidiFile:
    """Parsed MIDI: ppq, tempo (microseconds per quarter), time signature,
    key signature (sharps, is_minor) and, per track, a list of notes
    (start_tick, end_tick, pitch)."""

    def __init__(self, data):
        if data[:4] != b"MThd":
            raise ConvertError("not a MIDI file")
        fmt, ntracks, division = struct.unpack(">HHH", data[8:14])
        if fmt not in (0, 1):
            raise ConvertError("only MIDI type 0 and 1 are supported")
        if division & 0x8000:
            raise ConvertError("SMPTE time division is not supported")
        self.ppq = division
        self.tempo = None
        self.timesig = None
        self.keysig = None
        self.tracks = []
        self.names = []
        pos = 14
        for _ in range(ntracks):
            if data[pos:pos + 4] != b"MTrk":
                raise ConvertError("bad track header")
            length = struct.unpack(">I", data[pos + 4:pos + 8])[0]
            self._track(data[pos + 8:pos + 8 + length])
            pos += 8 + length
        if fmt == 0:
            self._split_channels()

    def _track(self, tr):
        i = 0
        tick = 0
        status = 0
        on = {}
        notes = []
        name = ""
        while i < len(tr):
            delta, i = _vlq(tr, i)
            tick += delta
            b = tr[i]
            if b == 0xFF:
                kind = tr[i + 1]
                n, k = _vlq(tr, i + 2)
                body = tr[k:k + n]
                i = k + n
                if kind == 0x03 and not name:
                    name = body.decode("latin-1", "replace").strip()
                elif kind == 0x51 and self.tempo is None and n == 3:
                    self.tempo = int.from_bytes(body, "big")
                elif kind == 0x58 and self.timesig is None and n >= 2:
                    self.timesig = (body[0], 1 << body[1])
                elif kind == 0x59 and self.keysig is None and n == 2:
                    sf = body[0] - 256 if body[0] > 127 else body[0]
                    self.keysig = (sf, bool(body[1]))
            elif b in (0xF0, 0xF7):
                n, k = _vlq(tr, i + 1)
                i = k + n
            else:
                if b & 0x80:
                    status = b
                    i += 1
                kind = status >> 4
                chan = status & 15
                if kind in (0xC, 0xD):
                    i += 1
                    continue
                a, v = tr[i], tr[i + 1]
                i += 2
                if kind == 9 and v > 0:
                    on.setdefault((chan, a), []).append(tick)
                elif kind == 8 or (kind == 9 and v == 0):
                    stack = on.get((chan, a))
                    if stack:
                        notes.append((stack.pop(0), tick, a, chan))
        notes.sort()
        self.tracks.append(notes)
        self.names.append(name)

    def _split_channels(self):
        notes = self.tracks[0]
        chans = sorted({n[3] for n in notes})
        if len(chans) > 1:
            self.tracks = [[n for n in notes if n[3] == c] for c in chans]
            self.names = ["channel %d" % c for c in chans]


def quantize_tracks(midi, snap=1, tracks=None, merge=False, floor=None):
    """Return a list of staves; each staff is a sorted list of (start, end, pitch)
    in grid units. Grace notes are dropped (see module docstring)."""
    scale = Fraction(UNIT, 4 * midi.ppq)
    grace_len = midi.ppq / 8
    staves = []
    for idx, notes in enumerate(midi.tracks):
        if not notes or (tracks is not None and idx not in tracks):
            continue
        notes = [list(n) for n in notes]
        graces = [n for n in notes if n[1] - n[0] < grace_len]
        for g in graces:  # in time order, so a run of grace notes hands its time back in turn
            for n in notes:
                if n is not g and abs(n[1] - g[0]) <= 3 and n[1] - n[0] >= grace_len:
                    n[1] = g[1]
        notes = [n for n in notes if n[1] - n[0] >= grace_len]
        q = []
        for s, e, p, _ in notes:
            qs = int(round(s * scale / snap)) * snap
            qe = int(round(e * scale / snap)) * snap
            if floor is not None:
                while p < floor:  # lift notes below the playable range by an octave
                    p += 12
            if qe > qs:
                q.append((qs, qe, p))
        q.sort()
        staves.append(q)
    if merge and len(staves) > 1:
        staves = [sorted(n for st in staves for n in st)]
    return staves


# ---------------------------------------------------------- voices and spelling

def staff_events(notes):
    """Group notes of one staff by start. Return a list of (start, end, [pitches])
    when every start group has one end and nothing overlaps; else None."""
    groups = {}
    for s, e, p in notes:
        groups.setdefault(s, []).append((e, p))
    events = []
    last_end = 0
    for s in sorted(groups):
        ends = {e for e, _ in groups[s]}
        if len(ends) > 1 or s < last_end:
            return None
        e = ends.pop()
        events.append((s, e, sorted(p for _, p in groups[s])))
        last_end = e
    return events


def split_voices(notes, max_voices=3, assign="low"):
    """Split a staff into voices. At each start the notes are grouped by end; the
    group with the highest top note goes to the lowest free voice (voice 0 is
    the upper voice, so a melody over held chords stays in voice 0)."""
    groups = {}
    for s, e, p in notes:
        groups.setdefault((s, e), []).append(p)
    by_start = {}
    for (s, e), ps in groups.items():
        by_start.setdefault(s, []).append((e, sorted(ps)))
    voices = [[] for _ in range(max_voices)]
    free_at = [0] * max_voices
    for s in sorted(by_start):
        subs = sorted(by_start[s], key=lambda x: -x[1][-1])
        free = [v for v in range(max_voices) if free_at[v] <= s]
        if len(subs) == 1 and len(free) > 1:
            # one group and several free voices: keep to the lowest voice unless
            # that would put this group on the wrong side of a sounding voice
            top = subs[0][1][-1]
            busy = [(v, voices[v][-1][2][-1]) for v in range(max_voices) if free_at[v] > s and voices[v]]
            def penalty(v):
                return sum(1 for bv, bt in busy if (v < bv and top < bt) or (v > bv and top > bt))
            def gap(v):  # distance from this voice's last note ("near" mode: a bass line stays a bass line)
                return abs(voices[v][-1][2][-1] - top) if voices[v] else 1000 + v
            if assign == "near":
                free = [min(free, key=lambda v: (penalty(v), gap(v), v))]
            else:
                free = [min(free, key=lambda v: (penalty(v), v))]
        if len(free) < len(subs):
            raise ConvertError("more than %d voices needed in one staff at unit %d" % (max_voices, s))
        for (e, ps), v in zip(subs, free):
            voices[v].append((s, e, ps))
            free_at[v] = e
    return [v for v in voices if v]


def key_info(sf, minor):
    acc = {l: 0 for l in LETTERS}
    if sf > 0:
        for l in SHARP_ORDER[:sf]:
            acc[l] = 1
    elif sf < 0:
        for l in FLAT_ORDER[:-sf]:
            acc[l] = -1
    return acc


def parse_key(text):
    t = text.strip()
    minor = t.endswith("m") and not t.endswith("dim")
    name = t[:-1] if minor else t
    name = name[0].upper() + name[1:]
    table = MINOR_FIFTHS if minor else MAJOR_FIFTHS
    if name not in table:
        raise ConvertError("unknown key %r (try G, Bb, Am, F#m)" % text)
    return table[name], minor


def key_name(sf, minor):
    table = MINOR_FIFTHS if minor else MAJOR_FIFTHS
    for n, f in table.items():
        if f == sf:
            return n + ("m" if minor else "")
    return "C"


class Speller:
    def __init__(self, sf, minor, pc_overrides=None):
        self.sf = sf
        self.minor = minor
        self.keyacc = key_info(sf, minor)
        self.pc_over = pc_overrides or {}
        self.table = {}
        for l in LETTERS:
            self.table[(STEP[l] + self.keyacc[l]) % 12] = (l, self.keyacc[l])
        if minor:
            tonic_name = key_name(sf, True)[:-1]
            ti = LETTERS.index(tonic_name[0])
            l7 = LETTERS[ti - 1]
            self.table[(STEP[l7] + self.keyacc[l7] + 1) % 12] = (l7, self.keyacc[l7] + 1)

    def spell(self, midi, forced=None):
        pc = midi % 12
        if forced:
            return forced
        if pc in self.pc_over:
            return self.pc_over[pc]
        if pc in self.table:
            return self.table[pc]
        for l in LETTERS:
            if STEP[l] == pc:
                return (l, 0)
        names = {1: "C", 3: "D", 6: "F", 8: "G", 10: "A"} if self.sf >= 0 else {1: "D", 3: "E", 6: "G", 8: "A", 10: "B"}
        return (names[pc], 1 if self.sf >= 0 else -1)


def parse_name(text):
    """'Db' -> ('D', -1), 'F#' -> ('F', 1), 'Gn' -> ('G', 0)."""
    t = text.strip()
    letter = t[0].upper()
    acc = {"": 0, "#": 1, "b": -1, "n": 0, "##": 2, "bb": -2}.get(t[1:])
    if letter not in LETTERS or acc is None:
        raise ConvertError("bad note name %r" % text)
    return (letter, acc)


def abc_note_name(midi, spelled):
    letter, acc = spelled
    octave = (midi - acc - STEP[letter]) // 12 - 1
    if octave >= 5:
        base = letter.lower() + "'" * (octave - 5)
    else:
        base = letter + "," * (4 - octave)
    # octave 4 is the capital letter with no commas, octave 5 the lowercase
    return base, letter, octave, acc


def acc_text(acc):
    return {0: "=", 1: "^", -1: "_", 2: "^^", -2: "__"}[acc]


# ------------------------------------------------------------------ writing ABC

def decompose(n):
    out = []
    while n > 0:
        for v in VALID:
            if v <= n:
                out.append(v)
                n -= v
                break
        else:
            raise ConvertError("length of %d units is not a plain or dotted note" % n)
    return out


def dur_text(d, unit_l):
    f = Fraction(d, unit_l)
    if f == 1:
        return ""
    if f.denominator == 1:
        return str(f.numerator)
    if f.numerator == 1:
        return "/" + str(f.denominator) if f.denominator != 2 else "/"
    return "%d/%d" % (f.numerator, f.denominator)


class Piece:
    """The result of a conversion."""

    def __init__(self):
        self.text = ""
        self.staves = []        # per staff: list of voice names
        self.voice_events = {}  # voice name -> list of (start, end, pitches or None) in units
        self.voice_tokens = {}  # voice name -> list of written note tokens (notated order)
        self.nbars = 0
        self.key = ""
        self.meter = ""


def make_beat(num, den):
    if den >= 8:
        group = 3 if num % 3 == 0 else 2
        return group * UNIT // den
    return UNIT // 4


def _rest_pieces(start, end):
    """A gap as one or more rests. A gap that is not a plain or dotted note length
    (it sits between triplet notes) is cut into triplet eighths."""
    try:
        decompose(end - start)
        return [(start, end, None)]
    except ConvertError:
        if start % 8 == 0 and (end - start) % 8 == 0:
            return [(p, p + 8, None) for p in range(start, end, 8)]
        return [(start, end, None)]


def build_events(events, total):
    """Fill gaps with rests: returns list of (start, end, pitches or None)."""
    out = []
    pos = 0
    for s, e, ps in events:
        if s > pos:
            out.extend(_rest_pieces(pos, s))
        out.append((s, e, ps))
        pos = e
    if pos < total:
        out.extend(_rest_pieces(pos, total))
    return out


def parse_marks(path):
    marks = {}
    spells = {}
    with open(path, encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            parts = line.split(None, 3)
            if len(parts) < 4:
                raise ConvertError("%s:%d: need VOICE BAR OFFSET TEXT" % (path, ln))
            voice, bar, off, text = parts
            key = (voice, int(bar), Fraction(off))
            if text.startswith("="):
                m, name = text[1:].split(":")
                spells.setdefault(key, {})[int(m)] = parse_name(name)
            else:
                marks.setdefault(key, []).append(text)
    return marks, spells


def _plan_folds(repeats, voltas, first_num, nbar, sign_repeats=(), sign_voltas=()):
    """Work out which bars to drop and where the repeat signs go. Bar indexes
    here count from 0 at the first bar of the file (the pickup, if any)."""
    drop, start_rep, end_rep, volta1, volta2, checks = set(), set(), set(), set(), set(), []
    for s, b in repeats:
        i0 = s - first_num
        drop.update(range(i0 + b, i0 + 2 * b))
        start_rep.add(i0)
        end_rep.add(i0 + b - 1)
        checks.append((i0, i0 + b, b))
    for s, b, e1, e2 in voltas:
        i0 = s - first_num
        drop.update(range(i0 + b + e1, i0 + 2 * b + e1))
        start_rep.add(i0)
        volta1.update(range(i0 + b, i0 + b + e1))
        end_rep.add(i0 + b + e1 - 1)
        volta2.update(range(i0 + 2 * b + e1, i0 + 2 * b + e1 + e2))
        checks.append((i0, i0 + b + e1, b))
    for s, b in sign_repeats:
        i0 = s - first_num
        start_rep.add(i0)
        end_rep.add(i0 + b - 1)
    for s, b, e1, e2 in sign_voltas:
        i0 = s - first_num
        start_rep.add(i0)
        volta1.update(range(i0 + b, i0 + b + e1))
        end_rep.add(i0 + b + e1 - 1)
        volta2.update(range(i0 + b + e1, i0 + b + e1 + e2))
    for a, c, n in checks:
        if a < 0 or c + n > nbar:
            raise ConvertError("repeat bars %d-%d are outside the piece" % (a + first_num, c + n - 1 + first_num))
    return drop, start_rep, end_rep, volta1, volta2, checks


def _render_voice(vname, evs, bounds, spellers, unit_l, beat, notated_of, marks, mark_spells, used, secondary=False, shift=0):
    """Write one voice as a list of bar strings (one per bar in bounds)."""
    nbar = len(bounds) - 1
    toks = [[] for _ in range(nbar)]
    sigs = [[] for _ in range(nbar)]
    spelled = []
    state = {}
    state_bar = -1
    written = []
    bi = 0
    # triplets: three equal events of 4, 8 or 16 units that start on a group boundary
    tri_first, tri_all = set(), set()
    for idx in range(len(evs) - 2):
        s0, e0, _ = evs[idx]
        d0 = e0 - s0
        if idx in tri_all or d0 not in (4, 8, 16, 32):
            continue
        if all(evs[idx + k][1] - evs[idx + k][0] == d0 and evs[idx + k][0] == s0 + k * d0 for k in range(3)):
            b0 = max(i for i in range(nbar) if bounds[i] <= s0)
            if (s0 - bounds[b0]) % (3 * d0) == 0 and s0 + 3 * d0 <= bounds[b0 + 1]:
                tri_first.add(idx)
                tri_all.update((idx, idx + 1, idx + 2))
    for ei, (s, e, ps) in enumerate(evs):
        while bounds[bi + 1] <= s:
            bi += 1
        nnum = notated_of.get(bi)
        off = Fraction(s - bounds[bi], UNIT)
        pre = post = post_first = ""
        forced = {}
        if nnum is not None:
            mkey = (vname, nnum, off)
            if mkey in marks:
                used.add(mkey)
                for t in marks[mkey]:
                    if t.startswith("<<"):
                        post_first += t[2:]
                    elif t.startswith("<"):
                        post += t[1:]
                    else:
                        pre += t
            if mkey in mark_spells:
                used.add(mkey)
                forced = mark_spells[mkey]
        # parts: (bar index, position, length)
        parts = []
        pos, b = s, bi
        if ei in tri_all:
            parts = [(bi, s, e - s)]
            if ei in tri_first:
                pre = "(3" + pre
        else:
            while pos < e:
                seg = min(e, bounds[b + 1])
                for d in decompose(seg - pos):
                    parts.append((b, pos, d))
                    pos += d
                b += 1
        for k, (pb, pp, d) in enumerate(parts):
            first, last = k == 0, k == len(parts) - 1
            dt = dur_text(d * 3 // 2 if ei in tri_all else d, unit_l)
            if ps is None:
                text = ("x" if secondary else "z") + dt
            else:
                if pb != state_bar:
                    state, state_bar = {}, pb
                names = []
                speller = spellers[pb]
                for m in ps:
                    sp = speller.spell(m, forced.get(m))
                    base, letter, octv, acc = abc_note_name(m + shift, sp)
                    have = state.get((letter, octv), speller.keyacc[letter])
                    names.append((acc_text(acc) if have != acc else "") + base)
                    if first:
                        spelled.append((pb, letter, acc))
                    state[(letter, octv)] = acc
                body = names[0] if len(ps) == 1 else "[" + "".join(names) + "]"
                text = body + dt + ("" if last else "-") + (post_first if first and not last else "")
                written.append((pb, pp, d, ps))
            if first:
                text = pre + text
            if last:
                text += post + (post_first if first else "")
            toks[pb].append((pp, d, text))
            sigs[pb].append((pp - bounds[pb], d, tuple(ps) if ps else None))
    bars = []
    for bi in range(nbar):
        line, prev = "", 0
        for pos, d, text in toks[bi]:
            if line and ((pos - bounds[bi]) % beat == 0 or d >= 24 or prev >= 24):
                line += " "
            line += text
            prev = d
        bars.append(line)
    return bars, written, sigs, spelled


def convert(midi, title="", composer="", source="", key=None, meter=None, unit_l=None,
            tempo=None, pickup=None, names=None, clefs=None, split=(), spell=None,
            marks_path=None, repeats=(), voltas=(), sign_repeats=(), sign_voltas=(), bars_per_line=4, snap=1, tracks=None,
            comments=(), tempo_unit="1/4", key_changes=(), guitar=False, merge_tracks=False, options="", voice_assign="low", max_voices=3, floor=None):
    """Convert a MidiFile to ABC. Returns a Piece (see its .text)."""
    staves = quantize_tracks(midi, snap=snap, tracks=tracks, merge=merge_tracks, floor=floor)
    if not staves:
        raise ConvertError("no notes found")
    num, den = meter or midi.timesig or (4, 4)
    sf, minor = parse_key(key) if key else (midi.keysig or (0, False))
    speller = Speller(sf, minor, spell)
    if UNIT * num % den:
        raise ConvertError("time signature %d/%d does not fit the grid" % (num, den))
    bar_len = UNIT * num // den
    pick = int(Fraction(pickup) * UNIT) if pickup else 0
    if pick >= bar_len:
        raise ConvertError("the pickup is as long as a bar or longer")
    end = max(n[1] for st in staves for n in st)
    bounds = [0] + ([pick] if pick else [])
    while bounds[-1] < end:
        bounds.append(bounds[-1] + bar_len)
    total = bounds[-1]
    nbar = len(bounds) - 1
    first_num = 0 if pick else 1
    marks, mark_spells = parse_marks(marks_path) if marks_path else ({}, {})

    if len(staves) == 1:
        default_names = ["Melody"]
    elif len(staves) == 2:
        default_names = ["RH", "LH"]
    else:
        default_names = ["V%d" % (i + 1) for i in range(len(staves))]
    names = names or default_names
    if len(names) < len(staves):
        raise ConvertError("--names needs %d names" % len(staves))
    if guitar:
        clefs = ["treble-8"] * len(staves)
    if clefs is None:
        clefs = ["treble" if sum(n[2] for n in st) / len(st) >= 58 else "bass" for st in staves]
    voices = []
    piece = Piece()
    for si, st in enumerate(staves):
        ev = staff_events(st) if names[si] not in split else None
        groups = [ev] if ev is not None else split_voices(st, max_voices=max_voices, assign=voice_assign)
        nm = []
        for gi, g in enumerate(groups):
            vname = names[si] if gi == 0 else names[si] + str(gi + 1)
            nm.append(vname)
            voices.append((vname, clefs[si], build_events(g, total)))
        piece.staves.append(nm)

    if unit_l is None:
        shortest = min(e - s for _, _, evs in voices for s, e, ps in evs if ps)
        unit_l = 6 if shortest < 12 else 12
    else:
        unit_l = int(UNIT * Fraction(unit_l))
    beat = make_beat(num, den)

    spellers, changed = [], {}
    cur = speller
    changes = {b - first_num: parse_key(k) for b, k in key_changes}
    for bi in range(nbar):
        if bi in changes:
            cur = Speller(changes[bi][0], changes[bi][1], spell)
            changed[bi] = "[K:%s]" % key_name(*changes[bi])
        spellers.append(cur)
    drop, start_rep, end_rep, volta1, volta2, checks = _plan_folds(repeats, voltas, first_num, nbar, sign_repeats, sign_voltas)
    kept = [i for i in range(nbar) if i not in drop]
    notated_of = {i: n + (0 if pick else 1) for n, i in enumerate(kept)}

    rendered, used, sigs = {}, set(), {}
    piece.spelled = {}
    for vname, clef, evs in voices:
        rendered[vname], piece.voice_tokens[vname], sigs[vname], piece.spelled[vname] = _render_voice(
            vname, evs, bounds, spellers, unit_l, beat, notated_of, marks, mark_spells, used,
            secondary=vname not in [nm[0] for nm in piece.staves], shift=12 if guitar else 0)
        piece.voice_events[vname] = evs
        for bi, txt in changed.items():
            rendered[vname][bi] = txt + rendered[vname][bi]
    for key_ in list(marks) + list(mark_spells):
        if key_ not in used:
            raise ConvertError("mark %s bar %d offset %s did not land on the start of a note or rest" % key_)
    for a, c, n in checks:
        for vname in rendered:
            for k in range(n):
                if sigs[vname][a + k] != sigs[vname][c + k]:
                    raise ConvertError("bars %d and %d differ in voice %s, so this is not a plain repeat"
                                       % (a + k + first_num, c + k + first_num, vname))

    def barline(i_left, i_right):
        left_end = i_left in end_rep
        right_start = i_right is not None and i_right in start_rep
        if i_right is None:
            return ":|]" if left_end else "|]"
        line = "::" if left_end and right_start else ":|" if left_end else "|:" if right_start else "|"
        if i_right in volta1 and i_left not in volta1:
            line += "[1"
        elif i_right in volta2 and i_left not in volta2:
            line += "[2"
        return line

    head = (["%%opts " + options] if options else []) + ["% " + c for c in comments]
    if source:
        head.append("% Source: " + source)
    head.append("X:1")
    if title:
        head.append("T:" + title)
    if composer:
        head.append("C:" + composer)
    head.append("M:%d/%d" % (num, den))
    head.append("L:1/%d" % (8 if unit_l == 12 else 16))
    bpm = tempo or (round(60000000 / midi.tempo) if midi.tempo else None)
    if bpm:
        head.append("Q:%s=%d" % (tempo_unit, bpm))
    if len(voices) > 1:
        head.append("K:" + key_name(sf, minor))
        grp = [nm[0] if len(nm) == 1 else "(" + " ".join(nm) + ")" for nm in piece.staves]
        head.append(("%%score {" + " ".join(grp) + "}") if len(staves) == 2 else "%%score " + " ".join(grp))
        for vname, clef, evs in voices:
            head.append("V:%s clef=%s" % (vname, clef))
    else:
        head.append("K:" + key_name(sf, minor) + " clef=" + voices[0][1])
    body = []
    n = len(kept)
    for chunk in range(0, n, bars_per_line):
        for vname, clef, evs in voices:
            if len(voices) > 1:
                body.append("V:" + vname)
            line = "|: " if chunk == 0 and kept[0] in start_rep else ""
            for k in range(chunk, min(chunk + bars_per_line, n)):
                nxt = kept[k + 1] if k + 1 < n else None
                line += rendered[vname][kept[k]] + " " + barline(kept[k], nxt) + " "
            body.append(line.rstrip())
    piece.text = "\n".join(head + body) + "\n"
    piece.nbars = n
    piece.kept = kept
    piece.spelled = {v: [(l, a) for (bi, l, a) in sp if bi in set(kept)] for v, sp in piece.spelled.items()}
    piece.key = key_name(sf, minor)
    piece.meter = "%d/%d" % (num, den)
    return piece


# --------------------------------------------------------------------- checking

def read_abc(text, unfold=True):
    """Parse the ABC this tool writes (plus plain hand-written tunes). Returns
    (staff_notes, bar_counts): staff_notes[i] = sorted (start, end, pitch) in
    grid units with repeats unfolded and ties joined."""
    unit = Fraction(1, 8)
    num, den = 4, 4
    sf, minor = 0, False
    voices = {}  # name -> list of bars; bar = dict(events, start_rep, end_rep, volta)
    order = []
    staff_groups = []
    cur = None
    curbar = None
    volta = {}
    for raw in text.splitlines():
        line = raw.split("%", 1)[0] if not raw.startswith("%%") else raw
        line = line.strip()
        if not line:
            continue
        if line.startswith("%%score"):
            body = line[7:]
            body = body.replace("{", " ").replace("}", " ").replace("|", " ")
            toks = body.replace("(", " ( ").replace(")", " ) ").split()
            grp = None
            for t in toks:
                if t == "(":
                    grp = []
                elif t == ")":
                    staff_groups.append(grp)
                    grp = None
                elif grp is not None:
                    grp.append(t)
                else:
                    staff_groups.append([t])
            continue
        if line.startswith("%"):
            continue
        if len(line) > 1 and line[1] == ":" and line[0] in "XTCMLQKVNZ":
            f, v = line[0], line[2:].strip()
            if f == "M":
                num, den = (int(x) for x in v.split("/"))
            elif f == "L":
                a, b = v.split("/")
                unit = Fraction(int(a), int(b))
            elif f == "K":
                tonic = v.split()[0]
                m = tonic.endswith("m") and len(tonic) > 1
                sf, minor = parse_key(tonic)
            elif f == "V":
                cur = v.split()[0]
                if cur not in voices:
                    voices[cur] = {"bars": [], "pend": None}
                    order.append(cur)
                curbar = None
            continue
        if cur is None:
            cur = "1"
            voices[cur] = {"bars": [], "pend": None}
            order.append(cur)
        voices[cur].setdefault("keyacc", key_info(sf, minor))
        _read_body(line, voices[cur], unit, None, num, den)
    for name in voices:
        v = voices[name]
        if v["pend"] is not None and v["pend"]["events"]:
            v["bars"].append(v["pend"])
            v["pend"] = None
    if not staff_groups:
        staff_groups = [[n] for n in order]
    shift = 12 if "treble-8" in text else 0  # guitar: written an octave above the sound
    result = []
    for grp in staff_groups:
        notes = []
        for name in grp:
            notes.extend((a, b, p - shift) for a, b, p in _join_ties(_unfold(voices[name]["bars"]) if unfold else voices[name]["bars"]))
        result.append(notes)
    return result, {n: len(voices[n]["bars"]) for n in order}, staff_groups


_BARLINE = re.compile(r"::|:\|\]|:\||\|\]|\|\||\|:|\||(?=\[[12])")
_VOLTA = re.compile(r"\[?([12])")


def _read_body(line, v, unit, keyacc, num, den):
    def new_bar(start_rep=False):
        return {"events": [], "start_rep": start_rep, "end_rep": False, "volta": 0}

    if v["pend"] is None:
        v["pend"] = new_bar()
        v["volta_now"] = 0
        v["state"] = {}
    bar = v["pend"]
    state = v["state"]
    i, n = 0, len(line)
    keyacc = v["keyacc"]
    while i < n:
        c = line[i]
        if c in " \t.~)uvHT":
            i += 1
        elif c == '"':
            i = line.index('"', i + 1) + 1
        elif c == "!":
            i = line.index("!", i + 1) + 1
        elif c == "{":
            i = line.index("}", i) + 1
        elif c == "[" and i + 2 < n and line[i + 1].isalpha() and line[i + 2] == ":":
            j = line.index("]", i)
            if line[i + 1] == "K":
                words = [w for w in line[i + 3:j].split() if "=" not in w]
                if words:
                    v["keyacc"] = keyacc = key_info(*parse_key(words[0]))
            i = j + 1  # inline field such as [K:clef=bass] or [K:C]
        elif c == "(":
            if i + 2 < n and line[i + 1] == "3" and not line[i + 2].isdigit():
                v["tri"] = 3
                i += 2
            elif i + 1 < n and line[i + 1].isdigit():
                raise ConvertError("only triplets (3 are supported")
            else:
                i += 1
        elif c in "|:" or (c == "[" and i + 1 < n and line[i + 1] in "12"):
            m = _BARLINE.match(line, i)
            tok = m.group(0) if m else ""
            j = m.end() if m else i
            vm = _VOLTA.match(line, j)
            marker = 0
            if vm:
                marker = int(vm.group(1))
                j = vm.end()
            if not tok and not marker:
                i += 1
                continue
            end_rep = tok.startswith(":")
            start_rep = (tok.endswith(":") and "|" in tok) or tok == "::"
            if bar["events"]:
                bar["end_rep"] = end_rep
                bar["volta"] = v["volta_now"]
                v["bars"].append(bar)
                bar = new_bar(start_rep)
            else:
                bar["start_rep"] = bar["start_rep"] or start_rep
            v["pend"] = bar
            state.clear()
            if marker:
                v["volta_now"] = marker
            elif end_rep or start_rep:
                v["volta_now"] = 0
            i = j
        else:
            chord = []
            if c == "[":
                j = line.index("]", i)
                inner, i = line[i + 1:j], j + 1
                k = 0
                while k < len(inner):
                    p, k2 = _read_pitch(inner, k, keyacc, state)
                    if p is None:
                        k += 1
                        continue
                    chord.append(p)
                    k = k2
                    while k < len(inner) and inner[k] in "0123456789/-":
                        k += 1
                rest = False
            elif c in "zZxX":
                i += 1
                rest = True
            else:
                p, i2 = _read_pitch(line, i, keyacc, state)
                if p is None:
                    raise ConvertError("cannot read ABC near %r" % line[i:i + 10])
                chord.append(p)
                i = i2
                rest = False
            j = i
            while j < n and line[j] in "0123456789/":
                j += 1
            ds = line[i:j]
            i = j
            mult = Fraction(1)
            if ds:
                if "/" in ds:
                    a, b = ds.split("/", 1)
                    mult = Fraction(int(a) if a else 1, int(b) if b else 2)
                else:
                    mult = Fraction(int(ds))
            tie = False
            while i < n and line[i] == ")":
                i += 1
            if i < n and line[i] == "-":
                tie = True
                i += 1
            while i < n and line[i] == ")":
                i += 1
            length = mult * unit
            if v.get("tri", 0) > 0:
                length = length * Fraction(2, 3)
                v["tri"] -= 1
            if rest:
                if c == "Z":
                    length = mult * Fraction(num, den)
                bar["events"].append((None, length, False))
            else:
                bar["events"].append((chord, length, tie))
    v["pend"] = bar


def _read_pitch(s, i, keyacc, state):
    acc = None
    n = len(s)
    j = i
    if j < n and s[j] in "^_=":
        k = j
        while k < n and s[k] == s[j]:
            k += 1
        cnt = k - j
        acc = {"^": cnt, "_": -cnt, "=": 0}[s[j]]
        j = k
    if j >= n or s[j].upper() not in LETTERS:
        return None, i
    letter = s[j].upper()
    octv = 4 if s[j].isupper() else 5
    j += 1
    while j < n and s[j] in "',":
        octv += 1 if s[j] == "'" else -1
        j += 1
    key = (letter, octv)
    if acc is None:
        acc = state.get(key, keyacc[letter])
    state[key] = acc
    return 12 * (octv + 1) + STEP[letter] + acc, j


def _unfold(bars):
    out = []
    i = 0
    loop = 0
    second = False
    guard = 0
    while i < len(bars):
        guard += 1
        if guard > 100000:
            raise ConvertError("repeat structure does not terminate")
        b = bars[i]
        if b["volta"] == 1 and second:
            while i < len(bars) and bars[i]["volta"] == 1:
                i += 1
            continue
        if b["start_rep"] and not (second and loop == i):
            loop = i
            second = False
        out.append(b)
        if b["end_rep"]:
            if not second:
                second = True
                i = loop
                continue
            second = False
        i += 1
    return out


def _join_ties(bars):
    notes = []
    pos = Fraction(0)
    open_ties = {}  # pitch -> index in notes
    for b in bars:
        for ps, d, tie in b["events"]:
            if ps is not None:
                new_open = {}
                for p in ps:
                    if p in open_ties:
                        k = open_ties.pop(p)
                        notes[k][1] += d
                    else:
                        notes.append([pos, pos + d, p])
                        k = len(notes) - 1
                    if tie:
                        new_open[p] = k
                open_ties = new_open
            pos += d
    return [(int(s * UNIT), int(e * UNIT), p) for s, e, p in notes]


def check(abc_text, midi, snap=1, tracks=None, out=sys.stdout, merge=False, floor=None):
    """Compare an ABC tune with a MIDI file note by note. A MIDI file may play
    each repeat out or only once, so both readings of the repeat signs are tried.
    Returns 0 when all notes (pitch, start, length) agree, else 1."""
    from collections import Counter
    staves_midi = quantize_tracks(midi, snap=snap, tracks=tracks, merge=merge, floor=floor)
    best = None
    for unfold in (True, False):
        staves_abc, counts, groups = read_abc(abc_text, unfold)
        if len(staves_abc) != len(staves_midi):
            print("staff count differs: ABC has %d, MIDI has %d" % (len(staves_abc), len(staves_midi)), file=out)
            return 1
        bad = 0
        for a, m in zip(staves_abc, staves_midi):
            if sorted(a) != sorted(m):
                bad += 1
        if best is None or bad < best[0]:
            best = (bad, unfold, staves_abc, groups)
        if bad == 0:
            break
    bad, unfold, staves_abc, groups = best
    how = "repeats unfolded" if unfold else "as written, repeats played once"
    problems = 0
    for si, (a, m) in enumerate(zip(staves_abc, staves_midi)):
        a, m = sorted(a), sorted(m)
        label = "staff %d (%s)" % (si + 1, "+".join(groups[si]))
        if a == m:
            print("%s: %d notes match (pitch, start, length; %s)" % (label, len(a), how), file=out)
            continue
        problems += 1
        print("%s: MISMATCH (%s), ABC has %d notes, MIDI has %d" % (label, how, len(a), len(m)), file=out)
        ca, cm = Counter(a), Counter(m)
        for name, lst in (("only in ABC", sorted((ca - cm).elements())), ("only in MIDI", sorted((cm - ca).elements()))):
            for s, e, p in lst[:15]:
                print("  %s: pitch %d start %s length %s" % (name, p, Fraction(s, UNIT), Fraction(e - s, UNIT)), file=out)
            if len(lst) > 15:
                print("  ... %d more" % (len(lst) - 15), file=out)
    return 1 if problems else 0


# ------------------------------------------------------------------------- CLI

def _spell_arg(text):
    out = {}
    if not text:
        return out
    for item in text.split(","):
        pc, name = item.split("=")
        out[int(pc) % 12] = parse_name(name)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Convert a MIDI file to ABC notation (see the module docstring).")
    ap.add_argument("files", nargs="+", help="FILE.mid, or with --check: TUNE.abc FILE.mid")
    ap.add_argument("-o", "--out", help="write the ABC here (default: print)")
    ap.add_argument("--check", action="store_true", help="compare an ABC file with a MIDI file")
    ap.add_argument("--title", default="")
    ap.add_argument("--composer", default="")
    ap.add_argument("--source", default="", help="text for the Source comment")
    ap.add_argument("--comment", action="append", default=[], help="extra comment line (repeatable)")
    ap.add_argument("--key", help="override the key, for example G, Bb, Am, F#m")
    ap.add_argument("--meter", help="override the time signature, for example 3/4")
    ap.add_argument("--L", dest="unit", help="note length, 1/8 or 1/16 (default: chosen from the music)")
    ap.add_argument("--tempo", type=int, help="quarter notes per minute (default: from the MIDI)")
    ap.add_argument("--tempo-unit", default="1/4", help="note value the tempo counts, for example 3/8 in 6/8 (default 1/4)")
    ap.add_argument("--pickup", help="length of the pickup bar as a fraction of a whole note, for example 1/8")
    ap.add_argument("--names", help="voice names, comma separated (default RH,LH)")
    ap.add_argument("--clefs", help="clefs, comma separated (default: chosen from the pitch range)")
    ap.add_argument("--split", default="", help="staff names to split into two voices, comma separated")
    ap.add_argument("--spell", help="pitch class spelling, for example 1=Db,6=Gb")
    ap.add_argument("--marks", help="marks file (slurs, dynamics, text, spelling)")
    ap.add_argument("--repeat", action="append", default=[], help="S:B  bars played twice in a row")
    ap.add_argument("--sign-repeat", action="append", default=[], help="S:B  bars S..S+B-1 get repeat signs (MIDI plays them once)")
    ap.add_argument("--sign-volta", action="append", default=[], help="S:B:E1:E2  repeat signs with endings (MIDI plays them once)")
    ap.add_argument("--volta", action="append", default=[], help="S:B:E1:E2  repeat with first and second endings")
    ap.add_argument("--key-change", action="append", default=[], help="BAR:KEY  change key at this MIDI bar, for example 31:C")
    ap.add_argument("--guitar", action="store_true", help="guitar score: clef=treble-8, notes written an octave above the sound")
    ap.add_argument("--options", default="", help="text for the first-line %%opts directive, for example 'tab=guitar sound=nylon'")
    ap.add_argument("--voice-assign", choices=["low", "near"], default="low", help="how a lone note picks its voice in a split staff: lowest free voice (default) or nearest in pitch (good for melody over bass)")
    ap.add_argument("--max-voices", type=int, default=3, help="most voices to split one staff into (default 3)")
    ap.add_argument("--floor", type=int, help="lowest MIDI note allowed; lower notes are raised an octave (guitar: 40 is the low E string)")
    ap.add_argument("--merge-tracks", action="store_true", help="put all note tracks on one staff")
    ap.add_argument("--bars-per-line", type=int, default=4)
    ap.add_argument("--snap", type=int, default=1, help="snap times to this many grid units (1/96 whole note each)")
    ap.add_argument("--tracks", help="MIDI track numbers to use, comma separated (default: all with notes)")
    args = ap.parse_args(argv)
    try:
        tracks = [int(x) for x in args.tracks.split(",")] if args.tracks else None
        if args.check:
            if len(args.files) != 2:
                ap.error("--check needs TUNE.abc and FILE.mid")
            with open(args.files[0], encoding="utf-8") as f:
                abc = f.read()
            with open(args.files[1], "rb") as f:
                midi = MidiFile(f.read())
            return check(abc, midi, snap=args.snap, tracks=tracks, merge=args.merge_tracks, floor=args.floor)
        with open(args.files[0], "rb") as f:
            midi = MidiFile(f.read())
        meter = tuple(int(x) for x in args.meter.split("/")) if args.meter else None
        piece = convert(
            midi, title=args.title, composer=args.composer, source=args.source, key=args.key,
            meter=meter, unit_l=args.unit, tempo=args.tempo, tempo_unit=args.tempo_unit, pickup=args.pickup,
            names=args.names.split(",") if args.names else None,
            clefs=args.clefs.split(",") if args.clefs else None,
            split=[x for x in args.split.split(",") if x], spell=_spell_arg(args.spell),
            marks_path=args.marks,
            repeats=[tuple(int(x) for x in r.split(":")) for r in args.repeat],
            voltas=[tuple(int(x) for x in r.split(":")) for r in args.volta],
            guitar=args.guitar, options=args.options, voice_assign=args.voice_assign, max_voices=args.max_voices, floor=args.floor, merge_tracks=args.merge_tracks,
            key_changes=[(int(r.split(":")[0]), r.split(":")[1]) for r in args.key_change],
            sign_repeats=[tuple(int(x) for x in r.split(":")) for r in args.sign_repeat],
            sign_voltas=[tuple(int(x) for x in r.split(":")) for r in args.sign_volta],
            bars_per_line=args.bars_per_line, snap=args.snap, tracks=tracks, comments=args.comment)
    except (ConvertError, OSError, ValueError) as e:
        print("midi2abc: %s" % e, file=sys.stderr)
        return 2
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(piece.text)
        print("wrote %s (%d bars, K:%s, M:%s)" % (args.out, piece.nbars, piece.key, piece.meter), file=sys.stderr)
    else:
        sys.stdout.write(piece.text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
