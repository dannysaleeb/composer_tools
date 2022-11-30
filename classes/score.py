class Score:
    def __init__(self):
        self.xml_data = {
            "boilerplate": "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<!DOCTYPE score-partwise PUBLIC\n\t\"-//Recordare//DTD MusicXML 4.0 Partwise//EN\"\n\t\"http://www.musicxml.org/dtds/partwise.dtd\">"
        }
        self.midi_data = {}
        self.children = []

    def get_xml(self):
        xml_string = ""
        for k,v in self.xml_data.items():
            xml_string += v + "\n"
        return xml_string

class Part:
    def __init__(self):
        self.xml_data = {
            # MAYBE PUT NODES in the data here?? no.
            "part": ""
        }
        self.midi_data = {}
        self.children = []

    def get_xml(self):
        xml_string = ""
        for k,v in self.xml_data.items():
            xml_string += f"<{k}>{v}</{k}>" + "\n"
        return xml_string

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

