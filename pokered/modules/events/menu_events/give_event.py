from os.path import join
from .menu_party import MenuParty
from .bag import Bag
from ..dialogue import Dialogue
from ...utils.UI.drawable import Drawable
from ...enumerated.battle_actions import BattleActions
from ...utils.UI.resizable_menu import ResizableMenu
from ...utils.text_maker import TextMaker
from ...utils.UI.text_cursor import TextCursor
from ..response_box import ResponseBox
from ...enumerated.item_types import ItemTypes


class GiveEvent(MenuParty):
    """Event which is created when the player presses give from the bag. Takes
    the player through the process of giving an item to a pokemon. If the
    player presses give from the pokemon menu then this stage of the event is
    skipped and will go straight to the GiveEventHandler. Extends MenuParty to
    display the pokemon menu when the user is deciding who to give the item
    to."""
    def __init__(self, item, player):
        # Need to keep track of the offset going into the event because
        # MenuParty messes up the offset and if we do not reset at the end of
        # the GiveEvent then the game will hitch for one frame when returning
        # to the overworld.
        self._old_offset = Drawable.WINDOW_OFFSET

        super().__init__(player)
        self.item = item
        self.player = player
        self.is_dead = False

        self._text_bar.blit_string("Give item to whom?")
        self.give_event_handler = None

    def draw(self, draw_surface):
        """Always draw the pokemon menu. Additionally, if the player has
        initiated the giving process then also draw the handler."""
        super().draw(draw_surface)
        if self.give_event_handler is not None:
            self.give_event_handler.draw(draw_surface)

    def handle_event(self, event):
        """If player has not yet pressed a pokemon or cancel then move cursor
        around menu. Otherwise, pass event to give handler."""
        if self.give_event_handler is not None:
            self.give_event_handler.handle_event(event)

        elif event.key in [BattleActions.UP.value,
                           BattleActions.DOWN.value,
                           BattleActions.LEFT.value,
                           BattleActions.RIGHT.value]:
            self.change_cursor_pos(event)

        elif event.key == BattleActions.SELECT.value:
            # Player pressed CANCEL so end event.
            if self._cursor == 6:
                self.is_dead = True

            # Player selected a pokemon. Create GiveEventHandler.
            else:
                pokemon = self.player.pokemon_team[self._cursor]
                self.give_event_handler = GiveEventHandler(pokemon, self.item,
                                                           self.player.bag)

    def update(self, ticks):
        """Calls super to animate bouncing pokemon and passes control to
        handler if it is not none."""
        super().update(ticks)
        if self.give_event_handler is not None:
            self.give_event_handler.update(ticks)
            if self.give_event_handler.is_dead:
                self.is_dead = True

    def is_over(self):
        """Tells the Bag whether or not the event is over."""
        # If menu is over reset the offset
        if self.is_dead:
            Drawable.WINDOW_OFFSET = self._old_offset
        return self.is_dead


class GiveEventFromMenu(Bag):
    def __init__(self, pokemon, player):
        super().__init__(player)
        self.pokemon = pokemon
        self.player = player
        self.active_give_event = None
        self.display_pokemon_menu = False

    def draw(self, draw_surface):
        if self.active_give_event is None:
            super().draw(draw_surface)
        else:
            self.active_give_event.draw(draw_surface)

    def handle_event(self, event):
        if self.active_give_event is None:
            super().handle_event(event)
        else:
            self.active_give_event.handle_event(event)

    def update(self, ticks):
        if self.active_give_event is None:
            super().update(ticks)
        else:
            self.active_give_event.update(ticks)
            if self.active_give_event.is_dead:
                self.is_dead = True

    def _handle_select_event(self):
        selected_item = self.item_list[self.item_cursor.cursor]
        if selected_item == "CANCEL":
            self.is_dead = True
        else:
            if selected_item.type == ItemTypes.KEY_ITEMS:
                self.do_what_response_menu = Dialogue("27", self.player, self.player, replace=[selected_item.name.upper()])
            else:
                self.display_pokemon_menu = True
                self.active_give_event = GiveEventHandler(self.pokemon, selected_item, self.player.bag)


