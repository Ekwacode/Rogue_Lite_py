from perso.mob import mob
import pygame as pg

class Bad_Chest(mob.Mob):
    def __init__(self, x, y, player, game, coins, projectile):
        mob.Mob.__init__(self, x, y, player, game, coins, projectile)
        self.sprite = [pg.image.load("sprite/enemy/chest/chest_e_f0.png").convert_alpha(),pg.image.load("sprite/enemy/chest/chest_e_f1.png").convert_alpha(),pg.image.load("sprite/enemy/chest/chest_e_f2.png").convert_alpha()]
        self.mob_speed = 2.5
        self.forced = True