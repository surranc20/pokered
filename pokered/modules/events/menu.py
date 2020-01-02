import pygame
from ..utils.managers.frameManager import FRAMES


class Menu():
    def __init__(self):
        """Creates the pause menu for the game."""
        self._is_over = False
        self._save_queued = False
        self._make_menu(32, 32, 2)  #if you want to increase mids then increment y by 8 each time

    def draw(self, draw_surface):
        """Draws the menu."""
        print("drawing")
        draw_surface.blit(self._menu_surface, (130, 130))

    def update(self, ticks):
        """Updates the menu."""
        print(ticks)
        if self._save_queued:
            print("yo")
            return "Pickle"

    def handle_event(self, event):
        """Handles the inputs and updates menu accordingly."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RSHIFT:
            self._save_queued = True
            self._is_over = True

    def is_over(self):
        """Determines whether or not the menu is closed."""
        return self._is_over

    def get_end_event(self):
        """Returns the player back to the level."""
        return "Level"

    def _make_menu(self, x, y,how_many_mids):
        
        self._menu_surface = pygame.Surface((x, y))
        self._menu_surface.fill((255, 255, 255))  # random thing
        self._menu_surface.set_colorkey((255, 255, 255))
        top_left = FRAMES.getFrame("menu_parts.png", offset=(0, 0))
        top_mid = FRAMES.getFrame("menu_parts.png", offset=(1, 0))
        top_right = FRAMES.getFrame("menu_parts.png", offset=(2, 0))
        white_blob = FRAMES.getFrame("menu_parts.png", offset=(1, 1))
        mid_left = FRAMES.getFrame("menu_parts.png", offset=(0, 1))
        mid_right = FRAMES.getFrame("menu_parts.png", offset=(2, 1))
        bottom_right = FRAMES.getFrame("menu_parts.png", offset=(2, 2))
        bottom_left = FRAMES.getFrame("menu_parts.png", offset=(0, 2))
        bottom_mid = FRAMES.getFrame("menu_parts.png", offset=(1, 2))

        white_blob.set_colorkey((30, 40, 10))
        self._menu_surface.blit(top_left, (0, 0))
        self._menu_surface.blit(top_mid, (8, 0))
        self._menu_surface.blit(top_mid, (16, 0))
        self._menu_surface.blit(top_right, (24, 0))
        current_y = 8
        for i in range(how_many_mids):
            self._menu_surface.blit(mid_left, (0, current_y))
            self._menu_surface.blit(white_blob, (8, current_y))
            self._menu_surface.blit(white_blob, (16, current_y))
            self._menu_surface.blit(mid_right, (24, current_y))
            current_y += 8
        self._menu_surface.blit(bottom_left, (0, current_y))
        self._menu_surface.blit(bottom_mid, (8, current_y))
        self._menu_surface.blit(bottom_mid, (16, current_y))
        self._menu_surface.blit(bottom_right, (24, current_y))
        #self._menu_surface.blit(top_right, (16, 0))
        #self._menu_surface.blit(white_blob, (8, 8))
        #self._menu_surface.blit(mid_left, (0, 8))
        
        # self._menu_surface.blit(mid_right, (16, 8))
        # self._menu_surface.blit(bottom_right, (16, 16))
        # self._menu_surface.blit(bottom_left, (0, 16))
        # self._menu_surface.blit(bottom_mid, (8, 16))



