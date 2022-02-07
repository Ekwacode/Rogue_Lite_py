from perso.mob import mob
import pygame as pg

class Orc_Chaman(mob.Mob):
    def __init__(self, x, y, player, game, coins, projectile):
        mob.Mob.__init__(self, x, y, player, game, coins, projectile)
        self.sprite = [pg.image.load("sprite/enemy/orc/chaman/orc_c_f0.png").convert_alpha(),pg.image.load("sprite/enemy/orc/chaman/orc_c_f1.png").convert_alpha(),pg.image.load("sprite/enemy/orc/chaman/orc_c_f2.png").convert_alpha(),pg.image.load("sprite/enemy/orc/chaman/orc_c_f3.png").convert_alpha()]
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.mob_speed = 1.5
        self.can_shoot = True
        self.projectile = self.game.projectile
        self.health = 4