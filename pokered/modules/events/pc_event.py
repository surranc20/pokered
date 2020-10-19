import pygame
from os.path import join
from .response_box import ResponseBox
from .dialogue import Dialogue
from ..battle.battle_menus.poke_party import BouncingPokemon
from ..utils.UI.tileset_tile import TilesetTile
from ..utils.UI.text_cursor import TextCursor
from ..utils.UI.animated import Animated
from ..utils.managers.soundManager import SoundManager
from ..utils.managers.frameManager import FRAMES
from ..utils.text_maker import TextMaker
from ..utils.misc import center, end_at
from ..enumerated.battle_actions import BattleActions
from .menu_events.summary_menu_pc import SummaryMenuPC


class PCEvent():
    def __init__(self, player, pc_pos):
        """Creates the events that starts when the user boots up a pc. Passes
        on control to the various event that can take place while the user is
        on the pc."""
        self.player = player
        self.is_dead = False
        self.shutting_down = False
        self.turned = True

        self.pc_pos = pc_pos

        # First thing to do is boot up the pc.
        self.active_sub_event = TurnOn(player, pc_pos)

    def draw(self, draw_surface):
        """Draws the active sub event"""
        self.active_sub_event.draw(draw_surface)

    def update(self, ticks):
        """Updates the active sub event and handles the transtions between sub
        events """
        self.active_sub_event.update(ticks)

        if self.active_sub_event.is_over():
            if self.shutting_down:
                self.is_dead = True

            # Depending on how some events in it is possible that the desired
            # outcome is the immediate closure of the pc.
            elif self.active_sub_event.super_kill:
                self.shutting_down = True
                self.turned = False
                self.active_sub_event = TurnOff(self.player, self.pc_pos)

            else:
                self.active_sub_event = self.active_sub_event.end_event
                if type(self.active_sub_event) == BillsPC:
                    self.turned = False

    def handle_event(self, event):
        """Passes control of event handling to the active sub event."""
        if event.type != pygame.KEYDOWN:
            return

        self.active_sub_event.handle_event(event)

    def is_over(self):
        """Tells the level manager whether or not the event is done."""
        return self.is_dead

    def get_end_event(self):
        """Tells the level manager to return control to the level when the
        event is done."""
        return "Level"


class TurnOff():
    def __init__(self, player, pc_pos):
        """This events sole purpose is to display the animation of the
        computer turning off."""
        self.player = player
        self.is_dead = False
        self.super_kill = False
        self.end_event = None

        self.end_timer = .2

        self.pc_pos = pc_pos
        self.screen_tile_info = {"rowNum": 12, "columnNum": 3,
                                 "tileSetName": "tileset_12.png"}

        self.screen = TilesetTile(self.screen_tile_info,
                                  [pc_pos[0] * 16, pc_pos[1] * 16])

        SoundManager.getInstance().playSound("firered_0003.wav", sound=1)

    def draw(self, draw_surface):
        """Draw the screen and the player. The player is drawn so that the
        screen does not cut off the player's head."""
        self.screen.draw(draw_surface)
        self.player.draw(draw_surface)

    def update(self, ticks):
        """Updates the end timer so that the event does not end right away."""
        if self.end_timer > 0:
            self.end_timer -= ticks
        else:
            self.is_dead = True

    def handle_event(self, event):
        """Nothing should happen regardless of input."""
        pass

    def is_over(self):
        """Tells PC event whether or not the pc has been turned off."""
        return self.is_dead


class TurnOn():
    def __init__(self, player, pc_pos):
        """Displays the animation that turns on the PC."""
        self.player = player
        self.is_dead = False
        self.super_kill = False
        self.end_event = ChoosePC(player)

        # Keep track of how many times the screen has flickered.
        self.flicker_count = 0
        self.flicker_timer = 0
        self.fps = 10

        self.end_timer = .2

        self.on = False
        self.pc_pos = pc_pos
        self.screen_tile_info = {"rowNum": 12, "columnNum": 2,
                                 "tileSetName": "tileset_12.png"}

        self.screen = TilesetTile(self.screen_tile_info,
                                  [pc_pos[0] * 16, pc_pos[1] * 16])

        SoundManager.getInstance().playSound("firered_0004.wav", sound=1)

    def draw(self, draw_surface):
        """Draws the flickering screen and then the player to make sure the
        top of the player's head is not cut off."""
        self.screen.draw(draw_surface)
        self.player.draw(draw_surface)

    def update(self, ticks):
        """Controls the flickering of the screen. Screen flickers five times
        and then waits before ending the event."""
        if self.flicker_count < 5:
            self.flicker_timer += ticks
            if self.flicker_timer > 1 / self.fps:
                self.flicker_count += 1

                self.on = not self.on

                # Change tile based on if the screen is on or off.
                if self.on:
                    self.screen_tile_info["columnNum"] = 3
                else:
                    self.screen_tile_info["columnNum"] = 2

                self.screen = TilesetTile(self.screen_tile_info,
                                          [self.pc_pos[0] * 16,
                                           self.pc_pos[1] * 16])

                self.flicker_timer -= 1 / self.fps

        elif self.end_timer > 0:
            self.end_timer -= ticks

        else:
            self.is_dead = True

    def handle_event(self, event):
        """No matter the input nothing should happen."""
        pass

    def is_over(self):
        """Tells PCEvent whether or not the pc has turned on."""
        return self.is_dead


