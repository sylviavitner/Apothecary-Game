import pygame
from sprite import Sprite

class Item(Sprite):
    def __init__(self, img, name, stack_size=100):
        super().__init__(img, size=32, num_frames=1, x_pos=0, y_pos=0, scale=3)
        self.name = name # red_berry or seed
        self.stack_size = stack_size

    def add_to_item_slot(self, inventory, amount=1):
        inventory.add(self, amount)

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def remove_from_item_slot(self, inventory, amount=1):
        pass
        # inventory.remove(self, amount)


    # for clicking items and moving them (in or out of inventory/map, swapping slots, brewing, etc.)
    def handle_event(self, event):
        pass

class RedBerry(Item):
    def __init__(self):
        super().__init__("assets/red_berry.png", "red_berry")

class Seed(Item):
    def __init__(self):
        super().__init__("assets/seed.png", "seed")