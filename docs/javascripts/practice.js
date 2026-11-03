// Practice tools: note flashcards, reading drill, fretboard drill, interval
// and chord ear quizzes. A page holds <div class="mf-tool" data-tool="..."></div>
// and this file builds the tool inside it. Uses abcjs (loaded before this file).
// Saves settings and flashcard boxes in localStorage ("musicftgu-practice-v1").
(function () {
  "use strict"

  const SOUNDFONT = new URL("../assets/soundfont/", document.currentScript ? document.currentScript.src : location.href).href
  const PREFIX = "musicftgu-practice-v1"

  // ---------- small helpers ----------

  function store(name, fallback) {
    try {
      const raw = localStorage.getItem(PREFIX + ":" + name)
      return raw === null ? fallback : JSON.parse(raw)
    } catch (e) {
      return fallback
    }
  }
  function save(name, value) {
    try {
      localStorage.setItem(PREFIX + ":" + name, JSON.stringify(value))
    } catch (e) { /* storage blocked: the tool still works for this visit */ }
  }

  function h(tag, attrs, kids) {
    const el = document.createElement(tag)
    for (const k in attrs || {}) {
      const v = attrs[k]
      if (k === "text") el.textContent = v
      else if (k.startsWith("on")) el.addEventListener(k.slice(2), v)
      else if (v !== false && v !== null && v !== undefined) el.setAttribute(k, v === true ? "" : v)
    }
    ;(kids || []).forEach((c) => c && el.appendChild(typeof c === "string" ? document.createTextNode(c) : c))
    return el
  }
  const SVGNS = "http://www.w3.org/2000/svg"
  function s(tag, attrs, kids) {
    const el = document.createElementNS(SVGNS, tag)
    for (const k in attrs || {}) {
      if (k === "text") el.textContent = attrs[k]
      else el.setAttribute(k, attrs[k])
    }
    ;(kids || []).forEach((c) => c && el.appendChild(c))
    return el
  }
  const rand = (n) => Math.floor(Math.random() * n)
  const pick = (a) => a[rand(a.length)]

  let cleanups = []
  function onCleanup(fn) { cleanups.push(fn) }
  function addTimer(fn, ms) {
    const id = setTimeout(fn, ms)
    onCleanup(() => clearTimeout(id))
    return id
  }
  function onKey(fn) {
    const handler = (e) => {
      const t = e.target
      if (e.ctrlKey || e.metaKey || e.altKey) return
      if (t && /^(INPUT|SELECT|TEXTAREA)$/.test(t.tagName) && t.type !== "checkbox") return
      fn(e)
    }
    document.addEventListener("keydown", handler)
    onCleanup(() => document.removeEventListener("keydown", handler))
  }

  // ---------- notes ----------

  const LETTERS = ["C", "D", "E", "F", "G", "A", "B"]
  const SEMI = [0, 2, 4, 5, 7, 9, 11]
  const SHARP_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

  function parseNote(str) {
    const m = /^([A-G])([#b]?)(\d)$/.exec(str)
    return { l: LETTERS.indexOf(m[1]), acc: m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0, oct: Number(m[3]) }
  }
  const midiOf = (n) => 12 * (n.oct + 1) + SEMI[n.l] + n.acc
  const nameOf = (n) => LETTERS[n.l] + (n.acc > 0 ? "#" : n.acc < 0 ? "b" : "") + n.oct
  const diaOf = (n) => n.oct * 7 + n.l
  const fromDia = (d) => ({ l: ((d % 7) + 7) % 7, oct: Math.floor(d / 7), acc: 0 })
  function naturalRange(from, to) {
    const out = []
    for (let d = diaOf(parseNote(from)); d <= diaOf(parseNote(to)); d++) out.push(fromDia(d))
    return out
  }
  function midiToNote(m) {
    const pc = ((m % 12) + 12) % 12
    const name = SHARP_NAMES[pc]
    return { l: LETTERS.indexOf(name[0]), acc: name.length > 1 ? 1 : 0, oct: Math.floor(m / 12) - 1 }
  }

  // abc spelling of a note. withAcc writes an explicit natural sign (=) so a
  // sharp earlier in the bar never carries over.
  function abcPitch(n, withAcc) {
    const prefix = n.acc > 0 ? "^" : n.acc < 0 ? "_" : withAcc ? "=" : ""
    const letter = LETTERS[n.l]
    if (n.oct >= 5) return prefix + letter.toLowerCase() + "'".repeat(n.oct - 5)
    return prefix + letter + ",".repeat(4 - n.oct)
  }

  // ---------- audio ----------

  let activeSynth = null
  let controllers = []

  function stopAudio() {
    if (activeSynth) {
      try { activeSynth.stop() } catch (e) { /* already stopped */ }
      activeSynth = null
    }
    controllers.forEach((c) => {
      try { c.pause() } catch (e) { /* already gone */ }
    })
  }

  function audioOk() {
    return !!(window.ABCJS && ABCJS.synth && ABCJS.synth.supportsAudio())
  }

  // events: [{ midis: [60, 64], beats: 2 }, ...] played one after the other.
  // Builds a tiny abc tune, never drawn, and plays it with CreateSynth.
  async function playEvents(events, bpm) {
    if (!audioOk()) return false
    stopAudio()
    const body = events.map((e) => {
      const ps = e.midis.map((m) => abcPitch(midiToNote(m), true))
      return (ps.length > 1 ? "[" + ps.join("") + "]" : ps[0]) + (e.beats === 1 ? "" : e.beats)
    }).join(" ")
    const abc = "X:1\nM:none\nL:1/4\nQ:1/4=" + (bpm || 80) + "\nK:C\n" + body + " |]\n"
    try {
      const tune = ABCJS.renderAbc("*", abc, {})[0]
      const synth = new ABCJS.synth.CreateSynth()
      activeSynth = synth
      await synth.init({ visualObj: tune, options: { soundFontUrl: SOUNDFONT, program: 0, soundFontVolumeMultiplier: 3.0 } })
      await synth.prime()
      if (activeSynth !== synth) return false
      const ctx = ABCJS.synth.activeAudioContext && ABCJS.synth.activeAudioContext()
      if (ctx && ctx.state === "suspended") await ctx.resume()
      synth.start()
      return true
    } catch (e) {
      return false
    }
  }

  // ---------- shared pieces ----------

  function btn(label, onclick, extra) {
    return h("button", Object.assign({ type: "button", class: "mf-tool-btn", text: label, onclick: onclick }, extra || {}))
  }
  function check(label, checked, onchange) {
    const input = h("input", { type: "checkbox" })
    input.checked = !!checked
    input.addEventListener("change", () => onchange(input.checked))
    return h("label", { class: "mf-tool-check" }, [input, h("span", { text: label })])
  }
  function field(label, control) {
    return h("label", { class: "mf-tool-field" }, [h("span", { text: label }), control])
  }
  function select(options, value, onchange) {
    const el = h("select", { class: "mf-tool-select" })
    options.forEach((o) => {
      const opt = h("option", { value: o[0], text: o[1] })
      if (String(o[0]) === String(value)) opt.selected = true
      el.appendChild(opt)
    })
    el.addEventListener("change", () => onchange(el.value))
    return el
  }
  function toggle(label, pressed, onchange) {
    const b = btn(label, () => {
      const on = b.getAttribute("aria-pressed") !== "true"
      b.setAttribute("aria-pressed", String(on))
      onchange(on)
    }, { "aria-pressed": String(!!pressed) })
    return b
  }
  function setPressed(group, id) {
    group.forEach(([key, b]) => b.setAttribute("aria-pressed", String(key === id)))
  }

  // A session score: right, wrong and average seconds per card.
  function makeStats(target) {
    const st = { right: 0, wrong: 0, secs: 0, n: 0 }
    const rightEl = h("strong", { text: "0" })
    const wrongEl = h("strong", { text: "0" })
    const avgEl = h("strong", { text: "-" })
    const avgBox = h("div", { class: "mf-stat" }, [h("span", { text: "Average per card" }), avgEl])
    const box = h("div", { class: "mf-stats" }, [
      h("div", { class: "mf-stat" }, [h("span", { text: "Right" }), rightEl]),
      h("div", { class: "mf-stat" }, [h("span", { text: "Wrong" }), wrongEl]),
      avgBox,
    ])
    function paint() {
      rightEl.textContent = st.right
      wrongEl.textContent = st.wrong
      if (st.n) {
        const avg = st.secs / st.n
        avgEl.textContent = avg.toFixed(1) + " s"
        avgBox.classList.toggle("is-right", st.n >= 3 && avg < (target || 3))
      } else {
        avgEl.textContent = "-"
        avgBox.classList.remove("is-right")
      }
    }
    return {
      el: box,
      add(ok, secs) {
        if (ok) st.right++
        else st.wrong++
        if (secs !== undefined) { st.secs += Math.min(30, secs); st.n++ }
        paint()
      },
      time(secs) { st.secs += Math.min(60, secs); st.n++; paint() },
      reset() { st.right = 0; st.wrong = 0; st.secs = 0; st.n = 0; paint() },
    }
  }

  // A reset button that needs a second tap.
  function resetButton(label, doReset) {
    let armed = false
    let timer = null
    const b = btn(label, () => {
      if (!armed) {
        armed = true
        b.textContent = "Tap again to confirm"
        timer = setTimeout(() => { armed = false; b.textContent = label }, 3000)
        return
      }
      clearTimeout(timer)
      armed = false
      b.textContent = label
      doReset()
    })
    onCleanup(() => clearTimeout(timer))
    return b
  }

  // Answer letters A to G, plus sharp and flat latches when asked.
  function letterPad(withAccidentals, onAnswer) {
    const letters = {}
    let latch = 0
    const accBtns = {}
    const pad = h("div", { class: "mf-letters" })
    "ABCDEFG".split("").forEach((L) => {
      letters[L] = btn(L, () => answer(L))
      pad.appendChild(letters[L])
    })
    const wrap = h("div", {}, [pad])
    function paintLatch() {
      if (accBtns.sharp) {
        accBtns.sharp.setAttribute("aria-pressed", String(latch === 1))
        accBtns.flat.setAttribute("aria-pressed", String(latch === -1))
      }
    }
    function setLatch(v) {
      latch = latch === v ? 0 : v
      paintLatch()
    }
    if (withAccidentals) {
      accBtns.sharp = btn("# sharp", () => setLatch(1), { "aria-pressed": "false" })
      accBtns.flat = btn("b flat", () => setLatch(-1), { "aria-pressed": "false" })
      wrap.appendChild(h("div", { class: "mf-tool-row mf-two" }, [accBtns.sharp, accBtns.flat]))
    }
    function answer(L) {
      const acc = latch
      latch = 0
      paintLatch()
      onAnswer(L, acc)
    }
    return {
      el: wrap,
      letters,
      accBtns,
      latchKey(v) { if (withAccidentals) setLatch(v) },
      clear() {
        Object.values(letters).concat(Object.values(accBtns)).forEach((b) => b.classList.remove("is-right", "is-wrong"))
        latch = 0
        paintLatch()
      },
    }
  }

  // ---------- A. note flashcards ----------

  const FC_SETS = [
    { id: "treble-cg", label: "Treble: middle C to G", clef: "treble", notes: naturalRange("C4", "G4") },
    { id: "treble-all", label: "Treble: all lines and spaces", clef: "treble", notes: naturalRange("E4", "F5") },
    { id: "treble-ledger", label: "Treble: ledger lines", clef: "treble", notes: naturalRange("A3", "C4").concat(naturalRange("G5", "C6")) },
    { id: "bass-c", label: "Bass: C position", clef: "bass", notes: naturalRange("C3", "G3") },
    { id: "bass-all", label: "Bass: all lines and spaces", clef: "bass", notes: naturalRange("G2", "A3") },
    { id: "bass-ledger", label: "Bass: ledger lines", clef: "bass", notes: naturalRange("C2", "F2").concat(naturalRange("B3", "E4")) },
    { id: "grand", label: "Grand staff", clef: "grand", notes: naturalRange("G2", "F5") },
    {
      id: "black", label: "Sharps and flats", clef: "auto",
      notes: [3, 4].reduce((acc, oct) => acc.concat(
        ["C#", "Eb", "D#", "Gb", "F#", "Ab", "G#", "Bb", "A#", "Db"].map((n) => parseNote(n + oct))), []),
    },
  ]

  function flashcardAbc(card) {
    const n = card.note
    const pitch = abcPitch(n, false)
    if (card.clef === "grand") {
      const upper = n.oct >= 4
      return "X:1\nM:none\nL:1\n%%score {1 2}\nV:1 clef=treble\nV:2 clef=bass\nK:C\n" +
        "[V:1] " + (upper ? pitch : "x") + " |]\n[V:2] " + (upper ? "x" : pitch) + " |]\n"
    }
    return "X:1\nM:none\nL:1\nK:C clef=" + card.clef + "\n" + pitch + " |]\n"
  }

  function buildFlashcards(root) {
    const saved = store("flashcards", {})
    const state = {
      sets: Array.isArray(saved.sets) && saved.sets.length ? saved.sets : ["treble-cg"],
      mode: saved.mode === "piano" ? "piano" : "letters",
      play: !!saved.play,
      boxes: saved.boxes && typeof saved.boxes === "object" ? saved.boxes : {},
    }
    const persist = () => save("flashcards", state)

    let deck = []
    let card = null
    let lastId = null
    let pending = []
    let locked = false
    let t0 = 0
    let kbStart = 3

    const stats = makeStats(3)
    const boxLine = h("p", { class: "mf-small" })
    const cardEl = h("div", { class: "mf-card", "aria-label": "Note on a staff" })
    const msg = h("div", { class: "mf-msg", "aria-live": "polite" })
    const nextBtn = btn("Next card", () => nextCard(), { class: "mf-tool-btn mf-next", hidden: true })
    const answerHost = h("div", {})
    const kbHost = h("div", {})

    // --- controls
    const setBox = h("div", { class: "mf-sets" })
    FC_SETS.forEach((set) => {
      setBox.appendChild(check(set.label, state.sets.includes(set.id), (on) => {
        state.sets = state.sets.filter((x) => x !== set.id)
        if (on) state.sets.push(set.id)
        if (!state.sets.length) { state.sets = [set.id]; renderSets() }
        persist()
        buildDeck()
        nextCard()
      }))
    })
    function renderSets() {
      setBox.querySelectorAll("input").forEach((input, i) => { input.checked = state.sets.includes(FC_SETS[i].id) })
    }
    const modeBtns = [
      ["letters", btn("Letter buttons", () => setMode("letters"), { "aria-pressed": "false" })],
      ["piano", btn("Piano keyboard", () => setMode("piano"), { "aria-pressed": "false" })],
    ]
    function setMode(m) {
      state.mode = m
      persist()
      setPressed(modeBtns, m)
      drawAnswerArea()
      if (card) startCard(card)
    }

    // --- deck
    function buildDeck() {
      deck = []
      const seen = {}
      state.sets.forEach((id) => {
        const set = FC_SETS.find((x) => x.id === id)
        if (!set) return
        set.notes.forEach((n) => {
          const clef = set.clef === "auto" ? (n.oct <= 3 ? "bass" : "treble") : set.clef
          const cid = clef + ":" + nameOf(n)
          if (!seen[cid]) {
            seen[cid] = true
            deck.push({ id: cid, note: n, clef: clef })
          }
        })
      })
      pending = []
      drawAnswerArea()
    }
    const boxOf = (c) => state.boxes[c.id] || 1

    function nextCard() {
      if (!deck.length) return
      pending.forEach((p) => p.wait--)
      let chosen = null
      const due = pending.find((p) => p.wait <= 0 && deck.some((c) => c.id === p.id))
      if (due) {
        chosen = deck.find((c) => c.id === due.id)
        pending = pending.filter((p) => p !== due)
      } else {
        const pool = deck.length > 1 ? deck.filter((c) => c.id !== lastId) : deck
        const weights = pool.map((c) => Math.pow(2, 5 - boxOf(c)))
        let r = Math.random() * weights.reduce((a, b) => a + b, 0)
        for (let i = 0; i < pool.length; i++) {
          r -= weights[i]
          if (r <= 0) { chosen = pool[i]; break }
        }
        chosen = chosen || pool[pool.length - 1]
      }
      startCard(chosen)
    }

    function startCard(c) {
      card = c
      lastId = c.id
      locked = false
      msg.textContent = ""
      msg.className = "mf-msg"
      nextBtn.hidden = true
      cardEl.textContent = ""
      try {
        ABCJS.renderAbc(cardEl, flashcardAbc(c), { staffwidth: c.clef === "grand" ? 170 : 150, scale: 1.7, paddingtop: 10, paddingbottom: 10, paddingleft: 5, paddingright: 5 })
      } catch (e) {
        cardEl.textContent = nameOf(c.note)
      }
      clearMarks()
      if (state.mode === "piano") showKeyboardRange()
      t0 = performance.now()
      paintBoxes()
    }

    function paintBoxes() {
      const n5 = deck.filter((c) => boxOf(c) >= 4).length
      boxLine.textContent = n5 + " of " + deck.length + " cards in these sets are in box 4 or 5 (nearly learned)."
    }

    // --- answering
    function finish(ok) {
      const secs = (performance.now() - t0) / 1000
      stats.add(ok, secs)
      state.boxes[card.id] = ok ? Math.min(5, boxOf(card) + 1) : 1
      persist()
      paintBoxes()
      locked = true
      const name = nameOf(card.note)
      if (state.play) playEvents([{ midis: [midiOf(card.note)], beats: 2 }], 90)
      if (ok) {
        msg.textContent = "Right: " + name
        msg.className = "mf-msg is-right"
        addTimer(() => nextCard(), 700)
      } else {
        msg.textContent = "That note is " + name
        msg.className = "mf-msg is-wrong"
        pending.push({ id: card.id, wait: 3 })
        nextBtn.hidden = false
        nextBtn.focus({ preventScroll: true })
      }
    }

    function clearMarks() {
      pad.clear()
      kbHost.querySelectorAll(".mf-key").forEach((k) => k.classList.remove("is-right", "is-wrong", "is-tapped"))
    }

    function answerLetter(L, acc) {
      if (locked || !card) return
      const n = card.note
      const ok = LETTERS[n.l] === L && n.acc === acc
      if (ok) {
        pad.letters[L].classList.add("is-right")
        if (n.acc && pad.accBtns.sharp) (n.acc > 0 ? pad.accBtns.sharp : pad.accBtns.flat).classList.add("is-right")
      } else {
        pad.letters[L].classList.add("is-tapped")
        const right = pad.letters[LETTERS[n.l]]
        right.classList.add("is-wrong")
        if (n.acc && pad.accBtns.sharp) (n.acc > 0 ? pad.accBtns.sharp : pad.accBtns.flat).classList.add("is-wrong")
      }
      finish(ok)
    }

    function answerKey(midi) {
      if (locked || !card) return
      const ok = midi === midiOf(card.note)
      const keyEl = (m) => kbHost.querySelector('.mf-key[data-midi="' + m + '"]')
      const tapped = keyEl(midi)
      if (ok) {
        tapped && tapped.classList.add("is-right")
      } else {
        tapped && tapped.classList.add("is-tapped")
        const right = keyEl(midiOf(card.note))
        right && right.classList.add("is-wrong")
      }
      finish(ok)
    }

    // --- answer area
    let pad = letterPad(false, answerLetter)
    function drawAnswerArea() {
      answerHost.textContent = ""
      kbHost.textContent = ""
      if (state.mode === "letters") {
        pad = letterPad(state.sets.includes("black"), answerLetter)
        answerHost.appendChild(pad.el)
      } else {
        pad = letterPad(false, answerLetter)
        drawKeyboard()
      }
    }
    function keyboardVisible(midi) {
      return midi >= 12 * (kbStart + 1) && midi <= 12 * (kbStart + 3)
    }
    function showKeyboardRange() {
      const m = midiOf(card.note)
      if (!keyboardVisible(m)) {
        kbStart = Math.max(1, Math.min(5, card.note.oct - 1))
        drawKeyboard()
      }
    }
    function drawKeyboard() {
      kbHost.textContent = ""
      kbHost.appendChild(makeKeyboard(kbStart, answerKey, true))
      const shift = (d) => {
        kbStart = Math.max(1, Math.min(5, kbStart + d))
        drawKeyboard()
      }
      kbHost.appendChild(h("div", { class: "mf-tool-row mf-two" }, [
        btn("Lower octave", () => shift(-1)),
        btn("Higher octave", () => shift(1)),
      ]))
    }

    // --- assemble
    root.appendChild(h("div", { class: "mf-tool-group" }, [h("strong", { text: "Card sets" }), setBox]))
    root.appendChild(h("div", { class: "mf-tool-row mf-two" }, modeBtns.map((m) => m[1])))
    root.appendChild(h("div", { class: "mf-tool-row" }, [
      toggle("Play the note after each answer", state.play, (on) => { state.play = on; persist() }),
    ]))
    root.appendChild(cardEl)
    root.appendChild(msg)
    root.appendChild(nextBtn)
    root.appendChild(answerHost)
    root.appendChild(kbHost)
    root.appendChild(stats.el)
    root.appendChild(h("p", { class: "mf-small", text: "Aim for under 3 seconds per card. The average turns teal when you are under 3 seconds." }))
    root.appendChild(boxLine)
    root.appendChild(h("div", { class: "mf-tool-row" }, [
      resetButton("Reset boxes and score", () => {
        state.boxes = {}
        persist()
        stats.reset()
        pending = []
        nextCard()
      }),
    ]))
    root.appendChild(h("p", { class: "mf-small", text: "Keyboard: press A to G to answer. For sharps and flats, press # or - first, then the letter. Press Enter for the next card." }))

    onKey((e) => {
      const k = e.key
      if (k === "Enter") {
        if (!nextBtn.hidden) { e.preventDefault(); nextCard() }
        return
      }
      if (k === "#") { pad.latchKey(1); return }
      if (k === "-") { pad.latchKey(-1); return }
      if (state.mode !== "letters") return
      const L = k.length === 1 ? k.toUpperCase() : ""
      if (/^[A-G]$/.test(L)) {
        e.preventDefault()
        pad.letters[L].click()
      }
    })

    setPressed(modeBtns, state.mode)
    buildDeck()
    nextCard()
  }

  // An SVG piano: two octaves from C(startOct) plus the next C.
  function makeKeyboard(startOct, onTap, labelCs) {
    const W = 24
    const whites = 15
    const H = 140
    const svg = s("svg", { class: "mf-kb", viewBox: "0 0 " + whites * W + " " + H, role: "group", "aria-label": "Piano keyboard, tap a key" })
    const whiteMidi = []
    for (let i = 0; i < whites; i++) {
      const octave = startOct + Math.floor(i / 7)
      whiteMidi.push(12 * (octave + 1) + SEMI[i % 7])
    }
    whiteMidi.forEach((m, i) => {
      const r = s("rect", { class: "mf-key", x: i * W, y: 0, width: W, height: H, "data-midi": m })
      r.addEventListener("click", () => onTap(m))
      svg.appendChild(r)
    })
    whiteMidi.forEach((m, i) => {
      if (labelCs && i % 7 === 0) {
        svg.appendChild(s("text", { class: "mf-key-label", x: i * W + W / 2, y: H - 8, "text-anchor": "middle", text: "C" + (startOct + i / 7) }))
      }
    })
    const bw = 15
    whiteMidi.forEach((m, i) => {
      if (i >= whites - 1) return
      const pc = i % 7
      if (pc === 2 || pc === 6) return
      const r = s("rect", { class: "mf-key black", x: (i + 1) * W - bw / 2, y: 0, width: bw, height: 86, "data-midi": m + 1 })
      r.addEventListener("click", () => onTap(m + 1))
      svg.appendChild(r)
    })
    return svg
  }

  // ---------- B. reading drill ----------

  const KEY_SIGS = { C: {}, G: { 3: 1 }, F: { 6: -1 } } // letter index (F = 3, B = 6) to accidental
  const KEY_TONIC = { C: 0, G: 4, F: 3 }

  const DRILL_LEVELS = [
    { id: 1, label: "1. C position, right hand", pickKey: () => ({ key: "C", lo: "C4", hi: "G4", tonicOct: 4 }), clefs: ["treble"], leap: 0 },
    { id: 2, label: "2. C position, left hand", pickKey: () => ({ key: "C", lo: "C3", hi: "G3", tonicOct: 3 }), clefs: ["bass"], leap: 0 },
    { id: 3, label: "3. G position", pickKey: () => ({ key: "C", lo: "G4", hi: "D5", tonicOct: 4, tonicL: 4 }), clefs: ["treble"], leap: 0 },
    { id: 4, label: "4. Both hands on a grand staff", grand: true, clefs: ["treble", "bass"] },
    {
      id: 5, label: "5. Key of G or F",
      pickKey: () => pick([{ key: "G", lo: "D4", hi: "D5", tonicOct: 4 }, { key: "F", lo: "C4", hi: "C5", tonicOct: 4 }]),
      clefs: ["treble"], leap: 0.05,
    },
    {
      id: 6, label: "6. Wider range, with leaps",
      pickKey: () => pick([{ key: "C", lo: "C4", hi: "G5", tonicOct: 4 }, { key: "G", lo: "C4", hi: "G5", tonicOct: 4 }, { key: "F", lo: "C4", hi: "G5", tonicOct: 4 }]),
      clefs: ["treble"], leap: 0.3,
    },
  ]

  const RHYTHMS = [[1, 1, 1, 1], [2, 1, 1], [1, 2, 1], [1, 1, 2], [2, 2]]
  const END_RHYTHMS = [[2, 2], [1, 1, 2], [2, 2]]

  // Returns [[{d, len}, ...] per bar]. d is a diatonic index (octave * 7 + letter).
  function makeLine(loD, hiD, tonicL, leap) {
    const bars = [pick(RHYTHMS), pick(RHYTHMS), pick(RHYTHMS), pick(END_RHYTHMS)]
    const total = bars.reduce((a, b) => a + b.length, 0)
    const tonics = []
    for (let d = loD; d <= hiD; d++) if (((d % 7) + 7) % 7 === tonicL) tonics.push(d)
    const chordTones = []
    for (let d = loD; d <= hiD; d++) if ([0, 2, 4].includes((((d - tonicL) % 7) + 7) % 7)) chordTones.push(d)
    const seq = [pick(chordTones.length ? chordTones : tonics)]
    let dir = rand(2) ? 1 : -1
    for (let i = 1; i < total - 2; i++) {
      const prev = seq[i - 1]
      const r = Math.random()
      let step
      if (r < 0.58) step = 1
      else if (r < 0.8) step = 2
      else if (r < 0.9) step = 0
      else step = leap ? 3 + rand(3) : 1
      if (leap && Math.random() < leap) step = 3 + rand(3)
      if (Math.random() < 0.3) dir = -dir
      let next = prev + dir * step
      if (next < loD || next > hiD) { dir = -dir; next = prev + dir * step }
      if (next < loD || next > hiD) next = prev
      if (i >= 3 && prev === seq[i - 2] && prev === seq[i - 3] && next === prev) next = prev + (prev < hiD ? 1 : -1)
      seq.push(next)
    }
    // Last note is the tonic nearest the note before the ending; the one before steps into it.
    const ref = seq[seq.length - 1]
    let target = tonics[0]
    tonics.forEach((t) => { if (Math.abs(t - ref) < Math.abs(target - ref)) target = t })
    const approach = [target - 1, target + 1].filter((d) => d >= loD && d <= hiD)
    approach.sort((a, b) => Math.abs(a - ref) - Math.abs(b - ref))
    if (total >= 3) seq.push(approach[0] === undefined ? target : approach[0])
    seq.push(target)
    let k = 0
    return bars.map((b) => b.map((len) => ({ d: seq[k++], len: len })))
  }

  // A left hand part for the grand staff: half notes, then a whole note on the tonic.
  function makeBass(loD, hiD, tonicD) {
    const out = []
    let cur = tonicD
    for (let bar = 0; bar < 3; bar++) {
      const notes = []
      for (let i = 0; i < 2; i++) {
        if (bar > 0 || i > 0) {
          const step = pick([-2, -1, -1, 1, 1, 2, 0])
          cur = Math.max(loD, Math.min(hiD, cur + step))
        }
        notes.push({ d: cur, len: 2 })
      }
      out.push(notes)
    }
    out.push([{ d: tonicD, len: 4 }])
    return out
  }

  function barsToAbc(bars) {
    return bars.map((bar) => bar.map((n) => abcPitch(fromDia(n.d), false) + (n.len === 1 ? "" : n.len)).join(" ")).join(" | ") + " |]"
  }
  function barsToNames(bars, key) {
    const sig = KEY_SIGS[key]
    return bars.map((bar) => bar.map((n) => {
      const l = ((n.d % 7) + 7) % 7
      const a = sig[l] || 0
      return LETTERS[l] + (a > 0 ? "#" : a < 0 ? "b" : "")
    }).join(" ")).join(" ")
  }

  function buildReadingDrill(root) {
    const saved = store("reading", {})
    let level = DRILL_LEVELS.find((l) => l.id === Number(saved.level)) || DRILL_LEVELS[0]
    let names = false
    let melody = null

    const box = h("div", { class: "mf-music mf-drill" })
    const paper = h("div", { class: "mf-paper" })
    const bar = h("div", { class: "mf-audio" })
    box.appendChild(paper)
    box.appendChild(bar)

    let synth = null
    function initSynth() {
      if (!audioOk()) return
      synth = new ABCJS.synth.SynthController()
      let lit = []
      const clear = () => { lit.forEach((el) => el.classList.remove("mf-playing")); lit = [] }
      synth.load(bar, {
        onStart: clear,
        onFinished: clear,
        onEvent(ev) {
          clear()
          if (!ev || !ev.elements) return
          ev.elements.forEach((g) => g.forEach((el) => { el.classList.add("mf-playing"); lit.push(el) }))
        },
      }, { displayLoop: true, displayRestart: true, displayPlay: true, displayProgress: true, displayWarp: true })
      controllers.push(synth)
    }

    function generate() {
      if (level.grand) {
        const rh = makeLine(diaOf(parseNote("C4")), diaOf(parseNote("G4")), 0, 0)
        const lo = diaOf(parseNote("C3"))
        const lh = makeBass(lo, diaOf(parseNote("G3")), lo)
        return { key: "C", voices: [{ clef: "treble", bars: rh }, { clef: "bass", bars: lh }] }
      }
      const p = level.pickKey()
      const tonicL = p.tonicL !== undefined ? p.tonicL : KEY_TONIC[p.key]
      const bars = makeLine(diaOf(parseNote(p.lo)), diaOf(parseNote(p.hi)), tonicL, level.leap)
      return { key: p.key, voices: [{ clef: level.clefs[0], bars: bars }] }
    }

    function draw() {
      let abc = "X:1\nM:4/4\nL:1/4\nQ:1/4=70\n"
      if (melody.voices.length === 2) {
        abc += "%%score {1 2}\nV:1 clef=treble\nV:2 clef=bass\nK:" + melody.key + "\n"
        melody.voices.forEach((v, i) => {
          abc += "[V:" + (i + 1) + "] " + barsToAbc(v.bars) + "\n"
          if (names) abc += "w: " + barsToNames(v.bars, melody.key) + "\n"
        })
      } else {
        const v = melody.voices[0]
        abc += "K:" + melody.key + " clef=" + v.clef + "\n" + barsToAbc(v.bars) + "\n"
        if (names) abc += "w: " + barsToNames(v.bars, melody.key) + "\n"
      }
      if (synth) { try { synth.pause() } catch (e) { /* not playing */ } }
      paper.textContent = ""
      let tune
      try {
        tune = ABCJS.renderAbc(paper, abc, { responsive: "resize", staffwidth: 400, wrap: { minSpacing: 1.6, maxSpacing: 2.8, preferredMeasuresPerLine: 2 }, paddingleft: 0, paddingright: 0, paddingtop: 8, paddingbottom: 8 })[0]
      } catch (e) {
        paper.textContent = "This melody could not be drawn."
        return
      }
      if (synth) {
        synth.setTune(tune, false, { program: 0, soundFontUrl: SOUNDFONT, soundFontVolumeMultiplier: 3.0, chordsOff: true })
          .catch(() => { bar.textContent = "Audio could not start in this browser." })
      }
    }

    function newMelody() {
      melody = generate()
      draw()
    }

    root.appendChild(h("div", { class: "mf-tool-row" }, [
      field("Level", select(DRILL_LEVELS.map((l) => [l.id, l.label]), level.id, (v) => {
        level = DRILL_LEVELS.find((l) => l.id === Number(v))
        save("reading", { level: level.id })
        newMelody()
      })),
    ]))
    root.appendChild(h("div", { class: "mf-tool-row mf-two" }, [
      btn("New melody", newMelody),
      toggle("Show note names", false, (on) => { names = on; draw() }),
    ]))
    root.appendChild(box)
    initSynth()
    root.appendChild(h("p", { class: "mf-small", text: "Read it first, then press play to check. The tempo slider changes the speed. Press play and play along." }))
    newMelody()
  }

  // ---------- C. fretboard drill ----------

  const OPEN_MIDI = [64, 59, 55, 50, 45, 40] // strings 1 to 6
  const NATURAL_PC = [0, 2, 4, 5, 7, 9, 11]

  function stringsPhrase(list) {
    const l = list.slice().sort((a, b) => b - a)
    if (l.length === 1) return "string " + l[0]
    return "strings " + l.slice(0, -1).join(", ") + " and " + l[l.length - 1]
  }

  function buildFretboard(root) {
    const saved = store("fretboard", {})
    const cfg = {
      mode: saved.mode === "find" ? "find" : "name",
      strings: Array.isArray(saved.strings) && saved.strings.length ? saved.strings : [6, 5],
      lo: Number.isInteger(saved.lo) ? saved.lo : 0,
      hi: Number.isInteger(saved.hi) ? saved.hi : 12,
      sharps: !!saved.sharps,
    }
    const persist = () => save("fretboard", cfg)
    const stats = makeStats(5)

    // --- the board
    const FW = 40
    const X0 = 56
    const YS = 28
    const Y0 = 26
    const W = X0 + 12 * FW + 16
    const H = Y0 + 5 * YS + 40
    const xOf = (f) => (f === 0 ? X0 - 22 : X0 + (f - 0.5) * FW)
    const yOf = (str) => Y0 + (str - 1) * YS
    const svg = s("svg", { class: "mf-fretboard-svg", viewBox: "0 0 " + W + " " + H, role: "group", "aria-label": "Guitar fretboard, string 1 on top" })
    svg.appendChild(s("rect", { x: X0, y: Y0 - 10, width: 12 * FW, height: 5 * YS + 20, class: "mf-fb-wood" }))
    for (let f = 1; f <= 12; f++) {
      if ([3, 5, 7, 9].includes(f)) svg.appendChild(s("circle", { cx: xOf(f), cy: Y0 + 2.5 * YS, r: 6, class: "mf-fb-inlay" }))
      if (f === 12) {
        svg.appendChild(s("circle", { cx: xOf(f), cy: Y0 + 1.5 * YS, r: 6, class: "mf-fb-inlay" }))
        svg.appendChild(s("circle", { cx: xOf(f), cy: Y0 + 3.5 * YS, r: 6, class: "mf-fb-inlay" }))
      }
      svg.appendChild(s("line", { x1: X0 + f * FW, y1: Y0 - 10, x2: X0 + f * FW, y2: Y0 + 5 * YS + 10, class: "mf-fb-fret" }))
      svg.appendChild(s("text", { x: xOf(f), y: H - 8, "text-anchor": "middle", class: "mf-fb-num", text: f }))
    }
    svg.appendChild(s("line", { x1: X0, y1: Y0 - 10, x2: X0, y2: Y0 + 5 * YS + 10, class: "mf-fb-nut" }))
    svg.appendChild(s("text", { x: xOf(0), y: H - 8, "text-anchor": "middle", class: "mf-fb-num", text: "0" }))
    for (let str = 1; str <= 6; str++) {
      svg.appendChild(s("line", { x1: X0 - 44, y1: yOf(str), x2: X0 + 12 * FW, y2: yOf(str), class: "mf-fb-string", "stroke-width": 1 + str * 0.5 }))
      svg.appendChild(s("text", { x: 8, y: yOf(str) + 5, class: "mf-fb-num", text: str }))
    }
    const dotLayer = s("g", {})
    const hitLayer = s("g", {})
    svg.appendChild(dotLayer)
    svg.appendChild(hitLayer)
    const midiAt = (str, f) => OPEN_MIDI[str - 1] + f

    function dot(str, f, cls, label) {
      const g = s("g", { class: "mf-fb-dot " + cls }, [
        s("circle", { cx: xOf(f), cy: yOf(str), r: 12 }),
        s("text", { x: xOf(f), y: yOf(str) + 5, "text-anchor": "middle", text: label }),
      ])
      dotLayer.appendChild(g)
      return g
    }

    // --- state
    let q = null
    let locked = false
    let t0 = 0
    let lastKey = ""
    const msg = h("div", { class: "mf-msg", "aria-live": "polite" })
    const prompt = h("p", { class: "mf-prompt" })
    const nextBtn = btn("Next", () => nextQuestion(), { class: "mf-tool-btn mf-next", hidden: true })
    const showBtn = btn("Show the rest", () => revealRest(), { hidden: true })
    const padHost = h("div", {})
    let pad = null

    function pool() {
      const out = []
      cfg.strings.forEach((str) => {
        for (let f = cfg.lo; f <= cfg.hi; f++) {
          const pc = midiAt(str, f) % 12
          if (cfg.sharps || NATURAL_PC.includes(pc)) out.push({ str: str, fret: f, pc: pc })
        }
      })
      return out
    }
    const pcName = (pc) => SHARP_NAMES[pc]

    function nextQuestion() {
      msg.textContent = ""
      msg.className = "mf-msg"
      nextBtn.hidden = true
      showBtn.hidden = true
      locked = false
      dotLayer.textContent = ""
      hitLayer.textContent = ""
      const p = pool()
      if (!p.length) {
        prompt.textContent = "No notes in this range. Tick more strings or widen the frets."
        q = null
        return
      }
      if (cfg.mode === "name") {
        let spot
        for (let tries = 0; tries < 20; tries++) {
          spot = pick(p)
          if (spot.str + ":" + spot.fret !== lastKey || p.length === 1) break
        }
        lastKey = spot.str + ":" + spot.fret
        q = { spot: spot }
        prompt.textContent = "Which note is the dot?"
        dot(spot.str, spot.fret, "is-ask", "?")
      } else {
        const pcs = Array.from(new Set(p.map((x) => x.pc)))
        let pc
        for (let tries = 0; tries < 20; tries++) {
          pc = pick(pcs)
          if (String(pc) !== lastKey || pcs.length === 1) break
        }
        lastKey = String(pc)
        const targets = p.filter((x) => x.pc === pc)
        q = { pc: pc, targets: targets, found: {}, misses: 0 }
        prompt.textContent = "Find every " + pcName(pc) + " on " + stringsPhrase(cfg.strings) + " from fret " + cfg.lo + " to " + cfg.hi + ". Tap the board. (" + targets.length + " to find)"
        cfg.strings.forEach((str) => {
          for (let f = cfg.lo; f <= cfg.hi; f++) {
            const r = s("rect", { x: xOf(f) - (f === 0 ? 18 : FW / 2), y: yOf(str) - YS / 2, width: f === 0 ? 36 : FW, height: YS, class: "mf-fb-hit" })
            r.addEventListener("click", () => tapSpot(str, f))
            hitLayer.appendChild(r)
          }
        })
        showBtn.hidden = false
      }
      t0 = performance.now()
    }

    function tapSpot(str, f) {
      if (locked || !q || cfg.mode !== "find") return
      const key = str + ":" + f
      if (q.found[key]) return
      const isTarget = q.targets.some((x) => x.str === str && x.fret === f)
      if (isTarget) {
        q.found[key] = true
        dot(str, f, "is-right", pcName(q.pc))
        stats.add(true)
        if (Object.keys(q.found).length === q.targets.length) {
          const secs = (performance.now() - t0) / 1000
          stats.time(secs)
          locked = true
          msg.textContent = "Found all " + q.targets.length + " in " + secs.toFixed(0) + " s"
          msg.className = "mf-msg is-right"
          showBtn.hidden = true
          nextBtn.hidden = false
          nextBtn.focus({ preventScroll: true })
        }
      } else {
        stats.add(false)
        const g = dot(str, f, "is-wrong", pcName(midiAt(str, f) % 12))
        addTimer(() => g.remove(), 900)
      }
    }

    function revealRest() {
      if (!q || cfg.mode !== "find" || locked) return
      q.targets.forEach((x) => {
        if (!q.found[x.str + ":" + x.fret]) dot(x.str, x.fret, "is-wrong", pcName(q.pc))
      })
      locked = true
      showBtn.hidden = true
      nextBtn.hidden = false
      nextBtn.focus({ preventScroll: true })
    }

    function answerName(L, acc) {
      if (locked || !q || cfg.mode !== "name") return
      const secs = (performance.now() - t0) / 1000
      const guessPc = (SEMI[LETTERS.indexOf(L)] + acc + 12) % 12
      const ok = guessPc === q.spot.pc
      dotLayer.textContent = ""
      const label = pcName(q.spot.pc)
      dot(q.spot.str, q.spot.fret, ok ? "is-right" : "is-wrong", label)
      stats.add(ok, secs)
      locked = true
      if (ok) {
        msg.textContent = "Right: " + label
        msg.className = "mf-msg is-right"
        addTimer(() => nextQuestion(), 700)
      } else {
        msg.textContent = "That note is " + label
        msg.className = "mf-msg is-wrong"
        nextBtn.hidden = false
        nextBtn.focus({ preventScroll: true })
      }
    }

    function drawPad() {
      padHost.textContent = ""
      pad = letterPad(cfg.sharps, answerName)
      padHost.hidden = cfg.mode !== "name"
      padHost.appendChild(pad.el)
    }

    // --- controls
    const modeBtns = [
      ["name", btn("Name the note", () => setMode("name"), { "aria-pressed": "false" })],
      ["find", btn("Find the note", () => setMode("find"), { "aria-pressed": "false" })],
    ]
    function setMode(m) {
      cfg.mode = m
      persist()
      setPressed(modeBtns, m)
      drawPad()
      nextQuestion()
    }
    const stringBox = h("div", { class: "mf-sets mf-strings" })
    for (let str = 1; str <= 6; str++) {
      stringBox.appendChild(check("String " + str, cfg.strings.includes(str), (on) => {
        cfg.strings = cfg.strings.filter((x) => x !== str)
        if (on) cfg.strings.push(str)
        persist()
        nextQuestion()
      }))
    }
    const fretOptions = []
    for (let f = 0; f <= 12; f++) fretOptions.push([f, String(f)])
    const loSel = select(fretOptions, cfg.lo, (v) => {
      cfg.lo = Number(v)
      if (cfg.hi < cfg.lo) { cfg.hi = cfg.lo; hiSel.value = String(cfg.hi) }
      persist(); nextQuestion()
    })
    const hiSel = select(fretOptions, cfg.hi, (v) => {
      cfg.hi = Number(v)
      if (cfg.lo > cfg.hi) { cfg.lo = cfg.hi; loSel.value = String(cfg.lo) }
      persist(); nextQuestion()
    })

    root.appendChild(h("div", { class: "mf-tool-row mf-two" }, modeBtns.map((m) => m[1])))
    root.appendChild(h("div", { class: "mf-tool-group" }, [h("strong", { text: "Strings" }), stringBox]))
    root.appendChild(h("div", { class: "mf-tool-row" }, [
      field("From fret", loSel),
      field("To fret", hiSel),
      check("Include sharps", cfg.sharps, (on) => { cfg.sharps = on; persist(); drawPad(); nextQuestion() }),
    ]))
    root.appendChild(prompt)
    root.appendChild(h("div", { class: "mf-fretboard" }, [svg]))
    root.appendChild(msg)
    root.appendChild(h("div", { class: "mf-tool-row" }, [showBtn, nextBtn]))
    root.appendChild(padHost)
    root.appendChild(stats.el)
    root.appendChild(h("div", { class: "mf-tool-row" }, [resetButton("Reset score", () => { stats.reset(); nextQuestion() })]))
    root.appendChild(h("p", { class: "mf-small", text: "String 1 is the thinnest string, on top, as in tab. In standard tuning the open strings are E2 A2 D3 G3 B3 E4. Keyboard: press A to G to answer, # to add a sharp, Enter for the next one." }))

    onKey((e) => {
      if (e.key === "Enter") {
        if (!nextBtn.hidden) { e.preventDefault(); nextQuestion() }
        return
      }
      if (e.key === "#") { pad && pad.latchKey(1); return }
      if (cfg.mode !== "name" || !pad) return
      const L = e.key.length === 1 ? e.key.toUpperCase() : ""
      if (/^[A-G]$/.test(L)) { e.preventDefault(); pad.letters[L].click() }
    })

    setPressed(modeBtns, cfg.mode)
    drawPad()
    nextQuestion()
  }

  // ---------- D and E. ear quizzes ----------

  const INTERVALS = [
    { id: 1, name: "minor 2nd" }, { id: 2, name: "major 2nd" },
    { id: 3, name: "minor 3rd" }, { id: 4, name: "major 3rd" },
    { id: 5, name: "perfect 4th" }, { id: 6, name: "tritone" },
    { id: 7, name: "perfect 5th" }, { id: 8, name: "minor 6th" },
    { id: 9, name: "major 6th" }, { id: 10, name: "minor 7th" },
    { id: 11, name: "major 7th" }, { id: 12, name: "octave" },
  ]
  const INTERVAL_LEVELS = {
    1: [2, 4, 7, 12],
    2: [1, 2, 3, 4, 5, 7, 12],
    3: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
  }
  const CHORDS = [
    { id: "major", name: "major", steps: [0, 4, 7] },
    { id: "minor", name: "minor", steps: [0, 3, 7] },
    { id: "dim", name: "diminished", steps: [0, 3, 6] },
    { id: "aug", name: "augmented", steps: [0, 4, 8] },
    { id: "maj7", name: "major 7", steps: [0, 4, 7, 11] },
    { id: "dom7", name: "dominant 7", steps: [0, 4, 7, 10] },
    { id: "min7", name: "minor 7", steps: [0, 3, 7, 10] },
  ]
  const CHORD_LEVELS = { 1: ["major", "minor"], 2: ["major", "minor", "dim", "aug"], 3: ["major", "minor", "dim", "aug", "maj7", "dom7", "min7"] }

  function buildEarQuiz(root, cfg) {
    const saved = store(cfg.id, {})
    let level = [1, 2, 3].includes(saved.level) ? saved.level : 1
    let mode = cfg.modes.some((m) => m[0] === saved.mode) ? saved.mode : cfg.modes[0][0]
    const totals = saved.totals && typeof saved.totals === "object" ? saved.totals : {}
    const persist = () => save(cfg.id, { level: level, mode: mode, totals: totals })

    const stats = makeStats(0)
    let q = null
    let locked = true
    let t0 = 0
    const msg = h("div", { class: "mf-msg", "aria-live": "polite" })
    const grid = h("div", { class: "mf-choices" })
    const playBtn = btn("Play", () => startOrReplay(), { class: "mf-tool-btn mf-play" })
    const nextBtn = btn("Next question", () => newQuestion(true), { class: "mf-tool-btn mf-next", hidden: true })
    const allTime = h("p", { class: "mf-small" })

    function paintAllTime() {
      let r = 0
      let t = 0
      Object.values(totals).forEach((v) => { r += v[0]; t += v[1] })
      allTime.textContent = t ? "All time on this device: " + r + " right out of " + t + " (" + Math.round((100 * r) / t) + "%)." : ""
    }

    function drawChoices() {
      grid.textContent = ""
      cfg.choices(level).forEach((c) => {
        const b = btn(c.name, () => answer(c.id), { "data-id": String(c.id) })
        grid.appendChild(b)
      })
    }

    function newQuestion(autoplay) {
      q = cfg.make(level, mode)
      locked = false
      msg.textContent = ""
      msg.className = "mf-msg"
      nextBtn.hidden = true
      grid.querySelectorAll("button").forEach((b) => b.classList.remove("is-right", "is-wrong", "is-tapped"))
      playBtn.textContent = "Play again"
      if (autoplay) play()
      t0 = performance.now()
    }

    function play() {
      if (!q) return
      playEvents(cfg.events(q, mode), cfg.bpm).then((ok) => {
        if (!ok && !audioOk()) msg.textContent = "This browser cannot play sound."
      })
    }
    function startOrReplay() {
      if (!q) newQuestion(true)
      else play()
    }

    function answer(id) {
      if (locked || !q) return
      const secs = (performance.now() - t0) / 1000
      const ok = String(id) === String(q.answer)
      const key = String(q.answer)
      totals[key] = totals[key] || [0, 0]
      totals[key][1]++
      if (ok) totals[key][0]++
      persist()
      paintAllTime()
      locked = true
      stats.add(ok, secs)
      const rightBtn = grid.querySelector('[data-id="' + q.answer + '"]')
      if (ok) {
        rightBtn.classList.add("is-right")
        msg.textContent = "Right: " + q.label
        msg.className = "mf-msg is-right"
        addTimer(() => newQuestion(true), 1100)
      } else {
        const tapped = grid.querySelector('[data-id="' + id + '"]')
        tapped && tapped.classList.add("is-tapped")
        rightBtn.classList.add("is-wrong")
        msg.textContent = "The answer is " + q.label
        msg.className = "mf-msg is-wrong"
        nextBtn.hidden = false
        nextBtn.focus({ preventScroll: true })
      }
    }

    const levelSel = select(cfg.levelLabels.map((l, i) => [i + 1, l]), level, (v) => {
      level = Number(v)
      persist()
      q = null
      locked = true
      stopAudio()
      msg.textContent = ""
      nextBtn.hidden = true
      playBtn.textContent = "Play"
      drawChoices()
    })
    const modeSel = select(cfg.modes, mode, (v) => { mode = v; persist(); if (q && !locked) play() })

    root.appendChild(h("div", { class: "mf-tool-row" }, [field("Level", levelSel), field(cfg.modeLabel, modeSel)]))
    root.appendChild(h("div", { class: "mf-tool-row" }, [playBtn]))
    root.appendChild(msg)
    root.appendChild(grid)
    root.appendChild(h("div", { class: "mf-tool-row" }, [nextBtn]))
    root.appendChild(stats.el)
    root.appendChild(allTime)
    root.appendChild(h("div", { class: "mf-tool-row" }, [resetButton("Reset score", () => { stats.reset() })]))
    root.appendChild(h("p", { class: "mf-small", text: "Sound starts when you tap Play. If you hear nothing, check the volume and that the silent switch on a phone is off." }))
    drawChoices()
    paintAllTime()
    onKey((e) => {
      if (e.key === "Enter" && !nextBtn.hidden) { e.preventDefault(); newQuestion(true) }
      else if (e.key === "r" || e.key === "R") { if (q) play() }
    })
  }

  function buildIntervalQuiz(root) {
    buildEarQuiz(root, {
      id: "intervals",
      levelLabels: ["Level 1: 2nd, 3rd, 5th, octave", "Level 2: adds minor 2nd, minor 3rd, 4th", "Level 3: adds 6ths, 7ths, tritone"],
      modeLabel: "Notes",
      modes: [["up", "Going up"], ["down", "Going down"], ["both", "Together (harmonic)"]],
      bpm: 72,
      choices: (level) => INTERVALS.filter((i) => INTERVAL_LEVELS[level].includes(i.id)).map((i) => ({ id: i.id, name: i.name })),
      make(level) {
        const ivId = pick(INTERVAL_LEVELS[level])
        const iv = INTERVALS.find((i) => i.id === ivId)
        const low = 53 + rand(17) // F3 to A4
        return { answer: iv.id, low: low, semis: iv.id, label: iv.name + " (" + nameOf(midiToNote(low)) + " and " + nameOf(midiToNote(low + iv.id)) + ")" }
      },
      events(q, mode) {
        const a = q.low
        const b = q.low + q.semis
        if (mode === "both") return [{ midis: [a, b], beats: 4 }]
        return mode === "down" ? [{ midis: [b], beats: 2 }, { midis: [a], beats: 3 }] : [{ midis: [a], beats: 2 }, { midis: [b], beats: 3 }]
      },
    })
  }

  function buildChordQuiz(root) {
    buildEarQuiz(root, {
      id: "chords",
      levelLabels: ["Level 1: major or minor", "Level 2: adds diminished and augmented", "Level 3: adds 7th chords"],
      modeLabel: "Played",
      modes: [["block", "Block (together)"], ["broken", "Broken (one by one)"]],
      bpm: 80,
      choices: (level) => CHORDS.filter((c) => CHORD_LEVELS[level].includes(c.id)).map((c) => ({ id: c.id, name: c.name })),
      make(level) {
        const chId = pick(CHORD_LEVELS[level])
        const ch = CHORDS.find((c) => c.id === chId)
        const base = 48 + rand(13) // C3 to C4
        const names = ch.steps.map((st) => nameOf(midiToNote(base + st)))
        return { answer: ch.id, root: base, steps: ch.steps, label: ch.name + " chord (" + names.join(" ") + ")" }
      },
      events(q, mode) {
        const notes = q.steps.map((st) => q.root + st)
        if (mode === "broken") return notes.map((m, i) => ({ midis: [m], beats: i === notes.length - 1 ? 3 : 1 }))
        return [{ midis: notes, beats: 4 }]
      },
    })
  }

  // ---------- start up ----------

  const TOOLS = {
    flashcards: buildFlashcards,
    "reading-drill": buildReadingDrill,
    fretboard: buildFretboard,
    intervals: buildIntervalQuiz,
    chords: buildChordQuiz,
  }

  let built = []

  document$.subscribe(() => {
    // Instant navigation swaps the page without a reload. If the tools on screen
    // are gone, stop their sound, timers and key handlers. If they are still
    // there (a jump to a heading on the same page), leave them running.
    if (!built.length || built.some((el) => !el.isConnected)) {
      stopAudio()
      controllers = []
      cleanups.forEach((fn) => { try { fn() } catch (e) { /* ignore */ } })
      cleanups = []
      built = []
    }
    document.querySelectorAll(".mf-tool[data-tool]").forEach((el) => {
      const build = TOOLS[el.getAttribute("data-tool")]
      if (!build || el.dataset.built) return
      el.dataset.built = "1"
      el.textContent = ""
      built.push(el)
      try {
        build(el)
      } catch (e) {
        el.textContent = "This practice tool could not start in this browser."
      }
    })
  })
})()
