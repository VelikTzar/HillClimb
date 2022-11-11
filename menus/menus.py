import pygame


class Menu:
    DISPLAY_W = 400
    DISPLAY_H = 600
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    FPS = 60

    def __init__(self, game):
        pygame.init()
        self.display = pygame.display.set_mode((Menu.DISPLAY_W, Menu.DISPLAY_H))
        self.mid_w, self.mid_h = Menu.DISPLAY_W / 2, Menu.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.font_name = './menus/8-BIT WONDER.TTF'
        self.offset = - 100
        self.clock = pygame.time.Clock()
        self.game = game

    def draw_cursor(self):
        self.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def draw(self):
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run_display = False

    def run(self):
        while self.run_display:
            self.handle_events()
            self.draw()
            self.clock.tick(Menu.FPS)


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.run_display = True

    def draw(self):
        self.display.fill(self.BLACK)
        self.draw_text('Monki Racing', 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2 - 20)
        self.draw_text("Start Game", 20, self.startx, self.starty)
        self.draw_text("Options", 20, self.optionsx, self.optionsy)
        self.draw_text("Credits", 20, self.creditsx, self.creditsy)
        self.draw_cursor()
        pygame.display.update()

    def move_cursor(self, btn):
        if btn == pygame.K_DOWN:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif btn == pygame.K_UP:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        if self.state == 'Start':
            self.game.playing = True
        elif self.state == 'Options':
            self.game.curr_menu = 'OPTIONS'
        elif self.state == 'Credits':
            self.game.curr_menu = 'CREDITS'
        self.run_display = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run_display = False
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                self.move_cursor(event.key)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.check_input()


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run_display = False
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or pygame.K_BACKSPACE:
                    self.game.curr_menu = 'MAIN'
                    self.run_display = False

    def draw(self):
        self.display.fill(Menu.BLACK)
        self.draw_text('Credits', 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2 - 40)
        self.draw_text('Pako', 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2)
        self.draw_text('Rabani', 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2 + 30)
        pygame.display.update()
