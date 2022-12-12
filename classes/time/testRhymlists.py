import os, sys

# Adds parent directory (classes) to sys.path
filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(filepath)

from pitch.note import Note, Notelist
import mido

out = mido.open_output('IAC Driver Bus 1')

# I want to use this representation because it is a tree ...
rhythmlist = [4, 1, [3, -1, 0, 1], [3, [2, -1, 1], 1, 0], [2, 1, 0]]

# It means that the notes will have a durational tree representation, as well as having pitch as an attribute...

# That should mean -- the bar is divided in 3, and there are 3 equally divided notes in 

note_duration = 0
rest_duration = 0

top_level_value = 1

"""

A note should be created when:
    1. a new note onset is encountered and we've already counted up some note duration
    2. the end of the list is reached, and we've counted up some note duration...

for each item in the list:
    if the item is a zero:
        check if you already have some note_duration:
            if yes, add a note with that duration, and delta rest_duration to the list
            reset note_duration to zero
            reset rest_duration to zero
        add unit to ongoing rest_duration
    if the item is a one:
        check if you already have some note_duration:
            if yes, add a note with that duration, and delta rest_duration to the list
            reset note_duration to zero
            reset rest_duration to zero
        add unit to ongoing note_duration
    if the item is a -1:
        add unit to ongoing note_duration     

"""

def get_rhythms(rhythmlist, new_list=[], unit_duration=1, note_duration=0, rest_duration=0):

    # Make sure each 1 represents appropriate unit of duration
    unit_duration /= rhythmlist[0]

    for value in rhythmlist[1:]:
        # if list, we're going in ... go again
        if isinstance(value, list):
            new_list, note_duration, rest_duration = get_rhythms(value, new_list, unit_duration, note_duration, rest_duration)
        else:
            if value == 0:
                if note_duration:
                    new_list.append(Note(60, fractional_value=note_duration, delta=rest_duration))
                    note_duration = 0
                    rest_duration = 0
                rest_duration += unit_duration
            elif value > 0:
                if note_duration:
                    new_list.append(Note(60, fractional_value=note_duration, delta=rest_duration))
                    note_duration = 0
                    rest_duration = 0
                note_duration += unit_duration
            else:
                note_duration += unit_duration
    if note_duration:
        new_list.append(Note(60, fractional_value=note_duration, delta=rest_duration))
        note_duration = 0
        rest_duration = 0
    return new_list, note_duration, rest_duration

def rl_to_nl(rhythmlist, notes):
    # create a function that brings together a notelist with pitches
    # and the rhythmlist with rhythms...
    pass

myNotelist = get_rhythms(rhythmlist)[0]

for item in myNotelist:
    print(item.tick_duration, item.delta)

notelist = Notelist(myNotelist)

track = notelist.get_midi()

file = mido.MidiFile()

file.tracks.append(track)

gen = file.play()

for item in gen:
    out.send(item)