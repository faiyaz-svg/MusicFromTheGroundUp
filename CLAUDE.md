# Music From the Ground Up

A self-study music textbook for one reader: a 4th-year CS student in Ontario who is a complete beginner at music, with an 88-key digital piano (three pedals) and a right-handed acoustic steel-string guitar, about 30 minutes a day to practise, and a taste for classical and film, game and anime music. The goal is an intermediate level on both instruments: piano from sheet music with good sight reading (roughly RCM Level 5-6), guitar from chords and tab, theory to roughly RCM Theory 6-7 plus film and anime harmony, improvising and playing by ear. The Markdown in `docs/` is published to https://faiyaz-svg.github.io/MusicFromTheGroundUp/ and also read directly in VS Code. The sibling books are https://faiyaz-svg.github.io/MathFromTheGroundUp/ and https://faiyaz-svg.github.io/CSFromTheGroundUp/.

## Rules to follow

- Writing: `STYLE.md`. Every page must follow it, including the list of AI-writing patterns to avoid and the music conventions. Em dashes are the most common slip.
- Lesson structure: `LESSON_TEMPLATE.md`.
- Site look: `DESIGN.md`.
- Don't make decisions the reader hasn't agreed to. Ask first when a change goes beyond what was requested.

## Layout

- `docs/00-start-here`, then `docs/01-first-sounds` to `docs/13-capstones`: the book in reading order, as 13 stages. Each stage folder is flat (`NN-slug.md` lessons) with an `index.md` overview and cheat sheet. Each lesson is tagged with one area (theory, reading, piano, guitar, ear, improvise, other) in `tools/lessons.yml`. The piano path skips lessons tagged guitar, and the guitar path skips lessons tagged piano.
- `docs/practice`: note flashcards and the reading, fretboard and ear drills (they run in the browser). `docs/reference`: glossary, notation symbols, Italian terms, chord charts, scales and keys, common mistakes, videos, play next.
- `docs/my-music/` is the reader's own purchased music. It is gitignored, never committed while the repo is public, and the CI workflow deletes it before building, so it never reaches the public site. No public page links to it.
- `mkdocs.yml` holds the site config and the `nav`. `tools/lessons.yml` lists every lesson; run `tools/build_nav.py` after adding one.
- Music examples are `abc` code blocks. `docs/javascripts/music.js` draws them with abcjs (6.7.2, from jsDelivr) and plays them with the self-hosted FluidR3_GM soundfont subset in `docs/assets/soundfont/` (CC BY 3.0, credited on the credits page).
- `tools/figures/musicfigs.py` draws keyboards, chord diagrams, fretboards and staff notes as SVG; each lesson's figure script lives in `tools/figures/<stage>/<lesson>.py` and writes to `docs/assets/figures/<stage>/`.
- `anki/cards/<stage>.tsv` -> `anki/build_decks.py` -> `docs/downloads/anki/<stage>.apkg`.

## Commands (Windows, Git Bash)

```bash
npm install                                  # abcjs, for check_abc.mjs (dev only)
py -m venv .venv
.venv/Scripts/python -m pip install -r requirements-dev.txt
.venv/Scripts/zensical serve                 # preview at http://127.0.0.1:8000/MusicFromTheGroundUp/
.venv/Scripts/zensical build --clean
node tools/check_abc.mjs                     # every abc block parses and every bar adds up
.venv/Scripts/python tools/check_theory.py   # chord spellings, key signatures and intervals in the text
.venv/Scripts/python tools/build_nav.py      # after adding lessons: nav, progress page, stage lesson lists
.venv/Scripts/python tools/link_planned.py   # turn <!-- link: ... --> comments into links once targets exist
.venv/Scripts/python anki/build_decks.py
```

## Before committing a page

1. Run the self-check in `STYLE.md` (em dashes, curly quotes, banned words and patterns).
2. Run `node tools/check_abc.mjs` and `tools/check_theory.py`. Recompute every answer and table value.
3. Check that no copyrighted melody, tab or lyric appears, and that public-domain pieces name their source edition.
4. `zensical build --clean` must report no issues.
5. `git ls-files` must show nothing under `docs/my-music` and no `.pdf` or `.mid` files.

## Git

- Work on `main`. The whole repo has a hard cap of 100 commits, so commit 3 or 4 lessons at a time. Check the count with `git rev-list --count HEAD`. Short, plain messages ("add stage 1 lessons 1 to 4").
- No Co-Authored-By or any other attribution lines in commits or pull requests, even if a tool suggests one.
- No force pushes.
