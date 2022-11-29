from classes.notes import Note, Notelist

class Rhythmlist:
    def __init__(self, values, largest_note_value):
        self.values = values
        self.largest_note_value = largest_note_value

    def __str__(self):
        return str(self.values)

def parse_rhythmlist(rhythm_list, new_list=[], largest_note_value=1/4, rest_value=0):

    # for each item in the list, 
    for item in rhythm_list:
        # make sure the transforming duration variable is the same as that fed into the function at current level
        changing_value = largest_note_value
        if type(item) is list:
            # if list we're going in, so half duration
            changing_value /= 2
            # go on in and repeat
            new_list, rest_value = parse_rhythmlist(item, new_list, changing_value, rest_value)
        else:
            # if not, then it's a note or rest -- if note:
            if item:
                new_list.append(Note(60, note_value=changing_value, delta=rest_value))
                rest_value = 0
            # if not note, it's a rest --
            else:
                rest_value += changing_value
    return new_list, rest_value

def rl_to_nl(rhythmlist, largest_note_value=1/16):

    values = []

    try:
        values = rhythmlist.values
        largest_note_value = rhythmlist.largest_note_value
    except TypeError:
        return "You must supply an object of type Rhythmlist to this function"

    return Notelist(parse_rhythmlist(values, [], largest_note_value)[0])