from _common import *

F = FOLDER + "/chord-symbols-and-chord-charts-"
save(chart_svg(["Am", "%", "Dm", "%", "E7", [(0, "Am"), (2, "E7")], "Am", "Am"],
               "A chord chart in A minor: eight bars, a repeat sign at each end, one chord per bar, a repeat-bar sign, and one bar with two chords",
               start_repeat=True, end_repeat=True,
               caption="Each slash is one beat. The sign in bar 2 means play bar 1 again."), F + "chart.svg")
save(chart_svg(["G", "D/F#", "Em", "C"], "A one-line chart with the slash chord D/F# in bar 2",
               caption="D/F# is a D chord with F# as the lowest note."), F + "slash-chord.svg")
save(chart_svg(["G", "Em", "C", "D"], "A four-bar loop in G: G, Em, C and D, with a repeat sign at each end",
               start_repeat=True, end_repeat=True, caption="Play the four bars, go back to the first repeat sign, and play them again."), F + "loop.svg")
print("chart done")
