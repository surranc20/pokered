from ....utils.vector2D import Vector2

class HorizontalLunge():
    def __init__(self, pokemon, lunge_dist):
        """This animation lunges the pokemon by the init argument specefied
        in lunge_dist. If lunge_dist is negative the pokemon lunges left and 
        if it is positive it lunges right."""
        self._pokemon = pokemon
        self._is_dead = False
        self._anchored_pos = Vector2(pokemon._position.x, pokemon._position.y)
        self._lung_dist = lunge_dist

    def draw(self, draw_surface):
        """Since this animation only changes the position of the pokemon 
        the draw method does not need to do anything."""
        pass

    def is_dead(self):
        """Returns whether or not the animation is over"""
        return self._is_dead
    
    def update(self, ticks):
        """Changes the position of the pokemon 2 pixels at a time. 
        Stops when the total lunge distance has been reached."""
        if not self.is_dead():
            if self._lung_dist > 0:
                self._pokemon._position.x += 2
                self._lung_dist -= 1
            
            elif self._lung_dist < 0:
                self._pokemon._position.x -= 2
                self._lung_dist += 1

            if self._lung_dist == 0:
                self._is_dead = True

        