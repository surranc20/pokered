import pygame
from os.path import join
from .response_box import ResponseBox
from .dialogue import Dialogue
from ..battle.battle_menus.poke_party import BouncingPokemon
from ..utils.UI.tileset_tile import TilesetTile
from ..utils.UI.text_cursor import TextCursor
from ..utils.managers.soundManager import SoundManager
from ..utils.managers.frameManager import FRAMES
from ..utils.text_maker import TextMaker
from ..utils.misc import center
from ..enumerated.battle_actions import BattleActions


class PCEvent():
    def __init__(self, player, pc_pos):
        self.player = player
        self.is_dead = False
        self.shutting_down = False
        self.turned = True

        self.pc_pos = pc_pos

        # Create the initial prompt to ask user what they want to do in pc
        self.active_sub_event = TurnOn(player, pc_pos)

    def draw(self, draw_surface):
        self.active_sub_event.draw(draw_surface)

    def update(self, ticks):
        self.active_sub_event.update(ticks)

        if self.active_sub_event.is_over():
            if self.shutting_down:
                self.is_dead = True

            elif self.active_sub_event.super_kill:
                self.shutting_down = True
                self.turned = False
                self.active_sub_event = TurnOff(self.player, self.pc_pos)

            else:
                self.active_sub_event = self.active_sub_event.end_event

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        self.active_sub_event.handle_event(event)

    def is_over(self):
        return self.is_dead

    def get_end_event(self):
        return "Level"


class TurnOff():
    def __init__(self, player, pc_pos):
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
        self.screen.draw(draw_surface)
        self.player.draw(draw_surface)

    def update(self, ticks):
        if self.end_timer > 0:
            self.end_timer -= ticks
        else:
            self.is_dead = True

    def handle_event(self, event):
        pass

    def is_over(self):
        return self.is_dead


class TurnOn():
    def __init__(self, player, pc_pos):
        self.player = player
        self.is_dead = False
        self.super_kill = False
        self.end_event = ChoosePC(player)

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
        self.screen.draw(draw_surface)
        self.player.draw(draw_surface)

    def update(self, ticks):
        if self.flicker_count < 5:
            self.flicker_timer += ticks
            if self.flicker_timer > 1 / self.fps:
                self.flicker_count += 1

                self.on = not self.on
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
        pass

    def is_over(self):
        return self.is_dead


class ChoosePC():
    def __init__(self, player):
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
        self.response_box.draw(draw_surface)
        self.dialogue.draw(draw_surface)

    def update(self, ticks):
        self.response_box.update(ticks)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        self.response_box.handle_event(event)

        if self.response_box.is_dead:
            if self.player.pc_options[self.response_box.cursor.cursor] == \
                    "LOG OFF":
                self.super_kill = True
            elif self.player.pc_options[self.response_box.cursor.cursor] == \
                    "BILL'S PC":
                self.end_event = BillsPC(self.player)
            self.is_dead = True

    def is_over(self):
        return self.is_dead


class BillsPC():
    def __init__(self, player):
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
        self.response_box.draw(draw_surface)
        self.dialogue.draw(draw_surface)

    def update(self, ticks):
        self.response_box.update(ticks)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        self.response_box.handle_event(event)
        self.dialogue = Dialogue(f'pc{self.response_box.cursor.cursor}',
                                 self.player, self.player,
                                 gender=self.player.gender, show_curs=False,
                                 turn=False)

        if self.response_box.is_dead:
            if self.box_options[self.response_box.cursor.cursor] == "SEE YA!":
                self.end_event = ChoosePC(self.player)
            elif self.box_options[self.response_box.cursor.cursor] == \
                    "WITHDRAW POKéMON":
                self.end_event = BoxScreen(self.player)
            self.is_dead = True

    def is_over(self):
        return self.is_dead


class BoxScreen():
    def __init__(self, player, box_number=0):
        self.player = player
        self.is_dead = False
        self.super_kill = False

        self.pc_background = FRAMES.getFrame(join("pc", "pc_background.png"))
        self.box_header = BoxHeader(box_number)
        self.close_box = BoxButton(join("pc", "close_box.png"), (170, 0))
        self.box = Box(player, box_number)

        self.party_pokemon = BoxButton(join("pc", "party_pokemon.png"),
                                       (83, 0))

    def draw(self, draw_surface):
        draw_surface.blit(self.pc_background, (0, 0))
        self.box_header.draw(draw_surface)
        self.box.draw(draw_surface)
        self.close_box.draw(draw_surface)
        self.party_pokemon.draw(draw_surface)

    def update(self, ticks):
        self.box_header.update(ticks)

    def handle_event(self, event):
        self.box.handle_event(event)

    def is_over(self):
        return self.is_dead


