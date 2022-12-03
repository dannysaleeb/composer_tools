class Node:
    # Generic Node
    def __init__(self, node_type, parent=None):
        self.id = id(self)
        self.node_type = node_type

        self.parent = parent
        
        # Make children a dict, with different categories...
        self.children = []
        
        self.data = {
            "xml": {
                "empty": False,
                "element": {
                    f"{self.node_type}": ""
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

    def __str__(self):
        return f"Node: {self.node_type}"

    def set_element(self, data):
        for k,v in data.items():
            self.data["xml"]["element"][k] = v

    def set_content(self, data):
        self.data['xml']['content'] = data
        self.data['xml']['empty'] = False

    def add_child(self, node):
        if isinstance(node, Node):
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

    def get_xml(self, root):
        xml = []
        if root:
            # first check if it's the leaf node (if leaf?) and return fully closed element if so
            if len(root.children) < 1:
                content = root.data['xml']['content']
                for k,v in root.data['xml']['element'].items():
                    xml.append("\t" * root.depth + f"<{k}{v}>{content}</{k}>")
            # else do open tags which are closed after the recursion (not sure why k is accessible after the for loops though)
            else:
                content = root.data["xml"]["content"]
                for k,v in root.data["xml"]["element"].items():
                    xml.append("\t" * root.depth + f"<{k}{v}>{content}")
                for child in root.children:
                    xml = xml + self.get_xml(child)
                xml.append("\t" * root.depth + f"</{k}>")
        return xml

class Score(Node):
    def __init__(self, type="score-partwise", parent=None):
        super().__init__(type, parent)

        self.parts = []

        self.data = {
            "xml": {
                "empty": False,
                "element": {
                    f"{self.node_type}": " version=\"4.0\""
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
    def __init__(self, instrument, type="part", parent=None):
        super().__init__(type, parent)

        self.measures = []

        self.instrument = instrument
        self.data = {
                "xml": {
                    "empty": False,
                    "element": {
                        f"{self.node_type}": f" id=\"{self.instrument}: {self.id}\""
                    },
                    "content": ""
                },
                "midi": {}
        }
    
    def add_measure(self, number):
        self.measures.append(Measure(number, parent=self))

class Meta(Node):
    def __init__(self, type, parent=None):
        super().__init__(type, parent)

"""
************
************
Level 2(a) Nodes -- sub-branches of Part node

Mainly Measures ...
************
************
"""
class Measure(Node):
    def __init__(self, number, type="measure", parent=None):
        super().__init__(type, parent)

        self.number = number
        self.data = {
                "xml": {
                    "empty": False,
                    "element": {
                        f"{self.node_type}": f" number=\"{self.number}\""
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
            if child.type == "measure":
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
    def __init__(self, pitch, octave, duration, type="note", parent=None):
        super().__init__(type, parent)
        self.pitch = pitch
        self.octave = octave
        self.duration = duration

        self.children = []

        self.instrument = instrument
        self.data = {
                "xml": {
                    "empty": False,
                    "element": {
                        f"{self.node_type}": ""
                    },
                    "content": {
                        "pitch": {
                            "step": f"{self.pitch}",
                            "octave": f"{self.octave}"
                        },
                        "duration": f"{self.duration}",
                        "type": "quarter"
                    }
                },
                "midi": {}
        }
    # NEED TO FIX
    def get_xml_content(self, element, counter=0):
        content = ""
        for k,v in element.items():
            if isinstance(v, dict):
                content += "\t" * counter + f"<{k}>"
                counter += 1
                self.get_xml_content(v)
            else:
                content += "\t" * counter + f"<{k}>{v}</{k}>"
            content += "\t" * counter + f"</{k}>"
        return content

if __name__ == "__main__":

    score = Score()
    meta = Node("meta", score)

    instruments = ['violin', 'viola', 'cello']

    for instrument in instruments:
        score.add_child(Part(instrument, 'part', score))

    for child in score.children:
        if child.node_type == "part":
            for i in range(10):
                child.add_child(Measure(i+1, "measure", child))


    for item in score.get_xml(score):
        print(item)

    note = Note("C", 4, 1)

    content = note.get_xml_content(note.data["xml"]["content"])

    print(content)



"""

At some point need to look up how to write this stuff to a file.

Can have add_part method on Score (and self.parts)
Can have add_measure method on Part (and self.measures)
Can have add_note method on Measure (and self.notes)

"""