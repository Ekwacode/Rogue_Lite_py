
import pygame as pg
import sys
from os import path
from color import *
from random import randint
from perso import player

TILESIZE = 64


class Spell_book(pg.sprite.Sprite):
    def __init__(self, x, y, game):
        pg.sprite.Sprite.__init__(self)
        self._layer = 9
        self.game = game
        self.image = pg.image.load("sprite/object/spell_book/spelbook_1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.rect.x = (x * TILESIZE) + 6
        self.rect.y = (y * TILESIZE) + 6
        self.font_name = 'font/Minecraft.ttf'
        self.price = 0

    def book_collect(self):
        hits = pg.sprite.spritecollide(self, self.game.players, False)
        if hits:
            for player in hits:
                if player.coin >= self.price:
                    player.coin = player.coin - self.price
                    self.effect()
                    self.kill()

    def draw_price(self):
        self.font_a = pg.font.Font(self.font_name, 35)
        self.f_price = str(self.price)
        textsurface = self.font_a.render(self.f_price, False, (255, 255, 255))
        self.game.window.blit(textsurface,(self.rect.x+6,self.rect.y+50))

    def effect(self):
        pass
    
    def update(self):
        self.draw_price
        self.book_collect()