class ChoosePC():
    def __init__(self, player):
        """This is the event which asks the player to choose the pc they wish
        to enter."""
        self.player = player
        self.is_dead = False
        self.super_kill = False

        # Create the initial prompt to ask user what they want to do in pc
        self.response_box = ResponseBox(self.player.pc_options, (1, 1),
                                        width=16)
        self.dialogue = Dialogue("33", self.player, self.player,
                                 gender=self.player.gender, show_curs=False,
                                 turn=False)

    def draw(self, draw_surface):
        """Draw the response box and dialoogue."""
        self.response_box.draw(draw_surface)
        self.dialogue.draw(draw_surface)

    def update(self, ticks):
        """Update the response box."""
        self.response_box.update(ticks)

    def handle_event(self, event):
        """Pass control of the event handling to the response box."""
        if event.type != pygame.KEYDOWN:
            return

        self.response_box.handle_event(event)

        # Grab response from the response box and set the next event
        # accordingly.
        if self.response_box.is_dead:
            if self.player.pc_options[self.response_box.cursor.cursor] == \
                    "LOG OFF":
                self.super_kill = True
            elif self.player.pc_options[self.response_box.cursor.cursor] == \
                    "BILL'S PC":
                self.end_event = BillsPC(self.player)
            self.is_dead = True

    def is_over(self):
        """Tell PCEvent whether or not the pc has been chosen."""
        return self.is_dead


class BillsPC():
    def __init__(self, player):
        """Asks the user what they want to do in Bill's PC (The main pc)."""
        self.player = player
        self.is_dead = False
        self.super_kill = False

        # Create the initial prompt to ask user what they want to do in pc
        self.box_options = ["WITHDRAW POKéMON", "DEPOSIT POKéMON",
                            "MOVE POKéMON", "MOVE ITEMS", "SEE YA!"]
        self.response_box = ResponseBox(self.box_options, (1, 1),
                                        width=16)

        self.dialogue = Dialogue("pc0", self.player, self.player,
                                 gender=self.player.gender, show_curs=False,
                                 turn=False)

    def draw(self, draw_surface):
        """Draws the response dialogue and box."""
        self.response_box.draw(draw_surface)
        self.dialogue.draw(draw_surface)

    def update(self, ticks):
        """Updates the response box."""
        self.response_box.update(ticks)

    def handle_event(self, event):
        """Passes control of event handling to the response box."""
        if event.type != pygame.KEYDOWN:
            return

        self.response_box.handle_event(event)
        self.dialogue = Dialogue(f'pc{self.response_box.cursor.cursor}',
                                 self.player, self.player,
                                 gender=self.player.gender, show_curs=False,
                                 turn=False)

        # Get response from response box and handle branching to next event.
        if self.response_box.is_dead:
            if self.box_options[self.response_box.cursor.cursor] == "SEE YA!":
                self.end_event = ChoosePC(self.player)
            elif self.box_options[self.response_box.cursor.cursor] == \
                    "WITHDRAW POKéMON":
                self.end_event = MoveScreen(self.player)
            self.is_dead = True

    def is_over(self):
        """Tells PCEvent whether or not the event is over."""
        return self.is_dead


class MoveScreen():
    def __init__(self, player, box_number=0):
        """The event that takes place when a user is inside a box."""
        self.player = player
        self.is_dead = False
        self.super_kill = False

        self.pc_background = FRAMES.getFrame(join("pc", "pc_background.png"))
        self.box_header = BoxHeader(box_number, header_pos=[100, 18])
        self.close_box = BoxButtonClose(join("pc", "close_box.png"), (170, 0))
        self.box = Box(player, box_number)
        self.box.toggle()

        self.party_pokemon = BoxButtonParty(join("pc", "party_pokemon.png"),
                                            (83, 0))

        self.active_event = self.box

        self.move_count = 0

    def draw(self, draw_surface):
        """Draws everything."""
        draw_surface.blit(self.pc_background, (0, 0))
        self.move_count += 1
        if self.move_count == 240:
            self.pc_background = FRAMES.reload(join("pc", "pc_background.png"))
            self.move_count = 0
        self.box_header.draw(draw_surface)
        if type(self.active_event) is BoxSwitch:
            self.active_event.draw(draw_surface)
        self.close_box.draw(draw_surface)
        self.party_pokemon.draw(draw_surface)
        self.box.draw(draw_surface)

        if type(self.active_event) is Exit:
            self.active_event.draw(draw_surface)

    def update(self, ticks):
        """Updates the box header (for the bobbing arrows)."""
        self.pc_background.scroll(dx=-1, dy=-1)
        self.active_event.update(ticks)
        if self.active_event.is_dead:
            next_event = self.active_event.end_event
            if type(self.active_event) == BoxSwitch:
                self.box = self.active_event.new_box
                self.box_header = self.active_event.new_header
            elif type(next_event) == SummaryMenuPC:
                self.active_event = next_event
            if next_event == "BoxHeader":
                self.active_event = self.box_header
            elif next_event == "Box":
                self.active_event = self.box
            elif next_event == "PartyPokemon":
                self.active_event = self.party_pokemon
            elif next_event == "CloseBox":
                self.active_event = self.close_box
            elif next_event == "BoxSwitch":
                self.active_event = BoxSwitch(self.active_event.direction,
                                              self.box, self.box_header)
            elif next_event == "Exit":
                self.active_event = Exit(self.player)
            elif next_event == "ConfirmExit":
                self.is_dead = True
                self.end_event = BillsPC(self.player)
                self.pc_background = \
                    FRAMES.reload(join("pc", "pc_background.png"))
            elif next_event == "PokemonSelectedEvent":
                self.active_event = PokemonSelectedEvent(self.active_event)
            self.active_event.toggle()

    def handle_event(self, event):
        """WIP."""
        self.active_event.handle_event(event)

    def is_over(self):
        """Tells PCEvent whether or not the box screen event is over."""
        return self.is_dead


