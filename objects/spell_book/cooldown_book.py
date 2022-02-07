from objects.spell_book import spell_book
from perso.player import player
import pygame as pg

class Cooldown_Book(spell_book.Spell_book):
    def __init__(self, x, y, game):
        spell_book.Spell_book.__init__(self, x, y, game)
        self.image = pg.image.load("sprite/object/spell_book/spelbook_11.png").convert_alpha()
        self.price = 10
    
    def effect(self):
        self.game.player.cooldown -= 50