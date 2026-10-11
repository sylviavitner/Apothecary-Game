from item_slot import ItemSlot
import pygame

class Inventory():
    def __init__(self, slot_img):
        self.capacity = 30
        self.taken_slots = 0
        self.slots = []
        self.extend = False
        self.columns = 5
        self.hotbar_slots = 5
        self.scale = 3
        self.slot_size = 32 * self.scale
        self.gap = 32
        self.margin = 32

        for _ in range(self.capacity):
            self.slots.append(ItemSlot(slot_img, scale=self.scale))

    def add(self, item, amount=1):
        # adding to preexisting item stack
        for slot in self.slots:
            if slot.item == item:
                add_amount = amount
                if add_amount > item.stack_size - slot.quantity:
                    add_amount = item.stack_size - slot.quantity
                slot.quantity += add_amount
                amount -= add_amount
                if amount <= 0:
                    return

        # go to next available slot
        for slot in self.slots:
            if slot.item == None:
                slot.item = item
                if item.stack_size < amount:
                    slot.quantity = item.stack_size
                    return self.add(item, amount - item.stack_size)
                else:
                    slot.quantity = amount
                    return
                
    def remove(self, item, amount=1):
        pass

    # when i is pressed, toggle inventory on/off
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
            self.extend = not self.extend

    # draw each 32x32 item 
    def draw(self, screen):
        screen_w, screen_h = screen.get_size()
        dx = self.slot_size + self.gap
        inv_w = (self.slot_size + self.gap) * self.columns
        start_x = (screen_w // 2) - (inv_w // 2)
        
        if self.extend:
            # draw full extended inventory on screen, moving the 5 hotbar slots to the top followed by 25 slots (6x5 grid)
            rows = self.capacity // self.columns
            total_h = rows * self.slot_size + (rows - 1) * self.gap
            start_y = (screen_h - total_h) // 2

            i = 0
            for row in range(rows):
                for col in range(self.columns):
                    slot = self.slots[i]
                    slot.rect.x = start_x + col * dx
                    slot.rect.y = start_y + row * dx
                    slot.draw(screen)
                    i += 1
        else:
            y = screen_h - self.slot_size - self.margin
            for i in range(self.hotbar_slots):
                slot = self.slots[i]
                slot.rect.x = start_x + i * dx
                slot.rect.y = y
                slot.draw(screen)
            # draw first 5 slots (hotbar) on bottom center of the screen

        