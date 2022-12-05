from meta import *
from mido import Message, MidiTrack
"""

MAYBE PUT GLOBALS IN THEIR OWN FILE? Or in META??

Default tempo is crotchet = 500000microseconds (NB not milliseconds!!) (crot=120)

so:

1000000 microsecs = 1 second (this tempo is 60bpm)
60,000,000 microsecs = 1 minute

to convert ... 

60 / tempo (e.g. 120bpm) = 0.5secs * 1,000000 = microseconds

"""
# Couple of global look-up tables??
DYNAMICS = {
        'pppp': 13,
        'ppp': 25,
        'pp': 37,
        'p': 49,
        'mp': 61,
        'mf': 73,
        'f': 85,
        'ff': 97,
        'fff': 109,
        'ffff': 123
}

NOTE_NAMES = ['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B']

# I can find a better way of doing this, also ... mathematically work out frequency???

note_to_midi_frequency = {
    "C": {"midi": 60, "frequency": 261.63},
    "C#": {"midi": 61, "frequency": 277.18},
    "Db": {"midi": 61, "frequency": 277.18},
    "D": {"midi": 62, "frequency": 293.66},
    "D#": {"midi": 63, "frequency": 311.13},
    "Eb": {"midi": 63, "frequency": 311.13},
    "E": {"midi": 64, "frequency": 329.63},
    "F": {"midi": 65, "frequency": 349.23},
    "F#": {"midi": 66, "frequency": 369.99},
    "Gb": {"midi": 66, "frequency": 369.99},
    "G": {"midi": 67, "frequency": 392.00},
    "G#": {"midi": 68, "frequency": 415.30},
    "Ab": {"midi": 68, "frequency": 415.30},
    "A": {"midi": 69, "frequency": 440.00},
    "A#": {"midi": 70, "frequency": 466.16},
    "Bb": {"midi": 70, "frequency": 466.16},
    "B": {"midi": 71, "frequency": 493.88}
}

# I'm sure there's a better way than this ...

# So now note_value is given in American system as fraction: 1, 1/2, 1/4, 1/8 ... etc.

class Note:
    def __init__(self, midi, octave=4, frequency=None, note_value=1/4, dynamic='mf', articulation='nat', delta=0):
        self.midi = midi
        self.octave = octave
        self.freq = frequency
        self.note_value = note_value
        self.dur = int(self.note_value * TICKS_PER_WHOLE)
        self.dynamic = dynamic
        self.vel = DYNAMICS[dynamic]
        self.articulation = articulation
        self.delta = int(delta * TICKS_PER_WHOLE)

        for k, v in note_to_midi_frequency.items():
            if v['midi'] % 12 == self.midi % 12:
                self.name = k
                break
            else:
                self.name = "?"

        if self.freq == None:
            try: 
                if note_to_midi_frequency[self.name]:
                    self.freq = note_to_midi_frequency[self.name]['frequency']
            except KeyError:
                pass

    def __str__(self):
        return f"{self.name}{self.octave}"

    def get_midi_pair(self):
        midi = []
        midi.append(Message('note_on', note=self.midi, velocity=self.vel, time=0))
        midi.append(Message('note_off', note=self.midi, velocity=self.vel, time=self.dur))

        return midi

"""
What does a Note need to produce useful MIDI info?:

midi value
duration (in beats / ticks / time? -- quarter note is actually considered 1 beat ... eek ... but I suppose possible for MIDI)
dynamic (which will be parsed as velocity info: pppp: 1 ppp: 13 pp: 25 p: 37 mp: 49 mf: 61 f: 73 ff: 85 fff: 97 ffff: 109 ... 123 spread across 1-127)
articulation (which presumably will modulate the note length to some extent? Or, in cases where I have a good sample library, will use program change to 
select appropriate articulations)

"""
NOTES = {}

for note_name in NOTE_NAMES:
    NOTES[note_name] = Note(note_to_midi_frequency[note_name]['midi'], frequency=note_to_midi_frequency[note_name]['frequency'])

class B(Note):
    def __init__(self, name, midi, frequency=None, delta=8, duration=8, velocity=100, value="Breve"):
        super().__init__(name, midi, frequency, delta, duration, velocity)
        self.value = value

    def __str__(self):
        return f"{self.value} {self.name}: [velocity: {self.velocity}]"

class SB(Note):
    def __init__(self, name, midi, frequency=None, delta=4, duration=4, velocity=100, value="Semibreve"):
        super().__init__(name, midi, frequency, delta, duration, velocity)
        self.value = value

    def __str__(self):
        return f"{self.value} {self.name}: [velocity: {self.velocity}]"

class M(Note):
    def __init__(self, name, midi, frequency=None, delta=2, duration=2, velocity=100, value="Minim"):
        super().__init__(name, midi, frequency, delta, duration, velocity)
        self.value = value

    def __str__(self):
        return f"{self.value} {self.name}: [velocity: {self.velocity}]"

class C(Note):
    def __init__(self, name, midi, frequency=None, delta=1, duration=1, velocity=100, value="Crotchet"):
        super().__init__(name, midi, frequency, delta, duration, velocity)
        self.value = value

    def __str__(self):
        return f"{self.value} {self.name}: [velocity: {self.velocity}]"

class Q(Note):
    def __init__(self, name, midi, frequency=None, delta=0.5, duration=0.5, velocity=100, value="Quaver"):
        super().__init__(name, midi, frequency, delta, duration, velocity)
        self.value = value

    def __str__(self):
        return f"{self.value} {self.name}: [velocity: {self.velocity}]"

# It would be good to express their delta/duration as a function of a pulse

class SQ(Note):
    def __init__(self, name, midi, frequency=None, delta=0.25, duration=0.25, velocity=100, value="Quaver"):
        super().__init__(name, midi, frequency, delta, duration, velocity)
        self.value = value

    def __str__(self):
        return f"{self.value} {self.name}: [velocity: {self.velocity}]"

class DSQ(Note):
    def __init__(self, name, midi, frequency=None, delta=0.125, duration=0.125, velocity=100, value="Demisemiquaver"):
        super().__init__(name, midi, frequency, delta, duration, velocity)
        self.value = value

    def __str__(self):
        return f"{self.value} {self.name}: [velocity: {self.velocity}]"



class Notelist:
    def __init__(self, notes=[]):
        self.notes = notes

    def __str__(self):
        return_list = '| '
        for i in range(len(self.notes)):
            if i != len(self.notes) - 1:
                return_list += f'{self.notes[i].name}, '
            else:
                return_list += f"{self.notes[i].name} |"
        return return_list

    def __add__(self, other):
        if isinstance(other, Notelist):
            return Notelist(self.notes + other.notes)
        else:
            raise TypeError("Other object must be of type Notelist")

    def get_midi(self):
        
        return_track = MidiTrack()

        # add settings argument to modulate velocity etc.?, could do this with conditional 
        # which checks if settings present?
        
        for note in self.notes:
            return_track.append(Message('note_on', note=note.midi, velocity=note.vel, time=note.delta))
            return_track.append(Message('note_off', note=note.midi, velocity=note.vel, time=note.dur))

        return return_track

if __name__ == "__main__":

    note = Note(60, note_value=1/2)

    print(int(note.dur / TICKS_PER_BEAT))