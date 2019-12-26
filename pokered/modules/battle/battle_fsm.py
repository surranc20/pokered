import pygame
import textwrap
import random
import sys
from os.path import join
from ..utils.UI.drawable import Drawable
from ..utils.vector2D import Vector2
from ..animations.toss_pokemon import TossPokemon
from ..animations.change_hp import ChangeHP
from ..animations.poke_death import PokeDeath
from ..animations.moves import *
from ..animations.moves.generic.hit import Hit
from ..utils.managers.soundManager import SoundManager
from ..enumerated.battle_actions import BattleActions
from ..enumerated.battle_states import BattleStates
from ..utils.UI.text_cursor import TextCursor
from .battle_menus.poke_info import PokeInfo
from .battle_menus.poke_party import PokeParty
from .damage_calculator import DamageCalculator

# TODO: Never display the number of pokemon remaining


class BattleFSM:

    TRANSITIONS = {
        (BattleStates.CHOOSING_FIGHT_OR_RUN, 0): BattleStates.CHOOSING_MOVE,
        (BattleStates.CHOOSING_FIGHT_OR_RUN, 1):
            BattleStates.CHOOSING_FIGHT_OR_RUN,
        (BattleStates.CHOOSING_FIGHT_OR_RUN, 2): BattleStates.CHOOSING_POKEMON,
        (BattleStates.CHOOSING_FIGHT_OR_RUN, 3): BattleStates.RUNNING,
        (BattleStates.CHOOSING_FIGHT_OR_RUN, BattleActions.BACK):
            BattleStates.CHOOSING_FIGHT_OR_RUN,
        BattleStates.CHOOSING_MOVE: BattleStates.CHOOSE_OPPONENT_ACTION,
        BattleStates.RUNNING: BattleStates.CHOOSING_FIGHT_OR_RUN,
        (BattleStates.CHOOSING_POKEMON, BattleActions.BACK):
            BattleStates.CHOOSING_FIGHT_OR_RUN,
        (BattleStates.CHOOSING_MOVE, BattleActions.BACK):
            BattleStates.CHOOSING_FIGHT_OR_RUN,
        BattleStates.DISPLAY_EFFECT: BattleStates.CHOOSING_FIGHT_OR_RUN,
        BattleStates.MOVE_MISSED: BattleStates.CHOOSING_FIGHT_OR_RUN,
        BattleStates.MULTI_HIT_TEXT: BattleStates.CHOOSING_FIGHT_OR_RUN,
        BattleStates.PARALYZED_CANT_MOVE: BattleStates.CHOOSING_FIGHT_OR_RUN
    }

    def __init__(self, player, opponent, state=BattleStates.NOT_STARTED):
        """Creates the battle fsm. This object keeps track of the current
        state of the battle and also fascilitates the various actions that can
        be taken. The transitions dictionary specefies the next state to
        travel to based on which state you are currently in and sometimes the
        position of the cursor. This dictionary is only used in a select
        few states. This dictionary helps eliminate some if statements from
        the logic of the code."""
        # Variable that keeps track of the state of the battle.
        self._state = state

        # Occasionally a certain state will need to que up multiple states
        # that need to happen one after another.
        self._state_queue = []

        # The font used in text wait events
        self._font = pygame.font.Font(join("fonts", "pokemon_fire_red.ttf"), 16)

        # The cursor that keeps track of where the player is clicking
        self._cursor = Cursor()

        # The animation that is currently playing. If this is a list then it
        # is a collection of animations.
        self._active_animation = None

        # The string that will be rendered in the next text wait event
        self._active_string = None

        # The cursor that bounces up and down when waiting for player to hit
        # enter.
        self._text_cursor = TextCursor((0, 0))

        # The opponent and player objects
        self._opponent = opponent
        self._player = player

        # These are placeholder objects and just exist to save a certain space
        # in the draw list for the corresponding object.
        self._active_player_pokemon = None
        self._active_opponent_pokemon = None
        self._player_poke_info = None
        self._opponent_poke_info = None

        # The player and opponents queued move. If it is equal to None at the
        # end of the selecting actions phase then then the player will do
        # nothing.
        self._player_move_queued = None
        self._enemy_move_queued = None

        # List containing the move order of a specefic turn
        self._turn_order = []

        # Variable that keeps track of whether or not the initial battle
        # animations are over.
        self._initial_stage_over = False

        # How long a text_wait state has been displaying its text.
        self._text_wait_timer = 0

        # The scrolling background of a move it it exists.
        self._scrolling_background_surf = None

        # Various objects that will be drawn to the screen in the battle.
        self._background = Drawable(join("battle", "battle_background.png"),
                                    Vector2(0, 0), offset=(0, 0))
        self._battle_text_background = Drawable(join("battle", "battle_menus.png"),
                                                Vector2(0, 112), offset=(0, 1))
        self._move_select = Drawable(join("battle", "battle_menus.png"),
                                     Vector2(0, 113), offset=(0, 0))
        self._fight_run = Drawable(join("battle", "battle_menus.png"),
                                   Vector2(120, 113), offset=(0, 2))

        # The list of objects that need to be drawn and updated.
        self._draw_list = [self._background,
                           self._battle_text_background,
                           self._active_player_pokemon,
                           self._active_opponent_pokemon,
                           self._player_poke_info,
                           self._opponent_poke_info,
                           self._text_cursor]

        self._update_list = [self._player_poke_info,
                             self._opponent_poke_info,
                             self._text_cursor]

        # Keeps track of whether the battle is over and whether or not the
        # player lost.
        self._is_over = False
        self._player_lost = False

    def is_over(self):
        """Returns whether or not the battle is over."""
        return self._is_over

    def get_draw_list(self):
        """Get the currrent draw list so that the battle object knows what to
        draw."""
        draw_list = [item for item in self._draw_list if item is not None and
                     not item.is_dead()]

        if self._active_animation is not None:
            if self._scrolling_background_surf is not None:
                draw_list.insert(1, self._scrolling_background_surf)
            if type(self._active_animation) == list:
                for anim in self._active_animation:
                    draw_list.append(anim)
            else:
                draw_list.append(self._active_animation)
        return draw_list

    def get_update_list(self):
        """Get the currrent update list so that the battle object knows what
        to update."""
        update_list = [item for item in self._update_list if item is not None
                       and not item.is_dead()]

        if self._active_animation is not None:
            print(self._active_animation)
            if type(self._active_animation) == list:
                for anim in self._active_animation:
                    update_list.append(anim)
            else:
                update_list.append(self._active_animation)

        return update_list

    def update(self, ticks):
        """The update loop for the battle fsm. Most of the logic of the battle
        occurs here. Is organized by both state and the states value."""

        # This only occurs at the very start of the battle. Handles all of the
        # intro animations.
        if self._state == BattleStates.NOT_STARTED:
            self._state_queue = [BattleStates.TEXT_WAIT,
                                 BattleStates.OPPONENT_TOSSING_POKEMON,
                                 BattleStates.PLAYER_TOSSING_POKEMON,
                                 BattleStates.CHOOSING_FIGHT_OR_RUN]
            self._active_string = self._opponent.name.upper() + \
                " would like to battle!"
            self._state = self._state_queue.pop(0)
            self._player.set_active_pokemon(0)
            self._opponent.set_active_pokemon(0)

            self._draw_list.append(
                TossPokemon(self._player.active_pokemon.name,
                            self._player,
                            lead_off=True,
                            enemy=False)
                )

            self._draw_list.append(
                TossPokemon(self._opponent.active_pokemon.name,
                            self._opponent,
                            lead_off=True,
                            enemy=True)
                )

        # Handles updates if the battle is over
        if self._state == BattleStates.BATTLE_OVER:
            self._is_over = True

        # Triggers if the value of the current state is text wait. This groups
        # similar functionality together.
        if self._state.value[0] == "text wait":
            self._update_text_wait(ticks)

        # Triggers if the value of the current state is compute. An event is a
        # compute event if it does not need to print anything to the screen or
        # wait for user input.
        elif self._state.value[0] == "compute":
            self._update_compute(ticks)

        # An event is an auto event if the event consists of an animation that
        # needs to play.
        elif self._state.value[0] == "auto":
            self._update_auto(ticks)

    def _update_text_wait(self, ticks):
        # Sometimes the active string will be "" and if this is the case the
        # text wait will end after the timer is up.
        self._text_wait_timer += ticks
        if self._active_string is not None and self._active_string != "":
            # Different states need the text to be displayed at different
            # widths.
            self._handle_text_wait_active_string_update()

        # Go to next state at the end of the timer if the active string is the
        # empty string.
        elif self._active_string == "":
            self._handle_text_wait_empty_string_update()

    def _handle_text_wait_empty_string_update(self):
        if self._text_wait_timer > .2:
            self._text_wait_timer = 0
            if len(self._state_queue) > 0:
                self._active_string = None
                self._handle_state_change(self._state_queue.pop(0))
            else:
                self._active_string = None
                self._handle_state_change(self.TRANSITIONS[self._state])

    def _handle_text_wait_active_string_update(self):
        if self._state == BattleStates.UPDATE_PLAYER_STATUS_EFFECT \
                or self._state == BattleStates.UPDATE_ENEMY_STATUS_EFFECT \
                or self._state == BattleStates.PARALYZED_CANT_MOVE:
            self._text_cursor.set_pos(self._wrap_text(40))
        else:
            self._text_cursor.set_pos(self._wrap_text(25))
        # Make sure the text cursor bobs up and down at the end of the
        # string.
        self._text_cursor.activate()
        self._active_string = None

    def _update_compute(self, ticks):
        # As of right now the only action the player can select is choosing a
        # move to use.
        if self._state == BattleStates.CHOOSE_OPPONENT_ACTION:
            self._handle_state_change(BattleStates.OPPONENT_CHOOSING_MOVE)

        # The opponent chooses the move to use and then the current state is
        # set to Deciding Battle Order
        elif self._state == BattleStates.OPPONENT_CHOOSING_MOVE:
            self._update_opponent_choosing_move()

        # The player has won. Triggers the series of events that happens after
        # the player wins
        elif self._state == BattleStates.VICTORY:
            self._update_victory()

        # The player has lost. Triggers the series of events that happens
        # after the player has lost.
        elif self._state == BattleStates.DEFEAT:
            self._update_defeat()

        # Decides the battle order. Depends on whether or not each player has
        # queued an action and the speeds of the pokemon.
        elif self._state == BattleStates.DECIDING_BATTLE_ORDER:
            self._update_deciding_battle_order()

        # Queues up the individual steps of a battle turn.
        elif self._state == BattleStates.EXECUTE_TURN:
            self._update_execute_turn()

        # Checks the health of a pokemon after it has taken damage to see if
        # it is still alive and handle accordingly.
        elif self._state == BattleStates.CHECK_HEALTH:
            self._update_check_health()

        # Make the appropriate state change if an opponent's pokemon has died.
        elif self._state == BattleStates.OPPONENT_POKEMON_DIED:
            # If all the opponent's pokemon are dead then the player has won
            # the battle.
            self._update_opponent_pokemon_died()

        # Does the exact same as the OPPONENT_POKEMON_DIED except for the
        # player.
        elif self._state == BattleStates.PLAYER_POKEMON_DIED:
            self._update_player_pokemon_died()

        # Opponent chooses a pokemon that is eligible to be sent out into the
        # battle.
        elif self._state == BattleStates.OPPONENT_CHOOSING_POKEMON:
            while self._opponent.active_pokemon.stats["Current HP"] <= 0:
                self._opponent.set_active_pokemon(random.randint(0, 4))
            self._handle_state_change(self._state_queue.pop(0))

        # Check to make sure the player's pokemon can move. This means
        # checking for statuses like paralysis.
        elif self._state == BattleStates.CHECK_PLAYER_CAN_MOVE \
                or self._state == BattleStates.CHECK_OPPONENT_CAN_MOVE:
            self._update_can_move()

    def _update_can_move(self):
        can_move = self._player.active_pokemon.can_move() \
            if self._state == BattleStates.CHECK_PLAYER_CAN_MOVE \
            else self._opponent.active_pokemon.can_move()
        # If the player can not move then remove all the states pertaining to
        # the player from the battle queue.
        if can_move is not True:
            while True:
                self._state_queue.pop(0)
                if self._state_queue == [] \
                        or (self._state_queue[0] ==
                            BattleStates.CHECK_PLAYER_CAN_MOVE) \
                        or (self._state_queue[0] ==
                            BattleStates.CHECK_OPPONENT_CAN_MOVE):
                    break

            # If the player could not move then specify why. Right now only
            # paralysis is implemented.
            self._state_queue.insert(0, BattleStates.PARALYZED_CANT_MOVE)

        # If there is a chance that the pokmeon could not move but did move
        # state why (if a pokemon is paralyzed it prints this out in the
        # battle text box each turn).
        if self._state == BattleStates.CHECK_PLAYER_CAN_MOVE:
            status = self._player.active_pokemon.status
        else:
            status = self._opponent.active_pokemon.status

        if "paralyze" in status:
            self._can_move_paralyze()

        # After the above state has been added to the queue go to said state.
        self._handle_state_change(self._state_queue.pop(0))

    def _can_move_paralyze(self):
        self._state_queue.insert(0, BattleStates.PARALYZED)
        if self._state == BattleStates.CHECK_PLAYER_CAN_MOVE:
            self._active_string = self._player.active_pokemon.name.upper()
        else:
            self._active_string = self._opponent.active_pokemon.name.upper() \
                + " is paralyzed!"

    def _update_player_pokemon_died(self):
        if self._player.all_dead():
            self._handle_state_change(BattleStates.DEFEAT)
        else:
            self._state_queue = [BattleStates.TEXT_WAIT,
                                 BattleStates.PLAYER_FEINT,
                                 BattleStates.CHOOSING_POKEMON,
                                 BattleStates.CHOOSING_FIGHT_OR_RUN]
            self._active_string = \
                self._player.active_pokemon.name.capitalize() + " fainted!"
            self._handle_state_change(self._state_queue.pop(0))

    def _update_opponent_pokemon_died(self):
        # If all the opponent's pokemon are dead then the player has won
        # the battle.
        if self._opponent.all_dead():
            self._state_queue = [BattleStates.OPPONENT_FEINT,
                                 BattleStates.VICTORY]
            self._handle_state_change(self._state_queue.pop(0))

        # Otherwise populate the state queue with the sequence of states that
        # play when a pokemon dies.
        else:
            self._state_queue = [BattleStates.TEXT_WAIT,
                                 BattleStates.OPPONENT_FEINT,
                                 BattleStates.OPPONENT_CHOOSING_POKEMON,
                                 BattleStates.OPPONENT_TOSSING_POKEMON,
                                 BattleStates.CHOOSING_FIGHT_OR_RUN]
            self._active_string = "Foe " + \
                self._opponent.active_pokemon.name.capitalize() + " fainted!"
            self._handle_state_change(self._state_queue.pop(0))

    def _update_check_health(self):
        if self._player.active_pokemon.stats["Current HP"] <= 0:
            self._handle_state_change(BattleStates.PLAYER_POKEMON_DIED)
        elif self._opponent.active_pokemon.stats["Current HP"] <= 0:
            self._handle_state_change(BattleStates.OPPONENT_POKEMON_DIED)
        else:
            if self._state_queue == []:
                self._handle_state_change(BattleStates.CHOOSING_FIGHT_OR_RUN)
            else:
                self._handle_state_change(self._state_queue.pop(0))

    def _update_execute_turn(self):
        # For each player that has a move queued add each phase of
        # executing that move Note: if checking whether or not the
        # player/enemy can move yields the result that they cannot move
        # then the rest of the states pertaining to that player will be
        # removed from the state queue after the checking process.
        for player in self._turn_order:
            self._state_queue.append(BattleStates.CHECK_PLAYER_CAN_MOVE
                                     if player == self._player
                                     else BattleStates.CHECK_OPPONENT_CAN_MOVE)
            self._state_queue.append(BattleStates.PLAYER_MOVE_TEXT
                                     if player == self._player
                                     else BattleStates.OPPONENT_MOVE_TEXT)

            # Decide whether or not the move hits
            accuracy = (self._player_move_queued.accuracy
                        if player == self._player
                        else self._enemy_move_queued.accuracy)
            if random.randint(0, 100) > accuracy:
                self._state_queue.append(BattleStates.MOVE_MISSED)

            # If the move hits add the rest of the states pertaining to
            # executing the move to the state queue.
            else:
                num_hits = (self._player_move_queued.get_num_hits()
                            if player == self._player
                            else self._enemy_move_queued.get_num_hits())
                # This for loop is neccessary because some move hit more than
                # one time in a turn (double slap for example).
                self._populate_player_turn_state_queue(num_hits, player)

                # If a move is a multi hit move it displays how many times it
                # hits.
                if num_hits > 1:
                    # This variable is neccesary because Multi Hit Text needs
                    # to know how many times the move hit.
                    self._num_hits = num_hits
                    self._state_queue.append(BattleStates.MULTI_HIT_TEXT)

        # Add nothing to the state queue if nobody used a move and return to
        # the choosing action screen.
        if self._state_queue == []:
            self._handle_state_change(BattleStates.CHOOSING_FIGHT_OR_RUN)

        # Go to the first state in the newly generated queue
        else:
            self._handle_state_change(self._state_queue.pop(0))

    def _populate_player_turn_state_queue(self, num_hits, player):
        for x in range(num_hits):
            self._state_queue.append((BattleStates.PLAYER_MOVE_ANIMATION
                                      if player == self._player
                                      else BattleStates.ENEMY_MOVE_ANIMATION))
            self._state_queue.append((BattleStates.UPDATE_ENEMY_STATUS
                                      if player == self._player
                                      else BattleStates.UPDATE_PLAYER_STATUS))
            self._state_queue.append(BattleStates.DISPLAY_EFFECT)
            self._state_queue.append((BattleStates.UPDATE_ENEMY_STATUS_EFFECT
                                      if player == self._player
                                      else BattleStates.UPDATE_PLAYER_STATUS_EFFECT))
            self._state_queue.append(BattleStates.CHECK_HEALTH)

    def _update_deciding_battle_order(self):
        if self._player_move_queued is None and self._enemy_move_queued is None:
            self._turn_order = []
        elif self._player_move_queued is None and self._enemy_move_queued is not None:
            self._turn_order.append(self._opponent)
        elif self._player_move_queued is not None and self._enemy_move_queued is None:
            self._turn_order.append(self._player)
        else:
            if (self._player.active_pokemon.stats["Speed"] >=
                    self._opponent.active_pokemon.stats["Speed"]):
                self._turn_order.append(self._player)
                self._turn_order.append(self._opponent)
            else:
                self._turn_order.append(self._opponent)
                self._turn_order.append(self._player)
        self._handle_state_change(BattleStates.EXECUTE_TURN)

    def _update_defeat(self):
        self._player_lost = True
        self._state_queue = [BattleStates.TEXT_WAIT, BattleStates.BATTLE_OVER]
        self._active_string = "Player was defeated by " + \
            self._opponent.name.upper() + "!"
        self._handle_state_change(self._state_queue.pop(0))

    def _update_victory(self):
        self._state_queue = [BattleStates.TEXT_WAIT, BattleStates.VICTORY_TEXT,
                             BattleStates.BATTLE_OVER]
        self._active_string = "Player defeated " + \
            self._opponent.name.upper() + "!"
        self._handle_state_change(self._state_queue.pop(0))

    def _update_opponent_choosing_move(self):
        while True:
            self._enemy_move_queued = \
                self._opponent.active_pokemon.moves[random.randint(0, 3)]
            if self._enemy_move_queued.category in ["Physical", "Special"]:
                print(self._enemy_move_queued.move_name)
                break
        self._handle_state_change(BattleStates.DECIDING_BATTLE_ORDER)

    def _update_auto(self, ticks):
        # If the active animation is None then grab the correct animation
        # based on what the current state is.
        if self._active_animation is None:

            # If the opponent is tossing out a pokemon then grab the
            # TossPokemon animation and which pokemon they are sending out to
            # the battle text box.
            if self._state == BattleStates.OPPONENT_TOSSING_POKEMON:
                self._update_opponent_tossing_pokemon()

            # If the player is tossing out a pokemon then grab the TossPokemon
            # animation and which pokemon they are sending out to the battle
            # text box. Operates in the same manner as the
            # OPPONENT_TOSSING_POKEMON state which is more thourougly
            # commented.
            if self._state == BattleStates.PLAYER_TOSSING_POKEMON:
                self._update_player_tossing_pokemon()

            # This state attempts to play the animation for the player's
            # currently selected move. If said animation does not exist then
            # it simply skips displaying the animation.
            if self._state == BattleStates.PLAYER_MOVE_ANIMATION:
                self._update_player_move_animation()

            # This state attempts to play the animation for the opponent's
            # currently selected move. If said animation does not exist then
            # it simply skips displaying the animation.
            if self._state == BattleStates.ENEMY_MOVE_ANIMATION:
                self._update_enemy_move_animation()

            # This state calculates the damage done by the move and if it is
            # greater than zero it animates the hp change and the player being
            # hit.
            if self._state == BattleStates.UPDATE_PLAYER_STATUS:
                self._update_player_status()

            # This state calculates the damage done by the move and if it is
            # greater than zero it animates the hp change and the opponent
            # being hit.
            if self._state == BattleStates.UPDATE_ENEMY_STATUS:
                self._update_enemy_status()

            # These states set the active animation to the active pokemon's
            # death animation.
            if self._state == BattleStates.OPPONENT_FEINT:
                self._active_animation = \
                    PokeDeath(self._opponent.active_pokemon)

            if self._state == BattleStates.PLAYER_FEINT:
                self._active_animation = PokeDeath(self._player.active_pokemon)

        # This code block controls auto states once the active animation for
        # the state has been set.
        else:
            # If the active animation is a list then we need to handle all of
            # the animations in the list.
            self._update_anim_done()

    def _update_anim_done(self):
        # If the active animation is a list then we need to handle all of
        # the animations in the list.
        if type(self._active_animation) == list:
            all_done = True
            # Check to see if all the animations are done.
            for anim in self._active_animation:
                if not anim.is_dead():
                    all_done = False
            # If all of the animations are done then go to the next state.
            if all_done:
                self._active_animation = None
                if len(self._state_queue) > 0:
                    self._handle_state_change(self._state_queue.pop(0))
                else:
                    self._handle_state_change(BattleStates.CHOOSE_OPPONENT_ACTION)

        # If the active animation is only one animation and that animation
        # is done do the following.
        elif self._active_animation.is_dead():
            self._active_animation = None

            # After the opponent has finished tossing a pokemon we need to
            # add that pokemon its corresponding poke info to the
            # draw/update list.
            if self._state == BattleStates.OPPONENT_TOSSING_POKEMON:
                self._draw_list[3] = self._opponent.active_pokemon
                op_poke_info = PokeInfo(self._opponent.active_pokemon,
                                        enemy=True)
                self._draw_list[5] = op_poke_info
                self._update_list[1] = op_poke_info

            # After the player has finished tossing a pokemon we need to
            # add that pokemon and its corresponding poke info to the
            # draw/update list.
            if self._state == BattleStates.PLAYER_TOSSING_POKEMON:
                self._draw_list[2] = self._player.active_pokemon
                self._player_poke_info = \
                    PokeInfo(self._player.active_pokemon)
                self._draw_list[4] = self._player_poke_info
                self._update_list[0] = self._player_poke_info

            # Go to the next state.
            if len(self._state_queue) > 0:
                self._handle_state_change(self._state_queue.pop(0))
            else:
                self._handle_state_change(BattleStates.CHOOSE_OPPONENT_ACTION)

    def _update_enemy_status(self):
        calc = DamageCalculator((self._player.active_pokemon,
                                 self._player_move_queued),
                                self._opponent.active_pokemon)
        dmg = calc.get_damage()
        if dmg > 0:
            self._active_animation = [ChangeHP(self._opponent.active_pokemon,
                                               dmg,
                                               calc.get_effectiveness_sound()),
                                      Hit(self._opponent.active_pokemon)]
        else:
            self._active_animation = []
        self._active_string = calc.get_effectiveness()

    def _update_player_status(self):
        calc = DamageCalculator((self._opponent.active_pokemon,
                                 self._enemy_move_queued),
                                self._player.active_pokemon)
        dmg = calc.get_damage()
        if dmg > 0:
            self._active_animation = [ChangeHP(self._player.active_pokemon,
                                      dmg,
                                      calc.get_effectiveness_sound()),
                                      Hit(self._player.active_pokemon)]
        else:
            self._active_animation = []

        # This is how effective the move was (super effective, not
        # very effective, no effect ...)
        self._active_string = calc.get_effectiveness()

    def _update_enemy_move_animation(self):
        try:
            self._active_animation = \
                getattr(sys.modules[__name__],
                        self._enemy_move_queued.move_name.replace(" ", ""))(self._opponent.active_pokemon,
                                                                            self._player.active_pokemon,
                                                                            enemy=True)
        except Exception:
            self._handle_state_change(self._state_queue.pop(0))

    def _update_player_move_animation(self):
        try:
            self._active_animation = \
                getattr(sys.modules[__name__],
                        self._player_move_queued.move_name.replace(" ", ""))(self._player.active_pokemon,
                                                                             self._opponent.active_pokemon)
        except Exception:
            self._handle_state_change(self._state_queue.pop(0))

    def _update_player_tossing_pokemon(self):
        self._active_string = "Go! " + \
            self._player.active_pokemon.nick_name.upper() + "!"
        self._wrap_text(20)
        if self._initial_stage_over:
            self._draw_list[2] = None
            self._draw_list[4] = None
            trainer_toss = TossPokemon(self._player.active_pokemon.name,
                                       self._player,
                                       lead_off=False,
                                       enemy=False)
        else:
            trainer_toss = self._draw_list.pop()
            # After the player has tossed their pokemon the initial
            # animation phase of the battle is over.
            self._initial_stage_over = True
        self._active_animation = trainer_toss

    def _update_opponent_tossing_pokemon(self):
        self._active_string = self._opponent.name.upper() + \
            " sent out " + self._opponent.active_pokemon.name.upper() \
            + "!"
        self._wrap_text(20)
        if self._initial_stage_over:
            self._draw_list[3] = None
            self._draw_list[5] = None
            trainer_toss = TossPokemon(self._opponent.active_pokemon.name,
                                       self._player,
                                       lead_off=False,
                                       enemy=True)

        # If this is the toss at the beginning of the battle grab the
        # toss animation from the last spot in the draw list. This was
        # added there in the BATTLE_NOT_STARTED state. We must do this
        # differently because we need the trainer to be standing still
        # at the start of the battle and we achieve this effect by
        # drawing the animation and simply not starting it.
        else:
            trainer_toss = self._draw_list.pop()
        self._active_animation = trainer_toss

    def handle_action(self, action):
        """Handles the actions that a user provides. Calls helper methods."""
        if self._state.value[0] == "text wait":
            self._handle_action_during_text_wait(action)
        elif self._state.value[0] == "wait":
            self._handle_action_during_wait(action)

    def _handle_action_during_wait(self, action):
        """Handles actions during a wait event."""
        if action.type == pygame.KEYDOWN:
            # If action is a navigation key being pressed (wasd)
            if action.key in [BattleActions.UP.value,
                              BattleActions.DOWN.value,
                              BattleActions.LEFT.value,
                              BattleActions.RIGHT.value]:
                # Grab the appropriate cursor and update its position
                if self._state == BattleStates.CHOOSING_POKEMON:
                    self._poke_party.change_cursor_pos(action)
                else:
                    self._cursor.change_cursor_pos(action)
                    if self._state == BattleStates.CHOOSING_MOVE:
                        self._pp_surface._update_cursor(self._cursor.get_value())

            # If the action is the select key being pressed then do one of the
            # following:
            if action.key == BattleActions.SELECT.value:
                # If in the choosing pokemon menu pass the action into the
                # poke party and get a response.
                if self._state == BattleStates.CHOOSING_POKEMON:
                    response = self._poke_party.handle_select_event(action)
                    # If the response is not go the state specified in the
                    # response.
                    if response is not None:
                        if self._state_queue != []:
                            self._state_queue.insert(0, response[0])
                            self._handle_state_change(self._state_queue.pop(0))
                        else:
                            self._handle_state_change(response[0])

                # If not in the choosing pokemon menu then travel to the state
                # specefied in the TRANSITION dictionary.
                else:
                    SoundManager.getInstance().playSound("firered_0005.wav")
                    if self._state == BattleStates.CHOOSING_MOVE:
                        self._player_move_queued = \
                            self._player.active_pokemon.moves[
                                self._cursor.get_move_corrected_value()
                                ]
                        self._handle_state_change(self.TRANSITIONS[self._state])
                    else:
                        self._handle_state_change(self.TRANSITIONS[
                                (self._state), self._cursor.get_value()])

            # If the action is the back key being pressed then go to the state
            # specefied in the TRANSITION dictionary.
            if action.key == BattleActions.BACK.value:
                if self._state == BattleStates.CHOOSING_POKEMON:
                    response = self._poke_party.handle_back_event()
                    if response == "change":
                        self._handle_state_change(self.TRANSITIONS[
                            (self._state), BattleActions.BACK])
                        SoundManager.getInstance().playSound("firered_0005.wav")

                else:
                    self._handle_state_change(self.TRANSITIONS[(self._state),
                                                               BattleActions.BACK])
                    SoundManager.getInstance().playSound("firered_0005.wav")

    def _handle_action_during_text_wait(self, action):
        """Handles actions during a text wait event."""
        if action.type == pygame.KEYDOWN \
                and action.key == BattleActions.SELECT.value:
            SoundManager.getInstance().playSound("firered_0005.wav")
            if len(self._state_queue) > 0:
                self._handle_state_change(self._state_queue.pop(0))
            else:
                self._handle_state_change(self.TRANSITIONS[self._state])

    def _handle_state_change(self, new_state):
        """This method cleans performs the visual changes necessary when
        performing a state change. The first half of the method cleans things
        up when leaving a particular state and the second half of the method
        adds things when changing to a state."""
        if self._state.value[0] == "text wait":
            self._text_cursor.deactivate()

        if self._state == BattleStates.CHOOSING_FIGHT_OR_RUN:
            self._draw_list.pop(self._draw_list.index(self._fight_run))
            self._draw_list.pop(self._draw_list.index(self._cursor))

        if self._state == BattleStates.CHOOSING_MOVE:
            self._draw_list.pop(self._draw_list.index(self._move_select))
            self._draw_list.pop(self._draw_list.index(self._pp_surface))
            self._draw_list.pop(self._draw_list.index(self._moves_surface))
            try:
                self._draw_list.pop(self._draw_list.index(self._cursor))
            except ValueError:
                pass
            self._cursor.deactivate()

        if self._state == BattleStates.CHOOSING_POKEMON:
            self._draw_list.pop()
            self._update_list.pop()

        if new_state == BattleStates.CHOOSING_FIGHT_OR_RUN:
            self._turn_order = []
            self._player_move_queued = None
            self._enemy_move_queued = None
            self._active_string = str("What will " +
                                      self._player.active_pokemon.name.upper()
                                      + " do?")
            self._wrap_text(16)
            self._draw_list.append(self._fight_run)
            self._draw_list.append(self._cursor)
            self._cursor.activate()
            self._cursor.set_positions(new_state)
            self._cursor.reset()

        elif new_state == BattleStates.CHOOSING_MOVE:
            self._cursor.set_positions(new_state)
            self._cursor.reset()
            self._draw_list.append(self._move_select)
            self._moves_surface = MovesSurface(self._player.active_pokemon)
            self._pp_surface = PPSurface(self._player.active_pokemon)
            self._draw_list.append(self._moves_surface)
            self._draw_list.append(self._pp_surface)
            self._draw_list.append(self._cursor)

        elif new_state == BattleStates.RUNNING:
            try:
                self._draw_list.pop(self._draw_list.index(self._cursor))
            except ValueError:
                pass
            self._active_string = "There is no running from a trainer battle!"

        elif new_state == BattleStates.CHOOSING_POKEMON:
            self._poke_party = PokeParty(self._player)
            self._draw_list.append(self._poke_party)
            self._update_list.append(self._poke_party)

        elif new_state == BattleStates.OPPONENT_MOVE_TEXT:
            self._enemy_move_queued.current_pp -= 1
            self._active_string = (self._opponent.active_pokemon.name.upper() +
                                   " used " +
                                   self._enemy_move_queued.move_name + "!")

        elif new_state == BattleStates.PLAYER_MOVE_TEXT:
            self._player_move_queued.current_pp -= 1
            self._active_string = (self._player.active_pokemon.name.upper() +
                                   " used " +
                                   self._player_move_queued.move_name + "!")

        elif new_state == BattleStates.MOVE_MISSED:
            self._active_string = "Its move missed!"

        elif new_state == BattleStates.MULTI_HIT_TEXT:
            self._active_string = "Hit " + str(self._num_hits) + " times!"
            self._num_hits = 1

        elif new_state == BattleStates.UPDATE_ENEMY_STATUS_EFFECT:
            calc = DamageCalculator((self._player.active_pokemon,
                                     self._player_move_queued),
                                    self._opponent.active_pokemon)

            effect = calc.get_effect()
            if effect is not None:
                self._opponent.active_pokemon.add_status(effect)
                if effect == "paralyze":
                    self._active_string = \
                        (self._opponent.name.upper() +
                         "'s " + self._opponent.active_pokemon.name.upper() +
                         " became paralyzd! It may not be able to move!")
            else:
                self._active_string = ""

        elif new_state == BattleStates.PARALYZED_CANT_MOVE:
            self._active_string = "It can't move!"

        elif new_state == BattleStates.UPDATE_PLAYER_STATUS_EFFECT:
            calc = DamageCalculator((self._opponent.active_pokemon,
                                     self._enemy_move_queued),
                                    self._player.active_pokemon)

            effect = calc.get_effect()
            if effect is not None:
                self._player.get_active_pokemon.add_status(effect)
                if effect == "paralyze":
                    self._active_string = \
                        ("Your " +
                         self._player.active_pokemon.name.upper() +
                         " became paralyzd! It may not be able to move!")
            else:
                self._active_string = ""

        elif new_state == BattleStates.VICTORY_TEXT:
            self._active_string = self._opponent.battle_dialogue

        self._state = new_state

    def _wrap_text(self, width):
        """Helper method that renders and blits text to the text box. Wraps
        the text if its width exceeds the provided width parameter."""
        self._battle_text_background.reload()
        string_lyst = textwrap.wrap(self._active_string, width=width)
        height = 10
        for string in string_lyst:
            rendered = self._font.render(string, False, (200, 200, 200))
            self._battle_text_background._image.blit(rendered, (10, height))
            height += 15
        return (rendered.get_width(), height)


