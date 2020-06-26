import pygame
from os.path import join
from .menu_party import MenuParty
from ..poke_mart_event import QuantityCursor
from ...utils.misc import end_at
from ...utils.cursor import Cursor
from ...utils.text_maker import TextMaker
from ...utils.managers.frameManager import FRAMES
from ...utils.UI.text_cursor import TextCursor
from ...utils.UI.resizable_menu import ResizableMenu
from ...utils.UI.drawable import Drawable
from ...enumerated.battle_actions import BattleActions
from ...enumerated.item_types import ItemTypes

from ..response_box import ResponseBox


class Bag():
    """The bag menu from the game."""
    def __init__(self, player):
        self.player = player
        self.is_dead = False
        self.background_surf = FRAMES.getFrame("bag_background.png")
        self.bag_index = 1
        self.start_item_index = 0

        self.update_bag_info()
        self.create_cursors()

        self.do_what_response_menu = None
        self.do_what_response = None

    def is_over(self):
        """Returns whether or not the bag has been exited."""
        return self.is_dead

    def update(self, ticks):
        """Updates the bag."""
        self.up_bobbing_cursor.update(ticks)
        self.down_bobbing_cursor.update(ticks)
        self.right_bobbing_cursor.update(ticks)
        self.left_bobbing_cursor.update(ticks)

        if self.do_what_response_menu is not None:
            self.do_what_response_menu.update(ticks)
            if self.do_what_response_menu.is_over():
                self.do_what_response = self.do_what_response_menu.response
                self.do_what_response_menu = None
                self.create_items_surface()

    def handle_event(self, event):
        """Handles event."""
        if self.do_what_response_menu is not None:
            self.do_what_response_menu.handle_event(event)
            return

        if event.type == pygame.KEYDOWN:
            # When going left and right change bag open and reset cursors.
            if event.key == BattleActions.RIGHT.value:
                if self.bag_index < 2:
                    self.bag_index += 1
                    self.update_bag_info()
                    self.create_cursors()
                    self.start_item_index = 0
            elif event.key == BattleActions.LEFT.value:
                if self.bag_index > 0:
                    self.bag_index -= 1
                    self.update_bag_info()
                    self.create_cursors()
                    self.start_item_index = 0

            # When going up and down change cursors appropriately.

            # If the user presses up & draw cursor is on the second item slot
            # (index 1) and their are more items left at the
            # beginning of the list then the draw cursor stays on the second
            # slot and we change which items are blitted to the screen (Next
            # item up in the list + the first four currently displayed).
            elif event.key == BattleActions.UP.value:
                if self.draw_cursor.cursor == 1 and \
                        self.item_cursor.cursor != 1:
                    self.start_item_index -= 1
                else:
                    self.draw_cursor.change_cursor_pos(event)

            # If the user presses down and the draw cursor is on the second to
            # last positon (index 3) and their are more items left to display
            # at the end of the list then the cursor stays where it is and the
            # items blitted to the screen change. (Last four + a new one at
            # the end of the list). If this is not the case then simply
            # increase the draw cursor.
            elif event.key == BattleActions.DOWN.value:
                if self.draw_cursor.cursor == 3 and \
                        self.item_cursor.cursor < \
                        len(self.item_list) - 3:
                    self.start_item_index += 1
                else:
                    self.draw_cursor.change_cursor_pos(event)

            elif event.key == BattleActions.BACK.value:
                self.is_dead = True

            elif event.key == BattleActions.SELECT.value:
                selected_item = self.item_list[self.item_cursor.cursor]
                if selected_item == "CANCEL":
                    self.is_dead = True
                else:
                    self.do_what_response_menu = DoWhatMenu(self.bag_index,
                                                            selected_item,
                                                            self.player)

            # Change cursor pos method will update the cursor's position if
            # necessary.
            self.item_cursor.change_cursor_pos(event)
            self.create_items_surface()
            self.update_bobbbing_cursor_status()

    def draw(self, draw_surface):
        """Draws the bag."""
        draw_surface.blit(self.background_surf, (0, 0))
        draw_surface.blit(self.open_bag_surf, (11, 40))
        draw_surface.blit(self.title_surf, (10, 8))
        draw_surface.blit(self.item_surface, (0, 0))
        self.draw_cursor.draw(draw_surface)

        self.up_bobbing_cursor.draw(draw_surface)
        self.down_bobbing_cursor.draw(draw_surface)
        self.left_bobbing_cursor.draw(draw_surface)
        self.right_bobbing_cursor.draw(draw_surface)

        if self.do_what_response_menu is not None:
            self.do_what_response_menu.draw(draw_surface)

    def update_bag_info(self):
        """Updates the bag picture and title displayed."""
        self._create_title_surf()
        self._update_bag_pic()
        self.create_items_surface()

    def create_items_surface(self):
        """Creates the item surfaces based on where the cursor is."""
        # Create item surface
        self.item_surface = pygame.Surface((240, 160))
        self.item_surface.fill((255, 255, 254))
        self.item_surface.set_colorkey((255, 255, 254))

        # Create the item list that contains the items to be displayed.
        bag_key = [ItemTypes.ITEMS, ItemTypes.KEY_ITEMS,
                   ItemTypes.POKE_BALLS][self.bag_index]

        self.item_list = list(self.player.bag[bag_key]) + ["CANCEL"]

        # Blit items based on current start index
        height = 15
        text_maker = TextMaker(join("fonts", "party_txt_font.png"))
        for item in self.item_list[self.start_item_index:
                                   self.start_item_index + 6]:
            # CANCEL and normal items are separated because cancel does not
            # have a quantity and it is a str and not an Item.
            if item == "CANCEL":
                item_surf = text_maker.get_surface(item)
            else:
                item_surf = text_maker.get_surface(item.name.upper())
                if bag_key != ItemTypes.KEY_ITEMS:
                    quantity = str(self.player.bag[bag_key][item]).zfill(3)
                    quantity_surf = \
                        text_maker.get_surface("x" + quantity)

                    # Blit quantity in bag
                    self.item_surface.blit(quantity_surf,
                                           end_at(quantity_surf,
                                                  (223, height)))

            # Blit Cancel/item name then increase height for next item.
            self.item_surface.blit(item_surf, (97, height))
            height += 16

    def create_cursors(self):
        """Creates the two cursors."""

        self.draw_cursor = Cursor(min(6, len(self.item_list)),
                                  initial_pos=(88, 13), line_height=16)
        self.item_cursor = Cursor(len(self.item_list))

        self.up_bobbing_cursor = TextCursor((153, 3), "shop_menu_cursor_f.png",
                                            invert=True)
        self.down_bobbing_cursor = TextCursor((153, 100),
                                              "shop_menu_cursor.png")

        self.left_bobbing_cursor = TextCursor((2, 70),
                                              "shop_menu_cursor_l.png",
                                              horizontal=True)

        self.right_bobbing_cursor = TextCursor((69, 70),
                                               "shop_menu_cursor_r.png",
                                               horizontal=True, invert=True)

        self.update_bobbbing_cursor_status()

    def update_bobbbing_cursor_status(self):
        """Activate or deactivate the bobbing cursors based on what part of
        the bag you are in."""
        if self.start_item_index < len(self.item_list) - 6:
            self.down_bobbing_cursor.activate()
        else:
            self.down_bobbing_cursor.deactivate()

        if self.start_item_index != 0:
            self.up_bobbing_cursor.activate()
        else:
            self.up_bobbing_cursor.deactivate()

        if self.bag_index > 0:
            self.left_bobbing_cursor.activate()
        else:
            self.left_bobbing_cursor.deactivate()

        if self.bag_index < 2:
            self.right_bobbing_cursor.activate()
        else:
            self.right_bobbing_cursor.deactivate()

    def _create_title_surf(self):
        """Creates the title surface based on which bag is open."""
        titles = ["ITEMS", "KEY ITEMS", "POKéBALLS"]
        text_maker = TextMaker(join("fonts", "menu_font.png"))
        self.title_surf = text_maker.get_surface(titles[self.bag_index])

    def _update_bag_pic(self):
        """Gets the correct bag picture based on current bag index.
        Items - 0, Key Items - 1, Pokeballs - 2"""
        self.open_bag_surf = \
            FRAMES.getFrame("bag.png", offset=(self.bag_index, 0))


