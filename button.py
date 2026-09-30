import pygame
from sprite import Sprite

class Button(Sprite):
    def __init__(self, img, x_pos=200, y_pos=600, type="exit", frame=0):
        super().__init__(img, size=64, num_frames=5, x_pos=x_pos, y_pos=y_pos, scale=3, frame=frame)
        self.images = pygame.image.load(img).convert_alpha()
        self.type = type

    def handle_event(self, event, player, background, shop):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        elif event.button == 1: # left mouse click
            if self.rect.collidepoint(event.pos):
                match self.type:
                    case "exit":
                        player.inside_shop = False
                        background.set_state(0)
                        shop.set_state(0)
                    case "open_close":
                        pass
                    case "edit":
                        pass
                    case "buy":
                        pass






        