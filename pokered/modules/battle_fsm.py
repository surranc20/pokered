import pygame
import textwrap
import copy
from enum import Enum, auto
from os.path import join
from .animated import AnimatedGroup
from .drawable import Drawable
from .vector2D import Vector2
from .animations.toss_pokemon import TossPokemon
from .animations.change_hp import ChangeHP
from .battle_menus.poke_info import PokeInfo
from .battle_menus.pokemon_remaining import PokemonRemaining
from .battle_menus.poke_party import PokeParty
from .pokemon import Pokemon
from .frameManager import FRAMES
from .soundManager import SoundManager
from .battle_actions import BattleActions

#TODO: Never display the number of pokemon remaining

class BattleStates(Enum):
    """Simple Enumeration of battle states. The value is a list of valid actions
    and the corresponding state after that action is taken. There are numbers in the
    tuple just so that the states are not viewed as synonyms for eachother. The actual 
    numbers have no meaning."""
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
    RUNNING = ("text wait", 17)
    TEST = ("auto", 18)

class BattleActions(Enum):
    """Simple Enumeration of battle actions"""
    SELECT = pygame.K_RETURN
    BACK = pygame.K_b
    UP = pygame.K_w
    LEFT = pygame.K_a
    DOWN = pygame.K_s
    RIGHT = pygame.K_d


