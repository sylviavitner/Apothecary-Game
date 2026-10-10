from item_slot import ItemSlot

class Inventory():
    def __init__(self):
        self.capacity = 30
        self.taken_slots = 0
        self.slots = []
        for _ in range(self.capacity):
            self.slots.append(ItemSlot())

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

        