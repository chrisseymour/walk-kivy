#Sprite.py
#base class for image handling
from kivy.uix.image import Image
from kivy.uix.widget import Widget

class Sprite(Image):
    """load an image pass <source='imgname.pngs'>"""
    def __init__(self, scale, **kwargs):
        #super(Sprite, self).__init__(allow_stretch=True, **kwargs)
        super().__init__(allow_stretch=True,  **kwargs)
        #print('sprite kwargs', kwargs)
        #self.texture.mag_filter = 'nearest'
        w, h = self.texture_size
        self.size = (scale * w, scale * h)
        #print('size',self.size)


class Background(Widget):
    '''load the background image and scroll it from right to left on the screen
        making it look like you are moving right'''
    def __init__(self, source, scale, **kwargs):
        super().__init__()
        self.scale = scale
        self.image = Sprite( source=source, scale=self.scale)
        self.add_widget( self.image )
        self.size = self.image.size
        source2 = 'images/backgroundMAC.png'
        self.image2 = Sprite( source=source2, scale=self.scale, x=self.width )
        self.add_widget(self.image2)
        self.image3 = Sprite( source=source2, scale=self.scale, x=-self.width )
        self.add_widget(self.image3)


    def scroll(self, ihat):
        #scroll right
        amnt = 1.0
        if ihat > 0:
            self.image.x -= amnt * self.scale
            self.image2.x -= amnt * self.scale
            self.image3.x -= amnt * self.scale
        #scroll left
        elif ihat < 0:
            self.image.x += amnt * self.scale
            self.image2.x += amnt * self.scale
            self.image3.x += amnt * self.scale
        #else:
            #print('do not scroll, ihat is 0')

            ### **for continuous scrolling** ###
        #if self.image.right <= 0:
        #    self.image.x = 0
        #    self.image2.x = self.width
        #elif self.image.x+self.width >= self.width:
 
