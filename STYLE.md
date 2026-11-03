# Writing style

These rules apply to every page in `docs/`. The reader is a capable adult (a 4th-year university CS student in Ontario) who is a complete beginner at music. They own an 88-key digital piano with three pedals and a right-handed acoustic steel-string guitar, practise about 30 minutes a day, and like classical music and film, game and anime music. Assume no music terms at all: every word such as "staff", "bar", "chord" or "fret" is explained the first time it appears. Don't talk down to them.

The goal of each page is that the reader can play, read or hear something new by the end of it, and knows why it works.

## Voice

- Talk to the reader as "you" in instructions ("Put your thumb on middle C"). Use "we" when working through something together ("We want the left hand quieter").
- Explanations are plain and direct. Definitions use the standard wording a music teacher, the RCM theory books or a university course would use, so the reader can follow other books and teachers later.
- Active voice, present tense, plain verbs.
- Be modest. Don't praise pieces, composers, gear or methods. Say what you hear and what to do.
- Use Canadian spelling: colour, centre, practise (the verb) and practice (the noun), so "a practice routine" but "practise the scale". Keep the original spelling in names and titles.

## How to explain

1. Sound first, then sight, then the name. Let the reader hear the example (an `abc` block with a play bar), then see it on the staff or the fretboard, then learn the term, then the formal definition.
2. The first time a term or symbol appears, say what it means in words, and bold the term.
3. Start from what the reader already knows (from earlier lessons, or from everyday life), and say where an analogy stops working.
4. Give a physical skill as numbered steps (where each finger goes, what moves, what stays still), then refer to the step numbers.
5. Every exercise has a tempo in beats per minute (bpm) and a target you can check: "three times in a row with no stops at 60 bpm".
6. Name a common mistake at the step where it happens, not only in a separate list.
7. Never write "clearly", "obviously", "it is easy", "simply", "just" (as in "just play") or "trivially". Show the step instead.
8. Keep one idea per paragraph, in 2 to 5 sentences.
9. Aim for about 20 words per sentence on average, never more than about 40, and vary the length. A page of identical short sentences reads like a machine wrote it.
10. Put labels next to what they label: finger numbers on the keys, fret numbers on the diagram, not "see the figure above".
11. Leave out decoration. No fun facts or history asides that don't teach the skill. The eras lesson in stage 10 is where history goes.
12. One term per concept. If the book says "bar", it doesn't also say "measure", except once when introducing the term ("a bar, also called a measure").
13. Say what to listen for. Every routine names one thing to listen or watch for ("even volume between the thumb and finger 3").
14. Pain is a stop sign. Technique lessons say to stop if a hand, wrist, arm or back hurts, and to see a teacher or a doctor if it keeps happening.

## Music conventions

These keep the whole book consistent.

| Thing | Convention |
|---|---|
| Note names | Letters A to G. Sharps and flats are written with `#` and `b`, the way chord charts do: F#, Bb, C#m, Eb major. The first time, also write the word: "F sharp (F#)". Don't use the sharp and flat characters from Unicode; the site font doesn't have them. |
| Octaves | Scientific pitch notation. Middle C is C4, the A above it is A4 (440 Hz), the lowest piano key is A0. |
| Piano fingers | 1 to 5 in both hands: thumb = 1, little finger = 5. RH and LH mean right hand and left hand. |
| Guitar strings | 1 (the thinnest, high E) to 6 (the thickest, low E). |
| Guitar fingers | Fretting hand 1 (index) to 4 (little), thumb T. Picking hand p, i, m, a (thumb, index, middle, ring), the standard classical letters. |
| Frets | Counted from the nut. Fret 0 is the open string. |
| Chord symbols | C, Cm, C7, Cmaj7, Cm7, Cdim, Csus2, Csus4, Cadd9, and slash chords such as C/E (C with E in the bass). |
| Roman numerals | Upper case for major (I, IV, V), lower case for minor (ii, iii, vi), ° for diminished (vii°), a 7 for seventh chords (V7). |
| Scale degrees | Numbers 1 to 7, with b and # for altered degrees (b3, #4). Not solfege. |
| Counting | "1 & 2 &" for eighth notes, "1 e & a" for sixteenths, "1 trip let" for triplets. Tempo in bpm. |
| Time signatures | Written 4/4, 3/4 and 6/8 in prose. |

## Notation in ABC

Music examples are fenced `abc` blocks. On the site they are drawn as sheet music with a play bar (see `docs/javascripts/music.js`); in VS Code they show as text. `LESSON_TEMPLATE.md` has the full conventions. The main rules:

