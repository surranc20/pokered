import pygame
from os.path import join
from ...utils.managers.soundManager import SoundManager
from ...utils.managers.frameManager import FRAMES
from ...battle.battle_menus.poke_party import PokeParty, PokemonSelectedMenu
from ...utils.UI.drawable import Drawable
from ...utils.UI.resizable_menu import ResizableMenu
from ...utils.vector2D import Vector2
from ...enumerated.battle_actions import BattleActions
from ...animations.menu_switch import MenuSwitch


class MenuParty(PokeParty):
    def __init__(self, player):
        # Need to keep track of old offset so the game does not awkwardly
        # stutter when leaving the menu.
        self._old_offset = Drawable.WINDOW_OFFSET
        self._switch_queued = None  # Has the player initiated a switch
        self._switch_triggered = None  # Is a switch animation player
        Drawable.WINDOW_OFFSET = Vector2(0, 0)
        super().__init__(player)

    def is_over(self):
        """Needed as part of the general event interface. Cleans up the menu
        if it is over."""
        # If menu is over reset the offset
        if self._is_dead:
            Drawable.WINDOW_OFFSET = self._old_offset
        return self._is_dead

    def set_green_first(self, pokemon_bar):
        """Sets a pokemon bar green when their is an active switch even and
        the pokemon is the first pokemon chosen for the switch event."""
        print("called")
        pygame.transform.threshold(pokemon_bar._image, pokemon_bar._image.copy(), (120, 208, 232), set_color=(120, 216, 128), inverse_set=True)
        pygame.transform.threshold(pokemon_bar._image, pokemon_bar._image.copy(), (168, 232, 248), set_color=(176, 248, 160), inverse_set=True)
        pygame.transform.threshold(pokemon_bar._image, pokemon_bar._image.copy(), (248, 112, 48), set_color=(248, 248, 112), inverse_set=True)

    def set_green_second(self, pokemon_bar):
        """Sets a pokemon bar green but does not change the red outline. This
        happens when their is an active switch event and the pokemon being
        hovered over is not the first pokemon chosen for the switch event"""
        pygame.transform.threshold(pokemon_bar._image, pokemon_bar._image.copy(), (120, 208, 232), set_color=(120, 216, 128), inverse_set=True)
        pygame.transform.threshold(pokemon_bar._image, pokemon_bar._image.copy(), (168, 232, 248), set_color=(176, 248, 160), inverse_set=True)

    def _update_selected_pos(self, old_pos):
        """Toggles the appearance of the selectable objects (active pokmeon,
        secondary pokemon, and cancel button) based on whether or not they are
        selected. Also checks to see if their is an active switch event and
        handles the situation accordingly."""
        if self._cursor == 6:
            self._cancel_button.set_selected()
        else:
            self._selectable_items[self._cursor].set_selected()
            if self._switch_queued is not None:
                print(self._cursor, self._switch_queued)
                if self._cursor == self._switch_queued:
                    print("one")
                    self.set_green_first(self._selectable_items[self._cursor])
                else:
                    print("second")
                    self.set_green_second(self._selectable_items[self._cursor])

        if old_pos == 6:
            self._cancel_button.set_unselected()
        else:
            if self._switch_queued != old_pos:
                self._selectable_items[old_pos].set_unselected()

    def update(self, ticks):
        """Modifies the battle party system to support pokemon switching
        animation."""
        super().update(ticks)
        if self._switch_triggered is not None:
            self._switch_triggered.update(ticks)
            self._selectable_items[self._switch_triggered.slot1_index] = self._switch_triggered.slot1
            self._selectable_items[self._switch_triggered.slot2_index] = self._switch_triggered.slot2

            if self._switch_triggered.is_dead():
                self._switch_triggered = None
                # Redraw the pokemon.
                self._selectable_items = []
                self._blit_active_pokemon()
                self._blit_secondary_pokemon()
                self._selectable_items[0].set_unselected()
                self._selectable_items[self._cursor].set_selected()
                self._switch_queued = None

                self._text_bar.blit_string("Choose a POKeMON.")

    def handle_event(self, event):
        """Overrides the PokeParty events handling system
        to make it compatible with normal events"""
        # The player should not be able to do anything during a switch
        # animation.
        if self._switch_triggered:
            return
        if event.key in [BattleActions.UP.value, BattleActions.DOWN.value,
                         BattleActions.LEFT.value, BattleActions.RIGHT.value]:
            super().change_cursor_pos(event)

        elif event.key == BattleActions.BACK.value:
            # This needs to be rewritten
            if self._selected_pokemon:
                self._selected_pokemon = False
                self._pokemon_selected_menu = None
                self._text_bar.blit_string("Choose a POKeMON.")
            else:
                self._is_dead = True

        elif event.key == BattleActions.SELECT.value:
            # This needs to be rewritten as well
            if self._cursor == 6:
                self._is_dead = True
            else:
                # Check to see if the player is in the middle of switching
                # pokemon positions.
                if self._switch_queued is not None:
                    if self._cursor == self._switch_queued:
                        pass # Maybe do something here?
                    else:
                        # Switch the pokemon out.
                        poke1 = self._player.pokemon_team[self._cursor]
                        poke2 = self._player.pokemon_team[self._switch_queued]
                        self._player.pokemon_team[self._cursor] = poke2
                        self._player.pokemon_team[self._switch_queued] = poke1
                        if self._cursor == 0 or self._switch_queued == 0:
                            self._player.set_active_pokemon(0)

                        # Start the switch animation.
                        self._switch_triggered = MenuSwitch(self._selectable_items[self._cursor], self._cursor, self._selectable_items[self._switch_queued], self._switch_queued)

                # If a pokemon has not been selected then select the pokmeon
                elif not self._selected_pokemon:
                    self._selected_pokemon = True
                    self._pokemon_selected_menu = \
                        MenuPokemonSelectedMenu(self._player, self._cursor,
                                                battle=False)
                    self._text_bar.blit_string("Do what with this PKMN?")

                else:
                    response = self._pokemon_selected_menu.handle_event(event)
                    if response == "cancel":
                        self._selected_pokemon = False
                        self._pokemon_selected_menu = None
                        self._text_bar.blit_string("Choose a POKeMON.")
                    elif response == "switch":
                        self._pokemon_selected_menu = None
                        self._selected_pokemon = False
                        self._text_bar.blit_string("Move to where?")
                        self._switch_queued = self._cursor
                        self.set_green_first(self._selectable_items[self._switch_queued])
                        print("down here")


