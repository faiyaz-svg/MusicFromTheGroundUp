from _common import *
from _common import _verovio

F = "03-the-major-scale-and-keys/sharp-key-signatures-"
def sig(key, note, title, name):
    abc = f"X:1\nM:none\nL:1/1\nK:{key} clef=treble\n{note} |]\n"
    save(_verovio(abc, title), F + name + ".svg")

sig("G", "G", "The treble clef with a key signature of one sharp, F sharp, followed by the note G", "g-major")
sig("D", "d", "The treble clef with a key signature of two sharps, F sharp and C sharp, followed by the note D", "d-major")
sig("C#", "c", "The treble clef with all seven sharps in order: F, C, G, D, A, E, B", "order-of-sharps")
print("sharp sigs done")
