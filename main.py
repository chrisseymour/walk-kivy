from kivy import require
require('1.10.0')

#standard imports
from math import sqrt
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


#diagnostics
from kivy.logger import Logger
from kivy.metrics import Metrics
from kivy.clock import Clock

#set Window.size
from kivy.config import Config
Config.set('graphics', 'width', '340')
Config.set('graphics', 'heigt', '500')
#Config.set('graphics', 'position', 'custom')
#Config.set('graphics', 'left', '300')
#Config.set('graphics', 'top', '300')
Config.write()

# custom imports
from Shapes import Box
from Sprite import Sprite, Background
from Items import Fire, Hat


def getStats(Widget):
        print('pos',self.pos,
                '\n center', self.center,
                '\n width', self.width,
                '\n height',self.height)

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
footstep = SoundLoader.load('audio/Footstep.wav')



class Man(Sprite):
    def __init__(self, pos):
        #self.images = SpriteAtlas('images/man.atlas')
        self.images = Atlas('images/man.atlas')
        w, h = pos[0]-self.images['man-stop'].width/2, pos[1]-self.images['man-stop'].height/2
        w, h = self.width/2, self.height/2
        print('man init', pos, w, h)
        #w, h, = pos[0]-w/2, pos[1]-h/2
        print('man init',pos, w, h)
        super().__init__(texture=self.images['man-stop'], scale=props.scale, pos=(w,h) )

        self.keys = list(  self.images.textures.keys( ) )

        ks = 'man-left man-mid man-right man-mid'.split()
        ksl = 'manleft-left manleft-mid manleft-right manleft-mid'.split()
        self.walk = [self.images[k] for k in ks]
        self.walk_left = [self.images[k] for k in ksl]
        #print([x for x in self.walk])
        #fp = self.images['man-left'].flip_horizontal()
        ### set animation based on veloicity params instead
        ###    (implement later)
        self.moving = False
        self.stopped = True
        self.keynum = 0
        self.ihat = 0
        self.counter = 0


    def move(self, pos, *ignore):
        '''takes a touch down event and tells man to move to that spot'''
        #print('ignore', ignore)
        if self.moving is False:
            self.moving = True
            self.direction(pos)
           # self.counter = 0
        elif self.moving is True:
            #self.redirect()
            self.moving = False
            self.texture = self.images['man-stop']
            self.counter = 0


    def direction(self, touch_pos):
        print( 'final pos: from move()', touch_pos )
        self.finalpos = touch_pos
        #print('current pos', self.pos, self.center)
        delta_x = float( self.center[0]-touch_pos[0] )
        #delta_y = float( self.center[1]-touch_pos[1] )
        deltas = [self.center[i]-touch_pos[i] for i in range(2)]
        self.ihat = -deltas[0]/abs(deltas[0])
        print('ihat', self.ihat)
        #print('deltas',deltas)
        #print('delta x', delta_x)
        self.ihat = -delta_x/abs(delta_x)
        print('ihat', self.ihat)

    def animate(self):
        #print(self.counter)
        if self.counter%20 == 0:
            #print('man.keynum', self.keynum)
            if self.ihat < 0:
                self.texture = self.walk_left[self.keynum%4]
                print('left')
            else:
                self.texture = self.walk[self.keynum%4]
                print('right')
            if self.keynum%2 is 0:
                print('play footstep')
                #footstep.play()
            self.keynum += 1
            self.counter = 0
        self.counter += 1


    def check_edge(self):
        if self.right < Window.width and self.x:
            return True
        else:
            return False


    def update(self):
        if self.moving is True:
            #print('x', self.x)
            #print('man.counter', self.counter)
            if self.ihat > 0 and self.center[0]<self.finalpos[0] and self.right < Window.width-20:
                self.x += 0.7 * props.scale
                self.animate()
            elif self.ihat < 0 and self.center[0]>self.finalpos[0] and self.x > 20: 
                self.x -= 0.7 * props.scale
                self.animate()
            else:
                print('stop moving')#, ihat is 0')
                #self.ihat = 0
                self.texture = self.images['man-stop']
                self.moving = False
                #self.counter = 0
        else:
            self.ihat = 0
            self.counter = 0


'''
class Hat(Widget):
    def __init__(self, source, pos, angle):
        super().__init__(pos=pos)
        #self.angle = angle
        self.image = Sprite(source=source, scale=props.scale, pos=pos)
        self.size = self.image.size
        self.add_widget( self.image )
        self.inhand = False

    def toHand(self, new_pos):
        self.center = new_pos
        self.inhand = True
        print('hat in hand', self.inhand)

    def move(self, touch_pos, new_hat_pos):
        self.center = touch_pos
        a = sqrt(sum([x*x for x in self.center]))
        b = sqrt(sum([x*x for x in new_hat_pos]))
        print('a',a,'b',b)
        print('abs(a-b)',abs(a-b))

        if abs(a-b) < 1:
            self.toHand( new_hat_pos )
            
        #self.pos = pos
        #self.inhand = True
        #self.image.pos = self.pos

    def update(self, ihat):
        #print('hat pos',self.pos)
        print('hat inhand:', self.inhand)
        if ihat > 0:
            self.x -= props.scale
        elif ihat < 0:
            self.x += props.scale
        self.image.pos = self.pos
'''

