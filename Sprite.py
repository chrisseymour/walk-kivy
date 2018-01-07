#Sprite.py
#base class for image handling
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.atlas import Atlas

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
        self.images = Atlas('images/background.atlas')
        #self.keys = self.images.keys()
        #list(  self.images.textures.keys( ) )
        self.keys = ('top', 'back', 'mid')
        print('bg keys', self.keys)
        self.scale = scale
        self.size = (1600, 640) #self.image.size
        x0 = -self.width/2
        print('initial x position', x0)
        self.image_bot = Sprite( texture=self.images['back'], scale=self.scale, x=x0 )
        self.add_widget(self.image_bot)
        #self.image = Sprite( source=source, scale=self.scale)
        #source2 = 'images/backgroundMAC.png'
        self.image_mid = Sprite( texture=self.images['mid'], scale=self.scale, x=x0 )
        self.add_widget(self.image_mid)
        self.image_top = Sprite( texture=self.images['top'], scale=self.scale, x=x0)
        self.add_widget( self.image_top )


    def scroll(self, ihat):
        #scroll right
        amnt = 1.0
        if ihat > 0:
            self.image_top.x -= 1.3 * amnt * self.scale
            self.image_mid.x -=  amnt * self.scale
            self.image_bot.x -= amnt * self.scale / 2
        #scroll left
        elif ihat < 0:
            self.image_top.x += 1.3 * amnt * self.scale
            self.image_mid.x +=  amnt * self.scale
            self.image_bot.x += amnt * self.scale / 2
        #else:
            #print('do not scroll, ihat is 0')

            ### **for continuous scrolling** ###
        #if self.image.right <= 0:
        #    self.image.x = 0
        #    self.image2.x = self.width
        #elif self.image.x+self.width >= self.width:
 
