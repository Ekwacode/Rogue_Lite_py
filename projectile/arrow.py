import pygame as pg
import sys
from os import path
from color import *
from random import *
from perso import player
from perso import mob
from objects import coin
from pygame import mixer
vec = pg.math.Vector2

TILESIZE = 64


class Arrow(pg.sprite.Sprite):
    def __init__(self, x, y, game, direc, attack_point):
        self.pos = vec(x, y)
        self.direc = direc
        self.game = game
        self._layer = 10
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("sprite/projectile/arrow.png").convert_alpha()
        self.rect = self.image.get_rect(center = (x,y))
        self.cooldown = 0
        self.damage = attack_point
        self.v_a = 20
    
    def shoot_dir(self):
        if self.direc == 'd':
            self.rect.x += self.v_a

        elif self.direc == 'g':
            self.rect.x -= self.v_a
        
        elif self.direc == 'h':
            self.rect.y -= self.v_a
        
        elif self.direc == 'b':
            self.rect.y += self.v_a
        
        elif self.direc == 'a':
            self.rect.x -= self.v_a
            self.rect.y -= self.v_a

        elif self.direc == 'e':
            self.rect.x += self.v_a
            self.rect.y -= self.v_a
        
        elif self.direc == 'w':
            self.rect.x += self.v_a
            self.rect.y += self.v_a
        
        elif self.direc == 'c':
            self.rect.x -= self.v_a
            self.rect.y += self.v_a

    def collide_with_walls(self):
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
            self.v_a = 10
            self.shoot_dir()
        else:        
            self.pos += self.direc
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y
        self.collide_with_walls()
        self.attack()