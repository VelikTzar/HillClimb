import pygame
import pymunk
import pymunk.pygame_util
from common_functions import *


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
            self.orig_image, math.degrees(self.body.angle))
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
