import pygame

class Customer(pygame.sprite.Sprite):
    def __init__(self, img, screen):
        pygame.sprite.Sprite.__init__(self)
        self.images = None
        self.size = 32
        self.scale = 3
        self.speed = 5
        self.frames_list = None