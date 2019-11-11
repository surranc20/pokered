from .vector2D import Vector2
from .drawable import Drawable
   
class LevelManager(object):
   def __init__(self, player):
      self._player = player

   def draw(self, surface):
      surface.fill((30,30,30))
      
   def handle_event(self, event):
      self._player.handleEvent(event)
      
   def update(self, ticks, screenSize):
      self._star.update(ticks, LevelManager._WORLD_SIZE)
      Drawable.updateWindowOffset(self._star, screenSize, LevelManager._WORLD_SIZE)