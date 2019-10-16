from .mobile import Mobile
from .cardinality import Cardinality
import pygame

class Player(Mobile):
    def __init__(self, position, name, enemy=False):
        super().__init__("trainer.png", position, Cardinality.NORTH)
        self._nFrames = 4
        self._framesPerSecond = 4
        self._running = False
        self._moving = False
        self._pokemon_team = []
        self._active_pokemon = None
        self._is_enemy = enemy
        self._name = name

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
    
    def get_pokemon_team(self):
        return self._pokemon_team
    
    def is_enemy(self):
        return self._is_enemy

    def get_active_pokemon(self):
        return self._active_pokemon
    
    def set_active_pokemon(self, index):
        self._active_pokemon = self.get_pokemon_team()[index]

    def get_pokemon_by_index(self, index):
        print(self.get_pokemon_team()[index])
        return self.get_pokemon_team()[index]
    
    def get_name(self):
        return self._name
        