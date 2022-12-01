class Node:
    # Generic Node
    def __init__(self, parent=None):
        self.id = id(self)

        self.parent = parent
        
        self.children = []
        
        self.data = {
            "xml": {
                "empty": False,
                "element": {},
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
        return f"Node: {self.id}"

    def set_element(self, data):
        for k,v in data.items():
            self.data["xml"]["element"][k] = v

    def set_content(self, data):
        self.data['xml']['content'] = data
        self.data['xml']['empty'] = False

    def add_child(self):
        self.children.append(Node(self))

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

if __name__ == "__main__":

    root = Node()
    root.set_element({"score-partwise": " version=\"4.0\""})

    for i in range(10):
        root.add_child()
        print(root.children[i].depth)
        root.children[i].set_element({"part": f" id=\"{root.children[i].id}\""})
        root.children[i].set_content(i)

    for child in root.children:
        child.add_child()
        for child in child.children:
            child.set_element({"measure": f" number=\'1\'"})

    for item in root.get_xml(root):
        print(item)

