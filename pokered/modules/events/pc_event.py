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
        self.box_header = BoxHeader(box_number)
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
        self.box.draw(draw_surface)
        self.close_box.draw(draw_surface)
        self.party_pokemon.draw(draw_surface)

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
    def __init__(self, player, box_number=0):
        """Sub event which is responsible for drawing the box and all pokemon
        inside of the box. Also keeps track of the cursor and moves it
        around."""
        self.player = player
        self.box_number = box_number
        self.box_pos = [84, 43]
        offset = (box_number % 4, box_number // 4)
        self.box_background = \
            FRAMES.getFrame(join("pc", "box_backgrounds.png"),
                            offset)

        self.cursor_pos = [0, 0]
        self.create_pokemon_surface()

        self.hand = FRAMES.getFrame(join("pc", "hands.png"), (0, 0))
        self.pokemon_data = PokemonData(None)

        self.is_dead = True

    def draw(self, draw_surface):
        """Draws everything."""
        draw_surface.blit(self.box_background, self.box_pos)
        draw_surface.blit(self.pokemon_surface,
                          (self.box_pos[0] - 1, self.box_pos[1] - 18))

        self.pokemon_data.draw(draw_surface)

        if not self.is_dead:
            draw_surface.blit(self.hand,
                              (90 + self.cursor_pos[0] * 25,
                               20 + self.cursor_pos[1] * 24))

    def create_pokemon_surface(self):
        """Create the surface that displays all of the pokemon in the box."""
        self.pokemon_surface = pygame.Surface((156, 130))
        self.pokemon_surface.set_colorkey((0, 0, 0))
        for y, row in enumerate(self.player.pc_boxes):
            for x, pokemon in enumerate(row):
                if pokemon is not None:
                    poke = BouncingPokemon(pokemon, (25 * x, 24 * y),
                                           item=False)
                    poke._world_bound = False
                    poke.draw(self.pokemon_surface)

    def handle_event(self, event):
        """Handles the updating of the cursor."""
        pokemon_changed = False
        if event.key == BattleActions.UP.value:
            if self.cursor_pos[1] > 0:
                self.cursor_pos[1] -= 1
                pokemon_changed = True
            else:
                self.toggle()
                self.end_event = "BoxHeader"
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

        if pokemon_changed:
            pokemon = \
                self.player.pc_boxes[self.cursor_pos[1]][self.cursor_pos[0]]
            self.pokemon_data = PokemonData(pokemon)

    def toggle(self):
        """Toggles the box on and off."""
        self.is_dead = not self.is_dead
        if self.pokemon_data.pokemon is None:
            pokemon = \
                self.player.pc_boxes[self.cursor_pos[1]][self.cursor_pos[0]]
            self.pokemon_data = PokemonData(pokemon)
        else:
            self.pokemon_data = PokemonData(None)

    def update(self, ticks):
        """Updates the pokemon data side bar."""
        self.pokemon_data.update(ticks)


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
        offset = (box_number % 4, box_number // 4)
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
        self.left_arrow.set_pos_no_off([self.left_arrow._position[0] + delta,
                                        self.left_arrow._position[1]])

        self.right_arrow.set_pos_no_off([self.right_arrow._position[0] + delta,
                                         self.right_arrow._position[1]])


class BoxSwitch():
    def __init__(self, direction, box, header):
        """Create a box switch event which transitions between boxes."""
        self.is_dead = False
        self.direction = 1 if direction == "right" else -1

        # Grab the header and box that are currently on display
        self.box = box
        self.header = header

        # Grab the box that is being transitioned to.
        box_number = (self.box.box_number + self.direction) % 12
        header_pos = [270, 18] if direction == "right" else [-70, 18]
        self.new_header = BoxHeader(box_number, header_pos=header_pos)
        self.new_box = Box(self.box.player, box_number)
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
