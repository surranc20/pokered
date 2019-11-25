import pygame
import textwrap
import copy
import random
from enum import Enum, auto
from os.path import join

from ..utils.animated import AnimatedGroup
from ..utils.drawable import Drawable
from ..utils.vector2D import Vector2
from ..animations.toss_pokemon import TossPokemon
from ..animations.change_hp import ChangeHP
from ..animations.poke_death import PokeDeath
from ..animations.moves.thunder import Thunder
from ..utils.frameManager import FRAMES
from ..utils.soundManager import SoundManager
from ..enumerated.battle_actions import BattleActions
from ..enumerated.battle_states import BattleStates
from ..pokemon import Pokemon
from ..move import Move
from .battle_menus.poke_info import PokeInfo
from .battle_menus.pokemon_remaining import PokemonRemaining
from .battle_menus.poke_party import PokeParty
from .damage_calculator import DamageCalculator

#TODO: Never display the number of pokemon remaining

class BattleFSM:

    TRANSITIONS = {
        (BattleStates.CHOOSING_FIGHT_OR_RUN, 0) : BattleStates.CHOOSING_MOVE,
        (BattleStates.CHOOSING_FIGHT_OR_RUN, 1) : BattleStates.TEST,
        (BattleStates.CHOOSING_FIGHT_OR_RUN, 2) : BattleStates.CHOOSING_POKEMON,
        (BattleStates.CHOOSING_FIGHT_OR_RUN, 3) : BattleStates.RUNNING,
        BattleStates.CHOOSING_MOVE : BattleStates.CHOOSE_OPPONENT_ACTION,
        BattleStates.RUNNING : BattleStates.CHOOSING_FIGHT_OR_RUN,
        (BattleStates.CHOOSING_POKEMON, BattleActions.BACK) : BattleStates.CHOOSING_FIGHT_OR_RUN,
        (BattleStates.CHOOSING_MOVE, BattleActions.BACK) : BattleStates.CHOOSING_FIGHT_OR_RUN,
        BattleStates.DISPLAY_EFFECT : BattleStates.CHOOSING_FIGHT_OR_RUN, 
        BattleStates.MOVE_MISSED : BattleStates.CHOOSING_FIGHT_OR_RUN
    }

    def __init__(self, player, opponent, state=BattleStates.NOT_STARTED):
        self._state = state
        self._state_queue = []
        self._font = pygame.font.Font(join("fonts", "pokemon_fire_red.ttf"), 16)
        self._cursor = Cursor()
        self._active_animation = None
        self._active_string = None
        self._text_cursor = TextCursor((0,0))
        self._opponent = opponent
        self._player = player
        self._active_player_pokemon = None
        self._active_opponent_pokemon = None
        self._player_poke_info = None
        self._opponent_poke_info = None
        self._player_move_queued = None
        self._enemy_move_queued = None
        self._turn_order = []
        self._initial_stage_over = False
        self._text_wait_timer = 0
        self._scrolling_background_surf = None
        self._background = Drawable(join("battle", "battle_background.png"), Vector2(0,0), offset= (0,0))
        self._battle_text_background = Drawable(join("battle", "battle_menus.png"), Vector2(0,112), offset=(0, 1))
        self._move_select = Drawable(join("battle", "battle_menus.png"), Vector2(0, 113), offset=(0, 0))
        self._fight_run = Drawable(join("battle", "battle_menus.png"), Vector2(120, 113), offset=(0, 2))
        self._draw_list = [self._background, self._battle_text_background, self._active_player_pokemon, self._active_opponent_pokemon, self._player_poke_info, self._opponent_poke_info, self._text_cursor]
        self._update_list = [self._player_poke_info, self._opponent_poke_info, self._text_cursor]
        self._is_over = False
   
    def is_over(self):
        return self._is_over

    def get_draw_list(self):
        draw_list = [item for item in self._draw_list if item != None and not item.is_dead()]
        if self._active_animation != None:
            if self._scrolling_background_surf != None:
                draw_list.insert(1, self._scrolling_background_surf)
            draw_list.append(self._active_animation)

        return draw_list
    
    def get_update_list(self):
        update_list =  [item for item in self._update_list if item != None and not item.is_dead()]
        if self._active_animation != None:
            print(self._active_animation)
            update_list.append(self._active_animation)
    
        return update_list
    
    def update(self, ticks):

        if self._state == BattleStates.NOT_STARTED:
            self._state_queue = [BattleStates.TEXT_WAIT, BattleStates.OPPONENT_TOSSING_POKEMON, BattleStates.PLAYER_TOSSING_POKEMON, BattleStates.CHOOSING_FIGHT_OR_RUN]
            self._active_string = self._opponent.get_name().upper() + " would like to battle!"
            self._state = self._state_queue.pop(0)
            self._player.set_active_pokemon(0)
            self._opponent.set_active_pokemon(0)

            self._draw_list.append(TossPokemon(self._player.get_active_pokemon().get_name(), self._player, lead_off=True, enemy=False))
            self._draw_list.append(TossPokemon(self._opponent.get_active_pokemon().get_name(), self._opponent, lead_off=True, enemy=True))

        if self._state == BattleStates.BATTLE_OVER:
            self._is_over = True

        if self._state.value[0] == "text wait":
            self._text_wait_timer += ticks
            if self._active_string != None and self._active_string != "":
                self._text_cursor.set_pos(self._wrap_text(25))
                self._text_cursor.activate()
                self._active_string = None
            elif self._active_string == "":
                if self._text_wait_timer > 1:
                    self._text_wait_timer = 0
                    if len(self._state_queue) > 0:
                        self._active_string = None
                        self._handle_state_change(self._state_queue.pop(0))
                    else:
                        self._active_string = None
                        self._handle_state_change(self.TRANSITIONS[self._state])

        
        elif self._state.value[0] == "compute":
            if self._state == BattleStates.CHOOSE_OPPONENT_ACTION:
                self._handle_state_change(BattleStates.OPPONENT_CHOOSING_MOVE)

            elif self._state == BattleStates.OPPONENT_CHOOSING_MOVE:
                self._enemy_move_queued = self._opponent.get_active_pokemon().get_moves()[0]
                self._handle_state_change(BattleStates.DECIDING_BATTLE_ORDER)
            
            elif self._state == BattleStates.VICTORY:
                self._state_queue = [BattleStates.TEXT_WAIT, BattleStates.BATTLE_OVER]
                self._active_string = "Player defeated " + self._opponent.get_name().upper() + "!"
                self._handle_state_change(self._state_queue.pop(0))

            elif self._state == BattleStates.DECIDING_BATTLE_ORDER:
                if self._player_move_queued == None and self._enemy_move_queued == None:
                    self._turn_order = []
                elif self._player_move_queued == None and self._enemy_move_queued != None:
                    self._turn_order.append(self._opponent)
                elif self._player_move_queued != None and self._enemy_move_queued == None:
                    self._turn_order.append(self._player)
                else:
                    if self._player.get_active_pokemon()._stats["Speed"] >= self._opponent.get_active_pokemon()._stats["Speed"]:
                        self._turn_order.append(self._player)
                        self._turn_order.append(self._opponent)
                    else:
                        self._turn_order.append(self._opponent)
                        self._turn_order.append(self._player)
                self._handle_state_change(BattleStates.EXECUTE_TURN)
            
            elif self._state == BattleStates.EXECUTE_TURN:
                for player in self._turn_order:
                    accuracy = self._player_move_queued.accuracy if player == self._player else self._enemy_move_queued.accuracy
                    if random.randint(0, 100) > accuracy:
                        self._state_queue.append(BattleStates.PLAYER_MOVE_TEXT if player == self._player else BattleStates.OPPONENT_MOVE_TEXT)
                        self._state_queue.append(BattleStates.MOVE_MISSED)
                        

                    else:
                        self._state_queue.append(BattleStates.PLAYER_MOVE_TEXT if player == self._player else BattleStates.OPPONENT_MOVE_TEXT)
                        self._state_queue.append(BattleStates.MOVE_ANIMATION)
                        self._state_queue.append(BattleStates.UPDATE_ENEMY_STATUS if player == self._player else BattleStates.UPDATE_PLAYER_STATUS)
                        self._state_queue.append(BattleStates.DISPLAY_EFFECT)
                        self._state_queue.append(BattleStates.CHECK_HEALTH)
                

                if self._state_queue == []:
                    self._handle_state_change(BattleStates.CHOOSING_FIGHT_OR_RUN)
                else:
                    self._handle_state_change(self._state_queue.pop(0))

            elif self._state == BattleStates.CHECK_HEALTH:
                if self._player.get_active_pokemon()._stats["Current HP"] <= 0:
                    self._handle_state_change(BattleStates.PLAYER_POKEMON_DIED)
                elif self._opponent.get_active_pokemon()._stats["Current HP"] <= 0:
                    self._handle_state_change(BattleStates.OPPONENT_POKEMON_DIED)
                else:
                    if self._state_queue == []:
                        self._handle_state_change(BattleStates.CHOOSING_FIGHT_OR_RUN)
                    else:
                        self._handle_state_change(self._state_queue.pop(0))
            
            elif self._state == BattleStates.OPPONENT_POKEMON_DIED:
                if self._opponent.all_dead():
                    self._handle_state_change(BattleStates.VICTORY)
                else:
                    self._state_queue = [BattleStates.TEXT_WAIT, BattleStates.OPPONENT_FEINT, BattleStates.OPPONENT_CHOOSING_POKEMON, BattleStates.OPPONENT_TOSSING_POKEMON, BattleStates.CHOOSING_FIGHT_OR_RUN]
                    self._active_string = "Foe " + self._opponent.get_active_pokemon().get_name().capitalize() + " fainted!"
                    self._handle_state_change(self._state_queue.pop(0))

            elif self._state == BattleStates.PLAYER_POKEMON_DIED:
                self._state_queue = [BattleStates.TEXT_WAIT, BattleStates.PLAYER_FEINT, BattleStates.CHOOSING_POKEMON, BattleStates.CHOOSING_FIGHT_OR_RUN]
                self._active_string = self._player.get_active_pokemon().get_name().capitalize() + " fainted!"
                self._handle_state_change(self._state_queue.pop(0))

            elif self._state == BattleStates.OPPONENT_CHOOSING_POKEMON:
                while self._opponent.get_active_pokemon()._stats["Current HP"] <= 0:
                    self._opponent.set_active_pokemon(random.randint(0, 4))
                self._handle_state_change(self._state_queue.pop(0))
        
        elif self._state.value[0] == "auto":
            if self._active_animation == None:
                if self._state == BattleStates.OPPONENT_TOSSING_POKEMON:
                    self._active_string = self._opponent.get_name().upper() + " sent out " + self._opponent.get_active_pokemon().get_name().upper() + "!"
                    self._wrap_text(20)
                    if self._initial_stage_over:
                        self._draw_list[3] = None
                        self._draw_list[5] = None
                        trainer_toss = TossPokemon(self._opponent.get_active_pokemon().get_name(), self._player, lead_off=False, enemy=True)
                    else:
                        trainer_toss = self._draw_list.pop()
                    self._active_animation = trainer_toss

                if self._state == BattleStates.PLAYER_TOSSING_POKEMON:
                    self._active_string = "Go! " + self._player.get_active_pokemon().get_nick_name().upper() + "!"
                    self._wrap_text(20)
                    if self._initial_stage_over:
                        self._draw_list[2] = None
                        self._draw_list[4] = None
                        trainer_toss = TossPokemon(self._player.get_active_pokemon().get_name(), self._player, lead_off=False, enemy=False)
                    else:
                        trainer_toss = self._draw_list.pop()
                        self._initial_stage_over = True
                    self._active_animation = trainer_toss

                if self._state == BattleStates.MOVE_ANIMATION:
                    self._active_animation = Thunder()
                    #self._handle_state_change(self._state_queue.pop(0))
                
                if self._state == BattleStates.UPDATE_PLAYER_STATUS:
                    calc = DamageCalculator((self._opponent.get_active_pokemon(), self._enemy_move_queued), self._player.get_active_pokemon())
                    dmg = calc.get_damage()

                    self._active_animation = ChangeHP(self._player.get_active_pokemon(), dmg, calc.get_effectiveness_sound())
                    self._active_string = calc.get_effectiveness()
                
                if self._state == BattleStates.UPDATE_ENEMY_STATUS:
                    calc = DamageCalculator((self._player.get_active_pokemon(), self._player_move_queued), self._opponent.get_active_pokemon())
                    dmg = calc.get_damage()
                    self._active_animation = ChangeHP(self._opponent.get_active_pokemon(), dmg, calc.get_effectiveness_sound())
                    self._active_string = calc.get_effectiveness()
                
                if self._state == BattleStates.OPPONENT_FEINT:
                    self._active_animation = PokeDeath(self._opponent.get_active_pokemon())
                
                if self._state == BattleStates.PLAYER_FEINT:
                    self._active_animation = PokeDeath(self._player.get_active_pokemon())
                

            else:
                if self._active_animation.is_dead():
                    self._active_animation = None
                    if self._state == BattleStates.OPPONENT_TOSSING_POKEMON:
                        self._draw_list[3] = self._opponent.get_active_pokemon()
                        op_poke_info = PokeInfo(self._opponent.get_active_pokemon(), enemy=True)
                        self._draw_list[5] = op_poke_info
                        self._update_list[1] = op_poke_info

                    if self._state == BattleStates.PLAYER_TOSSING_POKEMON:
                        self._draw_list[2] = self._player.get_active_pokemon()
                        self._player_poke_info = PokeInfo(self._player.get_active_pokemon())
                        self._draw_list[4] = self._player_poke_info
                        self._update_list[0] = self._player_poke_info
                        
                    if len(self._state_queue) > 0:
                        self._handle_state_change(self._state_queue.pop(0))
                    else:
                        self._handle_state_change(BattleStates.CHOOSE_OPPONENT_ACTION)

    def handle_action(self, action):
        if self._state.value[0] == "text wait":
            self._handle_action_during_text_wait(action)
        elif self._state.value[0] == "wait":
            self._handle_action_during_wait(action)
    
    def _handle_action_during_wait(self, action):
        if action.type == pygame.KEYDOWN:
            if action.key in [BattleActions.UP.value, BattleActions.DOWN.value, BattleActions.LEFT.value, BattleActions.RIGHT.value]:
                if self._state == BattleStates.CHOOSING_POKEMON:
                    self._poke_party.change_cursor_pos(action)
                else:
                    self._cursor.change_cursor_pos(action)
                    if self._state == BattleStates.CHOOSING_MOVE:
                        self._pp_surface._update_cursor(self._cursor.get_value())

            if action.key == BattleActions.SELECT.value:
                if self._state == BattleStates.CHOOSING_POKEMON:
                    response = self._poke_party.handle_select_event(action)
                    if response != None:
                        if self._state_queue != []:
                            self._state_queue.insert(0, response[0])
                            self._handle_state_change(self._state_queue.pop(0))
                        else:
                            self._handle_state_change(response[0])

                else:
                    SoundManager.getInstance().playSound("firered_0005.wav")
                    if self._state == BattleStates.CHOOSING_MOVE:
                        self._player_move_queued = self._player.get_active_pokemon().get_moves()[self._cursor.get_value()]
                        self._handle_state_change(self.TRANSITIONS[self._state])
                    else:
                        self._handle_state_change(self.TRANSITIONS[(self._state), self._cursor.get_value()])
            
            if action.key == BattleActions.BACK.value:
                self._handle_state_change(self.TRANSITIONS[(self._state), BattleActions.BACK])
                SoundManager.getInstance().playSound("firered_0005.wav")

    def _handle_action_during_text_wait(self, action):
        if action.type == pygame.KEYDOWN and action.key == BattleActions.SELECT.value:
            SoundManager.getInstance().playSound("firered_0005.wav")
            if len(self._state_queue) > 0:
                self._handle_state_change(self._state_queue.pop(0))
            else:
                self._handle_state_change(self.TRANSITIONS[self._state])
    
    def _handle_state_change(self, new_state):
        if self._state.value[0] == "text wait":
            self._text_cursor.deactivate()

        if self._state == BattleStates.CHOOSING_FIGHT_OR_RUN:
            self._draw_list.pop(self._draw_list.index(self._fight_run))
            self._draw_list.pop(self._draw_list.index(self._cursor))
        
        if self._state == BattleStates.CHOOSING_MOVE:
            self._draw_list.pop(self._draw_list.index(self._move_select))
            self._draw_list.pop(self._draw_list.index(self._pp_surface))
            self._draw_list.pop(self._draw_list.index(self._moves_surface))
            self._cursor.deactivate()
        
        if self._state == BattleStates.CHOOSING_POKEMON:
            self._draw_list.pop()
            self._update_list.pop()
        
        if new_state == BattleStates.CHOOSING_FIGHT_OR_RUN:
            self._turn_order = []
            self._player_move_queued = None
            self._enemy_move_queued = None
            self._active_string = str("What will " + self._player.get_active_pokemon().get_name().upper() + " do?")
            self._wrap_text(12)
            self._draw_list.append(self._fight_run)
            self._draw_list.append(self._cursor)
            self._cursor.activate()
            self._cursor.set_positions(new_state)
            self._cursor.reset()
        
        elif new_state == BattleStates.CHOOSING_MOVE:
            self._cursor.set_positions(new_state)
            self._cursor.reset()
            self._draw_list.append(self._move_select)
            self._moves_surface = MovesSurface(self._player.get_active_pokemon())
            self._pp_surface = PPSurface(self._player.get_active_pokemon())
            self._draw_list.append(self._moves_surface)
            self._draw_list.append(self._pp_surface)
            self._draw_list.append(self._cursor)
        
        elif new_state == BattleStates.RUNNING:
            self._active_string = "There is no running from a trainer battle!"
            
        
        elif new_state == BattleStates.CHOOSING_POKEMON:
            self._poke_party = PokeParty(self._player)
            self._draw_list.append(self._poke_party)
            self._update_list.append(self._poke_party)
        
        elif new_state == BattleStates.OPPONENT_MOVE_TEXT:
            self._enemy_move_queued.current_pp -=1
            self._active_string = self._active_string = self._opponent.get_active_pokemon().get_name().upper() + " used " +  self._enemy_move_queued.move_name + "!"


        elif new_state == BattleStates.PLAYER_MOVE_TEXT:
            self._player_move_queued.current_pp -= 1
            self._active_string = self._active_string = self._player.get_active_pokemon().get_name().upper() + " used " +  self._player_move_queued.move_name + "!"

        elif new_state == BattleStates.MOVE_MISSED:
            self._active_string = "Its move missed!"

        self._state = new_state


    def _wrap_text(self, width):
        self._battle_text_background.reload()
        string_lyst = textwrap.wrap(self._active_string, width=width)
        height = 10
        for string in string_lyst:
            rendered = self._font.render(string, False, (200, 200, 200))
            self._battle_text_background._image.blit(rendered, (10, height))
            height += 15
        return (rendered.get_width(), height)
    
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
        

