import pygame

class StartScreen():
    def __init__(self):
        self.font = pygame.font.SysFont("opensans", 49)
        self.start = True
        self.name_submitted = False
        self.shop_name = ""
        self.text = None

    def start_new_game(self, player, current_time):
        keys = pygame.key.get_pressed()

        if not self.name_submitted:
            self.shop_name += player.get_shop_name()

        if (current_time // 500) % 2 == 0:
            cursor = "_"
        else:
            cursor = ""

        self.text = self.font.render(f"Enter shop name: {self.shop_name}{cursor}")


        