import json
from os.path import join
from ..level import Level
from ..player import Player
from ..pokemon import Pokemon
from ..battle.battle import Battle
from .vector2D import Vector2


class LevelManager(object):
    def __init__(self, player, level_name, screen_size =(240, 160)):
        self._player = player
        self._level_name = level_name
        self._screen_size = screen_size
        enemy = Player(Vector2(30,30), "CHAMPION GARY", enemy=True)
        enemy._pokemon_team.append(Pokemon("charizard", enemy=True))
        enemy._pokemon_team.append(Pokemon("pikachu", enemy=True))
        enemy._pokemon_team.append(Pokemon("charizard", enemy=True))
        self._active_battle = None #Battle(player, enemy)
        self._level = Level(level_name, player, screen_size)
    

    def draw(self, draw_surface):
        if self._active_battle == None:
            self._level.draw(draw_surface)

        else:
            self._active_battle.draw(draw_surface)
      
    def handle_event(self, event):
        if self._active_battle == None:
            self._active_battle = self._player.handle_event(event, self._level.get_nearby_tiles(self._player._current_tile._pos))
        else:
            self._active_battle.handle_event(event)
      
    def update(self, ticks):
        print(self._active_battle)
        if self._active_battle == None:
            self._level.update(ticks)
        else:
            self._active_battle.update(ticks)