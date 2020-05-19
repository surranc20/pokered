from .npc import NPC
from .events.nurse_heal import NurseHeal


class Nurse(NPC):
    def __init__(self, position, facing):
        """Creates a nurse object"""
        super().__init__("nurse", position, facing)
        self.gender = "female"

    def update(self, ticks, nearby_tiles, current_tile):
        pass

    def talk_event(self, player):
        """Returns the nurse "talk event" which heals the player's pokemon"""
        return NurseHeal(self, player)
