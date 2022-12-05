from mido import Message, MidiFile, MidiTrack

from meta import *
from node import Node

from pitch.note import Note

"""
GLOBALS
"""
XML_BOILERPLATE = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<!DOCTYPE score-partwise PUBLIC\n\t\"-//Recordare//DTD MusicXML 4.0 Partwise//EN\"\n\t\"http://www.musicxml.org/dtds/partwise.dtd\">\n\n"

"""
SCORE TREE CLASSES
"""
class Score(Node):
    def __init__(self, xml_tag="score-partwise", parent=None):
        super().__init__(xml_tag, parent)

        self.parts = []

        self.children = [Partlist(parent=self)]

        self.data = {
            "xml": {
                "empty": False,
                "element": {
                    f"{self.xml_tag}": " version=\"4.0\""
                },
                "content": ""
            },
            "midi": {}
        }

    def add_part(self, instrument):
        self.parts.append(Part(instrument, parent=self))

"""
************
************
Level 1 Nodes -- sub-branches of Score (root) node

Part and Meta nodes inherit from Node class and generally are added to the Score root node.
************
************
"""
class Part(Node):
    def __init__(self, instrument, xml_tag="part", parent=None):
        super().__init__(xml_tag, parent)

        self.measures = []

        self.instrument = instrument
        self.data = {
                "xml": {
                    "empty": False,
                    "element": {
                        f"{self.xml_tag}": f" id=\"{self.instrument}: {self.id}\""
                    },
                    "content": ""
                },
                "midi": {}
        }

        for child in self.parent.children:
            if isinstance(child, Partlist):
                child.add_child(Scorepart(self.id, self.instrument, parent=child))
    
    def add_measure(self, number):
        self.measures.append(Measure(number, parent=self))

# This is also problematic!!! but I will overcome it.
class Partlist(Node):
    def __init__(self, xml_tag="part-list", parent=None):
        super().__init__(xml_tag, parent)

        self.data = {
                "xml": {
                    "empty": False,
                    "element": {
                        f"{self.xml_tag}": ""
                    },
                    "content": ""
                },
                "midi": {}
        }

class Meta(Node):
    def __init__(self, xml_tag, parent=None):
        super().__init__(xml_tag, parent)

class Scorepart(Node):
    def __init__(self, id, instrument, xml_tag="score-part", parent=None):
        super().__init__(xml_tag, parent)
        self.id = id
        self.instrument = instrument

        self.data = {
                "xml": {
                    "empty": False,
                    "element": {
                        f"{self.xml_tag}": f" id=\"{self.instrument}: {self.id}\""
                    },
                    "content": ""
                },
                "midi": {}
        }

"""
************
************
Level 2(a) Nodes -- sub-branches of Part node

Mainly Measures ...
************
************
"""
class Measure(Node):
    def __init__(self, number, xml_tag="measure", parent=None):
        super().__init__(xml_tag, parent)

        self.number = number
        self.data = {
                "xml": {
                    "empty": False,
                    "element": {
                        f"{self.xml_tag}": f" number=\"{self.number}\""
                    },
                    "content": ""
                },
                "midi": {}
        }

        self.notes = []

    def add_note(self, note):
        self.notes.append(Note())

    def number_measures(self):
        for num, child in self.parent.children:
            if child.xml_tag == "measure":
                 child.data["measure"] = f" number=\"{num}\""

"""
HELPERS
"""
def create_score(parts, settings=None):
    new_score = Score()
    
    for part in parts:
        new_score.add_child(Part(part, parent=new_score))

    part_ids = []
    for part in new_score.children:
        if isinstance(part, Part):
            for i in range(4):
                part.add_child(Measure(i+1, parent=part))
            part_ids.append(part.id)

    return new_score, part_ids

def create_xml_file(filename, score):
    try:
        f = open(f"{filename}.xml", "x")
    except FileExistsError:
        overwrite = input("File already exists. Overwrite? (y/n): ")
        if overwrite == "y":
            f = open(f"{filename}.xml", "w")
        else:
            return 0
    
    f.write(XML_BOILERPLATE)

    write_string = ''
    for item in score.get_xml(score):
        write_string += item

    f.write(write_string)

    return f

def create_midi_file():
    pass


"""
TESTING...
"""
if __name__ == "__main__":

    score = Score()
    meta = Node("meta", score)

    instruments = ['violin', 'viola', 'cello']

    for instrument in instruments:
        score.add_child(Part(instrument, 'part', score))

    for child in score.children:
        if isinstance(child, Part):
            for i in range(10):
                child.add_child(Measure(i+1, "measure", child))

# Need to find a way of making sure each node gets depth ... when they're attached to the node above ... (or attached
# using add_child() method)

    note = Note("C", 4)
    print(note.get_midi_pair())

"""

Can have add_part method on Score (and self.parts)
Can have add_measure method on Part (and self.measures)
Can have add_note method on Measure (and self.notes)

"""