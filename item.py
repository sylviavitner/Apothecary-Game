import pygame
from sprite import Sprite

class Item(Sprite):
    def __init__(self, img, name, stack_size=100, inside_inventory=True):
        super().__init__(img, size=32, num_frames=2, x_pos=0, y_pos=0, scale=3)
        self.name = name # red_berry, seed, or purple_berry
        self.stack_size = stack_size
        self.inside_inventory = inside_inventory
        self.slot_index = -1 # -1 for not in inventory, 0-29  for slots
        self.allow_click_to_move = False
        self.allow_pickup = False
        self.time_placed = None
        
    def add_to_inventory(self, inventory, amount=1):
        match self.name:
            case "red_berry":
                item = RedBerry()
            case "seed":
                item = Seed()
            case "purple_berry":
                item = PurpleBerry()

        inventory.add(item, amount)
        return item

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    # for clicking items and moving them (in or out of inventory/map)
    def handle_event(self, event, inventory, sprites, growables, all_items):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return sprites

        elif event.button == 1:
            if self.inside_inventory:
                if self.rect.collidepoint(event.pos):
                    if not self.allow_click_to_move:
                        self.allow_click_to_move = True
                        self.set_frame(1) # change to interaction frame
                    else:
                        self.allow_click_to_move = False
                        self.set_frame(0)
            
                elif self.allow_click_to_move:
                    for item in all_items:
                        if item.rect.collidepoint(event.pos) and item.inside_inventory:
                            self.allow_click_to_move = False
                            self.set_frame(0)
                            return sprites
                            # will need to swap items in inventory
                    match self.name:
                        case "red_berry":
                            new_item = RedBerry()
                        case "seed":
                            new_item = Seed()
                        case "purple_berry":
                            new_item = PurpleBerry()
                    # to track time for seeds and other future items that rely on time to grow
                    new_item.inside_inventory = False
                    new_item.time_placed = pygame.time.get_ticks()
                    new_item.set_position(event.pos[0] - self.size, event.pos[1] - self.size)
                    sprites.add(new_item)
                    inventory.remove(self, 1)

                    if new_item.name == "seed":
                        growables.add(new_item)
                    
                    self.allow_click_to_move = False
                    self.set_frame(0) # set back to original frame

        return sprites

class RedBerry(Item):
    def __init__(self):
        super().__init__("assets/red_berry.png", "red_berry")

import bush

class Seed(Item):

    def __init__(self):
        super().__init__("assets/seed.png", "seed")
        self.cooldown = 3000

    def grow_bush(self, current_time):
        if not self.inside_inventory and current_time - self.time_placed >= self.cooldown:
            b = bush.Bush("assets/bush.png", self.rect.x - self.size, self.rect.y - self.size)
            b.last_harvested = current_time
            b.has_berries = False
            b.can_harvest = False
            b.set_frame(0)
            return b
        return None

class PurpleBerry(Item):
    def __init__(self):
        super().__init__("assets/purple_berry.png", "purple_berry")