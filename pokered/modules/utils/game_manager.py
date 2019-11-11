import pygame
from .levelManager import LevelManager
from .FSMs.gameFSM import GameState


class GameManager(object):
   def __init__(self, screenSize):
      self._level = LevelManager()
      self._FSM = "running" #This is a temporary hack. Do not know if I will need FSM.

   def draw(self, surface):
      if self._FSM == "running":
         self._level.draw(surface)
   
   def handleEvent(self, event):
    if self._FSM == "running": 
        self._level.handleEvent(event)
    
   def update(self, ticks, screenSize):
      if self._FSM == "running":
         self._level.update(ticks, screenSize)

