import pygame
from sprite import Sprite

class ShopSprite(Sprite):
    def __init__(self, img, x_pos=800, y_pos=100):
        # now inherits from sprite
        super().__init__(img, size=64, num_frames=2, x_pos=x_pos, y_pos=y_pos, scale=5)
        self.state = 1
        self.show = True
        self.name = ""
        self.font = pygame.font.SysFont("opensans", 49)
   
    def draw(self, screen):
        if self.show:
            super().draw(screen)
            text = self.font.render(self.name, True, (255, 255, 235))
            # measures from middle bottom of text to displace from sprite
            text_rect = text.get_rect(midbottom=(self.rect.centerx, self.rect.y + 50)) # fix sprites later
            screen.blit(text, text_rect)





