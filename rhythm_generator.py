import mido

from classes.notes import Note, Notelist

import os, random

"""

Work in progress... 

Ultimately, this could be useful for generating rhythmic structures with Copycat-type algorithm ... if suitable
concepts can be defined. 

Also useful for my weekend work with SMA, though... for now, I can comb through and pick useful things. Ultimately,
would be nice to have something that generates notated web-examples... 

And then ... it would be great to have something that generates exercises according to the skill-level of the 
user ... for later. To start with it would simply be useful to have a sort of complexity-calculator ... so 
rhythmic complexity can be turned up/down on a dial.

Anyhow -- there's something in the idea of a recursive algo that goes to some level of depth in a rhythm tree,
and probabilistically replaces certain beats with further divisions. 

It would need to only replace those that have already been divided, else it would keep changing each time...

Need to think about the best data structure for this!! 

tree = {
    double: {
        beat1: {
            half1 {
                quarter1: None,
                quarter2: None
            },
            half2 {
                quarter1: None,
                quarter2: None
            }
        },
        beat2 {
            half1 {
                quarter1: None,
                quarter2: None
            },
            half2 {
                quarter1: None,
                quarter2: None
            }
        }
    }
}

I don't think so... 

[[1, [1, [1, 1]]], [0, 1]]

that seems more useful ... 

also ... this is a fun use of binary information?

Then, at each beat, check: is it a list? if yes, go inside, if no, parse the midi info

Encoding / Decoding ... 

To create this, there would need to be certain probability of splitting a beat, and then
only beats that have been split could be ripe for further splitting ... 

This is recursive somehow ... going in and checking the items in the list if they are list or not? For 
each beat it's recursive. 

"""


NUM_EXERCISES = 10

TICKS_PER_BEAT = 480

NUMERATOR = 5
DENOMINATOR = 8

NOTE_VALUES = [2, 1, 0.5]
BARS = 2

TOTAL_BEATS = NUMERATOR * BARS

BEAT_SIZE = int((1 / (DENOMINATOR / 4)) * TICKS_PER_BEAT)

quad = int(BEAT_SIZE * 4)
double = int(BEAT_SIZE * 2)
BEAT = BEAT_SIZE
half = int(BEAT_SIZE * 0.5)
quarter = int(BEAT_SIZE * 0.25)
eighth = int(BEAT_SIZE * 0.125)

print(f'eighth: {eighth}, quarter: {quarter}, half: {half}, beat: {BEAT}, double: {double}, quad: {quad}')

fragments = [Notelist(Note(60))]
"""

representation: 

in 2/4

| 2 | | 0 |

| 1, 1 | | 1, 0 | | 0, 1 | ( 0, 0 ) (is this essentially the only option at every level for each beat?)

| .5, .5, .5, .5 | |1, .5, .5 | |.5, 1, .5 | | .5, .5, 1 | 

| now with semis ... |

Some type of tree division ... 

{(1, 1), (1, 0), (0, 1), (0, 0)} (at every level this is true of one division of 2 [4 options and the 0,0 option is only relevant at some levels ... -- these maybe 
get conjoined according to another rule afterwards...])

2/4:

at crotchet level: these refer to crotchets in the bar
at quaver level: these refer to quavers in each crotchet beat (therefore options total or 16 -- 4^2 actually?)
{(1,1)(1,1), (1,1)(1,0), (1,1)(0,1), (1,1)(0,0)} & same with the other three, so 16 total
at semiquaver level: these refer to semis in each quaver beat (therefore 8^2)
as demisemi level: these refer to demis in each semiquaver beat (therefore 16^2) = 256
at hemidemisemi: (32^2) = 1024


"""
    

# Now need to probabilistically select beats within the number of beats there, and decide whether or not to divide further?
"""

At each level, need to go through and replace the rhythm given by a list or nested list ... of beats at the desired level,
depending on depth/difficulty level.

And to do ties ... would need to consider the higher levels starting on offbeat?? I don't know 
at what point it would make sense to make that adjustment ..

HOW could Copycat be applied to this? could be perfect, given that it is a tree already? 

bottom up would be starting with the lowest level of durations ... until 

"""


# This lot converts the calculated rhythm to MIDI...

meta = mido.MidiTrack()

meta.append(mido.MetaMessage('time_signature', numerator=NUMERATOR, denominator=DENOMINATOR, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))

rest_amount = 0

print(f"beat is {BEAT}")

file = mido.MidiFile()
file.tracks.append(meta)

for i in range(NUM_EXERCISES):

    top_rhythm = []

    for beat in range(TOTAL_BEATS):
        randnum = random.randint(0,100)
        if randnum > 40:
            top_rhythm.append(1)
        else:
            top_rhythm.append(0)



    rhythm = []

    # Creates a set of 1/0 pairs for each beat in the given number of bars, which represent the division of two below
    for beat in range(TOTAL_BEATS):
        fragment = []
        for i in range(2):
            randnum = random.randint(0,100)
            if randnum > 40:
                fragment.append(1)
            else:
                fragment.append(0)
        rhythm.append(fragment)


    for beat in range(TOTAL_BEATS):
        if random.randint(0,1) > 0:
            top_rhythm[beat] = rhythm[beat]

    print(top_rhythm)

    track = mido.MidiTrack()
    # For the "beat" level
    for note in top_rhythm:
        if isinstance(note, list):
            for i in range(2):
                if note[i]:
                    track.append(mido.Message('note_on', note=60, time=rest_amount))
                    track.append(mido.Message('note_off', note=60, time=half))
                    rest_amount = 0
                else:
                    rest_amount += half
        elif isinstance(note, int) and note:
            track.append(mido.Message('note_on', note=60, time=rest_amount))
            track.append(mido.Message('note_off', note=60, time=BEAT))
            rest_amount = 0
        else:
            rest_amount += BEAT
    file.tracks.append(track)


# # This is for the "half-beat" level
# for item in rhythm:
#     for i in range(2):
#         if item[i]:
#             track.append(mido.Message('note_on', note=60, time=rest_amount))
#             track.append(mido.Message('note_off', note=60, time=half))
#             rest_amount = 0
#         else:
#             rest_amount += half

print(file)

file.save('testRhythm.mid')


# file = mido.MidiFile()

# rf = mido.MidiFile()

# meta = mido.MidiTrack()
# content = mido.MidiTrack()

# meta.append(mido.MetaMessage('time_signature', numerator=5, denominator=128, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
# content.append(mido.Message('program_change', channel=1, program=2, time=0))
# content.append(mido.Message('note_on', note=60, time=0))
# content.append(mido.Message('note_off', note=60, time=480*4))

# rf.tracks.append(meta)
# rf.tracks.append(content)

# rf.save('testFile.mid')

# os.system('open testFile.mid')