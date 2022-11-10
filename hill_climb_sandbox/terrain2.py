import pygame
import pymunk
import pymunk.pygame_util
import terrain_maths

pygame.init()

WIDTH, HEIGHT = 1000, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))


def create_segment(space, radius, a, b):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, a, b, radius)
    shape.mass = 10
    shape.color = (255, 0, 0, 100)
    shape.elasticity = 0.2
    shape.friction = 1.5
    space.add(body, shape)
    return shape


def create_terrain(space, radius, width, height, spacing, smoothness=8):
    terrain_height = height//2
    height_coordinates = terrain_maths.return_terrain_height_cos(width // spacing, terrain_height, smoothness)
    for i in range(1, len(height_coordinates)):
        create_segment(space, radius, ((i-1)*spacing, height - height_coordinates[i-1]), ((i)*spacing, height - height_coordinates[i]))


def draw(space, window, draw_options):
    window.fill("white")


    space.debug_draw(draw_options)
    pygame.display.update()



def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1/fps

    space = pymunk.Space()
    space.gravity = (0, 981)


    create_terrain(space, 2, WIDTH, 10, 6)
    draw_options = pymunk.pygame_util.DrawOptions(window)



    while run:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break



        draw(space, window, draw_options)
        space.step(dt)
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)