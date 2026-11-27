import pygame

class TextHandler():
    def __init__(self):
        self.font = pygame.font.SysFont("opensans", 24)
        self.interactions_text = set() # list of strings currently to display
        self.offset = 30

    def update_text(self, sprite):
        if not sprite.frame == 1:
            return
        elif sprite.name in ["red_berry", "purple_berry", "seed", "red_potion", "purple_potion", "green_potion"]:
            self.interactions_text.add("Press [X] to pick up")
        elif sprite.name == "bush":
            self.interactions_text.add("Press [E] to harvest")
        elif sprite.name in ["item_stand", "cauldron"]:
            self.interactions_text.add("Press [E] to place item")
            self.interactions_text.add("Press [X] to pick up")

    def clear_text(self):
        self.interactions_text = set()

    def draw(self, inventory, screen):
        center_slot = inventory.slots[2]
        for i, text in enumerate(self.interactions_text):
            t = self.font.render(text, True, (255, 255, 235))
            rect = t.get_rect(midbottom=(center_slot.rect.centerx, center_slot.rect.y - self.offset * (i+1))) # center above 3rd inventory slot
            screen.blit(t, rect)


