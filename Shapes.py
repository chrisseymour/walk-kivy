#shapes.py
#Round and Box classes

from kivy.graphics import Color, Rectangle, InstructionGroup
from kivy.graphics import Line
from kivy.uix.widget import Widget
from math import sqrt

class Box(Widget):
    def __init__(self, pos, size):
        super().__init__()
        self.pos = pos
        self.size = size
        #
        self.grp = self.group(1)
        self.canvas.add( self.grp)
#        with self.canvas:
            #self.canvas.add( xyz )

            #Color(1, 0, 0)
            #self.nrect = Rectangle( pos=pos, size=size )

    def group(self, color):
        rgb = InstructionGroup()
        color = Color(1, 1, 0)
        xyz = color
        rgb.add(xyz)
        rgb.add(Rectangle(pos=self.pos, size=self.size) )
        return rgb



    def update(self):
        self.canvas.remove( self.grp )
        self.grp = self.group( 0 )
        self.canvas.add( self.grp )


class Round(Widget):
    def __init__(self, pos, size):
        super().__init__()
        self.pos = pos
        self.size = size
        self.grp = self.group(1)
        self.canvas.add( self.grp )

    def group(self, color):
        rgb = InstructionGroup()
        color = Color(1, 0, 0)
        xyz = color
        rgb.add(xyz)
        radius = sqrt(sqrt(sum([x*x for x in self.size])))
        rgb.add(Line(circle=(self.pos[0], self.pos[1], radius ) ) )
        return rgb

    def update(self):
        self.canvas.remove( self.grp )
        self.grp = self.group( 0 )
        self.canvas.add( self.grp )

