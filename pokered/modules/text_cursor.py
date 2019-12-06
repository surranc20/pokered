from .utils.drawable import Drawable

class TextCursor(Drawable):
    def __init__(self, pos):
        """A simple text cursor object that bobs up and down while waiting for the user to press enter."""
        super().__init__("text_cursor.png", pos)
        self._is_active = False
        self._current_delta = 1
        self._timer = 0
        self._world_bound = False
    
    def activate(self):
        """Activates the cursor so that it can be drawn."""
        self._is_active = True
    
    def deactivate(self):
        """Deactivates the cursor so that if will not be drawn."""
        self._is_active = False
    
    def set_pos(self, pos):
        """Sets the position of the cursor. The parameter expects the position passed in to be the cursors position in the text box."""
        pos = (pos[0] + 10, pos[1] + 100)
        self._position = pos
        self._anchored_pos = pos
    
    def draw(self, draw_surface):
        """Draws the cursor."""
        if self._is_active:
            super().draw(draw_surface)

    def update(self, ticks):
        """Updates the cursor so that it can bob up and down."""
        if self._position == self._anchored_pos:
            self._current_delta = 1
        elif self._position[1] - self._anchored_pos[1] >= 2:
            self._current_delta = -1

        self._timer += ticks
        if self._timer > .2:
            self._position = (self._position[0], self._position[1] + self._current_delta)
            self._timer -= .2