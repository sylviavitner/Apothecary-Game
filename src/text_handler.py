import pygame

class TextHandler():
    def __init__(self):
        self.font = pygame.font.SysFont("opensans", 24)
        self.text = set() # list of strings currently to display
        self.offset = 30

    def update_text(self, sprite):
        if not sprite.frame == 1:
            return
        elif sprite.name in ["red_berry", "purple_berry", "seed", "red_potion", "purple_potion", "green_potion"]:
            self.text.add("Press [X] to pick up")
        elif sprite.name == "bush":
            self.text.add("Press [E] to harvest")
        elif sprite.name in ["item_stand", "cauldron"]:
            self.text.add("Press [E] to place item")
            self.text.add("Press [X] to pick up")

    def clear_text(self):
        self.text = set()

    def draw(self, inventory, screen):
        center_slot = inventory.slots[2]
        for i, text in enumerate(self.text):
            t = self.font.render(text, True, (255, 255, 235))
            rect = t.get_rect(midbottom=(center_slot.rect.centerx, center_slot.rect.y - self.offset * (i+1))) # center above 3rd inventory slot
            screen.blit(t, rect)


