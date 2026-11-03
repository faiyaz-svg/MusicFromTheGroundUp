# Design

The site look for Music From the Ground Up. It follows the spirit of Ableton's Learning Music site: big type, flat blocks of colour, lots of space, square corners. It uses no Ableton name, logo, image, icon or font. Our own addition is that each stage of the book has its own colour.

Files: `docs/stylesheets/site.css` (all styles) and `docs/javascripts/theme.js` (sets the stage colour). Writing rules are in `STYLE.md` and lesson structure is in `LESSON_TEMPLATE.md`.

## Principles

- Flat. No shadows, no gradients, no glow, no blur, no rounded corners.
- Big and spacious. The base size is 20px with a line height of 1.5. Headings are bold.
- Long reading text is black on white (light on dark in dark mode). Bright colours only sit behind short text, and that text is always black.
- Colour has jobs. It marks the stage you are in, and nothing else is coloured for decoration.
- Not everything has the same weight. The page title is a big block, boxes are quieter, and body text is plain.

## Type

Jost from Google Fonts (weights 400, 500, 700 and italic 400). It is a free font close to Futura. Code uses the system monospace font.

## Colours

Five bright colours, plus red and greys.

| Name | Hex | Use |
|---|---|---|
| Goldfish yellow | `#fed134` | Stage colour 1 |
| Salmon | `#ff8389` | Stage colour 2, playing guitar tag |
| Lavender | `#d5b3ff` | Stage colour 3 only. Never an accent, link or background fill. |
| Tiffany teal | `#00d2be` | Stage colour 4 |
| Sky blue | `#6dcbff` | Stage colour 5 |
| Red | `#ff2956` | Warnings, the note being played |
| Grey | `#b3b3b3` | Pages with no stage |

Text on any of these is black. Every pair has a contrast ratio above 4.5:1.

## Stage colours

The 13 stages cycle through the five colours, based on the folder number in the URL.

| Stage folders | Colour |
|---|---|
| 01, 06, 11 | Yellow |
| 02, 07, 12 | Salmon |
| 03, 08, 13 | Lavender |
| 04, 09 | Teal |
| 05, 10 | Blue |

`theme.js` reads the URL on every page change (including instant navigation) and sets `data-stage="1"` to `"5"` on `body`. The CSS variable `--stage` follows from that. Pages outside stages 01 to 13 (start here, practice tools, reference, this guide) have no `data-stage` and use grey.

The stage colour shows in four places:

- the solid block behind the page title (h1)
- the marker under the active tab
- the bar on the left of the current sidebar item
- the underline of links, the underline of h2 headings and the bar beside h3 headings

## Layout

- Header: black, with the site title and search box. Square, no shadow.
- Tabs: about 16 short labels such as "1 Sounds" and "13 Capstones", then "Start here", "Practice tools" and "Reference". They are small so they fit at 1400px. On narrow screens the tabs are replaced by the menu drawer.
- Sidebar: plain list, the current page has a 4px bar in the stage colour.
- Page: a column about 44rem wide. The h1 block comes first, then the tags on one line, then the Previous and Next buttons, then the lesson.
- Footer: black. The theme's own Previous and Next links are hidden because the page has its own buttons.

## Previous and Next buttons

`prevnext.js` adds `nav.mf-prevnext` after the h1 and at the end of the page. Next is filled with the stage colour and has black text. Previous is outlined. Both are square. On hover they swap colours.

## Boxes

Boxes are flat panels with a thick bar on the left. Write them as `<div class="..." markdown>` so Markdown works inside.

| Class | Use | Bar colour |
|---|---|---|
| `example` | Worked example | Stage colour, grey panel |
| `note` | Side remark | Blue |
| `warning` | Common mistake or danger | Red |
| `practice` | Practice routine, holds a table of minutes and tasks | Yellow |
| `move-on` | "Move on when" checklist | Teal |
| `film` | "Film yourself" checklist with one video link | Salmon |

Example:

```markdown
<div class="practice" markdown>
**Practice routine**

| Minutes | Task |
|---|---|
| 2 | Slow scales |
| 5 | The tune, hands apart |
</div>

<div class="move-on" markdown>
**Move on when**

- [ ] You can find middle C without looking
- [ ] You can play the scale at 60 beats per minute
</div>
```

Never put one box inside another.

### Solutions

A collapsible answer is white with a thin grey border.

```markdown
<details class="solution" markdown>
<summary>Show the answer</summary>

The answer is two steps.
</details>
```

## Lesson tags

Small square labels, written on one line under the h1.

```markdown
<span class="tag tag-piano">Piano</span> <span class="tag tag-theory">Theory</span>
```

| Class | Colour |
|---|---|
| `tag-piano` | Yellow |
| `tag-guitar` | Salmon |
| `tag-theory` | Lavender |
| `tag-reading` | Teal |
| `tag-ear` | Blue |
| `tag-improvise` | Red |
| `tag-other` | Grey |
| `tag-optional` | White with a dashed border |
| `tag-stretch` | Black with white text |

## Music blocks

Write music as a fenced `abc` block. `music.js` draws it with abcjs.

- The score sits in `.mf-music` as a white panel with a black border. Notation is black on white in both colour schemes, so in dark mode the panel stays white.
- The play bar (`.mf-audio`) is a flat black strip with square buttons. Pressed buttons and the progress marker use the stage colour.
- The note being played gets `.mf-playing` and turns red (`#ff2956`).
- The ABC source is hidden on the site.
- The play bar CSS is based on `abcjs-audio.css` from abcjs (MIT licence).

## Tables and code

Tables have a 2px dark outline, a grey header row and thin row lines. Inline code is a flat grey chip with square corners. Code blocks are flat and square.

## Figures

SVG figures sit on white. In dark mode they get a white panel with a little padding, so the drawing keeps its colours.

## Dark mode

- Surfaces are dark grey: page `#1e1e1e`, panels `#2a2a2a`, header `#121212`.
- Text is `#f2f2f2`. Muted text is `#b3b3b3`.
- The five bright colours stay the same, and text on them stays black.
- Boxes keep their coloured left bars on a dark panel.
- No neon, no glow.

## Things to avoid

- Gradients, glow or aurora backgrounds, glass or blur, neon on dark.
- Emoji as icons.
- A centred hero with a pill badge, a tagline, three icon cards and a button.
- Inter or Geist fonts.
- Drop shadows, rounded corners, and cards inside cards.
- Marketing words such as "unlock", "master", "journey", "elevate" and "level up".
- Making every part the same visual weight.
- Lavender as the main accent, a link colour or part of a gradient.
- Long text on a bright colour.
