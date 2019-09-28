from .mobile import Mobile
from .cardinality import Cardinality
import pygame

class Player(Mobile):
    def __init__(self, position):
        super().__init__("trainer.png", position, Cardinality.NORTH)
        self._nFrames = 4
        self._framesPerSecond = 4
        self._running = False
        self._moving = False

    def move(self, event):
        """Updates the players moving, flip, and orientation values based on the event"""
        # If wasd have been presed then set the correct cardinality and set moving to be true
        # The flip value is only true when the player is moving EAST. 
        # This allows us to flip the horizontal running animation.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w: 
            self._orientation = Cardinality.NORTH
            self._moving = True
            self._flip = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_a: 
            self._orientation = Cardinality.WEST
            self._moving = True
            self._flip = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_s: 
            self._orientation = Cardinality.SOUTH
            self._moving = True
            self._flip = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_d: 
            self._orientation = Cardinality.EAST
            self._moving = True
            self._flip = True
        
        # When b is pressed the player is runnign which doubles movement speed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            self.start_running()
        
        # If wasd have been lifted then the player is no longer moving
        if event.type == pygame.KEYUP and event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
            self._moving = False
        
        if event.type == pygame.KEYUP and event.key == pygame.K_b:
            self.stop_running()
        
        # ABS is used because EAST and WEST should both point to row 2 but need to have distint values
        # Because of this WEST = -2 and to get to the correct row we simply take the absolute value 
        self._row = abs(self._orientation.value)
        print(self._moving, self._orientation)

    def update(self, ticks):
        """Updates the player class"""
        if self._moving:
            self.startAnimation()
            super().update(ticks)
        else:
            self._frame = 0
            self.stopAnimation()
    
    def start_running(self):
        """"""
        self._running = True
        self._framesPerSecond = 8
    
    def stop_running(self):
        """"""
        self._runnign = False
        self._framesPerSecond = 4


        
        