import pymunk
import pymunk.pygame_util
from game import terrain_maths


class Boundaries:
    THICKNESS = 20
    OFFSET = 10
    BOUNDARIES_ELASTICITY = 0.4
    BOUNDARIES_FRICTION = 5

    def __init__(self, space, width, height):
        self.space = space
        self.width = width
        self.height = height
        self.rectangles = [
            [(width / 2, height - Boundaries.OFFSET), (width, Boundaries.THICKNESS)],
            [(width / 2, Boundaries.OFFSET), (width, Boundaries.THICKNESS)],
            [(Boundaries.OFFSET, height / 2), (Boundaries.THICKNESS, height)],
            [(width - Boundaries.OFFSET, height / 2), (Boundaries.THICKNESS, height)],
        ]

    def generate_boundaries(self):
        for pos, size in self.rectangles:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = pos
            shape = pymunk.Poly.create_box(body, size)
            shape.elasticity = Boundaries.BOUNDARIES_ELASTICITY
            shape.friction = Boundaries.BOUNDARIES_FRICTION
            self.space.add(body, shape)


class Terrain:
    TERRAIN_COLOR = (156, 102, 31, 100)
    TERRAIN_ELASTICITY = 0.2
    TERRAIN_FRICTION = 1.5
    TERRAIN_THICKNESS = 5
    TERRAIN_COLLISION_TYPE = 2

    def __init__(self, space, width, height):
        self.spacing = None
        self.terrain_height_coordinates = None
        self.space = space
        self.thickness = Terrain.TERRAIN_THICKNESS
        self.width = width
        self.height = height

    @staticmethod
    def create_segment(space, radius, a, b):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, a, b, radius)
        shape.color = Terrain.TERRAIN_COLOR
        shape.elasticity = Terrain.TERRAIN_ELASTICITY
        shape.friction = Terrain.TERRAIN_FRICTION
        shape.collision_type = Terrain.TERRAIN_COLLISION_TYPE
        space.add(body, shape)
        return body

    # smoothness defines the number of iterations made during the cosine interpolation superposition
    def generate_terrain(self, spacing, max_height_ratio, smoothness=8):
        terrain_height = self.height * max_height_ratio
        self.spacing = spacing
        self.terrain_height_coordinates = terrain_maths.return_terrain_height_cos(self.width // spacing, terrain_height,
                                                                                  smoothness)
        segment_body_list = []
        for i in range(1, len(self.terrain_height_coordinates)):
            a = Terrain.create_segment(self.space, self.thickness,
                                       ((i - 1) * spacing, self.height - self.terrain_height_coordinates[i - 1]),
                                       (i * spacing, self.height - self.terrain_height_coordinates[i]))
            segment_body_list.append(a)
        return segment_body_list
        #    Terrain.create_segment(self.space, self.spacing,
        #                           (i * spacing, self.height),
        #                           (i * spacing, self.height - self.terrain_height_coordinates[i] + self.spacing))

    def return_spawn(self):
        a = (Boundaries.THICKNESS // self.spacing) + 1
        b = Car.WIDTH // self.spacing + 1
        c = self.terrain_height_coordinates.index(max(self.terrain_height_coordinates[a:(a + b)]))
        return pymunk.Vec2d((a * self.spacing + Car.WIDTH / 2), (
                    self.height - Terrain.TERRAIN_THICKNESS - self.terrain_height_coordinates[
                c] - Car.HEIGHT - 2 * Car.WHEEL_RADIUS))


class Car:
    CHASSIS_MASS = 30
    WHEEL_MASS = 25
    WHEEL_FRICTION = 1.5

    WHEEL_COLOR = (0, 0, 0, 0)
    CHASSIS_COLOR = (255, 0, 0, 0)
    WHEEL_CONT_COLOR = (0, 255, 255, 0)

    ACCELERATION = 1000
    DECCELERATION = 10000

    MAX_RATE = 200
    MAX_FORCE = 1000000

    WIDTH = 80
    HEIGHT = 80 / 4
    CHASSIS_SIZE = (WIDTH, HEIGHT)
    WHEEL_RADIUS = WIDTH / 8

    WHEEL_OFFSET_X = 5 * WIDTH / 16
    WHEEL_OFFSET_Y = 0
    CHASSIS_OFFSET_X = 0
    CHASSIS_OFFSET_Y = 3 * WIDTH / 16

    CHASSIS_CURVE_OFFSET_X = 5 * WIDTH / 12

    WINDSHIELD_WIDTH = WIDTH / 4
    WINDSHIELD_HEIGHT = HEIGHT * 0.8
    WINDSHIELD_THICKNESS = WIDTH / 16

    def __init__(self, pos, space):
        self.pos = pos
        self.space = space

        # wheels
        wheel_moment = pymunk.moment_for_circle(Car.WHEEL_MASS, 20, Car.WHEEL_RADIUS)

        # wheel1
        self.wheel1_body = pymunk.Body(Car.WHEEL_MASS, wheel_moment)
        self.wheel1_shape = pymunk.Circle(self.wheel1_body, Car.WHEEL_RADIUS)
        self.wheel1_shape.friction = Car.WHEEL_FRICTION
        self.wheel1_shape.color = Car.WHEEL_COLOR

        # wheel2
        self.wheel2_body = pymunk.Body(Car.WHEEL_MASS, wheel_moment)
        self.wheel2_shape = pymunk.Circle(self.wheel2_body, Car.WHEEL_RADIUS)
        self.wheel2_shape.friction = Car.WHEEL_FRICTION
        self.wheel2_shape.color = Car.WHEEL_COLOR

        # chassis
        chassis_moment = pymunk.moment_for_box(Car.CHASSIS_MASS, Car.CHASSIS_SIZE)
        w, h = Car.CHASSIS_SIZE
        self.chassis_body = pymunk.Body(Car.CHASSIS_MASS, chassis_moment)
        vs = [(-w / 2, -h / 2), (Car.CHASSIS_CURVE_OFFSET_X, -h / 2), (w / 2, -3 * h / 10),
              (w / 2, h / 2), (-w / 2, h / 2)]
        self.chassis_shape = pymunk.Poly(self.chassis_body, vs)
        self.chassis_shape.color = Car.CHASSIS_COLOR

        # Windshield
        #  w, h = Car.CHASSIS_SIZE
        ww, wh, wt = Car.WINDSHIELD_WIDTH, Car.WINDSHIELD_HEIGHT, Car.WINDSHIELD_THICKNESS
        wvs = [(-ww / 2 + 0.29 * w, -wh / 2 - h / 2),
               (-ww / 2 + wt + 0.29 * w, -wh / 2 - h / 2),
               (ww / 2 - wt + 0.29 * w, wh / 2 - h / 2),
               (ww / 2 + 0.29 * w, wh / 3 - h / 2)]
        self.windshield_shape = pymunk.Poly(self.chassis_body, wvs)
        self.windshield_shape.color = Car.CHASSIS_COLOR

        # Positions
        w, h = Car.CHASSIS_SIZE
        chassis_offset_x = Car.CHASSIS_OFFSET_X
        chassis_offset_y = Car.CHASSIS_OFFSET_Y
        wheels_offset_x = Car.WHEEL_OFFSET_X
        wheels_offset_y = Car.CHASSIS_OFFSET_Y

        self.chassis_body.position = self.pos + (chassis_offset_x, chassis_offset_y)
        self.wheel1_body.position = self.pos + (-wheels_offset_x, wheels_offset_y)
        self.wheel2_body.position = self.pos + (wheels_offset_x, wheels_offset_y)

        # Suspension/Joints
        self.spring1 = pymunk.DampedSpring(self.chassis_body, self.wheel1_body, (-wheels_offset_x, 0),
                                           (0, 0), 15, 5000, 250)
        self.spring1.collide_bodies = False
        self.spring2 = pymunk.DampedSpring(self.chassis_body, self.wheel2_body, (wheels_offset_x, 0),
                                           (0, 0), 15, 5000, 250)
        self.spring2.collide_bodies = False

        self.groove1 = pymunk.GrooveJoint(self.chassis_body, self.wheel1_body, (-wheels_offset_x, 0),
                                          (-wheels_offset_x, wheels_offset_x), (0, 0))
        self.groove1.collide_bodies = False
        self.groove2 = pymunk.GrooveJoint(self.chassis_body, self.wheel2_body, (wheels_offset_x, 0),
                                          (wheels_offset_x, wheels_offset_x), (0, 0))
        self.groove2.collide_bodies = False

        self.motor1 = pymunk.SimpleMotor(self.wheel1_body, self.chassis_body, 100)
        self.motor2 = pymunk.SimpleMotor(self.wheel2_body, self.chassis_body, 100)
        self.motor1.max_force = 1000
        self.motor2.max_force = 1000

        self.space.add(
            self.spring1,
            self.spring2,
            self.groove1,
            self.groove2,
            self.motor1,
            self.motor2,
            self.chassis_body,
            self.chassis_shape,
            self.windshield_shape,
            self.wheel1_body,
            self.wheel1_shape,
            self.wheel2_body,
            self.wheel2_shape,
        )

    def gas(self):
        accelaration = Car.ACCELERATION
        if self.motor1.max_force >= Car.MAX_FORCE:
            return
        self.motor1.max_force += accelaration
        self.motor2.max_force += accelaration

    def breaks(self):
        deccelaration = Car.DECCELERATION

        if (self.motor1.max_force - deccelaration) < 0.1 or (self.motor2.max_force - deccelaration) < 0.1:
            self.motor1.max_force = 0.1
            self.motor2.max_force = 0.1

        else:
            self.motor1.max_force -= deccelaration
            self.motor2.max_force -= deccelaration

    def slow_down(self):
        deccelaration = Car.ACCELERATION
        if (self.motor1.max_force - deccelaration) < 0.1 or (self.motor2.max_force - deccelaration) < 0.1:
            self.motor1.max_force = 0.1
            self.motor2.max_force = 0.1

        else:
            self.motor1.max_force -= deccelaration
            self.motor2.max_force -= deccelaration

    def get_velocity(self):
        return self.chassis_body.velocity


class Person:
    HEAD_COLLISION_TYPE = 1
    HEAD_COLOR = (0, 255, 0, 100)
    BODY_COLOR = (0, 0, 0, 100)
    # head/(neck-to-waist) = 1:3; 1/4 of total length (head-to-waist)
    HEAD_SIZE_RATIO = 1 / 2
    HEAD_FRICTION = 1
    HEIGHT = Car.HEIGHT
    WIDTH = Car.WIDTH / 4
    HEAD_RADIUS = HEAD_SIZE_RATIO * HEIGHT
    HEAD_MASS = 1
    BODY_MASS = 5
    BODY_SIZE = (WIDTH, HEIGHT - HEAD_RADIUS)

    def __init__(self, pos, space):
        self.pos = pos
        self.space = space

        # head
        head_moment = pymunk.moment_for_circle(Person.HEAD_MASS, 2 * Person.HEAD_RADIUS, Person.HEAD_RADIUS)
        self.head_body = pymunk.Body(Person.HEAD_MASS, head_moment)
        self.head_shape = pymunk.Circle(self.head_body, Person.HEAD_RADIUS)
        self.head_shape.friction = Person.HEAD_FRICTION
        self.head_shape.color = Person.HEAD_COLOR
        self.head_shape.collision_type = Person.HEAD_COLLISION_TYPE

        # body
        body_moment = pymunk.moment_for_box(Person.BODY_MASS, Person.BODY_SIZE)
        self.body_body = pymunk.Body(Person.BODY_MASS, body_moment)
        self.body_shape = pymunk.Poly.create_box(self.body_body, Person.BODY_SIZE)
        self.body_shape.color = Person.BODY_COLOR

        # joint
        self.pivot1 = pymunk.PivotJoint(self.head_body, self.body_body, (0, Person.HEAD_RADIUS),
                                        (0, -Person.BODY_SIZE[1] / 2))
        self.pivot1.collide_bodies = False
        self.spring1 = pymunk.DampedSpring(self.body_body, self.head_body, (0, 0),
                                           (0, 0), 15, 10000, 250)
        self.spring1.collide_bodies = False

        # position
        self.head_body.position = self.pos + (0, -(Person.HEAD_RADIUS + Car.HEIGHT) / 2)
        self.body_body.position = self.pos + (0, Person.HEAD_RADIUS)

        self.space.add(
            self.body_body,
            self.body_shape,
            self.head_body,
            self.head_shape,
            self.pivot1,
            self.spring1
        )


class HeadCollisionHandler:
    def __init__(self, space, handler_pygame):
        self.space = space
        self.handler_pygame = handler_pygame
        self.handler = self.space.add_collision_handler \
            (collision_type_a=Person.HEAD_COLLISION_TYPE, collision_type_b=Terrain.TERRAIN_COLLISION_TYPE)
        self.handler.begin = self.on_collision

    def on_collision(self, space, arbiter, dummy):
        self.handler_pygame.post_loss_event()
        return True


class Player:
    def __init__(self, pos, space):
        self.pos = pos
        self.space = space

        self.car = Car(pos, space)
        self.person = Person(pos + (0, (-Car.HEIGHT / 2 + Car.CHASSIS_OFFSET_Y)), space)

        self.pivot1 = pymunk.PivotJoint(self.person.body_body, self.car.chassis_body, (0, Person.BODY_SIZE[1] / 2),
                                        (0, 0))
        self.pivot1.collide_bodies = False

        self.spring1 = pymunk.DampedSpring(self.person.body_body, self.car.chassis_body,
                                           (0, Person.BODY_SIZE[1] / 2), (0, 0), 0, 100, 100)
        self.spring1.collide_bodies = False

        self.spring2 = pymunk.DampedSpring(self.person.body_body, self.car.chassis_body,
                                           (0, 0), (Car.WIDTH / 4, 0), Car.WIDTH / 4, 100, 100)
        self.spring2.collide_bodies = False

        self.space.add(
            self.pivot1,
            self.spring1,
            self.spring2
        )
