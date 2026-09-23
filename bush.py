import pygame
import random
from sprite import Sprite

class Bush(Sprite):
    def __init__(self, img, x_pos=600, y_pos=400):
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
            self.last_harvested = pygame.time.get_ticks()



