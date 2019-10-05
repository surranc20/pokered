from os.path import join
import pygame
from ..frameManager import FRAMES
from ..animated import AnimatedGroupPart

class PokeEmerge(AnimatedGroupPart):
    def __init__(self, position, pokemon_name, anim_sequence_pos):
        super().__init__(join("pokemon", pokemon_name + "~.png"), position, anim_sequence_pos)
        self._frame = 1
        self._image = FRAMES.getFrame(self._imageName, (self._frame, self._row))
        self._image = pygame.transform.scale(self._image, (16, 16))
        self._nFrames = 2
        self._animate = True
        self._current_growth_number = 0
        self._framesPerSecond = 3
    
    def update(self, ticks):
        if self._animate:
            self._animationTimer += ticks

        if self._animationTimer > 1 / self._framesPerSecond:
            pass





    




    
        
        
