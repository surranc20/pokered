import pygame
from ..managers.frameManager import FRAMES


class ResizableMenu():
    def __init__(self, lines, width=8):
        self.lines = lines
        self.width = width
        self._middlelines = self._calculate_middlelines()
        self._create_menu()
        self.size = self._middlelines + 2

    def _calculate_middlelines(self):
        """Return how many middle sections are needed for the size of the
        menu."""
        if self.lines == 8:
            return 12
        elif self.lines == 7:
            return 10
        elif self.lines == 6:
            return 9
        elif self.lines == 5:
            return 7
        elif self.lines == 4:
            return 6
        elif self.lines == 3:
            return 4
        elif self.lines == 2:
            return 3

    def _create_menu(self):
        # Create the surface where the menu is drawn
        self.menu_surface = pygame.Surface((100, 120))
        self.menu_surface.fill((255, 255, 255))
        self.menu_surface.set_colorkey((255, 255, 255))

        # Create the top corners of the menu
        top_left = FRAMES.getFrame("menu_parts.png", offset=(0, 0))
        top_mid = FRAMES.getFrame("menu_parts.png", offset=(1, 0))
        top_right = FRAMES.getFrame("menu_parts.png", offset=(2, 0))
        self.menu_surface.blit(top_left, (0, 0))


        # Create the middle rows
        white_blob = FRAMES.getFrame("menu_parts.png", offset=(1, 1))
        mid_left = FRAMES.getFrame("menu_parts.png", offset=(0, 1))
        mid_right = FRAMES.getFrame("menu_parts.png", offset=(2, 1))
        white_blob.set_colorkey((30, 40, 10))

        # Create the appropriated number of middle rows
        current_y = 8
        for i in range(self._middlelines):
            self.menu_surface.blit(mid_left, (0, current_y))
            width = 8
            for x in range(self.width - 2):
                self.menu_surface.blit(top_mid, (width, 0))
                self.menu_surface.blit(white_blob, (width, current_y))
                width += 8

            self.menu_surface.blit(top_right, (width, 0))
            self.menu_surface.blit(mid_right, (width, current_y))
            current_y += 8

        # Create the bottom row
        bottom_right = FRAMES.getFrame("menu_parts.png", offset=(2, 2))
        bottom_left = FRAMES.getFrame("menu_parts.png", offset=(0, 2))
        bottom_mid = FRAMES.getFrame("menu_parts.png", offset=(1, 2))
        self.menu_surface.blit(bottom_left, (0, current_y))
        width = 8
        for x in range(self.width - 2):
            self.menu_surface.blit(bottom_mid, (width, current_y))
            width += 8
        self.menu_surface.blit(bottom_right, (width, current_y))

