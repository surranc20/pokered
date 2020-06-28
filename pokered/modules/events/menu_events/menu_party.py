import pygame
from ...battle.battle_menus.poke_party import PokeParty, PokemonSelectedMenu
from ...utils.UI.drawable import Drawable
from ...utils.vector2D import Vector2
from ...enumerated.battle_actions import BattleActions
from ...animations.menu_switch import MenuSwitch
from .summary_menu import SummaryMenu
from ..response_box import ResponseBox


class MenuParty(PokeParty):
    def __init__(self, player):
        # Need to keep track of old offset so the game does not awkwardly
        # stutter when leaving the menu.
        self._old_offset = Drawable.WINDOW_OFFSET
        self._switch_queued = None  # Has the player initiated a switch
        self._switch_triggered = None  # Is a switch animation player
        self._summary_active = None  # Is a summary menu active?
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
        pygame.transform.threshold(pokemon_bar._image,
                                   pokemon_bar._image.copy(),
                                   (120, 208, 232),
                                   set_color=(120, 216, 128), inverse_set=True)
        pygame.transform.threshold(pokemon_bar._image,
                                   pokemon_bar._image.copy(),
                                   (168, 232, 248),
                                   set_color=(176, 248, 160), inverse_set=True)
        pygame.transform.threshold(pokemon_bar._image,
                                   pokemon_bar._image.copy(),
                                   (248, 112, 48),
                                   set_color=(248, 248, 112), inverse_set=True)

    def set_green_second(self, pokemon_bar):
        """Sets a pokemon bar green but does not change the red outline. This
        happens when their is an active switch event and the pokemon being
        hovered over is not the first pokemon chosen for the switch event"""
        pygame.transform.threshold(pokemon_bar._image,
                                   pokemon_bar._image.copy(),
                                   (120, 208, 232),
                                   set_color=(120, 216, 128), inverse_set=True)
        pygame.transform.threshold(pokemon_bar._image,
                                   pokemon_bar._image.copy(),
                                   (168, 232, 248),
                                   set_color=(176, 248, 160), inverse_set=True)

    def _update_selected_pos(self, old_pos):
        """Toggles the appearance of the selectable objects (active pokmeon,
        secondary pokemon, and cancel button) based on whether or not they are
        selected. Also checks to see if their is an active switch event and
        handles the situation accordingly."""
        if self._cursor == 6:
            self._cancel_button.set_selected()
        else:
            if self._cursor != self._switch_queued:
                self._selectable_items[self._cursor].set_selected()
            if self._switch_queued is not None:
                if self._cursor == self._switch_queued:
                    self.set_green_first(self._selectable_items[self._cursor])
                else:
                    self.set_green_second(self._selectable_items[self._cursor])

        if old_pos == 6:
            self._cancel_button.set_unselected()
        else:
            if self._switch_queued != old_pos and old_pos != 6:
                self._selectable_items[old_pos].set_unselected()

    def update(self, ticks):
        """Modifies the battle party system to support pokemon switching
        animation."""

        # If the summary menu is active then update that instead.
        if self._summary_active is not None:
            if not self._summary_active.is_over():

                # If sub event is item event then sometimes the pokemon menu
                # itself needs to be updated as well.
                if self._should_display_pokemon_menu():
                    super().update(ticks)

                return self._summary_active.update(ticks)
            else:
                self._summary_active = None
                self._text_bar.blit_string("Choose a POKeMON.")

        super().update(ticks)
        if self._switch_triggered is not None:
            self._switch_triggered.update(ticks)

            # Get the updated pokemon bars from the bar animation.
            self._selectable_items[self._switch_triggered.slot1_index] = \
                self._switch_triggered.slot1
            self._selectable_items[self._switch_triggered.slot2_index] = \
                self._switch_triggered.slot2

            # Clean up after the animation is done.
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
        # If the summary is active then let that handle the event.
        if self._summary_active is not None:
            return self._summary_active.handle_event(event)

        # The player should not be able to do anything during a switch
        # animation.
        if self._switch_triggered:
            return
        if event.key in [BattleActions.UP.value, BattleActions.DOWN.value,
                         BattleActions.LEFT.value, BattleActions.RIGHT.value]:
            super().change_cursor_pos(event)

        elif event.key == BattleActions.BACK.value:
            if self._selected_pokemon:
                self._selected_pokemon = False
                self._pokemon_selected_menu = None
                self._text_bar.blit_string("Choose a POKeMON.")
            else:
                self._is_dead = True

        elif event.key == BattleActions.SELECT.value:
            # The player hit the cancel button so the menu is over.
            if self._cursor == 6:
                self._is_dead = True
            else:
                # Check to see if the player is in the middle of switching.
                # pokemon positions.
                if self._switch_queued is not None:
                    if self._cursor == self._switch_queued:
                        pass  # Maybe do something here?
                    else:
                        # Switch the pokemon out.
                        poke1 = self._player.pokemon_team[self._cursor]
                        poke2 = self._player.pokemon_team[self._switch_queued]
                        self._player.pokemon_team[self._cursor] = poke2
                        self._player.pokemon_team[self._switch_queued] = poke1
                        if self._cursor == 0 or self._switch_queued == 0:
                            self._player.set_active_pokemon(0)

                        # Start the switch animation.
                        self._switch_triggered = \
                            MenuSwitch(self._selectable_items[self._cursor],
                                       self._cursor,
                                       self._selectable_items[self._switch_queued],
                                       self._switch_queued)

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
                    elif response == "summary":
                        self._summary_active = SummaryMenu(self._player,
                                                           self._cursor)
                    elif response == "item":
                        from .item_event import ItemEvent
                        self._text_bar.blit_string("Do what with an item?")
                        self._summary_active = ItemEvent(self._player.pokemon_team[self._cursor], self._player)
                        self._pokemon_selected_menu = None
                        self._selected_pokemon = False

    def draw(self, draw_surface):
        if self._summary_active is not None:
            # If sub event is item event then sometimes the pokemon menu
            # itself needs to be drawn as well.
            if self._should_display_pokemon_menu():
                super().draw(draw_surface)
            self._summary_active.draw(draw_surface)
        else:
            super().draw(draw_surface)

    def _should_display_pokemon_menu(self):
        """Not using duck typing here because I expect this function to return
        False the majority of the time. This means the try catch would fail
        much more often than not."""
        from .item_event import ItemEvent
        if type(self._summary_active) is ItemEvent:
            if self._summary_active.display_pokemon_menu:
                return True
        return False


class MenuPokemonSelectedMenu(PokemonSelectedMenu):
    def __init__(self, player, selected_pos, battle=False):
        """Overrides pokemon selected menu to include switch and the
        possibility of HM moves."""
        super().__init__(player, selected_pos, False)

    def _handle_option_selected(self):
        """Handles a select event for the selected pokemon menu."""
        # If the cancel button is selected then cancel
        response = self.response_box.response
        max_value = self.response_box.cursor._max_value - 1

        if response == max_value:
            return "cancel"

        # If the summary button is selected then get summary NOTE: This is
        # not implemented yet.
        elif response == 0:
            return "summary"

        # Switch button is selected
        elif response == max_value - 2:
            return "switch"

        elif response == max_value - 1:
            return "item"

    def _create_response_box(self):
        """Overwrite blit text to correctly display out of battle options"""
        lines = ["SUMMARY"]
        self._hms = 0
        # Find all moves that can be used outside of battle
        for move in self._player.pokemon_team[self._selected_pos].moves:
            if move.outside_battle:
                lines.append(move.move_name.upper())
                self._hms += 1
        lines += ["SWITCH", "ITEM", "CANCEL"]

        self.response_box = ResponseBox(lines, (240, 159), end_at=True)
