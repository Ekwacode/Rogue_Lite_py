#------------------------#
# Made by Julien Vanherf #
#------------------------#

from game import Game
from menu import Menu
from os import path
from tilemap import Map

g = Game()
m_change = False
while g.running:
    g.curr_menu.display_menu()
    g.game_loop()