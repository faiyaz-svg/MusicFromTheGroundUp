# Cadences

<span class="tag tag-theory">Theory</span>

After this lesson you can name and play the perfect, plagal, half and deceptive cadences in a major key and in a minor key, and tell them apart by ear.

Before this: [The chords of a key](02-diatonic-chords.md), [Roman numerals](01-roman-numerals.md), [Inversions on piano](../04-intervals-and-triads/08-inversions-on-piano.md). You need: your piano and your guitar.

## The idea

### Sound first: how a phrase ends

Play this phrase and stop after the last chord. The music ends, and you do not need to be told it is over.

```abc
X:1
M:4/4
L:1/4
Q:1/4=60
K:C
%%score {RH LH}
V:RH clef=treble
V:LH clef=bass
[V:RH] "C"[CEG]4 | "F"[CFA]4 | "G"[B,DG]4 | "C"[CEG]4 |]
[V:LH] C,4 | F,4 | G,4 | C,4 |]
```

Now play the same first three bars and stop on the G chord. This time the music hangs, as if a sentence stopped in the middle. The last two chords of a phrase set how the phrase ends. Those last chords are a **cadence**, the chord pattern that closes a phrase, like the punctuation at the end of a sentence.

### Four cadences

Each cadence is a pair of chords. Here they are in C major, with the numerals.

| Cadence | Chords | In C major | What you hear |
|---|---|---|---|
| Perfect (authentic) | V to I | G to C | Finished, like a full stop |
| Plagal | IV to I | F to C | Finished, but softer |
| Half (imperfect) | any chord to V | C to G | Open, like a comma or a question mark |
| Deceptive | V to vi | G to Am | A surprise, like a sentence that turns |

The **perfect cadence** (also called the **authentic cadence**) goes from V to I. It is the strongest ending because the dominant pulls toward the tonic. It sounds most final when both chords are in root position and the melody ends on the tonic note.

The **plagal cadence** goes from IV to I. It has no leading tone pulling up, so it sounds gentler. Hymns end with it, on the word "Amen".

The **half cadence** (also called an **imperfect cadence**) ends on V, from I, ii or IV. The music stops on the dominant, so it feels unfinished and calls for more.

The **deceptive cadence** goes from V to vi. The listener expects I, and gets Am instead. Am shares two notes with C, so the chord is a tonic chord and the music still feels at home, but it is the wrong home.

### Hear them

Listen to all four in C. Each one runs four bars. The first three chords are I, IV and V or similar. The right hand moves by the nearest inversion, and the left hand plays the roots.

```abc
X:1
M:4/4
L:1/4
Q:1/4=60
K:C
%%score {RH LH}
V:RH clef=treble
V:LH clef=bass
[V:RH] "C"[CEG]4 | "G"[B,DG]4 | "F"[CFA]4 | "C"[CEG]4 |
[V:LH] C,4 | G,4 | F,4 | C,4 |
[V:RH] "C"[CEG]4 | "Am"[CEA]4 | "F"[CFA]4 | "G"[B,DG]4 |
[V:LH] C,4 | A,,4 | F,,4 | G,,4 |
[V:RH] "C"[CEG]4 | "F"[CFA]4 | "G"[B,DG]4 | "Am"[CEA]4 |]
[V:LH] C,4 | F,4 | G,4 | A,,4 |]
```

The first line ends with the plagal cadence (F to C). The second ends with the half cadence (the last chord is G). The third ends with the deceptive cadence (G to Am). Play the perfect cadence from the example above for the fourth.

Compare the last two chords of the perfect and deceptive versions. From G to C the right hand steps up (B to C, D to E) and the G stays. From G to Am the same two notes step up, and the G steps up to A as well. The ear expects C, and the A in the bass and the top voice turns the ending.

### In a minor key

