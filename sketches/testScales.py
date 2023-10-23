import setup
import mido

out = mido.open_output('IAC Driver Bus 1')

from time import sleep

from composer_tools.pitch.scales import Scale
from composer_tools.pitch.note import Note

from composer_tools.pitch.sequence import Sequence

print("===============================")
print("SCALES")
print("===============================" + '\n\n')
"""
SCALE ONE
defining a major scale from scratch and retrieving various scales as Notelists.
"""
scale_one = Scale([2,2,1,2,2,2], Note(60, 4))

one_notes = scale_one.get_Notes()

one_asc = scale_one.get_asc(2)
one_desc = scale_one.get_desc(2)
one_asc_desc = scale_one.get_asc_desc(2)

print("=========one_notes=========")
print(one_notes)
print('\n\n')

print('playing one_asc.notes...')
for note in one_asc.notes:
    out.send(mido.Message('note_on', note=note.midi))
    sleep(0.5)
sleep(1.5)

print('playing one_desc.notes...')
for note in one_desc.notes:
    out.send(mido.Message('note_on', note=note.midi))
    sleep(0.5)
sleep(1.5)

print('playing one_asc_desc.notes...')
for note in one_asc_desc.notes:
    out.send(mido.Message('note_on', note=note.midi))
    sleep(0.5)
sleep(1.5)
print('\n\n')


"""
SCALE TWO
another scale, pentatonic minor.
"""
scale_two = Scale([3,2,2,3], Note(63))

two_notes = scale_two.get_Notes()

print("=========two_notes=========")
print(two_notes)
print('\n\n')

two_asc = scale_two.get_asc(2)
two_desc = scale_two.get_desc(2)
two_asc_desc = scale_two.get_asc_desc(2)

print('playing two_asc.notes...')
for note in two_asc.notes:
    out.send(mido.Message('note_on', note=note.midi))
    sleep(0.5)
sleep(1.5)

print('playing two_desc.notes...')
for note in two_desc.notes:
    out.send(mido.Message('note_on', note=note.midi))
    sleep(0.5)
sleep(1.5)

print('playing two_asc_desc.notes...')
for note in two_asc_desc.notes:
    out.send(mido.Message('note_on', note=note.midi))
    sleep(0.5)
sleep(1.5)
print('\n\n')


"""
INTERLEAVING
Interleaving two scales using the length of the shortest as ref for indexing, sending
directly to MIDI out.
"""
print("===============================")
print("SCALES")
print("===============================" + '\n\n')
counter = 0

print('playing interleaved scales...')
for i in range(len(two_asc_desc.notes * 2)):
    if i % 2 == 0:
        out.send(mido.Message('note_on', note=one_asc_desc.notes[counter].midi))
        sleep(0.5)
    else:
        out.send(mido.Message('note_on', note=two_asc_desc.notes[counter].midi))
        sleep(0.5)
        counter += 1
sleep(1.5)
print('\n\n')


"""
SEQUENCES
"""
print("===============================")
print("SEQUENCES")
print("===============================" + '\n\n')
sequence_one = Sequence([4,2], ['down', 'up'])

print("=========seq_one_notes=========")
seq_one_notes = sequence_one.get_notelist(scale_one, 1, 2)
print(seq_one_notes)
print("playing...")
print('\n\n')

for note in seq_one_notes.notes:
    out.send(mido.Message('note_on', note=note.midi))
    sleep(0.5)

print("=========seq_one_midi=========")
# Gets Midi note values directly from the Sequence class
seq_one_midi = sequence_one.getSequenceRootsMIDI(scale_one, 1, 2)
print(seq_one_midi)
print("playing...")
print('\n\n')

for value in seq_one_midi:
    out.send(mido.Message('note_on', note=value))
    sleep(0.5)

print("=========seq_one_otherMidi=========")
# Returns a mido MidiTrack with note_on/note_off pairs 
seq_one_otherMidi = seq_one_notes.get_midi()
print(seq_one_otherMidi)
print("playing...")
print('\n\n')

for msg in seq_one_otherMidi:
    out.send(msg)
    sleep(0.5)

"OR"

file = mido.MidiFile()

file.tracks.append(seq_one_otherMidi)

gen = file.play()

for item in gen:
    out.send(item)


sequence_two = Sequence([5,4,2], ['down', 'up', 'up'])

seq_two_notes = sequence_two.get_notelist(scale_two, 1, 2)

seq_two_track = seq_two_notes.get_midi()

file = mido.MidiFile()

file.tracks.append(seq_two_track)

gen = file.play()

for item in gen:
    out.send(item)

counter = 0


"""
Interleaving Sequences using Notelists...
"""
interleave_track = mido.MidiTrack()

for i in range(len(seq_one_notes.notes * 2)):
    if i % 2 == 0:
        midi_pair = seq_one_notes.notes[counter].get_midi_pair()
        for msg in midi_pair:
            interleave_track.append(msg)
    else:
        midi_pair = seq_two_notes.notes[counter].get_midi_pair()
        for msg in midi_pair:
            interleave_track.append(msg)
        counter += 1

file = mido.MidiFile()

file.tracks.append(interleave_track)

gen = file.play()

for item in gen:
    out.send(item)