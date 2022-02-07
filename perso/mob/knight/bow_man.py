from perso.mob import mob
import pygame as pg

class Bow_Man(mob.Mob):
    def __init__(self, x, y, player, game, coins, projectile):
        mob.Mob.__init__(self, x, y, player, game, coins, projectile)
        self.sprite = [pg.image.load("sprite/enemy/knight/bow_man/bow_man_f0.png").convert_alpha(),pg.image.load("sprite/enemy/knight/bow_man/bow_man_f1.png").convert_alpha(),pg.image.load("sprite/enemy/knight/bow_man/bow_man_f2.png").convert_alpha(),pg.image.load("sprite/enemy/knight/bow_man/bow_man_f3.png").convert_alpha()]
        self.image = self.sprite[self.current_sprite]
        self.mob_speed = 1.5
        self.can_shoot = True
        self.projectile = self.game.projectile