import pygame
from random import randint
from sprite import Sprite
from item import RedBerry, Seed

class Bush(Sprite):
    def __init__(self, img, x_pos=400, y_pos=600):
        # now inherits from Sprite class
        super().__init__(img, size=32, num_frames=4, x_pos=x_pos, y_pos=y_pos, scale=5, frame=2)
        self.name = "bush"
        self.has_berries = True
        self.can_harvest = False
        self.last_harvested = pygame.time.get_ticks()
        self.berry_cooldown = 30000

    def grow_berries(self, current_time):
        if current_time - self.last_harvested >= self.berry_cooldown:
            self.has_berries = True

    def harvest(self, inventory):
        self.can_harvest = False
        self.has_berries = False
        self.set_frame(0)
        self.last_harvested = pygame.time.get_ticks()
        # for now, creates a new berry and adds to inventory
        n = randint(1, 100)
        # Pick between dropping a red berry or seed
        if n > 50:
            item = RedBerry()
        else:
            item = Seed()
        inventory.add(item)




