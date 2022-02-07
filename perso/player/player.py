import pygame as pg
from color import *
from random import randint
from perso.mob import mob
from projectile import fire_ball
from pygame import mixer

vec = pg.math.Vector2

TILESIZE = 64


class Player(pg.sprite.Sprite):
    def __init__(self, game, fire_ball):
        self.projectile = fire_ball
        self.time = 0
        self.cooldown = 500
        self._layer = 10
        self.max_health = 10
        self.health = 10
        self.coin = 0
        self.attack_point = 2
        self.player_speed = 5
        self.is_alive = True
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game = game
        self.sprites_idle_l = [pg.image.load("sprite/player/mage/mage_idle_l_f0.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_idle_l_f1.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_idle_l_f2.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_idle_l_f3.png").convert_alpha()]
        self.sprites_move_l = [pg.image.load("sprite/player/mage/mage_walk_l_f0.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_walk_l_f1.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_walk_l_f2.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_walk_l_f3.png").convert_alpha()]
        self.sprites_idle_r = [pg.image.load("sprite/player/mage/mage_idle_r_f0.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_idle_r_f1.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_idle_r_f2.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_idle_r_f3.png").convert_alpha()]
        self.sprites_move_r = [pg.image.load("sprite/player/mage/mage_walk_r_f0.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_walk_r_f1.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_walk_r_f2.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_walk_r_f3.png").convert_alpha()]
        self.hearts = [pg.image.load("sprite/ui/heart_full.png").convert_alpha(), pg.image.load("sprite/ui/heart_half.png").convert_alpha(), pg.image.load("sprite/ui/heart_empty.png").convert_alpha()]
        self.current_sprite = 0
        self.image = self.sprites_idle_l[self.current_sprite]
        self.move = False
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(0, 0) * TILESIZE
        self.direc = ''
        self.direc_idle = 'd'
        self.debug = False
        self.projectile_speed = 15
        self.fly = False

    def set_position(self, x, y):
        x = (x * TILESIZE) + self.image.get_width()/2
        y = (y * TILESIZE) - self.image.get_height()/4
        self.pos = vec(x, y)
    
    def set_money(self, coin_value):
        self.coin += coin_value
    
    def set_health(self, value):
        self.health += value
    
    def set_max_health(self, value):
        self.max_health += value

    def action(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_q]:
            self.vel.x = -self.player_speed
            self.move = True
            self.direc = 'g'
            self.direc_idle = 'g'
        if keys[pg.K_d]:
            self.vel.x = self.player_speed
            self.move = True
            self.direc = 'd'
            self.direc_idle = 'd'
        if keys[pg.K_z]:
            self.vel.y = -self.player_speed
            self.move = True
        if keys[pg.K_s]:
            self.vel.y = self.player_speed
            self.move = True
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
        
        if keys[pg.K_p] and keys[pg.K_m]:
            self.debug = True

    def debug_men(self):
        if self.debug:
            keys = pg.key.get_pressed()
            if keys[pg.K_SPACE]:
                for orc in self.game.mobs:
                    orc.health = 0

            if keys[pg.K_v]:
                self.coin = 99 

            if keys[pg.K_n]:
                self.health = 0
            
            if keys[pg.K_k]:
                self.game.boss_list = []

    def shooting(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.direc = 'd'
            self.direc_idle = 'd'
            self.shoot(self.direc, self.attack_point)

        if keys[pg.K_LEFT]:
            self.direc = 'g'
            self.direc_idle = 'g'
            self.shoot(self.direc, self.attack_point)

        if keys[pg.K_UP]:
            self.direc = 'h'
            self.shoot(self.direc, self.attack_point)

        if keys[pg.K_DOWN]:
            self.direc = 'b'
            self.shoot(self.direc, self.attack_point)
    

    def shoot(self, direc, attack_point):
        self.attack_point = attack_point
        self.direc = direc
        if pg.time.get_ticks() - self.time >= self.cooldown:
            self.projectile.add(fire_ball.Fire_ball(self.pos.x+25, self.pos.y+25, self.game, self.direc, self.attack_point, self.projectile_speed))
            self.time = pg.time.get_ticks()

    def collide_with_walls(self, dir):
        if dir == 'x':
            if self.fly:
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
            else :
                hits = pg.sprite.spritecollide(self, self.game.hurts, False)

            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            if self.fly:
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
            else :
                hits = pg.sprite.spritecollide(self, self.game.hurts, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def animator(self, player_speed):
        self.player_speed = player_speed
        if self.move:
            # Gestion animation Mouvement
            if self.direc == 'g':
                self.current_sprite += self.player_speed/50

                if self.current_sprite >= len(self.sprites_move_l):
                    self.current_sprite = 0
                
                self.image = self.sprites_move_l[int(self.current_sprite)]

                self.move = False

            elif self.direc == 'd':
                self.current_sprite += self.player_speed/50

                if self.current_sprite >= len(self.sprites_move_r):
                    self.current_sprite = 0
                
                self.image = self.sprites_move_r[int(self.current_sprite)]

                self.move = False

            else:
                self.current_sprite += self.player_speed/50

                if self.current_sprite >= len(self.sprites_idle_r):
                    self.current_sprite = 0
                
                self.image = self.sprites_move_r[int(self.current_sprite)]

                self.move = False
        
        else:
            # Gestion animation Idle
            if self.direc_idle == 'd':
               
                self.current_sprite += 0.1

                if self.current_sprite >= len(self.sprites_idle_r):
                    self.current_sprite = 0
                
                self.image = self.sprites_idle_r[int(self.current_sprite)]

            else:
                   
                self.current_sprite += 0.1

                if self.current_sprite >= len(self.sprites_idle_l):
                    self.current_sprite = 0
                
                self.image = self.sprites_idle_l[int(self.current_sprite)]

    def draw_health(self):
        half_hearts_total = self.health / 2
        half_heart_exists = half_hearts_total - int(half_hearts_total) != 0
        heart_down = 0

        for heart in range(int(self.max_health / 2)):
            if int(half_hearts_total) > heart:
                if heart < 5:
                    self.game.window.blit(self.hearts[0], (heart * 45 + 10, 10))
                else:
                    self.game.window.blit(self.hearts[0], (heart_down * 45 + 10, 50))
                    heart_down +=1
            elif half_heart_exists and int(half_hearts_total) == heart:
                if heart < 5:
                    self.game.window.blit(self.hearts[1], (heart * 45 + 10, 10))
                else:
                    self.game.window.blit(self.hearts[1], (heart_down * 45 + 10, 50))
                    heart_down +=1
            else:
                if heart < 5:
                    self.game.window.blit(self.hearts[2], (heart * 45 + 10, 10))
                else:
                    self.game.window.blit(self.hearts[2], (heart_down * 45 + 10, 50))
                    heart_down +=1
    
    def check_is_alive(self):
        if self.health <= 0:
            self.game.curr_menu = self.game.death
            self.game.curr_menu.display_menu()
            self.kill()


    def update(self):
        self.action()
        self.check_is_alive()
        self.animator(self.player_speed)
        self.pos += self.vel 
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        self.shooting()
        self.debug_men()
