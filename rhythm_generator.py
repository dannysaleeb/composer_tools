"""
How best to generate Rhythmlists?

To start with, we can look at probabilistically adding 1 or 0 within some number of beats ...

"""
import random
import mido

from classes.rhythms import Rhythmlist, rl_to_nl

NUMERATOR = 4
DENOMINATOR = 4

BARS = 4

TOTAL_BEATS = NUMERATOR * BARS

BEAT_VALUE = 1 / DENOMINATOR

def split(list, probability, depth):
    return_list = list

    randnum = random.randint(0,100)
    for item in list:
        # This does NOT work but some kind of recursive something needs to happen ...
        if type(item) is list and depth > 0:
            depth -= 1
            return split(item, probability - 0.1)
        if randnum < 100 * probability:
            index = list.index(item)
            list[index] = []
            for i in range(2):
                randnum = random.randint(0,100)
                if randnum > 60:
                    list[index].append(1)
                else:
                    list[index].append(0)
    return return_list

myList = [1, 1, 1, 1, 1]

print(split(myList, 0.6))

"""

the split function will take a beat and decide whether or note to split it -- and this could be done recursively
using a depth value, so that for each beat in a list, the program decides if it splits the beat, and then again
provided the depth amount hasn't reached 0


Given an empty list:

feed it a bunch of beats
then ... new function ... 

go through the beats that are there:

if they are note:
    while depth > 0:
        decide whether or not to split
            if split:
                depth - 1
                decide whether or not to split again

if depth == 0:
    append whatever OH FUCK!!!

"""

def generate(depth):
    rhythm = Rhythmlist([], BEAT_VALUE)
    # first fill Rhythmlist with values
    for i in range(TOTAL_BEATS):
        randnum = random.randint(0,100)    
        if randnum > 30:
            rhythm.values.append(1)
        else:
            rhythm.values.append(0)

    for beat in rhythm.values:
        for i in range(depth):
            split(beat)


# for i in range(TOTAL_BEATS):

#     randnum = random.randint(0,100)
    
#     if randnum > 30:
#         rhythm.values.append(1)
#     else:
#         rhythm.values.append(0)

# for item in rhythm.values:
#     randnum = random.randint(0,100)

#     if randnum > 80:
#         rhythm.values[rhythm.values.index(item)] = []
#     else:
#         continue

# for item in rhythm.values:
    
#     randnum = random.randint(0,100)

#     if type(item) is list:
#         for i in range(2):
#             if randnum > 30:
#                 item.append(1)
#             else:
#                 item.append(0)

# print(rl_to_nl(rhythm).get_midi())

# file = mido.MidiFile()

# track = mido.MidiTrack()

# track.append(mido.MetaMessage('time_signature', numerator=NUMERATOR, denominator=DENOMINATOR, time=0))

# file.tracks.append(track)
# file.tracks.append(rl_to_nl(rhythm).get_midi())

# file.save('fileTest.mid')