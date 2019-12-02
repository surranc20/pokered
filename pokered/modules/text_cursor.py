from .utils.drawable import Drawable

class TextCursor(Drawable):
    def __init__(self, pos):
        super().__init__("text_cursor.png", pos)
        self._is_active = False
        self._current_delta = 1
        self._timer = 0
    
    def activate(self):
        self._is_active = True
    
    def deactivate(self):
        self._is_active = False
    
    def set_pos(self, pos):
        pos = (pos[0] + 10, pos[1] + 100)
        self._position = pos
        self._anchored_pos = pos
    
    def draw(self, draw_surface):
        if self._is_active:
            super().draw(draw_surface)

    def update(self, ticks):
        if self._position == self._anchored_pos:
            self._current_delta = 1
        elif self._position[1] - self._anchored_pos[1] >= 2:
            self._current_delta = -1

        self._timer += ticks
        if self._timer > .2:
            self._position = (self._position[0], self._position[1] + self._current_delta)
            self._timer -= .2