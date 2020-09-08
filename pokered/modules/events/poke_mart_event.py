import pygame
from os.path import join
from .dialogue import Dialogue
from .response_dialogue import ResponseDialogue
from .menu_events.bag import Bag
from ..utils.UI.resizable_menu import ResizableMenu
from ..utils.UI.drawable import Drawable
from ..utils.UI.quantity_cursor import QuantityCursor
from ..utils.text_maker import TextMaker
from ..utils.managers.frameManager import FRAMES
from ..utils.misc import end_at
from ..utils.UI.text_cursor import TextCursor
from ..utils.cursor import Cursor
from ..enumerated.battle_actions import BattleActions
from ..enumerated.item_types import ItemTypes


class PokeMartEvent():
    def __init__(self, clerk, player):
        # Store arguments.
        self._clerk = clerk
        self._player = player

        # Tracks the status of the event.
        self._is_dead = False
        self.turned = False

        # Variable to track if the initial response box has been cleared.
        self._response_box_cleared = False

        # Response from initial prompt.
        self._response = None

        # Create the dialogues used in the event.
        self._initial_prompt = \
            MartResponseDialogue("20", self._player,
                                 self._clerk,
                                 response_string="BUY SELL SEE YA!")
        self._seeya_dialogue = Dialogue("19", self._player, self._clerk)

        # Create the buy and sell menus
        self._buy_menu = PokeMartMenu(self._clerk.inventory, self._player,
                                      self._clerk)

        self._sell_menu = SellEvent(self._player)

        # Create surface which displays how much money the player has.
        self._create_money_surface()

        # Create blue help surface background
        self._help_surface = pygame.Surface((240, 49))
        self._help_surface.blit(FRAMES.getFrame("blue_help_box_b.png"), (0, 0))

    def update(self, ticks):
        """Updates the PokeMart event and all of its sub dialogues/menus. Code
        is organized from first dialouge/menu up to the last in terms of
        chronological order."""

        # If waiting for an intitial response then pass control to prompt.
        if not self._initial_prompt.is_over():
            self._initial_prompt.update(ticks)

        # If the initial prompt is finished then extract response from
        # dialogue once.
        elif self._response is None:
            self._response = self._initial_prompt.response

        # If the user selected seeya then pass control to seeya dialogue.
        elif self._response == 2 and not self._seeya_dialogue.is_over():
            self._seeya_dialogue.update(ticks)

        # If seeya ends then the total event is over.
        elif self._seeya_dialogue.is_over():
            self._is_dead = True

        # If the user selected buy then pass control to the buy menu.
        elif self._response == 0 and not self._buy_menu.is_over():
            # Use turned variable to clear response dialogue box.
            if not self._response_box_cleared:
                self.turned = False
                self._response_box_cleared = True
            self._buy_menu.update(ticks)

            # Check to see if the buy menu needs the level to be redrawn.
            if self._buy_menu.turned is False:
                self.turned = False
                self._buy_menu.turned = True

            # Check to see if the player's wallet has changed so it can be
            # reflected in UI.
            if self._buy_menu.player_money_updated:
                self._buy_menu.player_money_updated = False
                self._create_money_surface()

        # If the buy menu is done then signal the level to redraw once to
        # clear UI. Then reset the initial prompt and buy menu objects.
        elif self._buy_menu.is_over():
            self.turned = False
            self._response = None
            self._initial_prompt = \
                MartResponseDialogue("21", self._player,
                                     self._clerk,
                                     response_string="BUY SELL SEE YA!")
            self._buy_menu = PokeMartMenu(self._clerk.inventory, self._player,
                                          self._clerk)

        elif self._response == 1 and not self._sell_menu.is_over():
            self._sell_menu.update(ticks)

        elif self._response == 1 and self._sell_menu.is_over():
            self._response = None
            self.turned = False
            self._sell_menu = SellEvent(self._player)
            self._initial_prompt = \
                MartResponseDialogue("21", self._player,
                                     self._clerk,
                                     response_string="BUY SELL SEE YA!")

    def draw(self, draw_surface):
        """Draws the poke mart menu event based on where the user is in the
        event. Code is ordered from first to last in terms of chrnological
        order."""
        if not self._initial_prompt.is_over():
            self._initial_prompt.draw(draw_surface)
        elif self._response == 2 and not self._seeya_dialogue.is_over():
            self._seeya_dialogue.draw(draw_surface)
        elif self._response == 0 and not self._buy_menu.is_over():
            draw_surface.blit(self._money_surface, (2, 2))
            draw_surface.blit(self._help_surface, (0, 111))
            self._buy_menu.draw(draw_surface)
        elif self._response == 1 and not self._sell_menu.is_over():
            self._sell_menu.draw(draw_surface)

    def handle_event(self, event):
        """Passes on the event to the active subevent/menu. Code is ordered
        from first to last in terms of chronological order."""
        # Get rid of all non keydown events
        if event.type != pygame.KEYDOWN:
            return

        if not self._initial_prompt.is_over():
            self._initial_prompt.handle_event(event)

        # If response is 2 then the user selected SEE YA!. Pass control to
        # seeya dialogue.
        elif self._response == 2 and not self._seeya_dialogue.is_over():
            self._seeya_dialogue.handle_event(event)

        # If response is 0 then the user selected BUY. Pass control to buy
        # menu.
        elif self._response == 0 and not self._buy_menu.is_over():
            self._buy_menu.handle_event(event)

        elif self._response == 1 and not self._sell_menu.is_over():
            self._sell_menu.handle_event(event)

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
        money_surf = text_maker.get_surface(f"~{self._player.money}")
        title_surf = text_maker.get_surface("MONEY")

        # Create money surface and fill it in with transparent color
        self._money_surface = pygame.Surface((76, 36))
        self._money_surface.fill((255, 245, 245))
        self._money_surface.set_colorkey((255, 245, 245))

        # Add menu background, MONEY,and player's money count to the surface.
        menu_frame = FRAMES.getFrame("shop_menu_money.png")
        self._money_surface.blit(menu_frame, (0, 0))
        self._money_surface.blit(title_surf, (6, 8))
        self._money_surface.blit(money_surf, end_at(money_surf, (70, 24)))


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
        """Draw dialogue to screen."""
        Dialogue.draw(self, draw_surface)
        if self.response_menu is not None:
            draw_surface.blit(self.response_menu, (1, 1))
            self.cursor.draw(draw_surface)