- Every block has `X:1`, `M:`, `L:` and `K:` lines. Leave out `T:` in examples, because the heading above already names the example. Full pieces have `T:` and `C:` (composer).
- Guitar music uses `K:<key> clef=treble-8` and is written the way guitar music is printed (an octave above the sound). Add `%%opts tab=guitar` as the first line to show tab under the staff.
- Piano music for both hands uses two voices, `V:1 clef=treble` and `V:2 clef=bass`, joined with `%%score {1 2}`.
- Put about 4 bars on a line, so the music fits a phone screen.
- Fingerings go above notes as `!1!` to `!5!`. Dynamics are `!p!`, `!mf!`, `!f!` and so on.
- Every block must pass `node tools/check_abc.mjs`: it parses, and every bar has the right number of beats.

## Copyright

- Pieces printed in the book are either public domain in both Canada and the US (the composer died long ago and the work was first published before 1931), engraved by the book from an original edition, or written for the book.
- Never write out a melody, riff, tab or lyric from a copyrighted song, film, game or anime score, even a few bars. A chord progression on its own is fine to name ("the royal road, IV V iii vi").
- Real copyrighted pieces appear by title only, in the "play next" list, with the publisher of a licensed arrangement.
- Each public-domain piece names its source edition and licence in the lesson and on the credits page.

## Facts that change

Prices, gear models, app names and app features change. Each lesson that uses one:

- takes it from the official site at writing time (never from memory),
- states the year ("as of 2026"),
- links the source at the point of use.

If a number or a product is not needed to learn the skill, leave it out.

## Markdown that works on the site and in VS Code

The same files are read in VS Code's preview and built into the website (Zensical with abcjs). These rules keep both working.

### Boxes

Use HTML containers with the `markdown` attribute. Leave a blank line after the opening tag and a blank line before the closing tag, or the content inside won't be processed. `DESIGN.md` shows how each one looks.

```html
<div class="example" markdown>

### Example 1: counting a bar of eighth notes

...

</div>

<div class="note" markdown>

...

</div>

<div class="warning" markdown>

...

</div>

<div class="practice" markdown>

### Practice routine (30 minutes)

| Minutes | What to do | Tempo | Listen for |
|---|---|---|---|
| 5 | ... | ... | ... |

</div>

<div class="move-on" markdown>

### Move on when

- [ ] ...

</div>

<div class="film" markdown>

### Film yourself

...

</div>
```

Collapsible answer:

```html
<details class="solution" markdown>
<summary>Answer</summary>

...

</details>
```

Don't use `!!!`, `???` or `===` blocks. They need indented content, which VS Code shows as a raw code block.

### Links, headings and figures

- Link between pages with relative paths to the `.md` file: `[the treble staff](../01-first-sounds/09-treble-staff-and-c-position.md)`.
- Keep punctuation out of headings that other pages link to, so the anchor stays stable.
- Figures (keyboards, chord diagrams, fretboards) are SVG files drawn by the scripts in `tools/figures/`. Alt text says what the figure shows: `![Keyboard with C, E and G marked with fingers 1, 3 and 5](...)`.
- Code blocks are rare in this book. When one appears, it names its language.

## Patterns to avoid

These are signs of AI-generated text, collected from Wikipedia's "Signs of AI writing" page (including its 2026 updates) and from studies of words that language models overuse (Kobak et al. 2024; Juzek and Ward 2025; Liang et al. 2024). One or two of them can appear by chance in human writing; the problem is when they pile up. Treat them as hard rules here anyway, because the whole book is drafted with AI help and would otherwise drift toward them.

### Words: never use

delve, tapestry, testament, pivotal, underscore (as a verb), intricate, intricacies, meticulous, meticulously, showcase, garner, bolster, interplay, vibrant, multifaceted, realm, groundbreaking, renowned, nestled, seamless, seamlessly, commendable, noteworthy, invaluable, transformative, unparalleled, unveil, harness (as a verb), elucidate, burgeoning, foster, leverage (in any sense), quietly, deep dive, boasts, journey, unlock, elevate, master (as a verb), "key role", "key factor", "key takeaway", "key insight", "key concept".

Music senses are allowed: "key" as in "the key of G" and "a key on the piano", "the key signature", "master volume" on a keyboard's settings.

### Words: use rarely

crucial, vital, essential, comprehensive, notably, additionally, moreover, furthermore, consequently, ultimately, enhance, valuable, insights, practical, remarkable, nuanced, significant, robust, powerful, modern, rich, lush, best practice (name the practice and the reason instead). Prefer a plain word: "needed", "also", "so", "big".

### Phrases and patterns: never use

