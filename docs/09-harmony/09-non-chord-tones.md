# Non-chord tones

<span class="tag tag-theory">Theory</span>

After this lesson you can find the notes of a melody that are not in the chord, and name them as a passing tone, neighbour tone, suspension, appoggiatura, anticipation or escape tone.

Before this: [The chords of a key](02-diatonic-chords.md), [Cadences](03-cadences.md), [Interval numbers](../04-intervals-and-triads/01-interval-numbers.md). You need: your piano and your guitar.

## The idea

### Chord tones and the others

A melody over a chord does not use only the notes of that chord. Play the C chord (C, E, G) in the left hand and play C, E, G, E, C in the right hand. It sounds like an exercise, because every note is in the chord. Now play E, D, C instead of E, C, hearing the D in between. The tune moves.

A note that belongs to the chord is a **chord tone**. A note that does not is a **non-chord tone**. Non-chord tones are not mistakes. They add motion and a small tension, and they are named by how they arrive and where they go. Two things decide the name: whether the note is approached by step or by leap, and whether it resolves (moves on to a chord tone) by step or by leap. A step is to the next note of the scale and a leap is bigger.

In the examples below, the left hand holds the chord and a label marks the non-chord tone in the right hand.

### Passing tone

A **passing tone** moves by step between two chord tones that are a 3rd apart, filling the gap. In C major, E and C are chord tones of the C chord, and the D between them is the passing tone. The melody moves in one direction through it.

```abc
X:1
M:4/4
L:1/4
Q:1/4=60
K:C
%%score {RH LH}
V:RH clef=treble
V:LH clef=bass
[V:RH] "C"E "^passing tone"D C2 |]
[V:LH] [C,E,G,]4 |]
```

### Neighbour tone

A **neighbour tone** steps away from a chord tone and comes back to the same note. It can be above (an upper neighbour) or below (a lower neighbour). In the example, F is the upper neighbour of E.

```abc
X:1
M:4/4
L:1/4
Q:1/4=60
K:C
%%score {RH LH}
V:RH clef=treble
V:LH clef=bass
[V:RH] "C"E "^neighbour tone"F E2 |]
[V:LH] [C,E,G,]4 |]
```

### Suspension

A **suspension** holds a note of the old chord into the new chord, where it clashes. The held note is tied over the bar line. It then falls by step to a chord tone of the new chord. In the example, F is a chord tone of the F chord, and it is tied into the C chord. It clashes with the C chord, and falls to E, which belongs to it.

```abc
X:1
M:4/4
L:1/4
Q:1/4=60
K:C
%%score {RH LH}
V:RH clef=treble
V:LH clef=bass
[V:RH] "F"A A F2- | "C"F "^resolves"E E2 |]
[V:LH] [F,,A,,C,]4 | [C,E,G,]4 |]
```

Listen to bar 2. At the start of the bar the F is held against the new chord and sounds tense. The tension ends when the F falls to E.

### Appoggiatura

An **appoggiatura** (say "ah-pod-jah-TOO-rah") is a non-chord tone on a strong beat, approached by a leap, and resolved by step, usually in the opposite direction. In the example, the melody leaps up from E to A on beat 3, and A steps down to G, which belongs to the C chord.

```abc
X:1
M:4/4
L:1/4
Q:1/4=60
K:C
%%score {RH LH}
V:RH clef=treble
V:LH clef=bass
[V:RH] "C"C E "^appoggiatura"A G |]
[V:LH] [C,E,G,]4 |]
```

### Anticipation

An **anticipation** arrives early. A note of the next chord sounds shortly before the chord changes, on a weak part of the beat. In the example, the last eighth note of bar 1 is C, which belongs to the C chord in bar 2, while the left hand still plays G.

```abc
X:1
M:4/4
L:1/8
Q:1/4=60
K:C
%%score {RH LH}
V:RH clef=treble
V:LH clef=bass
[V:RH] "G"B2 d2 G2 B"^anticipation"c | "C"c8 |]
[V:LH] [G,,B,,D,]8 | [C,E,G,]8 |]
```

### Escape tone

An **escape tone** (also called an echappee, "ay-shah-PAY") is approached by step and left by a leap in the opposite direction. In the example, G steps up to A, and A leaps down to E.

