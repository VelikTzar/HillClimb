import math
import os

import pygame
import pymunk
from game.classes_pymunk import *
from game.classes_pygame import *
from pymunk import pygame_util


class Game:
    WIDTH = 4000
    HEIGHT = 600
    DISPLAY_W = 400
    DISPLAY_H = 600
    FPS = 60

    def __init__(self, app):
        self.app = app
        self.done = False
        self.clock = pygame.time.Clock()

        self.display_window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.Surface((self.WIDTH, self.HEIGHT))

        # Pymunk stuff.
        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0.0, 300)

        # A sprite group which holds the pygame.sprite.Sprite objects.
        self.sprite_group = pygame.sprite.Group()

        # objects_group - handles events relating to pymunk objects (gas/drive)
        self.objects_group = []

        self.camera = Camera(self.DISPLAY_W, self.DISPLAY_H, self.WIDTH, self.HEIGHT)

    def run(self):
        while not self.done:
            self.handle_events()
            self.run_logic()
            self.draw()
            self.clock.tick(self.FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                self.app.running = False
            for obj in self.objects_group:
                obj.handle_event(event)
        #   for sprite in self.sprite_group:
            #   sprite.handle_event(event)
        else:
            self.handle_pressed_keys()

    def handle_pressed_keys(self):
        for obj in self.objects_group:
            obj.handle_keys()

    def run_logic(self):
        self.space.step(1/self.FPS)  # Update physics.
        self.sprite_group.update()  # Update pygame sprites.

    def draw(self):
        self.window.fill("white")

        draw_options = pymunk.pygame_util.DrawOptions(self.window)
        draw_options.flags = \
            pymunk.SpaceDebugDrawOptions.DRAW_SHAPES | pymunk.SpaceDebugDrawOptions.DRAW_COLLISION_POINTS
        self.space.debug_draw(draw_options)

        self.sprite_group.draw(self.window)

        offset = self.camera.follow_coordinates()

        self.display_window.blit(self.window, offset)

        pygame.display.update()

    def run_game_loop(self):
        pygame.init()

        space = self.space

        # ph_car = Car(pos, space)
        # person = Person(pos, space)

        terrain = Terrain(space, self.WIDTH, self.HEIGHT)
        terrain.generate_terrain(10, 0.5, 7)
        boundaries = Boundaries(space, self.WIDTH, self.HEIGHT)
        boundaries.generate_boundaries()

        pos = terrain.return_spawn()
        player = Player(pos, space)
        car = CarMovementHandler(player.car)
        self.objects_group.append(car)
        
        image_path = 'sprites\pig.png'
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (80, 20))
        car_sprite = Entity(body=player.car.chassis_body, space=space, window=self.window, height=self.HEIGHT, image=image)
        self.sprite_group.add(car_sprite)
        self.camera.set_obj(car_sprite)

        self.run()


