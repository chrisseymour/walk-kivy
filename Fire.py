# Fire.py

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


