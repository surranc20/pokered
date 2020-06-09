import pygame
from os.path import join
from .dialogue import Dialogue
from .response_dialogue import ResponseDialogue
from .menu import Cursor
from ..utils.UI.resizable_menu import ResizableMenu
from ..utils.UI.drawable import Drawable
from ..utils.UI.text_cursor import TextCursor
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
        self._buy_menu = PokeMartMenu(self._clerk.inventory, self._player, self._clerk)

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
            if not self._response_box_cleared:
                self.turned = False
                self._response_box_cleared = True
            self._buy_menu.update(ticks)
            if self._buy_menu.turned is False:
                self.turned = False
                self._buy_menu.turned = True
            if self._buy_menu.player_money_updated:
                self._buy_menu.player_money_updated = False
                self._create_money_surface()
        elif self._buy_menu.is_over():
            self.turned = False
            self._response = None
            self._initial_prompt = \
                MartResponseDialogue("21", self._player,
                                     self._clerk,
                                     response_string="BUY SELL SEE YA!")
            self._buy_menu = PokeMartMenu(self._clerk.inventory, self._player, self._clerk)

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
        money_surf = text_maker.get_surface(f"~{self._player.money}")
        title_surf = text_maker.get_surface("MONEY")

        # Create money surface and fill it in with transparent color
        self._money_surface = pygame.Surface((76, 36))
        self._money_surface.fill((255, 245, 245))
        self._money_surface.set_colorkey((255, 245, 245))

        menu_frame = FRAMES.getFrame("shop_menu_money.png")
        self._money_surface.blit(menu_frame, (0, 0))
        self._money_surface.blit(title_surf, (6, 8))
        self._money_surface.blit(money_surf, end_at(money_surf, (70, 24)))


class PokeMartMenu(Drawable):
    def __init__(self, inventory, player, npc):
        """Creates the pokemart menu. Displays the items for sale and their
        prices."""
        super().__init__("shop_menu.png", (80, 1), world_bound=False)
        self._is_dead = False
        self._player = player
        self._npc = npc
        self._inventory = inventory
        self._inventory_list = list(self._inventory.keys()) + ["CANCEL"]
        self.draw_cursor = Cursor(6, initial_pos=(88, 13), line_height=16)
        self.item_cursor = Cursor(len(self._inventory_list))
        self.start_item_index = 0
        self.create_item_surface()
        self.select_count_event = None
        self.confirm_buy_response = None
        self.thanks_dialogue = None
        self.turned = False
        self.pending_buy = None
        self.player_money_updated = False

    def is_over(self):
        """Tells when the menu is over."""
        return self._is_dead

    def update(self, ticks):
        """Updates the cursor on the poke mart menu."""
        if self.select_count_event is not None:
            self.select_count_event.update(ticks)
            if self.select_count_event.is_over():
                if self.select_count_event.num_selected is not None:
                    self.confirm_buy_response = ResponseDialogue("24", self._player, self._npc, replace=[self.select_count_event.item_name, str(self.select_count_event.num_selected), str(self.select_count_event.num_selected * self.select_count_event.item_cost)], dy=1)
                    self.turned = False
                    self.pending_buy = {
                        "name": self.select_count_event.item_name,
                        "quantity": self.select_count_event.num_selected,
                        "cost": self.select_count_event.num_selected * self.select_count_event.item_cost
                    }
                self.select_count_event = None

        if self.thanks_dialogue is not None:
            self.thanks_dialogue.update(ticks)
            if self.thanks_dialogue.is_over():
                self.thanks_dialogue = None

        if self.confirm_buy_response is not None:
            self.confirm_buy_response.update(ticks)

            if self.confirm_buy_response.is_over():
                if self.confirm_buy_response.response == 0:
                    self.thanks_dialogue = Dialogue("25", self._player, self._npc, dy=1)
                    self._player.money -= self.pending_buy["cost"]
                    self._player.add_items(self.pending_buy["name"], self.pending_buy["quantity"])
                    self.player_money_updated = True

                self.confirm_buy_response = None

    def draw(self, draw_surface):
        """Draw menu background and print out items for sale and their
        prices."""
        if self.select_count_event is not None:
            self.select_count_event.draw(draw_surface)
        else:
            super().draw(draw_surface)
            draw_surface.blit(self._item_surface, (0, 0))
            self.draw_cursor.draw(draw_surface)
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
            name = self._inventory_list[self.item_cursor.cursor]
            if name == "CANCEL":
                self._is_dead = True
            else:
                self.select_count_event = SelectCountEvent(self._player, name, self._inventory[name], self._npc)
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
                price_surf = text_maker.get_surface(f"~{self._inventory[item]}")
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


