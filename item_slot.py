import pygame
from sprite import Sprite

class InventorySlot(Sprite):
    def __init__(self, img, x_pos, y_pos):
        super().__init__ (img, size=32, num_frames=1, x_pos=x_pos, y_pos=y_pos, scale=5, frame=0)
        self.image = pygame.image.load(img).convert_alpha()
        self.item = None
        self.quantity = 0
        
