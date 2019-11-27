from ....utils.vector2D import Vector2

class HorizontalJiggle():
    def __init__(self, pokemon):
        self._pokemon = pokemon
        self._timer = 0
        self._current_delta = 1        
        self._fps = 20
        self._is_dead = False
        self._anchored_pos = Vector2(pokemon._position.x, pokemon._position.y)
        
    
    def draw(self, draw_surface):
        pass

    def is_dead(self):
        return self._is_dead
    
    def reset(self):
        self._pokemon._position = self._anchored_pos
        print("RESET                    ",self._pokemon._position)
        self._is_dead = True
    
    def update(self, ticks):
        if not self.is_dead():
            if self._pokemon._position[0] == self._anchored_pos.x:
                self._current_delta = 2
            elif self._pokemon._position[0] - self._anchored_pos[0] <= 4:
                self._current_delta = -2

            self._timer += ticks
            if self._timer > 1 / self._fps:
                self._timer -= 1 / self._fps
                self._pokemon._position = Vector2(self._pokemon._position[0] + self._current_delta, self._pokemon._position[1])
                