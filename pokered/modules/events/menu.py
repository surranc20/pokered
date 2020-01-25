import pygame
from os.path import join
from ..utils.vector2D import Vector2
from ..utils.text_maker import TextMaker
from ..utils.managers.frameManager import FRAMES


class Menu():
    def __init__(self, player):
        """Creates the pause menu for the game."""
        self._player = player
        self._is_over = False
        self._save_queued = False
        self._make_menu()
        self._make_menu_text()

    def draw(self, draw_surface):
        """Draws the menu."""
        draw_surface.blit(self._menu_surface, (180, 10))
        draw_surface.blit(self._text_surface, (180, 10))

    def update(self, ticks):
        """Updates the menu."""
        if self._save_queued:
            return "Pickle"

    def handle_event(self, event):
        """Handles the inputs and updates menu accordingly."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RSHIFT:
            # self._save_queued = True
            self._is_over = True

    def is_over(self):
        """Determines whether or not the menu is closed."""
        return self._is_over

    def get_end_event(self):
        """Returns the player back to the level."""
        return "Level"

    def _make_menu(self):
        """Creates the menu image."""
        # Create the surface where the menu is drawn
        self._menu_surface = pygame.Surface((56, 100))
        self._menu_surface.fill((255, 255, 255))
        self._menu_surface.set_colorkey((255, 255, 255))

        # Create the top row of the menu
        top_left = FRAMES.getFrame("menu_parts.png", offset=(0, 0))
        top_mid = FRAMES.getFrame("menu_parts.png", offset=(1, 0))
        top_right = FRAMES.getFrame("menu_parts.png", offset=(2, 0))
        self._menu_surface.blit(top_left, (0, 0))
        self._menu_surface.blit(top_mid, (8, 0))
        self._menu_surface.blit(top_mid, (16, 0))
        self._menu_surface.blit(top_mid, (24, 0))
        self._menu_surface.blit(top_mid, (32, 0))
        self._menu_surface.blit(top_mid, (40, 0))
        self._menu_surface.blit(top_right, (48, 0))

        # Create the middle rows
        white_blob = FRAMES.getFrame("menu_parts.png", offset=(1, 1))
        mid_left = FRAMES.getFrame("menu_parts.png", offset=(0, 1))
        mid_right = FRAMES.getFrame("menu_parts.png", offset=(2, 1))
        white_blob.set_colorkey((30, 40, 10))

        current_y = 8
        for i in range(7):
            self._menu_surface.blit(mid_left, (0, current_y))
            self._menu_surface.blit(white_blob, (8, current_y))
            self._menu_surface.blit(white_blob, (16, current_y))
            self._menu_surface.blit(white_blob, (24, current_y))
            self._menu_surface.blit(white_blob, (32, current_y))
            self._menu_surface.blit(white_blob, (40, current_y))
            self._menu_surface.blit(mid_right, (48, current_y))
            current_y += 8

        # Create the bottom rows
        bottom_right = FRAMES.getFrame("menu_parts.png", offset=(2, 2))
        bottom_left = FRAMES.getFrame("menu_parts.png", offset=(0, 2))
        bottom_mid = FRAMES.getFrame("menu_parts.png", offset=(1, 2))
        self._menu_surface.blit(bottom_left, (0, current_y))
        self._menu_surface.blit(bottom_mid, (8, current_y))
        self._menu_surface.blit(bottom_mid, (16, current_y))
        self._menu_surface.blit(bottom_mid, (24, current_y))
        self._menu_surface.blit(bottom_mid, (32, current_y))
        self._menu_surface.blit(bottom_mid, (40, current_y))
        self._menu_surface.blit(bottom_right, (48, current_y))

    def _make_menu_text(self):
        """Adds the menu text to the menu"""
        # Create the surface where the text is drawn
        self._text_surface = pygame.Surface((56, 100))
        self._text_surface.fill((255, 255, 255))
        self._text_surface.set_colorkey((255, 255, 255))

        menu_text = ["bag", "PLAYER", "SAVE", "OPTION", "EXIT"]
        current_pos = Vector2(0, 10)
        text_maker = TextMaker(join("fonts", "party_txt_font.png"))
        for text in menu_text:
            current_pos.x = 12
            word_surf = text_maker.get_surface(text)
            self._text_surface.blit(word_surf, (current_pos.x, current_pos.y))
            current_pos.y += 11






            # for char in text.lower():
            #     font_index = int(ord(char)) - 97
            #     font_char = FRAMES.getFrame("party_txt_font.png",
            #                                 offset=(font_index, 0))
            #     font_char.set_colorkey((255, 255, 255))
            #     self._text_surface.blit(font_char, (current_pos.x, current_pos.y))
            #     current_pos.x += 5
            # current_pos.y += 11