class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__()
        self.background = Background(source= 'images/backgroundMAC.png', scale=props.scale )
        self.add_widget(self.background)
        #self.quit_to_menu = Button( text='back to menu', font_size=14 )
        #self.add_widget(self.quit_to_menu)
        #self.quit_to_menu.bind( on_press=self._on_quit )
        ww, wh = Window.size
        print('window size',ww, wh)
        sw, sh = self.size
        print('self size',ww, wh)
        sx, sy = (self.width, self.height)
        print('xx yy',sx, sy)

        ##hat
        self.hat = Hat(source='images/hat.png', scale=props.scale, pos=(ww*3/4, wh/10), angle=20)
        self.rect_hat = Box(pos=self.hat.pos, size=self.hat.size)
        print('hat size', self.hat.size)
        self.add_widget( self.rect_hat )
        self.add_widget( self.hat )

        self.fire = Fire( scale=props.scale, pos=(-ww*1/4, wh/10), angle=5 )
        self.add_widget( self.fire )

        ##man
        self.man = Man( (ww/2, wh/2) )
        self.add_widget( self.man )

        #self.man_rect = Rectangle( pos=self.man.pos, size= self.man.size )
        #self.add_widget( self.man_rect )

        Clock.schedule_interval(self.update, 1.0/60.0)
        self.moving = False

    def _on_quit(self, *ignore):
        parent = self.parent
        parent.remove_widget( self )
        parent.add_widget( MainMenu() )


    def update(self, dt):
        self.man.update()
        self.background.scroll(self.man.ihat)
        self.fire.update(self.man.ihat)
        #if self.hat.inhand:
        #    print('inhand', self.hat.inhand)
        #else:
        self.hat.update(self.man.ihat)
        self.rect_hat.pos = self.hat.pos
        self.rect_hat.update()

    def on_touch_down(self, touch):
        print(touch.profile)
        print('touch pos',touch.pos)
                #if 5 < touch.pos[0] < 95:
        edge = 25
            #if self.hat.collide_point(*touch.pos):
                #self.hat.inhand = True

        if self.hat.collide_point(*touch.pos):
            if self.hat.inhand:
                self.hat.inhand = False

            if touch.is_double_tap:
                print('Touch is a Dobule tap')
                print(' - interval is', touch.double_tap_time)
                print(' - distance between previous is', touch.double_tap_distance)
                self.hat.toHand( (self.man.pos[0]+self.man.width, self.man.pos[1]+self.man.height/2) )
            else:
                touch.grab(self)
                print('touch in hat!')
                
        elif edge < touch.pos[0] < Window.width-edge:
            self.man.move(touch.pos)
            print('touch out of hat')
        else:
            print('touch out of bounds')
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            print('grab move')
            new_hat_pos = (self.man.pos[0]+self.man.width, self.man.pos[1]+self.man.height/2)
            self.hat.move( touch_pos=touch.pos, new_hat_pos=new_hat_pos )


    def on_touch_up(self, touch):
        if touch.grab_current is self:
            print('grab up')
            ###if end position is on man's hand stop the hat...

            new_hat_pos = (self.man.pos[0]+self.man.width, self.man.pos[1]+self.man.height/2)
            self.hat.move( touch_pos=touch.pos, new_hat_pos=new_hat_pos )
            #self.hat.pos =  new_hat_pos
            '''
            self.hat.center = touch.pos
            a = sqrt(sum([x*x for x in self.hat.center]))
            b = sqrt(sum([x*x for x in new_hat_pos]))
            print('a',a,'b',b)
            print('abs(a-b)',abs(a-b))

            if abs(a-b) < 1:
                self.hat.center = new_hat_pos
                self.hat.inhand = True
                print('hat in hand', self.hat.inhand)
            '''
            touch.ungrab(self)

            # accept the up
            return True



class MainMenu(Widget):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        #self.add_widget(Sprite(source='images/background.png'))
        self.background = Sprite( source='images/background2.png', scale=props.scale )
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
        print('props dim', self.width, self.height)
        self.center = Window.center
        ws = self.width / self.bg_width
        hs = self.height / self.bg_height
        self.scale = min(ws, hs)
        print('window scale', self.scale)
        print('window size', min(ws,hs), ws, hs)
        Logger.info('size={}; dpi={}, density={}, scale={}'.format(Window.size, Metrics.dpi, Metrics.density, self.scale) )
        '''
        if ws > hs:
            gap = self.width - self.bg_width *hs
            self.blank_rect = ((self.width - gap, 0), (gap, self.height))
        else:
            gap = self.height - self.bg_height * ws
            self.blank_rect =  ((0, self.height - gap), (self.width, gap))
        '''



if __name__ =='__main__':
    #Window.size = (360, 540)
    props = props()
    #sound1 = MultiSound('audio/sound1.wav', 4)
    #sound2 = SoundLoader.load('audio/sound2.wav')
    CatApp().run()
