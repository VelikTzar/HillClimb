from game.classes_pygame import *
from pymunk import pygame_util
from game.classes_pymunk import Car


class Game:
    HEIGHT = 600
    DISPLAY_W = 400
    DISPLAY_H = 600
    FPS = 60

    def __init__(self, app, settings):
        self.car_rate = None
        self.car_max_force = None
        self.height_amplitude = None
        self.smoothness = None
        self.gravity = None
        self.terrain_spacing = None
        self.width = None
        self.load_sprites = False
        self.settings = settings
        self.load_settings(settings)
        self.app = app
        self.done = False
        self.clock = pygame.time.Clock()

        self.display_window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.Surface((self.width, self.HEIGHT))

        # Pymunk stuff.
        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0.0, self.gravity)

        # A sprite group which holds the pygame.sprite.Sprite objects.
        self.sprite_group = pygame.sprite.Group()

        # objects_group - handles events relating to pymunk objects (gas/drive)
        self.objects_group = []

        self.camera = Camera(self.DISPLAY_W, self.DISPLAY_H, self.width, self.HEIGHT)

    def run(self):
        while not self.done:
            self.run_logic()
            self.draw()
            self.handle_events()
            self.handle_event_generation()
            self.clock.tick(self.FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                self.app.running = False
            for obj in self.objects_group:
                obj.handle_event(event)
        else:
            self.handle_pressed_keys()

    def handle_pressed_keys(self):
        for obj in self.objects_group:
            obj.handle_keys()

    def handle_event_generation(self):
        for obj in self.objects_group:
            obj.generate_event()

    def run_logic(self):
        self.space.step(1/self.FPS)  # Update physics.
        self.sprite_group.update()  # Update pygame sprites.

    def show_distance(self):
        font = pygame.font.Font(None, 30)
        distance = self.camera.get_coordinates()
        x_distance = distance[0]
        y_distance = distance[1]
        text = f'Distance: {x_distance: .2f}'
        text_surface = font.render(text, True, 'black')
        text_rect = text_surface.get_rect()
        text_rect.center = (100, 50)
        self.display_window.blit(text_surface, text_rect)

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, 'black')
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display_window.blit(text_surface, text_rect)

    def draw(self):
        self.window.fill('cadetblue1')

        draw_options = pymunk.pygame_util.DrawOptions(self.window)
        draw_options.flags = \
            pymunk.SpaceDebugDrawOptions.DRAW_SHAPES | pymunk.SpaceDebugDrawOptions.DRAW_COLLISION_POINTS
        self.space.debug_draw(draw_options)

        self.sprite_group.draw(self.window)

        offset = self.camera.follow_coordinates()

        self.display_window.blit(self.window, offset)
        self.show_distance()

        pygame.display.update()

    def load_settings(self, settings):
        self.settings = settings
        self.gravity = self.settings.gravity
        self.terrain_spacing = self.settings.terrain_spacing
        self.height_amplitude = self.settings.terrain_amplitude
        self.smoothness = self.settings.terrain_smoothness
        self.width = self.settings.map_length
        self.car_rate = self.settings.car_rate
        self.car_max_force = self.settings.car_max_force
        self.load_sprites = self.settings.load_sprites

    def run_game_loop(self):
        pygame.init()

        space = self.space
        terrain = Terrain(space, self.width, self.HEIGHT)
        terrain_bodies = terrain.generate_terrain(self.terrain_spacing, self.height_amplitude, self.smoothness)
        boundaries = Boundaries(space, self.width, self.HEIGHT)
        boundaries.generate_boundaries()
        Car.RATE = self.car_rate
        Car.MAX_FORCE = self.car_max_force

        pos = terrain.return_spawn()
        player = Player(pos, space)
        car = CarMovementHandler(player.car)
        head = HeadCollisionHandlerPyGame(space, self)
        victory_checker = VictoryHandler(self, player)
        message_boxes = MessageBox(self)
        self.objects_group.append(car)
        self.objects_group.append(head)
        self.objects_group.append(victory_checker)
        self.objects_group.append(message_boxes)

        if self.load_sprites:
            car_image_path = 'sprites\car.png'
            head_image_path = 'sprites\headLarge.png'
            wheel_image_path = 'sprites\wheel.png'
            car_image = pygame.image.load(car_image_path)
            head_image = pygame.image.load(head_image_path)
            wheel_image = pygame.image.load(wheel_image_path)
            car_image = pygame.transform.scale(car_image, (1.2 * Car.WIDTH, 4 * Car.HEIGHT))
            head_image = pygame.transform.scale(head_image,
                                                (3 * player.person.head_shape.radius,
                                                 3 * player.person.head_shape.radius))
            wheel_image = pygame.transform.scale(wheel_image, (2.1 * Car.WHEEL_RADIUS, 2.1 * Car.WHEEL_RADIUS))
            car_sprite = Entity(body=player.car.chassis_body,
                                space=space, window=self.window, height=self.HEIGHT, image=car_image)
            head_sprite = Entity(body=player.person.head_body,
                                 space=space, window=self.window, height=self.HEIGHT, image=head_image)
            wheel1 = Entity(body=player.car.wheel1_body,
                            space=space, window=self.window, height=self.HEIGHT, image=wheel_image)
            wheel2 = Entity(body=player.car.wheel2_body,
                            space=space, window=self.window, height=self.HEIGHT, image=wheel_image)
            self.sprite_group.add(car_sprite)
            self.sprite_group.add(head_sprite)
            self.sprite_group.add(wheel1)
            self.sprite_group.add(wheel2)

        self.camera.set_obj(car)

        self.run()


