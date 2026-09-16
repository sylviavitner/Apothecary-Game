# main game loop

import pygame
from player import Player
from shop_sprite import ShopSprite
from background import Background
from start_screen import StartScreen

pygame.init()

WIDTH, HEIGHT = 1920, 1080
FPS = 60
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
BG_COLORS = [(60, 163, 112), (150, 66, 83)] # map, shop
BG_STATE = 0

pygame.display.set_caption("Apothecary Shop Sim")

player = Player("assets/player.png")
shop_sprite = ShopSprite("assets/shop.png")
background = Background()
start_screen = StartScreen()

run = True
while run:

    CLOCK.tick(FPS)
    current_time = pygame.time.get_ticks()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        player.handle_event(event, background, shop_sprite)

    # fill bg
    SCREEN.fill(background.current_bg)

    if player.shop_input_active:
        start_screen.draw(SCREEN, player, current_time)

    else:
        # draw shop sprite on map
        shop_sprite.draw(SCREEN)
        # move and draw player
        player.check_collisions(shop_sprite)
        player.move(current_time)
        player.draw(SCREEN)

    pygame.display.flip()

# exit game
pygame.quit()