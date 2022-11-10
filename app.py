import math
import pygame
import pymunk
from classes_pymunk import *
from pymunk import pygame_util
from pymunk import Vec2d
from common_functions import *
from classes_pygame import *
from camera import *

WIDTH = 4000
HEIGHT = 600
DISPLAY_W = 400
DISPLAY_H = 600
FPS = 60


class Game:
    def __init__(self):
        self.done = False
        self.clock = pygame.time.Clock()

        self.display_window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
        self.window = pygame.Surface((WIDTH, HEIGHT))

        # Pymunk stuff.
        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0.0, 981)

        # A sprite group which holds the pygame.sprite.Sprite objects.
        self.sprite_group = pygame.sprite.Group()

        # objects_group - handles events relating to pymunk objects (gas/drive)
        self.objects_group = []

    def run(self):
        while not self.done:
            self.handle_events()
            self.run_logic()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
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
        self.space.step(1/FPS)  # Update physics.
        self.sprite_group.update()  # Update pygame sprites.

    def draw(self):
        # Debug draw. Outlines of the Pymunk shapes.
        #for obj in self.sprite_group:
        #    shape = obj.shape
        #    ps = [pos.rotated(shape.body.angle) + shape.body.position
        #          for pos in shape.get_vertices()]
        #    ps = [flipy((pos)) for pos in ps]
        #    ps += [ps[0]]
        #    pygame.draw.lines(self.window, self.red, False, ps, 1)
        self.window.fill("white")

        draw_options = pymunk.pygame_util.DrawOptions(self.window)
        draw_options.flags = \
            pymunk.SpaceDebugDrawOptions.DRAW_SHAPES | pymunk.SpaceDebugDrawOptions.DRAW_COLLISION_POINTS
        self.space.debug_draw(draw_options)

        self.sprite_group.draw(self.window)

        offset = [-car_sprite.rect.centerx + DISPLAY_W/2, -car_sprite.rect.centery + DISPLAY_H/2]
        if offset[0] > 0:
            offset[0] = 0
        if offset[1] > 0:
            offset[1] = 0
        if offset[0] + DISPLAY_W > WIDTH:
            offset[0] = WIDTH - DISPLAY_W
        if offset[1] + DISPLAY_H < HEIGHT:
            offset[1] = DISPLAY_H - HEIGHT

        self.display_window.blit(self.window, offset)

        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    game = Game()
    space = game.space
    pos = pymunk.Vec2d(100, 200)
    #ph_car = Car(pos, space)
    #person = Person(pos, space)

    player = Player(pos, space)
    car = CarMovementHandler(player.car)
    game.objects_group.append(car)
    terrain = Terrain(space, WIDTH, HEIGHT)
    terrain.generate_terrain(10, 0.5, 7)
    boundaries = Boundaries(space, WIDTH, HEIGHT)
    boundaries.generate_boundaries()


    image = pygame.image.load('pig.png')
    image = pygame.transform.scale(image, (80, 30))
    car_sprite = Entity(body=player.car.chassis_body, space=space, window=game.window, height=HEIGHT, image=image)
    game.sprite_group.add(car_sprite)

    game.run()
    pygame.quit()