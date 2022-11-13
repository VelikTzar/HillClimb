import pygame
import pymunk
import pymunk.pygame_util
from game.common_functions import *
from game.classes_pymunk import *
from game.messageboxes import LossMessageBox, EscapeMessageBox, VictoryMessageBox


class Entity(pygame.sprite.Sprite):
    def __init__(self, body, space, window, height, image):
        self.height = height
        self.space = space
        self.window = window
        self.body = body # pymunk body
        self.image = image
        self.orig_image = self.image
        self.rect = self.image.get_rect(topleft=self.body.position)
        super().__init__()

    def update(self):
        self.rect.center = self.body.position
        self.image = pygame.transform.rotate(
            self.orig_image, -math.degrees(self.body.angle))
        self.rect = self.image.get_rect(center=self.rect.center)


class PygameObject:
    def __init__(self):
        pass

    def generate_event(self):
        pass

    def handle_event(self, event):
        pass

    def handle_keys(self):
        pass


class CarMovementHandler(PygameObject):
    def __init__(self, car):
        super().__init__()
        self.car = car  # classes_pymunk.Car

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.car.breaks()
            elif event.key == pygame.K_RIGHT:
                self.car.gas()

    def handle_keys(self):
        keys = pygame.key.get_pressed() # checking pressed keys
        if keys[pygame.K_LEFT]:
            self.car.breaks()
        elif keys[pygame.K_RIGHT]:
            self.car.gas()
        else:
            self.car.slow_down()


class HeadCollisionHandlerPyGame(PygameObject):
    HEADCOLLISIONEVENT = pygame.event.Event(pygame.USEREVENT + 1)

    def __init__(self, space, game):
        super().__init__()
        self.head_collider = HeadCollisionHandler(space, self)
        self.collision_event = self.HEADCOLLISIONEVENT
        self.game = game

    def post_loss_event(self):
        if not self.game.done:
            pygame.event.post(self.collision_event)


class VictoryHandler(PygameObject):
    VICTORY_EVENT = pygame.event.Event(pygame.USEREVENT + 2)

    def __init__(self, game, player):
        super().__init__()
        self.victory_event = self.VICTORY_EVENT
        self.game = game
        self.player = player

    def generate_event(self):
        if (not self.game.done) and (self.player.person.head_body.position[0] >=
                                     (self.game.WIDTH - Boundaries.THICKNESS - self.player.car.WIDTH)):
            pygame.event.post(self.victory_event)


class Camera:
    def __init__(self, display_width, display_height, total_width, total_height):
        self.obj = None
        self.display_width = display_width
        self.display_height = display_height
        self.total_width = total_width
        self.total_height = total_height

    def set_obj(self, obj):
        self.obj = obj

    def get_coordinates(self):
        return [self.obj.rect.centerx, self.obj.rect.centery]

    def follow_coordinates(self):
        obj = self.obj
        offset = [-obj.rect.centerx + self.display_width / 2, -obj.rect.centery + self.display_height / 2]
        if offset[0] > 0:
            offset[0] = 0
        if offset[1] > 0:
            offset[1] = 0
        if offset[0] + self.display_width > self.total_width:
            offset[0] = self.total_width - self.display_width
        if offset[1] + self.display_height < self.total_height:
            offset[1] = self.display_height - self.total_height

        return offset


class MessageBox(PygameObject):
    def __init__(self, game):
        super(PygameObject).__init__()
        self.game = game
        self.fired = False

    def handle_event(self, event):
        if not self.fired:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    messagebox = EscapeMessageBox(self.game)
                    messagebox.run()
            if event == HeadCollisionHandlerPyGame.HEADCOLLISIONEVENT:
                messagebox = LossMessageBox(self.game)
                messagebox.run()
                self.fired = True
            if event == VictoryHandler.VICTORY_EVENT:
                messagebox = VictoryMessageBox(self.game)
                messagebox.run()
                self.fired = True
