import pygame
from .trainer import Trainer
from .utils.mobile import Mobile
from .utils.soundManager import SoundManager
from .enumerated.cardinality import Cardinality

class Player(Trainer):
    def __init__(self, position, name, enemy=False):
        super().__init__(position, name, Cardinality.NORTH, enemy=False)
        self._nFrames = 4
        self._last_wall_bump = 0
        
    
    def handle_event(self, event):
        if (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_b]:
            self.move(event)

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
            self._key_down_timer = 0
        
        if event.type == pygame.KEYUP and event.key == pygame.K_b:
            self.stop_running()
        
        # ABS is used because EAST and WEST should both point to row 2 but need to have distint values
        # Because of this WEST = -2 and to get to the correct row we simply take the absolute value 
        self._row = abs(self._orientation.value)
        

    def update(self, ticks, nearby_tiles, current_tile):
        """Updates the player class"""
        #print(nearby_tiles)
        if self._moving:
            self.startAnimation()
            self._key_down_timer += ticks
            self._last_wall_bump += ticks
            if self._walk_event == None:
                if self._current_image_row != self._row:
                    self.get_current_frame()
                if nearby_tiles[self._orientation].is_clear():
                    if self._key_down_timer > .1:
                        self._walk_event = [0, self._orientation]    
                else: 
                    if self._last_wall_bump > .7:
                        SoundManager.getInstance().playSound("firered_0007.wav", sound=1)
                        self._last_wall_bump = self._last_wall_bump - .7
                    

        if self._walk_event != None:
            Mobile.update(self, ticks)
            self._wait_till_next_update += ticks
            self._walk_event[0] += 1

            if self._walk_event[1] == Cardinality.WEST:
                self._position.x -= 1
            elif self._walk_event[1] == Cardinality.SOUTH:
                self._position.y += 1
            elif self._walk_event[1] == Cardinality.NORTH:
                self._position.y -= 1
            elif self._walk_event[1] == Cardinality.EAST:
                self._position.x += 1
            if self._walk_event[0] == 16: 
                nearby_tiles[self._walk_event[1]].add_obj(self)
                current_tile.remove_obj()
                self._walk_event = None
                    
        if not self._moving and self._walk_event == None:
            self._key_down_timer = 0
            self._walk_event = None
            self._frame = 0
            self._last_wall_bump = 0
            self.stopAnimation()
    
    def start_running(self):
        """"""
        self._running = True
        self._framesPerSecond = 8
    
    def stop_running(self):
        """"""
        self._runnign = False
        self._framesPerSecond = 4
    
    