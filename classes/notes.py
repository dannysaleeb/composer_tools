class Note:
    def __init__(self, name, midi, frequency=None, delta=1, duration=1, velocity=100):
        self.name = name
        self.midi = midi
        self.delta = delta
        self.freq = frequency
        self.dur = duration
        self.vel = velocity

    def __str__(self):
        return f"{self.name}: {self.midi}, {self.freq}"

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

    "C": Note("C", 60, 261.63),
    "C#": Note("C#", 61, 277.18),
    "Db": Note("Db", 61, 277.18),
    "D": Note("D", 62, 293.66),
    "D#": Note("D#", 63, 311.13),
    "Eb": Note("Eb", 63, 311.13),
    "E": Note("E", 64, 329.63),
    "F": Note("F", 65, 349.23),
    "F#": Note("F#", 66, 369.99),
    "Gb": Note("Gb", 66, 369.99),
    "G": Note("G", 67, 392.00),
    "G#": Note("G#", 68, 415.30),
    "Ab": Note("Ab", 68, 415.30),
    "A": Note("A", 69, 440.00),
    "A#": Note("A#", 70, 466.16),
    "Bb": Note('Bb', 70, 466.16),
    "B": Note("B", 71, 493.88)
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