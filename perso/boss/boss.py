import pygame as pg
from color import *
from random import *
from perso.player import player 
from projectile import brain
from projectile import arrow
from objects import heart_container
from objects import heart
from effects import Death_Effect
from objects import coin
vec = pg.math.Vector2

TILESIZE = 64

class Boss(pg.sprite.Sprite):
    def __init__(self, x, y, player, game, coins):
        pg.sprite.Sprite.__init__(self)
        self.font_name = 'font/Minecraft.ttf'
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.window = game.window 
        self.i = 0
        self.player = player
        self.coins = coins
        self.health = 50
        self.max_health = 50
        self.health_bar_length = 500
        self.health_ratio = self.max_health / self.health_bar_length
        self.game = game
        self.state = 'alive'
        self._layer = 9
        self.mob_speed = 10
        self.sprite = [pg.image.load("sprite/enemy/boss_orc/ogre_run_anim_f0.png").convert_alpha(),pg.image.load("sprite/enemy/boss_orc/ogre_run_anim_f1.png").convert_alpha(),pg.image.load("sprite/enemy/boss_orc/ogre_run_anim_f2.png").convert_alpha(), pg.image.load("sprite/enemy/boss_orc/ogre_run_anim_f3.png").convert_alpha()]
        self.current_sprite = 0
        self.current_sprite_d = 0
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.dirvect = pg.math.Vector2(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.nom = 'A'
        self.cooldown = 0
        self.is_animating = False
        self.is_moving = False
    
    def avoid_other(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < 70:
                    self.dirvect += dist.normalize()
    
    def health_bar(self):
        head = pg.image.load("sprite/head/boss_head.png").convert_alpha()

        pg.draw.rect(self.game.window, (255,0,0), (320,20,self.health / self.health_ratio,30))
        pg.draw.rect(self.game.window, (255,255,255),(320,20,self.health_bar_length,30),3)
        
        self.game.window.blit(head, (280, 10))

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.dirvect.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.dirvect.x < 0:
                    self.pos.x = hits[0].rect.right
                self.dirvect.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.dirvect.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.dirvect.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.dirvect.y = 0
                self.rect.y = self.pos.y

        return hits
    
    def destroy_rocks(self):
        hits = pg.sprite.spritecollide(self, self.game.rocks, False)
        for rock in hits:
            if self.game.stage == 1:
                rock.kill()
                self.is_moving = False
            elif self.game.stage == 3 :
                self.val = randrange(0,4)
                if self.val == 0:
                    self.shooting('cross')
                else :
                    self.shooting('plus')
                rock.kill()
                self.is_moving = False
    
    def shooting(self, choose_type):
        self.type = choose_type
        self.projectile_speed = 10
        directions = {'plus': 'ghbd','cross': 'aewc', 'circle': 'ghbdaewc'}
        if self.type in directions.keys():
            direc = directions[self.type]
            for i in direc:
                if self.game.stage == 2:
                    self.projectile.add(brain.Brain(self.rect.centerx, self.rect.centery, self.game, i))
                else:
                    self.projectile.add(arrow.Arrow(self.rect.centerx, self.rect.centery, self.game, i, 2))
        
        self.cooldown = pg.time.get_ticks()

    def animator(self):
        self.current_sprite += 0.1

        if self.current_sprite >= len(self.sprite):
            self.current_sprite = 0
            
        self.image = self.sprite[int(self.current_sprite)]

        
    
    def death(self):
        if self.health <= 0:
            d_e = Death_Effect(self.pos.x/TILESIZE, self.pos.y/TILESIZE)
            self.game.effects.add(d_e)
            self.state = 'dead'
            c = coin.Coin(self.pos.x/TILESIZE, self.pos.y/TILESIZE, self.game, 10)
            self.coins.add(c)
            nb = randrange(0,2)
            if nb == 0:
                h = heart.Heart(self.pos.x/TILESIZE, (self.pos.y/TILESIZE) +1, self.game)
            else:
                h = heart_container.Heart_container(self.pos.x/TILESIZE, (self.pos.y/TILESIZE) +1, self.game)
            self.game.hearts.add(h)

            self.kill()
    
    def attack(self):
        pass


    def dash(self):
        if pg.time.get_ticks() - self.cooldown >= 2000:
            self.dirvect = pg.math.Vector2(self.player.rect.centerx - self.rect.centerx,
                                           self.player.rect.centery - self.rect.centery)
            if self.dirvect.x != 0 or self.dirvect.y != 0:
                self.dirvect.normalize()
                self.dirvect.scale_to_length(self.mob_speed)
            
            self.is_moving = True

            self.cooldown = pg.time.get_ticks()
        
    
    def move(self):
        self.pos += self.dirvect

    def update(self):      
        pass