class BattleFSM:

    TRANSITIONS = {(BattleStates.CHOOSING_MOVE, BattleActions.BACK) : BattleStates.CHOOSING_FIGHT_OR_RUN, (BattleStates.CHOOSING_FIGHT_OR_RUN, 0) : BattleStates.CHOOSING_MOVE, (BattleStates.CHOOSING_FIGHT_OR_RUN, 1) : BattleStates.TEST, (BattleStates.CHOOSING_FIGHT_OR_RUN, 2) : BattleStates.CHOOSING_POKEMON, (BattleStates.CHOOSING_FIGHT_OR_RUN, 3) : BattleStates.RUNNING,BattleStates.PLAYER_TOSSING_POKEMON : BattleStates.PLAYER_POKEMON_MENU, BattleStates.OPPONENT_TOSSING_POKEMON : BattleStates.OPPONENT_POKEMON_MENU, BattleStates.DISPLAY_OPPONENT_TOSS_TEXT : BattleStates.OPPONENT_TOSSING_POKEMON, BattleStates.DISPLAY_PLAYER_TOSS_TEXT : BattleStates.PLAYER_TOSSING_POKEMON}

    def __init__(self, player, opponent, draw_surface, state=BattleStates.NOT_STARTED):
        self._state = state
        self._font = pygame.font.Font(join("fonts", "pokemon_fire_red.ttf"), 16)
        self._cursor = Cursor()
        self._draw_surface = draw_surface
        self._active_player = opponent
        self._active_animation = None
        self._active_string = None
        self._opponent = opponent
        self._player = player
        self._background = Drawable(join("battle", "battle_background.png"), Vector2(0,0), offset= (0,0))
        self._battle_text_background = Drawable(join("battle", "battle_menus.png"), Vector2(0,113), offset=(0, 1))
        self._move_select = Drawable(join("battle", "battle_menus.png"), Vector2(0, 113), offset=(0, 0))
        self._fight_run = Drawable(join("battle", "battle_menus.png"), Vector2(120, 113), offset=(0, 2))


        self._draw_list = [self._background, self._battle_text_background]
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
            self._state = BattleStates.OPPONENTS_CHOOSING_POKEMON


        if self._state.value[0] == "wait":
            if self._state == BattleStates.CHOOSING_MOVE:
                pass
                
        elif self._state.value[0] == "text":
            self._wrap_text(20)
            self._state = self.TRANSITIONS[self._state]
        
        elif self._state.value[0] == "text wait":
            self._active_string = "There is no running from a trainer battle!"
            self._wrap_text(25)
            
        elif self._state.value[0] == "auto":
            if self._active_animation == None:
                print(self._active_animation)
                if self._state == BattleStates.OPPONENT_TOSSING_POKEMON:
                    trainer_toss = TossPokemon(self._opponent.get_active_pokemon().get_name(), lead_off=True, enemy=True)
                    self._active_animation = trainer_toss
                
                if self._state == BattleStates.PLAYER_TOSSING_POKEMON:
                    trainer_toss = TossPokemon(self._player.get_active_pokemon().get_name(), lead_off=True, enemy=False)
                    self._active_animation = trainer_toss
                
                if self._state == BattleStates.TEST:
                    hp_anim = ChangeHP(self._player.get_active_pokemon(), 20)
                    self._active_animation = hp_anim

            else:
                if self._active_animation.is_dead():
                    print("anim died", self._state)
                    self._active_animation = None
                    self.handle_nebulous_transition()
                    
        elif self._state.value[0] == "compute":
            self.handle_compute_event()

    def is_dead(self):
        return self._state == BattleStates.FINISHED

    def handle_action(self, action):
        if self._state.value[0] == "wait":
            self.handle_action_during_wait_event(action)
        elif self._state.value[0] == "text wait":
            self.handle_action_during_text_wait_event(action)
    
    def handle_compute_event(self):
        if self._state == BattleStates.OPPONENTS_CHOOSING_POKEMON:
            self._opponent.set_active_pokemon(0)
            self._handle_state_change(BattleStates.DISPLAY_OPPONENT_TOSS_TEXT)
    
    def handle_nebulous_transition(self):
        if self._state == BattleStates.OPPONENT_TOSSING_POKEMON:
            self._draw_list.append(self._opponent.get_active_pokemon())
            self._draw_list.append(PokeInfo(self._opponent.get_active_pokemon(), enemy=True))
            if self._player.get_active_pokemon() != None:
                self._handle_state_change(BattleStates.CHOOSING_FIGHT_OR_RUN)

            elif self._player.get_active_pokemon() == None:
                self._player.set_active_pokemon(0)
                self._handle_state_change(BattleStates.DISPLAY_PLAYER_TOSS_TEXT)
        
        elif self._state == BattleStates.PLAYER_TOSSING_POKEMON:
            self._draw_list.append(self._player.get_active_pokemon())
            self._player_poke_info = PokeInfo(self._player.get_active_pokemon())
            self._draw_list.append(self._player_poke_info)
            self._handle_state_change(BattleStates.CHOOSING_FIGHT_OR_RUN)
        
        elif self._state == BattleStates.TEST:
            print("WEEEE HRRRERE")
            self._player.get_active_pokemon()._stats["Current HP"] = 25
            self._handle_state_change(BattleStates.CHOOSING_FIGHT_OR_RUN)
           
    def handle_action_during_wait_event(self, action):
        if action.type == pygame.KEYDOWN:
            if action.key == BattleActions.SELECT.value:
                self._handle_state_change(self.TRANSITIONS[(self._state), self._cursor.get_value()])
                SoundManager.getInstance().playSound("firered_0005.wav")


            elif action.key == BattleActions.BACK.value and (self._state, BattleActions.BACK) in self.TRANSITIONS.keys():
                self._handle_state_change(self.TRANSITIONS[(self._state, BattleActions.BACK)])
                SoundManager.getInstance().playSound("firered_0005.wav")
            
            elif action.type == pygame.KEYDOWN and action.key in [BattleActions.UP.value, BattleActions.DOWN.value, BattleActions.LEFT.value, BattleActions.RIGHT.value]:
                if self._state != BattleStates.CHOOSING_POKEMON:
                    self._cursor.change_cursor_pos(action)
                    if self._state == BattleStates.CHOOSING_MOVE:
                        self._pp_surface._update_cursor(self._cursor.get_value())
                else:
                    self._draw_list[-1].change_cursor_pos(action)
    
    def handle_action_during_text_wait_event(self, action):
        if action.type == pygame.KEYDOWN and action.key == BattleActions.SELECT.value:
            SoundManager.getInstance().playSound("firered_0005.wav")
            self._handle_state_change(BattleStates.CHOOSING_FIGHT_OR_RUN)
    
    def _handle_state_change(self, new_state):
        # Clean up draw list and update list if neccessary
        if self._state == BattleStates.CHOOSING_FIGHT_OR_RUN:
            self._draw_list.pop(self._draw_list.index(self._fight_run))
            self._draw_list.pop(self._draw_list.index(self._cursor))
        elif self._state == BattleStates.CHOOSING_MOVE:
            self._draw_list.pop(self._draw_list.index(self._move_select))
            self._draw_list.pop(self._draw_list.index(self._pp_surface))
            self._draw_list.pop(self._draw_list.index(self._moves_surface))
        elif self._state == BattleStates.TEST:
            self._player_poke_info = PokeInfo(self._player.get_active_pokemon())
            
        if new_state == BattleStates.CHOOSING_FIGHT_OR_RUN:
            self._active_string = str("What will " + self._player.get_active_pokemon().get_name().upper() + " do?")
            self._wrap_text(12)
            self._draw_list.append(self._fight_run)
            self._cursor.activate()
            self._cursor.set_positions(new_state)
            self._cursor.reset()
            self._draw_list.append(self._cursor)
        
        elif new_state == BattleStates.RUNNING:
            try:
                self._draw_list.pop(self._draw_list.index(self._cursor))
            except ValueError: pass
        
        elif new_state == BattleStates.CHOOSING_POKEMON:
            poke_party = PokeParty(self._player)
            self._draw_list.append(poke_party)
            self._update_list.append(poke_party)
        
        elif new_state == BattleStates.CHOOSING_MOVE:
            self._cursor.set_positions(new_state)
            self._cursor.reset()
            self._draw_list.append(self._move_select)
            self._moves_surface = MovesSurface(self._player.get_active_pokemon())
            self._pp_surface = PPSurface(self._player.get_active_pokemon())
            self._draw_list.append(self._moves_surface)
            self._draw_list.append(self._pp_surface)
            self._draw_list.append(self._cursor)
        
        elif new_state == BattleStates.DISPLAY_OPPONENT_TOSS_TEXT:
            self._active_string = str(self._opponent.get_name() + " sent out " + self._opponent.get_active_pokemon().get_name().upper() + "!")
        
        elif new_state == BattleStates.DISPLAY_PLAYER_TOSS_TEXT:
            self._active_string = str("Go! " + self._player.get_active_pokemon().get_name().upper() +"!")
        
        self._state = new_state
    
    def _wrap_text(self, width):
        self._battle_text_background.reload()
        string_lyst = textwrap.wrap(self._active_string, width=width)
        height = 10
        for string in string_lyst:
            self._battle_text_background._image.blit(self._font.render(string, False, (200, 200, 200)), (10, height))
            height += 15
    
