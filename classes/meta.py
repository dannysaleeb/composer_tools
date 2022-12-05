# from notes import Note

TICKS_PER_BEAT = 480
TICKS_PER_WHOLE = TICKS_PER_BEAT * 4

DYNAMICS = {
        'pppp': 13,
        'ppp': 25,
        'pp': 37,
        'p': 49,
        'mp': 61,
        'mf': 73,
        'f': 85,
        'ff': 97,
        'fff': 109,
        'ffff': 123
}

NOTE_NAMES = ['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B']

NOTE_TO_MIDI_FREQUENCY = {
    "C": {"midi": 60, "frequency": 261.63},
    "C#": {"midi": 61, "frequency": 277.18},
    "Db": {"midi": 61, "frequency": 277.18},
    "D": {"midi": 62, "frequency": 293.66},
    "D#": {"midi": 63, "frequency": 311.13},
    "Eb": {"midi": 63, "frequency": 311.13},
    "E": {"midi": 64, "frequency": 329.63},
    "F": {"midi": 65, "frequency": 349.23},
    "F#": {"midi": 66, "frequency": 369.99},
    "Gb": {"midi": 66, "frequency": 369.99},
    "G": {"midi": 67, "frequency": 392.00},
    "G#": {"midi": 68, "frequency": 415.30},
    "Ab": {"midi": 68, "frequency": 415.30},
    "A": {"midi": 69, "frequency": 440.00},
    "A#": {"midi": 70, "frequency": 466.16},
    "Bb": {"midi": 70, "frequency": 466.16},
    "B": {"midi": 71, "frequency": 493.88}
}

FRACTION_TO_SYMBOL = {
    "2": "breve",
    "1": "whole",
    "1/2": "half",
    "1/4": "quarter",
    "1/8": "eighth",
    "1/16": "16th",
    "1/32": "32nd",
    "1/64": "64th",
    "1/128": "128th",
    "1/256": "256th",
    "1/512": "512th",
    "1/1024": "1024th"
}

def bpm_to_microseconds(bpm):
    return (60 / bpm) * 1000000