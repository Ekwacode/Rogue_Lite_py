#------------------------#
# Made by Julien Vanherf #
#------------------------#

from menu import *
import sys
import pygame as pg
from pygame import mixer
from os import path
from environement import *
from tilemap import *
from perso.player import wizard
from perso.player import fairy
from perso.mob.orc import orc_brawler
from perso.mob.orc import orc_fighter
from perso.mob.orc import orc_chaman
from perso.mob.orc import orc_nain
from perso.mob.undead import skelet
from perso.mob.undead import zombie
from perso.mob.undead import blue_zombie
from perso.mob.undead import tiny_zombie
from perso.mob.knight import knight
from perso.mob.knight import knight_brute
from perso.mob.knight import bow_man
from objects.spell_book import spell_book
from objects.spell_book import speed_book
from objects.spell_book import projectile_speed_book
from objects.spell_book import cooldown_book
from objects.spell_book import attack_book
from projectile import ball
from projectile import brain
from projectile import arrow
from projectile import fire_ball
from perso.boss import orc_boss
from perso.boss import undead_boss
from perso.boss import knight_boss
from objects import coin
from objects import chest
from objects import heart
from objects import heart_container
from projectile import fire_ball 
from random import *

BGCOLOR = (34, 34, 34)

TILESIZE = 64
config = configparser.ConfigParser()
config.read("config.ini")


