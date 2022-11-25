from .notes import NOTES, Note, Notelist

"""
************************************
************************************
SCALE


************************************
************************************
"""
class Scale:

    def __init__(self, intervals, tonic=Note(60), sharp=0):
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

    def getAscScaleMIDI(self, octaves=2, starting_octave=4, closed=True):

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

    def getDescScaleMIDI(self, octaves, starting_octave=4, closed=True):
        if closed:
            return [x for x in reversed(self.getAscScaleMIDI(octaves, starting_octave))]
        else:
            desc_scale = [x for x in reversed(self.getAscScaleMIDI(octaves, starting_octave))]
            desc_scale.remove(desc_scale[-1])
            return desc_scale

    def getAscDescScaleMIDI(self, octaves, starting_octave=4):
        return self.getAscScaleMIDI(octaves, starting_octave, False) + self.getDescScaleMIDI(octaves, starting_octave)


    def getDescAscScaleMIDI(self, octaves, starting_octave=4):     
        return self.getDescScaleMIDI(octaves, starting_octave, False) + self.getAscScaleMIDI(octaves, starting_octave)

    def getScaleDegreeFromInterval(self, degree, interval, is_descending):
        if is_descending:
            new_degree = (degree + ((9 - interval) - 1)) % self.length
            return new_degree if new_degree != 0 else self.length
        else:
            new_degree = (degree + (interval - 1)) % self.length
            return new_degree if new_degree != 0 else self.length
