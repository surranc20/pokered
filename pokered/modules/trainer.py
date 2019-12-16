import pygame
from os.path import join
from .battle.battle import Battle
from .events.dialogue import Dialogue
from .utils.UI.mobile import Mobile
from .enumerated.cardinality import Cardinality

class Trainer(Mobile):
    def __init__(self, position, name, facing, enemy=True, dialogue_id=None, battle_dialogue_id=None, post_battle_dialogue_id=None, event=None, gender="male"):
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
        self.pokemon_team = []
        self.active_pokemon = None
        self.is_enemy = enemy
        self.name = name.upper()
        self._key_down_timer = 0
        self._wait_till_next_update = 0
        self._walk_event = None
        self.event = event
        self._dialogue_id = dialogue_id
        self._battle_dialogue_id = battle_dialogue_id
        self._post_battle_dialogue_id = post_battle_dialogue_id
        self.gender = gender
        self.defeated = False

    def all_dead(self):
        """Returns if all of the trainers pokemon are dead."""
        for pokemon in self.pokemon_team:
            if pokemon.stats["Current HP"] > 0:
                return False
        return True

    def get_pokemon_team(self):
        """Returns the pokemon team of the trainer."""
        return self.pokemon_team

    def is_enemy(self):
        """Returns whether or not the trainer is the enemy."""
        return self.is_enemy

    def get_active_pokemon(self):
        """Returns the trainer's active pokemon."""
        return self.active_pokemon

    def set_active_pokemon(self, index):
        """Sets the trainer's active pokemon to the pokmeon at the provided index."""
        self.active_pokemon = self.get_pokemon_team()[index]

    def get_pokemon_by_index(self, index):
        """Returns the pokemon at the specified index."""
        return self.get_pokemon_team()[index]

    def get_name(self):
        """Returns the name of the trainer."""
        return self.name

    def update(self, ticks, nearby_tiles, current_tile):
        """Updates the trainer. Right now it does not need to do anything."""
        pass

    def talk_event(self, player):
        """Returns the talke event associated with the trainer."""
        if not self.defeated:
            return Dialogue(str(self._dialogue_id), player, self, gender=self.gender)
        else:
            return Dialogue(str(self._post_battle_dialogue_id), player, self, gender=self.gender)

    def heal_all(self):
        """Heals all of the trainer's pokemon."""
        for pokemon in self.pokemon_team:
            pokemon.stats["Current HP"] = pokemon.stats["HP"]
            for move in pokemon.get_moves():
                move.reset_pp()