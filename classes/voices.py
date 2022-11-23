class Voice:
    def __init__(self, id, tempo, content):
        self.id = id
        # In typical circumstances, the voice should inherit the score's tempo
        # Need to look at how this might otherwise be modulated, though
        self.tempo = tempo
        self.content = content

    def __str__(self):
        voice = '\n'
        for item in self.content:
            voice += f"| {item.value}: {item.name} | "
        return voice + '\n'

    # format voice in some way? 
    # What do I want to be able to do?
    # It would be good to be able to treat a voice as having some kind of 
    # dynamic shape ... applied to all notes over time.

class Score:
    def __init__(self, name="Untitled", voices=[], tempo=100):
        self.name = name
        self.voices = voices
        self.tempo = tempo

    """
    
    So ... a voice would have a bunch of content, but also a dynamics plane (applied to velocity and to some 
    extent articulation? of notes contained in content), and articulation plane (applied to duration of notes
    in content), and even maybe a tempo / accuracy / quantization plane

    For now, a voice has a bunch of notes and chords -- a voice is not only notes, but can be -- like Sibelius)
    
    """