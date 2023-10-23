import setup

from composer_tools.structure.score import Score, Part, create_score, create_midi_file, create_xml_file
from composer_tools.pitch.note import Note
from composer_tools.structure.node import Node
from composer_tools.pitch.scales import Scale

scale = Scale([2, 1, 2, 2, 2, 1], Note(60))

score, part_ids = create_score(['violin', 'viola', 'cello'])

print(score, part_ids)

for part in score.children:
    if isinstance(part,Part):
        for measure in part.children:
            for note in scale.get_asc_desc().notes:
                # type issue -- maybe Federico will know how best to solve ...
                if isinstance(note, Note):
                    measure.add_child(note)

for item in score.get_xml(score):
    print(item)

file = create_xml_file('testFile', score)
midi_file = create_midi_file('testMidi.mid', score, part_ids)