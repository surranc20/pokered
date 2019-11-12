import json
from os.path import join
from ..level import Level


class LevelManager(object):
    def __init__(self, player, level_name, screen_size =(240, 160)):
        self._player = player
        self._level_name = level_name
        self._screen_size = screen_size
        self._active_battle = None
        self._level = Level(level_name, player, screen_size)
    

    def draw(self, draw_surface):
        if self._active_battle == None:
            self._level.draw(draw_surface)

        else:
            self._active_battle.draw(draw_surface)
      
    def handle_event(self, event):
        if self._active_battle == None:
            self._player.handle_event(event)
        else:
            self._active_battle.handle_event(event)
      
    def update(self, ticks):
        if self._active_battle == None:
            self._level.update(ticks)
        else:
            self._active_battle.update(ticks)