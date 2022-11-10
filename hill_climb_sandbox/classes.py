import pygame
import pymunk
import pymunk.pygame_util
import math


def add_ball(space, radius, mass, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.color = (255, 0, 0, 100)
    shape.elasticity = 0.9
    shape.friction = 0.4
    space.add(body, shape)
    return shape


def add_rectangle(space, pos, size, mass):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Poly.create_box(body, size)
    shape.mass = mass
    shape.color = (0, 0, 255, 100)
    shape.elasticity = 0.4
    shape.friction = 0.5
    space.add(body, shape)
    return shape


class App:
    size = 1000, 800

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.running = True


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((255, 255, 255))
            space.debug_draw(self.draw_options)
            pygame.display.update()
            space.step(0.01)

        pygame.quit()


class Box:
    def __init__(self, space, width, height):
        rectangles = [
            [(width / 2, height - 10), (width, 20)],
            [(width / 2, 10), (width, 20)],
            [(10, height / 2), (20, height)],
        ]
        for pos, size in rectangles:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = pos
            shape = pymunk.Poly.create_box(body, size)
            shape.elasticity = 0.4
            shape.friction = 0.5
            space.add(body, shape)


class Car:
    def __init__(self, pos, space):
        self.rect = add_rectangle(space, pos, (50, 20), 50)
        self.wheel1 = add_ball(space, 10, 10, (pos[0] - 25, pos[1] + 10))
        self.wheel2 = add_ball(space, 10, 10, (pos[0] + 25, pos[1] + 10))
        self.joint1 = pymunk.PinJoint(self.rect.body, self.wheel1.body, (-25, 10), (0, 0))
        self.joint2 = pymunk.PinJoint(self.rect.body, self.wheel2.body, (25, 10), (0, 0))
        self.joint1.collide_bodies = False
        self.joint2.collide_bodies = False
        self.motor = pymunk.SimpleMotor(self.rect.body, self.wheel2.body, 0)
        space.add(self.joint1, self.joint2, self.motor)

    def gas(self):
        self.motor.rate = -100

    def stop(self):
        self.motor.rate = 0


space = pymunk.Space()
space.gravity = 0, 981
b0 = space.static_body
app = App()
Box(space, 1000, 800)
Car((500, 400), space)
app.run()