class MenuPokemonSelectedMenu(PokemonSelectedMenu):
    def __init__(self, player, selected_pos, battle=False):
        super().__init__(player, selected_pos, False)
        self._menu_surface = ResizableMenu(self._num_lines)
        self._position = (self._position[0], self._position[1] - (self._menu_surface.size - 6) * 8)

    def _handle_select_event(self):
        """Handles a select event for the selected pokemon menu."""
        SoundManager.getInstance().playSound("firered_0005.wav")
        # If the cancel button is selected then cancel
        if self._cursor == self._num_lines - 1:
            return "cancel"

        # If the summary button is selected then get summary NOTE: This is
        # not implemented yet.
        elif self._cursor == 0:
            return  # summary

        # Switch button is selected
        elif self._cursor == self._num_lines - 3:
            return "switch"

        elif self._cursor == self._num_lines - 2:
            return "item"

    def blit_text(self):
        """Overwrite blit text to correctly display out of battle options"""
        lines = ["SUMMARY"]
        self._hms = 0
        # Find all moves that can be used outside of battle
        for move in self._player.pokemon_team[self._selected_pos].moves:
            if move.outside_battle:
                lines.append(move.move_name.upper())
                self._hms += 1
        lines += ["SWITCH", "ITEM", "CANCEL"]

        self._txt = pygame.Surface((160, 120))
        self._txt.fill((255, 255, 255))
        self._txt.set_colorkey((255, 255, 255))
        current_pos = Vector2(15, 7)
        for line in lines:
            for char in line:
                if char != " ":
                    font_index = int(ord(char)) - 65
                    font_char = FRAMES.getFrame(join("fonts", "party_txt_font.png"),
                                                offset=(font_index, 0))
                    font_char.set_colorkey((255, 255, 255))
                    self._txt.blit(font_char, (current_pos.x, current_pos.y))

                    # The I character is particularly small so add an extra
                    # space.
                    if char != "I":
                        current_pos.x += 5
                    else:
                        current_pos.x += 4
                else:
                    current_pos.x += 2
            current_pos.y += 12
            current_pos.x = 15
        self._num_lines = len(lines)


