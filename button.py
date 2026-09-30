import pygame
from sprite import Sprite

class Button(Sprite):
    def __init__(self, img, x_pos=200, y_pos=600, type="exit", frame=0):
        super().__init__(img, size=64, num_frames=5, x_pos=x_pos, y_pos=y_pos, scale=3, frame=frame)
        self.images = pygame.image.load(img).convert_alpha()
        self.type = type

    def detect_mouse_press(self):
        pass






        