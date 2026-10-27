import pygame
from player import Player
from shop_sprite import ShopSprite
from background import Background
from start_screen import StartScreen
from bush import Bush
from button import Button
from inventory import Inventory
from shop_window import ShopWindow

pygame.init()

WIDTH, HEIGHT = 1920, 1080
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
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
shop_window = ShopWindow("assets/shop_screen.png", SCREEN)

# Generate 5 bushes at random positions (close to spawn)
#bushes = pygame.sprite.Group()
#def gen_bush():
    #bush = Bush("assets/bush.png")
    #bush.randomize_position(WIDTH, HEIGHT)
    #collide = False
    #if bushes:
        #for b in bushes:
            #if bush.detect_collision(b):
                #gen_bush()
                #collide=True
    #if bush.detect_collision(shop_sprite) or bush.detect_collision(player):
        #gen_bush()
        #collide=True
    #if not collide:
        #bushes.add(bush)
#for i in range(5):
    #gen_bush()

# shop buttons
open_close_button = Button("assets/buttons.png", CENTER_X - 64, 50, "open_close", 1) # 64 for size scaled by 2
exit_button = Button("assets/buttons.png", open_close_button.rect.x - (open_close_button.size*2) - 128, 50, "exit", 0)
buy_button = Button("assets/buttons.png", open_close_button.rect.right + 128, 50, "buy", 3)

# starting bushes
bush = Bush("assets/bush.png", CENTER_X - 384, CENTER_Y - 50)
bush2 = Bush("assets/bush.png", CENTER_X + 224, CENTER_Y - 50)

# sprite groups (at start)
bushes = pygame.sprite.Group(bush, bush2)
shop_buttons = pygame.sprite.Group(open_close_button, exit_button, buy_button)
map_sprites = pygame.sprite.Group(shop_sprite, bush, bush2) # sprites that appear on the map (outside and only of the shop)
shop_sprite_group = pygame.sprite.Group(exit_button, open_close_button, buy_button) # sprites that appear inside the shop (and only inside the shop)
all_items = pygame.sprite.Group()
growables = pygame.sprite.Group()

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
        player.handle_event(event, background, shop_sprite, map_sprites, shop_sprite_group, inventory, all_items)
        # mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            # shop button events
            for button in shop_buttons:
                button.handle_event(event, player, background, shop_sprite, shop_window, inventory, all_items)
            for button in shop_window.buttons:
                button.handle_event(event, player, background, shop_sprite, shop_window, inventory, all_items)

            # update item positions (inventory, map, and shop)
            if all_items:
                for item in all_items:
                    if not player.inside_shop:
                        map_sprites = item.handle_event(event, inventory, map_sprites, growables, all_items)
                    else:
                        shop_sprite_group = item.handle_event(event, inventory, shop_sprite_group, growables, all_items)
            
            
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

        # grow growable items after a cooldown
        if growables:
            for g in growables:
                b = g.grow_bush(current_time)
                if b:
                    bushes.add(b)
                    map_sprites.add(b)
                    g.kill()


        # move sprites opposite of player
        for sprite in map_sprites:
            sprite.move(-player.dx * player.speed, -player.dy * player.speed)

        # draw sprites
        for sprite in map_sprites:
            sprite.draw(SCREEN)

        for sprite in shop_sprite_group:
            if sprite.name == "button":
                continue
            else:
                sprite.draw(SCREEN)

        # draw player
        player.draw(SCREEN)

        # draw inventory
        inventory.draw(SCREEN)

        # shop screen (if visible)
        shop_window.draw(SCREEN, player)

        # draw buttons last
        for b in shop_buttons:
            b.draw(SCREEN)

    pygame.display.flip()

# exit game
pygame.quit()