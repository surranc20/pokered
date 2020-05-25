from os.path import join
from .dialogue import Dialogue
from .response_dialogue import ResponseDialogue
from .menu import Cursor
from ..utils.UI.resizable_menu import ResizableMenu
from ..utils.UI.drawable import Drawable
from ..utils.text_maker import TextMaker


class PokeMartEvent():
    def __init__(self, clerk, player):
        self._clerk = clerk
        self._player = player
        self._is_dead = False
        self._response = None  # Response from initial prompt.

        # Create the dialogues used in the event.
        self._initial_prompt = \
            MartResponseDialogue("20", self._player,
                                 self._clerk,
                                 response_string="BUY SELL SEE YA!")
        self._seeya_dialogue = Dialogue("19", self._player, self._clerk)
        self._buy_menu = PokeMartMenu(self._clerk.inventory)

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
        elif self._response == 0 and not self._buy_menu.is_over():
            self._buy_menu.update(ticks)

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


class PokeMartMenu(Drawable):
    def __init__(self, inventory):
        """Creates the pokemart menu. Displays the items for sale and their
        prices."""
        super().__init__("shop_menu.png", (40, 2), world_bound=False)
        self._inventory = inventory

    def is_over(self):
        """Tells when the menu is over."""
        return False

    def update(self, ticks):
        """Updates the cursor on the poke mart menu."""
        pass

    def handle_event(self, event):
        """Handles the events: up, down, and select."""
        pass


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