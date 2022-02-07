
import pygame as pg
import sys
from os import path
from color import *
from random import randint
from perso import player
import configparser

TILESIZE = 64
config = configparser.ConfigParser()
config.read("config.ini")


class Coin(pg.sprite.Sprite):
    def __init__(self, x, y, game, coin_value):
        pg.sprite.Sprite.__init__(self)
        self._layer = 9
        self.game = game
        self.sprites_y = [pg.image.load("sprite/object/coins/coin1.png").convert_alpha(), pg.image.load("sprite/object/coins/coin2.png").convert_alpha(), pg.image.load("sprite/object/coins/coin3.png").convert_alpha(), pg.image.load("sprite/object/coins/coin4.png").convert_alpha()]
        self.sprites_r = [pg.image.load("sprite/object/coins/coin1_r.png").convert_alpha(), pg.image.load("sprite/object/coins/coin2_r.png").convert_alpha(), pg.image.load("sprite/object/coins/coin3_r.png").convert_alpha(), pg.image.load("sprite/object/coins/coin4_r.png").convert_alpha()]
        self.sprites_g = [pg.image.load("sprite/object/coins/coin1_g.png").convert_alpha(), pg.image.load("sprite/object/coins/coin2_g.png").convert_alpha(), pg.image.load("sprite/object/coins/coin3_g.png").convert_alpha(), pg.image.load("sprite/object/coins/coin4_g.png").convert_alpha()]
        self.current_sprite = 0
        self.image = self.sprites_y[self.current_sprite]
        self.rect = self.image.get_rect()
        self.c_value = coin_value
        self.x = x
        self.y = y 
        self.rect.x = (x * TILESIZE) + self.image.get_width()/2
        self.rect.y = (y * TILESIZE) + self.image.get_height()/2
        self.font_name = 'font/dogicapixel.ttf'

    def coin_collect(self):
        hits = pg.sprite.spritecollide(self, self.game.players, False)
        if hits:
            for player in hits:
                if player.coin != 99:
                    player.set_money(self.c_value) 
                    self.game.c_sound.play()
                    self.kill()
                
    def animator(self):
        if self.c_value == 1:
            self.current_sprite += 0.1

            if self.current_sprite >= len(self.sprites_r):
                self.current_sprite = 0
            
            self.image = self.sprites_r[int(self.current_sprite)]

        elif self.c_value == 2:
            self.current_sprite += 0.1

            if self.current_sprite >= len(self.sprites_g):
                self.current_sprite = 0
            
            self.image = self.sprites_g[int(self.current_sprite)]
        else :
            self.current_sprite += 0.1

            if self.current_sprite >= len(self.sprites_y):
                self.current_sprite = 0
            
            self.image = self.sprites_y[int(self.current_sprite)]
        

    def update(self):
        self.animator()
        self.coin_collect()
