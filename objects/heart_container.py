
import pygame as pg
import sys
from os import path
from perso import player

TILESIZE = 64


class Heart_container(pg.sprite.Sprite):
    def __init__(self, x, y, game):
        pg.sprite.Sprite.__init__(self)
        self._layer = 9
        self.game = game
        self.image = pg.image.load("sprite/object/heart/heart_empty.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = (x * TILESIZE)+10
        self.rect.y = (y * TILESIZE)+7

    def heart_collect(self):
        hits = pg.sprite.spritecollide(self, self.game.players, False)
        if hits:
            for player in hits:
                if player.max_health < 20:
                    player.set_max_health(2)
                    self.kill()

        
    def update(self):
        self.heart_collect()