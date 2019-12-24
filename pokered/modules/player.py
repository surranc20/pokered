import pygame
from .trainer import Trainer
from .utils.UI.mobile import Mobile
from .utils.managers.soundManager import SoundManager
from .enumerated.cardinality import Cardinality
from .enumerated.battle_actions import BattleActions


class Player(Trainer):
    def __init__(self, position, name, enemy=False):
        """Creates an instance of a player. Requires the player's start
        position, and name."""
        super().__init__(position, name, Cardinality.NORTH, enemy=False)
        self._nFrames = 4
        self._hidden_inventory = []

    def handle_event(self, event, nearby_tiles):
        """Handles the events from the level manager. Is capable of taking
        control away from the player if a movement scipt is active."""
        if self._move_script_active is None:
            if (event.type == pygame.KEYDOWN or
                    event.type == pygame.KEYUP) and \
                    event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_b]:
                self.move(event)
            elif event.type == pygame.KEYDOWN and event.key == BattleActions.SELECT.value:
                if nearby_tiles[self._orientation]._obj is not None and \
                        nearby_tiles[self._orientation]._obj is not self:
                    return nearby_tiles[self._orientation]._obj.talk_event(self)
        else:
            return

    def move(self, event):
        """Updates the players moving, flip, and orientation values based on
        the event"""
        # If wasd have been presed then set the correct cardinality and set
        # moving to be true. The flip value is only true when the player is
        # moving EAST. This allows us to flip the horizontal running animation.
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

        # When b is pressed the player is running which doubles movement speed
        # (not actually implemented)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            self.start_running()

        # If no more wasd keys are held down then the player stops moving
        if event.type == pygame.KEYUP and event.key in \
                [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
            if (event.key == pygame.K_w and self._orientation == Cardinality.NORTH) or \
                    (event.key == pygame.K_s and self._orientation == Cardinality.SOUTH) or \
                    (event.key == pygame.K_d and self._orientation == self._orientation.EAST) or \
                    (event.key == pygame.K_a and self._orientation == Cardinality.WEST):

                # Make sure that no other wasd key is pressed. If one is, then
                # start moving in that direction.
                still_pressed = [x for x in pygame.key.get_pressed() if x in
                                 [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]]
                if still_pressed != []:
                    return self.move(pygame.event.Event(pygame.KEYDOWN,
                                                        {key: still_pressed[0]}))
                else:
                    self._moving = False
                    self._key_down_timer = 0

        if event.type == pygame.KEYUP and event.key == pygame.K_b:
            self.stop_running()

        # ABS is used because EAST and WEST should both point to row 2 but
        # need to have distint values. Because of this WEST = -2 and to get to
        # the correct row we simply take the absolute value.
        self._row = abs(self._orientation.value)

    def start_running(self):
        """Player starts running."""
        self._running = True
        self._framesPerSecond = 8

    def stop_running(self):
        """Player stops running."""
        self._runnign = False
        self._framesPerSecond = 4