class Game():
    pg.mixer.init(frequency=44100)
    pg.mixer.music.load('music/bc_sound.ogg')
    pg.mixer.music.set_volume(int(config['SOUND']['bg'])*0.1)
    def __init__(self):
        pg.init()
        icon = pg.image.load('sprite/ui/logo.png')
        pg.display.set_icon(icon)
        pg.display.set_caption("Sorcellers")
        self.running, self.playing, self.game_on = True, False, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.PAUSE_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1024, 768
        self.display = pg.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pg.display.set_mode((self.DISPLAY_W,self.DISPLAY_H))
        #self.font_name = pg.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.menu = Menu(self)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.quit = Quit(self)
        self.death = Death_Menu(self)
        self.pause = Pause_Menu(self)
        self.confirm_quit = Confirm_Quit(self)
        self.sound = Sound_menu(self)
        self.control = ControlMenu(self)
        self.win = Win_Menu(self)
        self.select_player = Select_Player_Menu(self)
        self.pause_show  = False
        self.curr_menu = self.main_menu
        self.clock = pg.time.Clock()
        self.room_maps = ['map/map_1.txt', 'map/map_2.txt', 'map/map_3.txt', 'map/map_4.txt', 'map/map_6.txt','map/map_7.txt','map/map_8.txt','map/map_9.txt','map/map_10.txt','map/map_11.txt','map/map_12.txt','map/map_13.txt','map/map_14.txt','map/map_15.txt','map/map_16.txt','map/map_17.txt','map/map_18.txt','map/map_19.txt','map/map_20.txt']
        self.forced_maps = ['map/map_0.txt', 'map/map_shop.txt']
        self.boss_maps = ['map/map_b_1.txt','map/map_b_2.txt','map/map_b_3.txt']
        self.stage_num = 1
        self.stage = 1
        self.font_name = 'font/Minecraft.ttf'
        self.m_change = False
        self.lvl = 0
        self.boss_created = False
        self.book_created = False
        self.book_collected = False
        self.fb_sound = pg.mixer.Sound('music/fireball_1.ogg')
        self.hit_sound = pg.mixer.Sound('music/hit.ogg')
        self.c_sound = pg.mixer.Sound('music/coin.ogg')
        self.hit_sound.set_volume(int(config['SOUND']['shoot'])*0.1)
        self.fb_sound.set_volume(int(config['SOUND']['shoot'])*0.1)
        self.c_sound.set_volume(int(config['SOUND']['coin'])*0.1)
        pg.mixer.music.play()


    def game_loop(self):
        if self.playing:
            self.menu.fade(1024, 768, 250)
            self.new(False, self.select_player.player)
        while self.playing:
            self.check_events()
            self.draw()
            
            if self.BACK_KEY:
                self.reset_keys()
                self.pause_show = True
                self.curr_menu = self.pause
                while self.pause_show:
                    self.curr_menu.display_menu()
                
                self.menu.fade(1024, 768, 100)


            self.dt = self.clock.tick(60) / 1000
            
            self.update()
            self.reset_keys()


    def quit_game(self):
        sys.exit()


    def check_events(self):
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing and self.curr_menu != self.win:
                    config.read("config.ini")
                    config['GAME']['game_loosed'] = str(int(config['GAME']['game_loosed'])+1)
                    with open("config.ini", 'w') as configfile:
                        config.write(configfile)
                self.quit_game()
               
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.START_KEY = True
                if event.key == pg.K_ESCAPE:
                    self.BACK_KEY = True
                if event.key == pg.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pg.K_UP:
                    self.UP_KEY = True
                if event.key == pg.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pg.K_RIGHT:
                    self.RIGHT_KEY = True
                if event.key == pg.K_x:
                    config['CHARACTERS']['fairy_unlocked'] = 'True'
                    with open("config.ini", 'w') as configfile:
                        config.write(configfile)


    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.PAUSE_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False, False

    def draw_text(self, text, size, x, y ):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
    

    def random_maps(self, length):
        nb_s = randrange(2,length)
        temp_map = [self.forced_maps[0]]
        i = 0
        while i < length - 2:
            if i == nb_s:
                temp_map.append(self.forced_maps[1])
                i += 1
            else:
                nb = randrange(0,len(self.room_maps))
                temp_map.append(self.room_maps[nb])
                i += 1
            
        temp_map.append(self.boss_maps[self.stage_num - 1])

        self.stage_num += 1
        print(temp_map, len(temp_map))
        return temp_map

            
    def load_data(self):
        self.stage_num = 1
        self.stage = 1
        self.maps = self.random_maps(10)
        self.maps_s_2 = self.random_maps(randrange(10,15))
        self.maps_s_3 = self.random_maps(randrange(15,20))
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, self.maps[0]))
        self.stage_list = [self.maps, self.maps_s_2, self.maps_s_3]

    def new(self, m_change, player):
        self.d = 0
        self.effects = pg.sprite.Group()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.spikes = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.floor = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.hearts = pg.sprite.Group()
        self.rocks = pg.sprite.Group()
        self.hurts = pg.sprite.Group()
        self.coffres = pg.sprite.Group()
        self.books = pg.sprite.Group()
        self.ladders = pg.sprite.Group()
        if m_change:
            self.player = self.tmp_player
        else :
            self.projectile = pg.sprite.Group()
            if player == 'Wizard':
                self.player = wizard.Wizard(self, self.projectile)
            elif player == 'Fairy':
                self.player = fairy.Fairy(self, self.projectile)
            self.tmp_player = self.player
            self.m_change = False
            self.lvl = 0
        alpha = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
        ia = 0
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                # Décors et map
                if tile == 'w':
                    # Wall(self, col, row)
                    w = Wall(col, row)
                    self.hurts.add(w)
                    self.walls.add(w)
                    self.all_sprites.add(w)

                if tile == 'W':
                    # Mur avec trou
                    W = Wall_Hole(col, row, self, self.projectile)
                    self.hurts.add(W)
                    self.walls.add(W)
                    self.all_sprites.add(W)

                if tile == 's':
                    # Spike

                    s = Spike(col, row, self)
                    self.spikes.add(s)
                    self.all_sprites.add(s)
                
                if tile == 'd':
                    # Door(self, col, row)
                    if self.d == 1:
                        self.d = 0
                    else :
                        self.d += 1
                    d = Door(col, row, self, self.map, self.d, self.lvl, self.maps)
                    self.doors.add(d)
                    self.all_sprites.add(d)

                if tile == 'l':
                    l = Ladder(col, row, self)
                    self.ladders.add(l)
                    self.all_sprites.add(l)
                
                if tile == 'L':
                    l = Win_Ladder(col, row, self)
                    self.ladders.add(l)
                    self.all_sprites.add(l)
                
                if tile == '.':
                    # Floor(self, col, row)
                    f = Floor(col, row)
                    self.floor.add(f)
                    self.all_sprites.add(f)

                if tile == 'r':
                    r = Rock(col, row)
                    self.hurts.add(r)
                    self.rocks.add(r)
                    self.all_sprites.add(r)

                    # Sol derrière la pierre 
                    f = Floor(col, row)
                    self.floor.add(f)
                    self.all_sprites.add(f)

                if tile == 't':
                    t = Hole(col, row)
                    self.hurts.add(t)
                    self.all_sprites.add(t)

                # Monstre, Player et Entitée 
                if tile == 'P':
                    # création du sol
                    f = Floor(col, row)
                    # ajout du sprite au groupe floor
                    self.floor.add(f)
                    # ajout du sprite au groupe all_sprites
                    self.all_sprites.add(f)
                    self.player.set_position(col, row)
                    self.players.add(self.player)
                    self.all_sprites.add(self.player)
                
                if tile == 'M':
                    f = Floor(col, row)
                    # ajout du sprite au groupe floor
                    self.floor.add(f)
                    # ajout du sprite au groupe all_sprites
                    self.all_sprites.add(f)
                    # Modifications [fin]
                    self.nb = randrange(0, 4)
                    if self.stage == 1:
                        if self.nb == 1:
                            self.mob = orc_brawler.Orc_Brawler(col, row, self.player, self, self.coins, False)
                        elif self.nb == 2:
                            self.mob = orc_fighter.Orc_Fighter(col, row, self.player, self, self.coins, False)
                        elif self.nb == 3:
                            self.mob = orc_chaman.Orc_Chaman(col, row, self.player, self, self.coins, 'ball')
                        else:
                            self.mob = orc_nain.Orc_Nain(col, row, self.player, self, self.coins, False)

                    elif self.stage == 2:
                        if self.nb == 1:
                            self.mob = skelet.Skelet(col, row, self.player, self, self.coins, False)
                        elif self.nb == 2:
                            self.mob = zombie.Zombie(col, row, self.player, self, self.coins, False)
                        elif self.nb == 3:
                            self.mob = blue_zombie.Blue_Zombie(col, row, self.player, self, self.coins, 'brain')
                        else:
                            self.mob = tiny_zombie.Tiny_Zombie(col, row, self.player, self, self.coins, 'brain')
                    
                    else:
                        if self.nb == 1:
                            self.mob = knight.Knight(col, row, self.player, self, self.coins, False)
                        elif self.nb == 2:
                            self.mob = knight_brute.Knight_Brute(col, row, self.player, self, self.coins, False)
                        else:
                            self.mob = bow_man.Bow_Man(col, row, self.player, self, self.coins, 'arrow')

                    self.mobs.add(self.mob)
                    self.all_sprites.add(self.mob)
            

                if tile == 'B':
                    f = Floor(col, row)
                    # ajout du sprite au groupe floor
                    self.floor.add(f)
                    # ajout du sprite au groupe all_sprites
                    self.all_sprites.add(f)
                    # Création du boss
                    if self.stage == 1:
                        self.boss = orc_boss.Orc_Boss(col, row, self.player, self, self.coins)
                    elif self.stage == 2:
                        self.boss = undead_boss.Undead_Boss(col, row, self.player, self, self.coins, self.projectile)
                    elif self.stage == 3:
                        self.boss = knight_boss.Knight_Boss(col, row, self.player, self, self.coins, self.projectile)
                    self.mobs.add(self.boss)
                    self.boss_created = True

                if tile == 'c':
                    self.c_value = randint(1,3)
                    c = coin.Coin(col, row, self, self.c_value)
                    self.coins.add(c)
                    self.all_sprites.add(c)

                    # Sol derrière le coin 
                    f = Floor(col, row)
                    self.floor.add(f)
                    self.all_sprites.add(f)
                
                if tile == 'b':
                    f = Floor(col, row)
                    # ajout du sprite au groupe floor
                    self.floor.add(f)
                    # ajout du sprite au groupe all_sprites
                    self.all_sprites.add(f)

                    nb = randrange(0, 4)

                    if nb == 0:
                        b = attack_book.Attack_Book(col, row, self)

                    elif nb == 1:
                        b = projectile_speed_book.Projectile_Speed_Book(col, row, self)

                    elif nb == 2:
                        b = cooldown_book.Cooldown_Book(col, row, self)

                    elif nb == 3:
                        b = speed_book.Speed_Book(col, row, self)
                    
                    self.books.add(b)
                    self.all_sprites.add(b)
                    self.book_created = True
                
                if tile == 'h':
                    h = heart.Heart(col, row, self)
                    self.hearts.add(h)
                    self.all_sprites.add(h)

                    # Sol derrière le coeur
                    f = Floor(col, row)
                    self.floor.add(f)
                    self.all_sprites.add(f)
                
                if tile == 'H':
                    h = heart_container.Heart_container(col, row, self)
                    self.hearts.add(h)
                    self.all_sprites.add(h)

                    # Sol derrière le coeur
                    f = Floor(col, row)
                    self.floor.add(f)
                    self.all_sprites.add(f)
                
                if tile == 'C':
                    # Wall(self, col, row)
                    C = chest.Chest(col, row, self, self.coins)
                    self.coffres.add(C)
                    self.all_sprites.add(C)

                    # Sol derrière le coin 
                    f = Floor(col, row)
                    self.floor.add(f)
                    self.all_sprites.add(f)

    
        self.camera = Camera(self.map.width, self.map.height)

    def update(self):
        for c in self.coins:
            self.all_sprites.add(c)
        
        for h in self.hearts:
            self.all_sprites.add(h)
        
        for m in self.mobs:
            self.all_sprites.add(m)
        
        for d_e in self.effects:
            self.all_sprites.add(d_e)
        
        for projectile in self.projectile:
            self.all_sprites.add(projectile)

        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        self.window.fill(BGCOLOR)
        for sprite in self.all_sprites:
            self.window.blit(sprite.image, self.camera.apply(sprite))
        
        self.player.draw_health() 

        if self.pause_show:
            self.draw_text('PAUSE', 60, self.DISPLAY_W / 2, self.DISPLAY_H / 2 )
            self.draw_text('Enter pour reprendre', 30, self.DISPLAY_W / 2+350, self.DISPLAY_H / 2+350 )


        if self.boss_created:
            if self.boss.state == 'alive':
                self.boss.health_bar()

        if self.book_created:
            for book in self.books:
                book.draw_price()           

        self.coin_image = pg.image.load("sprite/object/coins/coin1.png").convert_alpha()
        self.window.blit(self.coin_image, (940, 10))

        self.font_a = pg.font.Font(self.font_name, 35)

        
        #self.dmg = str(self.player.attack_point)
        #dam_surface = self.font_a.render(self.dmg, False,(255,255,255))
        #self.window.blit(dam_surface,(900,50))

        self.p_coin = str(self.player.coin)
        textsurface = self.font_a.render(self.p_coin, False, (255, 255, 255))
        self.window.blit(textsurface,(975,15))

        self.lvl_nb = str(self.lvl + 1)
        lvl_nb_t = self.font_a.render(self.lvl_nb, False, (255,255,255))
        self.window.blit(lvl_nb_t, (960,720))


        pg.display.flip()



