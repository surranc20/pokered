import pygame
from os.path import join
from .move_base import MoveBase
from ...utils.frameManager import FRAMES
from ...utils.drawable import Drawable

class ScrollingMove(MoveBase):
    def __init__(self, attacker, defender, enemy=False):
        self._attacker = attacker
        self._defender = defender
        super().__init__(attacker, defender, enemy=enemy)
        self._scroll_count = 0


    def update(self, ticks):
        super().update(ticks)
        self._scrolling_background.scroll(dx=-1)
        if self.is_dead():
            # splice to get rid of .png at the end of the name
            self._scrolling_background = FRAMES.reload(self._move_file_name[:-4] + "_background.png", (0,0))
            return
        
        background_surface = Drawable("", (0,0))
        background_surface._image = pygame.Surface((240, 112))
        background_surface._image.blit(self._scrolling_background, (0,0))
        return background_surface

