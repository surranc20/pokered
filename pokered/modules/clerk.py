from .npc import NPC
from .events.poke_mart_event import PokeMartEvent


class Clerk(NPC):
    def __init__(self, position, facing, inventory):
        """Creates a clerk object"""
        super().__init__("clerk", position, facing)
        self.gender = "male"
        self.inventory = inventory

    def update(self, ticks, nerby_tiles, current_tile):
        pass

    def talk_event(self, player):
        return PokeMartEvent(self, player)
