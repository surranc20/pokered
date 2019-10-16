import pygame
import textwrap
import copy
from enum import Enum, auto
from os.path import join
from .animated import AnimatedGroup
from .drawable import Drawable
from .vector2D import Vector2
from .animations.toss_pokemon import TossPokemon
from .battle_menus.poke_info import PokeInfo
from .battle_menus.pokemon_remaining import PokemonRemaining
from .pokemon import Pokemon
from .frameManager import FRAMES

#TODO: Never display the number of pokemon remaining

class BattleStates(Enum):
    """Simple Enumeration of battle states. The value is a list of valid actions
    and the corresponding state after that action is taken"""
    NOT_STARTED = ("auto", 1)
    OPENING_ANIMS = ("wait", 2)
    OPPONENT_TOSSING_POKEMON = ("auto", 3)
    OPPONENTS_CHOOSING_POKEMON = ("compute", 4)
    CHOOSING_POKEMON = ("wait", 5)
    CHOOSING_FIGHT_OR_RUN = ("wait", 6)
    CHOOSING_MOVE = ("wait", 7)
    POKEMON_DEAD = (8)
    PLAYER_TOSSING_POKEMON = ("auto", 9)
    CHOOSING_ITEM = ("wait", 10)
    EXECUTING_MOVE = ("auto", 11)
    FINISHED = ("finished", 12)
    PLAYER_POKEMON_MENU = ("auto", 13)
    OPPONENT_POKEMON_MENU = ("auto", 14)
    DISPLAY_OPPONENT_TOSS_TEXT = ("text", 15)
    DISPLAY_PLAYER_TOSS_TEXT = ("text", 16)

class BattleActions(Enum):
    """Simple Enumeration of battle actions"""
    SELECT = auto()
    BACK = auto()
    UP = auto()
    LEFT = auto()
    DOWN = auto()
    RIGHT = auto()





