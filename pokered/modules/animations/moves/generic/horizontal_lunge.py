from ....utils.vector2D import Vector2

class HorizontalLunge():
    def __init__(self, pokemon, lunge_dist):
        self._pokemon = pokemon
        self._is_dead = False
        self._anchored_pos = Vector2(pokemon._position.x, pokemon._position.y)
        self._lung_dist = lunge_dist

    def draw(self, draw_surface):
        pass

    def is_dead(self):
        return self._is_dead
    
    def update(self, ticks):
        if not self.is_dead():
            if self._lung_dist > 0:
                self._pokemon._position.x += 2
                self._lung_dist -= 1
            
            elif self._lung_dist < 0:
                self._pokemon._position.x -= 2
                self._lung_dist += 1

            if self._lung_dist == 0:
                self._is_dead = True

        