class PokeMartMenu(Drawable):
    def __init__(self, inventory, player, npc):
        """Creates the pokemart menu. Displays the items for sale and their
        prices."""
        super().__init__("shop_menu.png", (80, 1), world_bound=False)
        self._is_dead = False  # Status of the event

        # Store arguments
        self._player = player
        self._npc = npc

        # Extract inventory from npc (store clerk)
        self._inventory = inventory

        # Concert inventory keys to a list so that cancel can be added and
        # looped over to concisely display all options.
        self._inventory_list = list(self._inventory.keys()) + ["CANCEL"]

        # Variable used to determine which 5 items from the store to display.
        self.start_item_index = 0

        # Cursor that keeps track of where the black cursor is on the menu.
        self.draw_cursor = Cursor(min(6, len(self._inventory_list)),
                                  initial_pos=(88, 13), line_height=16)

        # Cursor that keeps track of which item in the store is currently
        # selected. Two cursors are needed because it is possible for a store
        # to sell more than five items (the amount displayed on the screen at
        # once).
        self.item_cursor = Cursor(len(self._inventory_list))

        # Create bobbing cursors
        self.down_bobbing_cursor = TextCursor((153, 100),
                                              "shop_menu_cursor.png")
        self.up_bobbing_cursor = TextCursor((153, 3),
                                            "shop_menu_cursor_f.png",
                                            invert=True)

        # Decide if the down cursor should be updated right off of the start
        self._update_cursor_status()

        # Create the 5 item surfaces (which says the items name and price).
        self.create_item_surface()

        # Instatiate the various sub events.
        self.select_count_event = None
        self.confirm_buy_response = None
        self.thanks_dialogue = None

        # Variable which when turned true will signal to the level manager
        # that it needs to redraw the current level to clear the events screen.
        self.turned = False

        # Variable which keeps track of an item that the user might buy.
        # Necessary because we double check if the user wants to buy the item.
        self.pending_buy = None

        # Variable which signals the PokeMartEvent that the user's money has
        # changed. In this case it will have decreased.
        self.player_money_updated = False

    def is_over(self):
        """Tells when the menu is over."""
        return self._is_dead

    def update(self, ticks):
        """Updates the cursor on the poke mart menu."""
        # Always update the bobbing cursors
        self.down_bobbing_cursor.update(ticks)
        self.up_bobbing_cursor.update(ticks)

        # If select count subevent then update that and pass control to it.
        if self.select_count_event is not None:
            self.select_count_event.update(ticks)

            # If the subevent is over then extract the num selected.
            if self.select_count_event.is_over():

                # If the num selected is not none then extract the information
                # about the items being purchased.
                if self.select_count_event.num_selected is not None:
                    name = self.select_count_event.item
                    num_selected = self.select_count_event.num_selected
                    cost = self.select_count_event.num_selected * \
                        self.select_count_event.item_cost

                    # Create a response dialogue which doublechecks if the
                    # player actually wants to buy the items.
                    self.confirm_buy_response = \
                        ResponseDialogue("24", self._player, self._npc,
                                         replace=[name.name, str(num_selected),
                                                  str(cost)],
                                         dy=1)

                    # Trigger the level manager to redraw the level to reset
                    # the event's screen.
                    self.turned = False

                    # Store the info about the potential purchase if user
                    # decides to finalize purchase.
                    self.pending_buy = {
                        "name": name,
                        "quantity": num_selected,
                        "cost": cost
                    }

                # Reset the count event.
                self.select_count_event = None

        # If thanks dialogue is occuring (thanks for your purchase...) then
        # pass control to it. End the subevent when it is over.
        if self.thanks_dialogue is not None:
            self.thanks_dialogue.update(ticks)
            if self.thanks_dialogue.is_over():
                self.thanks_dialogue = None

        # If asking the user if they really want to go through with purchase
        # then pass control to said response dialogue.
        if self.confirm_buy_response is not None:
            self.confirm_buy_response.update(ticks)

            if self.confirm_buy_response.is_over():
                # If the user says yes then subtract money from account, add
                # items to bag, and signal PokeMartEvent that user's money has
                # changed so it can reflect said change in UI.
                if self.confirm_buy_response.response == 0:
                    item = self.pending_buy["name"]

                    if self._player.bag[item.type].get(item, 0) + \
                            self.pending_buy["quantity"] > 999:
                        self.thanks_dialogue = Dialogue("28", self._player,
                                                        self._npc, dy=1)
                    else:
                        self.thanks_dialogue = Dialogue("25", self._player,
                                                        self._npc, dy=1)
                        self._player.money -= self.pending_buy["cost"]
                        self._player.add_items(self.pending_buy["name"],
                                               self.pending_buy["quantity"])
                        self.player_money_updated = True

                self.confirm_buy_response = None

    def draw(self, draw_surface):
        """Draw menu background and blit items for sale and their
        prices."""
        # If their is an active select count sub event pass control to it.
        if self.select_count_event is not None:
            self.select_count_event.draw(draw_surface)
        else:
            # Draw the background menu.
            super().draw(draw_surface)

            # Draw the items and prices.
            draw_surface.blit(self._item_surface, (0, 0))

            # Draw the cursors.
            self.draw_cursor.draw(draw_surface)
            self.down_bobbing_cursor.draw(draw_surface)
            self.up_bobbing_cursor.draw(draw_surface)

            # Also draw subevents if they exist.
            if self.confirm_buy_response is not None:
                self.confirm_buy_response.draw(draw_surface)
            elif self.thanks_dialogue is not None:
                self.thanks_dialogue.draw(draw_surface)

    def handle_event(self, event):
        """Handles the events: up, down, and select."""
        if self.select_count_event is not None:
            self.select_count_event.handle_event(event)
            return  # Use return here to avoid an extra layer of indentation.

        if self.confirm_buy_response is not None:
            self.confirm_buy_response.handle_event(event)
            return  # Use return here to avoid an extra layer of indentation.

        if self.thanks_dialogue is not None:
            self.thanks_dialogue.handle_event(event)
            return  # Use return here to avoid an extra layer of indentation.

        # If no subevents need to take control then change the cursor
        # positions based on the input.
        if event.type == pygame.KEYDOWN and event.key in \
                [BattleActions.UP.value, BattleActions.DOWN.value]:

            # If the user presses up & draw cursor is on the second item slot
            # (index 1) and their are more items left at the
            # beginning of the list then the draw cursor stays on the second
            # slot and we change which items are blitted to the screen (Next
            # item up in the list + the first four currently displayed).
            if event.key == BattleActions.UP.value:
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
                        len(self._inventory_list) - 3:
                    self.start_item_index += 1
                else:
                    self.draw_cursor.change_cursor_pos(event)

            # Update the item cursor and redraw items for sale.
            self.item_cursor.change_cursor_pos(event)
            self.create_item_surface()

            # Activate or deactivate down bobbing cursors if neccessary
            self._update_cursor_status()

        # Handle when the user hits select.
        elif event.type == pygame.KEYDOWN and event.key == \
                BattleActions.SELECT.value:

            # Find out which item they selected.
            name = self._inventory_list[self.item_cursor.cursor]

            # If the button was cancel then the menu event ends. Otherwise
            # find out how much of the item the user wants.
            if name == "CANCEL":
                self._is_dead = True
            else:
                self.select_count_event = \
                    SelectCountEvent(self._player, name, self._inventory[name],
                                     self._npc)

        # If the user hits back the menu event is over.
        elif event.type == pygame.KEYDOWN and event.key == \
                BattleActions.BACK.value:
            self._is_dead = True

    def create_item_surface(self):
        """Creates the five item surfaces that will be displayed. Will also
        show a cancel button if we are at the end of the shops inventory."""
        # Create the surface the subsurfaces will be blitted to.
        self._item_surface = pygame.Surface((240, 160))
        self._item_surface.fill((255, 255, 254))
        self._item_surface.set_colorkey((255, 255, 254))

        # Text maker used to make subsurfaces.
        text_maker = TextMaker(join("fonts", "party_txt_font.png"))

        # Height variable used to dynamically change where subsurfaces are
        # blitted to.
        height = 15
        for item in self._inventory_list[self.start_item_index:
                                         self.start_item_index + 6]:

            # If the item is not cancel then also display its price.
            if item != "CANCEL":
                price_surf = \
                    text_maker.get_surface(f"~{self._inventory[item]}")
                self._item_surface.blit(price_surf,
                                        end_at(price_surf, (223, height)))
                # Display item name.
                self._item_surface.blit(text_maker.get_surface(item.name),
                                        (97, height))
            else:
                # Display item name.
                self._item_surface.blit(text_maker.get_surface(item),
                                        (97, height))

            height += 16

    def _update_cursor_status(self):
        if self.start_item_index < len(self._inventory_list) - 6:
            self.down_bobbing_cursor.activate()
        else:
            self.down_bobbing_cursor.deactivate()

        if self.start_item_index != 0:
            self.up_bobbing_cursor.activate()
        else:
            self.up_bobbing_cursor.deactivate()


