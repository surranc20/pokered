import pygame
from ..managers.frameManager import FRAMES


class ResizableMenu():
    def __init__(self, lines):
        self.lines = lines
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

    def _create_menu(self):
        # Create the surface where the menu is drawn
        self.menu_surface = pygame.Surface((64, 120))
        self.menu_surface.fill((255, 255, 255))
        self.menu_surface.set_colorkey((255, 255, 255))

        # Create the top row of the menu
        top_left = FRAMES.getFrame("menu_parts.png", offset=(0, 0))
        top_mid = FRAMES.getFrame("menu_parts.png", offset=(1, 0))
        top_right = FRAMES.getFrame("menu_parts.png", offset=(2, 0))
        self.menu_surface.blit(top_left, (0, 0))
        self.menu_surface.blit(top_mid, (8, 0))
        self.menu_surface.blit(top_mid, (16, 0))
        self.menu_surface.blit(top_mid, (24, 0))
        self.menu_surface.blit(top_mid, (32, 0))
        self.menu_surface.blit(top_mid, (40, 0))
        self.menu_surface.blit(top_mid, (48, 0))
        self.menu_surface.blit(top_right, (56, 0))

        # Create the middle rows
        white_blob = FRAMES.getFrame("menu_parts.png", offset=(1, 1))
        mid_left = FRAMES.getFrame("menu_parts.png", offset=(0, 1))
        mid_right = FRAMES.getFrame("menu_parts.png", offset=(2, 1))
        white_blob.set_colorkey((30, 40, 10))

        # Create the appropriated number of middle rows
        current_y = 8
        for i in range(self._middlelines):
            self.menu_surface.blit(mid_left, (0, current_y))
            self.menu_surface.blit(white_blob, (8, current_y))
            self.menu_surface.blit(white_blob, (16, current_y))
            self.menu_surface.blit(white_blob, (24, current_y))
            self.menu_surface.blit(white_blob, (32, current_y))
            self.menu_surface.blit(white_blob, (40, current_y))
            self.menu_surface.blit(white_blob, (48, current_y))
            self.menu_surface.blit(mid_right, (56, current_y))
            current_y += 8

        # Create the bottom rows
        bottom_right = FRAMES.getFrame("menu_parts.png", offset=(2, 2))
        bottom_left = FRAMES.getFrame("menu_parts.png", offset=(0, 2))
        bottom_mid = FRAMES.getFrame("menu_parts.png", offset=(1, 2))
        self.menu_surface.blit(bottom_left, (0, current_y))
        self.menu_surface.blit(bottom_mid, (8, current_y))
        self.menu_surface.blit(bottom_mid, (16, current_y))
        self.menu_surface.blit(bottom_mid, (24, current_y))
        self.menu_surface.blit(bottom_mid, (32, current_y))
        self.menu_surface.blit(bottom_mid, (40, current_y))
        self.menu_surface.blit(bottom_mid, (48, current_y))
        self.menu_surface.blit(bottom_right, (56, current_y))

