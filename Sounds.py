# Sounds.py

from kivy.core.audio import SoundLoader

class MultiSound(object):
    '''load a sound multiple times, sinze kivy can only play a sound onece'''
    def __init__(self, file, n):
        self.num = n
        self.sounds = [SoundLoader.load(file) for _ in range(n)]
        self.index = 0

    def play(self):
        self.sounds[self.index].play()
        self.index += 1
        if self.index == self.num:
            self.index = 0


#footsteps = MultiSound(file = 'audio/footstep.wav', n=3)
#footstep = SoundLoader.load('audio/Footstep.wav')
