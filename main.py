from kivy import require
require('1.10.0')

#standard imports
#import numpy as np

# kivy widget basics
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.button import Button
# graphics and sound
from kivy.uix.image import Image
from kivy.atlas import Atlas
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle


#diagnostics
from kivy.logger import Logger
from kivy.metrics import Metrics
from kivy.clock import Clock

#set Window.size
#from kivy.config import Config
#Config.set('graphics', 'width', '360')
#Config.set('graphics', 'heigt', '540')
#Config.write()

def getStats(Widget):
        print('pos',self.pos,
                '\n center', self.center,
                '\n width', self.width,
                '\n height',self.height)

class MulitSound(object):
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


class Sprite(Image):
    """load an image pass <source='imgname.pngs'>"""
    def __init__(self,  **kwargs):
        #super(Sprite, self).__init__(allow_stretch=True, **kwargs)
        super().__init__(allow_stretch=True,  **kwargs)
        print(kwargs)
        #self.texture.mag_filter = 'nearest'
        w, h = self.texture_size
        self.size = (props.scale * w, props.scale * h)
        print('size',self.size)
        
class Background(Widget):
    '''load the background image and scroll it from right to left on the screen
        making it look like you are moving right'''
    def __init__(self, source, **kwargs):
        super().__init__()
        self.image = Sprite( source=source )
        self.add_widget( self.image )
        self.size = self.image.size
        source2 = 'images/background2.png'
        self.image2 = Sprite( source=source2, x=self.width )
        self.add_widget(self.image2)
        self.image3 = Sprite( source=source2, x=-self.width )
        self.add_widget(self.image3)


    def scroll(self, ihat):
        if ihat > 0:
            self.image.x -= 0.25 * props.scale
            self.image2.x -= 0.25 * props.scale
            self.image3.x -= 0.25 * props.scale
        elif ihat < 0:
            self.image.x += 0.25 * props.scale
            self.image2.x += 0.25 * props.scale
            self.image3.x += 0.25 * props.scale
        #if self.image.right <= 0:
        #    self.image.x = 0
        #    self.image2.x = self.width
        #elif self.image.x+self.width >= self.width:
        #    self.image.x = 0
        #    self.image2.x = -self.width


class Man(Sprite):
    def __init__(self, pos):
        #self.images = SpriteAtlas('images/man.atlas')
        self.images = Atlas('images/man.atlas')
        super().__init__(texture=self.images['man-stop'], pos=pos)

        self.keys = list(  self.images.textures.keys( ) )

        ks = 'man-left man-mid man-right man-mid'.split()
        ksl = 'manleft-left manleft-mid manleft-right manleft-mid'.split()
        self.walk = [self.images[k] for k in ks]
        self.walk_left = [self.images[k] for k in ksl]
        print([x for x in self.walk])
        #fp = self.images['man-left'].flip_horizontal()
        ### set animation based on veloicity params instead
        ###    (implement later)
        self.moving = False
        self.stopped = True
        self.keynum = 0
        self.ihat = 0
        self.counter = 0


    def move(self, pos, *ignore):
        print('ignore', ignore)
        if self.moving is False:
            self.moving = True
        elif self.moving is True:
            self.moving = False
            self.texture = self.images['man-stop']
            self.counter = 0
        self.direction(pos)
        

    def direction(self, touch_pos):
        print( 'pos in move()', touch_pos )
        print('current pos', self.pos, self.center)
        delta_x = float( self.center[0]-touch_pos[0] )
        delta_y = float( self.center[1]-touch_pos[1] ) 
        print('delta x', delta_x)
        self.ihat = -delta_x/abs(delta_x)
        print('ihat', self.ihat)

        
    def update(self):
        if self.moving is True:
            #print('man.counter', self.counter)
            if self.ihat > 0:
                self.x += 0.7 * props.scale
            elif self.ihat < 0:
                self.x -= 0.7 * props.scale
            else:
                print('error ihat =', self.ihat )

            if self.counter%45 == 0:
                print('man.keynum', self.keynum)
                if self.ihat < 0:
                    self.texture = self.walk_left[self.keynum%4]
                    print('left')
                else:
                    self.texture = self.walk[self.keynum%4]
                    print('right')
                self.keynum += 1
                self.counter = 0
            self.counter += 1
                
        elif self.stopped is not True:
            self.texture = self.images['man-stop']
        else: 
            print('stopped')



class Box(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__()
        self.background = Background(source= 'images/background.png' )
        self.add_widget(self.background)
        #self.quit_to_menu = Button( text='back to menu', font_size=14 )
        #self.add_widget(self.quit_to_menu)
        #self.quit_to_menu.bind( on_press=self._on_quit )
        self.man = Man( (50, 100) )
        self.add_widget( self.man )

        Clock.schedule_interval(self.update, 1.0/30.0)
        self.moving = False

    def _on_quit(self, *ignore):
        parent = self.parent
        parent.remove_widget( self )
        parent.add_widget( MainMenu() )


    def update(self, dt):
        if self.man.moving is True:
            self.man.update()
            self.background.scroll(self.man.ihat)

    def on_touch_down(self, touch):
        print(touch.profile)
        print(touch.pos)
        self.man.move(touch.pos)



class MainMenu(Widget):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        #self.add_widget(Sprite(source='images/background.png'))
        self.background = Sprite( source='images/background2.png' )
        self.add_widget(self.background)
        self.size = self.children[0].size
        #self.start_button = Button(text='Start', pos=(10*props.scale, 0), font_size=14)
        #self.start_button.size = [s for s in self.size]
        #self.add_widget(self.start_button)
        #self.options_button = Button(text='Quit', pos=(110*props.scale, 0), font_size=14)
        #self.add_widget(self.options_button)
        #self.start_button.bind( on_press=self._on_start ) # on_press=App.stop() ) # *largs
        #self.options_button.bind( on_press=self._on_options ) # on_press=App.stop() ) # *largs
        
    def _on_start(self, *ignore):
        print('start!')
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget( Game() )

    def _on_options(self, *ignore):
        print('options')
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget( Options() )


#    def on_touch_down(self, *ignore):
#        parent = self.parnet
#        parent.remove_widget(self)
#        parent.add_widget(Game())


class CatApp(App):
    def build(self):
#        props.init()
        top = Widget()
        top.add_widget(Game())
        #top.add_widget(MainMenu())
        return top

class props(object):
    '''screen properties and background
        scaling factors'''
    def __init__(self):
        self.bg_width, self.bg_height = 360, 540
        self.width, self.height = Window.size
        self.center = Window.center
        ws = self.width / self.bg_width
        hs = self.height / self.bg_height
        self.scale = min(ws, hs)
        print('window scale', self.scale)
        print('window size', min(ws,hs), ws, hs)
        Logger.info('size={}; dpi={}, density={}, scale={}'.format(Window.size, Metrics.dpi, Metrics.density, self.scale) )
        if ws > hs:
            gap = self.width - self.bg_width *hs
            self.blank_rect = ((self.width - gap, 0), (gap, self.height))
        else:
            gap = self.height - self.bg_height * ws 
            self.blank_rect =  ((0, self.height - gap), (self.width, gap))



if __name__ =='__main__':
    #Window.size = (360, 540)
    props = props()
    #sound1 = MultiSound('audio/sound1.wav', 4)
    #sound2 = SoundLoader.load('audio/sound2.wav')
    CatApp().run()

