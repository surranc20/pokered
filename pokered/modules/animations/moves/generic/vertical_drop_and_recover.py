from ....utils.vector2D import Vector2

class VerticalDropAndRecovery():
    def __init__(self, pokemon, drop_dist):
        self._pokemon = pokemon
        self._fps = 5
        self._timer = 1.001 / self._fps
        self._drop_dist = drop_dist
        self._is_dead = False
        self._anchored_po = Vector2(pokemon._position.x, pokemon._position.y)
        self._current_dir = "stationary"
    
    def draw(self, draw_surface):
        pass

    def is_dead(self):
        return self._is_dead

    def reset(self):
        self._pokemon._position = self._anchored_pos
        self._is_dead = True
    
    def update(self, ticks):
        if not self.is_dead():
            self._timer += ticks
            
            if self._timer > 1 / self._fps:
                self._timer -= 1 / self._fps
                if self._current_dir == "stationary":
                    self._current_dir = "down"
                    self._pokemon._position.y += self._drop_dist
                elif self._current_dir == "down":
                    self._current_dir = "done"
                    self._pokemon._position.y -= self._drop_dist
                elif self._current_dir == "done":
                    self._is_dead = True
            