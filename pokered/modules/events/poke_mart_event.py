import pygame
from os.path import join
from .dialogue import Dialogue
from .response_dialogue import ResponseDialogue
from .menu import Cursor
from ..utils.UI.resizable_menu import ResizableMenu
from ..utils.UI.drawable import Drawable
from ..utils.text_maker import TextMaker
from ..utils.managers.frameManager import FRAMES
from ..utils.misc import end_at
from ..enumerated.battle_actions import BattleActions


class PokeMartEvent():
    def __init__(self, clerk, player):
        self._clerk = clerk
        self._player = player
        self._is_dead = False
        self.turned = True
        self._response_box_cleared = False
        self._response = None  # Response from initial prompt.

        # Create the dialogues used in the event.
        self._initial_prompt = \
            MartResponseDialogue("20", self._player,
                                 self._clerk,
                                 response_string="BUY SELL SEE YA!")
        self._seeya_dialogue = Dialogue("19", self._player, self._clerk)
        self._buy_menu = PokeMartMenu(self._clerk.inventory)

        self._create_money_surface()

        self._help_surface = pygame.Surface((240, 49))
        self._help_surface.blit(FRAMES.getFrame("blue_help_box_b.png"), (0, 0))

    def update(self, ticks):
        """Updates the PokeMart event and all of its sub dialogues/menus. Code
        is organized from first dialouge/menu up to the last in terms of
        chronological order."""
        if not self._initial_prompt.is_over():

            self._initial_prompt.update(ticks)
        elif self._response is None:
            self._response = self._initial_prompt.response
        elif self._response == 2 and not self._seeya_dialogue.is_over():
            self._seeya_dialogue.update(ticks)
        elif self._seeya_dialogue.is_over():
            self._is_dead = True
        elif self._response == 0 and not self._buy_menu.is_over():
            if self.turned:
                self.turned = False
            self._buy_menu.update(ticks)
        elif self._buy_menu.is_over():
            self.turned = False
            self._response = None
            self._initial_prompt = \
                MartResponseDialogue("21", self._player,
                                     self._clerk,
                                     response_string="BUY SELL SEE YA!")
            self._buy_menu = PokeMartMenu(self._clerk.inventory)

    def draw(self, draw_surface):
        """Draws the poke mart menu event based on where the user is in the
        event. Code is ordered from first to last in terms of chrnological
        order."""
        if not self._initial_prompt.is_over():
            self._initial_prompt.draw(draw_surface)
        elif self._response == 2 and not self._seeya_dialogue.is_over():
            self._seeya_dialogue.draw(draw_surface)
        elif self._response == 0 and not self._buy_menu.is_over():
            self._buy_menu.draw(draw_surface)
            draw_surface.blit(self._money_surface, (2, 2))
            draw_surface.blit(self._help_surface, (0, 111))

    def handle_event(self, event):
        """Passes on the event to the active subevent/menu. Code is ordered
        from first to last in terms of chronological order."""
        if not self._initial_prompt.is_over():
            self._initial_prompt.handle_event(event)
        elif self._response == 2 and not self._seeya_dialogue.is_over():
            self._seeya_dialogue.handle_event(event)
        elif self._response == 0 and not self._buy_menu.is_over():
            self._buy_menu.handle_event(event)

    def get_end_event(self):
        """Tells the level manager to return control to the level once the
        event is over."""
        return "Level"

    def is_over(self):
        """Tells when the event is over."""
        return self._is_dead

    def _create_money_surface(self):
        """Create the money surface and blit it to the screen."""
        text_maker = TextMaker(join("fonts", "party_txt_font.png"))
        money_surf = text_maker.get_surface(str(self._player.money))

        # Create money surface and fill it in with transparent color
        self._money_surface = pygame.Surface((76, 36))
        self._money_surface.fill((255, 245, 245))
        self._money_surface.set_colorkey((255, 245, 245))

        menu_frame = FRAMES.getFrame("shop_menu_money.png")
        self._money_surface.blit(menu_frame, (0, 0))
        self._money_surface.blit(money_surf, (20, 10))


class PokeMartMenu(Drawable):
    def __init__(self, inventory):
        """Creates the pokemart menu. Displays the items for sale and their
        prices."""
        super().__init__("shop_menu.png", (80, 1), world_bound=False)
        self._is_dead = False
        self._inventory = inventory
        self._inventory_list = list(self._inventory.keys()) + ["CANCEL"]
        self.draw_cursor = Cursor(6, initial_pos=(88, 13), line_height=16)
        self.item_cursor = Cursor(len(self._inventory_list))
        self.start_item_index = 0
        self.create_item_surface()

    def is_over(self):
        """Tells when the menu is over."""
        return self._is_dead

    def update(self, ticks):
        """Updates the cursor on the poke mart menu."""
        pass

    def draw(self, draw_surface):
        """Draw menu background and print out items for sale and their
        prices."""
        super().draw(draw_surface)
        draw_surface.blit(self._item_surface, (0, 0))
        self.draw_cursor.draw(draw_surface)

    def handle_event(self, event):
        """Handles the events: up, down, and select."""
        if event.type == pygame.KEYDOWN and event.key in \
                [BattleActions.UP.value, BattleActions.DOWN.value]:
            if event.key == BattleActions.UP.value:
                if self.draw_cursor.cursor == 1 and self.item_cursor.cursor != 1:
                    self.start_item_index -= 1
                else:
                    self.draw_cursor.change_cursor_pos(event)
            elif event.key == BattleActions.DOWN.value:
                if self.draw_cursor.cursor == 3 and self.item_cursor.cursor < len(self._inventory_list) - 3:
                    self.start_item_index += 1
                else:
                    self.draw_cursor.change_cursor_pos(event)

            self.item_cursor.change_cursor_pos(event)
            self.create_item_surface()
        elif event.type == pygame.KEYDOWN and event.key == \
                BattleActions.SELECT.value:
            print(self._inventory_list[self.item_cursor.cursor])
            if self._inventory_list[self.item_cursor.cursor] == "CANCEL":
                self._is_dead = True
        elif event.type == pygame.KEYDOWN and event.key == \
                BattleActions.BACK.value:
            self._is_dead = True

    def create_item_surface(self):
        self._item_surface = pygame.Surface((240, 160))
        self._item_surface.fill((255, 255, 254))
        self._item_surface.set_colorkey((255, 255, 254))

        text_maker = TextMaker(join("fonts", "party_txt_font.png"))
        height = 15
        for item in self._inventory_list[self.start_item_index: self.start_item_index + 6]:
            self._item_surface.blit(text_maker.get_surface(item), (97, height))
            if item != "CANCEL":
                price_surf = text_maker.get_surface(str(self._inventory[item]))
                self._item_surface.blit(price_surf, end_at(price_surf, (223, height)))
            height += 16





class MartResponseDialogue(ResponseDialogue):
    """Overrides the Response Dialouge to take into account increased width
    and the different options (Buy, sell, See ya!)"""
    def _blit_response(self):
        self.response_menu = ResizableMenu(3, width=9).menu_surface
        text_maker = TextMaker(join("fonts", "party_txt_font.png"),
                               max=15, line_height=12)
        self.response_menu.blit(text_maker.get_surface("BUY SELL"), (15, 8))
        text_maker._max = 40
        self.response_menu.blit(text_maker.get_surface("SEE YA!"), (15, 32))
        self.cursor = Cursor(3, initial_pos=(7, 8))

    def draw(self, draw_surface):
        Dialogue.draw(self, draw_surface)
        if self.response_menu is not None:
            draw_surface.blit(self.response_menu, (1, 1))
            self.cursor.draw(draw_surface)
