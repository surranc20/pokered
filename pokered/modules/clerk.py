from .npc import NPC
from .item import Item
from .events.poke_mart_event import PokeMartEvent


class Clerk(NPC):
    def __init__(self, position, facing, inventory):
        """Creates a clerk object"""
        super().__init__("clerk", position, facing)
        self.gender = "male"
        self.inventory = inventory
        self._convert_inventory_to_items()

    def update(self, ticks, nerby_tiles, current_tile):
        pass

    def talk_event(self, player):
        return PokeMartEvent(self, player)

    def _convert_inventory_to_items(self):
        """Convert's the items in the inventory receieved in the constructor
        to actual item class"""
        self.inventory = {Item(item): price for (item, price) in
                          self.inventory.items()}
