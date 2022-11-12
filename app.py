import pygame
from game.game import *
from menus.menus import *


class App:
    def __init__(self):
        self.menu = None
        self.game = None
        self.running = True
        self.playing = False
        self.curr_menu = 'MAIN'

    def get_menu(self):
        if self.curr_menu == 'MAIN':
            self.menu = MainMenu(self)
        elif self.curr_menu == 'OPTIONS':
            self.menu = None
        elif self.curr_menu == 'CREDITS':
            self.menu = CreditsMenu(self)

    def get_game(self):
        self.game = Game(self)

    def run(self):
        while self.running:
            if self.playing:
                self.get_game()
                self.game.run_game_loop()
                self.game = None
                self.playing = False
            else:
                self.get_menu()
                self.menu.run()
                self.menu = None
        pygame.quit()
