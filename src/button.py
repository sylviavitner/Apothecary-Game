import pygame
from sprite import Sprite
from item import ItemStand, EmptyFlask, Cauldron

class Button(Sprite):
    def __init__(self, img, x_pos=200, y_pos=600, type="exit", frame=0, scale=2):
        super().__init__(img, size=64, num_frames=4, x_pos=x_pos, y_pos=y_pos, scale=scale, frame=frame)
        self.images = pygame.image.load(img).convert_alpha()
        self.type = type
        self.name = "button"
        self.show = False

    def handle_event(self, event, player, background, shop, shop_screen, inventory, all_items, buttons):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        elif event.button == 1: # left mouse click
            if self.show and self.rect.collidepoint(event.pos):
                match self.type:
                    case "exit":
                        player.inside_shop = False
                        player.rect.center = player.map_position
                        background.set_state(0)
                        shop.set_state(0)
                        for b in buttons:
                            if b.type == "open_close":
                                b.set_frame(1)
                                player.shop_open = False
                    case "open_close":
                        if self.frame == 1:
                            self.set_frame(2)
                            player.shop_open = True
                        elif self.frame == 2:
                            self.set_frame(1)
                            player.shop_open = False
                    #case "edit":
                        #pass
                    case "buy":
                        shop_screen.show = not shop_screen.show
                    case "item_stand":
                        item_stand = ItemStand(inside_inventory=True)
                        if player.coins >= item_stand.market_price:
                            all_items.add(item_stand.add_to_inventory(inventory))
                            player.coins -= item_stand.market_price
                    case "empty_flask":
                        flask = EmptyFlask(inside_inventory=True)
                        if player.coins >= flask.market_price:
                            all_items.add(flask.add_to_inventory(inventory))
                            player.coins -= flask.market_price
                    case "cauldron":
                       cauldron = Cauldron(inside_inventory=True)
                       if player.coins >= cauldron.market_price:
                            all_items.add(cauldron.add_to_inventory(inventory))
                            player.coins -= cauldron.market_price







        