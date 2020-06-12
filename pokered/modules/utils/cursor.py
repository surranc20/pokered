from os.path import join
from .UI.drawable import Drawable
from .managers.soundManager import SoundManager
from ..enumerated.battle_actions import BattleActions


class Cursor(Drawable):
    """Small Cursor class that keeps track of the menu cursor."""
    def __init__(self, max_value, initial_pos=(178, 20), line_height=11):
        """Initialize the cursor. Max_value is the highest possible value the
        cursor can have based on the size of the menu."""
        self._max_value = max_value
        self._initial_pos = initial_pos
        self._line_height = line_height
        self.cursor = 0
        super().__init__(join("battle", "cursor.png"), initial_pos,
                         world_bound=False)

    def reset(self):
        """Resets the cursor to its initial position."""
        self.cursor = 0
        self._position = self._initial_pos

    def draw(self, draw_surface):
        """Draws the cursor"""
        super().draw(draw_surface)

    def change_cursor_pos(self, action):
        """Changes the cursor pos based on the action provided"""
        if action.key == BattleActions.UP.value:
            if self.cursor > 0:
                self.cursor -= 1
                SoundManager.getInstance().playSound("firered_0005.wav")

        elif action.key == BattleActions.DOWN.value:
            if self.cursor < self._max_value - 1:
                self.cursor += 1
                SoundManager.getInstance().playSound("firered_0005.wav")

        self._position = (178, 20 + self.cursor * 11)
        self._position = (self._initial_pos[0],
                          self._initial_pos[1] +
                          self.cursor * self._line_height)
