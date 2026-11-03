// Draw every ```abc block as sheet music (and guitar tab when asked), with a
// play bar: play, loop, restart, progress and a tempo slider. Notes light up
// as they play. Uses abcjs (loaded before this file in mkdocs.yml).
//
// The first line of a block can hold options, for example:
//   %%opts tab=guitar sound=steel
//   tab=guitar      add guitar tab under the staff (standard tuning)
//   sound=piano|steel|nylon   the instrument for playback (piano by default,
//                   steel when the block has tab)
//   play=off        no play bar (for a picture of notation only)
//   chords=on       also play the chord symbols above the staff
//   capo=N          tab with a capo at fret N

const MF_SOUNDFONT = new URL("../assets/soundfont/", document.currentScript ? document.currentScript.src : location.href).href
const MF_PROGRAMS = { piano: 0, nylon: 24, steel: 25 }
let mfSynths = []

function mfOptions(text) {
  const opts = {}
  const first = text.split("\n", 1)[0]
  if (first.startsWith("%%opts")) {
    first.slice(6).trim().split(/\s+/).forEach((pair) => {
      const [k, v] = pair.split("=")
      if (k) opts[k] = v === undefined ? "on" : v
    })
  }
  return opts
}

function mfCursor(paper) {
  let lit = []
  const clear = () => {
    lit.forEach((el) => el.classList.remove("mf-playing"))
    lit = []
  }
  return {
    onStart: clear,
    onFinished: clear,
    onEvent(ev) {
      clear()
      if (!ev || !ev.elements) return
      ev.elements.forEach((group) => group.forEach((el) => {
        el.classList.add("mf-playing")
        lit.push(el)
      }))
    },
  }
}

function mfRender(pre) {
  const code = pre.querySelector("code") || pre
  const text = code.textContent.replace(/\s+$/, "") + "\n"
  const opts = mfOptions(text)

  const box = document.createElement("div")
  box.className = "mf-music"
  const paper = document.createElement("div")
  paper.className = "mf-paper"
  box.appendChild(paper)
  pre.after(box)
  pre.classList.add("mf-source")

  const params = {
    responsive: "resize",
    add_classes: true,
    paddingleft: 0,
    paddingright: 0,
    paddingtop: 8,
    paddingbottom: 8,
  }
  // abcjs makes the drawing a little too short for tab, which clips the
  // lowest string, so tab blocks get extra room at the bottom.
  if (opts.tab) {
    params.paddingbottom = 30
    // Guitar music uses clef=treble-8, so abcjs already moves the written
    // notes down an octave (correct playback). Its tab also expects written
    // pitch, so the tuning is given an octave lower to match: E2 A2 D3 G3 B3 E4.
    params.tablature = [{
      instrument: "guitar",
      tuning: ["E,,", "A,,", "D,", "G,", "B,", "E"],
      label: "",
      capo: opts.capo ? Number(opts.capo) : 0,
      highestNote: "e'''",
    }]
  }

  let tune
  try {
    tune = ABCJS.renderAbc(paper, text.replace(/^%%opts.*\n/m, ""), params)[0]
  } catch (e) {
    paper.textContent = "This music could not be drawn. The notation is shown above."
    pre.classList.remove("mf-source")
    return
  }

  if (opts.play === "off" || !ABCJS.synth.supportsAudio()) return

  const bar = document.createElement("div")
  bar.className = "mf-audio"
  box.appendChild(bar)
  const sound = opts.sound || (opts.tab ? "steel" : "piano")
  const synth = new ABCJS.synth.SynthController()
  synth.load(bar, mfCursor(paper), {
    displayLoop: true,
    displayRestart: true,
    displayPlay: true,
    displayProgress: true,
    displayWarp: true,
  })
  synth.setTune(tune, false, {
    program: MF_PROGRAMS[sound] === undefined ? 0 : MF_PROGRAMS[sound],
    soundFontUrl: MF_SOUNDFONT,
    soundFontVolumeMultiplier: 3.0,
    chordsOff: opts.chords !== "on",
  }).catch(() => {
    bar.textContent = "Audio could not start in this browser."
  })
  mfSynths.push(synth)
}

document$.subscribe(() => {
  // Instant navigation swaps the page without a reload: stop the old players.
  mfSynths.forEach((s) => {
    try { s.pause() } catch (e) { /* already gone */ }
  })
  mfSynths = []
  document.querySelectorAll("pre.abc:not(.mf-done)").forEach((pre) => {
    pre.classList.add("mf-done")
    mfRender(pre)
  })
})
