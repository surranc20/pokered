import pygame
from .level_manager import LevelManager

class GameManager(object):
    def __init__(self, screen_size, player):
        self._player = player
        self._level = LevelManager(player, "elite_four_1")
        self._FSM = "running" #This is a temporary hack. Do not know if I will need FSM.

    def draw(self, surface):
        if self._FSM == "running":
            self._level.draw(surface)
   
    def handle_event(self, event):
        if self._FSM == "running": 
            self._level.handle_event(event)
    
    def update(self, ticks):
        if self._FSM == "running":
            warped = self._level.update(ticks)
            if warped == "RESTART":
                return "RESTART"
            if warped != None:
                self._level = LevelManager(self._player, warped)

