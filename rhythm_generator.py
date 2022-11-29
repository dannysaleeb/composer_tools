"""
How best to generate Rhythmlists?

To start with, we can look at probabilistically adding 1 or 0 within some number of beats ...

"""
import random
import mido

from classes.rhythms import Rhythmlist, rl_to_nl

NUMERATOR = 5
DENOMINATOR = 8

BARS = 8

TOTAL_BEATS = NUMERATOR * BARS

BEAT_VALUE = 1 / DENOMINATOR

rhythm = Rhythmlist([], BEAT_VALUE)

for i in range(TOTAL_BEATS):

    randnum = random.randint(0,100)
    
    if randnum > 30:
        rhythm.values.append(1)
    else:
        rhythm.values.append(0)

print(rl_to_nl(rhythm).get_midi())

file = mido.MidiFile()

track = mido.MidiTrack()

track.append(mido.MetaMessage('time_signature', numerator=NUMERATOR, denominator=DENOMINATOR, time=0))

file.tracks.append(track)
file.tracks.append(rl_to_nl(rhythm).get_midi())

file.save('fileTest.mid')