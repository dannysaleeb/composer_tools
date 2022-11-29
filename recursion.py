from classes.rhythms import Rhythmlist, rl_to_nl

import mido

myRhythm = Rhythmlist([1, [1,1], [1, [0,1]], [0,1]], 1/2)

print(rl_to_nl(myRhythm).get_midi())
    
file = mido.MidiFile()

file.tracks.append(rl_to_nl(myRhythm).get_midi())

file.save('showingKitty.mid')