class Cursor(Drawable):
    """Small Cursor class that keeps track of the in battle cursor. The below
    dictionaries hold the positions of the cursor depending on the
    current state of the battle."""
    CURSOR_POSITIONS = {0: (127, 124),
                        1: (182, 124),
                        2: (127, 140),
                        3: (182, 140)}
    CHOOSE_MOVE_POSITIONS = {0: (10, 124),
                             1: (80, 124),
                             2: (10, 140),
                             3: (80, 140)}

    def __init__(self):
        self._is_active = False
        self._active_pos_dict = self.CURSOR_POSITIONS
        self._cursor = 0
        super().__init__(join("battle", "cursor.png"),
                         self._active_pos_dict[self._cursor])

    def set_positions(self, state):
        """Grabs the correct position dictionary based on the state
        provided."""
        if state == BattleStates.CHOOSING_MOVE:
            self._active_pos_dict = self.CHOOSE_MOVE_POSITIONS
        if state == BattleStates.CHOOSING_FIGHT_OR_RUN:
            self._active_pos_dict = self.CURSOR_POSITIONS

    def get_value(self):
        """Returns the value of the cursor."""
        return self._cursor

    def reset(self):
        """Resets the cursor to its initial position."""
        self._cursor = 0
        self._position = self._active_pos_dict[self._cursor]

    def activate(self):
        """Activates the cursor so that it will be drawn."""
        self._is_active = True

    def deactivate(self):
        """Deactivates the cursor so that it will not be drawn."""
        self._is_active = False

    def draw(self, draw_surface):
        """Draws the cursor"""
        if self._is_active:
            super().draw(draw_surface)

    def get_move_corrected_value(self):
        """Corrects issue where moves 2 and 3 would be switched. This is
        becuase the moves list is ordered differently then the cursor."""
        if self._cursor == 1:
            return 2
        elif self._cursor == 2:
            return 1
        else:
            return self._cursor

    def __add__(self, other):
        """Add a simple add method to the cursor. Takes in an int as its
        argument."""
        return self._cursor + other

    def change_cursor_pos(self, action):
        """Changes the cursor pos based on the action provided"""
        if action.key == BattleActions.UP.value:
            if self._cursor == 2 or self._cursor == 3:
                SoundManager.getInstance().playSound("firered_0005.wav")
                self._cursor -= 2

        elif action.key == BattleActions.DOWN.value:
            if self._cursor == 0 or self._cursor == 1:
                SoundManager.getInstance().playSound("firered_0005.wav")
                self._cursor += 2

        elif action.key == BattleActions.LEFT.value:
            if self._cursor == 1 or self._cursor == 3:
                SoundManager.getInstance().playSound("firered_0005.wav")
                self._cursor -= 1

        elif action.key == BattleActions.RIGHT.value:
            if self._cursor == 0 or self._cursor == 2:
                SoundManager.getInstance().playSound("firered_0005.wav")
                self._cursor += 1
        self._position = self._active_pos_dict[self._cursor]


