import pygame
from game.game import *
from menus.menus import *


class App:
    def __init__(self):
        self.menu = None
        self.game = Game(self)
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

    def run(self):
        while self.running:
            if self.playing:
                self.game.run_game_loop()
                self.playing = False
            self.get_menu()
            self.menu.run()
            self.menu = None
        pygame.quit()
