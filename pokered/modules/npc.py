from os.path import join
from .utils.UI.mobile import Mobile
from .enumerated.cardinality import Cardinality


class NPC(Mobile):
    def __init__(self, name, position, facing, enemy=True):
        """Creates an npc instance (NOTE: Base class for all trainers,
        including yourself)"""
        if not enemy:
            super().__init__("trainer.png", position,
                             self._parse_cardinality(facing))
        else:
            super().__init__(join("trainers", name + ".png"), position,
                             self._parse_cardinality(facing))

        self.name = name.upper()
        self.is_enemy = enemy
        self.get_current_frame()

    def _parse_cardinality(self, card_string):
        if type(card_string) == Cardinality:
            return card_string
        elif card_string == "north":
            return Cardinality.NORTH
        elif card_string == "south":
            return Cardinality.SOUTH
        elif card_string == "east":
            return Cardinality.EAST
        else:
            return Cardinality.WEST

    def turn(self, direction):
        self._orientation = direction
        self._row = abs(self._orientation.value)
        self._flip = True if self._orientation == Cardinality.EAST else False
        self.get_current_frame()

    def determine_direction_to_tile(self, tile_pos):
        """Helper method to determine the cardinal direction to a tile."""
        if self.current_tile.pos == tile_pos:
            return self._orientation
        else:

            if tile_pos[0] > self.current_tile.pos[0]:
                direction = Cardinality.EAST
            elif tile_pos[0] < self.current_tile.pos[0]:
                direction = Cardinality.WEST
            elif tile_pos[1] > self.current_tile.pos[1]:
                direction = Cardinality.SOUTH
            else:
                direction = Cardinality.NORTH

            self._row = abs(direction.value)
            return direction