class Hit():
    def __init__(self, pokemon):
        """This is the animation that plays when a pokemon is hit by a move.
        It blinks repeatedly a few times and then the animation is over"""
        self._pokemon = pokemon
        self._animation_timer = 0
        self._blink_num = 0
        self._fps = 9
        self._is_dead = False

    def draw(self, draw_surface):
        """Since this animation simply toggles the pokemon's image on/off it does not
        need to do anything in the draw method."""
        return

    def is_dead(self):
        """Returns whether or not the animation is dead"""
        return self._is_dead

    def update(self, ticks):
        """Updates the animation. Toggles the pokemon's image 9
        times a second."""
        self._animation_timer += ticks
        if self._animation_timer > 1 / self._fps:
            self._animation_timer -= 1 / self._fps
            if self._blink_num < 8:
                self._blink_num += 1
                self._pokemon.can_draw = not self._pokemon.can_draw
            else:
                self._is_dead = True
