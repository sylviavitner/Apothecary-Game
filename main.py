import pygame
import random
from player import Player
from shop_sprite import ShopSprite
from background import Background
from start_screen import StartScreen
from bush import Bush
from button import Button
from inventory import Inventory
from item import Item

pygame.init()

WIDTH, HEIGHT = 1920, 1080
FPS = 60
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
BG_COLORS = [(60, 163, 112), (150, 66, 83)] # map, shop
BG_STATE = 0

pygame.display.set_caption("Apothecary Shop Sim")

# initialize sprites
player = Player("assets/player.png", SCREEN)
shop_sprite = ShopSprite("assets/shop.png")
background = Background()
start_screen = StartScreen()

# todo: randomize bush spawns
bush = Bush("assets/bush.png")
bush2 = Bush("assets/bush.png", 1400, 800)
bush3 = Bush("assets/bush.png", 600, 700)
bushes = pygame.sprite.Group(bush, bush2, bush3)

# sprites that appear on the map (outside and only of the shop)
map_sprites = pygame.sprite.Group(shop_sprite, bush, bush2, bush3)

# shop buttons
exit_button = Button("assets/buttons.png", (WIDTH // 2) - 350, 50, "exit", 0)
open_close_button = Button("assets/buttons.png", (WIDTH // 2) - 50, 50, "open_close", 1)
buy_button = Button("assets/buttons.png", (WIDTH // 2) + 250, 50, "buy", 3)

# sprites that appear inside the shop (and only inside the shop)
shop_sprite_group = pygame.sprite.Group(exit_button, open_close_button, buy_button)

# inventory
inventory = Inventory("assets/slot.png")

run = True
while run:

    CLOCK.tick(FPS)
    current_time = pygame.time.get_ticks()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # player events
        player.handle_event(event, background, shop_sprite, map_sprites, inventory)
        # shop events
        for button in shop_sprite_group:
            button.handle_event(event, player, background, shop_sprite)
        # inventory events
        inventory.handle_event(event)

    # fill bg
    SCREEN.fill(background.current_bg)

    # before the game starts
    if player.shop_input_active:
        start_screen.draw(SCREEN, player, current_time)

    else:
        # check player collisions and move player
        player.check_collisions(map_sprites, shop_sprite_group)
        player.move(current_time, SCREEN)
        # grow berries after cooldown
        for b in bushes:
            b.grow_berries(current_time)
   
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

        # draw inventory
        inventory.draw(SCREEN)

    pygame.display.flip()

# exit game
pygame.quit()