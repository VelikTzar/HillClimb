import pygame
import pymunk
import pymunk.pygame_util


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((700, 240))
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.image.save(self.screen, 'intro.png')

            self.screen.fill((220, 220, 220))
            space.debug_draw(self.draw_options)
            pygame.display.update()
            space.step(0.01)

        pygame.quit()


class Box:
    def __init__(self, p0=(10, 10), p1=(690, 230), d=2):
        x0, y0 = p0
        x1, y1 = p1
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for i in range(4):
            segment = pymunk.Segment(space.static_body, pts[i], pts[(i+1)%4], d)
            segment.elasticity = 1
            segment.friction = 1
            space.add(segment)


class PivotJoint:
    def __init__(self, b, b2, a=(0, 0), a2=(0, 0), collide=True):
        joint = pymunk.PinJoint(b, b2, a, a2)
        joint.collide_bodies = collide
        space.add(joint)

App()
space = pymunk.Space()
Box()


p = pymunk.Vec2d(200, 150)
vs = [(-50, -30), (50, -30), (50, 30), (-50, 30)]
v0, v1, v2, v3 = vs
chassis = pymunk.Poly(p, vs)

wheel1 = pymunk.Circle(p+v0)
wheel2 = pymunk.Circle(p+v1)

PivotJoint(chassis.body, wheel1.body, v0, (0, 0), False)
pymunk.SimpleMotor(chassis.body, wheel1.body, 5)

PivotJoint(chassis.body, wheel2.body, v1, (0, 0), False)
pymunk.SimpleMotor(chassis.body, wheel2.body, 5)

App().run()