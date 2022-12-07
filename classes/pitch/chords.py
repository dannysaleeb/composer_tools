import os, sys

# Adds parent directory (classes) to sys.path
filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(filepath)

from pitch.note import Note
"""
************************************
************************************
CHORD


************************************
************************************
"""
class Chord():

    def __init__(self, name, size, intervals, root):
        self.name = name
        self.size = size
        self.intervals = intervals
        if isinstance(root, Note):
            self.root = root
        else:
            print(f"Chord instance was given {type(root)}, not a valid root Note")

    def __str__(self):
        return f"{self.root.letter_name}{self.name} Chord"

    def getRootPosMIDI(self):
        
        cumulative_midi_total = self.root.midi

        chord = [self.root.midi]
        for i in range(self.size - 1):
            cumulative_midi_total += self.intervals[i]
            chord.append(cumulative_midi_total)

        return chord

    def getFirstInvMIDI(self):

        rootPos = self.getRootPosMIDI()
        
        # transpose bass of chord up octave
        rootPos[0] = rootPos[0] + 12
        # rotate chord members
        rootPos.append(rootPos.pop(0))

        firstInv = rootPos
        return firstInv

    def getSecondInvMIDI(self):
        firstInv = self.getFirstInvMIDI()
        # transpose bass of chord up octave
        firstInv[0] = firstInv[0] + 12
        # rotate chord members
        firstInv.append(firstInv.pop(0))

        secondInv = firstInv
        return secondInv

    def getOpenVoicing(self, closed_chord):
        # give it a closed root/1stinv/2ndinv triad and get open voicing ...
        # either specify different kinds ... or randomise
        pass

    def getFourNoteMIDIVoicing(self):
        # Gotta think about the best way to achieve this ...
        pass

    # WHAT OTHER THINGS CAN WE DO??

"""
Should I be making chords out of abstract notes? Or would it make more sense to make these
chords out of scale degrees? Or can both be true? When we get to extension chords ... then it gets trickier ...
"""

class Triad(Chord):
    def __init__(self, name, intervals, root):
        super().__init__(name, 3, intervals, root)

    def __str__(self):
        return f"{self.root.name}{self.name} Chord"

class MajTriad(Triad):
    def __init__(self, root, name="Major", intervals=[4, 3]):
        super().__init__(name, intervals, root)

class MinTriad(Triad):
    def __init__(self, root, name="Minor", intervals=[3, 4]):
        super().__init__(name, intervals, root)

class DimTriad(Triad):
    def __init__(self, root, name="Diminished", intervals=[3, 3]):
        super().__init__(name, intervals, root)

class AugTriad(Triad):
    def __init__(self, root, name="Augmented", intervals=[4, 4]):
        super().__init__(name, intervals, root)


class Tetrad(Chord):
    def __init__(self, name, intervals, root):
        super().__init__(name, 4, intervals, root)

class Seven(Tetrad):
    def __init__(self, root, name="7", intervals=[4, 3, 3]):
        super().__init__(name, intervals, root)

class MajSeven(Tetrad):
    def __init__(self, root, name="M7", intervals=[4, 3, 4]):
        super().__init__(name, intervals, root)

class MinSeven(Tetrad):
    def __init__(self, root, name="m7", intervals=[3, 4, 3]):
        super().__init__(name, intervals, root)

class DimSeven(Tetrad):
    def __init__(self, root, name="dim7", intervals=[3, 3, 3]):
        super().__init__(name, intervals, root)

class MinMajSeven(Tetrad):
    def __init__(self, root, name="mM7", intervals=[3, 4, 4]):
        super().__init__(name, intervals, root)


class Pentad(Chord):
    pass

class Hexad(Chord):
    pass

class Septad(Chord):
    pass

if __name__ == "__main__":

    myNote = Note(60, 4)
    print(isinstance(myNote, Note))

    myChord = Chord('Major', 3, [4,3], myNote)
    print(myChord)