class DoWhatMenu():
    def __init__(self, bag_index, item, player):
        """Creates a menu asking what to do with a particular item."""
        self.bag_index = bag_index
        self.item = item
        self.player = player
        text_maker = TextMaker(join("fonts", "party_txt_font.png"), max=15)
        if bag_index == 0:
            self.response_menu = ResizableMenu(4, width=8).menu_surface
            self.response_menu.blit(text_maker.get_surface("USE GIVE TOSS "
                                                           "CANCEL"),
                                    (15, 12))
            self.cursor = Cursor(4, initial_pos=(176, 104))
            self.options = ["USE", "GIVE", "TOSS", "CANCEL"]
        elif bag_index == 1:
            self.response_menu = ResizableMenu(3, width=8).menu_surface
            self.response_menu.blit(text_maker.get_surface("USE REGISTER "
                                                           "CANCEL"),
                                    (15, 10))
            self.cursor = Cursor(3, initial_pos=(176, 118))
            self.options = ["USE", "REGISTER", "CANCEL"]
        else:
            text_maker = TextMaker(join("fonts", "party_txt_font.png"), max=20)
            self.response_menu = ResizableMenu(3, width=8).menu_surface
            self.response_menu.blit(text_maker.get_surface("GIVE TOSS CANCEL"),
                                    (15, 10))
            self.cursor = Cursor(3, initial_pos=(176, 118))
            self.options = ["GIVE", "TOSS", "CANCEL"]

        self.create_item_selected_surf()

        self.response = None  # Response that that the player selects.
        self.is_dead = False  # Whether or not the menu is over.

    def create_item_selected_surf(self):
        """Creates a surface which says __ is seleted."""
        text_maker = TextMaker(join("fonts", "party_txt_font.png"), max=100)

        background_frame = FRAMES.getFrame("bag_item_selected.png")
        self.item_selected_surf = \
            pygame.Surface((background_frame.get_size()))
        self.item_selected_surf.fill((255, 255, 254))
        self.item_selected_surf.set_colorkey((255, 255, 254))
        self.item_selected_surf.blit(background_frame, (0, 0))

        item_surf = \
            text_maker.get_surface(f'{self.item.name.upper()} is selected.')
        self.item_selected_surf.blit(item_surf, (10, 10))

    def draw(self, draw_surface):
        """Draws the item selected frame, cursor, and menu of options."""
        if self.response is not None:
            self.response.draw(draw_surface)
        elif self.response_menu is not None:
            height = 95 if self.bag_index == 0 else 111
            draw_surface.blit(self.response_menu, (170, height))
            draw_surface.blit(self.item_selected_surf, (40, 114))
            self.cursor.draw(draw_surface)

    def handle_event(self, event):
        """Moves cursor in menu."""
        if self.response is None:
            if event.key in [BattleActions.UP.value, BattleActions.DOWN.value]:
                self.cursor.change_cursor_pos(event)
            elif event.key == BattleActions.SELECT.value:
                action = self.options[self.cursor.cursor]
                if action == "CANCEL":
                    self.is_dead = True
                elif action == "TOSS":
                    self.response = TossEvent(self.item, self.player)
                elif action == "GIVE":
                    self.response = GiveEvent(self.item, self.player)
                # self.is_dead = True
        else:
            self.response.handle_event(event)

    def update(self, ticks):
        if self.response is not None:
            self.response.update(ticks)
            if self.response.is_over():
                self.response = None
                self.is_dead = True

    def is_over(self):
        """Returns the status of the menu of options."""
        return self.is_dead


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


class GiveEvent(MenuParty):
    """Event which is created when the player presses give from the bag. Takes
    the player through the process of giving an item to a pokemon. If the
    player presses give from the pokemon menu then this stage of the event is
    skipped and will go straight to the GiveEventHandler. Extends MenuParty to
    display the pokemon menu when the user is deciding who to give the item
    to."""
    def __init__(self, item, player):
        super().__init__(player)
        self.item = item
        self.player = player
        self.is_dead = False

        self._text_bar.blit_string("Give item to whom?")
        self.give_event_handler = None

        # Need to keep track of the offset going into the event because
        # MenuParty messes up the offset and if we do not reset at the end of
        # the GiveEvent then the game will hitch for one frame when returning
        # to the overworld.
        self._old_offset = Drawable.WINDOW_OFFSET

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
