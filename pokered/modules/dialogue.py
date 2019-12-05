import pygame
import json
import textwrap
from os.path import join
from .enumerated.battle_actions import BattleActions
from .utils.drawable import Drawable
from .battle.battle import Battle
from .text_cursor import TextCursor

class Dialogue():
    def __init__(self, dialogue_id, player, npc, box=0):
        self._dialogue_frame = Drawable("dialog_boxes.png", (0, 110), offset=(0, box), world_bound=False)
        self._line_surface = pygame.Surface((self._dialogue_frame.getSize()[0] - 10, self._dialogue_frame.getSize()[1] ))
        self._player = player
        self._npc = npc
        self._text_cursor = TextCursor((0,0))
        self._text_cursor.activate()

        # Get line from json
        with open(join("jsons", "lines.json"), "r") as lines_json:
            lines = json.load(lines_json)
            self._dialogue = lines[dialogue_id][0]
            self._end_battle = bool(lines[dialogue_id][1])

        self._dialogue = self._dialogue.split("\n")
        self._font = pygame.font.Font(join("fonts", "pokemon_fire_red.ttf"), 15)
        self._current_line = 0
        self._blit_line()
        

    def _blit_line(self):
        print(self._current_line)
        if self._current_line == len(self._dialogue):
            self._current_line += 1
            return
        self._line_surface.fill((255, 255, 255))
        self._line_surface.set_colorkey((255,255,255))
        string_lyst = textwrap.wrap(self._dialogue[self._current_line], width=41)
        height = 10
        for string in string_lyst:
            rendered = self._font.render(string, False, (232, 81, 78))
            self._line_surface.blit(rendered, (10, height))
            height += 15
        self._current_line += 1

        self._text_cursor.set_pos((rendered.get_width() + 10, height))
        
    
    def draw(self, draw_surface):
        self._dialogue_frame.draw(draw_surface)
        draw_surface.blit(self._line_surface, (6, 111))
        self._text_cursor.draw(draw_surface)


    def update(self, ticks):
        self._text_cursor.update(ticks)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == BattleActions.SELECT.value:
            self._blit_line()
    
    def is_over(self):
        return self._current_line == len(self._dialogue) + 1
    
    def get_end_event(self):
        if self._end_battle:
            return Battle(self._player, self._npc)
        else:
            return None

    

    