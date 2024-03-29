
from .animated import Animated
from ..vector2D import Vector2
from ...enumerated.cardinality import Cardinality


class Mobile(Animated):
   def __init__(self, imageName, position, cardinality):
      """Simple mobile class. I should eventually extract out the movement code
      from my player class and move it here."""
      super().__init__(imageName, position)
      self._orientation = cardinality
      if self._orientation == Cardinality.EAST:
         self._flip = True
      self._row = abs(self._orientation.value)

   def update(self, ticks):
      """Updates"""
      super().update(ticks)


