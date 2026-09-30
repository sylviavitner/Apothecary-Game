import pygame

class Button():
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)

        self.images = pygame.image.load(img).convert_alpha()
        self.scale = 3

        