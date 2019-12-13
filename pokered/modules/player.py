import pygame
from .trainer import Trainer
from .utils.mobile import Mobile
from .utils.soundManager import SoundManager
from .enumerated.cardinality import Cardinality
from .enumerated.battle_actions import BattleActions

class Player(Trainer):
    def __init__(self, position, name, enemy=False):
        """Creates an instance of a player. Requires the player's start position, and name."""
        super().__init__(position, name, Cardinality.NORTH, enemy=False)
        self._nFrames = 4
        self._last_wall_bump = 0
        self._current_tile = 0
        self._move_script_active = None
        self._hidden_inventory = []
        
    
    def handle_event(self, event, nearby_tiles):
        """Handles the events from the level manager. Is capable of taking control away from the player if a movement scipt is active."""
        if self._move_script_active == None:
            if (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_b]:
                self.move(event)
            elif event.type == pygame.KEYDOWN and event.key == BattleActions.SELECT.value:
                if nearby_tiles[self._orientation]._obj != None:
                    return nearby_tiles[self._orientation]._obj.talk_event(self)
        else:
            pass
    
    def move_forward_to_tile(self, tile):
        """Allows the implementation of movement scripting. The player will move until they reach the tile provided."""
        self._move_script_active = tile
        return self._current_tile._pos == tile
    
    def _move_forward_to_tile(self, tile):
        """Helper function that implements the above functionality. Helps determine whether or not the script is over."""
        if self._current_tile._pos != tile:
            self._orientation = Cardinality.NORTH
            self._moving = True
            return False
        else:
            self._moving = False
            self._move_script_active = None
            return True

    def move(self, event):
        """Updates the players moving, flip, and orientation values based on the event"""
        # If wasd have been presed then set the correct cardinality and set moving to be true.
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
        
        # When b is pressed the player is running which doubles movement speed (not actually implemented)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            self.start_running()
        
        # If no more wasd keys are held down then the player stops moving
        if event.type == pygame.KEYUP and event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
            if (event.key == pygame.K_w and self._orientation == Cardinality.NORTH) or (event.key == pygame.K_s and self._orientation == Cardinality.SOUTH) or (event.key == pygame.K_d and self._orientation == self._orientation.EAST) or (event.key == pygame.K_a and self._orientation == Cardinality.WEST):
                
                # Make sure that no other wasd key is pressed. If one is, then start moving in that direction
                still_pressed = [x for x in pygame.key.get_pressed() if x in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]]
                if still_pressed != []:
                    return self.move(pygame.event.Event(pygame.KEYDOWN, {key : still_pressed[0]}))
                else:
                    self._moving = False
                    self._key_down_timer = 0
        
        if event.type == pygame.KEYUP and event.key == pygame.K_b:
            self.stop_running()
        
        # ABS is used because EAST and WEST should both point to row 2 but need to have distint values.
        # Because of this WEST = -2 and to get to the correct row we simply take the absolute value.
        self._row = abs(self._orientation.value)
        

    def update(self, ticks, nearby_tiles, current_tile):
        """Updates the player class's position"""
        self._current_tile = current_tile
        print(self._current_tile._pos)
        if self._move_script_active != None:
            self._move_forward_to_tile(self._move_script_active)
        if self._moving:
            self.startAnimation()
            self._key_down_timer += ticks
            self._last_wall_bump += ticks

            # If the player is not in the middle of crossing a tile then start a walk event.
            if self._walk_event == None:
                if self._current_image_row != self._row:
                    self.get_current_frame()
                if nearby_tiles[self._orientation].is_clear():
                    if self._key_down_timer > .2:
                        self._walk_event = [0, self._orientation]    
                else: 
                    if self._last_wall_bump > .7:
                        SoundManager.getInstance().playSound("firered_0007.wav", sound=1)
                        self._last_wall_bump = self._last_wall_bump - .7
                    
        # This ensures the player travels a full tile once they have begun moving.
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
        
        # Stop the player from animating if no button is pressed and not in the middle of a walk event.
        if not self._moving and self._walk_event == None:
            self._key_down_timer = 0
            self._walk_event = None
            self._frame = 0
            self._last_wall_bump = 0
            self.stopAnimation()
    
    def start_running(self):
        """Player starts running."""
        self._running = True
        self._framesPerSecond = 8
    
    def stop_running(self):
        """Player stops running."""
        self._runnign = False
        self._framesPerSecond = 4
    
    