class Box():
    def __init__(self, player, box_number=0):
        self.player = player
        offset = (box_number % 4, box_number // 4)
        self.box_background = \
            FRAMES.getFrame(join("pc", "box_backgrounds.png"),
                            offset)

        self.cursor_pos = (0, 0)
        self.create_pokemon_surface()

        self.hand = FRAMES.getFrame(join("pc", "hands.png"), (0, 0))
        self.cursor_pos = [0, 0]

    def draw(self, draw_surface):
        draw_surface.blit(self.box_background, (84, 43))
        draw_surface.blit(self.pokemon_surface, (83, 25))
        draw_surface.blit(self.hand,
                          (90 + self.cursor_pos[0] * 25,
                           25 + self.cursor_pos[1] * 24))

    def create_pokemon_surface(self):
        self.pokemon_surface = pygame.Surface((156, 130))
        self.pokemon_surface.set_colorkey((0, 0, 0))
        for y, row in enumerate(self.player.pc_boxes):
            for x, pokemon in enumerate(row):
                if pokemon is not None:
                    poke = BouncingPokemon(pokemon, (25 * x, 24 * y))
                    poke._world_bound = False
                    poke.draw(self.pokemon_surface)

    def handle_event(self, event):
        if event.key == BattleActions.UP.value:
            if self.cursor_pos[1] > 0:
                self.cursor_pos[1] -= 1
        elif event.key == BattleActions.DOWN.value:
            if self.cursor_pos[1] < 4:
                self.cursor_pos[1] += 1
        elif event.key == BattleActions.LEFT.value:
            if self.cursor_pos[0] > 0:
                self.cursor_pos[0] -= 1
        elif event.key == BattleActions.RIGHT.value:
            if self.cursor_pos[0] < 5:
                self.cursor_pos[0] += 1


class BoxButton():
    def __init__(self, button_path, pos):
        self.pos = pos
        self.button_path = button_path
        self.selected = False

        self.button_image = FRAMES.getFrame(button_path, offset=(0, 0))

    def toggle(self):
        self.selected = not self.selected
        if self.selected:
            self.button_image = \
                FRAMES.getFrame(self.button_path, offset=(1, 0))
        else:
            self.button_image = \
                FRAMES.getFrame(self.button_path, offset=(0, 0))

    def draw(self, draw_surface):
        draw_surface.blit(self.button_image, self.pos)


class BoxHeader():
    def __init__(self, box_number):
        self.selected = False

        offset = (box_number % 4, box_number // 4)
        self.header_image = FRAMES.getFrame(join("pc", "box_headers.png"),
                                            offset)

        self.left_arrow = TextCursor((90, 23),
                                     name=join("pc", "box_arrows.png"),
                                     horizontal=True, offset=(0, 0),
                                     invert=True)

        self.right_arrow = TextCursor((226, 23),
                                      name=join("pc", "box_arrows.png"),
                                      horizontal=True, offset=(1, 0))

        right_arrow_color_key = self.right_arrow._image.get_at((7, 0))
        self.right_arrow._image.set_colorkey(right_arrow_color_key)

        self.left_arrow.activate()
        self.right_arrow.activate()

        self.make_title_surf()

    def draw(self, draw_surface):
        draw_surface.blit(self.header_image, (100, 18))
        self.left_arrow.draw(draw_surface)
        self.right_arrow.draw(draw_surface)
        draw_surface.blit(self.title_surf,
                          center(self.title_surf, 100, 224, 22))

    def update(self, ticks):
        self.left_arrow.update(ticks)
        self.right_arrow.update(ticks)

    def toggle(self):
        self.left_arrow.reset()
        self.right_arrow.reset()
        self.left_arrow.should_update = not self.left_arrow.should_update
        self.right_arrow.should_update = not self.right_arrow.should_update

    def make_title_surf(self):
        text_maker = TextMaker(join("fonts", "menu_font.png"), 240)
        self.title_surf = text_maker.get_surface("TESTING")