The same four cadences exist in minor. The perfect cadence uses the major V, with the raised 7th (G#) as the leading tone.

| Cadence | In A minor |
|---|---|
| Perfect | E to Am (V to i) |
| Plagal | Dm to Am (iv to i) |
| Half | Am to E (i to V) |
| Deceptive | E to F (V to VI) |

```abc
X:1
M:4/4
L:1/4
Q:1/4=60
K:Am
%%score {RH LH}
V:RH clef=treble
V:LH clef=bass
[V:RH] "Am"[CEA]4 | "Dm"[DFA]4 | "E"[B,E^G]4 | "Am"[CEA]4 |]
[V:LH] A,,4 | D,4 | E,4 | A,,4 |]
```

### On the guitar

Play each cadence with open chords in G (G, C, D, Em) and in A minor (Am, Dm, E). Strum four down strokes on the first chord and hold the second one with a single strum, so the ending is clear.

## Try it

Exercise 1, the self-test: cover the staff with a sheet of paper, press play, and write down which cadence each bar pair ends with. The four bar pairs are in G major. Then uncover the music and check.

```abc
X:1
M:4/4
L:1/4
Q:1/4=60
K:G
%%score {RH LH}
V:RH clef=treble
V:LH clef=bass
[V:RH] "G"[GBd]2 "D"[FAd]2 | "D"[FAd]2 "Em"[GBe]2 | "C"[Gce]2 "G"[GBd]2 | "D"[FAd]2 "G"[GBd]2 |]
[V:LH] G,2 D,2 | D,2 E,2 | C,2 G,2 | D,2 G,2 |]
```

<details class="solution" markdown>
<summary>Answer</summary>

Bar 1: G to D, a half cadence (ends on V). Bar 2: D to Em, a deceptive cadence (V to vi). Bar 3: C to G, a plagal cadence (IV to I). Bar 4: D to G, a perfect cadence (V to I).

</details>

Exercise 2. Name the chords for a deceptive cadence in F major.

<details class="solution" markdown>
<summary>Answer</summary>

V to vi: C (C, E, G) to Dm (D, F, A).

</details>

Exercise 3. In the Minuet in G, bar 7 is a G chord, and bar 8 has D in the bass with the melody on A. What kind of cadence ends bar 8?

<details class="solution" markdown>
<summary>Answer</summary>

A half cadence: I (G) to V (D), ending on the dominant. The piece continues, as a half cadence asks it to.

</details>

<div class="practice" markdown>

### Practice routine (30 minutes)

| Minutes | What to do | Tempo | Listen for |
|---|---|---|---|
| 5 | Warm-up: A natural and harmonic minor scales, right hand | 60 bpm | The raised G# in the harmonic form |
| 15 | New skill: the four cadences in C, then in G (right-hand triad, left-hand root), saying the name of each after you play it | 50 bpm, then 60 | Finished, soft, open and surprised |
| 5 | Ear training: the self-test above; then ask a friend or a recording to stop on a chord, and say whether it is finished | Untimed | Whether the last chord is home |
| 5 | Guitar: G, D and C, then Am, Dm and E, one strum per chord, as perfect and plagal cadences | 60 bpm | The tonic chord ringing at the end |

Repeat this routine on at least three days.

</div>

<div class="move-on" markdown>

### Move on when

- [ ] You can play all four cadences in C and in G without notes, naming each, at 60 bpm.
- [ ] You can play the perfect and plagal cadences in A minor.
- [ ] You pass the self-test above with at most one wrong answer.
- [ ] You can name the cadence in any pair of chords in a key given the numerals, for example V to vi.

</div>

## Common mistakes

Calling every V to I a perfect cadence. If the V is not a real chord change at the end of a phrase, it is only part of a progression. A cadence sits at the end of a phrase.

Confusing the half cadence with the perfect cadence because both involve V. In a half cadence V is the last chord. In a perfect cadence V comes before the last chord.

Forgetting the raised 7th in minor. A perfect cadence in A minor needs E major (with G#), not Em.

## Key terms

- **Cadence**: the chords that close a phrase.
- **Perfect cadence** (authentic): V to I.
- **Plagal cadence**: IV to I.
- **Half cadence** (imperfect): a phrase ending on V.
- **Deceptive cadence**: V to vi.

Next: [Seventh chords](04-seventh-chords.md)
