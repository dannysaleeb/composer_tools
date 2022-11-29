TICKS_PER_BEAT = 480
TICKS_PER_WHOLE = TICKS_PER_BEAT * 4

def bpm_to_microseconds(bpm):
    return (60 / bpm) * 1000000