import os, sys

# Adds parent directory (classes) to sys.path
filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(filepath)

from mido import Message, MidiFile, MidiTrack

from node import Node
from meta import *

class Note(Node):
    def __init__(self, pitch, octave=4, fractional_value=1/4, xml_tag="note", delta=0, parent=None):
        super().__init__(xml_tag, parent)
        
        # Pitch attributes
        """
        Need to make midi true to octave pitch level
        """
        self.midi = 0
        self.letter_name = ""
        
        self.octave = octave
        
        if isinstance(pitch, int):
            self.midi = pitch
            for k,v in NOTE_TO_MIDI_FREQUENCY.items():
                if pitch % 12 == v["midi"] % 12:
                    self.letter_name = k
        elif isinstance(pitch, str):
            difference = self.octave - 4
            self.midi = NOTE_TO_MIDI_FREQUENCY[pitch]["midi"] + (12 * difference)
            self.letter_name = pitch
        else:
            print("Pitch must be int or string.")
            return 0

        self.frequency = NOTE_TO_MIDI_FREQUENCY[self.letter_name]["frequency"]
        """
        Need to make frequency true to octave pitch level
        """

        # Duration attributes
        self.fractional_value = fractional_value
        self.symbol = FRACTION_TO_SYMBOL[f"1/{int(1/self.fractional_value)}"]
        self.tick_duration = int(self.fractional_value * TICKS_PER_WHOLE)
        self.xml_duration = int(self.tick_duration / TICKS_PER_BEAT)
        self.delta = int(delta * TICKS_PER_WHOLE)

        self.children = []

        # self.instrument = instrument
        self.data = {
                "xml": {
                    "empty": False,
                    "element": {
                        f"{self.xml_tag}": ""
                    },
                    "content": {
                        "pitch": {
                            "step": f"{self.letter_name}",
                            "octave": f"{self.octave}"
                        },
                        "duration": f"{self.xml_duration}",
                        "type": "quarter"
                    }
                },
                "midi": {}
        }

    """
    MIDI methods
    """
    # Need to find best way to record velocity of notes as an attribute and amend this method
    def get_midi_pair(self):
        """
        Returns a list containing one note_on and one corresponding note_off MIDI message.
        """
        # Got to be a better way to approach this? I want it to return the on and off messages not as list,
        # but as individual items ...
        midi = []

        midi.append(Message('note_on', note=self.midi, velocity=100, time=0))
        midi.append(Message('note_off', note=self.midi, velocity=100, time=self.tick_duration))

        return midi

    """
    XML Methods
    """
    # NEED TO FIX -- if it's the last in the process, don't add a space -- maybe do this by adding to a list?
    def build_xml_content(self, content_dict, counter=0):
        # The return string
        content = []
        # for key, value in dictionary
        for k,v in content_dict.items():
            if not isinstance(v, dict):
                content.append("\t" * counter + f"<{k}>{v}</{k}>\n")
            else:
                content.append("\t" * counter + f"<{k}>\n")
                counter += 1
                content = content + self.build_xml_content(v, counter)
                counter -= 1
                content.append("\t" * counter + f"</{k}>\n")

        # strip last newline from content
        content[-1] = content[-1][:-1]

        return content

    def get_xml_content(self, content_dict, counter=0):
        content_string = ''
        
        content_list = self.build_xml_content(content_dict, counter)
        for item in content_list:
            content_string += item

        return content_string

class Notelist:
    def __init__(self, notes=[]):
        self.notes = notes

    def __str__(self):
        return_list = '| '
        for i in range(len(self.notes)):
            if i != len(self.notes) - 1:
                return_list += f'{self.notes[i].letter_name}, '
            else:
                return_list += f"{self.notes[i].letter_name} |"
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

"""
TESTING
"""
if __name__ == "__main__":

    # print(sys.path)

    # noteList = Notelist([Note(60, 4), Note(62, 4), Note(64, 4)])
    # print(noteList)

    file = MidiFile()
    note = Note(60, 4)

    print(type(note))

    # file.tracks.append(noteList.get_midi())

    # file.save('stillWorks.mid')