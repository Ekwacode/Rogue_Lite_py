from perso.mob import mob
import pygame as pg

class Zombie(mob.Mob):
    def __init__(self, x, y, player, game, coins, projectile):
        mob.Mob.__init__(self, x, y, player, game, coins, projectile)
        self.sprite = [pg.image.load("sprite/enemy/undead/zombie/zombie_run_anim_f0.png").convert_alpha(),pg.image.load("sprite/enemy/undead/zombie/zombie_run_anim_f1.png").convert_alpha(),pg.image.load("sprite/enemy/undead/zombie/zombie_run_anim_f0.png").convert_alpha(),pg.image.load("sprite/enemy/undead/zombie/zombie_run_anim_f3.png").convert_alpha()]
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.mob_speed = 2
        self.health = 6