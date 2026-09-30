# main game loop

import pygame
from player import Player
from shop_sprite import ShopSprite
from background import Background
from start_screen import StartScreen
from bush import Bush
from button import Button

pygame.init()

WIDTH, HEIGHT = 1920, 1080
FPS = 60
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
BG_COLORS = [(60, 163, 112), (150, 66, 83)] # map, shop
BG_STATE = 0

pygame.display.set_caption("Apothecary Shop Sim")

player = Player("assets/player.png", SCREEN)
shop_sprite = ShopSprite("assets/shop.png")
background = Background()
start_screen = StartScreen()
# bush (temp)
bush = Bush("assets/bush.png")

# all of the sprites that appear on the map are grouped and move together
map_sprites = pygame.sprite.Group(shop_sprite, bush)

# buttons
exit_button = Button("assets/buttons.png", 300, 900, "exit", 0)
open_close_button = Button("assets/buttons.png", 700, 900, "open_close", 1)
edit_button = Button("assets/buttons.png", 1100, 900, "edit", 3)
buy_button = Button("assets/buttons.png", 1500, 900, "buy", 4)

shop_sprite_group = pygame.sprite.Group(exit_button, open_close_button, edit_button, buy_button)

run = True
while run:

    CLOCK.tick(FPS)
    current_time = pygame.time.get_ticks()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        player.handle_event(event, background, shop_sprite, map_sprites)

    # fill bg
    SCREEN.fill(background.current_bg)

    if player.shop_input_active:
        start_screen.draw(SCREEN, player, current_time)

    else:
        # check player collisions and move player
        player.check_collisions(map_sprites, shop_sprite_group)
        player.move(current_time, SCREEN)
        bush.grow_berries(current_time)
   
        # move sprites opposite of player
        for sprite in map_sprites:
            sprite.move(-player.dx * player.speed, -player.dy * player.speed)

        # draw sprites
        for sprite in map_sprites:
            sprite.draw(SCREEN)

        for sprite in shop_sprite_group:
            sprite.draw(SCREEN)

        # draw player
        player.draw(SCREEN)

    pygame.display.flip()

# exit game
pygame.quit()