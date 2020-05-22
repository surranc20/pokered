from .npc import NPC


class Clerk(NPC):
    def __init__(self, position, facing, inventory):
        """Creates a clerk object"""
        super().__init__("clerk", position, facing)
        self.gender = "male"
        self.inventory = inventory

    def update(self, ticks, nerby_tiles, current_tile):
        print(self._orientation)

    def talk_event(self, player):
        return
