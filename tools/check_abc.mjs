// Check every ```abc block in docs/: it parses without warnings, every bar
// has the right length for its time signature, and guitar tab notes are
// playable in standard tuning (frets 0 to 19).
//
//   node tools/check_abc.mjs                 check all of docs/
//   node tools/check_abc.mjs docs/01-first-sounds/10-first-melodies-on-piano.md
//   node tools/check_abc.mjs --dump FILE     also print the notes (MIDI numbers) of each block
//
// A first or last bar may be short (a pickup and its partner). Anything else
// that doesn't add up is reported with the block number and bar number.

import fs from "node:fs"
import path from "node:path"
import abcjs from "abcjs"

const args = process.argv.slice(2)
const dump = args.includes("--dump")
const targets = args.filter((a) => !a.startsWith("--"))
const roots = targets.length ? targets : ["docs"]

const STEP = [0, 2, 4, 5, 7, 9, 11] // C D E F G A B
const ACC = { sharp: 1, flat: -1, natural: 0, dblsharp: 2, dblflat: -2, quartersharp: 0, quarterflat: 0 }
const GUITAR_LOW = 40 // E2, open string 6
const GUITAR_HIGH = 64 + 19 // fret 19 on string 1

function walk(p, out) {
  const st = fs.statSync(p)
  if (st.isDirectory()) {
    for (const name of fs.readdirSync(p)) {
      if (name === "my-music" || name.startsWith(".")) continue
      walk(path.join(p, name), out)
    }
  } else if (p.endsWith(".md")) out.push(p)
  return out
}

function blocks(text) {
  const found = []
  const re = /^```abc[^\n]*\n([\s\S]*?)^```/gm
  let m
  while ((m = re.exec(text))) {
    const line = text.slice(0, m.index).split("\n").length
    found.push({ abc: m[1], line })
  }
  return found
}

function close(a, b) {
  return Math.abs(a - b) < 1e-6
}

function checkTune(abc, report) {
  const warnings = []
  let tunes
  try {
    tunes = abcjs.parseOnly(abc.replace(/^%%opts.*\n/m, ""), { warnings_id: null })
  } catch (e) {
    report(`does not parse: ${e.message}`)
    return null
  }
  const tune = tunes[0]
  if (!tune) {
    report("no tune found (missing X: line?)")
    return null
  }
  for (const w of tune.warnings || []) warnings.push(String(w).replace(/<[^>]+>/g, ""))
  for (const w of warnings) report(`abcjs warning: ${w}`)

  const tab = /^%%opts\b.*\btab=guitar\b/m.test(abc)
  const meter = tune.getMeterFraction ? tune.getMeterFraction() : { num: 4, den: 4 }
  const barLength = meter.num / meter.den
  const voices = new Map() // voice index -> {bars: [len...], notes: []}

  tune.lines.forEach((line) => {
    if (!line.staff) return
    line.staff.forEach((staff, si) => {
      const clefShift = staff.clef && staff.clef.type && staff.clef.type.includes("-8") ? -12 : 0
      const keyAcc = {}
      for (const a of (staff.key && staff.key.accidentals) || []) keyAcc[a.note.toLowerCase()] = ACC[a.acc] || 0
      staff.voices.forEach((voice, vi) => {
        const id = `${si}.${vi}`
        if (!voices.has(id)) voices.set(id, { bars: [], current: 0, notes: [], barAcc: {}, triplet: 1, tripletLeft: 0, keyAcc })
        const v = voices.get(id)
        v.keyAcc = keyAcc
        for (const el of voice) {
          if (el.el_type === "key" && el.accidentals) {
            v.keyAcc = {}
            for (const a of el.accidentals) v.keyAcc[a.note.toLowerCase()] = ACC[a.acc] || 0
          }
          if (el.el_type === "bar") {
            if (v.current > 1e-9) v.bars.push(v.current)
            v.current = 0
            v.barAcc = {}
            continue
          }
          if (el.el_type !== "note") continue
          if (el.startTriplet) {
            v.triplet = el.tripletMultiplier || 2 / 3
            v.tripletLeft = el.startTriplet
          }
          if (!el.duration) continue
          v.current += el.duration * v.triplet
          if (el.endTriplet) v.triplet = 1
          if (el.pitches && !el.rest) {
            const midis = el.pitches.map((p) => {
              const letter = ((p.pitch % 7) + 7) % 7
              const octave = Math.floor(p.pitch / 7)
              const name = "cdefgab"[letter] + octave
              let acc
              if (p.accidental) {
                acc = ACC[p.accidental] || 0
                v.barAcc[name] = acc
              } else if (name in v.barAcc) acc = v.barAcc[name]
              else acc = v.keyAcc["cdefgab"[letter]] || 0
              return 60 + 12 * octave + STEP[letter] + acc + clefShift
            })
            v.notes.push(midis)
            if (tab) {
              for (const m of midis) {
                if (m < GUITAR_LOW || m > GUITAR_HIGH) report(`tab note out of guitar range (MIDI ${m})`)
              }
            }
          }
        }
      })
    })
  })

  for (const [id, v] of voices) {
    if (v.current > 1e-9) v.bars.push(v.current)
    const bars = v.bars
    bars.forEach((len, i) => {
      if (close(len, barLength)) return
      // A short first bar is a pickup. A short last bar is allowed only
      // when there was a pickup, since the two together make a full bar.
      if (i === 0 && len < barLength) return
      if (i === bars.length - 1 && len < barLength && bars[0] < barLength - 1e-6) return
      report(`voice ${id}, bar ${i + 1}: ${+(len * meter.den).toFixed(3)} beats of 1/${meter.den}, expected ${meter.num}`)
    })
  }
  return voices
}

let problems = 0
let count = 0
const files = roots.flatMap((r) => walk(r, []))
for (const file of files) {
  const text = fs.readFileSync(file, "utf8")
  blocks(text).forEach((b, i) => {
    count++
    const report = (msg) => {
      problems++
      console.log(`${file}:${b.line} block ${i + 1}: ${msg}`)
    }
    if (!/^X:/m.test(b.abc)) report("missing X: line")
    if (!/^M:/m.test(b.abc)) report("missing M: line")
    if (!/^L:/m.test(b.abc)) report("missing L: line")
    if (!/^K:/m.test(b.abc)) report("missing K: line")
    const voices = checkTune(b.abc, report)
    if (dump && voices) {
      for (const [id, v] of voices) console.log(`${file}:${b.line} block ${i + 1} voice ${id}: ${v.notes.map((n) => n.join("+")).join(" ")}`)
    }
  })
}
console.log(`${count} abc blocks in ${files.length} files, ${problems} problems`)
process.exit(problems ? 1 : 0)
