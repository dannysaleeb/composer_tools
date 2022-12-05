from .settings import SETTINGS as s
import mido

from time import sleep


out = mido.open_output(s["MIDI_OUT"])

from classes.pitch.note import Note
from classes.pitch.chords import Chord

"""

What it needs to do:

1. Create a midi file, with all the relevant meta-information
    - take each voice and create a MidiTrack that has all of the information in that voice (notes & chords)
    - add all voices into a MidiFile (MidiFile.tracks)
    - also create any necessary meta-information ... so if there's structural information ... beats and barlines ... these 
      need to align with notes info. 

2. Think about how notes in scales are produced -- they need duration now (note_on and note_off pairs, dictated by duration)

So ... 

    1. Look at Note class -- does it have all of the midi information it might need?

"""
# Takes a Score object and plays the Voices therein
def serialPlayer(score, tempo):

    # pedal off
    out.send(mido.Message('control_change', control=64, value=63))

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
                    sleep(item.dur)
                    out.send(mido.Message('note_off', note=item.midi, velocity=item.vel))

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
