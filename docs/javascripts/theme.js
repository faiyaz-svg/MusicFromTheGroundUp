// Give every page a stage colour. Pages under /01-.../ get colour 1, /02-.../
// colour 2, and so on, cycling every 5 (yellow, salmon, lavender, teal, blue).
// Start-here, practice tools and reference pages get no stage, so they stay grey.
// The colours themselves are in stylesheets/site.css (body[data-stage]).
document$.subscribe(() => {
  const parts = location.pathname.split("/")
  let stage = ""
  for (const part of parts) {
    const m = /^(\d{2})-/.exec(part)
    if (m) {
      const n = Number(m[1])
      if (n >= 1 && n <= 13) stage = String(((n - 1) % 5) + 1)
      break
    }
  }
  if (stage) document.body.setAttribute("data-stage", stage)
  else document.body.removeAttribute("data-stage")
})
