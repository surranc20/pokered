import pygame
from os.path import join
from ...utils.frameManager import FRAMES
from ...utils.drawable import Drawable


class MoveBase():
    def __init__(self, enemy=False):
        self._enemy = enemy
        self._is_dead = False
        self._move_surface = pygame.Surface((240, 112))
        self._frame_num = 0
        self._fps = 30
        self._animation_timer = 0

    def is_dead(self):
        return self._is_dead
    
    def draw(self, draw_surface):
        draw_surface.blit(self._move_surface, (0,0))
    
    def update(self, ticks):
        self._animation_timer += ticks
        if self._animation_timer > 1 / self._fps:
            self._animation_timer -= 1 / self._fps

            self._move_surface = pygame.Surface((240, 112))
            self._move_surface.set_colorkey((0,0,0))
            frame = self.FRAME_LIST[self._frame_num]
            for sprite in frame:
                sprite_frame = FRAMES.getFrame(self._move_file_name,(sprite[0], 0))
                if len(sprite) == 3:
                    if sprite[2] == "h":
                        sprite_frame = pygame.transform.flip(sprite_frame, True, False)
                    elif sprite[2] == "v":
                        sprite_frame = pygame.transform.flip(sprite_frame, False, True)
                    elif sprite[2] == "hv":
                        sprite_frame = pygame.transform.flip(sprite_frame, True, True)
                    elif sprite[2] == "r":
                        sprite_frame = pygame.transform.rotate(sprite_frame, 90)
                if self._enemy:
                    self._move_surface.blit(sprite_frame, (sprite[1][0] - 120, max(sprite[1][1], 0) + 40))
                else:
                    self._move_surface.blit(sprite_frame, (sprite[1][0] - 5, sprite[1][1]))
            if self._frame_num < len(self.FRAME_LIST) - 1:
                self._frame_num += 1
            else:
                 self._is_dead = True
                 

        
        