class MovesSurface(Drawable):
    """This class displays a pokemon's moves when the player is selecting
    which move to use."""
    def __init__(self, pokemon):
        super().__init__("", (7, 120))
        self._image = pygame.Surface((145, 33))
        self._image.fill((255, 255, 255, 0))
        self._image.set_colorkey((255, 255, 255))
        self._pokemon = pokemon
        self._font = pygame.font.Font(join("fonts", "pokemon_fire_red.ttf"),
                                      13)
        self._add_moves()

    def _add_moves(self):
        """Blit the moves names to the image surface."""
        pos = [(11, 2), (11, 18), (81, 2), (81, 18)]
        for move in self._pokemon.moves:
            move_name = move.move_name.upper()
            self._image.blit(self._font.render(move_name,
                                               False,
                                               (69, 60, 60)), pos.pop(0))


class PPSurface(Drawable):
    """This class displays the pp status of the selected move."""
    def __init__(self, pokemon):
        super().__init__("", (168, 120))
        self._image = pygame.Surface((65, 33))
        self._image.fill((255, 255, 255, 0))
        self._image.set_colorkey((255, 255, 255))
        self._pokemon = pokemon
        self._cursor_pos = 0
        self._font = pygame.font.Font(join("fonts", "pokemon_fire_red.ttf"),
                                      14)
        self._add_pp()

    def _add_pp(self):
        """Blit the various pp data to the image surface."""
        move = self._pokemon.moves[self.get_move_corrected_value()]
        self._image.blit(self._font.render(str(move.current_pp),
                                           False,
                                           (69, 60, 60)), (34, 2))
        self._image.blit(self._font.render(str(move.max_pp),
                                           False,
                                           (69, 60, 60)), (53, 2))
        self._image.blit(self._font.render(move.move_type.upper(),
                                           False, (69, 60, 60)), (24, 19))

    def _update_cursor(self, new_cursor_pos):
        """Changes the shown pp info when a new move is selected."""
        self._cursor_pos = new_cursor_pos
        self._image = pygame.Surface((65, 33))
        self._image.fill((255, 255, 255, 0))
        self._image.set_colorkey((255, 255, 255))
        self._add_pp()

    def get_move_corrected_value(self):
        """Corrects issue where moves 2 and 3 would be switched. This is
        becuase the moves list is ordered differently then the cursor."""
        if self._cursor_pos == 1:
            return 2
        elif self._cursor_pos == 2:
            return 1
        else:
            return self._cursor_pos
