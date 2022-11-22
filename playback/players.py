from .settings import SETTINGS as s
import mido

from time import sleep


out = mido.open_output(s["MIDI_OUT"])

"""

What do I want the player to be able to do?? first of all, I want it to be able to play a list of midi values
in some alternating fashion ... either just play them directly, or interleave them according to what?

"""
def serialPlayer(threads, tempo):
    for thread in threads:
        for note in thread:
            out.send(mido.Message('note_on', note=note))
            sleep(60 / tempo)

# Make so that this tries indices, but doesn't crash if it gets Index error (or whatever)
def parallelPlayer(threads, tempo):
    longest_thread = 0
    for i in range(len(threads)):
        if len(threads[i]) > longest_thread:
                longest_thread = len(threads[i])
    print(longest_thread)
    for i in range(longest_thread):
        for j in range(len(threads)):
            try:
                note = threads[j][i]
            except IndexError:
                continue
            out.send(mido.Message('note_on', note=note))
        sleep(60 / tempo)
