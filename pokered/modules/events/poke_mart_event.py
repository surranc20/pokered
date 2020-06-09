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
        # Store arguments.
        self._clerk = clerk
        self._player = player

        # Tracks the status of the event.
        self._is_dead = False
        self.turned = True

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
        self._buy_menu = PokeMartMenu(self._clerk.inventory, self._player,
                                      self._clerk)

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

        # If the user selected seeya then pass control to said dialogue.
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

    def handle_event(self, event):
        """Passes on the event to the active subevent/menu. Code is ordered
        from first to last in terms of chronological order."""
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

        # Cursor that keeps track of where the black cursor is on the menu.
        self.draw_cursor = Cursor(6, initial_pos=(88, 13), line_height=16)

        # Cursor that keeps track of which item in the store is currently
        # selected. Two cursors are needed because it is possible for a store
        # to sell more than five items (the amount displayed on the screen at
        # once).
        self.item_cursor = Cursor(len(self._inventory_list))

        # Variable used to determine which 5 items from the store to display.
        self.start_item_index = 0

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
        # If select count subevent then update that and pass control to it.
        if self.select_count_event is not None:
            self.select_count_event.update(ticks)

            # If the subevent is over then extract the num selected.
            if self.select_count_event.is_over():

                # If the num selected is not none then extract the information
                # about the items being purchased.
                if self.select_count_event.num_selected is not None:
                    name = self.select_count_event.item_name
                    num_selected = self.select_count_event.num_selected
                    cost = self.select_count_event.num_selected * \
                        self.select_count_event.item_cost

                    # Create a response dialogue which doublechecks if the
                    # player actually wants to buy the items.
                    self.confirm_buy_response = \
                        ResponseDialogue("24", self._player, self._npc,
                                         replace=[name, str(num_selected),
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

            # Draw the store cursor.
            self.draw_cursor.draw(draw_surface)

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
                        self.item_cursor.cursor < len(self._inventory_list) - 3:
                    self.start_item_index += 1
                else:
                    self.draw_cursor.change_cursor_pos(event)

            # Update the item cursor and redraw items for sale.
            self.item_cursor.change_cursor_pos(event)
            self.create_item_surface()

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

            # Display item name.
            self._item_surface.blit(text_maker.get_surface(item), (97, height))

            # If the item is not cancel then also display its price.
            if item != "CANCEL":
                price_surf = text_maker.get_surface(f"~{self._inventory[item]}")
                self._item_surface.blit(price_surf,
                                        end_at(price_surf, (223, height)))

            height += 16


class SelectCountEvent():
    def __init__(self, player, item_name, item_cost, npc):
        """Creates a SelectCountEvent. It's purpose is to return the amount of
        an item that a user will buy. If the user can't afford any of the item
        that they selected than a dialogue is displayed."""
        # Store arguments
        self.player = player
        self.item_name = item_name
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
                                              replace=[item_name], dy=1)
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


class QuantityCursor():
    def __init__(self, pos):
        """Creates a Quantity Cursor. Shows number selected and the cursor's
        going up and down."""
        # Create the two arrow cursors.
        self.down_arrow_surf = FRAMES.getFrame("shop_menu_cursor.png")
        # The up arrow needs to be flipped horizontally. Need to make a
        # separate surface because FRAMES are Singleton. Directly transforming
        # the frame will also change the down cursor.
        self.up_arrow_surf = pygame.Surface(self.down_arrow_surf.get_size())
        self.up_arrow_surf.fill((255, 245, 245))
        self.up_arrow_surf.set_colorkey((255, 245, 245))
        self.up_arrow_surf.blit(pygame.transform.flip(self.down_arrow_surf,
                                                      False, True), (0, 0))

        # Create the position's of the cursors.
        self.up_pos = pos
        self.up_anchor = self.up_pos
        self.down_pos = (pos[0], pos[1] + 25)
        self.down_anchor = self.down_pos

        # Default pixel amount the cursor changes per change.
        self.current_delta = 1

        # Timer for cursors.
        self.timer = 0

        # Create the count surface which displays the amount of items selected.
        self.text_maker = TextMaker(join("fonts", "party_txt_font.png"))
        self.count_surf = self.text_maker.get_surface("x01")
        self.count_pos = (self.up_pos[0] + 1, self.up_pos[1] + 13)

    def change_count(self, count):
        """Changes the amount displayed on the cursor."""
        self.count_surf = \
            self.text_maker.get_surface(f"x{str(count).zfill(2)}")

    def draw(self, draw_surface):
        """Draws the two cursors and the amount selected."""
        draw_surface.blit(self.up_arrow_surf, self.up_pos)
        draw_surface.blit(self.count_surf, self.count_pos)
        draw_surface.blit(self.down_arrow_surf, self.down_pos)

    def update(self, ticks):
        """Updates the two cursors and changes their positions."""
        self.timer += ticks

        # Direction that the cursors are going. Anchor points are used to
        # determine when the cursor needs to change direction.
        if self.down_pos == self.down_anchor:
            self.current_delta = 1
        elif self.down_pos[1] - self.down_anchor[1] >= 2:
            self.current_delta = -1

        # Cursor only moves 5 times a second.
        if self.timer > .2:
            self.up_pos = (self.up_pos[0], self.up_pos[1] - self.current_delta)
            self.down_pos = (self.down_pos[0],
                             self.down_pos[1] + self.current_delta)
            self.timer -= .2
