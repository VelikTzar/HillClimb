import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(pygame.Color('dodgerblue'))
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2((100, 200))

    def update(self, events, dt):
        pressed = pygame.key.get_pressed()
        move = pygame.Vector2((0, 0))
        if pressed[pygame.K_w]: move += (0, -1)
        if pressed[pygame.K_a]: move += (-1, 0)
        if pressed[pygame.K_s]: move += (0, 1)
        if pressed[pygame.K_d]: move += (1, 0)
        if move.length() > 0: move.normalize_ip()
        self.pos += move*(dt/5)
        self.rect.center = self.pos

def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    dt = 0
    player = Player()
    sprites = pygame.sprite.Group(player)
    # the "world" is now bigger than the screen
    # so we actually have anything to move the camera to
    background = pygame.Surface((100000, 1500))
    background.fill((30, 30, 30))

    # a camera is just two values: x and y
    # we use a vector here because it's easier to handle than a tuple
    camera = pygame.Vector2((0, 0))

    for _ in range(3000):
        x, y = random.randint(0, 1000), random.randint(0, 1000)
        pygame.draw.rect(background, pygame.Color('green'), (x, y, 2, 2))

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return

        # copy/paste because I'm lazy
        # just move the camera around
        pressed = pygame.key.get_pressed()
        camera_move = pygame.Vector2()
        if pressed[pygame.K_UP]: camera_move += (0, 1)
        if pressed[pygame.K_LEFT]: camera_move += (1, 0)
        if pressed[pygame.K_DOWN]: camera_move += (0, -1)
        if pressed[pygame.K_RIGHT]: camera_move += (-1, 0)
        if camera_move.length() > 0: camera_move.normalize_ip()
        camera += camera_move*(dt/5)

        sprites.update(events, dt)

        # before drawing, we shift everything by the camera's x and y values
        screen.blit(background, camera)
        for s in sprites:
            screen.blit(s.image, s.rect.move(*camera))

        pygame.display.update()
        dt = clock.tick(60)

if __name__ == '__main__':
    main()