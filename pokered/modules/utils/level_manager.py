from .vector2D import Vector2
from .drawable import Drawable
from ..player import Player
from ..pokemon import Pokemon
from ..battle.battle import Battle

class LevelManager(object):
    def __init__(self, player, screen_size =(240, 160)):
        self._player = player
        self._level_size = (200, 200)
        self._screen_size = screen_size
        enemy = Player(Vector2(0,0), "CHAMPION GARY", enemy=True)
        enemy._pokemon_team.append(Pokemon("charizard", enemy=True))
        enemy._pokemon_team.append(Pokemon("pikachu", enemy=True))
        enemy._pokemon_team.append(Pokemon("charizard", enemy=True))
        self._active_battle = Battle(player, enemy)

    def draw(self, draw_surface):
        if self._active_battle == None:
            pass
        else:
            self._active_battle.draw(draw_surface)
      
    def handle_event(self, event):
        if self._active_battle == None:
            self._player.handle_event(event)
        else:
            self._active_battle.handle_event(event)
      
    def update(self, ticks):
        if self._active_battle == None:
            self._player.update(ticks)
            Drawable.updateWindowOffset(self._player, self._screen_size, self._level_size)
        else:
            self._active_battle.update(ticks)