class SelectCountEvent():
    def __init__(self, player, item_name, item_cost, npc):
        self.player = player
        self.item_name = item_name
        self.item_cost = item_cost
        self.npc = npc
        self.is_dead = False
        self.num_selected = None
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
            self.how_many_selector = HowManySelector(self.player.money // self.item_cost, self.item_cost)

    def draw(self, draw_surface):
        if not self.can_afford:
            self.cant_afford_dialogue.draw(draw_surface)
        else:
            draw_surface.blit(self.in_bag_frame, (2, 81))
            self.how_many_dialogue.draw(draw_surface)
            self.how_many_selector.draw(draw_surface)

    def update(self, ticks):
        if not self.can_afford:
            if self.cant_afford_dialogue.is_over():
                self.is_dead = True
        else:
            self.how_many_dialogue.update(ticks)
            self.how_many_selector.update(ticks)
            if self.how_many_selector.is_over():
                self.num_selected = self.how_many_selector.num_selected
                self.is_dead = True

    def handle_event(self, event):
        if not self.can_afford:
            self.cant_afford_dialogue.handle_event(event)
        else:
            self.how_many_selector.handle_event(event)

    def is_over(self):
        return self.is_dead


class HowManySelector():
    def __init__(self, max_num, item_price):
        self.is_dead = False
        self.num_selected = 1
        self.max_num = max_num
        self.quantity_cursor = QuantityCursor((148, 74))
        self.menu_frame = ResizableMenu(2, width=9).menu_surface

        self.text_maker = TextMaker(join("fonts", "party_txt_font.png"))
        self.cost_surf = self.text_maker.get_surface(f"~{self.num_selected * item_price}")

        self.item_price = item_price

    def draw(self, draw_surface):
        draw_surface.blit(self.menu_frame, (140, 71))
        draw_surface.blit(self.cost_surf, end_at(self.cost_surf, (202, 87)))
        self.quantity_cursor.draw(draw_surface)

    def update(self, ticks):
        self.quantity_cursor.update(ticks)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == BattleActions.UP.value:
            if self.num_selected + 1 <= self.max_num:
                self.num_selected += 1
                self.quantity_cursor.change_count(self.num_selected)
                self.cost_surf = self.text_maker.get_surface(f"~{self.num_selected * self.item_price}")
            elif self.num_selected + 1 == self.max_num + 1:
                self.num_selected = 1
                self.quantity_cursor.change_count(self.num_selected)
                self.cost_surf = self.text_maker.get_surface(f"~{self.num_selected * self.item_price}")

        elif event.key == BattleActions.DOWN.value:
            if self.num_selected - 1 >= 1:
                self.num_selected -= 1
                self.quantity_cursor.change_count(self.num_selected)
                self.cost_surf = self.text_maker.get_surface(f"~{self.num_selected * self.item_price}")
            elif self.num_selected == 1:
                self.num_selected = self.max_num
                self.quantity_cursor.change_count(self.num_selected)
                self.cost_surf = self.text_maker.get_surface(f"~{self.num_selected * self.item_price}")

        elif event.key == BattleActions.SELECT.value:
            self.is_dead = True

    def is_over(self):
        return self.is_dead


class QuantityCursor():
    def __init__(self, pos):
        self.down_arrow_surf = FRAMES.getFrame("shop_menu_cursor.png")

        self.up_arrow_surf = pygame.Surface(self.down_arrow_surf.get_size())
        self.up_arrow_surf.fill((255, 245, 245))
        self.up_arrow_surf.set_colorkey((255, 245, 245))
        self.up_arrow_surf.blit(pygame.transform.flip(self.down_arrow_surf, False, True), (0, 0))

        self.up_pos = pos
        self.down_pos = (pos[0], pos[1] + 25)

        self.up_anchor = self.up_pos
        self.down_anchor = self.down_pos

        self.current_delta = 1

        self.timer = 0

        self.text_maker = TextMaker(join("fonts", "party_txt_font.png"))
        self.count_surf = self.text_maker.get_surface("x01")

        self.count_pos = (self.up_pos[0] + 1, self.up_pos[1] + 13)

    def change_count(self, count):
        self.count_surf = self.text_maker.get_surface(f"x{str(count).zfill(2)}")

    def draw(self, draw_surface):
        draw_surface.blit(self.up_arrow_surf, self.up_pos)
        draw_surface.blit(self.count_surf, self.count_pos)
        draw_surface.blit(self.down_arrow_surf, self.down_pos)

    def update(self, ticks):
        self.timer += ticks

        if self.down_pos == self.down_anchor:
            self.current_delta = 1
        elif self.down_pos[1] - self.down_anchor[1] >= 2:
            self.current_delta = -1

        if self.timer > .2:
            self.up_pos = (self.up_pos[0], self.up_pos[1] - self.current_delta)
            self.down_pos = (self.down_pos[0], self.down_pos[1] + self.current_delta)
            self.timer -= .2

