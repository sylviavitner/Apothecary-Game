from item import Item

class Furniture(Item):
    def __init__(self, img, name, sz, scale, x, y):
        super().__init__(img, name, stack_size = 100, inside_inventory=False, size=sz)
        self.stack_size = 1
        self.scale = scale
        self.rect.x = x
        self.rect.y = y

class Item_Stand(Furniture):
    def __init__(self, img, name, size, x_pos, y_pos):
        super().__init__(img, name, size, sz=32, x=x_pos, y=y_pos)
