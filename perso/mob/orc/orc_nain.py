from perso.mob import mob
import pygame as pg

class Orc_Nain(mob.Mob):
    def __init__(self, x, y, player, game, coins, projectile):
        mob.Mob.__init__(self, x, y, player, game, coins, projectile)
        self.sprite = [pg.image.load("sprite/enemy/orc/nain/orc_n_f0.png").convert_alpha(),pg.image.load("sprite/enemy/orc/nain/orc_n_f1.png").convert_alpha(),pg.image.load("sprite/enemy/orc/nain/orc_n_f2.png").convert_alpha(),pg.image.load("sprite/enemy/orc/nain/orc_n_f3.png").convert_alpha()]
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.mob_speed = 4.5
        self.health = 3