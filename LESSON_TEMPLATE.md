# Lesson template

Every lesson follows this layout, in this order. A lesson is short: 10 to 15 minutes of reading (about 700 to 1200 words of prose, never more than 1500), then a 30-minute practice routine the reader repeats on several days until the "Move on when" boxes are ticked. Music blocks, figures and tables don't count toward the word budget.

`STYLE.md` has the writing rules and the music conventions (note names, finger numbers, string numbers). `DESIGN.md` shows how each box looks.

## The layout

```markdown
# Title of the lesson

<span class="tag tag-piano">Piano</span>

After this lesson you can <one sentence: what the reader can play, read or hear>.

Before this: [Lesson name](../01-first-sounds/04-pitch-and-the-musical-alphabet.md), [Lesson name](...). You need: your piano.

## The idea

2 to 4 short sections (### headings) that build the idea: sound first, then the
picture, then the name, then the formal definition. Each new term is **bold**
where it is defined.

## Hear and see

Music examples (abc blocks with a play bar) and figures, each with a sentence
before it saying what to listen or look for. Some lessons fold this into "The idea";
then leave this heading out.

## Try it

2 or 3 small exercises (naming notes, counting a rhythm, spotting a chord), each
with its answer in a closed box.

## Practice routine

The 30-minute routine box.

## Move on when

The checklist box.

## Common mistakes

At most 3, each one short: what goes wrong, why, and the fix.

## Film yourself

Only in lessons that teach a physical technique (posture, hand shape, strumming,
pedalling). A checklist of what to look for in the video, and at most one free
video from the list in docs/reference/videos.md.

## Key terms

- **Term**: one-line definition.

Next: [Next lesson title](10-first-melodies-on-piano.md)
```

## The tag line

Right under the title, one span for the lesson's area, plus `tag-optional` or `tag-stretch` when the lesson has that flag in `tools/lessons.yml`:

| Area | Markup |
|---|---|
| Piano | `<span class="tag tag-piano">Piano</span>` |
| Guitar | `<span class="tag tag-guitar">Guitar</span>` |
| Theory | `<span class="tag tag-theory">Theory</span>` |
| Reading | `<span class="tag tag-reading">Reading</span>` |
| Ear | `<span class="tag tag-ear">Ear</span>` |
| Improvising | `<span class="tag tag-improvise">Improvising</span>` |
| Other | `<span class="tag tag-other">Practice</span>` |
| Optional | `<span class="tag tag-optional">Optional</span>` |
| Stretch | `<span class="tag tag-stretch">Stretch piece</span>` |

## "Before this" and "You need"

- "Before this:" links the earlier lessons this one uses. A lesson may only depend on lessons before it in `tools/lessons.yml`. Never use a term or skill that a later lesson teaches. If you need it, explain it in one sentence here and say which later lesson covers it.
- "You need:" names the instrument (your piano, your guitar, both, or nothing), plus anything else: a tuner app, a metronome app, a pencil.

## Music blocks

Write music in ABC inside an `abc` fence. On the site it is drawn as sheet music with a play bar (play, loop, restart, a progress bar and a tempo slider), and the notes light up as they play. In VS Code you see the ABC text.

````markdown
```abc
X:1
M:4/4
L:1/4
Q:1/4=80
K:C
C D E F | G2 G2 | A A G2 | F E D C |]
```
````

| Need | How |
|---|---|
| Header lines | `X:1`, `M:` (time signature), `L:` (default note length), `K:` (key) are required. `Q:1/4=80` sets the playback tempo. Leave out `T:` in examples; pieces have `T:` and `C:`. |
| Note lengths | With `L:1/4`, `C` is a quarter note, `C2` a half note, `C4` a whole note, `C/` an eighth note, `C3/` a dotted quarter. With `L:1/8`, `C` is an eighth note and `C2` a quarter. |
| Octaves | `C` is middle C (C4), `c` is C5, `c'` is C6, `C,` is C3, `C,,` is C2. |
| Sharps and flats | `^F` is F#, `_B` is Bb, `=F` is F natural. The key signature in `K:` applies to the whole piece (`K:G` gives F#). |
| Rests | `z` (with a length: `z2`, `z4`). |
| Ties, slurs | `C2-C2` ties; `(CDE)` is a slur. |
| Triplets | `(3CDE`. |
| Chords | `[CEG]` sounds C, E and G together. Chord symbols go in quotes before a note: `"Am"A2`. |
| Fingering | `!1!C !2!D !3!E` puts finger numbers above the notes. |
| Dynamics and marks | `!p!`, `!mf!`, `!f!`, `!crescendo(!` ... `!crescendo)!`, `.C` (staccato), `!fermata!C`. |
| Repeats | `|:` ... `:|`, first and second endings `|1` ... `:|2` ... `|]`. |
| End | Finish with `|]`. |
| Line length | About 4 bars per line, so the music fits a phone. |

