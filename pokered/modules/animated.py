import pygame
from pygame import image
import os
from .frameManager import FRAMES
from .drawable import Drawable

class Animated(Drawable):
   
   def __init__(self, imageName, location):
      super().__init__(imageName, location, (0,0))
      
      self._frame = 0
      self._row = 0
      self._animationTimer = 0
      self._framesPerSecond = 10.0
      self._nFrames = 2      
      self._animate = True
      self._flip = False
      
   def update(self, ticks):
      if self._animate:
         self._animationTimer += ticks
         
         if self._animationTimer > 1 / self._framesPerSecond:
            self._frame += 1
            self._frame %= self._nFrames
            self._animationTimer -= 1 / self._framesPerSecond
            self._image = FRAMES.getFrame(self._imageName, (self._frame, self._row))

            if self._flip: self._image = pygame.transform.flip(self._image, True, False)

   def startAnimation(self):
      self._animate = True
   
   
   def stopAnimation(self):
      self._animate = False
      self._image = FRAMES.getFrame(self._imageName, (self._frame, self._row))
      if self._flip: self._image = pygame.transform.flip(self._image, True, False)

class AnimatedGroup():
   def __init__(self, animations):
      self._animations = animations
      self._active_anims = {anim : False for anim in animations}
      self._active_anims[animations[0]] = True
      self._is_dead = False

   def update(self, ticks):
      action_taken = False
      for anim in self._animations: 
         if anim.is_dead(): self._active_anims[anim] = False
         if self._active_anims[anim]:
            trigger = anim.update(ticks)
            if trigger != None and trigger < len(self._animations):
               self._active_anims[self._animations[trigger]] = True
               action_taken = True
      
      if not action_taken: self._is_dead = True
   
   def is_dead(self): 
      return self._is_dead
   
   def draw(self, draw_surface):
      for anim in self._animations:
         if self._active_anims[anim]:
            anim.draw(draw_surface)
   
class AnimatedGroupPart(Animated):
   def __init__(self, imageName, location, anim_sequence_pos):
      super().__init__(imageName, location)
      self._anim_sequence_pos = anim_sequence_pos
      

      





