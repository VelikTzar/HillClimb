import pygame
import pymunk
import pymunk.pygame_util
import math



def calculate_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)


def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])


def create_boundaries(space, width, height):
    rectangles = [
        [(width/2, height-10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(10, height/2), (20, height)],
    ]
    for pos, size in rectangles:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)


def add_ball(space, radius, mass, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.color = (255, 0, 0, 100)
    shape.elasticity = 0.9
    shape.friction = 1
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


def draw(space, window, draw_options):
    window.fill("white")

    space.debug_draw(draw_options)
    pygame.display.update()


def car(space, pos):

    rect = add_rectangle(space, pos, (50, 20), 1)
    wheel1 = add_ball(space, 10, 1, (pos[0]-25, pos[1]+10))
    wheel2 = add_ball(space, 10, 1, (pos[0]+25, pos[1]+10))
    joint1 = pymunk.PinJoint(rect.body, wheel1.body, (-25, 10), (0, 0))
    joint2 = pymunk.PinJoint(rect.body, wheel2.body, (25, 10), (0, 0))
    joint1.collide_bodies = False
    joint2.collide_bodies = False
    motor1 = pymunk.SimpleMotor(rect.body, wheel1.body, 0)
    motor1.collide_bodies = False
    #motor2 = pymunk.SimpleMotor(rect.body, wheel2.body, 0)
    #motor2.collide_bodies = False
    #motor1.activate_bodies()
    space.add(joint1, joint2, motor1)
    return motor1


def car2(space, speed=10, add_car=True):
    car_pos = pymunk.Vec2d(100,300)

    #bodies
    wheel_color = (0,0,0,100)
    chassi_color = (255,0,0,100)
    wheelCon_color = (0,255,255,100)

    #Wheel 1
    mass = 25
    radius = 10
    moment = pymunk.moment_for_circle(mass, 20, radius)
    wheel1_b = pymunk.Body(mass, moment)
    wheel1_s = pymunk.Circle(wheel1_b, radius)
    wheel1_s.friction = 1.5
    wheel1_s.color = wheel_color

    #Wheel 2
    mass = 25
    radius = 10
    moment = pymunk.moment_for_circle(mass, 20, radius)
    wheel2_b = pymunk.Body(mass, moment)
    wheel2_s = pymunk.Circle(wheel2_b, radius)
    wheel2_s.friction = 1.5
    wheel2_s.color = wheel_color

    #Chassi
    mass = 30
    size = w, h = (80, 25)
    moment = pymunk.moment_for_box(mass, size)
    chassi_b = pymunk.Body(mass, moment)
    vs = [(-w/2, -h/2), (w/4, -h/2), (w/2, -3*h/10),
          (w/2, h/2), (-w/2, h/2)]
    chassi_s = pymunk.Poly(chassi_b, vs)
    chassi_s.color = chassi_color

    #Windshield
    ww, wh, wt = (w/3, 0.8*h, w/16) # windshield width, windshield height, windshield thickness
    moment = pymunk.moment_for_box(mass, size)
    #windshield_b = pymunk.Body(mass, moment)
    wvs = [(-ww/2 + w/5, -wh/2 - h/2),
           (-ww/2 + wt + w/5, -wh/2 - h/2),
          (ww/2 - wt + w/5, wh/2 - h/2),
           (ww/2 + w/5, wh/2 - h/2)]
    windshield_s = pymunk.Poly(chassi_b, wvs)
    windshield_s.color = chassi_color

    # Positions
    chassi_b.position = car_pos + (0, -0.6*h)
    wheel1_b.position = car_pos + (-0.3125*w, 0)
    wheel2_b.position = car_pos + (0.3125*w, 0)

    # Joints
    spring1 = pymunk.DampedSpring(chassi_b, wheel1_b, (-25,0), (0,0), 15, 5000, 250)
    spring1.collide_bodies = False
    spring2 = pymunk.DampedSpring(chassi_b, wheel2_b, (25,0), (0,0), 15, 5000, 250)
    spring2.collide_bodies = False

    groove1 = pymunk.GrooveJoint(chassi_b, wheel1_b, (-25,0), (-25,25), (0, 0))
    groove1.collide_bodies = False
    groove2 = pymunk.GrooveJoint(chassi_b, wheel2_b, (25,0), (25,25), (0,0))
    groove2.collide_bodies = False

    if add_car:
        motor1 = pymunk.SimpleMotor(wheel1_b, chassi_b, speed)
        motor2 = pymunk.SimpleMotor(wheel2_b, chassi_b, speed)
        space.add(
            spring1,
            spring2,
            groove1,
            groove2,
            motor1,
            motor2,
            chassi_b,
            chassi_s,
            windshield_s,
            wheel2_b,
            wheel2_s,
            wheel1_b,
            wheel1_s
        )

