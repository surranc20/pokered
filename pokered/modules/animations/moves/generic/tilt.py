import pygame
from ....utils.vector2D import Vector2

class Tilt():
    def __init__(self, pokemon):
        """This animation tilts the pokemon to the right. Also contains a method capable of undoing the tilt."""
        self._pokemon = pokemon 
    
    def draw(self, draw_surface):
        """Since this animation simply tilts the pokemon it does not need to do anything 
        in the draw function."""
        pass

    def is_dead(self):
        """Returns whether or not the animation is over."""
        return self._is_dead 
    
    def update(self, ticks):
        """Tilts the pokemon."""
        if not self.is_dead():
            pygame.transform.rotate(self._pokemon._image, 315)
    
    
        