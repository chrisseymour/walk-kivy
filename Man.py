#Man.py

from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.atlas import Atlas
from Sprite import Sprite


class Man(Sprite):
    def __init__(self, scale, pos):
        self.scale = scale
        #self.images = SpriteAtlas('images/man.atlas')
        self.images = Atlas('images/man.atlas')
        self.scale = scale
        w, h = pos[0]+self.images['man-stop'].width/2, pos[1]-self.images['man-stop'].height/2
        w, h = self.width/2, self.height/2
        print('man init', pos, w, h)
        #w, h, = pos[0]-w/2, pos[1]-h/2
        print('man init', pos, w, h)
        super().__init__(texture=self.images['man-stop'], scale=self.scale, pos=(w,h) )

        self.keys = list(  self.images.textures.keys( ) )

        ks = 'man-left man-mid man-right man-mid'.split()
        ksl = 'manleft-left manleft-mid manleft-right manleft-mid'.split()
        self.walk = [self.images[k] for k in ks]
        self.walk_left = [self.images[k] for k in ksl]
        #self.footstep = SoundLoader.load('audio/Footstep.wav')
        self.fskeys = 'footstep-0.wav footstep-1.wav footstep-2.wav footstep-3.wav'.split()
        self.footstep = SoundLoader.load('audio/footstep-0.wav')
        #print([x for x in self.walk])
        #fp = self.images['man-left'].flip_horizontal()
        ### set animation based on veloicity params instead
        ###    (implement later)
        self.moving = False
        self.stopped = True
        self.keynum = 0
        self.ihat = 0
        self.counter = 0

    @property
    def head(self):
        x = self.x+self.width/3
        y = self.y+self.height*9/10
        return x, y

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
                self.footstep.play()
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
            print('x', self.x)
            #print('man.counter', self.counter)
            if self.ihat > 0 and self.center[0]<self.finalpos[0]:# and self.right < Window.width-20:
                self.x += 0.7 * self.scale
                self.animate()
            elif self.ihat < 0 and self.center[0]>self.finalpos[0]:# and self.x > 20: 
                self.x -= 0.7 * self.scale
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

#if __name__ == '__main__':
    #Man = Man('images/logs.png', 1, (10, 10) )
