from perso.mob import mob
import pygame as pg

class Orc_Fighter(mob.Mob):
    def __init__(self, x, y, player, game, coins, projectile):
        mob.Mob.__init__(self, x, y, player, game, coins, projectile)
        self.sprite = [pg.image.load("sprite/enemy/orc/fighter/orc_f_f0.png").convert_alpha(),pg.image.load("sprite/enemy/orc/fighter/orc_f_f1.png").convert_alpha(),pg.image.load("sprite/enemy/orc/fighter/orc_f_f2.png").convert_alpha(),pg.image.load("sprite/enemy/orc/fighter/orc_f_f3.png").convert_alpha()]
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.health = 5