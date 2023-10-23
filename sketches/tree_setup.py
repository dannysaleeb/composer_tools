import setup

from composer_tools.structure.score import *

XML_BOILERPLATE = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<!DOCTYPE score-partwise PUBLIC\n\t\"-//Recordare//DTD MusicXML 4.0 Partwise//EN\"\n\t\"http://www.musicxml.org/dtds/partwise.dtd\">\n\n"

"""

I want access to all instrument nodes, basically

So score builder should return ... a list of instrument node ids, which can be given
variable names?

Should return the score, a list of instrument node ids

"""

"""

Would want to apply rhythmic transformations to notes in Notelist before adding to score,
so notes have the relevant durations from the outset...

"""

# This is way too wordy ... I need an easier way, or this needs to go into a function
def add_notes(score, part_id, notelist, measure_num=1):
    for part in score.children:
        if part.id == part_id:
            for measure in part.children:
                if measure.number == measure_num:
                    for note in notelist.notes:
                        measure.add_child(Note(note.pitch, note.octave, note.duration))
                        

score, new_parts = create_score(["violin 1", "violin 2", "viola", "cello", "double bass"])

# print(new_parts)

# for item in score.get_xml(score):
#     print(item)

violin_1, violin_2, viola, cello, db = new_parts

notes = ["C", "D", "E", "F"]

for part in score.children:
    if part.id == violin_1:
        for num, measure in enumerate(part.children):
                measure.add_child(Note(notes[num], 4, 1))

for item in score.get_xml(score):
    print(item)

file = create_xml_file('first_xml_file', score)

"""

I have created big bug -- need to make sure measures and notes and parts etc. 
on the relevant classes are stored in the children list, not a separate list

still want to be able to do "add_measures" etc. but they need to all go
to children list ... for each node.

Or ... just get rid of the "add_part" type methods ... 

"""