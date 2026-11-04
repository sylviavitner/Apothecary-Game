import pygame
from sprite import Sprite

class Item(Sprite):
    def __init__(self, img, name, stack_size=100, inside_inventory=True, size=32):
        super().__init__(img, size, num_frames=2, x_pos=0, y_pos=0, scale=3)
        self.name = name # red_berry, seed, purple_berry, item_stand
        self.stack_size = stack_size
        self.inside_inventory = inside_inventory
        self.slot_index = -1 # -1 for not in inventory, 0-29  for slots
        self.allow_click_to_move = False
        self.allow_pickup = False
        #self.for_sale = False

    def make_copy(self):
        match self.name:
            case "red_berry":
                return RedBerry()
            case "seed":
                return Seed()
            case "purple_berry":
                return PurpleBerry()
            case "item_stand":
                if self.inside_inventory:
                    return ItemStand(inside_inventory=True)
                return ItemStand(inside_inventory=False)

    # creates a new instance of the item and adds the amount to inventory
    def add_to_inventory(self, inventory, amount=1):
        item = self.make_copy()
        inventory.add(item, amount)
        return item

    # set x and y coords of item
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    # for clicking items and moving them (in or out of inventory/map)
    def handle_event(self, event, inventory, sprites, growables, all_items):

        # for getting input for item stand price and quantity
        if event.type == pygame.KEYDOWN:
            if self.name != "item_stand":
                return sprites
            else:
                self.handle_text_input(event, inventory)

        if event.type != pygame.MOUSEBUTTONDOWN:
            return sprites

        # left click
        elif event.button == 1:

            # moving an item inside inventory
            if self.inside_inventory:
                # toggle allow click to move and interaction frame
                if self.rect.collidepoint(event.pos):
                    if not self.allow_click_to_move:
                        self.allow_click_to_move = True
                        self.set_frame(1)
                    else:
                        self.allow_click_to_move = False
                        self.set_frame(0)

                # if an item is clicked
                elif self.allow_click_to_move:
                    for item in all_items:
                        if item.rect.collidepoint(event.pos) and item.inside_inventory:
                            self.allow_click_to_move = False
                            self.set_frame(0)
                            return sprites
                            # will need to swap items in inventory

                    # Placing items from inventory onto map (or shop)
                    new_item = self.make_copy()
                    new_item.inside_inventory = False
                    new_item.time_placed = pygame.time.get_ticks()
                    new_item.set_position(event.pos[0] - self.size, event.pos[1] - self.size)
                    sprites.add(new_item)
                    all_items.add(new_item)
                    inventory.remove(self, 1)

                    if new_item.name == "seed":
                        growables.add(new_item)
                    
                    self.allow_click_to_move = False
                    self.set_frame(0) # set back to original frame

        return sprites

# red berry
class RedBerry(Item):
    def __init__(self):
        super().__init__("assets/red_berry.png", "red_berry")
        self.market_price = 10

import bush

# seed
class Seed(Item):

    def __init__(self):
        super().__init__("assets/seed.png", "seed")
        self.cooldown = 3000
        self.market_price = 15

    def grow_bush(self, current_time):
        if not self.inside_inventory and current_time - self.time_placed >= self.cooldown:
            b = bush.Bush("assets/bush.png", self.rect.x - self.size, self.rect.y - self.size)
            b.last_harvested = current_time
            b.has_berries = False
            b.can_harvest = False
            b.set_frame(0)
            return b
        return None


# purple berry
class PurpleBerry(Item):
    def __init__(self):
        super().__init__("assets/purple_berry.png", "purple_berry")
        self.market_price = 25

# item stand
class ItemStand(Item):
    def __init__(self, size=32, x=0, y=0, inside_inventory=False):
        super().__init__("assets/item_stand.png", "item_stand", stack_size=1, inside_inventory=inside_inventory, size=size)
        self.stack_size = 1
        self.rect.x = x
        self.rect.y = y
        self.market_price = 50 # shop price and reccomended selling price
        self.name = "item_stand"
        self.item = None
        self.quantity = 0
        self.price_per_unit = 0
        self.font = pygame.font.SysFont("opensans", 20)
        self.prompt_active = False
        self.price_input_active = False
        self.quantity_input_active = False

    def handle_text_input(self, event, inventory):
        if not self.prompt_active:
            return

        # cast to string for input handling
        self.price_per_unit = str(self.price_per_unit)
        self.quantity = str(self.quantity)

        if event.key == pygame.K_BACKSPACE:
            if self.price_input_active:
                self.price_per_unit = self.price_per_unit[:-1]
            elif self.quantity_input_active:
                self.quantity = self.quantity[:-1]
        elif event.key == pygame.K_RETURN:
            if self.price_input_active:
                self.price_input_active = False
                if not self.price_per_unit:
                    self.price_per_unit = 0
                self.price_per_unit = int(self.price_per_unit) # back to int
                self.quantity_input_active = True
            elif self.quantity_input_active:
                self.quantity_input_active = False
                if not self.quantity:
                    self.quantity = 1
                self.quantity = int(self.quantity) # back to int
                if self.quantity > inventory.get_item_quantity(self.item.name) + 1 or self.quantity <= 0:
                    self.quantity = 1
                else:
                    inventory.remove_item_by_name(self.item.name, amount=self.quantity - 1) # already removed 1
                self.prompt_active = False
        elif event.unicode.isdigit():
            if self.price_input_active:
                self.price_per_unit += event.unicode
            elif self.quantity_input_active:
                self.quantity += event.unicode

    def prompt_user(self):
        self.prompt_active = True
        self.price_input_active = True

    def add_item(self, to_add, quantity=1):
        if to_add:
            item = to_add.make_copy()
            item.inside_inventory = False
            item.for_sale = True
            item.allow_pickup = False
            item.set_position(self.rect.x, self.rect.y - (item.size * item.scale // 2))
            self.item = item
            self.quantity += quantity
            return self.item

    def remove_item(self):
        pass

    def draw(self, screen):
        if self.show:
            screen.blit(self.image, (self.rect.x, self.rect.y))
            if self.item:
                current_time = pygame.time.get_ticks()
                cursor = "_" if (current_time // 500) % 2 == 0 else ""
                if self.price_input_active:
                    ppu_string = f"{self.price_per_unit}{cursor}"
                    q_string = f"{self.quantity}"
                elif self.quantity_input_active:
                    ppu_string = f"{self.price_per_unit}"
                    q_string = f"{self.quantity}{cursor}"
                else:
                    ppu_string = f"{self.price_per_unit}"
                    q_string = f"{self.quantity}"
                quantity_text = self.font.render(f"Quantity: {q_string}", True, (255, 255, 235))
                price_text = self.font.render(f"Price: {ppu_string}", True, (255, 255, 235))
                text_x = self.rect.x
                text_y = self.rect.y - (self.size * self.scale)
                screen.blit(price_text, (text_x, text_y))
                screen.blit(quantity_text, (text_x, text_y + 25))

