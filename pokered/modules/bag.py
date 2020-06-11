from .enumerated.item_types import ItemTypes


class Bag():
    def __init__(self):
        self.bag = {
            ItemTypes.ITEMS: {},
            ItemTypes.POKE_BALLS: {},
            ItemTypes.KEY_ITEMS: {}
        }

    def add_item(self, item, num=1):
        """Adds a given number of an item to the bag."""
        if self.bag[item.type].get(item) is None:
            self.bag[ItemTypes.ITEMS] = num
        else:
            self.bag[item.type] += num
