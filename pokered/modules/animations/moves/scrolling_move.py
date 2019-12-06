import pygame
from os.path import join
from .move_base import MoveBase
from ...utils.frameManager import FRAMES
from ...utils.drawable import Drawable

class ScrollingMove(MoveBase):
    def __init__(self, attacker, defender, enemy=False):
        """This class, which extends MoveBase, is the basis for all moves that have a scrolling background. 
        One can see an example of this in moves like Thunder. This class controls the scrolling of the 
        background."""
        self._attacker = attacker
        self._defender = defender
        super().__init__(attacker, defender, enemy=enemy)



    def update(self, ticks):
        """Handles the scrolling of the background and returns the background surface. We can not simply
        blit the scrolling background as usual becuase the background must appear behind the pokemon. Therefore,
        we need to pass it to the battle fsm and have it handle displaying the background."""
        super().update(ticks)
        self._scrolling_background.scroll(dx=-1)
        if self.is_dead():

            # Get the scrolling backgrounds file name based on the normal file name for the move and reset it.
            # The splice operaton gets rid of the .png which appears at the end of the move file name.
            self._scrolling_background = FRAMES.reload(self._move_file_name[:-4] + "_background.png", (0,0))
            return
        
        # Blit the scrolled move to the background_surfae and return it
        background_surface = Drawable("", (0,0))
        background_surface._image = pygame.Surface((240, 112))
        background_surface._image.blit(self._scrolling_background, (0,0))
        return background_surface

