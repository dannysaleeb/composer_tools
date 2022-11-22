class Note:
    def __init__(self, name, midi, freq):
        self.name = name
        self.midi = midi
        self.freq = freq

    def __str__(self):
        return f"{self.name}: {self.midi}, {self.freq}"


"""
Note look-up table (notes specified as default in "middle" range)

I have a feeling this could be done with a .csv file, which might be cleverer -- load into memory when the program is run.
Might be neater...

"""
NOTES = {

    "C": Note("C", 60, 261.63),
    "C#": Note("C#", 61, 277.18),
    "Db": Note("Db", 61, 277.18),
    "D": Note("D", 62, 293.66),
    "D#": Note("D#", 63, 311.13),
    "Eb": Note("Eb", 63, 311.13),
    "E": Note("E", 64, 329.63),
    "F": Note("F", 65, 349.23),
    "F#": Note("F#", 66, 369.99),
    "Gb": Note("Gb", 66, 369.99),
    "G": Note("G", 67, 392.00),
    "G#": Note("G#", 68, 415.30),
    "Ab": Note("Ab", 68, 415.30),
    "A": Note("A", 69, 440.00),
    "A#": Note("A#", 70, 466.16),
    "Bb": Note('Bb', 70, 466.16),
    "B": Note("B", 71, 493.88)
}