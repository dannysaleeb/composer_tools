# This import adds the relevant filepath to access the classes package
import setup

from composer_tools.pitch import scales
from composer_tools.pitch.NOTES import NOTES

from composer_tools.playback.players import serialPlayer, parallelPlayer

myScale = scales.Scale([2,1,2,2,2,1,2], NOTES['Eb'], -1)
print(myScale)

# THIS IS NOW BROKEN!
# serialPlayer([sequence.Sequence([4, 2], ["down", "up"]).getSequenceRootsMIDI(myScale, 1, 3)], 240)

