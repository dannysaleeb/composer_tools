TICKS_PER_BEAT = 480

def bpm_to_microseconds(bpm):
    return (60 / bpm) * 1000000