import pygame
from os.path import join
from .battle.battle import Battle
from .dialogue import Dialogue
from .utils.mobile import Mobile
from .enumerated.cardinality import Cardinality

class Trainer(Mobile):
    def __init__(self, position, name, facing, enemy=True, dialogue_id=None, event=None, gender="male"):
        """Creates a trainer instance. Expects the trainer's position, orientation in the world. Optionally expects
        whether or not the trainer is an enemy, the dialouge id associated with the trainer, the event that happens
        when interacting with the trainer, and the gender of the trainer."""
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
        self._event = event
        self._dialogue_id = dialogue_id
        self._gender = gender
    
    def all_dead(self):
        """Returns if all of the trainers pokemon are dead."""
        for pokemon in self._pokemon_team:
            if pokemon._stats["Current HP"] > 0:
                return False
        return True
    
    def get_pokemon_team(self):
        """Returns the pokemon team of the trainer."""
        return self._pokemon_team
    
    def is_enemy(self):
        """Returns whether or not the trainer is the enemy."""
        return self._is_enemy

    def get_active_pokemon(self):
        """Returns the trainer's active pokemon."""
        return self._active_pokemon
    
    def set_active_pokemon(self, index):
        """Sets the trainer's active pokemon to the pokmeon at the provided index."""
        self._active_pokemon = self.get_pokemon_team()[index]

    def get_pokemon_by_index(self, index):
        """Returns the pokemon at the specified index."""
        print(self.get_pokemon_team()[index])
        return self.get_pokemon_team()[index]
    
    def get_name(self):
        """Returns the name of the trainer."""
        return self._name
    
    def update(self, ticks, nearby_tiles, current_tile):
        """Updates the trainer. Right now it does not need to do anything."""
        pass

    def talk_event(self, player):
        """Returns the talke event associated with the trainer."""
        return Dialogue(str(self._dialogue_id), player, self, gender=self._gender)
    
    def heal_all(self):
        """Heals all of the trainer's pokemon."""
        for pokemon in self._pokemon_team:
            pokemon._stats["Current HP"] = pokemon._stats["HP"]
            for move in pokemon.get_moves():
                move.reset_pp()