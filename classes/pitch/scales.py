import os, sys

# Add parent directory (classes) to sys.path
filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(filepath)

# This needs fixing!!
from meta import NOTES
from note import Note, Notelist
from score import create_score, create_xml_file, create_midi_file, Part, Measure

"""
************************************
************************************
SCALE


************************************
************************************
"""
class Scale:

    def __init__(self, intervals, tonic=Note("C", 4), sharp=0):
        self.intervals = intervals
        self.length = len(self.intervals) + 1
        self.tonic = tonic
        self.sharp = sharp
    
    def __str__(self):
        
        intervals = {
            1: "ST",
            2: "T",
            3: "m3",
            4: "M3"
        }

        return_string = ''

        for i in range(len(self.intervals)):
            return_string += intervals[self.intervals[i]]
            if i == len(self.intervals) - 1:
                continue
            else:
                return_string += ", "

        return return_string

    def get_Notes(self):
        
        notelist = Notelist([self.tonic])
        
        cumulative_midi_total = self.tonic.midi

        counter = 1

        # Do I need NOTES after all?
        for interval in self.intervals:
            cumulative_midi_total += interval
            difference = (cumulative_midi_total - 60) % 12
            if self.sharp:
                for k, v in NOTES.items():
                    if "b" not in k and v.midi == 60 + difference:
                        notelist.notes.append(v)
            elif not self.sharp:
                for k, v in NOTES.items():
                    if "#" not in k and v.midi == 60 + difference:
                        notelist.notes.append(v)
            else:
                for k, v in NOTES.items():
                    if "#" not in k and "b" not in k and v.midi == cumulative_midi_total + difference:
                        notelist.notes.append(v)
            counter += 1
        
        return notelist

    def get_Notes_as_degrees(self):
        notes_as_degrees = {}
        
        counter = 1

        for note in self.get_Notes().notes:
            notes_as_degrees[counter] = note
            counter += 1

        return notes_as_degrees


    # This is either redundant, or could be used to return a midi pair for specific scale degree?
    def getScaleDegreeMIDI(self, degree):
        midiValue = self.tonic.midi
        for i in range(degree - 1):
            midiValue += self.intervals[i]
        return midiValue

    def get_asc(self, octaves=2, starting_octave=4, closed=True):

        # calculate starting note
        displacement = starting_octave - 4 # Could set this up as a _DEFAULT_OCTAVE variable and affect the NOTES table...
        starting_note = self.tonic.midi + (12 * displacement)

        # define return list variable and populate with starting tonic midi value
        asc_scale = Notelist([Note(starting_note)])

        # set the cumulative total to track
        cumulative_midi_total = starting_note

        # set octaves done counter to track
        counter = 0

        while counter < octaves:
            for interval in self.intervals:
                cumulative_midi_total += interval
                asc_scale.notes.append(Note(cumulative_midi_total))

            # Count off one octave
            counter += 1

            # If all octaves have been covered, check if tonic is required and return scale
            if counter == octaves:
                if closed:
                    asc_scale.notes.append(Note(starting_note + (12 * octaves)))
                    return asc_scale
                else:
                    return asc_scale
            # Otherwise, add the tonic for the next octave, and continue
            else:
                cumulative_midi_total = starting_note + (12 * counter)
                asc_scale.notes.append(Note(cumulative_midi_total))

        # returns a Notelist
        return asc_scale

    def get_desc(self, octaves=2, starting_octave=4, closed=True):
        if closed:
            return Notelist([x for x in reversed(self.get_asc(octaves, starting_octave).notes)])
        else:
            desc_scale = Notelist([x for x in reversed(self.get_asc(octaves, starting_octave).notes)])
            desc_scale.notes.remove(desc_scale.notes[-1])
            return desc_scale

    def get_asc_desc(self, octaves=2, starting_octave=4):
        return self.get_asc(octaves, starting_octave, False) + self.get_desc(octaves, starting_octave)


    def get_desc_asc(self, octaves=2, starting_octave=4):     
        return self.get_desc(octaves, starting_octave, False) + self.get_asc(octaves, starting_octave)

    def get_degree_from_interval(self, degree, interval, is_descending):
        if is_descending:
            new_degree = (degree + ((9 - interval) - 1)) % self.length
            return new_degree if new_degree != 0 else self.length
        else:
            new_degree = (degree + (interval - 1)) % self.length
            return new_degree if new_degree != 0 else self.length

"""

Need to check starting octave is working ??

"""

class MajorScale(Scale):
    def __init__(self, tonic=Note(60), intervals=[2,2,1,2,2,2], sharp=0):
        super().__init__(intervals, tonic, sharp)

class HarmMinorScale(Scale):
    pass

class MelMinorScale(Scale):
    pass

class NatMinorScale(Scale):
    pass

class PentatonicMajScale(Scale):
    pass

class PentatonicMinScale(Scale):
    pass


if __name__ == "__main__":

    scale = Scale([2,3,2,2,2])

    track = scale.get_asc_desc(2)
    # for note in track.notes:
    #     print(note.letter_name)

    score, parts = create_score(['violin'])

    note = Note(60, 4)

    if isinstance(note, Note):
        print("ISINSTANCE")
    else:
        print("NOTINSTANCE")

    for part in score.children:
        if isinstance(part, Part):
            for child in part.children:
                for note in track.notes:
                    if isinstance(note, Note):
                        child.add_child(note)

    # file = create_xml_file('makingHeadway', score)
    print(create_midi_file('testingMidiFile.mid', score, parts))