#Sprite.py
#base class for image handling
from kivy.uix.image import Image

class Sprite(Image):
    """load an image pass <source='imgname.pngs'>"""
    def __init__(self, scale, **kwargs):
        #super(Sprite, self).__init__(allow_stretch=True, **kwargs)
        super().__init__(allow_stretch=True,  **kwargs)
        print('sprite kwargs', kwargs)
        #self.texture.mag_filter = 'nearest'
        w, h = self.texture_size
        self.size = (scale * w, scale * h)
        #print('size',self.size)

