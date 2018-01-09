# Items.py
from math import sqrt
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.atlas import Atlas
from Sprite import Sprite
from kivy.core.audio import SoundLoader

class Fire(Widget):
    def __init__(self, scale, pos, angle):
        super().__init__(pos=pos)
        self.scale = scale
        source = 'images/logs.png'
        #self.angle = angle
        self.images = Atlas('images/fire.atlas')
        self.keys = list( self.images.textures.keys() )
        print('fire keys list', self.keys )
        self.keys = 'fire-04 fire-05'.split()
        print('fire keys list', self.keys )
        #self.images = Atlas('images/man.atlas')
        self.image = Sprite(texture=self.images[self.keys[0]], scale=self.scale, pos=pos)
        #self.image = Sprite(source=self.images[self.kys[0]], scale=self.scale, pos=pos)
        self.size = self.image.size
        self.add_widget( self.image )
        #self.inhand = False
        self.burn_counter = 0
        self.sprite = 0

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
            self.x -= 1.2*self.scale
        elif ihat < 0:
            self.x += 1.2*self.scale
        self.image.pos = self.pos
        
        if self.burn_counter%25 == 0:
            self.sprite += 1
            if self.sprite >= len(self.keys):
                self.sprite = 0
            self.image.texture = self.images[ self.keys[self.sprite] ]
            #print('fire burn counter {}, sprite {}'.format(self.burn_counter, self.sprite) )
        self.burn_counter += 1


class Hat(Widget):
    def __init__(self, source, scale, pos, angle):
        super().__init__(pos=pos)
        self.scale = scale
        self.images = Atlas('images/hat.atlas')  ## Atlas initialization
        self.keys = list( self.images.textures.keys() )  ## atlas keys into a list
        print('keys in Hat',self.keys)
        self.kys = ( 'hat_burnt0', 'hat_burnt1', 'hat_burnt2', 'hat_burnt3', 
                'hat_burnt4', 'hat_burnt-final')
        print('hat keys list', self.kys )
        self.image = Sprite(texture=self.images['hat'], scale=self.scale, pos=pos)
        #self.image = Sprite(source=source, scale=self.scale, pos=pos)
        self.size = self.image.size
        self.add_widget( self.image )
        self.inhand = False
        self.onhead = False
        self.onhead_timer = 0
        self.moving = False
        #burning status
        self.burning = False
        self.burnt = False
        self.burn_counter = 0
        self.sprite = 0
        self.animation_value = int(200/(len(self.kys)-1))
        print('animation value', self.animation_value)
        self.vy = 0
        self.combust = SoundLoader.load('audio/combust-both.wav')


    def burn(self, time):
        if not self.burning:
            self.win_time = time
            self.burning = True
            self.combust.play()
            print('win time:', self.win_time)
        #burn = 'images/hat_burn.png'
        #self.remove_widget(self.image)
        #self.image = Sprite(source=burn, scale=self.scale, pos=self.pos)
        #self.add_widget( self.image )
        
    def toHand(self, new_pos):
        self.center = new_pos
        self.inhand = True
        print('hat in hand', self.inhand)

    def toHead(self, new_pos):
        self.center = new_pos
        self.onhead = True
        print('hat on head', self.onhead)

    def move(self, touch_pos, target_pos, lock_on=True):
        '''drop the item in a spot, if it's within a certain range, stop it'''
        self.center = touch_pos
        a = sqrt(sum([x*x for x in self.center]))
        b = sqrt(sum([x*x for x in target_pos]))
        print('a', a, 'b', b)
        print('abs(a-b)', abs(a-b))

        limit = 25
        if abs(a-b) < limit and lock_on:
            self.toHead( target_pos )
            
        #self.pos = pos
        #self.inhand = True
        #self.image.pos = self.pos

    def update(self, ihat):
        '''if ihat is non-zero, move the hat'''
        #print('hat pos',self.pos)
        #print('hat inhand:', self.inhand)
        if ihat > 0: #make one and use ihat as a multiplier
            if self.onhead or self.inhand:
                self.x += 0.7*self.scale
            else:
                self.x -= 1.2*self.scale
        elif ihat < 0:
            if self.onhead or self.inhand:
                self.x -= 0.7*self.scale
            else:
                self.x += 1.2*self.scale

        if  (not self.inhand) and  (not self.onhead) and self.center[1] > Window.height/8 and (not self.moving):
            self.y -= self.scale + self.vy*self.scale
            self.vy += 0.4*self.scale
        else:
            self.vy = 0

        self.image.pos = self.pos #update hat position
        ## check if hat is on fire, if it is, start burn animation 
        if self.burning and self.burn_counter < 201-self.animation_value:
            if self.burn_counter%self.animation_value == 0:
                self.sprite += 1
                self.image.texture = self.images[ self.kys[self.sprite] ]
            self.burn_counter += 1
            #print('hat burn counter {}, sprite {}'.format(self.burn_counter, self.sprite) )
        elif self.burning and not self.burnt: ## if done burning, change status of hat
            print('burnt')
            self.burning = False
            self.burnt = True
            self.image.texture = self.images['hat_burnt-final']

        if self.onhead:
            self.onhead_timer += 1

        #elif self.burnt:
            #self.image.texture = self.images['hat_burnt-final']
        