class SelectCountEvent():
    def __init__(self, player, item, item_cost, npc):
        """Creates a SelectCountEvent. It's purpose is to return the amount of
        an item that a user will buy. If the user can't afford any of the item
        that they selected than a dialogue is displayed."""
        # Store arguments
        self.player = player
        self.item = item
        self.item_cost = item_cost
        self.npc = npc
        self.is_dead = False  # Status of the event
        self.num_selected = None  # Store the quantity that the user selects

        # If the user can afford at least one of a given item ask how many
        # they want. Otherwise display an ending dialogue.
        self.can_afford = player.money >= item_cost
        if not self.can_afford:
            self.cant_afford_dialogue = Dialogue("22", player, npc,
                                                 show_curs=False, turn=False,
                                                 dy=1)
        else:
            self.in_bag_frame = FRAMES.getFrame("in_bag_frame.png")
            self.how_many_dialogue = Dialogue("23", player, npc,
                                              show_curs=False, turn=False,
                                              replace=[item.name], dy=1)
            self.how_many_selector = \
                HowManySelector(self.player.money // self.item_cost,
                                self.item_cost)

    def draw(self, draw_surface):
        """Draws the appropriate subevents based on whether the user can
        afford the item that they selected."""
        if not self.can_afford:
            self.cant_afford_dialogue.draw(draw_surface)
        else:
            draw_surface.blit(self.in_bag_frame, (2, 81))
            self.how_many_dialogue.draw(draw_surface)
            self.how_many_selector.draw(draw_surface)

    def update(self, ticks):
        """Updates subevents if necesssary. Handles the closing of the event
        based on whether or not the user can afford the item they selected."""
        if not self.can_afford:
            if self.cant_afford_dialogue.is_over():
                self.is_dead = True
        else:
            self.how_many_dialogue.update(ticks)
            self.how_many_selector.update(ticks)

            # Once the how many selector is over we need to extract the amount
            # selected and the Select Count Event is over.
            if self.how_many_selector.is_over():
                self.num_selected = self.how_many_selector.num_selected
                self.is_dead = True

    def handle_event(self, event):
        """Passes on event to subevents."""
        if not self.can_afford:
            self.cant_afford_dialogue.handle_event(event)
        else:
            self.how_many_selector.handle_event(event)

    def is_over(self):
        """Returns the status of the event."""
        return self.is_dead


