import pygame

class ShopScreen():
    def __init__(self, img, screen):
        self.size = 256
        self.scale = 3
        image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.scale(image, (self.size * self.scale, self.size * self.scale))
        self.rect = self.image.get_rect()
        self.rect.center = screen.get_rect().center
        self.show = False

    def draw(self, screen):
        if self.show:
            screen.blit(self.image, (self.rect.x, self.rect.y))
