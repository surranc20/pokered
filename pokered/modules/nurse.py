from .npc import NPC


class Nurse(NPC):
    def __init__(self, position, facing):
        """Creates a nurse object"""
        super().__init__("nurse", position, facing)

    def update(self, ticks, nearby_tiles, current_tile):
        pass
