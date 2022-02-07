#------------------------#
# Made by Julien Vanherf #
#------------------------#

import pygame as pg
from color import *
from random import *
from tilemap import *
from os import path
from projectile import fire_ball
from projectile import arrow
vec = pg.math.Vector2

TILESIZE = 64


class Wall(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self._layer = 1
        self.image = pg.image.load("sprite/wall/wall1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Floor(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self._layer = 1
        nb = randint(1, 3)
        if nb == 1:
            self.image = pg.image.load(
                "sprite/floor/floor_1_1.png").convert_alpha()
        elif nb == 2:
            self.image = pg.image.load(
                "sprite/floor/floor_2_1.png").convert_alpha()
        elif nb == 3:
            self.image = pg.image.load(
                "sprite/floor/floor_3_1.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Door(pg.sprite.Sprite):
    def __init__(self, x, y, game, map, d, lvl, maps_list):
        pg.sprite.Sprite.__init__(self)
        self._layer = 1
        self.maps = maps_list
        self.image = [pg.image.load("sprite/wall/door1.png").convert_alpha(), pg.image.load("sprite/wall/door.png").convert_alpha()]
        self.image_o = [pg.image.load("sprite/wall/door_o_1.png").convert_alpha(), pg.image.load("sprite/wall/door_o.png").convert_alpha()]
        self.image = self.image[d]
        self.d = d
        self.game = game
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.lvl = lvl
        self.door_open = False
    
    def change_level(self):
        hits = pg.sprite.spritecollide(self, self.game.players, False)
        if hits:
            for player in hits:
                self.lvl += 1
                game_folder = path.dirname(__file__)
                self.game.map = Map(path.join(game_folder, self.maps[self.lvl]))
                for elem in self.game.all_sprites:
                    elem.kill()
                self.tmp_player = self.game.player
                self.m_change = True
                self.game.lvl = self.lvl
                self.game.new(self.m_change, self.game.select_player.player)
                self.door_open = False
                

    def update(self):
        if len(self.game.mobs) == 0: 
            self.door_open = True
        
        if self.door_open:
            self.change_level()
            self.image = self.image_o[self.d]
        

class Ladder(pg.sprite.Sprite):
    def __init__(self, x, y, game):
        pg.sprite.Sprite.__init__(self)
        self._layer = 1
        self.image = pg.image.load("sprite/floor/floor_1_1.png").convert_alpha()
        self.image_o = pg.image.load("sprite/floor/floor_ladder.png").convert_alpha()
        self.game = game
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    
    def change_stage(self):
        hits = pg.sprite.spritecollide(self, self.game.players, False)
        if hits:
            for player in hits:
                self.game.stage += 1 
                self.game.maps = self.game.stage_list[self.game.stage-1]
                print(self.game.stage)

                game_folder = path.dirname(__file__)
                self.game.map = Map(path.join(game_folder, self.game.maps[0]))
                self.tmp_player = self.game.player
                self.m_change = True
                self.game.lvl = 0
                self.game.new(self.m_change, self.game.select_player.player)

    def update(self):
        if len(self.game.mobs) == 0: 
            self.image = self.image_o
            self.change_stage()
    
class Rock(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self._layer = 2
        nb = randint(1, 3)
        if nb == 1:
            self.image = pg.image.load("sprite/floor/rock.png").convert_alpha()
        elif nb == 2:
            self.image = pg.image.load("sprite/floor/rock2.png").convert_alpha()
        elif nb == 3:
            self.image = pg.image.load("sprite/floor/rock3.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Spike(pg.sprite.Sprite):
    def __init__(self, x, y, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self._layer = 2
        self.sprites = [pg.image.load("sprite/spike/floor_spikes_anim_f0.png").convert_alpha(), pg.image.load("sprite/spike/floor_spikes_anim_f1.png").convert_alpha(), pg.image.load("sprite/spike/floor_spikes_anim_f2.png").convert_alpha(), pg.image.load("sprite/spike/floor_spikes_anim_f3.png").convert_alpha()]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.cooldown = 0
        self.state = 0
    
    def attack(self):
        hits = pg.sprite.spritecollide(self, self.game.players, False)
        if hits and not self.game.player.fly:
            if pg.time.get_ticks() - self.cooldown >= 700:
                self.game.player.health -= 0.5
                self.cooldown = pg.time.get_ticks()
    
    def check_state(self):
        if self.state == 1:
            self.attack()

    def animator(self):
        self.current_sprite += 0.05

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        
        if self.current_sprite >= 3:
            self.state = 1
        else :
            self.state = 0

        self.image = self.sprites[int(self.current_sprite)]
    
    def update(self):
        self.check_state()
        self.animator()
    
class Wall_Hole(pg.sprite.Sprite):
    def __init__(self, x, y, game, fire_ball):
        pg.sprite.Sprite.__init__(self)
        self._layer = 1
        self.image = pg.image.load("sprite/wall/wall_hole/wall_hole.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.game = game
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.cooldown = 0
        self.projectile = fire_ball
    
    def shoot(self):
        time = randrange(600, 900)
        if pg.time.get_ticks() - self.cooldown >= time:
            self.projectile.add(arrow.Arrow((self.x*64)+32, (1.01*64)+10, self.game, 'b', 1))
            self.cooldown = pg.time.get_ticks()
    
    def update(self):
        self.shoot()

class Win_Ladder(pg.sprite.Sprite):
    def __init__(self, x, y, game):
        pg.sprite.Sprite.__init__(self)
        self._layer = 1
        self.image = pg.image.load("sprite/floor/floor_1_1.png").convert_alpha()
        self.image_o = pg.image.load("sprite/floor/floor_ladder.png").convert_alpha()
        self.game = game
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    
    def check_win(self):
        hits = pg.sprite.spritecollide(self, self.game.players, False)
        if hits:
            for player in hits:
                self.game.curr_menu = self.game.win
                self.game.curr_menu.display_menu()

    def update(self):
        if len(self.game.mobs) == 0: 
            self.image = self.image_o
            self.check_win()

class Hole(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self._layer = 2
        nb = randint(1, 3)
        self.image = pg.image.load("sprite/floor/hole.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    