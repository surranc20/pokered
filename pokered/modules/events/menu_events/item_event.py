from ..response_box import ResponseBox
from .give_event import GiveEventFromMenu


class ItemEvent():
    """Event that triggers when the user presses item in the pokmeon menu.
    Asks the user if they want to give or take an item. If they want to give
    an item, then it passes control to the GiveEventFromMenu which wraps the
    GiveEventHandler from GiveEvent and allows the player to select which item
    they want to give."""
    def __init__(self, pokemon, player):
        self.pokemon = pokemon
        self.player = player

        self.display_pokemon_menu = True

        self.sub_event = None
        self.is_dead = False

        self.response_box = ResponseBox(["GIVE", "TAKE", "CANCEL"], (240, 159),
                                        end_at=True, dy=-2)

    def draw(self, draw_surface):
        """Draws the response box at the beginning of the event and draws the
        active sub event after it exists."""
        if self.sub_event is not None:
            self.sub_event.draw(draw_surface)
        else:
            self.response_box.draw(draw_surface)

    def update(self, ticks):
        """Updates the active sub event if it exists."""
        if self.sub_event is not None:
            self.sub_event.update(ticks)
            self.display_pokemon_menu = self.sub_event.display_pokemon_menu
            if self.sub_event.is_dead:
                self.is_dead = True

    def handle_event(self, event):
        """If their is an active sub event then pass control to that,
        otherwise allow the response box to handle events."""
        if self.sub_event is not None:
            self.sub_event.handle_event(event)
            return

        self.response_box.handle_event(event)

        # If the user pressed select then the response box will die. Use this
        # response to determine what to do next.
        if self.response_box.is_dead:
            # This means they want to give an item.
            if self.response_box.response == 0:
                self.display_pokemon_menu = False
                self.sub_event = GiveEventFromMenu(self.pokemon, self.player)

            # This means they want to take an item.
            elif self.response_box.response == 1:
                pass

            # This is cancel.
            elif self.response_box.response == 2:
                self.is_dead = True
                return

    def is_over(self):
        """Returns whether or not the item event is complete."""
        return self.is_dead
