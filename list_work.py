from classes.notes import Note, Notelist
import mido

"""

Do I need to think about how note durations are handled/defined?



"""

irregular_list = [1, [1, [1, [0, 1]]], [1,[1,1]], 0]

# This is what I need to be able to do what I want to do, but I need to understand it better.
# Must look closely at list comprehensions...
flatten_list = lambda irregular_list:[element for item in irregular_list for element in flatten_list(item)] if type(irregular_list) is list else [irregular_list]

"""
This is now working -- and usefully have added delta value to Note class...?

"""

"""

Ok, so this is now a good parser -- add a class for rhythmlist and add this functionality -- then can work out ways
of constructing rhythmlists that are useful ... start on git versions of this stuff ...

"""

def parse_rhythmlist(rhythm_list, new_list=[], largest_note_value=1/4, rest_value=0, counter=0):

    # for each item in the list, 
    for item in rhythm_list:
        # make sure the transforming duration variable is the same as that fed into the function at current level
        changing_value = largest_note_value
        if type(item) is list:
            # if list we're going in, so half duration
            changing_value /= 2
            # go on in and repeat
            counter += 1
            new_list, rest_value = parse_rhythmlist(item, new_list, changing_value, rest_value, counter)
        else:
            # if not, then it's a note or rest -- if note:
            if item:
                new_list.append(Note(60, note_value=changing_value, delta=rest_value))
                rest_value = 0
            # if not note, it's a rest --
            else:
                rest_value += changing_value
    return new_list, rest_value

def get_notelist_from_rhythmlist(rhythmlist, largest_note_value=1/16):

    return Notelist(parse_rhythmlist(rhythmlist, [], largest_note_value)[0])

file = mido.MidiFile()

file.tracks.append(get_notelist_from_rhythmlist(irregular_list).get_midi())

file.save('myRhythm.mid')

# returns a list of Notes ... which could directly be a Notelist?


"""
Now to convert to midi need to take delta into account?

"""