Both hands on piano use two voices on a grand staff:

````markdown
```abc
X:1
M:4/4
L:1/4
K:C
%%score {RH LH}
V:RH clef=treble
V:LH clef=bass
[V:RH] E D C2 | E D C2 |]
[V:LH] C,4 | G,,2 C,2 |]
```
````

Guitar music is written an octave above the sound, as in printed guitar music, with `clef=treble-8`. Add `%%opts tab=guitar` as the first line for tab under the staff. Playback uses a steel-string guitar sound by default.

````markdown
```abc
%%opts tab=guitar
X:1
M:4/4
L:1/4
K:Em clef=treble-8
E, B, E G | B e g2 |]
```
````

Other options on the `%%opts` line: `sound=piano`, `sound=steel` or `sound=nylon` (the playback instrument), `play=off` (no play bar, for a picture of notation), `chords=on` (also play the chord symbols), `capo=2` (tab with a capo).

Run `node tools/check_abc.mjs <file>` after writing. It checks that every block parses, that every bar has the right number of beats (only a pickup bar and the last bar may be short), and that tab notes are playable. `--dump` prints the notes of each block as MIDI numbers (middle C = 60), which helps when you check a melody against its source.

## Figures

Keyboards, chord diagrams and fretboard maps are SVG files drawn by Python. Each lesson that needs them has a script `tools/figures/<stage-folder>/<lesson-slug>.py` that imports the helpers in `tools/figures/musicfigs.py` and writes `docs/assets/figures/<stage-folder>/<lesson-slug>-<name>.svg`. Embed with a relative link and alt text that says what the figure shows:

```markdown
![Keyboard from C4 to C5 with fingers 1 to 5 of the right hand on C, D, E, F and G](../assets/figures/01-first-sounds/treble-staff-and-c-position-c-position.svg)
```

## The practice routine

Each routine fills 30 minutes, and the minutes in the table must add up to 30. The usual shape is a 5-minute warm-up, 15 minutes on the new skill, 5 minutes of sight reading or ear training, and 5 minutes on the other instrument (from earlier lessons), so both instruments get played every day. Every row has a tempo or a count and one thing to listen or watch for.

```markdown
<div class="practice" markdown>

### Practice routine (30 minutes)

| Minutes | What to do | Tempo | Listen for |
|---|---|---|---|
| 5 | Warm-up: five-finger pattern C D E F G and back, each hand alone | 60 bpm | The same volume on every finger |
| 15 | New skill: the melody in Example 2, hands separately, then together | 50 bpm, then 60 | No stops at the bar lines |
| 5 | Sight reading: the first line of the reading drill | 50 bpm | Keep going after a wrong note |
| 5 | Guitar: Em chord, four strums per bar | 60 bpm | Every string rings |

Repeat this routine on at least three days before you check the boxes below.

</div>
```

## The "Move on when" checklist

3 to 5 boxes, each one something the reader can test: a tempo, a count, a recording, naming notes against a timer.

```markdown
<div class="move-on" markdown>

### Move on when

- [ ] You can play the melody in Example 2 hands together at 60 bpm, three times in a row with no stops.
- [ ] You can name all eight notes from C4 to C5 on the staff in under 10 seconds (use the [note flashcards](../practice/note-flashcards.md)).

</div>
```

## Answers

Every exercise in "Try it" has its answer in a closed box right after it:

```markdown
<details class="solution" markdown>
<summary>Answer</summary>

E, G, B, D, F.

</details>
```

## Lesson types

The layout above fits every lesson. A few types add something:

- Piece lessons (a classical piece or an original piece): the whole piece as an `abc` block, the source edition and licence for public-domain pieces, a plan that splits the piece into sections of 2 to 4 bars, and the order to learn them in.
- Ear lessons: examples to listen to with the play bar, a self-test with answers in boxes, and a link to the ear quizzes in Practice tools.
- Improvising lessons: a backing pattern to loop (an `abc` block the reader loops with the play bar), the notes allowed, and three rules for the first improvisation.
- Theory lessons: "You need" may say "nothing", but the routine still uses an instrument to play what was learned.
