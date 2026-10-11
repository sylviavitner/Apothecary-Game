import pygame
from sprite import Sprite

class ItemSlot(Sprite):
    def __init__(self, img, x_pos=0, y_pos=0, scale=3):
        super().__init__ (img, size=32, num_frames=1, x_pos=x_pos, y_pos=y_pos, scale=scale, frame=0)
        self.item = None
        self.quantity = 0
        
