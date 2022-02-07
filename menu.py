#------------------------#
# Made by Julien Vanherf #
#------------------------#

import pygame as pg
import sys
import configparser
from projectile import fire_ball

config = configparser.ConfigParser()
config.read("config.ini")

if not config.has_section("SOUND"):
    config.add_section("SOUND")
    config.set("SOUND", "bg", "1")
    config.set("SOUND", "shoot", '1')
    config.set("SOUND", "coin", "1")
    config.set("SOUND", "menu", "1")

if not config.has_section("CHARACTERS"):
    config.add_section("CHARACTERS")
    config.set("CHARACTERS", "fairy_unlocked", "False")

if not config.has_section("GAME"):
    config.add_section("GAME")
    config.set("GAME", "game_winned", "0")
    config.set("GAME", "game_loosed", "0")
    config.set("GAME", "game_played", "0")

with open("config.ini", 'w') as configfile:
    config.write(configfile)


class Menu():
    def __init__(self, game):
        self.move_sound = pg.mixer.Sound('music/bip.ogg')
        self.select_sound = pg.mixer.Sound('music/select.ogg')
        self.select_sound.set_volume(float(config['SOUND']['menu'])*0.1)
        self.move_sound.set_volume(float(config['SOUND']['menu'])*0.1)
        self.fairy_image_unlocked = pg.image.load("sprite/player/fairy/fairy_menu.png").convert_alpha()
        self.fairy_image = pg.image.load("sprite/player/fairy/fairy_menu_not_unlocked.png").convert_alpha()
        self.wizard_image = pg.image.load("sprite/player/mage/mage_menu.png").convert_alpha()
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.coin_image = pg.image.load("sprite/object/coins/coin1.png").convert_alpha()
        self.cursor_rect = self.coin_image.get_rect()
        self.offset = - 100


    def draw_cursor(self):
        self.game.display.blit(self.coin_image, (self.cursor_rect.x-70, self.cursor_rect.y-25))

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        self.game.reset_keys()

        if self.game.select_player.run_display:
            config.read("config.ini")
            if config['CHARACTERS']['fairy_unlocked'] == 'True':
                self.game.window.blit(self.fairy_image_unlocked, (self.mid_w + 115, self.mid_h - 45))
            else:
                self.game.window.blit(self.fairy_image, (self.mid_w + 115, self.mid_h - 45))
            self.game.window.blit(self.wizard_image, (self.mid_w - 252, self.mid_h - 97))
            

        
        pg.display.update()
        
    
    def blit_background(self):
        self.background = pg.image.load("capture/background.png").convert_alpha()
        self.game.display.blit(self.background, (0, 0))
    
    def fade(self, width, height, time): 
        fade = pg.Surface((width, height))
        fade.fill((0,0,0))
        for alpha in range(0, time):
            fade.set_alpha(alpha)
            self.game.window.blit(fade, (0,0))
            pg.display.update()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 20
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 80
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 140
        self.quitx, self.quity = self.mid_w, self.mid_h + 200
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        
    def display_menu(self):
        self.fade(1024, 768, 50)
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.blit_background()
            self.game.draw_text("Sorceller's Rage", 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 285)
            self.game.draw_text("Demarrer", 50, self.startx, self.starty)
            self.game.draw_text("Options", 50, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 50, self.creditsx, self.creditsy)
            self.game.draw_text("Quitter", 50, self.quitx, self.quity)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.move_sound.play()
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'

        elif self.game.UP_KEY:
            self.move_sound.play()
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            self.select_sound.play()
            if self.state == 'Start':
                self.game.curr_menu = self.game.select_player
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Quit':
                self.game.curr_menu = self.game.quit
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Sons"
        self.volx, self.voly = self.mid_w, self.mid_h 
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 100
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.fade(1024, 768, 50)
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.blit_background()
            self.game.draw_text('Options', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 285)
            self.game.draw_text("Sons", 50, self.volx, self.voly)
            self.game.draw_text("Controls", 50, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            if self.game.pause_show:
                self.select_sound.play()
                self.game.curr_menu = self.game.pause
                self.run_display = False
            
            else:
                self.select_sound.play()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False

        elif self.game.UP_KEY or self.game.DOWN_KEY:
            self.move_sound.play()
            if self.state == 'Sons':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Sons'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            self.select_sound.play()
            if self.state == 'Sons':
                self.game.curr_menu = self.game.sound
                self.run_display = False
            elif self.state == 'Controls':
                self.game.curr_menu = self.game.control
                self.run_display = False

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.fade(1024, 768, 50)
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
                self.select_sound.play()
            self.game.display.fill(self.game.BLACK)
            self.blit_background()
            self.game.draw_text('Credits', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 285)
            self.game.draw_text('Fait et develloppe par', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.game.draw_text('Julien Vanherf', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 60)
            self.blit_screen()

class ControlMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.fade(1024, 768, 50)
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.options
                self.run_display = False
                self.select_sound.play()
            self.game.display.fill(self.game.BLACK)
            self.background = pg.image.load("capture/touche.png").convert_alpha()
            self.game.display.blit(self.background, (0, 0))
            self.game.draw_text('Controls', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 285)
            self.blit_screen()


class Quit(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        while self.run_display:
            pg.quit()
            sys.exit()

class Death_Menu(Menu):
    def __init__ (self,game):
        Menu.__init__(self, game)
        self.state = "Death"

    def display_menu(self):
        self.fade(1024, 768, 50)
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                config['GAME']['game_loosed'] = str(int(config['GAME']['game_loosed'])+1)
                with open("config.ini", 'w') as configfile:
                    config.write(configfile)
                self.m_change = False
                self.game.playing = False
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
                self.game.boss_created = False
            self.game.display.fill(self.game.BLACK)
            self.blit_background()
            self.game.draw_text('VOUS ETES MORT', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 )
            self.game.draw_text('Enter pour continuer', 30, self.game.DISPLAY_W / 2+350, self.game.DISPLAY_H / 2+350 )
            self.blit_screen()

class Pause_Menu(Menu):
    def __init__ (self,game):
        Menu.__init__(self, game)
        self.state = 'Options'
        self.volx, self.voly = self.mid_w, self.mid_h 
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 100
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.fade(1024, 768, 50)
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.blit_background()
            self.game.draw_text('Pause', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 285)
            self.game.draw_text("Options", 50, self.volx, self.voly)
            self.game.draw_text("Menu principal", 50, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()


    def check_input(self):
        if self.game.BACK_KEY:
            self.game.pause_show = False
            self.run_display = False
            self.select_sound.play()
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            self.move_sound.play()
            if self.state == 'Options':
                self.state = 'Menu principal'
                self.cursor_rect.midtop = (self.controlsx + self.offset-50, self.controlsy)
            elif self.state == 'Menu principal':
                self.state = 'Options'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            self.select_sound.play()
            if self.state == 'Options':
                self.game.curr_menu = self.game.options
                

            elif self.state == 'Menu principal':
                self.game.curr_menu = self.game.confirm_quit

            self.run_display = False

class Confirm_Quit(Menu):
    def __init__ (self,game):
        Menu.__init__(self, game)
        self.state = 'Oui'
        self.volx, self.voly = self.mid_w, self.mid_h 
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 100
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.fade(1024, 768, 50)
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.blit_background()
            self.game.draw_text('Voulez-vous vraiment quitter ?', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 285)
            self.game.draw_text("Oui", 50, self.volx, self.voly)
            self.game.draw_text("Non", 50, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()


    def check_input(self):
        if self.game.BACK_KEY:
            self.game.pause_show = False
            self.run_display = False
            self.select_sound.play()
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            self.move_sound.play()
            if self.state == 'Oui':
                self.state = 'Non'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Non':
                self.state = 'Oui'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            self.select_sound.play()
            if self.state == 'Oui':
                config['GAME']['game_loosed'] = str(int(config['GAME']['game_loosed'])+1)
                with open("config.ini", 'w') as configfile:
                    config.write(configfile)
                self.game.pause_show = False
                self.game.playing = False
                self.m_change = False
                self.game.win_game = True
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
                
            elif self.state == 'Non':
                self.game.curr_menu = self.game.pause

            self.run_display = False

class Sound_menu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Fond"
        self.vol_fondx, self.vol_fondy = self.mid_w, self.mid_h 
        self.vol_shootx, self.vol_shooty = self.mid_w, self.mid_h + 75
        self.vol_piecex, self.vol_piecey = self.mid_w, self.mid_h + 150
        self.vol_menux, self.vol_menuy = self.mid_w, self.mid_h + 225
        self.cursor_rect.midtop = (self.vol_fondx + self.offset, self.vol_fondy)
    
    def sound_modifier(self, sound, ope):
        nb = int(config['SOUND'][sound])
        if ope == 'add':
            if nb < 10:
                nb += 1
                config['SOUND'][sound] = str(nb) 
            else :
                config['SOUND'][sound] = '10' 
        
        else :
            if nb > 0:
                nb -= 1
                config['SOUND'][sound] = str(nb) 
            else :
                config['SOUND'][sound] = '0' 
     

    def display_menu(self):
        self.fade(1024, 768, 50)
        self.run_display = True
        while self.run_display:
            bg_vol = str(config['SOUND']['bg'])
            shoot_vol = str(config['SOUND']['shoot'])
            coin_vol = str(config['SOUND']['coin'])
            select_vol = str(config['SOUND']['menu'])
            self.game.check_events()
            self.check_input()
            self.move_cursor()
            self.game.display.fill((0, 0, 0))
            self.blit_background()
            self.game.draw_text('Sons', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 285)
            self.game.draw_text("Fond", 50, self.vol_fondx, self.vol_fondy)
            self.game.draw_text(bg_vol, 50, self.vol_fondx+200, self.vol_fondy)
            self.game.draw_text("Tir", 50, self.vol_shootx, self.vol_shooty)
            self.game.draw_text(shoot_vol, 50, self.vol_shootx +200, self.vol_shooty)
            self.game.draw_text("Pieces", 50, self.vol_piecex, self.vol_piecey)
            self.game.draw_text(coin_vol, 50, self.vol_piecex +200, self.vol_piecey)
            self.game.draw_text("Menu", 50, self.vol_menux, self.vol_menuy)
            self.game.draw_text(select_vol, 50, self.vol_menux +200, self.vol_menuy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.move_sound.play()
                
            if self.state == 'Fond':
                self.cursor_rect.midtop = (self.vol_shootx + self.offset, self.vol_shooty)
                self.state = 'Tir'
                
            elif self.state == 'Tir':
                self.cursor_rect.midtop = (self.vol_piecex + self.offset, self.vol_piecey)
                self.state = 'Pieces'
            
            elif self.state == 'Pieces':
                self.cursor_rect.midtop = (self.vol_menux + self.offset, self.vol_menuy)
                self.state = 'Menu'

            elif self.state == 'Menu':
                self.cursor_rect.midtop = (self.vol_fondx+ self.offset, self.vol_fondy)
                self.state = 'Fond'

        elif self.game.UP_KEY:
            self.move_sound.play()
                
            if self.state == 'Fond':
                self.cursor_rect.midtop = (self.vol_menux + self.offset, self.vol_menuy)
                self.state = 'Menu'
            
            elif self.state == 'Tir':
                self.cursor_rect.midtop = (self.vol_fondx + self.offset, self.vol_fondy)
                self.state = 'Fond'
            
            elif self.state == 'Pieces':
                self.cursor_rect.midtop = (self.vol_shootx + self.offset, self.vol_shooty)
                self.state = 'Tir'
            
            elif self.state == 'Menu':
                self.cursor_rect.midtop = (self.vol_piecex + self.offset, self.vol_piecey)
                self.state = 'Pieces'
                
    def check_input(self):
        if self.game.BACK_KEY:
            if self.game.pause_show:
                self.select_sound.play()
                self.game.curr_menu = self.game.options
                self.run_display = False
            
            else:
                self.select_sound.play()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False

        elif self.game.LEFT_KEY:
            self.select_sound.play()
      
            if self.state == 'Fond':
                self.sound_modifier('bg','sub')

            elif self.state == 'Tir':
                self.sound_modifier('shoot','sub')

            elif self.state == 'Pieces':
                self.sound_modifier('coin','sub')

            elif self.state == 'Menu':
                self.sound_modifier('menu','sub')
        
        elif self.game.RIGHT_KEY:
            self.select_sound.play()
            if self.state == 'Fond':
                self.sound_modifier('bg', 'add')
            elif self.state == 'Tir':
                self.sound_modifier('shoot', 'add')
            elif self.state == 'Pieces':
                self.sound_modifier('coin', 'add')
            elif self.state == 'Menu':
                self.sound_modifier('menu', 'add')

        self.select_sound.set_volume(int(config['SOUND']['menu'])*0.1)
        self.move_sound.set_volume(int(config['SOUND']['menu'])*0.1)
        pg.mixer.music.set_volume(int(config['SOUND']['bg'])*0.1)
        self.game.hit_sound.set_volume(int(config['SOUND']['shoot'])*0.1)
        self.game.fb_sound.set_volume(int(config['SOUND']['shoot'])*0.1)
        self.game.c_sound.set_volume(int(config['SOUND']['coin'])*0.1)
        with open("config.ini", 'w') as configfile:
            config.write(configfile)

class Win_Menu(Menu):
    def __init__ (self,game):
        Menu.__init__(self, game)
        self.state = "Win"

    def display_menu(self):
        self.fade(1024, 768, 50)
        self.run_display = True
        config['GAME']['game_winned'] = str(int(config['GAME']['game_winned'])+1)
        with open("config.ini", 'w') as configfile:
            config.write(configfile)
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.playing = False
                self.m_change = False
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
                if int(config['GAME']['game_winned']) == 5 and config['CHARACTERS']['fairy_unlocked'] == 'False' : 
                    config['CHARACTERS']['fairy_unlocked'] = 'True'
                    with open("config.ini", 'w') as configfile:
                        config.write(configfile)
            self.game.display.fill(self.game.BLACK)
            self.blit_background()
            self.game.draw_text('Bravo vous avez gagne !', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 3 )
            self.game.draw_text('Enter pour continuer', 30, self.game.DISPLAY_W / 2+350, self.game.DISPLAY_H / 2+350 )
            if int(config['GAME']['game_winned']) == 5 and config['CHARACTERS']['fairy_unlocked'] == 'False' : 
                self.game.draw_text('Grace a vos 5 victoires', 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 )
                self.game.draw_text('La Fee est maintenant debloque', 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 50 )
                self.game.window.blit(self.fairy_image, (self.mid_w + 115, self.mid_h - 45))
            self.blit_screen()

class Select_Player_Menu(Menu):
    def __init__ (self,game):
        Menu.__init__(self, game)
        self.state = 'Wizard'
        self.player = 'Wizard'
        self.run_display = False
        self.wizardx, self.wizardy = self.mid_w - 125 , self.mid_h + 90
        self.fairyx, self.fairyy = self.mid_w + 250 , self.mid_h + 90
        self.cursor_rect.midtop = (self.wizardx , self.wizardy +60)

    def display_menu(self):
        self.fade(1024, 768, 50)
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.blit_background()
            self.game.draw_text('Choix du personnage', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 285)
            self.game.draw_text("Mage", 40, self.game.select_player.wizardx-68, self.game.select_player.wizardy+10)
            if config['CHARACTERS']['fairy_unlocked'] == 'True':
                self.game.draw_text("Fee", 40, self.game.select_player.fairyx-68, self.game.select_player.fairyy+8)
            else :
                self.game.draw_text("???", 40, self.game.select_player.fairyx-68, self.game.select_player.fairyy+8)
            self.draw_cursor()
            self.blit_screen()
    
    def play_game(self, player):
        self.game.playing = True
        self.game.game_on = True
        if player == 'Wizard':
            self.player = 'Wizard'
        elif player == 'Fairy':
            self.player = 'Fairy'
        config['GAME']['game_played'] = str(int(config['GAME']['game_played'])+1)
        with open("config.ini", 'w') as configfile:
            config.write(configfile)
        self.game.load_data()

    def check_input(self):
        if self.game.BACK_KEY:
            self.select_sound.play()
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif (self.game.LEFT_KEY or self.game.RIGHT_KEY) and config['CHARACTERS']['fairy_unlocked'] == 'True':
            self.move_sound.play()
            if self.state == 'Wizard':
                self.state = 'Fairy'
                self.cursor_rect.midtop = (self.fairyx , self.fairyy +60)
            elif self.state == 'Fairy':
                self.state = 'Wizard'
                self.cursor_rect.midtop = (self.wizardx , self.wizardy +60)

        elif self.game.START_KEY:
            self.select_sound.play()
            if self.state == 'Wizard':
                self.play_game('Wizard')
                

            elif self.state == 'Fairy':
                self.play_game('Fairy')

            self.run_display = False