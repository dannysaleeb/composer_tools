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