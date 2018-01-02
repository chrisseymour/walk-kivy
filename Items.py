# -Fire.py-
# Items.py
from math import sqrt
from kivy.uix.widget import Widget
from Sprite import Sprite

class Fire(Widget):
    def __init__(self, scale, pos, angle):
        super().__init__(pos=pos)
        self.scale = scale
        source = 'images/logs.png'
        #self.angle = angle
        self.image = Sprite(source=source, scale=self.scale, pos=pos)
        self.size = self.image.size
        self.add_widget( self.image )
        self.inhand = False

    def moveToHand(self, pos):
        self.pos = pos
        self.inhand = True
        #self.image.pos = self.pos

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
        #self.angle = angle
        self.image = Sprite(source=source, scale=self.scale, pos=pos)
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
            self.x -= self.scale
        elif ihat < 0:
            self.x += self.scale
        self.image.pos = self.pos

