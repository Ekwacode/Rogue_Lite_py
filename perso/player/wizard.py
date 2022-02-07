from perso.player import player
import pygame as pg

class Wizard(player.Player):
    def __init__(self, game, fire_ball):
        player.Player.__init__(self, game, fire_ball)
        self.sprites_idle_l = [pg.image.load("sprite/player/mage/mage_idle_l_f0.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_idle_l_f1.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_idle_l_f2.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_idle_l_f3.png").convert_alpha()]
        self.sprites_move_l = [pg.image.load("sprite/player/mage/mage_walk_l_f0.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_walk_l_f1.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_walk_l_f2.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_walk_l_f3.png").convert_alpha()]
        self.sprites_idle_r = [pg.image.load("sprite/player/mage/mage_idle_r_f0.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_idle_r_f1.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_idle_r_f2.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_idle_r_f3.png").convert_alpha()]
        self.sprites_move_r = [pg.image.load("sprite/player/mage/mage_walk_r_f0.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_walk_r_f1.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_walk_r_f2.png").convert_alpha(), pg.image.load("sprite/player/mage/mage_walk_r_f3.png").convert_alpha()]