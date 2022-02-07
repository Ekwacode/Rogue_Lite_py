from objects.spell_book import spell_book
from perso.player import player
import pygame as pg

class Projectile_Speed_Book(spell_book.Spell_book):
    def __init__(self, x, y, game):
        spell_book.Spell_book.__init__(self, x, y, game)
        self.image = pg.image.load("sprite/object/spell_book/spelbook_1.png").convert_alpha()
        self.price = 15
    
    def effect(self):
        self.game.player.projectile_speed += 5
        