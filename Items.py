# -Fire.py-
# Items.py
from math import sqrt
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.atlas import Atlas
from Sprite import Sprite

class Fire(Widget):
    def __init__(self, scale, pos, angle):
        super().__init__(pos=pos)
        self.scale = scale
        source = 'images/logs.png'
        #self.angle = angle
        self.images = Atlas('images/fire.atlas')
        self.keys = list( self.images.textures.keys() )
        print('fire keys list', self.keys )
        #self.images = Atlas('images/man.atlas')
        self.image = Sprite(texture=self.images[self.keys[0]], scale=self.scale, pos=pos)
        #self.image = Sprite(source=self.images[self.kys[0]], scale=self.scale, pos=pos)
        self.size = self.image.size
        self.add_widget( self.image )
        #self.inhand = False

    def moveToHand(self, pos):
        self.pos = pos
        self.inhand = True
        #self.image.pos = self.pos

    def destroyHat(self):
        self.win = True
        return True

    def update(self, ihat):
        #print('hat pos',self.pos)
        if ihat > 0:
            self.x -= self.scale
        elif ihat < 0:
            self.x += self.scale
        self.image.pos = self.pos


class Hat(Widget):
    def __init__(self, source, scale, pos, angle):
        super().__init__(pos=pos)
        self.scale = scale
        self.images = Atlas('images/hat.atlas')  ## Atlas initialization
        self.kys = list( self.images.textures.keys() )  ## atlas keys into a list
        print('hat keys list', self.kys )
        self.image = Sprite(source=source, scale=self.scale, pos=pos)
        self.size = self.image.size
        self.add_widget( self.image )
        self.inhand = False
        self.onhead = False
        self.moving = False
        #burning status
        self.burning = False
        self.burnt = False
        self.burn_counter = 0
        self.sprite = 0

    def burn(self, time):
        self.win_time = time
        self.burnt = True
        burn = 'images/hat_burn.png'
        self.remove_widget(self.image)
        self.image = Sprite(source=burn, scale=self.scale, pos=self.pos)
        self.add_widget( self.image )
        
    def toHand(self, new_pos):
        self.center = new_pos
        self.inhand = True
        print('hat in hand', self.inhand)

    def toHead(self, new_pos):
        self.center = new_pos
        self.onhead = True
        print('hat on head', self.onhead)

    def move(self, touch_pos, target_pos, lock_on=True):
        self.center = touch_pos
        a = sqrt(sum([x*x for x in self.center]))
        b = sqrt(sum([x*x for x in target_pos]))
        print('a',a,'b',b)
        print('abs(a-b)',abs(a-b))

        limit = 15
        if abs(a-b) < limit and lock_on:
            self.toHead( target_pos )
            
        #self.pos = pos
        #self.inhand = True
        #self.image.pos = self.pos

    def update(self, ihat):
        #print('hat pos',self.pos)
        #print('hat inhand:', self.inhand)
        if ihat > 0:
            if self.onhead or self.inhand:
                self.x += 0.5*self.scale
            else:
                self.x -= self.scale
        elif ihat < 0:
            if self.onhead or self.inhand:
                self.x -= 0.5*self.scale
            else:
                self.x += self.scale
        if  (not self.inhand) and  (not self.onhead) and self.center[1] > Window.height/8 and (not self.moving):
            self.y -= self.scale
        
        self.image.pos = self.pos
"""
        if self.burnt:
            self.image = self.images['hat_burnt-final']
        elif self.burning and self.burn_counter < 200:
            if self.burn_counter%40 == 0:
                self.sprite += 1
                self.image = self.images[ self.keys[self.sprite] ]
            self.burn_counter += 1
            print('burn counter {}, sprite {}'.format(self.burn_counter, self.sprite) )
        else:
            self.burning = False
            self.burnt = True
"""

