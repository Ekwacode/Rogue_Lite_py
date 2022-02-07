import pygame as pg
import sys
from os import path
from color import *
from random import *
from perso import player
from perso import mob
vec = pg.math.Vector2

TILESIZE = 64


class Ball(pg.sprite.Sprite):
    def __init__(self, x, y, game, vect):
        self.pos = vec(x, y)
        self.vect = vect
        self.game = game
        self._layer = 10
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("sprite/projectile/energy_ball.png").convert_alpha()
        self.image = self.image
        self.rect = self.image.get_rect(center = (x,y))
        self.cooldown = 0
        self.v_b = 10
        self.collide = True
        self.damage = 1

    def collide_with_walls(self, collide):
        hits_wall = pg.sprite.spritecollide(self, self.game.walls, False)
        hit_rock = pg.sprite.spritecollide(self, self.game.rocks, False)
        if hits_wall or hit_rock:
            self.kill()
    
    def attack(self):
        hits = pg.sprite.spritecollide(self, self.game.players, False)
        for player in hits:
            player.health -= self.damage
            self.kill()

    def update(self):
        self.pos += self.vect
        print(self.pos)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.collide_with_walls(self.collide)
        self.attack()