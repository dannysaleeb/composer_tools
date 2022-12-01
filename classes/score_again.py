class Node:
    # Generic Node
    def __init__(self, node_type, parent=None):
        self.id = id(self)
        self.node_type = node_type

        self.parent = parent
        
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

    # Need to come up with a neat way to number measures ...

class Meta(Node):
    def __init__(self, type, parent=None):
        super().__init__(type, parent)

"""
************
************
Level 2(a) Nodes -- sub-branches of Part node

Part and Meta nodes inherit from Node class and generally are added to the Score root node.
************
************
"""

class Measure(Node):
    def __init__(self, type, parent=None):
        super().__init__(type, parent)

    def number_measures(self):
        for num, child in self.parent.children:
            if child.type == "measure":
                 child.data["measure"] = f" number=\"{num}\""

if __name__ == "__main__":

    score = Score()
    meta = Node("meta", score)

    instruments = ['violin', 'viola', 'cello']

    for instrument in instruments:
        score.add_child(Part(instrument, 'part', score))

    for child in score.children:
        if child.node_type == "part":
            for i in range(10):
                child.add_child(Measure('measure', child))

    for item in score.get_xml(score):
        print(item)

"""

At some point need to look up how to write this stuff to a file.

"""