class HowManySelector():
    def __init__(self, max_num, item_price):
        """Event with sole purpose of allowing the player to choose how much
        of an item they want to buy."""
        self.is_dead = False

        # The amount the user has currently selected.
        self.num_selected = 1

        # The max they can select based on argument.
        self.max_num = max_num

        # Price of the item. Needed so we can calculate num_selected * price.
        # and print to screen.
        self.item_price = item_price

        # Create the surfaces/cursor that will be drawn to screen.
        self.quantity_cursor = QuantityCursor((148, 74))

        # Background frame.
        self.menu_frame = ResizableMenu(2, width=9).menu_surface

        # Cost surface.
        self.text_maker = TextMaker(join("fonts", "party_txt_font.png"))
        self.cost_surf = \
            self.text_maker.get_surface(f"~{self.num_selected * item_price}")

    def draw(self, draw_surface):
        """Draw the background frame, cost information, and cursor."""
        draw_surface.blit(self.menu_frame, (140, 71))
        draw_surface.blit(self.cost_surf, end_at(self.cost_surf, (202, 87)))
        self.quantity_cursor.draw(draw_surface)

    def update(self, ticks):
        """Update the cursor."""
        self.quantity_cursor.update(ticks)

    def handle_event(self, event):
        """Handles events. Increase or decrease amount selected based on
        inputs."""
        # If the event is not a keydown event it has no effect on this event.
        if event.type != pygame.KEYDOWN:
            return

        # Variable used to track if an up or down press actually resulted in a
        # change in the amount the user plans to buy.
        change_made = False

        # Handle when user presses up.
        if event.key == BattleActions.UP.value:
            if self.num_selected + 1 <= self.max_num:
                self.num_selected += 1
                change_made = True

            elif self.num_selected + 1 == self.max_num + 1:
                self.num_selected = 1
                change_made = True

        # Handle when the user presses down.
        elif event.key == BattleActions.DOWN.value:
            if self.num_selected - 1 >= 1:
                self.num_selected -= 1
                change_made = True
            elif self.num_selected == 1:
                self.num_selected = self.max_num
                change_made = True

        # Update the amounts displayed in the selector if the amount changed
        # because of the event.
        if change_made:
            self.quantity_cursor.change_count(self.num_selected)
            cost_string = f"~{self.num_selected * self.item_price}"
            self.cost_surf = \
                self.text_maker.get_surface(cost_string)

        # Once the user presses select the event is over and "controlling"
        # class can accurately extract the correct num_selected and handle
        # accordingly.
        elif event.key == BattleActions.SELECT.value:
            self.is_dead = True

    def is_over(self):
        """Returns the status of the event."""
        return self.is_dead