class PokemonData():
    def __init__(self, pokemon):
        """Creates the pokemon data sidebar which displays the stats/name of
        the currently selected pokemon."""
        self.pokemon = pokemon
        self.create_surface()

    def draw(self, draw_surface):
        """Draws the side panel and lightning bolts."""
        draw_surface.blit(self.surface, (0, 0))
        self.lightning_l.draw(draw_surface)
        self.lightning_r.draw(draw_surface)

    def update(self, ticks):
        """Updates the lightning bolts."""
        self.lightning_l.update(ticks)
        self.lightning_r.update(ticks)

    def create_surface(self):
        """Creates the side panel."""
        self.surface = pygame.Surface((80, 158))
        self.surface.set_colorkey((0, 0, 0))
        self.surface.blit(FRAMES.getFrame(join("pc", "pokemon_data.png")),
                          (0, 2))

        if self.pokemon is not None:
            self.fill_data()

        self.create_lightning_bolts()

    def fill_data(self):
        """Fills in the data for the side panel."""
        # TODO: Neet different fonts here
        text_maker = TextMaker(join("fonts", "menu_font.png"), 240)
        self.surface.blit(self.pokemon.summary_image, (10, 10))

        nick_name = text_maker.get_surface(self.pokemon.nick_name)
        self.surface.blit(nick_name, end_at(nick_name, (70, 86)))

        name = text_maker.get_surface("/" + self.pokemon.name.upper())
        self.surface.blit(name, (7, 100))

        font_index = 0 if self.pokemon.gender == "male" else 1
        gender = \
            FRAMES.getFrame("gender_t.png", offset=(font_index, 0))
        self.surface.blit(gender, (20, 112))

        level = text_maker.get_surface("Lv" + str(self.pokemon.stats["LVL"]))
        self.surface.blit(level, (32, 113))

        item = "" if self.pokemon.held_item is None else \
            self.pokemon.held_item.name.upper()

        item_surf = text_maker.get_surface(item)
        self.surface.blit(item_surf, (7, 130))

    def create_lightning_bolts(self):
        """Creates the two lightning bolts."""
        self.lightning_l = Animated(join("pc", "lightning_l.png"), (2, 6))
        self.lightning_r = Animated(join("pc", "lightning_r.png"), (67, 6))
        self.create_bolt(self.lightning_l)
        self.create_bolt(self.lightning_r)

    def create_bolt(self, bolt):
        """Creates an individual lightning bolt."""
        bolt._nFrames = 3
        bolt._framesPerSecond = 7
        bolt._frame = 1
        bolt._world_bound = False
        bolt.get_current_frame()


