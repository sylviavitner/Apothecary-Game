import pygame
from random import randint
from sprite import Sprite
from item import RedBerry, PurpleBerry, Seed

class Bush(Sprite):
    def __init__(self, img, x_pos=400, y_pos=600):
        # now inherits from Sprite class
        super().__init__(img, size=32, num_frames=4, x_pos=x_pos, y_pos=y_pos, scale=5, frame=2)
        self.name = "bush"
        self.has_berries = True
        self.can_harvest = False
        self.last_harvested = pygame.time.get_ticks()
        self.berry_cooldown = 30000

    def randomize_position(self, screen_w, screen_h):
        self.rect.x = randint(-200, screen_w + 200)
        self.rect.y = randint(-200, screen_h + 200)

    # regrow berries after the cooldown
    def grow_berries(self, current_time):
        if current_time - self.last_harvested >= self.berry_cooldown:
            self.has_berries = True

    # harvest materials and add them to inventory
    def harvest(self, inventory):
        self.can_harvest = False
        self.has_berries = False
        self.set_frame(0)
        self.last_harvested = pygame.time.get_ticks()

        n = randint(1, 100)

        # always add red or purple berry (0.95% and 0.05% chances)
        if n > 5:
            berry = RedBerry()
        else:
            berry = PurpleBerry()

        inventory.add(berry)

        # 1/10 chance of recieving seed in addition to berry
        if n <= 10:
            seed = Seed()
            inventory.add(seed)





