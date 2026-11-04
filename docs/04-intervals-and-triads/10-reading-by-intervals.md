# Reading by intervals

<span class="tag tag-reading">Reading</span>

After this lesson you can find any note on the staff from the nearest of five landmark notes, read a melody as a series of steps, skips, leaps and repeated notes, and play short melodies from the page without naming every note.

Before this: [Interval numbers](01-interval-numbers.md), [The treble staff and C position](../01-first-sounds/09-treble-staff-and-c-position.md), [The bass clef and the grand staff](../02-two-hands-and-first-chords/01-bass-clef-and-grand-staff.md), [Sight-reading basics](../02-two-hands-and-first-chords/09-sight-reading-basics.md). You need: your piano.

## The idea

### Why not name every note

Naming each note works, but it is slow. A fluent reader does not say "E, G, F, A". They see "up a skip, down a step, up a skip" and let the hand follow the shape. Reading by intervals uses two ideas. First, you anchor yourself on a few notes you know on sight. Second, you read each move from one note to the next as a distance and a direction.

### The five landmark notes

A **landmark note** is a note you recognise on sight, so you can count a short way from it to the notes around it. These five are enough for the staves you read now.

| Landmark | Note | Where it sits |
|---|---|---|
| Middle C | C4 | On a ledger line below the treble staff, and above the bass staff |
| Treble G | G4 | Line 2 of the treble staff, where the clef curls |
| High C | C5 | Space 3 of the treble staff |
| Bass F | F3 | Line 4 of the bass staff, between the two dots of the clef |
| Low C | C3 | Space 2 of the bass staff |

Here they are on the staves. The first bar is treble: C4, G4, C5. The second bar is bass: F3, C3, C4.

```abc
%%opts play=off
X:1
M:3/4
L:1/4
K:C clef=treble
C G c |]
```

```abc
%%opts play=off
X:1
M:3/4
L:1/4
K:C clef=bass
F, C, C |]
```

To find another note, start at the nearest landmark and count lines and spaces. The line above treble G is B4, and A4 sits in the space between them. Landmarks also help you check an interval: treble G to high C is a 4th.

### Steps, skips and leaps

You met steps and skips in lesson 1. A move bigger than a skip is a **leap**. Together with a repeated note, these give four kinds of move.

| Move | Size | On the staff |
|---|---|---|
| Repeat | Same note | The same line or space |
| Step | 2nd | A line to the next space, or the reverse |
| Skip | 3rd | Line to line, or space to space |
| Leap | 4th or larger | Three or more lines and spaces away |

On the piano, a step on the staff is the next white key, a skip is the white key after that, and a leap is a bigger jump. In a five-finger position, a step is the next finger, a skip is two fingers over, and a leap needs the hand to move.

### Reading a melody in four steps

1. Find the first note from the nearest landmark, and place your hand.
2. Read each move after it as repeat, step, skip or leap, and its direction (up or down).
3. Let the hand follow the shape. Your eyes read the move, not the note name.
4. Look one bar ahead. Spot the next leap before you reach it.

Practise with a melody made of steps. Say the moves as you play: "start on E, step up, step up, step down, step down."

```abc
X:1
M:4/4
L:1/4
Q:1/4=60
K:C
!3!E !4!F !5!G !4!F | !3!E !2!D !1!C2 |]
```

Now a melody of skips. Say "start on C, skip up, skip up, skip down" and so on.

```abc
X:1
M:4/4
L:1/4
Q:1/4=60
K:C
C E G E | D F A F |]
```

Next, a melody with every kind of move. The first note is G4, treble G. After it come a repeat, a leap up, three steps down, a skip down, a skip up, a leap down and four steps up.

```abc
X:1
M:4/4
L:1/4
Q:1/4=60
K:C
G G c B | A G E G | C D E F | G4 |]
```

Two leaps move the hand: G up to C, and later G down to C. Read ahead so the hand is ready. After the leap down, the hand is back in C position.

## Try it

Exercise 1. Name the three landmark notes in the line below.

```abc
%%opts play=off
X:1
M:3/4
L:1/4
K:C clef=treble
C G c |]
```

<details class="solution" markdown>
<summary>Answer</summary>

C4 (middle C, on the ledger line), G4 (treble G, line 2) and C5 (high C, space 3).

</details>

Exercise 2. Label each move of this melody as repeat, step, skip or leap, and say whether it goes up or down.

```abc
X:1
M:4/4
L:1/4
K:C
E E G F | E C D E |]
```

<details class="solution" markdown>
<summary>Answer</summary>

E to E: repeat. E to G: skip up. G to F: step down. F to E: step down. E to C: skip down. C to D: step up. D to E: step up.

</details>

Exercise 3. You are on treble G (G4). The next note is a skip down. Which note is it? What about a leap up of a 5th?

<details class="solution" markdown>
<summary>Answer</summary>

A skip down from G4 is E4. A leap up of a 5th from G4 is D5 (G, A, B, C, D).

</details>

<div class="practice" markdown>

### Practice routine (30 minutes)

| Minutes | What to do | Tempo | Listen for |
|---|---|---|---|
| 5 | Warm-up: five-finger pattern C D E F G and back, each hand alone | 60 bpm | The same volume on every finger |
| 15 | New skill: for each of the four melodies, say the first note and the moves aloud, then play; start with eyes on the page only | 50 bpm, then 60 | Playing the shape, not hunting for letters |
| 5 | Reading: the [reading drill](../practice/reading-drill.md); find each note from the nearest landmark | Untimed | Counting one or two steps, not from the bottom line |
| 5 | Guitar: D D U U D U on Em and Am, four bars each | 60 bpm | The hand never stopping |

Repeat this routine on at least three days.

</div>

<div class="move-on" markdown>

### Move on when

- [ ] You can name all five landmark notes on the staff in under 10 seconds.
- [ ] You can name 10 random notes from the [note flashcards](../practice/note-flashcards.md) in under 30 seconds by counting from a landmark.
- [ ] You can label every move of a new four-bar melody as repeat, step, skip or leap.
- [ ] You can play the mixed melody above at 60 bpm, three times in a row, looking only at the page.

</div>

## Common mistakes

Counting up from the bottom line each time. Count from the nearest landmark, and from the note before it when the move is a step or a skip.

Reading the names but ignoring the direction. If the notes go up the page, the hand goes up the keyboard. Check the direction before you check the letter.

Looking down at the hands. Keep your eyes on the page. If you must look, glance at the keys and return at once to the same bar.

## Key terms

- **Landmark note**: a note you can recognise on sight and use to find the notes around it.
- **Repeat**: the same note played again.
- **Leap**: a melodic move of a 4th or larger.

Next: [Easy classical pieces: a musette and a minuet](11-easy-classical-pieces.md)