- "serves as", "stands as", "functions as" where "is" works. Write "The tonic is the home note", not "The tonic serves as...".
- Inflated importance: "plays a crucial role", "is a testament to", "is a cornerstone of", "sets the stage for", "marks a shift".
- A trailing "-ing" clause that adds vague commentary: "..., highlighting the importance of rhythm", "..., underscoring...", "..., showcasing...".
- Disclaimers: "It's important to note that", "It's worth noting", "It is worth mentioning". State the warning directly instead: "Watch out: ...".
- Summary endings: a closing paragraph starting "In summary", "In conclusion", "To sum up" or "Overall,". Lessons end with the key terms and the link to the next lesson, not a recap.
- Chatbot lines: "Great question", "Certainly!", "Let's dive in", "Let's unpack this", "I hope this helps", "Let me know". Plain "Let's play it slowly" is fine.
- Vague attribution: "teachers agree", "experts say", "it is widely believed". Name the source or drop the claim.
- Negative parallelism: "not only X but also Y", "it's not X, it's Y", "no X, no Y, just Z". The one exception is correcting a specific mistake: "count the rest, don't skip it".
- False ranges: "from X to Y" where X and Y are not two ends of one scale ("from Bach to anime"). Real ranges are fine: "from middle C to the C above", "from 60 to 80 bpm".
- Groups of three used for rhythm ("bright, warm and full"). A real list of three things is fine.
- Hedging about sources: "while details are limited", "based on available information".
- Hype about gear, apps or methods: "revolutionize", "game-changing", "supercharge", "magic", "secret", "hack". Say what the thing does and what it can't do.
- Praise of music or composers: "timeless", "beloved", "iconic", "masterpiece", "breathtaking", "hauntingly beautiful". Describe what you hear instead: "the left hand repeats one chord while the melody climbs".

### Punctuation and characters

- Em dashes (—) almost never: at most one per 500 words, and never with spaces around them. Studies cited on Wikipedia found Claude uses em dashes more than professional writers do, so this takes active effort. Use a comma, a colon, parentheses or a new sentence instead.
- En dashes (–) only in numeric ranges ("bars 9–16"), or write "9 to 16".
- Straight quotes and apostrophes only (`"` and `'`).
- No emoji, and no unicode bullets (•). Use Markdown `-` lists.
- Few exclamation marks in prose. (Inside an `abc` block, `!` marks decorations and is fine.)

### Formatting

- Headings are in sentence case: "How to read a chord chart", not "How To Read A Chord Chart". Note and chord names keep their capitals (C, F#, Am, Cmaj7, the C major scale), and so do proper nouns: composer names, Roman numerals (I, IV, V7, vii°), mode names (Ionian, Dorian, Phrygian, Lydian, Mixolydian, Aeolian, Locrian), CAGED, Travis picking, Alberti bass, the Picardy third, RCM, MIDI, ABC, VS Code, Anki, YouTube, JustinGuitar. Add a name here when a lesson needs one, instead of lowercasing it.
- A term is bold once, where it is defined, and nowhere else. Don't use bold for emphasis.
- Don't write bullet lists where every item starts with a bold label and a colon. Use a sentence, a table or a real subheading.
- Each page has one H1 (the title). Don't skip heading levels (H2 straight to H4).
- Don't put `---` lines between sections.
- Use a list for real steps or real collections of items. If prose reads fine, use prose.
- Use tables for real tables of values (practice routines, key signatures, chord spellings, finger charts). A two-row table that should be a sentence should be a sentence.

### Don't over-correct

Wikipedia now also flags the opposite extreme: text that never uses a dash or a semicolon, uses only commas and periods, and keeps every sentence between 8 and 20 words. Write like a teacher sitting next to the piano: plain "is" and "has" sentences, a colon or semicolon or parentheses where they fit, an occasional "usually" or "often", and sentences of different lengths.

## Self-check before a page is committed

1. Search the file for `—`, `–` (outside numeric ranges), `“`, `”`, `‘`, `’`, the Unicode sharp and flat signs, emoji, and every word in "never use".
2. Search for "serves as", "stands as", "important to note", "worth noting", "In summary", "In conclusion", "Overall,", "not only", "Let's dive", "simply", "just play", "masterpiece", "timeless".
3. Check headings for Title Case (outside the allowlist) and lists for bold "Label:" items.
4. Run `node tools/check_abc.mjs` and `.venv/Scripts/python tools/check_theory.py`.
5. Recompute every answer and table value (chord spellings, intervals, key signatures, bar counts, minutes adding up to 30). Python is fine.
6. Check that each changing fact has a source link and "as of 2026", and that no copyrighted melody, tab or lyric appears.
7. Read the page once from top to bottom for rhythm. If several sentences in a row have the same length and shape, rewrite some of them.
