from os.path import join
from .npc import NPC


class Nurse(NPC):
    def __init__(self, position, facing):
        """Creates a nurse object"""
        super().__init__(join("trainers", "nurse.png"), position, facing)

    def update(self, ticks, nearby_tiles, current_tile):
        pass
