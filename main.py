# main game loop

import pygame
from player import Player

pygame.init()

WIDTH, HEIGHT = 1920, 1080
FPS = 60
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
BG_COLOR = (60, 163, 112)

pygame.display.set_caption("Apothecary Shop Sim")

player = Player("assets/player.png")

run = True
while run:

    CLOCK.tick(FPS)
    current_time = pygame.time.get_ticks()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # draw bg and sprites
    SCREEN.fill(BG_COLOR)

    player.move(current_time)
    player.draw(SCREEN)

    pygame.display.flip()

# exit game
pygame.quit()