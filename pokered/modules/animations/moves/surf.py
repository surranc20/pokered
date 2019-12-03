import pygame
from os.path import join
from .move_base import MoveBase
from ...utils.soundManager import SoundManager
from ...utils.drawable import Drawable

class Surf(MoveBase):
    
    def __init__(self, attacker, defender, enemy=False):
        super().__init__(attacker, defender, enemy=enemy)
        self._surf = Drawable(join("moves", "surf.png"), (0 if not self._enemy else 130 ,48 if not self._enemy else 0), (0, 1 if not self._enemy else 0))
        if self._enemy:
            self._surf._image.set_colorkey(self._surf._image.get_at((111,63)))
        self._fps = 20
        SoundManager.getInstance().playSound(join("moves", "surf.wav"))

    def update(self, ticks):
        self._animation_timer += ticks
        if self._animation_timer > 1 / self._fps:
            self._animation_timer -= 1 / self._fps
            self._move_surface = pygame.Surface((240, 112))
            self._move_surface.set_colorkey((0,0,0))

            if not self._enemy:
                self._water_surface = pygame.Surface((240, 112 - self._surf._position[1] + 64))
                self._water_surface.fill(self._surf._image.get_at((0, 63)))
                self._move_surface.blit(self._water_surface, (0, self._surf._position[1] + 50))
                self._move_surface.blit(self._surf._image, self._surf._position)
                self._move_surface.set_alpha(200)
                self._surf._position = (self._surf._position[0] + 4, self._surf._position[1] - 2)

                if self._surf._position[0] > 130:
                    self._is_dead = True
            
            else: 
                self._water_surface = pygame.Surface((240, 64 + self._surf._position[1]))
                self._water_surface.fill(self._surf._image.get_at((0, 0)))
                self._move_surface.blit(self._water_surface, (0, 0))
                self._move_surface.blit(self._surf._image, self._surf._position)
                self._move_surface.set_alpha(200)
                self._surf._position = (self._surf._position[0] - 4, self._surf._position[1] + 2)

                if self._surf._position[0] < 2:
                    self._is_dead = True