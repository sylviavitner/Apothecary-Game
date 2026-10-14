import pygame
from sprite import Sprite

class Item(Sprite):
    def __init__(self, img, name, stack_size=100, inside_inventory=True):
        super().__init__(img, size=32, num_frames=2, x_pos=0, y_pos=0, scale=3)
        self.name = name # red_berry, seed, or purple_berry
        self.stack_size = stack_size
        self.inside_inventory = inside_inventory
        self.slot_index = -1 # -1 for not in inventory, 0-29  for slots
        self.allow_move = False
        
    def add_to_item_slot(self, inventory, amount=1):
        self.slot_index = inventory.add(self, amount)

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    # for clicking items and moving them (in or out of inventory/map, swapping slots, brewing, etc.)
    def handle_event(self, event, inventory, sprites):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return sprites

        elif event.button == 1:
            if self.inside_inventory:
                if self.rect.collidepoint(event.pos):
                    self.allow_move = True
                    self.set_frame(1) # change to interaction frame
            
                elif self.allow_move:
                    match self.name:
                        case "red_berry":
                            new_item = RedBerry()
                        case "seed":
                            new_item = Seed()
                        case "purple_berry":
                            new_item = PurpleBerry()
                    new_item.set_position(event.pos[0], event.pos[1])
                    sprites.add(new_item)
                    inventory.remove(self, 1)
                    self.allow_move = False
                    self.set_frame(0) # set back to original frame

        return sprites

class RedBerry(Item):
    def __init__(self):
        super().__init__("assets/red_berry.png", "red_berry")

class Seed(Item):
    def __init__(self):
        super().__init__("assets/seed.png", "seed")

class PurpleBerry(Item):
    def __init__(self):
        super().__init__("assets/purple_berry.png", "purple_berry")