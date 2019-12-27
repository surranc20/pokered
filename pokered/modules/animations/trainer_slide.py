class TrainerSlide():
    def __init__(self, trainer, dx=20):
        """Takes in a trainer drawable object and will move the sprite in the
        direction given in the dx parameter. dx must be even"""
        self._trainer = trainer
        self._dx = dx
        self._timer = 0
        self._moves_per_second = 60
        self._is_dead = False

        if dx % 2 != 0:
            raise Exception("DX value must be even")

    def draw(self, draw_surface):
        """Draws the trainer image."""
        self._trainer.draw(draw_surface)

    def update(self, ticks):
        """Moves the trainer to the left or right based on the +/- value of
        dx."""
        self._timer += ticks
        if self._timer > 1 / self._moves_per_second:
            self._timer -= 1 / self._moves_per_second
            if self._dx > 0:
                self._trainer._position.x += 2
                self._dx -= 2
            elif self._dx < 0:
                self._trainer._position.x -= 2
                self._dx += 2
            else:
                self._is_dead = True

    def is_dead(self):
        """Returns whether or not the animation is over."""
        return self._is_dead
