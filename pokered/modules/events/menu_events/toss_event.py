import pygame
from os.path import join
from ...utils.cursor import Cursor
from ...utils.UI.resizable_menu import ResizableMenu
from ...utils.UI.quantity_cursor import QuantityCursor
from ...enumerated.battle_actions import BattleActions
from ...utils.text_maker import TextMaker
from ...utils.managers.frameManager import FRAMES


class TossEvent():
    def __init__(self, item, player):
        """Creates a toss event which occurs whenever a player decides they
        want to toss out an item."""
        self.item = item
        self.player = player
        self.is_dead = False
        self.quantity_cursor = QuantityCursor((199, 119))
        self.menu_frame = ResizableMenu(3).menu_surface
        self._create_how_many_surface()

        self.num_selected = 1
        self.max_toss = player.bag[item.type][item]

        # Phases used throughout the event.
        # Note: These are not actual dialogue classes because the original
        # game does not treat them like normal dialogues.
        self.confirm_toss_response_dialogue = None
        self.threw_away_dialogue = None

        # This is the response from the confirm toss dialogue. Soley used to
        # check if it is not None (the user has answered the confirm toss
        # dialogue)
        self.confirmed_response = None

    def draw(self, draw_surface):
        """Draws the toss event."""

        # The menu frame and how many surf (frame that appears in the middle
        # of the bottom of the screen).
        draw_surface.blit(self.menu_frame, (176, 112))
        draw_surface.blit(self.how_many_surf, (40, 115))

        if self.confirm_toss_response_dialogue is None and \
                self.threw_away_dialogue is None:
            self.quantity_cursor.draw(draw_surface)

        # If on the trow away dialogue we don't need to draw anything else (it
        # is taken care of in the how many surf). Return so that cursor and
        # yes no surf are not drawn.
        if self.threw_away_dialogue is not None:
            return

        elif self.confirm_toss_response_dialogue is not None:
            draw_surface.blit(self.yes_no_surf, (195, 127))
            self.cursor.draw(draw_surface)

    def handle_event(self, event):
        """Updates the count displayed in the quanity cursor based on input.
        If the user hits select then..."""
        if self.threw_away_dialogue is not None:
            if event.key == BattleActions.SELECT.value:
                self.is_dead = True
                self.player.bag.subtract_item(self.item, self.num_selected)
        elif self.confirm_toss_response_dialogue is not None:
            if event.key in [BattleActions.UP.value,
                             BattleActions.DOWN.value]:
                self.cursor.change_cursor_pos(event)
            elif event.key == BattleActions.SELECT.value:
                self.confirmed_response = "Yes" if self.cursor.cursor == 0 \
                    else "No"
                self.threw_away_dialogue = True
                self._create_how_many_surface(dialogue_type="tossed")
                if self.confirmed_response == "No":
                    self.is_dead = True
            return

        if event.key == BattleActions.UP.value:
            if self.num_selected < self.max_toss:
                self.num_selected += 1
                self.quantity_cursor.change_count(self.num_selected)
            elif self.num_selected == self.max_toss:
                self.num_selected = 1
                self.quantity_cursor.change_count(self.num_selected)
        elif event.key == BattleActions.DOWN.value:
            if self.num_selected > 1:
                self.num_selected -= 1
                self.quantity_cursor.change_count(self.num_selected)
            elif self.num_selected == 1:
                self.num_selected = self.max_toss
                self.quantity_cursor.change_count(self.num_selected)
        elif event.key == BattleActions.SELECT.value:
            if self.confirm_toss_response_dialogue is None:
                self.confirm_toss_response_dialogue = True
                self._create_how_many_surface(dialogue_type="confirm")
                self._create_yes_no()
                self.cursor = Cursor(2, initial_pos=(187, 125))

    def update(self, ticks):
        """Updates the quantity cursor."""
        self.quantity_cursor.update(ticks)

    def _create_how_many_surface(self, dialogue_type="how many"):
        """Creates a surface which asks how many of an item the user wishes to
        toss."""
        text_maker = TextMaker(join("fonts", "party_txt_font.png"), max=100)

        # If the type is tossed then we need a wider bag item selected.
        if dialogue_type == "tossed":
            background_frame = FRAMES.getFrame("bag_item_selected_full.png")
        else:
            background_frame = FRAMES.getFrame("bag_item_selected.png")

        # Create a blank transparent surface where text surface will be
        # blitted.
        self.how_many_surf = \
            pygame.Surface((background_frame.get_size()))
        self.how_many_surf.fill((255, 255, 254))
        self.how_many_surf.set_colorkey((255, 255, 254))
        self.how_many_surf.blit(background_frame, (0, 0))

        # Get text surface.
        if dialogue_type == "how many":
            text_surf = \
                text_maker.get_surface((f'Toss out how many '
                                       f'{self.item.name.upper()}s?'))
        elif dialogue_type == "confirm":
            text_surf = \
                text_maker.get_surface((f'Throw away {self.num_selected} '
                                       f'of this item?'))
        elif dialogue_type == "tossed":
            text_surf = \
                text_maker.get_surface((f'Threw away {self.num_selected} '
                                       f'{self.item.name.upper()}s.'))
        self.how_many_surf.blit(text_surf, (8, 10))

    def _create_yes_no(self):
        """Creates the yes no surface."""
        text_maker = TextMaker(join("fonts", "party_txt_font.png"), max=15)
        self.yes_no_surf = text_maker.get_surface("YES NO")

    def is_over(self):
        """Returns whether or not the toss event is over."""
        return self.is_dead
