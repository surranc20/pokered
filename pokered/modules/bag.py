from .item import Item
from .enumerated.item_types import ItemTypes


class Bag():
    def __init__(self):
        self.bag = {
            ItemTypes.ITEMS: {},
            ItemTypes.POKE_BALLS: {},
            ItemTypes.KEY_ITEMS: {}
        }
        self.add_item(Item("Great Ball"), 10)
        self.add_item(Item("Pokeball"), 10)
        self.add_item(Item("Ultra Ball"), 10)
        self.add_item(Item("Master Ball"), 10)
        self.add_item(Item("Dive Ball"), 10)
        self.add_item(Item("Luxury Ball"), 10)
        self.add_item(Item("Potion"), 99)
        self.add_item(Item("Bike"))

    def __getitem__(self, bag_type):
        return self.bag[bag_type]

    def add_item(self, item, num=1):
        """Adds a given number of an item to the bag."""
        if self.bag[item.type].get(item) is None:
            self.bag[item.type][item] = num
        else:
            self.bag[item.type][item] += num

    def subtract_item(self, item, num=1):
        """Subtracts a given number of an item from the bag."""
        self.bag[item.type][item] -= num
        if self.bag[item.type][item] <= 0:
            self.bag[item.type].pop(item)
