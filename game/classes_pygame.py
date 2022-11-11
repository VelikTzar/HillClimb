import pygame
import pymunk
import pymunk.pygame_util
from game.common_functions import *


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
        #pos = convert_coordinates(self.body.position, self.height)
        self.rect.center = self.body.position
        self.image = pygame.transform.rotate(
            self.orig_image, -math.degrees(self.body.angle))
        self.rect = self.image.get_rect(center=self.rect.center)


class CarMovementHandler:
    def __init__(self, car):
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
        if keys[pygame.K_RIGHT]:
            self.car.gas()


class PersonCollisionHandler:
    pass


class Camera:
    def __init__(self, display_width, display_height, total_width, total_height):
        self.obj = None
        self.display_width = display_width
        self.display_height = display_height
        self.total_width = total_width
        self.total_height = total_height

    def set_obj(self, obj):
        self.obj = obj

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