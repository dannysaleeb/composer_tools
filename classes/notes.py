from .meta import *
from mido import Message
"""

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

class Note:
    def __init__(self, midi, octave=4, frequency=None, note_value=1, dynamic='mf', articulation='nat'):
        self.midi = midi
        self.octave = octave
        self.freq = frequency
        self.note_value = note_value
        self.dur = self.note_value * TICKS_PER_BEAT
        self.dynamic = dynamic
        self.vel = DYNAMICS[dynamic]
        self.articulation = articulation

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

"""
What does a Note need to produce useful MIDI info?:

midi value
duration (in beats / ticks / time? -- quarter note is actually considered 1 beat ... eek ... but I suppose possible for MIDI)
dynamic (which will be parsed as velocity info: pppp: 1 ppp: 13 pp: 25 p: 37 mp: 49 mf: 61 f: 73 ff: 85 fff: 97 ffff: 109 ... 123 spread across 1-127)
articulation (which presumably will modulate the note length to some extent? Or, in cases where I have a good sample library, will use program change to 
select appropriate articulations)

"""


"""
Note look-up table (notes specified as default in "middle" range)

I have a feeling this could be done with a .csv file, which might be cleverer -- load into memory when the program is run.
Might be neater...

"""
NOTES = {

    "C": Note(note_to_midi_frequency["C"]["midi"], note_to_midi_frequency["C"]["frequency"]),
    "C#": Note(note_to_midi_frequency["C#"]["midi"], note_to_midi_frequency["C"]["frequency"]),
    "Db": Note(note_to_midi_frequency["Db"]["midi"], note_to_midi_frequency["C"]["frequency"]),
    "D": Note(note_to_midi_frequency["D"]["midi"], note_to_midi_frequency["C"]["frequency"]),
    "D#": Note(note_to_midi_frequency["D#"]["midi"], note_to_midi_frequency["C"]["frequency"]),
    "Eb": Note(note_to_midi_frequency["Eb"]["midi"], note_to_midi_frequency["C"]["frequency"]),
    "E": Note(note_to_midi_frequency["E"]["midi"], note_to_midi_frequency["C"]["frequency"]),
    "F": Note(note_to_midi_frequency["F"]["midi"], note_to_midi_frequency["C"]["frequency"]),
    "F#": Note(note_to_midi_frequency["F#"]["midi"], note_to_midi_frequency["C"]["frequency"]),
    "Gb": Note(note_to_midi_frequency["Gb"]["midi"], note_to_midi_frequency["C"]["frequency"]),
    "G": Note(note_to_midi_frequency["G"]["midi"], note_to_midi_frequency["C"]["frequency"]),
    "G#": Note(note_to_midi_frequency["G#"]["midi"], note_to_midi_frequency["C"]["frequency"]),
    "Ab": Note(note_to_midi_frequency["Ab"]["midi"], note_to_midi_frequency["C"]["frequency"]),
    "A": Note(note_to_midi_frequency["A"]["midi"], note_to_midi_frequency["C"]["frequency"]),
    "A#": Note(note_to_midi_frequency["A#"]["midi"], note_to_midi_frequency["C"]["frequency"]),
    "Bb": Note(note_to_midi_frequency["Bb"]["midi"], note_to_midi_frequency["C"]["frequency"]),
    "B": Note(note_to_midi_frequency["B"]["midi"], note_to_midi_frequency["C"]["frequency"])
}

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

# How would the delta be dealt with in the player?
    # the sleep value would simply be given the current note's delta value?