class SellEvent(Bag):
    """Sell event triggered a when player wants to sell anything inside of a
    pokemon shop."""
    def __init__(self, player):
        super().__init__(player)
        self.active_sell_event = None

    def draw(self, draw_surface):
        """Always draw the bag and draw the active sell event if it exists."""
        super().draw(draw_surface)
        if self.active_sell_event is not None:
            self.active_sell_event.draw(draw_surface)

    def handle_event(self, event):
        """If the active sell event exists then pass control to it otherwise
        pass control to the bag."""
        if self.active_sell_event is not None:
            self.active_sell_event.handle_event(event)
        else:
            super().handle_event(event)

    def update(self, ticks):
        """Always update the bag and update the active sell event if it is not
        None."""
        if self.active_sell_event is not None:
            self.active_sell_event.update(ticks)

            # If the sell event is over then clear it and update the bag UI.
            if self.active_sell_event.is_dead:
                self.active_sell_event = None
                self.update_bag_info()
        super().update(ticks)

    def _handle_select_event(self):
        """Overwrites the Bag's select event to allow for new functionality
        when clicking on an item. If the player clicks on a key item let them
        know that they can't sell it. Otherwise create a sell event."""
        selected_item = self.item_list[self.item_cursor.cursor]
        if selected_item == "CANCEL":
            self.is_dead = True

        # You can't sell key items.
        elif selected_item.type == ItemTypes.KEY_ITEMS:
            self.do_what_response_menu = \
                Dialogue("29", self.player, self.player,
                         replace=[selected_item.name.upper()], show_curs=False)

        # Create a sell event with the selected item.
        else:
            self.active_sell_event = SellHowMany(self.player,
                                                 selected_item)


