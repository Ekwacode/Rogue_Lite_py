import pygame as pg
import sys
from os import path
from color import *
from random import *
from perso import player
from objects import heart
from perso.mob import bad_chest
from objects import coin

TILESIZE = 64


class Chest(pg.sprite.Sprite):
    def __init__(self, x, y, game, coins):
        pg.sprite.Sprite.__init__(self)
        self._layer = 5
        self.game = game
        self.sprites_c = [pg.image.load("sprite/object/chest/chest_f0.png").convert_alpha(),pg.image.load("sprite/object/chest/chest_f_empty.png").convert_alpha()]
        self.current_sprite = 0
        self.image = self.sprites_c[self.current_sprite]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.coins = coins
        self.c_open = False
        self.cooldown = 0

    def chest_col(self):
        hits = pg.sprite.spritecollide(self, self.game.players, False)
        if hits:
            while self.current_sprite < 2:
                self.animator()
                
    def animator(self):
        self.current_sprite += 1      
        if self.current_sprite < len(self.sprites_c):
            self.image = self.sprites_c[int(self.current_sprite)]
        else:
            self.state()
    
    def state(self):
        nb = randrange(0,5)
        if nb == 0:
            m = bad_chest.Bad_Chest(self.x,self.y, self.game.player, self.game, self.game.coins, False)
            self.game.mobs.add(m)
            self.kill()


        else :
            if nb == 3 or nb == 4:
                h = heart.Heart(self.x, self.y, self.game)
                self.game.hearts.add(h)
            else:
                i = 0
                while i < nb:
                    self.c_value = randrange(1,3)
                    c = coin.Coin(self.x, self.y, self.game, self.c_value)
                    self.coins.add(c)
                    i += 1

    def update(self):
        self.chest_col()
