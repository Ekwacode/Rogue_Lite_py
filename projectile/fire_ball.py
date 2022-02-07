import pygame as pg
import sys
from os import path
from color import *
from random import *
from perso import player
from perso import mob
from objects import coin
from pygame import mixer
import configparser
vec = pg.math.Vector2

TILESIZE = 64
config = configparser.ConfigParser()
config.read("config.ini")


class Fire_ball(pg.sprite.Sprite):
    def __init__(self, x, y, game, direc, attack_point, projectile_speed):
        self.direc = direc
        self.game = game
        self._layer = 10
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("sprite/fire_ball/fb_1.png").convert_alpha()
        self.rect = self.image.get_rect(center = (x,y))
        self.cooldown = 0
        self.damage = attack_point
        self.v_fb = projectile_speed
        self.game.fb_sound.play()
    
    def shoot_dir(self):
        if self.direc == 'd':
            self.rect.x += self.v_fb

        elif self.direc == 'g':
            self.rect.x -= self.v_fb
        
        elif self.direc == 'h':
            self.rect.y -= self.v_fb
        
        elif self.direc == 'b':
            self.rect.y += self.v_fb

    def collide_with_walls(self):
        hits_wall = pg.sprite.spritecollide(self, self.game.walls, False)
        hit_rock = pg.sprite.spritecollide(self, self.game.rocks, False)
        if hits_wall or hit_rock:
            self.kill()
    
    def attack(self):
        hits = pg.sprite.spritecollide(self, self.game.mobs, False)
        for mob in hits:
            self.game.hit_sound.play()
            mob.health -= self.damage
            self.kill()

    def update(self):
        self.shoot_dir()
        self.collide_with_walls()
        self.attack()