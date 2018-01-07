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
# text
from kivy.uix.label import Label


#diagnostics
from kivy.logger import Logger
from kivy.metrics import Metrics
from kivy.clock import Clock

# custom imports
from Shapes import Box, Round
from Sprite import Sprite, Background
from Items import Fire, Hat
from Man import Man
#from Sounds import MulitSound
#from Screens import GameOver, ScoreScreen

#set Window.size
from kivy.config import Config
Config.set('graphics', 'width', '340')
Config.set('graphics', 'heigt', '600')
#Config.set('graphics', 'position', 'custom')
#Config.set('graphics', 'left', '300')
#Config.set('graphics', 'top', '300')
Config.write()


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

class ScoreScreen(Widget):
    def __init__(self, time, scale, **kwargs):
        super().__init__(**kwargs)
        self.background = Background( source = 'images/backgroundMAC.png', scale = scale )
        self.add_widget( self.background )
        x, y = Window.size
        print('window size in Score Screen', x, y)
        self.message = Label(text="Congratulations Comrade!", pos = (x/4, y/2) )
        self.message2 = Label(text="You Win!", pos=(x/4, y/3), font_size='20sp' )
        self.message3 = Label(text="Completion time: {:03f}".format(time), pos=(x/3, y/5) )
        self.music = SoundLoader.load('audio/win_loop.wav')
        self.music.play()
        self.m1 = True
        self.m2 = True
        self.m3 = True
        
        #self.add_widget( self.message )
        #self.add_widget( self.message2 )
        
        self.counter = 0
        self.loaded = False
        self.ud = Clock.schedule_interval(self.update, 1.0/60.0)
        
    def update(self, dt):
        #print(self.counter)
        if self.counter < 300: # check if it's time to continue or not
            self.counter += 1
        elif not self.loaded: 
            self.loaded = True
            self.ud.cancel()

        if self.counter > 50 and self.m1: # draw win message
            self.m1 = False
            self.add_widget( self.message )
        elif self.counter > 120 and self.m2:
            self.m2 = False
            self.add_widget( self.message2 )
        elif self.counter > 200 and self.m3:
            self.m3 = False
            self.add_widget( self.message3 )


    def on_touch_down(self, touch):
        if self.loaded:
            parent = self.parent
            print('parent in GameOverWidget', parent)
            parent.remove_widget( self )
            self.music.stop()
            parent.add_widget( Game() )


class GameOver(Widget):
    def __init__(self, scale, **kwargs):
        super().__init__(**kwargs)
        self.background = Background( source = 'images/backgroundMAC.png', scale=scale )
        x,y = Window.size
        print('window size in Score Screen', x, y)
        self.message = Label(text="I'm sorry.", pos=(x/4, y/3) )
        self.message2 = Label(text="You're a rasict.", pos=(x/4, y/4), font_size='20sp' )
        self.message3 = Label(text="Game Over.", pos=(x/3, y/5) )
        self.music = SoundLoader.load('audio/beat1.wav')
        self.music.play()

        self.add_widget( self.background )
        self.add_widget( self.message )
        #self.add_widget( self.message2 )
        
        self.m1 = True
        self.m2 = True
        self.counter = 0

        self.loaded = False
        self.ud = Clock.schedule_interval(self.update, 1.0/60.0)
        #return self
        
    def update(self, dt):
        #print(self.counter)
        #if self.counter < 100:
        #    self.counter += 1
        #elif not self.loaded:
        #    self.loaded = True
        #    self.ud.cancel()

        if self.counter < 300: # check if it's time to continue or not
            self.counter += 1
        elif not self.loaded: 
            self.loaded = True
            self.ud.cancel()

        if self.counter > 100 and self.m1: # draw win message
            self.m1 = False
            self.add_widget( self.message2 )
        elif self.counter > 200 and self.m2:
            self.m2 = False
            self.add_widget( self.message3 )



    def on_touch_down(self, touch):
        if self.loaded:
            parent = self.parent
            print('parent in GameOverWidget', parent)
            parent.remove_widget( self )
            self.music.stop()
            parent.add_widget( Game() )


