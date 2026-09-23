import pygame

class StartScreen():
    def __init__(self):
        self.font = pygame.font.SysFont("opensans", 49)
        self.start = True
        self.name_submitted = False

    def draw(self, screen, player, current_time):
        # blinking cursor for input screen
        cursor = "_"
        text = self.font.render(f"Enter shop name: {player.shop_name}{cursor}", True, (255, 255, 235))
        rect = text.get_rect(center=screen.get_rect().center)
        screen.blit(text, rect)


        