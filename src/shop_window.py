import pygame
from item import ItemStand, EmptyFlask, Cauldron
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
        ts = ItemStand()
        size, scale = ts.size, ts.scale
        ts.kill()
        item_stand = ItemStand(x=(self.rect.centerx - (size*scale)) - 200, y=self.rect.y + 50)
        empty_flask = EmptyFlask(x=(self.rect.centerx - (size*scale)), y=item_stand.rect.y)
        cauldron = Cauldron(x=(self.rect.centerx - (size*scale)) + 200, y=item_stand.rect.y)
        return pygame.sprite.Group(item_stand, empty_flask, cauldron) # for now just 1 item

    def get_buttons(self):
        buttons = pygame.sprite.Group()
        for i, item in enumerate(self.items):
            b = Button(img="assets/shop_window_buttons.png", x_pos=item.rect.x - (item.size // 2), y_pos=item.rect.y + (item.size*item.scale), type=item.name, frame=i, scale=2)
            buttons.add(b)
        return buttons

    def draw(self, screen, player):
        self.rect.center = screen.get_rect().center # reset in case resized
        if self.show and player.inside_shop:
            screen.blit(self.image, (self.rect.x, self.rect.y))
            for item in self.items:
                item.show = True
                item.draw(screen)
            for button in self.buttons:
                button.show = True
                button.draw(screen)
        else:
            for item in self.items:
                item.show = False
            for button in self.buttons:
                button.show = False

