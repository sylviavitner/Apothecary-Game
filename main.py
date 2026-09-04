# main game loop

import pygame

pygame.init()

WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
BG_COLOR = (60, 163, 112)

pygame.display.set_caption("Apothecary Shop Sim")

run = True
while run:

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # draw bg and sprites
    SCREEN.fill(BG_COLOR)

    pygame.display.flip()

# exit game
pygame.quit()