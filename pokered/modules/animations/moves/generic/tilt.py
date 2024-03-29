import pygame


class Tilt():
    def __init__(self, pokemon, degrees):
        """This animation tilts the pokemon to the right.
        Also contains a method capable of undoing the tilt."""
        self._pokemon = pokemon
        self._degrees

    def draw(self, draw_surface):
        """Since this animation simply tilts the pokemon it does not
         need to do anything in the draw function."""
        pass

    def is_dead(self):
        """Returns whether or not the animation is over."""
        return self._is_dead

    def update(self, ticks):
        """Tilts the pokemon."""
        if not self.is_dead():
            pygame.transform.rotate(self._pokemon._image, self._degrees)

    def reset_tilt(self):
        """Resets the pokemon back to their original position."""
        pygame.transform.rotate(self._pokemon._image, 360 - self._degrees)
