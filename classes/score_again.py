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
    # for some reason this is a bit of a mess... 
    """

    Need to get the Node content if it's a dict, and then whack it in at the right tab length ... (which needs to be applied
    to each line within that content, so I guess it actually needs to go into the function also ... and add to the other amounts)
    
    The only problem is, "content" is being rendered as being between two tags on same line -- when it's a dict
    the tags need to be treated like other tags...

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
                        print(root.depth)
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
                print(f"CONTENT 2 is: \n{content}")
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

        for child in self.parent.children:
            if type(child) is Partlist:
                child.data["xml"]["content"][""]
    
    def add_measure(self, number):
        self.measures.append(Measure(number, parent=self))

# This is also problematic!!! but I will overcome it.
class Partlist(Node):
    def __init__(self, type="part-list", parent=None):
        super().__init__(type, parent)

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

    for child in score.children:
        for grandchild in child.children:
            grandchild.add_child(Note("C", 4, 1, parent=grandchild))
            for note in grandchild.children:
                print(note.depth)

# Need to find a way of making sure each node gets depth ... when they're attached to the node above ... (or attached
# using add_child() method)

    for item in score.get_xml(score):
        print(item)

"""

At some point need to look up how to write this stuff to a file.

Can have add_part method on Score (and self.parts)
Can have add_measure method on Part (and self.measures)
Can have add_note method on Measure (and self.notes)

"""