
from .animated import Animated
from .vector2D import Vector2


class Mobile(Animated):
   def __init__(self, imageName, position, cardinality):
      super().__init__(imageName, position)
      self._orientation = cardinality
      self._row = self._orientation.value
   
   def update(self, ticks):
      super().update(ticks)
      
      
      