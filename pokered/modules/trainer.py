import pygame
from os.path import join
from .battle.battle import Battle
from .utils.mobile import Mobile
from .enumerated.cardinality import Cardinality

class Trainer(Mobile):
    def __init__(self, position, name, facing, enemy=True):
        if not enemy:
            super().__init__("trainer.png", position, facing)
        else:
            super().__init__(join("trainers", name + ".png"), position,  Cardinality.NORTH)

        self._nFrames = 1
        self._framesPerSecond = 6
        self._running = False
        self._moving = False
        self._pokemon_team = []
        self._active_pokemon = None
        self._is_enemy = enemy
        self._name = name.upper()
        self._key_down_timer = 0
        self._wait_till_next_update = 0
        self._walk_event = None
    
    def get_pokemon_team(self):
        return self._pokemon_team
    
    def is_enemy(self):
        return self._is_enemy

    def get_active_pokemon(self):
        return self._active_pokemon
    
    def set_active_pokemon(self, index):
        self._active_pokemon = self.get_pokemon_team()[index]
    
    def get_pokemon_team(self):
        return self._pokemon_team

    def get_pokemon_by_index(self, index):
        print(self.get_pokemon_team()[index])
        return self.get_pokemon_team()[index]
    
    def get_name(self):
        return self._name
    
    def update(self, ticks, nearby_tiles, current_tile):
        pass

    def talk_event(self, player):
        return Battle(player, self)