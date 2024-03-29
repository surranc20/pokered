import pygame
import random
from .events.menu import Menu
from .trainer import Trainer
from .pokemon import Pokemon
from .bag import Bag
from .move import Move
from .enumerated.cardinality import Cardinality
from .enumerated.battle_actions import BattleActions


class Player(Trainer):
    # Create the base payout dict which gives the base price a trainer
    # must pay after losing a battle based on the number of gym badges
    # that the player has.
    BASE_PAYOUT = {
        0: 8,
        1: 16,
        2: 24,
        3: 36,
        4: 48,
        5: 60,
        6: 80,
        7: 100,
        8: 120
    }

    def __init__(self, position, name, enemy=False):
        """Creates an instance of a player. Requires the player's start
        position, and name."""
        super().__init__(position, name, Cardinality.NORTH, enemy=False)
        self.badges = []
        self.rival_name = "Gary"
        self.money = 1200
        self.hidden_inventory = []
        self.pokedex = "National"
        self.has_first_pokemon = True
        self.bag = Bag()

        self.pc_options = ["BILL'S PC", f"{name.upper()}'s PC",
                           "PROF. OAK's PC", "HALL OF FAME",
                           "LOG OFF"]

        self._create_pc_box()
        # Temporary code for test box
        pokes = ["charizard", "pikachu", "bulbasaur", "raichu"]
        for row in range(5):
            for slot in range(5):
                self.pc_boxes[0][row][slot] = Pokemon(random.choice(pokes))
                self.pc_boxes[0][row][slot].trainer_id = "65535"
                self.pc_boxes[0][row][slot].original_trainer = "RED"
                self.pc_boxes[0][row][slot].add_move(Move("Thunder"))
                self.pc_boxes[0][row][slot].add_move(Move("Thunderbolt"))
                self.pc_boxes[0][row][slot].add_move(Move("Thunder Wave"))
                self.pc_boxes[0][row][slot].add_move(Move("Double Slap"))

    def handle_event(self, event, nearby_tiles):
        """Handles the events from the level manager. Is capable of taking
        control away from the player if a movement scipt is active."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RSHIFT:
            self._moving = False
            return Menu(self)
        if self._move_script_active is None:
            if (event.type == pygame.KEYDOWN or
                    event.type == pygame.KEYUP) and \
                    event.key in [pygame.K_w, pygame.K_a, pygame.K_s,
                                  pygame.K_d, pygame.K_b]:
                self.move(event)
            elif event.type == pygame.KEYDOWN and \
                    event.key == BattleActions.SELECT.value:
                return nearby_tiles[self._orientation].talk_event(self)
        else:
            return

    def move(self, event):
        """Updates the players moving, flip, and orientation values based on
        the event"""
        # If wasd have been presed then set the correct cardinality and set
        # moving to be true. The flip value is only true when the player is
        # moving EAST. This allows us to flip the horizontal running animation.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            self._orientation = Cardinality.NORTH
            self._moving = True
            self._flip = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            self._orientation = Cardinality.WEST
            self._moving = True
            self._flip = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            self._orientation = Cardinality.SOUTH
            self._moving = True
            self._flip = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            self._orientation = Cardinality.EAST
            self._moving = True
            self._flip = True

        # When b is pressed the player is running which doubles movement speed
        # (not actually implemented)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            self.start_running()

        # If no more wasd keys are held down then the player stops moving
        if event.type == pygame.KEYUP and event.key in \
                [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
            if self.input_matches_travel(event):

                # Make sure that no other wasd key is pressed. If one is, then
                # start moving in that direction.
                still_pressed = [x for x in pygame.key.get_pressed() if x in
                                 [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]]  # NOQA
                if still_pressed != []:
                    return self.move(pygame.event.Event(pygame.KEYDOWN,
                                                        {key: still_pressed[0]}))  # NOQA
                else:
                    self._moving = False
                    self._key_down_timer = 0

        if event.type == pygame.KEYUP and event.key == pygame.K_b:
            self.stop_running()

        # ABS is used because EAST and WEST should both point to row 2 but
        # need to have distint values. Because of this WEST = -2 and to get to
        # the correct row we simply take the absolute value.
        self._row = abs(self._orientation.value)

    def payout(self):
        """Calculates and then pays the payout incurred after losing a
        battle. Returns the amount payed."""
        base_payout = self.BASE_PAYOUT[len(self.badges)]
        money_lost = base_payout * self.highest_level

        # The player can not lose more money than they have
        if money_lost - self.money > 0:
            payout = self.money
        else:
            payout = money_lost
        self.money -= payout
        return payout

    def start_running(self):
        """Player starts running."""
        self._running = True
        self._framesPerSecond = 8

    def stop_running(self):
        """Player stops running."""
        self._runnign = False
        self._framesPerSecond = 4

    def add_items(self, item_name, quantity):
        self.bag.add_item(item_name, quantity)

    @property
    def highest_level(self):
        """Returns the level of the player's highest level pokemon (that
        is in their current party)."""
        return max(pokemon.lvl for pokemon in self.pokemon_team)

    def input_matches_travel(self, event):
        """Return true if the user is going up and pressing 'w' or 's' and
        south...Otherwise return false."""
        return (event.key == pygame.K_w and
                self._orientation == Cardinality.NORTH) or \
            (event.key == pygame.K_s and
                self._orientation == Cardinality.SOUTH) or \
            (event.key == pygame.K_d and
                self._orientation == self._orientation.EAST) or \
            (event.key == pygame.K_a and
                self._orientation == Cardinality.WEST)

    def _create_pc_box(self):
        """Creates the player's pc box."""
        self.pc_boxes = []
        for x in range(14):
            box = []
            for x in range(5):
                box.append([None] * 6)
            self.pc_boxes.append(box)
