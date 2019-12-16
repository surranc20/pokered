import pygame
from os.path import join
from .move_base import MoveBase
from ...utils.managers.soundManager import SoundManager
from ...utils.UI.drawable import Drawable

# TODO: animate the actual wave like it appears in the game


class Surf(MoveBase):

    def __init__(self, attacker, defender, enemy=False):
        """Creates the surf animation. The move extends MoveBase but
        overwrites most of the logic."""
        super().__init__(attacker, defender, enemy=enemy)
        # Get the correct surf image based on who is using the move
        self._surf = Drawable(join("moves", "surf.png"),
                              (0 if not self._enemy else 130,
                              48 if not self._enemy else 0),
                              (0, 1 if not self._enemy else 0))

        # The location of the transparent pixel is different based on which
        # surf image is used
        if self._enemy:
            self._surf._image.set_colorkey(self._surf._image.get_at((111, 63)))

        # Set fps and play surf sound
        self._fps = 20
        SoundManager.getInstance().playSound(join("moves", "surf.wav"))

    def update(self, ticks):
        """Updates the surf animation. Essentially it moves the surf png
        diagonally anf fill in the levels the png has already travelled with
        blue in order to give the appearance of a wave. """
        self._animation_timer += ticks
        if self._animation_timer > 1 / self._fps:
            self._animation_timer -= 1 / self._fps
            self._move_surface = pygame.Surface((240, 112))
            self._move_surface.set_colorkey((0, 0, 0))

            # If the user uses the move then the wave travels upwards
            # diagonally and fills the area beneath the wave with blue.
            if not self._enemy:
                self._water_surface = \
                    pygame.Surface((240, 112 - self._surf._position[1] + 64))
                self._water_surface.fill(self._surf._image.get_at((0, 63)))
                self._move_surface.blit(self._water_surface,
                                        (0, self._surf._position[1] + 50))
                self._move_surface.blit(self._surf._image,
                                        self._surf._position)
                self._move_surface.set_alpha(200)
                self._surf._position = (self._surf._position[0] + 4,
                                        self._surf._position[1] - 2)

                if self._surf._position[0] > 130:
                    self._is_dead = True

            # If the enemy used the move then the wave travels diagonally
            # downward and fills the area above the wave with blue.
            else:
                self._water_surface = \
                    pygame.Surface((240, 64 + self._surf._position[1]))
                self._water_surface.fill(self._surf._image.get_at((0, 0)))
                self._move_surface.blit(self._water_surface, (0, 0))
                self._move_surface.blit(self._surf._image,
                                        self._surf._position)
                self._move_surface.set_alpha(200)
                self._surf._position = (self._surf._position[0] - 4,
                                        self._surf._position[1] + 2)

                # If the wave has travelled far enough to the right then the
                # animation is over.
                if self._surf._position[0] < 2:
                    self._is_dead = True
