import pygame
from sprite import Sprite
from item import ItemStand

class Button(Sprite):
    def __init__(self, img, x_pos=200, y_pos=600, type="exit", frame=0, scale=2):
        super().__init__(img, size=64, num_frames=4, x_pos=x_pos, y_pos=y_pos, scale=scale, frame=frame)
        self.images = pygame.image.load(img).convert_alpha()
        self.type = type
        self.name = "button"

    def handle_event(self, event, player, background, shop, shop_screen, inventory, all_items):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        elif event.button == 1: # left mouse click
            if self.rect.collidepoint(event.pos) and self.show:
                match self.type:
                    case "exit":
                        player.inside_shop = False
                        player.rect.center = player.map_position
                        background.set_state(0)
                        shop.set_state(0)
                    case "open_close":
                        if self.frame == 1:
                            self.set_frame(2)
                        elif self.frame == 2:
                            self.set_frame(1)
                    #case "edit":
                        #pass
                    case "buy":
                        shop_screen.show = not shop_screen.show
                    case "item_stand":
                        # implement coin logic here too
                        item_stand = ItemStand()
                        item_stand.add_to_inventory(inventory)
                        all_items.add(item_stand)







        