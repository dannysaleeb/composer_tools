"""
Each node has a name (the element name) and is either
empty or not.

Each node has a bunch of data, which manifests
as attributes on the element

"""
class Node:
    def __init__(self, name, empty=False, parent=None):
        self.name = name
        self.empty = empty
        self.parent = parent
        self.children = []
        self.data = {
            "element": {},
            "content": ""
        }
        self.depth = 0
        parent = self.parent
        while parent:
            self.depth += 1
            parent = parent.parent

    def __str__(self):
        return self.name

    def add_child(self, node):
        if isinstance(node, Node):
            self.children.append(node)
        else:
            print("Can only add Nodes and descendents of Node to tree")

    def set_data(self, data):
        if data["content"]:
            self.data["content"] = data["content"]
        else:
            for k,v in data.items():
                self.data["element"][k] = v

    def preorder_traversal(self, root):
        res = []
        if root:
            res.append(root.data)
            for child in root.children:
                res = res + self.preorder_traversal(child)
        return res


    # SO ... data on a node gives element name and the value is a string of attributes
    # on that element ...
    # But also need the content of the element ... which presumably needs to be 
    # in the data also ...
    def get_xml(self, root):
        xml = []
        if root:
            content = root.data["content"]
            for k,v in root.data["element"].items():
                xml.append("\t" * root.depth + f"<{k}{v}>{content}</{k}>\n")
            for child in root.children:
                xml = xml + self.get_xml(child)
        return xml


    # must be a recursive method you
    # can define to get all nodes ...

class Part(Node):
    def __init__(self, name, parent, empty=False):
        super().__init__(name, empty, parent)
        self.data = {
            "element": {"part": f" id=\"{name}\""},
            "content": ""
        }

class Score(Node):
    def __init__(self, name="score-partwise"):
        super().__init__(name)
        self.data = {
            "xml": {
                "boilerplate": f"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<!DOCTYPE {self.name} PUBLIC\n\t\"-//Recordare//DTD MusicXML 4.0 Partwise//EN\"\n\t\"http://www.musicxml.org/dtds/partwise.dtd\">"
            }
        }

    def get_xml(self):
        xml_string = ""
        for k,v in self.xml_data.items():
            xml_string += v + "\n"
        return xml_string
        
class Partlist(Node):
    def __init__(self, parent, name="part-list"):
        super().__init__(name, parent)
        self.xml_data = {
            name: ""
        }

    def get_tree_xml(self):
        xml_string = ""
        attributes = ""
        for k,v in self.xml_data.items():
            attributes = ""
            for k, v in v.items():
                attributes += f"{k}={v}"
            xml_string += f"<{k}>{v}</{k}>" + "\n"

# class Part:
#     def __init__(self):
#         self.xml_data = {
#             # MAYBE PUT NODES in the data here?? no.
#             "part": ""
#         }
#         self.midi_data = {}
#         self.children = []

#     def get_xml(self):
#         xml_string = ""
#         for k,v in self.xml_data.items():
#             xml_string += f"<{k}>{v}</{k}>" + "\n"
#         return xml_string

class Measure:
    pass

class TimeSig:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def __str__(self):
        return f"{self.numerator} / {self.denominator}"

class ScoreOld:
    def __init__(self, data={"title": 'Untitled', "composer": "Danny's Computer"}, num_bars=24, time_sig=TimeSig(4,4)):
        self.data = data
        self.num_bars = num_bars
        self.time_sig = time_sig
        self.bars = []
        for i in range(self.num_bars):
            self.bars.append(Bar(self.time_sig, {"number": i+1}))

    def __str__(self):
        return_data = ""
        for k, v in self.data.items():
            return_data += f"{k}: {v}\n"        
        return return_data

    def number_bars(self, start_num=1):
        for number, bar in enumerate(self.bars):
            bar.data["number"] = number + start_num


    def add_bars(self, number, position=None):
        for i in range(number):
            if len(self.bars) > 0 and position == None:
                position = self.bars[-1].data["number"]
                self.bars.insert(position, Bar(data={"number": position + 1}))
                position += 1
            elif position:
                self.bars.insert(position, Bar(data={"number": position + 1}))
                position += 1
            else:
                position = 0
                self.bars.insert(position, Bar(data={"number": position + 1}))
                position += 1
        self.number_bars()

    def remove_bars():
        pass

class Bar:
    def __init__(self, time_sig=TimeSig(4,4), data={"number": None, "subdivisions": None}):
        # How does a time_sig inherit from a previous one, and how to show
        # it doesn't need a midi_message?
        self.time_sig = time_sig
        self.data = data
        self.beats = []
        for beat in range(time_sig.numerator):
            self.beats.append(Beat([]))

    def __str__(self):
        return f"{self.beats}"
    
    def addNode(self, node):
        self.children.append(node)

class Beat:
    def __init__(self, data):
        self.data = data
        self.children = []

    def __str__(self):
        return self.data

    def addNode(self, node):
        self.children.append(node)

