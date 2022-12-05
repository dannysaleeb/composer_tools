from meta import *
from mido import Message, MidiTrack, MidiFile
from score import Note
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

# I can find a better way of doing this, also ... mathematically work out frequency???

# I'm sure there's a better way than this ...

# So now note_value is given in American system as fraction: 1, 1/2, 1/4, 1/8 ... etc.

# class Note:
#     def __init__(self, midi, octave=4, frequency=None, note_value=1/4, dynamic='mf', articulation='nat', delta=0):
#         self.midi = midi
#         self.octave = octave
#         self.freq = frequency
#         self.note_value = note_value
#         self.dur = int(self.note_value * TICKS_PER_WHOLE)
#         self.dynamic = dynamic
#         self.vel = DYNAMICS[dynamic]
#         self.articulation = articulation
#         self.delta = int(delta * TICKS_PER_WHOLE)

#         for k, v in NOTE_TO_MIDI_FREQUENCY.items():
#             if v['midi'] % 12 == self.midi % 12:
#                 self.name = k
#                 break
#             else:
#                 self.name = "?"

#         if self.freq == None:
#             try: 
#                 if NOTE_TO_MIDI_FREQUENCY[self.name]:
#                     self.freq = NOTE_TO_MIDI_FREQUENCY[self.name]['frequency']
#             except KeyError:
#                 pass

#     def __str__(self):
#         return f"{self.name}{self.octave}"

#     def get_midi_pair(self):
#         midi = []
#         midi.append(Message('note_on', note=self.midi, velocity=self.vel, time=0))
#         midi.append(Message('note_off', note=self.midi, velocity=self.vel, time=self.dur))

#         return midi

"""
What does a Note need to produce useful MIDI info?:

midi value
duration (in beats / ticks / time? -- quarter note is actually considered 1 beat ... eek ... but I suppose possible for MIDI)
dynamic (which will be parsed as velocity info: pppp: 1 ppp: 13 pp: 25 p: 37 mp: 49 mf: 61 f: 73 ff: 85 fff: 97 ffff: 109 ... 123 spread across 1-127)
articulation (which presumably will modulate the note length to some extent? Or, in cases where I have a good sample library, will use program change to 
select appropriate articulations)

"""
# NOTES = {}

# for note_name in NOTE_NAMES:
#     NOTES[note_name] = Note(NOTE_TO_MIDI_FREQUENCY[note_name]['midi'], frequency=NOTE_TO_MIDI_FREQUENCY[note_name]['frequency'])

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
            return_track.append(Message('note_on', note=note.midi, velocity=100, time=note.delta))
            return_track.append(Message('note_off', note=note.midi, velocity=100, time=note.tick_duration))

        return return_track

if __name__ == "__main__":

    noteList = Notelist([Note("C", 4), Note("D", 4), Note("E", 4)])

    file = MidiFile()

    file.tracks.append(noteList.get_midi())

    file.save('stillWorks.mid')