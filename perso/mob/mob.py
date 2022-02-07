import pygame as pg
from color import *
from random import *
from perso.player import player 
from projectile import ball
from projectile import arrow
from projectile import brain
from effects import Death_Effect
from objects import coin
vec = pg.math.Vector2

TILESIZE = 64

class Mob(pg.sprite.Sprite):
    def __init__(self, x, y, player, game, coins, projectile):
        pg.sprite.Sprite.__init__(self)
        self.can_shoot = False
        self.font_name = 'font/dogicapixel.ttf'
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.window = game.window 
        self.i = 0
        self.player = player
        self.coins = coins
        self.health = 5
        self.game = game
        self.state = 'alive'
        self._layer = 10
        self.mob_speed = 3.5
        self.sprite = [pg.image.load("sprite/player/mage/mage_idle_l_f0.png").convert_alpha()]
        self.current_sprite = 0
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.dirvect = pg.math.Vector2(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.nom = 'A'
        self.cooldown = 3000
        self.forced = False
        self.vect = pg.math.Vector2(0,0)
        self.projectile_name = projectile

    def move_towards_player(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        self.dirvect = pg.math.Vector2(player.rect.centerx - self.rect.centerx,
                                       player.rect.centery - self.rect.centery)
        
        if self.dirvect.x != 0 or self.dirvect.y != 0:
            self.dirvect.normalize()
            self.dirvect.scale_to_length(self.mob_speed)
    
    def avoid_other(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < 70:
                    self.dirvect += dist.normalize()
        
        for player in self.game.players:
            if player != self:
                dist = self.pos - player.pos
                if 0 < dist.length() < 30:
                    dist = pg.math.Vector2(0,0)
                    self.dirvect = dist
                    if pg.time.get_ticks() - self.cooldown >= 500:
                        player.health -= 1
                        self.cooldown = pg.time.get_ticks()

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.hurts, False)
            if hits:
                if self.dirvect.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.dirvect.x < 0:
                    self.pos.x = hits[0].rect.right
                self.dirvect.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.hurts, False)
            if hits:
                if self.dirvect.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.dirvect.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.dirvect.y = 0
                self.rect.y = self.pos.y

    def animator(self):
        self.current_sprite += 0.1

        if self.current_sprite >= len(self.sprite):
            self.current_sprite = 0
            
        self.image = self.sprite[int(self.current_sprite)]
    
    def shoot(self):
        self.vect = pg.math.Vector2(self.player.rect.centerx - self.rect.centerx,
                                    self.player.rect.centery - self.rect.centery)
        
        if self.vect.x != 0 or self.vect.y != 0:
            self.vect.normalize()
            self.vect.scale_to_length(10)
        
        if pg.time.get_ticks() - self.cooldown >= 1000:
            if self.projectile_name == 'arrow':
                self.projectile.add(arrow.Arrow(self.rect.centerx, self.rect.centery, self.game, self.vect, 1))
            elif self.projectile_name == 'brain':
                self.projectile.add(brain.Brain(self.rect.centerx, self.rect.centery, self.game, self.vect))
            elif self.projectile_name == 'ball':
                self.projectile.add(ball.Ball(self.rect.centerx, self.rect.centery, self.game, self.vect))
            
            self.cooldown = pg.time.get_ticks()

        
    
    def death(self):
        nb = randrange(0,4)
        if nb == 1 or self.forced:
            if self.forced:
                self.coin_val = 3
            else :
                self.coin_val = randrange(1,3)
            c = coin.Coin(self.pos.x/TILESIZE, self.pos.y/TILESIZE, self.game, self.coin_val)
            self.coins.add(c)


        self.kill()




    def update(self):
        if self.health <= 0:
            d_e = Death_Effect(self.pos.x/TILESIZE, self.pos.y/TILESIZE)
            self.game.effects.add(d_e)

            self.death()
        
        else:
            self.animator()
        
            self.move_towards_player(self.player)
            if self.can_shoot:
                self.shoot()
            self.avoid_other()
            self.pos += self.dirvect
            self.rect.x = self.pos.x
            self.collide_with_walls('x')
            self.rect.y = self.pos.y
            self.collide_with_walls('y')



