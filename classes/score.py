from mido import Message, MidiFile, MidiTrack

from meta import *

"""
GLOBALS
"""
XML_BOILERPLATE = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<!DOCTYPE score-partwise PUBLIC\n\t\"-//Recordare//DTD MusicXML 4.0 Partwise//EN\"\n\t\"http://www.musicxml.org/dtds/partwise.dtd\">\n\n"

"""
SCORE TREE CLASSES
"""
class Node:
    # Generic Node
    def __init__(self, xml_tag, parent=None):
        self.id = id(self)
        self.xml_tag = xml_tag

        self.parent = parent
        
        # Make children a dict, with different categories...
        self.children = []
        
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

        self.depth = 0
        parent = self.parent
        while parent:
            self.depth += 1
            parent = parent.parent

    def build_xml(name, atts, content=None):
        return f"<{name} {atts}>", content, f"</{name}>"

    def __str__(self):
        return f"Node: {self.xml_tag}"

    def set_element(self, data):
        for k,v in data.items():
            self.data["xml"]["element"][k] = v

    def set_content(self, data):
        self.data['xml']['content'] = data
        self.data['xml']['empty'] = False

    def add_child(self, node):
        if isinstance(node, Node):
            node.depth = 0
            parent = self
            while parent:
                node.depth += 1
                parent = parent.parent
            self.children.append(node)
        else:
            print("can only add Node")

    def set_data(self, data):
        if data["content"]:
            self.data["content"] = data["content"]
        else:
            for k,v in data.items():
                self.data['xml']["element"][k] = v

    def preorder_traversal(self, root):
        res = []
        if root:
            res.append(root.data)
            for child in root.children:
                res = res + self.preorder_traversal(child)
        return res
    # for some reason this is a bit of a mess... 
    """

    Getting xml info should be more generic -- try creating a xml build method on Node class, 
    which could be redefined for each class that inherits from Node. 

    e.g. Part class:
        def build_xml(content, name="part", atts=f"id=\'{self.instrument}: {self.id}\'"):
            return f"{cont}"

    """
    def get_xml(self, root):
        xml = []
        if root:
            # first check if it's the leaf node (if leaf?) and return fully closed element if so
            if len(root.children) < 1:
                content = root.data['xml']['content']
                # This needs to be treated in the same way as the open tags ... tricky, because this is being treated as a leaf currently
                if isinstance(content, dict):
                    content = self.get_xml_content(root.data["xml"]["content"], root.depth)
                    for k,v in root.data["xml"]["element"].items():
                        # Why is root.depth always 0 here?
                        xml.append("\t" * root.depth + f"<{k}{v}>\n{content}")
                        xml.append("\t" * root.depth + f"</{k}>")
                else:
                    for k,v in root.data['xml']['element'].items():
                        xml.append("\t" * root.depth + f"<{k}{v}>{content}</{k}>")
            # else do open tags which are closed after the recursion (not sure why k is accessible after the for loops though)
            else:
                content = root.data["xml"]["content"]
                # Why is this type str???
                if isinstance(content, dict):
                    content = self.get_xml_content(root.data["xml"]["content"], root.depth)
                for k,v in root.data["xml"]["element"].items():
                    xml.append("\t" * root.depth + f"<{k}{v}>{content}")
                for child in root.children:
                    xml = xml + self.get_xml(child)
                xml.append("\t" * root.depth + f"</{k}>")
        return xml

    def build_xml_content(self, content_dict, tabs, counter=0):
        # The return string
        content = []
        # for key, value in dictionary
        for k,v in content_dict.items():
            if not isinstance(v, dict):
                content.append("\t" * (tabs + 1 + counter) + f"<{k}>{v}</{k}>\n")
            else:
                content.append("\t" * (tabs + 1 + counter) + f"<{k}>\n")
                counter += 1
                content = content + self.build_xml_content(v, tabs, counter)
                counter -= 1
                content.append("\t" * (tabs + 1 + counter) + f"</{k}>\n")

        return content

    def get_xml_content(self, content_dict, tabs, counter=0):


        content_string = ''
        
        content_list = self.build_xml_content(content_dict, tabs, counter)
        # strip last newline from content
        content_list[-1] = content_list[-1][:-1]
        for item in content_list:
            content_string += item

        return content_string

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
************
************
Level 3 Nodes -- sub-branches of Measure node

Notes, mainly.
************
************
"""
# Already have a Note class -- just need to adapt it here.
# "type" should really be "xml_element"

# How to get the xml data for Note?
class Note(Node):
    def __init__(self, pitch, octave, fractional_value=1/4, xml_tag="note", delta=0, parent=None):
        super().__init__(xml_tag, parent)
        
        # Pitch attributes
        """
        Need to make midi true to octave pitch level
        """
        self.midi = NOTE_TO_MIDI_FREQUENCY[pitch]["midi"]
        self.pitch = pitch
        """
        Need to make frequency true to octave pitch level
        """
        self.frequency = NOTE_TO_MIDI_FREQUENCY[pitch]["frequency"]
        self.octave = octave

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
                            "step": f"{self.pitch}",
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