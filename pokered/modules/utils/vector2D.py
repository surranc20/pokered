import math
from pygame import Rect

class Vector2(object):
   def __init__(self, x, y):
      self.x = x
      self.y = y

   def __len__(self):
      """Length of vector."""
      return self.magnitude()
   
   def magnitude(self):
      """Length of vector, or distance."""
      return math.sqrt(self.x**2 + self.y**2)

   def normalize(self):
      """Calculates normal and modifies in-place."""
      distance = self.magnitude()
      
      if distance:
          self.x /= distance
          self.y /= distance
          
      return self


   def normalized(self):
      """Returns normalized Vector2, does not modify in-place."""
      distance = self.magnitude()
      
      if distance:
         return Vector2(self.x / distance, self.y / distance)

      return Vector2(*self)
   
   def dot(self, other):
      """Returns the dot product."""
      nOther = other.normalized()
      nSelf = self.normalized()
      
      products = [nOther[x] * nSelf[x] for x in range(2)]
      
      return sum(products)
   
   def rotate(self, radians):
      """Rotates the vector, expects radians."""
      newX = math.cos(radians)*self.x - math.sin(radians)*self.y
      newY = math.sin(radians)*self.x + math.cos(radians)*self.y
      
      self.x = newX
      self.y = newY
   
   def __iter__(self):
      """Iterates over both coordinates."""
      yield self.x
      yield self.y
      
   
   def __getitem__(self, index):
      """For easy access. Index must be 0 or 1."""
      if index == 0:
         return self.x
      
      elif index == 1:
         return self.y
      
      else:
         raise IndexError("Index out of bounds: " + str(index))
      
   def __setitem__(self, index, value):
      """For easy access. Index must be 0 or 1."""
      if index == 0:
         self.x = value
      
      elif index == 1:
         self.y = value
         
      else:
         raise IndexError("Index out of bounds: " + str(index))
         
   
   def scale(self, length):
      """Scales the magnitude of self to the length.
         First normalizes then scales to appropriate size."""
      self.normalize()
      
      self.x *= length
      self.y *= length
  
   
   def __mul__(self, other):
      """Multiplies self by other and returns result.
         Other can be of type Vector2 or type int/float."""
      if type(other) in [float, int]:
         clone = Vector2(*self)
         clone.x *= other
         clone.y *= other
      
         return clone
      
      elif type(other) == type(self):
         clone = Vector2(*self)
         clone.x *= other.x
         clone.y *= other.y
         
         return clone
   
   def __truediv__(self, other):
      """Divides self by other and returns result.
         Other can be of type Vector2 or type int/float."""
      if type(other) in [float, int]:
         clone = Vector2(*self)
         clone.x /= other
         clone.y /= other
      
         return clone
      
      elif type(other) == type(self):
         clone = Vector2(*self)
         clone.x /= other.x
         clone.y /= other.y
         
         return clone
      
   def __floordiv__(self, other):
      """Divides self by other and returns result.
         Other can be of type Vector2 or type int/float."""
      if type(other) in [float, int]:
         clone = Vector2(*self)
         clone.x //= other
         clone.y //= other
      
         return clone
      
      elif type(other) == type(self):
         clone = Vector2(*self)
         clone.x //= other.x
         clone.y //= other.y
         
         return clone
      
      
   def __add__(self, other):
      """Adds other to self and returns result.
         Other can be of type Vector2 or type pygame.Rect."""
      if type(other) == type(self):
         clone = Vector2(*self)
         clone[0] += other[0]
         clone[1] += other[1]
      
         return clone
   
      elif type(other) == Rect:
         clone = Rect(other)
         clone.left += self[0]
         clone.top += self[1]
         
         return clone
      
   def __sub__(self, other):
      """Subtracts other from self and returns result.
         Other can be of type Vector2 or type pygame.Rect."""
      if type(other) == type(self):
         clone = Vector2(*self)
         clone[0] -= other[0]
         clone[1] -= other[1]
      
         return clone
   
      elif type(other) == Rect:
         clone = Rect(other)
         clone.left -= self[0]
         clone.top -= self[1]
         
         return clone
  
   def __str__(self):
      return repr(self)

   def __repr__(self):
      return "Vector2({:.2f}, {:.2f})".format(self.x, self.y)