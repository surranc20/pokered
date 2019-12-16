from ....utils.vector2D import Vector2


class VerticalDropAndRecovery():
    def __init__(self, pokemon, drop_dist):
        """The pokemons dip down by the distance specefied in drop_dist and
        then quickly rebounds up."""
        self._pokemon = pokemon
        self._fps = 5

        # Start the timer with just enough initial value that the first frame
        # updates immediately
        self._timer = 1.001 / self._fps
        self._drop_dist = drop_dist
        self._is_dead = False
        self._anchored_pos = Vector2(pokemon._position.x, pokemon._position.y)

        # This variable keeps track of the direction the sprite is moving
        self._current_dir = "stationary"

    def draw(self, draw_surface):
        """Since this animation only changes the position of the pokemon it
        does not need to do anything in the draw method"""
        pass

    def is_dead(self):
        """Determines whether or not the animation has finished"""
        return self._is_dead

    def reset(self):
        """Safety feature. Ensures the pokemon is back in its original
        position and then ends animation."""
        self._pokemon._position = self._anchored_pos
        self._is_dead = True

    def update(self, ticks):
        """Update the position of the pokemon sprite."""
        if not self.is_dead():
            self._timer += ticks

            if self._timer > 1 / self._fps:
                self._timer -= 1 / self._fps

                # If the pokemon has not moved yet move down by the drop
                # distance
                if self._current_dir == "stationary":
                    self._current_dir = "down"
                    self._pokemon._position.y += self._drop_dist

                # If the pokemon moved down last then move up
                elif self._current_dir == "down":
                    self._current_dir = "done"
                    self._pokemon._position.y -= self._drop_dist

                # If the pokemon has moved up and down then end the animation
                elif self._current_dir == "done":
                    self.reset()
