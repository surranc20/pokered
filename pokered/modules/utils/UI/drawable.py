import math
import pygame
from pygame import image
import os
from ..managers.frameManager import FRAMES
from ..vector2D import Vector2

class Drawable(object):

   WINDOW_OFFSET = Vector2(0,0)

   @classmethod
   def updateWindowOffset(cls, followObject, screenSize, worldSize):
      position = followObject.getPosition()
      size = followObject.getSize()
      Drawable.WINDOW_OFFSET = [min(max(0, position[x] - screenSize[x] // 2 + size[x] // 2), worldSize[x] - screenSize[x]) for x in range(2)]
      if Drawable.WINDOW_OFFSET[0] < 0: Drawable.WINDOW_OFFSET[0] = 0
      elif Drawable.WINDOW_OFFSET[1] < 0: Drawable.WINDOW_OFFSET[1] = 0

   def __init__(self, imageName, position, offset=None, world_bound=True):
      self._imageName = imageName
      self._offset = offset
      self._world_bound = world_bound

      # Let frame manager handle loading the image
      if self._imageName != "":
         self._image = FRAMES.getFrame(self._imageName, offset)
      self._position = position
      self._is_dead = False
      self._x_off = 0


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

   def center_with_border(self, screen_size):
      """Should only be called on overworld level backgrounds and foregrounds. Only does something if one of the overworld
      levels is smaller than the screen. Adds black borders around the image where needed."""
      # Calculate how much border space is needed on each axis.
      x_off = (screen_size[0] - self.getSize()[0]) / 2
      self._x_off = max(x_off, 0)
      y_off = (screen_size[1] - self.getSize()[1]) / 2
      # In this case we need to add borders on all four sides.
      if x_off > 0 and y_off > 0:
         # Create the border rectangles
         border = pygame.Surface((math.ceil(x_off), self.getSize()[1] + math.ceil(y_off) * 2))
         border.fill((0,30,200))
         border_h = pygame.Surface((math.ceil(x_off) * 2 + self.getSize()[0] , math.ceil(y_off)))
         border_h.fill((40,200,0))
         # Prep the new surface for the Drawable object
         surf = pygame.Surface((math.ceil(x_off) * 2 + self.getSize()[0], math.ceil(y_off) * 2 + self.getSize()[1]))
         surf.fill((30,30,30))
         surf.set_colorkey((30,30,30))
         # Add the vertical borders
         surf.blit(border, (0,0))
         surf.blit(border_h, (0,0))
         #surf.blit(self._image, (x_off, y_off))
         surf.blit(border, (x_off + self.getSize()[0], 0))
         surf.blit(border_h, (0, y_off + self.getSize()[1]))
         self._image = surf

      # In this case we only need to add borders on the sides. As of right now this is the only condition that
      # ever actually happens.
      elif x_off > 0:
         border = pygame.Surface((math.ceil(x_off), self.getSize()[1]))
         border.fill((0,0,0))
         surf = pygame.Surface((math.ceil(x_off) * 2 + self.getSize()[0] ,self.getSize()[1]))
         surf.fill((30,30,30))
         surf.set_colorkey((30,30,30))
         surf.blit(border, (0,0))
         surf.blit(self._image, (x_off, 0))
         surf.blit(border, (x_off + self.getSize()[0], 0))
         self._image = surf


   def draw(self, surface):
      if self._world_bound:
         surface.blit(self._image, (int(self._position[0] - Drawable.WINDOW_OFFSET[0]),
                                    int(self._position[1] - Drawable.WINDOW_OFFSET[1])))
      else:
         surface.blit(self._image, self._position)


   def reload(self):
      self._image = FRAMES.reload(self._imageName, self._offset)

   def __setstate__(self, state):
      """Reloads image from pickled save file."""
      self.__dict__.update(state)
      state["_image"] = FRAMES.getFrame(self._imageName, self._offset)
      self.__dict__.update(state)

   def __getstate__(self):
      """Deletes pygame images so that they are not stored in the
      save file."""
      state = self.__dict__.copy()
      del state["_image"]
      return state
