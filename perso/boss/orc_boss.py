from perso.boss import boss
from effects import Death_Effect
import pygame as pg

TILESIZE = 64

class Orc_Boss(boss.Boss):
    def __init__(self, x, y, player, game, coins):
        boss.Boss.__init__(self, x, y, player, game, coins)
        self.sprite = [pg.image.load("sprite/enemy/boss_orc/ogre_run_anim_f0.png").convert_alpha(),pg.image.load("sprite/enemy/boss_orc/ogre_run_anim_f1.png").convert_alpha(),pg.image.load("sprite/enemy/boss_orc/ogre_run_anim_f2.png").convert_alpha(), pg.image.load("sprite/enemy/boss_orc/ogre_run_anim_f3.png").convert_alpha()]
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.mob_speed = 10
        self.forced = True
        self.max_health = 50
        self.health = 50
        self.health_ratio = self.max_health / self.health_bar_length
    
    def update(self):      
        self.death()
            
        if self.state != 'dead':
            self.health_bar()
            self.animator()
            if not self.is_moving:
                self.dash()
            
            if self.is_moving:
                print(self.dirvect)
                self.move()
                self.attack()
            
            self.avoid_other()
            self.rect.x = self.pos.x
            if self.collide_with_walls('x'):
                self.is_moving = False

            self.rect.y = self.pos.y
            if self.collide_with_walls('y'):
                self.is_moving = False
            self.destroy_rocks()
        
    
    