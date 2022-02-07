#------------------------#
# Made by Julien Vanherf #
#------------------------#

import pygame as pg

TILESIZE = 64

class Death_Effect(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self._layer = 1
        self.sprite = [pg.image.load("sprite/effect/death_explo_f0.png").convert_alpha(), pg.image.load("sprite/effect/death_explo_f1.png").convert_alpha(), pg.image.load("sprite/effect/death_explo_f2.png").convert_alpha(), pg.image.load("sprite/effect/death_explo_f3.png").convert_alpha()]
        self.current_sprite = 0
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def death_anim(self):
        self.current_sprite += 0.1     
        if self.current_sprite < len(self.sprite):
            self.image = self.sprite[int(self.current_sprite)]
        
        if int(self.current_sprite) == 4:
            self.kill()

    def update(self):
        self.death_anim()