class SellHowMany():
    def __init__(self, player, item):
        """Creates an event which determines how many of an item that the user
        wants to sell."""
        self.player = player
        self.item = item
        self.quant = 1
        self.max_quant = player.bag[item.type][item]
        self.is_dead = False

        # Asks the user how many of the item they want to sell.
        self.how_many_dialogue = Dialogue("30", self.player, self.player,
                                          show_curs=False,
                                          replace=[item.name.upper()])

        # Create the menu frame which shows the quantity cursor and the amount
        # the player recieaves for selling a given number of the item.
        self.text_maker = TextMaker(join("fonts", "party_txt_font.png"))
        self.menu_frame = ResizableMenu(3, width=14).menu_surface
        self.quantity_cursor = QuantityCursor((140, 71))
        self.cost_surf = \
            self.text_maker.get_surface(str(self.item.sell_price * self.quant))

        self.sub_event = None

    def update(self, ticks):
        """Updates the sell event if it exists. Otherwise update the quantity
        cursor."""
        if self.sub_event is not None:
            self.sub_event.update(ticks)
            if self.sub_event.is_dead:
                self.is_dead = True

        else:
            self.quantity_cursor.update(ticks)

    def handle_event(self, event):
        """If the sub event exists then pass control to it. Otherwise respond
        according to the action."""
        if self.sub_event is not None:
            self.sub_event.handle_event(event)
            return

        if event.key == BattleActions.UP.value:
            if self.quant < self.max_quant:
                self.update_cursor_and_price(self.quant + 1)
            elif self.quant == self.max_quant:
                self.update_cursor_and_price(1)
        elif event.key == BattleActions.DOWN.value:
            if self.quant > 1:
                self.update_cursor_and_price(self.quant - 1)
            elif self.quant == 1:
                self.update_cursor_and_price(self.max_quant)
        elif event.key == BattleActions.SELECT.value:
            self.sub_event = ConfirmSell(self.player, self.item, self.quant)

    def draw(self, draw_surface):
        """Draws the sub event if it exists. Otherwise draw the dialogue, and
        information regarding how much the user will buy."""
        if self.sub_event is not None:
            self.sub_event.draw(draw_surface)
            return

        # Draw info regarding how many of a given item the user will buy.
        self.how_many_dialogue.draw(draw_surface)
        draw_surface.blit(self.menu_frame, (128, 64))
        draw_surface.blit(self.cost_surf, end_at(self.cost_surf, (225, 84)))
        self.quantity_cursor.draw(draw_surface)

    def update_cursor_and_price(self, new_quant):
        """Updates the amount of the item the user intends to buy and updates
        UI to show said change."""
        self.quant = new_quant
        self.quantity_cursor.change_count(self.quant)
        self.cost_surf = \
            self.text_maker.get_surface(str(self.item.sell_price * self.quant))


