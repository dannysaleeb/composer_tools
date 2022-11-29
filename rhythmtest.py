from classes.rhythms import Rhythmlist

rhythm = Rhythmlist([1,[1,0]], 1/2)
thisList = rhythm.get_notelist_from_rhythmlist(rhythm.values)

print(rhythm.convert_to_Rhythmlist())