class TextCursor(Drawable):
    def __init__(self, pos):
        super().__init__("text_cursor.png", pos)
        self._is_active = False
        self._current_delta = 1
        self._timer = 0
    
    def activate(self):
        self._is_active = True
    
    def deactivate(self):
        self._is_active = False
    
    def set_pos(self, pos):
        pos = (pos[0] + 10, pos[1] + 100)
        self._position = pos
        self._anchored_pos = pos
    
    def draw(self, draw_surface):
        if self._is_active:
            super().draw(draw_surface)

    def update(self, ticks):
        if self._position == self._anchored_pos:
            self._current_delta = 1
        elif self._position[1] - self._anchored_pos[1] >= 2:
            self._current_delta = -1

        self._timer += ticks
        if self._timer > .2:
            self._position = (self._position[0], self._position[1] + self._current_delta)
            self._timer -= .2
        



class MovesSurface(Drawable):
    """This class displays the moves when the player is selecting their move"""
    def __init__(self, pokemon):
        super().__init__("", (7,120))
        self._image = pygame.Surface((145, 33))
        self._image.fill((255,255,255,0))
        self._image.set_colorkey((255, 255, 255))
        self._pokemon = pokemon
        self._font = pygame.font.Font(join("fonts", "pokemon_fire_red.ttf"), 13)
        self._add_moves()
    
    def _add_moves(self):
        pos = [(11, 2), (11, 18), (81, 2), (81, 18)]
        for move in self._pokemon.get_moves():
            move_name = move.move_name.upper()
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
        self._image.blit(self._font.render(str(move.current_pp), False, (69, 60, 60)), (34, 2))
        self._image.blit(self._font.render(str(move.max_pp), False, (69, 60, 60)), (53, 2))
        self._image.blit(self._font.render(move.move_type.upper(), False, (69, 60, 60)), (24, 19))

    def _update_cursor(self, new_cursor_pos):
        self._cursor_pos = new_cursor_pos
        self._image = pygame.Surface((65, 33))
        self._image.fill((255,255,255,0))
        self._image.set_colorkey((255, 255, 255))
        self._add_pp()


    
