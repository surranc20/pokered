import pygame
import json
import textwrap
from os.path import join
from .enumerated.battle_actions import BattleActions
from .utils.drawable import Drawable
from .battle.battle import Battle

class Dialogue():
    def __init__(self, dialogue_id, player, npc, box=0):
        self._dialogue_frame = Drawable("dialog_boxes.png", (0, 116), offset=(0, box), world_bound=False)
        self._line_surface = pygame.Surface((self._dialogue_frame.getSize()))
        self._player = player
        self._npc = npc

        # Get line from json
        with open(join("jsons", "lines.json"), "r") as lines_json:
            lines = json.load(lines_json)
            self._dialogue = lines[dialogue_id][0]
            self._end_battle = bool(lines[dialogue_id][1])
        self._dialogue = self._dialogue.split("\n")
        self._current_line = 0
        self._blit_line()
        

    def _blit_line(self):
        print(self._current_line)
        if self._current_line == len(self._dialogue):
            self._current_line += 1
            return
        self._line_surface.fill((255, 255, 255))
        self._line_surface.set_colorkey((255,255,255))
        self._font = pygame.font.Font(join("fonts", "pokemon_fire_red.ttf"), 16)
        string_lyst = textwrap.wrap(self._dialogue[self._current_line], width=60)
        height = 10
        for string in string_lyst:
            rendered = self._font.render(string, False, (200, 200, 200))
            self._line_surface.blit(rendered, (10, height))
            height += 15
        self._current_line += 1
        
    
    def draw(self, draw_surface):
        self._dialogue_frame.draw(draw_surface)
        draw_surface.blit(self._line_surface, (0, 120))

    def update(self, ticks):
        pass

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

    

    