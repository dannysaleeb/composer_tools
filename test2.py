from classes import notes, scales, chords
from playback.players import serialPlayer, parallelPlayer

myScale = scales.Scale([2,2,1,2,2,2], notes.NOTES['C'])
myOtherScale = scales.Scale([2,1,2,2,1,2], notes.NOTES['Eb'])

myChord = chords.Chord('Major', 3, [4,3], notes.NOTES["Eb"])

threads = [myScale.getAscScaleMIDI(2), myScale.getDescScaleMIDI(2), myChord.getFirstInvMIDI()]
print(threads)

parallelPlayer(threads, 180)

