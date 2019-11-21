import pygame
from ..utils.animated import Animated
from ..utils.soundManager import SoundManager

class PokeDeath(Animated):
    def __init__(self, poke):
        self._animationTimer = 0
        self._framesPerSecond = 80
        self._poke = poke
        self._count = 0
        SoundManager.getInstance().playSound("firered_0010.wav")
    
    def update(self, ticks):
        self._animationTimer += ticks
        if self._animationTimer > 1 / self._framesPerSecond:
            self._count += 2
            self._animationTimer -= 1 /self._framesPerSecond
            self._poke._image = self._poke._image.subsurface(pygame.Rect(0,0, self._poke._image.get_width(), self._poke._image.get_height() - 2))
            self._poke._position.y += 2
        if self._count == 64:
            self._poke._position.y -= 64
    def draw(self, draw_surface):
        pass

    def is_dead(self):
        return self._count > 63