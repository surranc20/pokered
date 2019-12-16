from ....utils.vector2D import Vector2


class HorizontalJiggle():
    def __init__(self, pokemon, timer=None):
        """This animation jiggles a pokemon back and forth.
        If no timer is provided it will do so indefinitly."""
        self._pokemon = pokemon
        self._timer = 0
        self._current_delta = 1
        self._fps = 20
        self._is_dead = False
        self._anchored_pos = Vector2(pokemon._position.x, pokemon._position.y)
        self._total_timer = timer

    def draw(self, draw_surface):
        """Since this animation simply moves the pokemon it does not
        need to do anything in the draw function."""
        pass

    def is_dead(self):
        """Returns whether or not the animation is over."""
        return self._is_dead

    def reset(self):
        """Resets the pokemons position to what it was before the animation started and
        then ends the animation."""
        self._pokemon._position = self._anchored_pos
        self._is_dead = True

    def update(self, ticks):
        """Jiggles the pokemon based on the animation timer."""
        if not self.is_dead():

            # If the move is on a timer check to see if the timer is over
            if self._total_timer is not None:
                self._total_timer -= ticks
                if self._total_timer < 0:
                    self.reset()
                    return True

            # Jiggle the pokemon based on where it is relative to
            # anchor point (its start point)
            if self._pokemon._position[0] == self._anchored_pos.x:
                self._current_delta = 2
            elif self._pokemon._position[0] - self._anchored_pos[0] <= 4:
                self._current_delta = -2

            # Update the pokemon's position if enough time has passed
            self._timer += ticks
            if self._timer > 1 / self._fps:
                self._timer -= 1 / self._fps
                self._pokemon._position =  \
                    Vector2(self._pokemon._position[0] + self._current_delta,
                            self._pokemon._position[1])
