import pygame
from os.path import join
from ...utils.misc import end_at
from ...utils.cursor import Cursor
from ...utils.text_maker import TextMaker
from ...utils.managers.frameManager import FRAMES
from ...utils.UI.text_cursor import TextCursor
from ...utils.UI.resizable_menu import ResizableMenu
from ...enumerated.battle_actions import BattleActions
from ...enumerated.item_types import ItemTypes


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
            if self.do_what_response_menu.is_over():
                self.do_what_response = self.do_what_response_menu.response
                self.do_what_response_menu = None

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
                                                            selected_item)

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

        self.item_list = list(self.player.bag.bag[bag_key]) + ["CANCEL"]

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
                    quantity = str(self.player.bag.bag[bag_key][item]).zfill(3)
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
    def __init__(self, bag_index, item):
        """Creates a menu asking what to do with a particular item."""
        self.bag_index = bag_index
        self.item = item
        text_maker = TextMaker(join("fonts", "party_txt_font.png"), max=15)
        if bag_index == 0:
            self.response_menu = ResizableMenu(4, width=8).menu_surface
            self.response_menu.blit(text_maker.get_surface("USE GIVE TOSS CANCEL"),
                                    (15, 12))
            self.cursor = Cursor(4, initial_pos=(176, 104))
        elif bag_index == 1:
            self.response_menu = ResizableMenu(3, width=8).menu_surface
            self.response_menu.blit(text_maker.get_surface("USE REGISTER CANCEL"),
                                    (15, 10))
            self.cursor = Cursor(3, initial_pos=(176, 118))
        else:
            text_maker = TextMaker(join("fonts", "party_txt_font.png"), max=20)
            self.response_menu = ResizableMenu(3, width=8).menu_surface
            self.response_menu.blit(text_maker.get_surface("GIVE TOSS CANCEL"),
                                    (15, 10))
            self.cursor = Cursor(3, initial_pos=(176, 118))

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
        height = 95 if self.bag_index == 0 else 111
        if self.response_menu is not None:
            draw_surface.blit(self.response_menu, (170, height))
            draw_surface.blit(self.item_selected_surf, (40, 114))
            self.cursor.draw(draw_surface)

    def handle_event(self, event):
        """Moves cursor in menu."""
        if self.response is None:
            if event.key in [BattleActions.UP.value, BattleActions.DOWN.value]:
                self.cursor.change_cursor_pos(event)
            elif event.key == BattleActions.SELECT.value:
                self.response = self.cursor.cursor
                self.is_dead = True

    def is_over(self):
        """Returns the status of the menu of options."""
        return self.is_dead
