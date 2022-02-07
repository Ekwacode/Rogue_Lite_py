from perso.boss import boss
from effects import Death_Effect
from random import randrange
import pygame as pg

TILESIZE = 64

class Undead_Boss(boss.Boss):
    def __init__(self, x, y, player, game, coins, projectile):
        self.projectile = projectile
        boss.Boss.__init__(self, x, y, player, game, coins)
        self.sprite = [pg.image.load("sprite/enemy/boss_undead/big_zombie_run_anim_f0.png").convert_alpha(),pg.image.load("sprite/enemy/boss_undead/big_zombie_run_anim_f1.png").convert_alpha(),pg.image.load("sprite/enemy/boss_undead/big_zombie_run_anim_f2.png").convert_alpha(), pg.image.load("sprite/enemy/boss_undead/big_zombie_run_anim_f3.png").convert_alpha()]
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.mob_speed = 5
        self.val = 0
        self.move_cooldown = 0
        self.max_health = 75
        self.health = 75
        self.health_ratio = self.max_health / self.health_bar_length
    
    def move_aleat(self):
        if pg.time.get_ticks() - self.move_cooldown >= 1000:
            self.dirvect = pg.math.Vector2(randrange(-10,10), randrange(-10,10))

            if self.dirvect.x != 0 or self.dirvect.y != 0:
                self.dirvect.normalize()
                self.dirvect.scale_to_length(self.mob_speed)
            self.move_cooldown = pg.time.get_ticks()

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


    def update(self):      
        self.death()
            
        if self.state != 'dead':
            if pg.time.get_ticks() - self.cooldown >= 800:
                if self.val % 3 == 0:
                    self.shooting('cross')
                elif self.val % 3 == 1:
                    self.shooting('plus')
                else :
                    self.shooting('circle')
                self.val += 1
            self.move_aleat()
            self.move()
            self.health_bar()
            self.animator()
            self.avoid_other()
            self.rect.x = self.pos.x
            self.collide_with_walls('x')
            self.rect.y = self.pos.y
            self.collide_with_walls('y')
            self.destroy_rocks()
        
    