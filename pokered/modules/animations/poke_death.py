import pygame
from ..utils.animated import Animated
from ..utils.soundManager import SoundManager

class PokeDeath(Animated):
    def __init__(self, poke):
        """Creates a simple pokemon death animation. Extends animation solely so that its type 
        can be checked in the battle fsm. It overwrites all of Animated's functionality."""
        self._animationTimer = 0
        self._framesPerSecond = 80
        self._poke = poke
        self._count = 0
        SoundManager.getInstance().playSound("firered_0010.wav")
    
    def update(self, ticks):
        # Simply lower the position of the pokemon's sprite 
        self._animationTimer += ticks
        if self._animationTimer > 1 / self._framesPerSecond:
            self._count += 2
            self._animationTimer -= 1 /self._framesPerSecond
            self._poke._image = self._poke._image.subsurface(pygame.Rect(0,0, self._poke._image.get_width(), self._poke._image.get_height() - 2))
            self._poke._position.y += 2
        
        # After the pokemon has been lowered all the way make sure to returns its position back to where it started
        if self._count == 64:
            self._poke._position.y -= 64

    def draw(self, draw_surface):
        """Since this animation just moves the position of the pokemon it does not need to do anything in draw"""
        pass

    def is_dead(self):
        """Returns whether or not the animation has been completed."""
        return self._count > 63