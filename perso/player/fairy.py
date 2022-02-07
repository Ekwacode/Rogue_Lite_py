from perso.player import player
import pygame as pg

class Fairy(player.Player):
    def __init__(self, game, fire_ball):
        player.Player.__init__(self, game, fire_ball)
        self.sprites_idle_l = [pg.image.load("sprite/player/fairy/fairy_idle_l_f0.png").convert_alpha(), pg.image.load("sprite/player/fairy/fairy_idle_l_f1.png").convert_alpha(), pg.image.load("sprite/player/fairy/fairy_idle_l_f2.png").convert_alpha(), pg.image.load("sprite/player/fairy/fairy_idle_l_f3.png").convert_alpha()]
        self.sprites_move_l = [pg.image.load("sprite/player/fairy/fairy_idle_l_f0.png").convert_alpha(), pg.image.load("sprite/player/fairy/fairy_idle_l_f1.png").convert_alpha(), pg.image.load("sprite/player/fairy/fairy_idle_l_f2.png").convert_alpha(), pg.image.load("sprite/player/fairy/fairy_idle_l_f3.png").convert_alpha()]
        self.sprites_idle_r = [pg.image.load("sprite/player/fairy/fairy_idle_r_f0.png").convert_alpha(), pg.image.load("sprite/player/fairy/fairy_idle_r_f1.png").convert_alpha(), pg.image.load("sprite/player/fairy/fairy_idle_r_f2.png").convert_alpha(), pg.image.load("sprite/player/fairy/fairy_idle_r_f3.png").convert_alpha()]
        self.sprites_move_r = [pg.image.load("sprite/player/fairy/fairy_idle_r_f0.png").convert_alpha(), pg.image.load("sprite/player/fairy/fairy_idle_r_f1.png").convert_alpha(), pg.image.load("sprite/player/fairy/fairy_idle_r_f2.png").convert_alpha(), pg.image.load("sprite/player/fairy/fairy_idle_r_f3.png").convert_alpha()]
        self.image = self.sprites_idle_l[self.current_sprite]
        self.rect = self.image.get_rect()
        self.player_speed = 7
        self.attack_point = 1.25
        self.max_health = 4
        self.health = 4
        self.projectile_speed = 20
        self.cooldown = 400
        self.fly = True