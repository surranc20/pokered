import pygame
from os.path import join
from .menu_events.menu_party import MenuParty
from .menu_events.bag import Bag
from ..enumerated.battle_actions import BattleActions
from ..utils.vector2D import Vector2
from ..utils.text_maker import TextMaker
from ..utils.managers.frameManager import FRAMES
from ..utils.UI.resizable_menu import ResizableMenu
from ..utils.managers.soundManager import SoundManager
from ..utils.cursor import Cursor

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
        "POKéMON": "Check and organize POKéMON that are traveling with you in "
        "your party.",
        "POKéDEX": "A device that records POKéMON secrets upon meeting them "
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
        self._active_sub_menu = None
        self._level_surface = None

    def add_level_surface(self, level_surface):
        self._level_surface = level_surface

    def draw(self, draw_surface):
        """Draws the menu."""
        if self._active_sub_menu is None:
            self._level_surface.draw(draw_surface)
            draw_surface.blit(self._menu_surface, (172, 10))
            draw_surface.blit(self._text_surface, (172, 10))
            draw_surface.blit(self._help_surface, (0, 122))
            draw_surface.blit(self._help_text_surface, (0, 122))
            self._cursor.draw(draw_surface)
        else:
            self._active_sub_menu.draw(draw_surface)

    def update(self, ticks):
        """Updates the menu."""
        if self._save_queued:
            return "Pickle"

        if self._active_sub_menu is not None:
            self._active_sub_menu.update(ticks)
            if self._active_sub_menu.is_over():
                self._active_sub_menu = None

    def handle_event(self, event):
        """Handles the inputs and updates menu accordingly."""
        if self._active_sub_menu is None:
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
                else:
                    self._active_sub_menu = \
                        self.create_sub_event(current_selected)

            # Back action.
            elif event.type == pygame.KEYDOWN and \
                    event.key == BattleActions.BACK.value:
                self._is_over = True

        else:
            if event.type == pygame.KEYDOWN:
                self._active_sub_menu.handle_event(event)

    def is_over(self):
        """Determines whether or not the menu is closed."""
        return self._is_over

    def get_end_event(self):
        """Returns the player back to the level."""
        return "Level"

    def create_sub_event(self, event_name):
        """Creates the menu sub event"""
        # TODO: ADD EVENTS
        if event_name == "BAG":
            return Bag(self._player)
        elif event_name == "SAVE":
            return None
        elif event_name == "OPTION":
            return None
        elif event_name == "POKéMON":
            return MenuParty(self._player)
        elif event_name == "POKéDEX":
            return None
        elif event_name == str(self._player.name):
            return None

    def _get_help_text(self):
        """Returns the appropriate help text given the selected menu item"""
        current_selected = self._options[self._cursor.cursor]
        if current_selected == str(self._player.name):
            current_selected = "PLAYER"
        return self.HELP_TEXT[current_selected]

    def _make_menu(self):
        """Creates the menu image."""
        # Look at the players progress and see which menu items should be
        # displayed given their progress in the game. (i.e has player received
        # their first pokemon yet...)
        size = 5
        if self._player.pokedex is not None:
            size += 1
        if self._player.has_first_pokemon:
            size += 1
        self._menu_surface = ResizableMenu(size).menu_surface

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
            menu_text.append("POKéDEX")
        if self._player.has_first_pokemon:
            menu_text.append("POKéMON")
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
