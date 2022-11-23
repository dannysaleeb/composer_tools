from .settings import SETTINGS as s
import mido

from time import sleep


out = mido.open_output(s["MIDI_OUT"])

from classes.notes import Note
from classes.chords import Chord
from classes.voices import Voice

"""

What do I want the player to be able to do?? first of all, I want it to be able to play a list of midi values
in some alternating fashion ... either just play them directly, or interleave them according to what?

"""
# Takes a Score object and plays the Voices therein
def serialPlayer(score, tempo):
    
    # Play the threads in order
    for voice in score.voices:
        # items in thread will be either notes or chords
        for item in voice.content:
            # If item is a Chord
            if isinstance(item, Chord):
                # should be made up of a bunch of Notes
                midi = item.getRootPosMIDI()
                for note in midi:
                    if note > 0 and note <= 127:
                        out.send(mido.Message('note_on', note=note))
                    sleep(60 / tempo)
            # Else it's a Note
            else:
                if item.midi > 0 and item.midi <= 127:
                    out.send(mido.Message('note_on', note=item.midi, velocity=item.vel))
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
