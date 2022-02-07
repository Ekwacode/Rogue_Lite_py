import pygame as pg
import sys
from os import path
from color import *
from random import *
from perso import player
from perso import mob
vec = pg.math.Vector2

TILESIZE = 64


class Brain(pg.sprite.Sprite):
    def __init__(self, x, y, game, direc):
        self.pos = vec(x, y)
        self.direc = direc
        self.game = game
        self._layer = 10
        pg.sprite.Sprite.__init__(self)
        self.image = [pg.image.load("sprite/projectile/brain_0.png").convert_alpha(),pg.image.load("sprite/projectile/brain_1.png").convert_alpha(),pg.image.load("sprite/projectile/brain_3.png").convert_alpha(),pg.image.load("sprite/projectile/brain_4.png").convert_alpha(), pg.image.load("sprite/projectile/brain_5.png").convert_alpha()]
        self.image = self.image[randrange(0,5)]
        self.rect = self.image.get_rect(center = (x,y))
        self.cooldown = 0
        self.v_b = 10
        self.collide = True
        if type(self.direc) == str:
            self.damage = 2
        else:
            self.damage = 1
    
    def shoot_dir(self):
        if self.direc == 'd':
            self.rect.x += self.v_b

        elif self.direc == 'g':
            self.rect.x -= self.v_b
        
        elif self.direc == 'h':
            self.rect.y -= self.v_b
        
        elif self.direc == 'b':
            self.rect.y += self.v_b
        
        elif self.direc == 'a':
            self.rect.x -= self.v_b
            self.rect.y -= self.v_b

        elif self.direc == 'e':
            self.rect.x += self.v_b
            self.rect.y -= self.v_b
        
        elif self.direc == 'w':
            self.rect.x += self.v_b
            self.rect.y += self.v_b
        
        elif self.direc == 'c':
            self.rect.x -= self.v_b
            self.rect.y += self.v_b

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
        if type(self.direc) == str:
            self.shoot_dir()
        else:
            self.pos += self.direc
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y
        self.collide_with_walls(self.collide)
        self.attack()