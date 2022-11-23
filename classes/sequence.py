"""
************************************
************************************
SEQUENCES


************************************
************************************
"""
class Sequence:
    def __init__(self, intervals, directions):
        self.intervals = intervals
        self.directions = directions
        self.connotations = []

    def __str__(self):
        if self.connotations:
            return f"{self.intervals}: {self.directions}, {self.connotations}"
        else:
            return f"{self.intervals}: {self.directions}"

    def getSequenceCell(self):

        sequence_cell = []

        for i in range(len(self.intervals)):
            sequence_cell.append((self.intervals[i], self.directions[i]))

        return sequence_cell

    def getSequenceRootsDegrees(self, scale, current_degree, octaves):

        # initialise the sequence cell, creates a tuple?
        cell = self.getSequenceCell()

        # initialise a return list
        sequence_data = [current_degree]

        # for the number of unique notes in the scale * the number of octaves
        for i in range((scale.length * octaves)):
            # for each interval in the cell
            for j in range(len(cell)):
                # if the direction of current interval is "down"
                if cell[j][1] == "down":
                    # use scale degree from interval method giving current_degree and the current interval with "is_descending" as True
                    next_degree = scale.getScaleDegreeFromInterval(current_degree, cell[j][0], True)
                    # add the next degree to the list
                    sequence_data.append(next_degree)
                    # make current_degree next_degree
                    current_degree = next_degree
                else:
                    # Same process, except "is_descending" is now False
                    next_degree = scale.getScaleDegreeFromInterval(current_degree, cell[j][0], False)
                    sequence_data.append(next_degree)
                    current_degree = next_degree

        return sequence_data

    def getSequenceRootsMIDI(self, scale, current_degree, octaves):

        sequence_data = self.getSequenceRootsDegrees(scale, current_degree, octaves)

        counter = 0
        pitch_level = 0

        current = sequence_data[0]
        midi_data = [scale.getScaleDegreeMIDI(current)]

        for i in range(len(sequence_data)):
            if i != len(sequence_data) - 1:
                next = sequence_data[i+1]
                if self.directions[counter % len(self.directions)] == 'down':
                    if current < next:
                        pitch_level += -1
                    midi_data.append(scale.getScaleDegreeMIDI(next) + (12 * pitch_level))
                    current = next
                    counter += 1
                else:
                    if next < current:
                        pitch_level += 1
                    midi_data.append(scale.getScaleDegreeMIDI(next) + (12 * pitch_level))
                    current = next
                    counter += 1
        
        return midi_data

    # # FIX THIS
    # def getSequenceChordsDegrees(self, sequence, interval, size):
    #     # sequence is a list of chord roots

    #     chords = []
    #     notes_as_degrees = self.getNotesAsDegrees()

    #     for degree in sequence:
    #         current = degree
    #         chord = []
    #         for i in range(size):
    #             chord.append(notes_as_degrees[current])
    #             next = ((current + (interval - (i + 1))) % self.length) + 1
    #             current = next
    #         chord.append(notes_as_degrees[current])
    #         chords.append(chord)
    #         """
    #         For each degree in the sequence, assuming same interval stacked chords, for i in range (size), next = degree + interval-(i+1),
    #         add this next degree to the chords list, 
    #         """
    #     return chords

class Pachelbel(Sequence):
    
    def __init__(self, scale):
        super().__init__([4, 2], ["down", "up"])
        self.scale = scale
    
    def __str__(self):
        if self.connotations:
            return f"{self.intervals}: {self.directions}, {self.connotations}"
        else:
            return f"{self.intervals}: {self.directions}"

    def getSequenceRootsDegrees(self, current_degree, octaves):

        # initialise the sequence cell, creates a tuple?
        cell = self.getSequenceCell()

        # initialise a return list
        sequence_data = [current_degree]

        # for the number of unique notes in the scale * the number of octaves
        for i in range((self.scale.length * octaves)):
            # for each interval in the cell
            for j in range(len(cell)):
                # if the direction of current interval is "down"
                if cell[j][1] == "down":
                    # use scale degree from interval method giving current_degree and the current interval with "is_descending" as True
                    next_degree = self.scale.getScaleDegreeFromInterval(current_degree, cell[j][0], True)
                    # add the next degree to the list
                    sequence_data.append(next_degree)
                    # make current_degree next_degree
                    current_degree = next_degree
                else:
                    # Same process, except "is_descending" is now False
                    next_degree = self.scale.getScaleDegreeFromInterval(current_degree, cell[j][0], False)
                    sequence_data.append(next_degree)
                    current_degree = next_degree

        # return list is a dict that has sequence degrees and directions for getting midi (although now maybe directions are easy to access?)
        return sequence_data

    def getSequenceRootsMIDI(self, current_degree, octaves):

        sequence_data = self.getSequenceRootsDegrees(current_degree, octaves)

        counter = 0
        pitch_level = 0

        current = sequence_data[0]
        midi_data = [self.scale.getScaleDegreeMIDI(current)]

        for i in range(len(sequence_data)):
            if i != len(sequence_data) - 1:
                next = sequence_data[i+1]
                if self.directions[counter % len(self.directions)] == 'down':
                    if current < next:
                        pitch_level += -1
                    midi_data.append(self.scale.getScaleDegreeMIDI(next) + (12 * pitch_level))
                    current = next
                    counter += 1
                else:
                    if next < current:
                        pitch_level += 1
                    midi_data.append(self.scale.getScaleDegreeMIDI(next) + (12 * pitch_level))
                    current = next
                    counter += 1
        
        return midi_data

# I don't know if I need the sequence class to be able to be too complex ... I probably want to give it a scale each time...
