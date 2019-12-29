import json
from os.path import join
from .events.dialogue import Dialogue
from .utils.UI.mobile import Mobile
from .utils.UI.drawable import Drawable
from .utils.vector2D import Vector2
from .enumerated.cardinality import Cardinality
from .utils.managers.soundManager import SoundManager


class Trainer(Mobile):
    BASE_PAYOUT = {
        "Beauty": 80,
        "Biker": 20,
        "Bird Keeper": 24,
        "Black Belt": 24,
        "Boss": 80,
        "Bug Catcher": 12,
        "Burglar": 12,
        "Channeler": 88,
        "Ace Trainer": 48,
        "Roughneck": 32,
        "Engineer": 48,
        "Fisher": 40,
        "Gambler": 72,
        "Gentleman": 72,
        "Grunt": 20,
        "Hiker": 36,
        "Camper": 20,
        "Picnicker": 40,
        "Juggler": 40,
        "Lass": 16,
        "Poké Maniac": 48,
        "Psychic": 24,
        "Rocker": 24,
        "Super Nerd": 24,
        "Swimmer": 4,
        "Sailor": 40,
        "Scientist": 48,
        "Tamer": 40,
        "Youngster": 16,
        "Guitarist": 32,
        "Poké Fan": 80,
        "School Kid": 32,
        "Twins": 20,
        "Admin": 32,
        "Aroma Lady": 40,
        "Battle Girl": 24,
        "Bug Maniac": 60,
        "Collector": 60,
        "Cool Couple": 48,
        "Crush Girl": 24,
        "Crush Kin": 48,
        "Dragon Tamer": 48,
        "Expert": 48,
        "Hex Maniac": 24,
        "Interviewer": 96,
        "Kindler": 32,
        "Lady": 200,
        "Ninja Boy": 12,
        "Old Couple": 80,
        "Painter": 16,
        "Parasol Lady": 40,
        "Pokémon Breeder": 40,
        "Pokémon Ranger": 36,
        "Rich Boy": 200,
        "Ruin Maniac": 48,
        "Sis and Bro": 8,
        "Teammates": 32,
        "Triathlete": 40,
        "Tuber": 4,
        "Young Couple": 64,
        "Leader": 100,
        "Elite Four": 100,
        "Champion": 200,
        "Pokémon Trainer": 200,
        "Rival": 36
        }

    def __init__(self, position, name, facing, enemy=True, dialogue_id=None,
                 battle_dialogue_id=None, post_battle_dialogue_id=None,
                 event=None, gender="male", type="Pokémon Trainer"):
        """Creates a trainer instance. Expects the trainer's position,
        orientation in the world. Optionally expects whether or not the
        trainer is an enemy, the dialouge id associated with the trainer, the
        event that happens when interacting with the trainer, and the gender
        of the trainer."""
        if not enemy:
            super().__init__("trainer.png", position, facing)
        else:
            super().__init__(join("trainers", name + ".png"), position,
                             self._parse_cardinality(facing))

        self._nFrames = 4
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
        self.event = None if event == "None" else event
        self.post_battle_dialogue_id = post_battle_dialogue_id
        self.gender = gender
        self.defeated = False
        self.current_tile = 0
        self._move_script_active = None
        self._last_wall_bump = 0
        self._talk_queued = False
        self.trainer_type = type

        if enemy:
            # Get battle dialogues lines/ids
            with open(join("jsons", "lines.json"), "r") as lines_json:
                lines = json.load(lines_json)
                self.battle_dialogue = lines[str(battle_dialogue_id)][0]
            self.post_battle_dialogue_id = post_battle_dialogue_id
            self._dialogue_id = dialogue_id

            self.battle_image = \
                Drawable(join("trainers", self.name.lower() + "_b.png"),
                         Vector2(240, 10))
        else:
            self.battle_image = \
                Drawable(join("battle", "trainer_toss_anim.png"),
                         Vector2(240, 80), (0, 0))

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
        """Sets the trainer's active pokemon to the pokmeon at the provided
        index."""
        self.active_pokemon = self.get_pokemon_team()[index]

    def get_pokemon_by_index(self, index):
        """Returns the pokemon at the specified index."""
        return self.get_pokemon_team()[index]

    def get_name(self):
        """Returns the name of the trainer."""
        return self.name

    def update(self, ticks, nearby_tiles, current_tile):
        """Updates the trainer class's position"""
        # print(current_tile)
        self.current_tile = current_tile
        if self._move_script_active is not None:
            self._move_to_tile(self._move_script_active)
        if self._moving:
            self.startAnimation()
            self._key_down_timer += ticks
            self._last_wall_bump += ticks

            # If the player is not in the middle of crossing a tile then start
            # a walk event.
            if self._walk_event is None:
                if self._current_image_row != self._row:
                    self.get_current_frame()
                if nearby_tiles[self._orientation].is_clear():
                    if self._key_down_timer > .2:
                        self._walk_event = [0, self._orientation]
                else:
                    # Make sure walking frame is displayed
                    self._frame = 0
                    self.get_current_frame()

                    # Play the wall bump sound based on timer if player
                    # continously walks into wall.
                    if self._last_wall_bump > .7:
                        SoundManager.getInstance().playSound(
                            "firered_0007.wav",
                            sound=1
                            )
                        self._last_wall_bump = self._last_wall_bump - .7

        # This ensures the player travels a full tile once they have begun
        # moving.
        if self._walk_event is not None:
            Mobile.update(self, ticks)
            self._wait_till_next_update += ticks
            self._walk_event[0] += 1

            if self._walk_event[1] == Cardinality.WEST:
                self._position.x -= 1
            elif self._walk_event[1] == Cardinality.SOUTH:
                self._position.y += 1
            elif self._walk_event[1] == Cardinality.NORTH:
                self._position.y -= 1
            elif self._walk_event[1] == Cardinality.EAST:
                self._position.x += 1
            if self._walk_event[0] == 16:
                nearby_tiles[self._walk_event[1]].add_obj(self)
                current_tile.remove_obj()
                self._walk_event = None

        # Stop the player from animating if no button is pressed and not in
        # the middle of a walk event.
        if not self._moving and self._walk_event is None:
            self._key_down_timer = 0
            self._walk_event = None
            self._frame = 0
            self._last_wall_bump = 0
            self.stopAnimation()

    def move_to_tile(self, tile_pos):
        """Allows the implementation of movement scripting. The player will
        move until they reach the tile provided."""
        self._move_script_active = tile_pos
        return self.current_tile.pos == tile_pos

    def turn(self, direction):
        self._orientation = direction
        self._row = abs(self._orientation.value)
        self._flip = True if self._orientation == Cardinality.EAST else False
        self.get_current_frame()

    def _move_to_tile(self, tile_pos):
        """Helper function that implements the above functionality. Helps
        determine whether or not the script is over."""
        if self.current_tile.pos != tile_pos:
            self._orientation = self.determine_direction_to_tile(tile_pos)
            self._moving = True
            return False
        else:
            self._moving = False
            self._move_script_active = None
            return True

    def determine_direction_to_tile(self, tile_pos):
        """Helper method to determine the cardinal direction to a tile."""
        if self.current_tile.pos == tile_pos:
            return self._orientation
        else:

            if tile_pos[0] > self.current_tile.pos[0]:
                direction = Cardinality.EAST
            elif tile_pos[0] < self.current_tile.pos[0]:
                direction = Cardinality.WEST
            elif tile_pos[1] > self.current_tile.pos[1]:
                direction = Cardinality.SOUTH
            else:
                direction = Cardinality.NORTH

            self._row = abs(direction.value)
            return direction

    def talk_event(self, player):
        """Returns the talke event associated with the trainer."""
        # Create the talk event
        if not self.defeated:
            return Dialogue(str(self._dialogue_id),
                            player,
                            self,
                            gender=self.gender)
        else:
            return Dialogue(str(self.post_battle_dialogue_id),
                            player,
                            self,
                            gender=self.gender)

    def heal_all(self):
        """Heals all of the trainer's pokemon."""
        for pokemon in self.pokemon_team:
            pokemon.stats["Current HP"] = pokemon.stats["HP"]
            for move in pokemon.get_moves():
                move.reset_pp()

    def payout(self):
        """Returns the amount of money that the trainer type pays out after a
        loss."""
        return self.pokemon_team[-1].lvl * self.BASE_PAYOUT[self.trainer_type]

    def _parse_cardinality(self, card_string):
        if card_string == "north":
            return Cardinality.NORTH
        elif card_string == "south":
            return Cardinality.SOUTH
        elif card_string == "east":
            return Cardinality.EAST
        else:
            return Cardinality.WEST