class Cursor(Drawable):
    """Small Cursor class that keeps track of the in battle cursor"""
    CURSOR_POSITIONS = {0 : (127, 124), 1 : (182, 124), 2 : (127, 140), 3 : (182, 140)}
    CHOOSE_MOVE_POSITIONS = {0 : (10, 124), 1 : (80, 124), 2 : (10, 140), 3 : (80, 140)}
    def __init__(self):
        self._is_active = False
        self._active_pos_dict = self.CURSOR_POSITIONS
        self._cursor = 0
        super().__init__(join("battle", "cursor.png"), self._active_pos_dict[self._cursor])
    
    def set_positions(self, state):
        if state == BattleStates.CHOOSING_MOVE:
            self._active_pos_dict = self.CHOOSE_MOVE_POSITIONS
        if state == BattleStates.CHOOSING_FIGHT_OR_RUN:
            self._active_pos_dict = self.CURSOR_POSITIONS
    
    def get_value(self):
        return self._cursor
    
    def reset(self):
        self._cursor = 0
        self._position = self._active_pos_dict[self._cursor]
    
    def activate(self):
        self._is_active = True
    
    def deactivate(self):
        self._is_active = False
    
    def draw(self, draw_surface):
        if self._is_active:
            super().draw(draw_surface)
    
    def __add__(self, other):
        return self._cursor + other
    
    def change_cursor_pos(self, action):
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
    """This class displays the moves when the player is selecting their move"""
    def __init__(self, pokemon):
        super().__init__("", (7,120))
        self._image = pygame.Surface((145, 33))
        self._image.fill((255,255,255,0))
        self._image.set_colorkey((255, 255, 255))
        self._pokemon = pokemon
        self._font = pygame.font.Font(join("fonts", "pokemon_fire_red.ttf"), 14)
        self._add_moves()
    
    def _add_moves(self):
        pos = [(11, 2), (11, 18), (81, 2), (81, 18)]
        for move in self._pokemon.get_moves():
            move_name = move[0].upper()
            self._image.blit(self._font.render(move_name, False, (69, 60, 60)), pos.pop(0))

class PPSurface(Drawable):
    """This class displays the pp status of the selected move"""
    def __init__(self, pokemon):
        super().__init__("", (168, 120))
        self._image = pygame.Surface((65, 33))
        self._image.fill((255,255,255,0))
        self._image.set_colorkey((255, 255, 255))
        self._pokemon = pokemon
        self._cursor_pos = 0
        self._font = pygame.font.Font(join("fonts", "pokemon_fire_red.ttf"), 14)
        self._add_pp()
        
    
    def _add_pp(self):
        move = self._pokemon.get_moves()[self._cursor_pos]
        self._image.blit(self._font.render(str(move[1]), False, (69, 60, 60)), (40, 2))
        self._image.blit(self._font.render(str(move[2]), False, (69, 60, 60)), (53, 2))
        self._image.blit(self._font.render(move[3].upper(), False, (69, 60, 60)), (24, 19))

    def _update_cursor(self, new_cursor_pos):
        self._cursor_pos = new_cursor_pos
        self._image = pygame.Surface((65, 33))
        self._image.fill((255,255,255,0))
        self._image.set_colorkey((255, 255, 255))
        self._add_pp()
