# Music From the Ground Up

A self-study music textbook for piano and guitar, for a complete beginner: reading sheet music and tab, chords, scales, harmony, sight reading, playing by ear and improvising, with classical pieces and original pieces in a film, game and anime style. Lessons are short, each with a 30-minute practice routine. Music examples are drawn and played in the browser.

Read it online: https://faiyaz-svg.github.io/MusicFromTheGroundUp/

The sibling books: [Math From the Ground Up](https://faiyaz-svg.github.io/MathFromTheGroundUp/) and [CS From the Ground Up](https://faiyaz-svg.github.io/CSFromTheGroundUp/).

## Preview locally

```bash
py -m venv .venv
.venv/Scripts/python -m pip install -r requirements-dev.txt
.venv/Scripts/zensical serve
```

Then open http://127.0.0.1:8000/MusicFromTheGroundUp/. The writing rules are in `STYLE.md`, the lesson layout in `LESSON_TEMPLATE.md` and the site design in `DESIGN.md`.

## Credits

- Sheet music and playback: [abcjs](https://github.com/paulrosen/abcjs) (MIT).
- Piano and guitar sounds: the FluidR3_GM soundfont by Frank Wen, as prepared in [midi-js-soundfonts](https://github.com/gleitz/midi-js-soundfonts) (CC BY 3.0).
