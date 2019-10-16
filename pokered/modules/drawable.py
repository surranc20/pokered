import pygame
from pygame import image
import os
from .frameManager import FRAMES

class Drawable(object):
   
   
   def __init__(self, imageName, position, offset=None):
      self._imageName = imageName
      self._offset = offset

      # Let frame manager handle loading the image
      self._image = FRAMES.getFrame(self._imageName, offset)
      self._position = position
      self._is_dead = False

      
   def getPosition(self):
      return self._position

   def setPosition(self, newPosition):
      self._position = newPosition
      
   def getSize(self):
      return self._image.get_size()

   def getCollisionRect(self):
      newRect =  self._position + self._image.get_rect()
      return newRect
   
   def kill(self):
      self._is_dead = True
   
   def is_dead(self):
      return self._is_dead
   
   def draw(self, surface):
      surface.blit(self._image, (self._position[0], self._position[1]))
   
   def reload(self):
      self._image = FRAMES.reload(self._imageName, self._offset)
     