class GiveEventHandler():
    """If selecting give from the pokemon menu then come straight here.
    Decides if pokmeon is currently holding and then passes control to the
    correct sub event."""
    def __init__(self, pokemon, item, bag):
        self.is_dead = False

        if pokemon.held_item is None:
            self.give_sub_event = NoItemGiveSubEvent(pokemon, item, bag)
        else:
            self.give_sub_event = HasItemGiveSubEvent(pokemon, item, bag)

    def handle_event(self, event):
        """Pass control to sub event."""
        self.give_sub_event.handle_event(event)

    def draw(self, draw_surface):
        """Pass control to sub event."""
        self.give_sub_event.draw(draw_surface)

    def update(self, ticks):
        """Pass control to sub event. Detect if sub event is over, if it is
        then the handler itself is done."""
        self.give_sub_event.update(ticks)
        if self.give_sub_event.is_dead:
            self.is_dead = True


class SubEvent():
    """Base class for the following sub events. Creates the background text
    frame and blits the given string to said frame."""
    def __init__(self, pokemon, item, bag, first_string):
        self.is_dead = False
        self.pokemon = pokemon
        self.item = item
        self.bag = bag

        # Create the background frame and blit string to it.
        self.background_frame = ResizableMenu(2, width=30).menu_surface
        self.text_maker = TextMaker(join("fonts", "party_txt_font.png"),
                                    max=180)
        self.text_surf = \
            self.text_maker.get_surface(first_string)
        self.background_frame.blit(self.text_surf, (9, 9))

    def draw(self, draw_surface):
        """Draw the background frame (which has string)."""
        draw_surface.blit(self.background_frame, (0, 120))

    def update(self, ticks):
        """Can be overwritten if necessary."""
        pass

    def handle_event(self, event):
        """Can be overwritten if necessary."""
        pass


class NoItemGiveSubEvent(SubEvent):
    """Handles the giving process if the pokemon is not currently holding an
    item. Simply display the one dialogue and end after the user presses
    select."""
    def __init__(self, pokemon, item, bag):
        first_string = (f'{pokemon.nick_name.upper()} was given the '
                        f'{item.name.upper()} to hold.')
        super().__init__(pokemon, item, bag, first_string)

    def handle_event(self, event):
        """Once the user presses select give the pokemon the item and end the
        sub event."""
        if event.key == BattleActions.SELECT.value:
            self.pokemon.held_item = self.item
            self.bag.subtract_item(self.item)
            self.is_dead = True


class HasItemGiveSubEvent(SubEvent):
    """Entry sub event for if the pokemon is holding an item. Notify the user
    of this act and then pass control to propose question which asks if they
    still want to switch items."""
    def __init__(self, pokemon, item, bag):
        first_string = (f'{pokemon.nick_name.upper()} is already holding '
                        f'one {item.name.upper()}.')
        super().__init__(pokemon, item, bag, first_string)

        # This event has a cursor that bobs up and down to make sure the user
        # knows that they need to press select.
        self.text_cursor = TextCursor(self.get_cursor_pos())
        self.text_cursor.activate()
        self.sub_event = None

    def draw(self, draw_surface):
        """Draw parent and either the sub event (if it exists) or the text
        cursor."""
        super().draw(draw_surface)
        if self.sub_event is not None:
            self.sub_event.draw(draw_surface)
        else:
            self.text_cursor.draw(draw_surface)

    def update(self, ticks):
        """Update the parent and either the sub event (if it exists) or the
        text cursor."""
        super().update(ticks)
        if self.sub_event is not None:
            self.sub_event.update(ticks)
            if self.sub_event.is_dead:
                self.is_dead = True
        else:
            self.text_cursor.update(ticks)

    def handle_event(self, event):
        """Once the user presses control for the first time create the
        ProposeQuestion sub event. Then pass control to that."""
        if self.sub_event is not None:
            self.sub_event.handle_event(event)
            return  # Return instead of if else to save from indentation.

        if event.key == BattleActions.SELECT.value:
            self.sub_event = ProposeQuestion(self.pokemon, self.item, self.bag)

    def get_cursor_pos(self):
        """Returns the position for the text cursor. Uses the ending position
        for the surface created by the text maker and adds the offset (9, 128)
        to said position. Why this offset? The 9 comes from wanting the cursor
        to appear 9 pixels to the right of the last word. The 128 is
        calculated from two parts 120 and 8. 120 comes from the fact that the
        background text frame appears 120 pixels down the screen. The 8 comes
        from the fact that the dialogue itself is blitted 9 pixels down into
        said background frame (I put it one higher because I thought it looked
        better)."""
        return (self.text_maker.pos[0] + 9, self.text_maker.pos[1] + 120 + 8)