```abc
X:1
M:4/4
L:1/4
Q:1/4=60
K:C
%%score {RH LH}
V:RH clef=treble
V:LH clef=bass
[V:RH] "C"G "^escape tone"A E2 |]
[V:LH] [C,E,G,]4 |]
```

### A summary table

| Name | Approached | Left | Where |
|---|---|---|---|
| Passing tone | step | step, same direction | usually a weak beat |
| Neighbour tone | step | step, back to the same note | usually a weak beat |
| Suspension | held from the old chord (tie) | step down | strong beat |
| Appoggiatura | leap | step, opposite direction | strong beat |
| Anticipation | step or leap, early | the same note stays | weak part, before a chord change |
| Escape tone | step | leap, opposite direction | weak beat |

## Try it

Exercise 1. Find and name the non-chord tone in each bar. Check the chord symbols for the chord notes.

```abc
X:1
M:4/4
L:1/4
Q:1/4=60
K:C
%%score {RH LH}
V:RH clef=treble
V:LH clef=bass
[V:RH] "C"E D C E | "G"D C B G | "F"A G A F | "C"E G c2 |]
[V:LH] [C,E,G,]4 | [G,,B,,D,]4 | [F,,A,,C,]4 | [C,E,G,]4 |]
```

<details class="solution" markdown>
<summary>Answer</summary>

Bar 1: D is a passing tone (C chord is C, E, G). Bar 2: C is a passing tone between D and B (G chord is G, B, D). Bar 3: G is a lower neighbour tone between two As (F chord is F, A, C). Bar 4: no non-chord tones.

</details>

Exercise 2. A note not in the chord arrives by a step up and leaves by a leap down. What is it?

<details class="solution" markdown>
<summary>Answer</summary>

An escape tone.

</details>

Exercise 3. In bar 1 of the anticipation example, which chord does the last note belong to, and which chord is playing?

<details class="solution" markdown>
<summary>Answer</summary>

C belongs to the C chord of bar 2. The G chord is still playing in bar 1.

</details>

<div class="practice" markdown>

### Practice routine (30 minutes)

| Minutes | What to do | Tempo | Listen for |
|---|---|---|---|
| 5 | Warm-up: C major and G major scales, hands separately | 60 bpm | Even volume |
| 15 | New skill: play each of the six examples (left hand chord, right hand melody), name the non-chord tone aloud, then Exercise 1 | 50 bpm, then 60 | The small tension, and where it ends |
| 5 | Reading: the Minuet in G, bar 1, over the G chord (G, B, D): find the two passing tones (A and C) | Untimed | The notes that move between the chord tones |
| 5 | Guitar: strum C, then play E, D and C on strings 1 and 2 (string 1 open, string 2 at frets 3 and 1) | 60 bpm | The D as a passing note |

Repeat this routine on at least three days.

</div>

<div class="move-on" markdown>

### Move on when

- [ ] You can name all six types from their definitions, without the table.
- [ ] You can play each of the six examples at 60 bpm and say which note is the non-chord tone.
- [ ] You get Exercise 1 right before looking at the answer.
- [ ] You can write one example of your own for each type, over a C chord or a G chord.

</div>

## Common mistakes

Calling every note outside the chord a passing tone. Check how it arrives and where it goes: a neighbour returns to the note it left, and an escape tone leaps away.

Missing the tie in a suspension. The note must be held from the old chord. A note that is only repeated is not a suspension.

Labelling by the beat alone. Appoggiaturas and suspensions are on strong beats. Passing and neighbour tones are usually on weak beats, but they can fall on strong ones too.

## Key terms

- **Chord tone**: a note that belongs to the chord.
- **Non-chord tone**: a note that does not belong to the chord.
- **Passing tone**: a non-chord tone that fills a 3rd by step.
- **Neighbour tone**: a non-chord tone that steps away and back.
- **Suspension**: a note held from the old chord that clashes with the new chord and falls by step.
- **Appoggiatura**: a non-chord tone on a strong beat, reached by leap and left by step.
- **Anticipation**: a note of the next chord that arrives early.
- **Escape tone**: a non-chord tone reached by step and left by a leap in the opposite direction.

Next: [Chopin: Prelude in A major](10-chopin-prelude-in-a-major.md)
