import pygame
from pygame import image
import os
from ..managers.frameManager import FRAMES
from .drawable import Drawable

class Animated(Drawable):

   def __init__(self, imageName, location, offset=(0,0)):
      """Simple Animated class that extends drawable. Is the same as what we have used in class."""
      super().__init__(imageName, location, offset)

      self._frame = 0
      self._row = 0
      self._animationTimer = 0
      self._framesPerSecond = 10.0
      self._nFrames = 2
      self._animate = True
      self._current_image_row = 0
      self._flip = False

   def update(self, ticks):
      if self._animate:
         self._animationTimer += ticks

         if self._animationTimer > 1 / self._framesPerSecond:
            self._frame += 1
            self._frame %= self._nFrames
            self._animationTimer -= 1 / self._framesPerSecond
            self._image = FRAMES.getFrame(self._imageName, (self._frame, self._row))
            self._current_image_row = self._row

            if self._flip: self._image = pygame.transform.flip(self._image, True, False)

   def get_current_frame(self):
      self._image = FRAMES.getFrame(self._imageName, (self._frame, self._row))
      if self._flip: self._image = pygame.transform.flip(self._image, True, False)

   def startAnimation(self):
      self._animate = True


   def stopAnimation(self):
      self._animate = False
      self._image = FRAMES.getFrame(self._imageName, (self._frame, self._row))
      if self._flip: self._image = pygame.transform.flip(self._image, True, False)

class AnimatedGroup():
   def __init__(self, animations, terminating_animation=False, all_on=False):
      """Creates an animated group. Takes the following as arguments: animations is the list of animated group parts
      that make up the animation group, if terminating_animation is not false then the animation passed into terminating_animation
      will play once the animated group is over, if all_on is true then the group will play all animations at once otherwise only the
      first will begin playing."""
      self._animations = animations
      self._active_anims = {anim : all_on for anim in animations}
      self._active_anims[animations[0]] = True
      self._is_dead = False
      self._terminating_animation = terminating_animation

   def update(self, ticks):
      """Updates the AnimatedGroup. It does so by updating each of the sub animations."""
      action_taken = False
      for anim in self._animations:
         if anim.is_dead(): self._active_anims[anim] = False
         if self._active_anims[anim]:
            # Trigger can either be None (the default case) or an index specifying the index of an animated group part.
            trigger = anim.update(ticks)
            action_taken = True
            # If one of the animated group parts returned a trigger then turn the animation at that index on.
            if trigger != None and trigger < len(self._animations):
               self._active_anims[self._animations[trigger]] = True

      # If no action was taken that means all the AnimatedGroupParts are dead and therefore the AniamtedGroup is done.
      if not action_taken:
         self.kill()
         return self._terminating_animation

   def kill(self):
      """Kills the animated group and returns the terminating animation."""
      self._is_dead = True
      return self._terminating_animation if self._terminating_animation else None

   def __repr__(self):
      """Used for debugging purposes. Allows the programmer to print the AnimatedGroup and see useful information."""
      return str(self._active_anims)

   def is_dead(self):
      """Returns whether or not the Animated Group is dead."""
      return self._is_dead

   def draw(self, draw_surface):
      """Draws each of the active animations."""
      for anim in self._animations:
         if self._active_anims[anim]:
            anim.draw(draw_surface)

class AnimatedGroupPart(Animated):
   def __init__(self, imageName, location, anim_sequence_pos, offset=(0,0)):
      """Small class that combines an animated object with its position in the animated group."""
      super().__init__(imageName, location, offset= offset)
      self._anim_sequence_pos = anim_sequence_pos