class Box():
    def __init__(self, player, box_number=0, move_event=None):
        """Sub event which is responsible for drawing the box and all pokemon
        inside of the box. Also keeps track of the cursor and moves it
        around."""
        self.player = player
        self.box_number = box_number
        self.box_pos = [84, 43]

        # There are only 12 box designs so grab correct design and handle
        # overflow. The % 4 is here because the designs are in rows of 4 in
        # the sprite sheet.
        offset = ((box_number % 12) % 4, (box_number % 12) // 4)
        self.box_background = \
            FRAMES.getFrame(join("pc", "box_backgrounds.png"),
                            offset)

        self.box = self.player.pc_boxes[self.box_number]

        self.cursor_pos = [0, 0]

        self.pokemon_grabbed = [-1, -1]

        self.create_pokemon_surface()

        self.hand = BoxHand()
        self.hand._position = (83 + self.cursor_pos[0] * 25,
                               17 + self.cursor_pos[1] * 24)

        self.pokemon_data = PokemonData(None)
        self.pokemon_held = None

        self.sub_event = None
        self.is_dead = True

        if move_event is not None and not move_event.is_dead:
            self.sub_event = move_event
            self.sub_event.box_changed(self)

        self.active_move_event = None

    def draw(self, draw_surface):
        """Draws everything."""
        if type(self.sub_event) is SummaryMenuPC:
            self.sub_event.draw(draw_surface)
            return

        draw_surface.blit(self.box_background, self.box_pos)
        draw_surface.blit(self.pokemon_surface,
                          (self.box_pos[0] - 1, self.box_pos[1] - 18))

        self.pokemon_data.draw(draw_surface)

        if not self.is_dead:
            # This monstrosity is necessary in order to draw the hand and the
            # events in the correct order. Based on what is happening the hand
            # might need to be infront of or behind the event.
            hand_drawn = False
            if self._should_draw_hand():
                self.hand.draw(draw_surface)
                hand_drawn = True
            if self.sub_event is not None:
                self.sub_event.draw(draw_surface)
            if not hand_drawn:
                self.hand.draw(draw_surface)

    def _should_draw_hand(self):
        """Helper function that decides if the hand should be drawn before or
        after the current subevent."""
        return self.cursor_pos[1] > 0 and self.cursor_pos[0] > 2 and \
            not(type(self.sub_event) is PokemonMoveEvent and
                self.sub_event.sub_event is None)

    def create_pokemon_surface(self):
        """Create the surface that displays all of the pokemon in the box."""
        self.pokemon_surface = pygame.Surface((156, 130))
        self.pokemon_surface.set_colorkey((0, 0, 0))
        for y, row in enumerate(self.box):
            for x, pokemon in enumerate(row):
                if pokemon is not None:
                    poke = BouncingPokemon(pokemon, (25 * x, 24 * y),
                                           item=False)
                    poke._world_bound = False
                    poke.draw(self.pokemon_surface)

    def handle_event(self, event):
        """Handles the updating of the cursor."""
        if self.sub_event is not None:
            self.sub_event.handle_event(event)
            if self.sub_event.is_dead:
                self.sub_event = self.sub_event.end_event
                if type(self.sub_event) == PokemonMoveEvent:
                    self.pokemon_grabbed = self.cursor_pos
                self.create_pokemon_surface()
            return

        self._handle_event_helper(event)

    def _handle_event_helper(self, event):
        pokemon_changed = False
        if event.key == BattleActions.UP.value:
            if self.cursor_pos[1] > 0:
                self.cursor_pos[1] -= 1
                pokemon_changed = True
            else:
                self.toggle()
                self.end_event = "BoxHeader"
                if type(self.sub_event) is PokemonMoveEvent:
                    self.pokemon_held = self.sub_event.pokemon_selected
                    self.active_move_event = self.sub_event
        elif event.key == BattleActions.DOWN.value:
            if self.cursor_pos[1] < 4:
                self.cursor_pos[1] += 1
                pokemon_changed = True
        elif event.key == BattleActions.LEFT.value:
            if self.cursor_pos[0] > 0:
                self.cursor_pos[0] -= 1
                pokemon_changed = True
        elif event.key == BattleActions.RIGHT.value:
            if self.cursor_pos[0] < 5:
                self.cursor_pos[0] += 1
                pokemon_changed = True
        elif event.key == BattleActions.SELECT.value:
            self.sub_event = PokemonSelectedEvent(self)

        self.hand._position = (83 + self.cursor_pos[0] * 25,
                               17 + self.cursor_pos[1] * 24)

        if pokemon_changed:
            try:
                x, y = self.cursor_pos
                pokemon = self.box[y][x]
                self.pokemon_data = PokemonData(pokemon)
            except IndexError:
                self.pokemon_data = PokemonData(None)

    def toggle(self):
        """Toggles the box on and off."""
        self.is_dead = not self.is_dead
        if self.pokemon_data.pokemon is None:
            pokemon = \
                self.box[self.cursor_pos[1]][self.cursor_pos[0]]
            self.pokemon_data = PokemonData(pokemon)
        else:
            self.pokemon_data = PokemonData(None)

    def update(self, ticks):
        """Updates the pokemon data side bar."""
        self.pokemon_data.update(ticks)
        self.hand.update(ticks)
        if self.sub_event is not None:
            self.sub_event.update(ticks)
            if self.sub_event.is_dead:
                if self.sub_event.end_event is None:
                    self.sub_event = None


class BoxButton():
    def __init__(self, button_path, pos):
        """Creates a box button (close box/party pokemon)."""
        self.pos = pos
        self.button_path = button_path
        self.is_dead = True

        self.button_image = FRAMES.getFrame(button_path, offset=(0, 0))
        self.hand = FRAMES.getFrame(join("pc", "hands.png"), (1, 0))

    def toggle(self):
        """Image changes appearance based on whether or not the box is
        currently selected. This function toggles the image."""
        self.is_dead = not self.is_dead
        if not self.is_dead:
            self.button_image = \
                FRAMES.getFrame(self.button_path, offset=(1, 0))
        else:
            self.button_image = \
                FRAMES.getFrame(self.button_path, offset=(0, 0))

    def draw(self, draw_surface):
        """Draws the button."""
        draw_surface.blit(self.button_image, self.pos)

    def update(self, ticks):
        pass


class BoxButtonClose(BoxButton):
    def __init__(self, button_path, pos):
        """Custom class for the close button which extends the BoxButton
        class."""
        super().__init__(button_path, pos)

    def handle_event(self, event):
        """Handles events while the user is on the button."""
        if event.key == BattleActions.DOWN.value:
            self.toggle()
            self.end_event = "BoxHeader"
        elif event.key == BattleActions.LEFT.value:
            self.toggle()
            self.end_event = "PartyPokemon"
        elif event.key == BattleActions.SELECT.value:
            self.toggle()
            self.end_event = "Exit"

    def draw(self, draw_surface):
        """Draw the button and the hand if the button is active."""
        super().draw(draw_surface)
        if not self.is_dead:
            draw_surface.blit(self.hand, (200, 12))


class BoxButtonParty(BoxButton):
    def __init__(self, button_path, pos):
        """Custom class for the party button which extends the BoxButton
        class."""
        super().__init__(button_path, pos)

    def draw(self, draw_surface):
        """Draws the button and the hand if the button is active."""
        super().draw(draw_surface)
        if not self.is_dead:
            draw_surface.blit(self.hand, (115, 12))

    def handle_event(self, event):
        """Handles the event for the button."""
        if event.key == BattleActions.DOWN.value:
            self.toggle()
            self.end_event = "BoxHeader"
        elif event.key == BattleActions.RIGHT.value:
            self.toggle()
            self.end_event = "CloseBox"


class BoxHeader():
    def __init__(self, box_number, header_pos=[100, 18]):
        """Creates the box header. Depending on whether or not the header is
        selected the arrows on the side will bob in and out."""
        self.is_dead = True
        self.header_pos = header_pos

        # Create the surfaces needed for the header

        # There are only 12 box designs so grab correct design and handle
        # overflow. The % 4 is here because the designs are in rows of 4 in
        # the sprite sheet.
        offset = ((box_number % 12) % 4, (box_number % 12) // 4)
        self.header_image = FRAMES.getFrame(join("pc", "box_headers.png"),
                                            offset)

        self.left_arrow = TextCursor((self.header_pos[0] - 10, 23),
                                     name=join("pc", "box_arrows.png"),
                                     horizontal=True, offset=(0, 0),
                                     invert=True)

        self.right_arrow = TextCursor((self.header_pos[0] + 126, 23),
                                      name=join("pc", "box_arrows.png"),
                                      horizontal=True, offset=(1, 0))

        self.hand = FRAMES.getFrame(join("pc", "hands.png"), (0, 0))

        # The right arrow needs to set the color key manually because the top
        # left pixel is part of the image.
        right_arrow_color_key = self.right_arrow._image.get_at((7, 0))
        self.right_arrow._image.set_colorkey(right_arrow_color_key)

        # Activate both cursors so they draw.
        self.left_arrow.activate()
        self.right_arrow.activate()

        # Create the title surface of the box.
        self.make_title_surf()
        self.title_pos = list(center(self.title_surf, self.header_pos[0],
                                     self.header_pos[0] + 124, 22))

    def draw(self, draw_surface):
        """Draws the header, title of box, and the two arrows."""
        draw_surface.blit(self.header_image, self.header_pos)
        self.left_arrow.draw(draw_surface)
        self.right_arrow.draw(draw_surface)
        draw_surface.blit(self.title_surf, self.title_pos)
        if not self.is_dead:
            draw_surface.blit(self.hand, (153, 4))

    def update(self, ticks):
        """Updates the bobbing arrows."""
        self.left_arrow.update(ticks)
        self.right_arrow.update(ticks)

    def toggle(self):
        """Toggles the arrows and resets them back to their start position."""
        self.is_dead = not self.is_dead
        self.left_arrow.reset()
        self.right_arrow.reset()

    def make_title_surf(self):
        """Creates the title of the box."""
        text_maker = TextMaker(join("fonts", "menu_font.png"), 240)
        self.title_surf = text_maker.get_surface("TESTING")

    def handle_event(self, event):
        if event.key == BattleActions.LEFT.value:
            self.toggle()
            self.end_event = "BoxSwitch"
            self.direction = "left"
        elif event.key == BattleActions.RIGHT.value:
            self.toggle()
            self.end_event = "BoxSwitch"
            self.direction = "right"
        elif event.key == BattleActions.UP.value:
            self.toggle()
            self.end_event = "PartyPokemon"
        elif event.key == BattleActions.DOWN.value:
            self.toggle()
            self.end_event = "Box"

    def change_pos(self, delta):
        """Change the positions of all elements of the header."""
        self.header_pos[0] += delta
        self.title_pos[0] += delta
        self.left_arrow.set_pos_no_off((self.left_arrow._position[0] + delta,
                                        self.left_arrow._position[1]))

        self.right_arrow.set_pos_no_off((self.right_arrow._position[0] + delta,
                                         self.right_arrow._position[1]))


class BoxSwitch():
    def __init__(self, direction, box, header):
        """Create a box switch event which transitions between boxes."""
        self.is_dead = False
        self.direction = 1 if direction == "right" else -1

        # Grab the header and box that are currently on display
        self.box = box
        self.header = header

        # Grab the box that is being transitioned to. There are only 14 boxes
        # so go back to 1/14 when overflowing.
        box_number = (self.box.box_number + self.direction) % 14
        header_pos = [270, 18] if direction == "right" else [-70, 18]
        self.new_header = BoxHeader(box_number, header_pos=header_pos)
        self.new_box = Box(self.box.player, box_number,
                           move_event=self.box.active_move_event)
        self.new_box.box_pos = [254, 43] if direction == "right" else [-86, 43]

        self.timer = 0
        self.fps = 45

    def draw(self, draw_surface):
        """Draw the new boxes that are sliding in."""
        self.new_header.draw(draw_surface)
        self.new_box.draw(draw_surface)

    def handle_event(self, event):
        """The player should not be able to do anything during the
        transition."""
        pass

    def update(self, ticks):
        """Updates the positions of the boxes and headers."""
        self.timer += ticks
        if self.timer > 1 / self.fps:
            self.timer -= 1 / self.fps
            self.box.box_pos[0] -= 5 * self.direction
            self.new_box.box_pos[0] -= 5 * self.direction
            self.header.change_pos(-5 * self.direction)
            self.new_header.change_pos(-5 * self.direction)

        if self.new_box.box_pos[0] == 84:
            self.is_dead = True
            self.end_event = "BoxHeader"

    def toggle(self):
        """Toggle does not need to do anything this event."""
        pass


class Exit():
    def __init__(self, player):
        """Create the exit dialogue event."""
        self.is_dead = False
        self.player = player

        # Confirm that the user wants to leave the PC
        self.response_box = ResponseBox(["Yes", "No"], (185, 90), width=7)
        self.dialogue = FRAMES.getFrame(join("pc", "exit_box.png"))

    def draw(self, draw_surface):
        """Draw the response box and question."""
        self.response_box.draw(draw_surface)
        draw_surface.blit(self.dialogue, (84, 131))

    def handle_event(self, event):
        """Handle the response box events."""
        self.response_box.handle_event(event)

        if self.response_box.is_dead:
            self.is_dead = True
            if self.response_box.response == 0:
                self.end_event = "ConfirmExit"
            else:
                self.end_event = "CloseBox"

    def toggle(self):
        pass

    def update(self, ticks):
        """Update the response box."""
        self.response_box.update(ticks)


class PokemonSelectedEvent():
    def __init__(self, box, prev=None):
        """Run as a subevent of either Box or MoveEvent. Allows the player to
        choose what they want to do when they click on a box slot."""
        self.box = box
        self.is_dead = False
        if prev is None:
            box.pokemon_grabbed = box.cursor_pos

        # Grab the pokemon that the player selected
        try:
            x, y = box.pokemon_grabbed
            self.pokemon_selected = box.box[y][x]

        except IndexError:
            # Catch the case when a pokemon does not exist at the spot
            self.pokemon_selected = None

        # Find first option of the list
        if prev is None:
            first = "MOVE"
        elif self.pokemon_selected is None:
            first = "PLACE"
        else:
            first = "SHIFT"

        self.options = [first, "SUMMARY", "WITHDRAW", "MARK", "RELEASE",
                        "CANCEL"]

        # If a previous pokemon has been selected -- which will only happen
        # when PokemonSelectedEvent is being run as a subevent of
        # PokemonMoveEvent -- then use the previous pokemon's info for the
        # dialogue.
        if prev is not None:
            self.pokemon_selected = prev

        if prev is None and self.pokemon_selected is None:
            self.is_dead = True
            self.end_event = None
            return

        # Create the options box and dialogue.
        self.options_box = \
            ResponseBox(self.options, (240, 128), width=9, end_at=True)
        self.create_dialogue_box()

    def draw(self, draw_surface):
        """Draw the options box and the dialogue."""
        draw_surface.blit(self.dialogue_box, (84, 131))
        self.options_box.draw(draw_surface)

    def update(self, ticks):
        """This event does not need to do anything during the update cycle."""
        pass

    def handle_event(self, event):
        """Allow the options box to handle user input until the user has
        selected an option. Once the user has selected and option pass control
        to the appropriate event."""
        self.options_box.handle_event(event)
        if self.options_box.is_dead:
            response = self.options_box.response
            self.is_dead = True

            # Correct plan of action when the user selects the first option
            # changes based on what that option was.
            if response == 0:

                # If it was move then control will be passed back to the Box
                # event and that Box event will then pass control to the
                # PokemonMoveEvent created here.
                if self.options[0] == "MOVE":
                    self.end_event = \
                        PokemonMoveEvent(self.box, self.pokemon_selected)

                # This happens when the selected event is being run as a
                # subevent of PokemonMoveEvent. Here we simply tell the move
                # event to place the currently held pokemon.
                elif self.options[0] == "PLACE":
                    self.end_event = "place"

                # This happens when the selected event is being run as a
                # subevent of PokemonMoveEvent. Tell the move event to switch
                # the pokemon in its hand with the pokemon at the current slot.
                else:
                    self.end_event = "shift"
            elif response == 1:
                self.end_event = SummaryMenuPC(self.box.player, 0,
                                               self.box.box)
            elif response == 2:
                pass
            elif response == 3:
                pass
            elif response == 4:
                pass
            else:
                self.end_event = None

    def create_dialogue_box(self):
        """Create the dialogue box asking the player what they want to do with
        the selected pokemon."""
        # Create dialogue box surface and add the dialogue frame to the surface
        dialouge_box = FRAMES.getFrame(join("pc", "dialogue_box.png"))
        self.dialogue_box = pygame.Surface(dialouge_box.get_size())
        self.dialogue_box.set_colorkey((0, 0, 0))
        self.dialogue_box.blit(dialouge_box, (0, 0))

        # Create string and blit it to dialogue box
        poke = self.pokemon_selected
        tm = TextMaker(join("fonts", "party_txt_font.png"), 240)
        text_surf = \
            tm.get_surface(f'{poke.nick_name} is selected.')
        self.dialogue_box.blit(text_surf, (10, 11))

    def is_over(self):
        return self.is_dead

    def toggle(self):
        pass


class PokemonMoveEvent():
    def __init__(self, box, pokemon_selected):
        """Event that controls what happens when a player is holding a pokemon
        while inside the box. Run as a subevent of the Box event."""
        self.box = box
        self.is_dead = False
        self.grabbed_location = self.box.cursor_pos
        self.grabbed_box = self.box.box_number
        self.pokemon_selected = pokemon_selected

        # Remove pokemon from previous spot.
        x, y = self.grabbed_location
        self.box.box[y][x] = None

        # Create the small pokemon image that the hand will grab and carry
        # around.
        self._create_bouncing()

        # Start the grab animation.
        self.box.hand.grab(self.pokemon_selected_img)

        # Will only exist when two pokemon are being swapped
        self.top_pokemon = None
        self.redraw_on_switch = False

        self.placing = False

        self.sub_event = None

    def draw(self, draw_surface):
        """Draw the pokemon being held and the active subevent if it
        exists."""
        self.pokemon_selected_img.draw(draw_surface)
        if self.top_pokemon is not None:
            self.top_pokemon.draw(draw_surface)

        if self.sub_event is not None:
            self.sub_event.draw(draw_surface)

    def update(self, ticks):
        """Update the subevent if it exists."""
        if self.redraw_on_switch and not self.box.hand.switching:
            self.redraw_on_switch = False
            self.box.create_pokemon_surface()
            self.top_pokemon = None

        if self.sub_event is not None:
            self.sub_event.update(ticks)

        if self.placing:
            if not self.box.hand.placing:
                self.is_dead = True
                self.placing = False
                self.box.create_pokemon_surface()

    def handle_event(self, event):
        """Handle events. Respond accordingly once events are finished. """
        if self.box.hand.grabbing or self.box.hand.placing or \
                self.box.hand.switching:
            return

        if self.sub_event is not None:
            self.sub_event.handle_event(event)
            if self.sub_event.is_dead:
                next_event = self.sub_event.end_event
                if next_event == "place":
                    # Place the pokemon and remove it from its old spot in the
                    # box.
                    self._prepare_place()

                if next_event == "shift":
                    # Switch the two pokemon.
                    self._prepare_shift()

                else:
                    self.sub_event = None
            return

        elif event.key == BattleActions.SELECT.value:
            # If the player selects a spot then create a select event.
            self.box.pokemon_grabbed = self.box.cursor_pos
            self.sub_event = PokemonSelectedEvent(self.box,
                                                  prev=self.pokemon_selected)
        else:
            # The player is moving the cursor around. Let the box handle the
            # movement.
            self.box._handle_event_helper(event)

            # Make sure to update the position of the pokemon so it travels
            # with the hand.
            x, y = self.box.cursor_pos
            pos = tuple(sum(x) for x in zip((25 * x, 24 * y),
                                            (self.box.box_pos[0] - 1,
                                             self.box.box_pos[1] - 24)))
            self.pokemon_selected_img._position = pos

    def _prepare_place(self):
        """Place the pokemon and remove it from its old spot in the
        box."""
        self.box.hand.place(self.pokemon_selected_img)
        x, y = self.box.cursor_pos  # Pokemon's new pos.
        x1, y1 = self.grabbed_location  # Pokemon's old pos.

        # Place the pokemon
        self.box.player.pc_boxes[self.grabbed_box][y1][x1], self.box.box[y][x] = \
            None, self.pokemon_selected

        self.end_event = None

        self.placing = True

    def _prepare_shift(self):
        """Switch the pokemon in your hand for the pokemon selected."""
        x, y = self.box.cursor_pos  # Coords for the current spot.
        poke2 = self.box.box[y][x]  # The new pokemon.

        # Clear the pokemon in the spot and then redraw.
        self.box.box[y][x] = None
        self.box.create_pokemon_surface()

        # Hold for the time being so it can be passed to the hand
        # to animate the switch.
        self.top_pokemon = self.pokemon_selected_img

        # Switch what is in hand and put what is in hand in the
        # spot that is being clicked on.
        self.box.box[y][x] = self.pokemon_selected
        self.pokemon_selected = poke2
        self._create_bouncing()

        # Animate the switch
        self.box.hand.switch(self.top_pokemon,
                             self.pokemon_selected_img)

        self.redraw_on_switch = True

        self.sub_event = None

    def _create_bouncing(self):
        """Create the pokemon image which will be grabbed by the hand"""
        x, y = self.box.cursor_pos

        # Need to make sure to add on the second tuple because unlike the box,
        # we are blitting directly onto the screen instead of the box surface.
        # This second tuple is the location the box is draw in the box class.
        pos = tuple(sum(x) for x in zip((25 * x, 24 * y),
                                        (self.box.box_pos[0] - 1,
                                         self.box.box_pos[1] - 18)))
        self.pokemon_selected_img = \
            BouncingPokemon(self.pokemon_selected, pos)
        self.pokemon_selected_img._world_bound = False

    def box_changed(self, box):
        """Runs whenever a move_event is still active whenever the box changes.
        Puts pokemon and hand in correct spot."""
        self.box = box
        self._create_bouncing()
        x, y = self.pokemon_selected_img._position
        self.pokemon_selected_img._position = (x, y - 6)
        self.box.hand._frame = self.box.hand._nFrames - 1
        self.box.hand.get_current_frame()

    def is_over(self):
        return self.is_dead

    def toggle(self):
        pass


class BoxHand(Animated):
    def __init__(self):
        """Creates a box hand capable of picking up / putting down a
        pokemon."""
        super().__init__(join("pc", "box_hand.png"), [0, 0])
        self._world_bound = False
        self._framesPerSecond = 8
        self._nFrames = 4
        self.grabbing = False
        self.placing = False
        self.switching = False
        self.motion = "none"
        self.stopAnimation()

        self.last_pos = self._position

    def update(self, ticks):
        """Update the update function to add support for a grabbing
        animation."""
        frame = self._frame
        super().update(ticks)

        # Handle grabs
        if self.grabbing:
            if self._frame != frame or self.motion == "up":
                delta = 2 if self.motion == "down" else -2
                self._position = (self._position[0], self._position[1] + delta)

                # When going up with the hand take pokemon with hand
                if delta < 0:
                    self.pokemon._position = \
                        (self.pokemon._position[0],
                         self.pokemon._position[1] + delta)

                if self._frame == self._nFrames - 1:
                    if self.motion == "down":
                        self.motion = "up"
                        self.stopAnimation()

            if self._position == self.return_pos and self.motion == "up":
                self.grabbing = False
                self._frame = self._nFrames - 1
                self.get_current_frame()

        # Handle placing
        elif self.placing:
            if self._frame != frame or self.motion == "down":
                delta = 2 if self.motion == "down" else -2
                self._position = (self._position[0],
                                  self._position[1] + delta)

                # Make sure to drop the pokemon off.
                if delta > 0 and self.pokemon_moved < 6:
                    self.pokemon_moved += delta
                    self.pokemon._position = \
                        (self.pokemon._position[0],
                         self.pokemon._position[1] + delta)

                if self._position == (self.return_pos[0],
                                      self.return_pos[1] + 8):
                    self.motion = "up"
                    self.startAnimation()
                    self.backwards = True

            if self._position == self.return_pos and self.motion == "up":
                self.placing = False
                self.backwards = False
                self._frame = 0
                self.stopAnimation()

        # Handle swapping
        elif self.switching:
            self.switch_timer += ticks
            if self.switch_timer > .05:
                self.switch_timer -= .05
                if len(self.poke1_coords) > 0:
                    self.pokemon1._position = self.poke1_coords.pop(0)
                    self.pokemon2._position = self.poke2_coords.pop(0)
                else:
                    self.switching = False

    def grab(self, pokemon):
        """Trigger a grabbing animation."""
        self.grabbing = True
        self.return_pos = self._position
        self.motion = "down"
        self.pokemon = pokemon
        self.startAnimation()

    def place(self, pokemon):
        """Trigger a placing animation."""
        self.placing = True
        self.return_pos = self._position
        self.motion = "down"
        self.pokemon = pokemon
        self.pokemon_moved = 0

    def switch(self, pokemon1, pokemon2):
        """Trigger the switch animation."""
        self.switching = True
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.switch_timer = 0

        # Create the paths that the pokemon will follow.

        # Top pokemon
        start_x, start_y = pokemon1._position
        self.poke1_coords = [
            (start_x - 3, start_y + 1), (start_x - 4, start_y + 3),
            (start_x - 3, start_y + 5), (start_x, start_y + 6)
        ]
        # Bottom pokemon
        start_x, start_y = pokemon2._position
        self.poke2_coords = [
            (start_x + 3, start_y - 1), (start_x + 4, start_y - 3),
            (start_x + 3, start_y - 5), (start_x, start_y - 6)
        ]