class ConfirmSell():
    def __init__(self, player, item, amount):
        """Sub event which asks the user if they really want to go through
        with the sale."""
        self.player = player
        self.item = item
        self.amount = amount
        self.confirm_response = \
            ResponseDialogue("31", player, player,
                             replace=[str(amount * item.sell_price)])
        self.is_dead = False
        self.sub_event = None

    def draw(self, draw_surface):
        """Draws the sub event if it exists. Otherwise draw the response
        dialogue."""
        if self.sub_event is not None:
            self.sub_event.draw(draw_surface)
        else:
            self.confirm_response.draw(draw_surface)

    def handle_event(self, event):
        """Pass control to sub event if it exists, otherwise let the response
        dialogue handle control."""
        if self.sub_event is not None:
            self.sub_event.handle_event(event)
        else:
            self.confirm_response.handle_event(event)

    def update(self, ticks):
        """Update the sub event if it exists. Otherwise update the resposne
        dialogue. Get response from response dialogue and respond
        accordingly."""
        if self.sub_event is not None:
            self.sub_event.update(ticks)
            if self.sub_event.is_dead:
                self.is_dead = True
            return

        # No sub event exists.
        self.confirm_response.update(ticks)
        if self.confirm_response.response is not None:
            # User decides to go through with the sale
            if self.confirm_response.response == 0:
                self.sub_event = SellConfirmed(self.player, self.item,
                                               self.amount)
            # User decides to not sell items
            else:
                self.is_dead = True


class SellConfirmed():
    def __init__(self, player, item, amount):
        """Sub event which tells the user they sold the items. Actually
        complete the transaction on the back end."""
        self.player = player
        self.item = item
        self.amount = amount
        self.is_dead = False

        self.confirmed_dialogue = \
            Dialogue("32", self.player, self.player,
                     replace=[item.name.upper(),
                              str(amount * item.sell_price)],
                     show_curs=False)

    def draw(self, draw_surface):
        """Draw the confirmed dialogue."""
        self.confirmed_dialogue.draw(draw_surface)

    def handle_event(self, event):
        """Pass control to the confirmed dialogue."""
        self.confirmed_dialogue.handle_event(event)

    def update(self, ticks):
        """Update the confirmed dialogue. Once the confirmed dialogue is over
        complete transaction on the backend and end the sub event."""
        self.confirmed_dialogue.update(ticks)
        if self.confirmed_dialogue.is_over():
            self.player.money += self.amount * self.item.sell_price
            self.player.bag.subtract_item(self.item, num=self.amount)
            self.is_dead = True