class Game(Widget):
    def __init__(self, **kwargs):
        print('info here', self.parent )
        super().__init__()
        print('info here', self.parent )
        self.music = SoundLoader.load('audio/indeed_vol1.wav')
        #self.music = SoundLoader.load('audio/walk-music-1.wav')
        self.music.play()
        self.background = Background(source= 'images/backgroundMAC.png', scale=props.scale )
        self.add_widget(self.background)

        ww, wh = Window.size
        #print('window size',ww, wh)
        #sw, sh = self.size
        #print('self size',ww, wh)
        #sx, sy = (self.width, self.height)
        #print('xx yy',sx, sy)

        self.fire = Fire( scale=props.scale, pos=(-ww*1/5, wh/10), angle=5 )
        self.add_widget( self.fire )
        #self.quit_to_menu = Button( text='back to menu', font_size=14 )
        #self.add_widget(self.quit_to_menu)
        #self.quit_to_menu.bind( on_press=self._on_quit )

        ##hat (ww*5/4, wh/10)
        self.hat = Hat(source='images/hat.png', scale=props.scale, pos=(ww*5/4, wh/10), angle=20)
        #self.rect_hat = Round(pos=self.hat.center, size=self.hat.size)
        self.rect_hat = Box(pos=self.hat.pos, size=self.hat.size)
        print('hat size', self.hat.size)
        #self.add_widget( self.rect_hat )
        self.add_widget( self.hat )


        ##man
        self.man = Man( props.scale, (ww/2, wh/2) )
        self.add_widget( self.man )

        #self.man_rect = Rectangle( pos=self.man.pos, size= self.man.size )
        #self.add_widget( self.man_rect )

        self.ud = Clock.schedule_interval(self.update, 1.0/60.0)
        ## status variables
        self.moving = False
        self.total_time = 0

    def _on_quit(self, *ignore):
        parent = self.parent
        print('parent in _on_quit()', parent)
        parent.remove_widget( self )
        #parent.add_widget( MainMenu() )
        parent.add_widget( GameOver(scale=props.scale) )
        self.ud.cancel()
        self.music.stop()

    def _on_win(self, *ignore):
        parent = self.parent
        print('parent in _on_quit()', parent)
        parent.remove_widget( self )
        #parent.add_widget( MainMenu() )
        parent.add_widget( ScoreScreen(time=self.hat.win_time, scale=props.scale) )
        self.ud.cancel()
        self.music.stop()
        #self.music.play()

    def messageScreen(self, f, args):
        parent = self.parent
        print('parent in messageScreen()', parent)
        parent.remove_widget( self )
        #parent.add_widget( MainMenu() )
        #parent.add_widget( ScoreScreen(self.hat.win_time) )
        print(args)
        parent.add_widget( f() )
        self.ud.cancel()
        self.music.stop()
         


    def update(self, dt):
        self.total_time += dt
        #print('total time', self.total_time)
        self.man.update()
        self.background.scroll(self.man.ihat)
        self.fire.update(self.man.ihat)
        #if self.hat.inhand:
        #    print('inhand', self.hat.inhand)
        #else:
        self.hat.update(self.man.ihat)
        #self.rect_hat.pos = self.hat.pos
        #self.rect_hat.update()
        if self.hat.collide_point( *self.fire.center ) and not self.hat.burning:
            #print( 'hat is burning' )
            self.hat.burn(self.total_time)


            #parent = self.parent
            #parent.remove_widget( self )
            #parent.add_widget( MainMenu() )
            #parent.add_widget( GameOver() )

    def on_touch_down(self, touch):
        if self.hat.onhead:
            self._on_quit()
            #self.messageScreen( GameOver, False )
        if self.hat.burnt:
            self._on_win()
        print(touch.profile)
        print('touch pos',touch.pos)
                #if 5 < touch.pos[0] < 95:
        edge = 20#self.man.width/2
            #if self.hat.collide_point(*touch.pos):
                #self.hat.inhand = True

        if self.hat.collide_point(*touch.pos):
            #if self.hat.inhand:
            if touch.is_double_tap:
                print('Touch is a Dobule tap')
                print(' - interval is', touch.double_tap_time)
                print(' - distance between previous is', touch.double_tap_distance)
                self.hat.toHand( (self.man.pos[0]+self.man.width, self.man.pos[1]+self.man.height/2) )
            elif self.hat.inhand:
                self.hat.inhand = False
                self.hat.moving = True
                touch.grab(self)
                print('hat leaving hand hat!')
            else:
                print('touch in hat, but its not in hand and not a double click!')
                
        elif edge < touch.pos[0] < Window.width-edge:
            self.man.move(touch.pos)
            print('touch out of hat')
            print('touch pos', touch.pos)

        else:
            print('touch out of bounds')
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            print('grab move')
            #new_hat_pos = (self.man.pos[0]+self.man.width, self.man.pos[1]+self.man.height/2)
            self.hat.move( touch_pos=touch.pos, target_pos=self.man.head, lock_on=False )


    def on_touch_up(self, touch):
        if touch.grab_current is self:
            print('grab up')
            ###if end position is on man's hand stop the hat...

            #new_hat_pos = (self.man.pos[0]+self.man.width, self.man.pos[1]+self.man.height/2)
            print('head pos:', self.man.head)
            self.hat.moving = False
            self.hat.move( touch_pos=touch.pos, target_pos=self.man.head )
            #self.hat.pos =  new_hat_pos
            touch.ungrab(self)

            # accept the up
            return True




class MainMenu(Widget):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        #self.add_widget(Sprite(source='images/background.png'))
        self.background = Sprite( source='images/background2.png', scale=props.scale )
        self.add_widget(self.background)
        self.music = SoundLoader.load('audio/song1.wav')
        self.music.play()
        #self.size = self.children[0].size
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
        self.music.stop()

    def _on_options(self, *ignore):
        print('options')
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget( Options() )


#    def on_touch_down(self, *ignore):
#        parent = self.parnet
#        parent.remove_widget(self)
#        parent.add_widget(Game())


class WalkApp(App):
    def build(self):
#        props.init()
        top = Widget()
        top.add_widget(Game())
        xxx = top.children[0]
        print('xxxxx', xxx.parent)

        #top.add_widget(MainMenu())
        return top

    def __len__(self):
        return 1

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
    WalkApp().run()
