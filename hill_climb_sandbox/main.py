import terrain2
from functions import *
from camera import *

pygame.init()

WIDTH, HEIGHT = 2000, 800
window = pygame.display.set_mode((WIDTH/2, HEIGHT))


def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1/fps

    space = pymunk.Space()
    space.gravity = (0, 981)

    create_boundaries(space, width, height)
    terrain2.create_terrain(space, 2, WIDTH, HEIGHT, 20, 6)
    draw_options = pymunk.pygame_util.DrawOptions(window)

    pressed_pos = None
    cara = car2(space)

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                cara.max_force = 0
            elif event.type == pygame.KEYDOWN:
                cara.max_force = 10000

        draw(space, window, draw_options)
        pygame.display.update()
        space.step(dt)
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)