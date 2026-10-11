import pygame
from sprite import Sprite

class Item(Sprite):
    def __init__(self, img, name, stack_size=100):
        super().__init__(img, size=32, num_frames=1, x_pos=0, y_pos=0, scale=3)
        self.name = name # just red_berry for now
        self.stack_size = stack_size

    def add_to_item_slot(self, inventory, amount=1):
        inventory.add(self, amount)

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y