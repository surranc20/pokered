import pygame
from .response_box import ResponseBox
from .dialogue import Dialogue
from ..utils.UI.tileset_tile import TilesetTile
from ..utils.managers.soundManager import SoundManager


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
                self.end_event = Box(self.player)
            self.is_dead = True

    def is_over(self):
        return self.is_dead


class Box():
    pass