class ProposeQuestion(SubEvent):
    """Asks the user if they want to go through with the item switch and acts
    accordingly."""
    def __init__(self, pokemon, item, bag):
        first_string = (f'Would you like to switch the two items?')
        super().__init__(pokemon, item, bag, first_string)
        self.response_box = ResponseBox(["YES", "NO"], (130, 80))

        self.sub_event = None

    def draw(self, draw_surface):
        """If the user has not responded yet then keep drawing the response
        box. Otherwise draw the active sub event."""
        if self.sub_event is not None:
            self.sub_event.draw(draw_surface)
        else:
            super().draw(draw_surface)
            self.response_box.draw(draw_surface)

    def handle_event(self, event):
        """If the user has not responded yet then pass control of events to
        the response box otherwise pass control to the active sub event."""
        if self.sub_event is not None:
            self.sub_event.handle_event(event)
            return

        elif not self.response_box.is_dead:
            self.response_box.handle_event(event)

    def update(self, ticks):
        """Once the user has responded create the sub event that correlates to
        said response. Once that subevent is over then the whole event is
        over."""
        if self.sub_event is not None:
            self.sub_event.update(ticks)
            if self.sub_event.is_dead:
                self.is_dead = True

        # Get response from user and act accordingly.
        elif self.response_box.is_dead:

            # User said they did not want to switch.
            if self.response_box.response == 1:
                self.is_dead = True
                return

            # They do want to switch.
            num_held = self.bag[self.item.type].get(self.item)
            if num_held is not None and num_held == 999:
                self.sub_event = NoRoomSubEvent(self.pokemon, self.item,
                                                self.bag)
            else:
                self.sub_event = HasRoomSubEvent(self.pokemon, self.item,
                                                 self.bag)


class NoRoomSubEvent(SubEvent):
    """This sub event is triggered when the player wants to switch but they
    don't have any room in their bag."""
    def __init__(self, pokemon, item, bag):
        first_string = (f"The BAG is full. The POKéMON's item could not be "
                        f'removed.')
        super().__init__(pokemon, item, bag, first_string)

    def handle_event(self, event):
        """Once the user presses select the event is over."""
        if event.key == BattleActions.SELECT.value:
            self.is_dead = True


class HasRoomSubEvent(SubEvent):
    """This sub event is triggered when the player does have room in their bag
    to perform the switch."""
    def __init__(self, pokemon, item, bag):
        first_string = (f'The {pokemon.held_item.name.upper()} was taken and '
                        f'replaced with the {item.name.upper()}.')
        super().__init__(pokemon, item, bag, first_string)

    def handle_event(self, event):
        """Once the user presses select the event is over and the switch is
        performed."""
        if event.key == BattleActions.SELECT.value:
            prev_item = self.pokemon.held_item
            self.pokemon.held_item = self.item
            self.bag.subtract_item(self.item)
            self.bag.add_item(prev_item)
            self.is_dead = True
