from .settings import SETTINGS as s
import mido

from time import sleep


out = mido.open_output(s["MIDI_OUT"])

"""

What do I want the player to be able to do?? first of all, I want it to be able to play a list of midi values
in some alternating fashion ... either just play them directly, or interleave them according to what?

"""
def serialPlayer(threads, tempo):
    
    # Play the threads in order
    for thread in threads:
        for note in thread:
            # check value within MIDI range
            if note > 0 and note <= 127:
                out.send(mido.Message('note_on', note=note))
                sleep(60 / tempo)

def parallelPlayer(threads, tempo):

    # Determine the length of the longest thread
    longest_thread = 0
    for i in range(len(threads)):
        if len(threads[i]) > longest_thread:
                longest_thread = len(threads[i])
               
    for i in range(longest_thread):
        for j in range(len(threads)):
            # In the case that threads are different lengths
            try:
                note = threads[j][i]
            except IndexError:
                continue
            # check value is within MIDI range
            if note > 0 and note <= 127:
                out.send(mido.Message('note_on', note=note))
        sleep(60 / tempo)
