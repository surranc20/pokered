import pygame
from .levelManager import LevelManager
from .FSMs.gameFSM import GameState


class GameManager(object):
    def __init__(self, screenSize):
        self._screen_size = screen_size
        self._level = LevelManager()
        self._FSM = "running" #This is a temporary hack. Do not know if I will need FSM.

    def draw(self, surface):
        if self._FSM == "running":
            self._level.draw(surface)
   
    def handle_event(self, event):
        if self._FSM == "running": 
            self._level.handle_event(event)
    
    def update(self, ticks):
        if self._FSM == "running":
            self._level.update(ticks, self._screen_size)

