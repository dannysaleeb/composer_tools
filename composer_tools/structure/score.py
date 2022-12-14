from mido import Message, MidiFile, MidiTrack

from .meta import *
from .node import Node

from ..pitch.note import Note, Notelist

from ..pitch.NOTES import NOTES

"""
GLOBALS
"""
XML_BOILERPLATE = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<!DOCTYPE score-partwise PUBLIC\n\t\"-//Recordare//DTD MusicXML 3.0 Partwise//EN\"\n\t\"http://www.musicxml.org/dtds/partwise.dtd\">\n\n"

"""
SCORE TREE CLASSES
"""
class Score(Node):
    """
    Root node of the score tree.
    """
    def __init__(self, xml_tag="score-partwise", parent=None):
        super().__init__(xml_tag, parent)

        self.parts = []

        self.children = [Partlist(parent=self)]

        self.data = {
            "xml": {
                "empty": False,
                "element": {
                    f"{self.xml_tag}": " version=\"3.0\""
                },
                "content": ""
            },
            "midi": {}
        }

    def add_part(self, instrument):
        self.parts.append(Part(instrument, parent=self))


class Part(Node):
    """
    Child of Score, takes additional 'instrument' argument on creation, which is used for id and part-name 
    """
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

class Partlist(Node):
    """
    Child of Score, required in xml file, and useful for reference elsewhere.
    Automatically updated when a Part is added to Score.
    """
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
    """
    For recording information about the score, such as titles and credits, etc.
    """
    def __init__(self, xml_tag, parent=None):
        super().__init__(xml_tag, parent)

class Scorepart(Node):
    """
    Child of Partlist, required by XML to itemise parts in the score, and to distniguish from actual <part></part> elements
    """
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

class Measure(Node):
    """
    Child of Part, container for Notes, means of defining metre in the score.
    """
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
        write_string += item + '\n'

    f.write(write_string)

    return f

def create_midi_file(filename, score, part_ids):
    """
    Need to create a track per part, append note pairs based on notes.
    """
    file = MidiFile()
    tracks = {}

    for id in part_ids:
        tracks[id] = MidiTrack()

    for id in part_ids:
        for part in score.children:
            if part.id == id:
                for measure in part.children:
                    for note in measure.children:
                        if isinstance(note, Note):
                            for item in note.get_midi_pair():
                                tracks[id].append(item)

    for k,v in tracks.items():
        file.tracks.append(v)
    file.save(filename)

    return file.tracks

"""
TESTING...
"""