class BattleFSM:

    TRANSITIONS = {BattleStates.PLAYER_TOSSING_POKEMON : BattleStates.PLAYER_POKEMON_MENU, BattleStates.OPPONENT_TOSSING_POKEMON : BattleStates.OPPONENT_POKEMON_MENU, BattleStates.DISPLAY_OPPONENT_TOSS_TEXT : BattleStates.OPPONENT_TOSSING_POKEMON, BattleStates.DISPLAY_PLAYER_TOSS_TEXT : BattleStates.PLAYER_TOSSING_POKEMON}

    def __init__(self, player, opponent, draw_surface, state=BattleStates.NOT_STARTED):
        self._state = state
        self._font = pygame.font.Font(join("fonts", "pokemon_fire_red.ttf"), 16)
        self._cursor = 0
        self._draw_surface = draw_surface
        self._active_player = opponent
        self._active_animation = None
        self._active_string = None
        self._opponent = opponent
        self._player = player
        self._background = Drawable(join("battle", "battle_background.png"), Vector2(0,0), offset= (0,0))
        self._battle_menus = Drawable(join("battle", "battle_menus.png"), Vector2(0,113), offset=(0, 1))
        self._fight_run = Drawable(join("battle", "battle_menus.png"), Vector2(120, 113), offset=(0, 2))


        self._draw_list = [self._background, self._battle_menus]
        self._update_list = []
    
    def manage_action(self, action):
        if action in [value[0] for value in self._state.value]:
            pass

    def get_state(self):
        return self._state

    def get_draw_list(self):
        draw_list = [item for item in self._draw_list if not item.is_dead()]
        if self._active_animation != None:
            draw_list.append(self._active_animation)
        return draw_list
    
    def get_update_list(self):
        update_list =  [item for item in self._update_list if not item.is_dead()]
        if self._active_animation != None:
            print(self._active_animation)
            update_list.append(self._active_animation)
    
        return update_list
    def update(self, ticks):
        print(self._state)
        if self._opponent.get_active_pokemon() == None and self._state != BattleStates.OPPONENT_TOSSING_POKEMON:
            print("HEREEEE")
            self._state = BattleStates.OPPONENTS_CHOOSING_POKEMON


        

        if self._state.value[0] == "wait":
            if self._state == BattleStates.CHOOSING_MOVE:
                self._active_string = str("What will " + self._player.get_active_pokemon().get_name().upper() + " do?")
                self._wrap_text(12)
                self._draw_list.append(self._fight_run)

    
        elif self._state.value[0] == "text":
            self._wrap_text(20)
            
            self._state = self.TRANSITIONS[self._state]

        elif self._state.value[0] == "auto":
            if self._active_animation == None:
                if self._state == BattleStates.OPPONENT_TOSSING_POKEMON:
                    trainer_toss = TossPokemon(self._opponent.get_active_pokemon().get_name(), lead_off=True, enemy=True)
                    self._active_animation = trainer_toss
                
                if self._state == BattleStates.PLAYER_TOSSING_POKEMON:
                    trainer_toss = TossPokemon(self._player.get_active_pokemon().get_name(), lead_off=True, enemy=False)
                    self._active_animation = trainer_toss

            else:
                if self._active_animation.is_dead():
                    self._active_animation = None
                    # if self._state in list(self.TRANSITIONS.keys()):
                    #     if self._state == BattleStates.OPPONENT_TOSSING_POKEMON:
                    #         self._display_opponent_pokemon = True
                    #     elif self._state == BattleStates.PLAYER_TOSSING_POKEMON:
                    #         self._display_player_pokemon = True
                            
                    #     self._state = self.TRANSITIONS[self._state]
                        

                    # else:
                    self.handle_nebulous_transition()
                
        
        elif self._state.value[0] == "compute":
            self.handle_compute_event()

                
    def is_dead(self):
        return self._state == BattleStates.FINISHED
    
    def handle_action(self, action):
        if self._state.value[0] == "wait":
            self.handle_action_during_wait_event(action)
    

    def handle_compute_event(self):
        if self._state == BattleStates.OPPONENTS_CHOOSING_POKEMON:
            self._opponent.set_active_pokemon(0)
            self._state = BattleStates.DISPLAY_OPPONENT_TOSS_TEXT
            self._active_string = str(self._opponent.get_name() + " sent out " + self._opponent.get_active_pokemon().get_name().upper() + "!")

    
            # if self._player.get_active_pokemon() == None and self._opponent.get_active_pokemon() == None:
            #     self._opponent.set_active_pokemon(0)
            #     trainer_toss = TossPokemon(self._opponent.get_active_pokemon().get_name(), lead_off=True, enemy=True)
            # else: 
            #     self._opponent.set_active_pokemon(0)
            #     trainer_toss = TossPokemon(self._opponent.get_active_pokemon().get_name(), lead_off=False, enemy=True)

            # self._state = BattleStates.OPPONENT_TOSSING_POKEMON

            # self._active_animation = trainer_toss
            # self._draw_list.append(trainer_toss)
            # self._update_list.append(trainer_toss)
    
    def handle_nebulous_transition(self):
        if self._state == BattleStates.OPPONENT_TOSSING_POKEMON:
            self._draw_list.append(self._opponent.get_active_pokemon())
            self._draw_list.append(PokeInfo(self._opponent.get_active_pokemon(), enemy=True))
            if self._player.get_active_pokemon() != None:
                self._state = BattleStates.CHOOSING_MOVE

            elif self._player.get_active_pokemon() == None:
                self._state = BattleStates.DISPLAY_PLAYER_TOSS_TEXT
                self._player.set_active_pokemon(0)
                self._active_string = str("Go! " + self._player.get_active_pokemon().get_name().upper() +"!")
                # self._player.set_active_pokemon(0)
                # self._state = BattleStates.PLAYER_TOSSING_POKEMON
                # toss_anim = TossPokemon(self._player.get_active_pokemon().get_name(), lead_off=True, enemy=False)
                # self._active_animation = toss_anim
                # self._draw_list.append(toss_anim)
                # self._update_list.append(toss_anim)
        
        elif self._state == BattleStates.PLAYER_TOSSING_POKEMON:
            self._draw_list.append(self._player.get_active_pokemon())
            self._draw_list.append(PokeInfo(self._player.get_active_pokemon()))

            self._state = BattleStates.CHOOSING_MOVE
    
    def handle_action_during_wait_event(self, action):
        if (self._state, action) in list(self.TRANSITIONS.keys()):
            self._state = self.TRANSITIONS[(self._state, action)]

            if action == BattleActions.UP.value:
                if self._cursor == 2 or self._cursor == 3:
                    self._cursor -= 2
            
            elif action == BattleActions.DOWN.value:
                if self._cursor == 0 or self._cursor == 1:
                    self._cursor += 2
            
            elif action == BattleActions.LEFT.value:
                if self._cursor == 1 or self._cursor == 3:
                    self._cursor -= 1
            
            elif action == BattleActions.RIGHT.value:
                if self._cursor == 0 or self._cursor == 2:
                    self._cursor += 1
    
    
    def _wrap_text(self, width):
        self._battle_menus.reload()
        string_lyst = textwrap.wrap(self._active_string, width=width)
        height = 10
        for string in string_lyst:
            self._battle_menus._image.blit(self._font.render(string, False, (200, 200, 200)), (10, height))
            height += 15
    
    