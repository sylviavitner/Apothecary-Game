import pygame
from item import ItemStand
from button import Button

class ShopWindow():
    def __init__(self, img, screen):
        self.size = 256
        self.scale = 3
        image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.scale(image, (self.size * self.scale, self.size * self.scale))
        self.rect = self.image.get_rect()
        self.rect.center = screen.get_rect().center
        self.rect.y = self.rect.y + 50
        self.show = False
        self.items = self.get_items()
        self.buttons = self.get_buttons()

    def get_items(self):
        item_stand = ItemStand(x=self.rect.x + 50, y=self.rect.y + 50)
        return pygame.sprite.Group(item_stand) # for now just 1 item

    def get_buttons(self):
        buttons = pygame.sprite.Group()
        for i, item in enumerate(self.items):
            b = Button("assets/shop_window_buttons.png", item.rect.centerx - 32, item.rect.y + (item.size*item.scale), item.name, i, scale=1)
            buttons.add(b)
        return buttons

    def draw(self, screen, player):
        if self.show and player.inside_shop:
            screen.blit(self.image, (self.rect.x, self.rect.y))
            for item in self.items:
                item.draw(screen)
            for button in self.buttons:
                button.draw(screen)

