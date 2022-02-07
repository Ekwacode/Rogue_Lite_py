from perso.boss import boss
from effects import Death_Effect
import pygame as pg

TILESIZE = 64

class Knight_Boss(boss.Boss):
    def __init__(self, x, y, player, game, coins, projectile):
        self.projectile = projectile
        boss.Boss.__init__(self, x, y, player, game, coins)
        self.sprite = [pg.image.load("sprite/enemy/boss_knight/knight_high/knight_boss_run_anim_f0.png").convert_alpha(),pg.image.load("sprite/enemy/boss_knight/knight_high/knight_boss_run_anim_f1.png").convert_alpha(),pg.image.load("sprite/enemy/boss_knight/knight_high/knight_boss_run_anim_f2.png").convert_alpha(), pg.image.load("sprite/enemy/boss_knight/knight_high/knight_boss_run_anim_f3.png").convert_alpha()]
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.mob_speed = 10
        self.forced = True
        self.val = 0
        self.max_health = 100
        self.health = 100
        self.health_ratio = self.max_health / self.health_bar_length
    
    def update(self):      
        self.death()
            
        if self.state != 'dead':
            if self.health <= self.max_health/2:
                self.sprite = [pg.image.load("sprite/enemy/boss_knight/knight_low/knight_boss_p2_run_anim_f0.png").convert_alpha(),pg.image.load("sprite/enemy/boss_knight/knight_low/knight_boss_p2_run_anim_f1.png").convert_alpha(),pg.image.load("sprite/enemy/boss_knight/knight_low/knight_boss_p2_run_anim_f2.png").convert_alpha(), pg.image.load("sprite/enemy/boss_knight/knight_low/knight_boss_p2_run_anim_f3.png").convert_alpha()]
                self.mob_speed = 12
            self.health_bar()
            self.animator()
            if not self.is_moving:
                self.dash()
            
            if self.is_moving:
                self.move()
                if pg.time.get_ticks() - self.cooldown >= 500:
                    self.shooting('circle')
                    self.cooldown = pg.time.get_ticks()
                self.attack()
            
            self.avoid_other()
            self.rect.x = self.pos.x
            if self.collide_with_walls('x'):
                self.shooting('circle')
                self.is_moving = False

            self.rect.y = self.pos.y
            if self.collide_with_walls('y'):
                self.shooting('circle')
                self.is_moving = False
            self.destroy_rocks()
        
    
    