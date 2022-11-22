# This import adds the relevant filepath to access the classes package
import setup

from classes import chords, notes, scales, sequence
from playback.players import serialPlayer, parallelPlayer

myScale = scales.Scale([2,1,2,2,2,1,2], notes.NOTES['Eb'], -1)

serialPlayer([sequence.Sequence([4, 2], ["down", "up"]).getSequenceRootsMIDI(myScale, 1, 3)], 120)

