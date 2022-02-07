
import pygame as pg
import sys
from os import path
from perso import player

TILESIZE = 64


class Heart(pg.sprite.Sprite):
    def __init__(self, x, y, game):
        pg.sprite.Sprite.__init__(self)
        self._layer = 9
        self.game = game
        self.image = pg.image.load("sprite/object/heart/heart_full.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = (x * TILESIZE)+10
        self.rect.y = (y * TILESIZE)+7

    def heart_collect(self):
        hits = pg.sprite.spritecollide(self, self.game.players, False)
        if hits:
            for player in hits:
                if player.health < player.max_health:
                    if (player.health + 2) > player.max_health:
                        player.set_health(1)
                        self.kill()
                    else :
                        player.set_health(2) 
                        self.kill()
        
    def update(self):
        self.heart_collect()