import pygame
from os.path import join
from ..enumerated.battle_actions import BattleActions
from ..utils.vector2D import Vector2
from ..utils.text_maker import TextMaker
from ..utils.managers.frameManager import FRAMES
from ..utils.UI.drawable import Drawable
from ..utils.managers.soundManager import SoundManager

# TODO: Inherit pokemon selected menu and pokeparty and override appropriate
# functions


class Menu():
    HELP_TEXT = {
        "BAG": "Equiped with pockets for storing items you bought, "
        "received, or found.",
        "SAVE": "Save your game with a complete record of your progress to "
        "take a break.",
        "OPTION": "Adjust various game settings such as text, speed, game "
        "rules, etc.",
        "EXIT": "Close this MENU window.",
        "POKeMON": "Check and organize POKeMON that are traveling with you in "
        "your party.",
        "POKeDEX": "A device that records POKeMON secrets upon meeting them "
        "or catching them.",
        "PLAYER": "Check your money and other game data."}

    def __init__(self, player):
        """Creates the pause menu for the game."""
        self._player = player
        self._is_over = False
        self._save_queued = False
        self._make_menu()
        self._make_menu_text()
        self._cursor = Cursor(len(self._options))
        self._make_help_bar()
        self._make_help_text(self._get_help_text())
        self._active_sub_menu = False

    def draw(self, draw_surface):
        """Draws the menu."""
        draw_surface.blit(self._menu_surface, (172, 10))
        draw_surface.blit(self._text_surface, (172, 10))
        draw_surface.blit(self._help_surface, (0, 122))
        draw_surface.blit(self._help_text_surface, (0, 122))
        self._cursor.draw(draw_surface)

    def update(self, ticks):
        """Updates the menu."""
        if self._save_queued:
            return "Pickle"

    def handle_event(self, event):
        """Handles the inputs and updates menu accordingly."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RSHIFT:
            # self._save_queued = True
            self._is_over = True

        # Up or down action.
        elif event.type == pygame.KEYDOWN and event.key in [
                BattleActions.UP.value, BattleActions.DOWN.value]:
            SoundManager.getInstance().playSound("firered_0005.wav")
            self._cursor.change_cursor_pos(event)
            self._make_help_text(self._get_help_text())

        # Select action.
        elif event.type == pygame.KEYDOWN and event.key == \
                BattleActions.SELECT.value:
            SoundManager.getInstance().playSound("firered_0005.wav")
            current_selected = self._options[self._cursor.cursor]
            if current_selected == "EXIT":
                self._is_over = True

    def is_over(self):
        """Determines whether or not the menu is closed."""
        return self._is_over

    def get_end_event(self):
        """Returns the player back to the level."""
        return "Level"

    def _get_help_text(self):
        """Returns the appropriate help text given the selected menu item"""
        current_selected = self._options[self._cursor.cursor]
        if current_selected == str(self._player.name):
            current_selected = "PLAYER"
        return self.HELP_TEXT[current_selected]

    def _make_menu(self):
        """Creates the menu image."""
        # Create the surface where the menu is drawn
        self._menu_surface = pygame.Surface((64, 100))
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
        self._menu_surface.blit(top_mid, (48, 0))
        self._menu_surface.blit(top_right, (56, 0))

        # Create the middle rows
        white_blob = FRAMES.getFrame("menu_parts.png", offset=(1, 1))
        mid_left = FRAMES.getFrame("menu_parts.png", offset=(0, 1))
        mid_right = FRAMES.getFrame("menu_parts.png", offset=(2, 1))
        white_blob.set_colorkey((30, 40, 10))

        # Look at the players progress and see which menu items should be
        # displayed given their progress in the game. (i.e has player received
        # their first pokemon yet...)
        middle_rows = 7
        if self._player.pokedex is not None:
            middle_rows += 1
        if self._player.has_first_pokemon:
            middle_rows += 1
        if middle_rows == 9:
            middle_rows += 1
        if middle_rows == 8:
            middle_rows += 1

        # Create the appropriated number of middle rows
        current_y = 8
        for i in range(middle_rows):
            self._menu_surface.blit(mid_left, (0, current_y))
            self._menu_surface.blit(white_blob, (8, current_y))
            self._menu_surface.blit(white_blob, (16, current_y))
            self._menu_surface.blit(white_blob, (24, current_y))
            self._menu_surface.blit(white_blob, (32, current_y))
            self._menu_surface.blit(white_blob, (40, current_y))
            self._menu_surface.blit(white_blob, (48, current_y))
            self._menu_surface.blit(mid_right, (56, current_y))
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
        self._menu_surface.blit(bottom_mid, (48, current_y))
        self._menu_surface.blit(bottom_right, (56, current_y))

    def _make_menu_text(self):
        """Adds the menu text to the menu"""
        # Create the surface where the text is drawn
        self._text_surface = pygame.Surface((64, 100))
        self._text_surface.fill((255, 255, 255))
        self._text_surface.set_colorkey((255, 255, 255))

        # Grab the appropriate options to display to the player based on thier
        # progress in the game.
        menu_text = []
        if self._player.pokedex is not None:
            menu_text.append("POKeDEX")
        if self._player.has_first_pokemon:
            menu_text.append("POKeMON")
        menu_text += ["BAG", str(self._player.name), "SAVE", "OPTION", "EXIT"]
        self._options = menu_text

        # Display the options.
        current_pos = Vector2(0, 12)
        text_maker = TextMaker(join("fonts", "party_txt_font.png"))
        for text in menu_text:
            current_pos.x = 15
            word_surf = text_maker.get_surface(text)
            self._text_surface.blit(word_surf, (current_pos.x, current_pos.y))
            current_pos.y += 11

    def _make_help_bar(self):
        """Create the blue help bar surface"""
        self._help_surface = pygame.Surface((240, 48))
        self._help_surface.blit(FRAMES.getFrame("blue_help_box.png"), (0, 0))

    def _make_help_text(self, string):
        """Create help text"""
        text_maker = TextMaker(join("fonts", "menu_font.png"), 240)
        self._help_text_surface = pygame.Surface((240, 48))
        self._help_text_surface.fill((190, 190, 112))
        self._help_text_surface.set_colorkey((190, 190, 112))
        word_surf = text_maker.get_surface(string)
        self._help_text_surface.blit(word_surf, (2, 5))


class Cursor(Drawable):
    """Small Cursor class that keeps track of the menu cursor."""
    def __init__(self, max_value):
        """Initialize the cursor. Max_value is the highest possible value the
        cursor can have based on the size of the menu."""
        self._max_value = max_value
        self.cursor = 0
        super().__init__(join("battle", "cursor.png"), (178, 20),
                         world_bound=False)

    def reset(self):
        """Resets the cursor to its initial position."""
        self.cursor = 0
        self._position = (174, 20 + self.cursor * 11)

    def draw(self, draw_surface):
        """Draws the cursor"""
        super().draw(draw_surface)

    def change_cursor_pos(self, action):
        """Changes the cursor pos based on the action provided"""
        if action.key == BattleActions.UP.value:
            if self.cursor > 0:
                self.cursor -= 1
                SoundManager.getInstance().playSound("firered_0005.wav")

        elif action.key == BattleActions.DOWN.value:
            if self.cursor < self._max_value - 1:
                self.cursor += 1
                SoundManager.getInstance().playSound("firered_0005.wav")

        self._position = (178, 20 + self.cursor * 11)
