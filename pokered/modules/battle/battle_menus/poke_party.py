import json
import pygame
from os.path import join
from ...utils.drawable import Drawable
from ...utils.animated import Animated
from ...utils.vector2D import Vector2
from ...utils.frameManager import FRAMES
from ...utils.soundManager import SoundManager
from ...enumerated.battle_states import BattleStates
from ...enumerated.battle_actions import BattleActions

class PokeParty(Drawable):
    def __init__(self, player):
        self._player = player
        super().__init__("party_background.png",(0,0))
        self._selectable_items = []
        self._blit_active_pokemon()
        self._blit_secondary_pokemon()
        self._cancel_button = CancelButton()
        self._text_bar = PartyTextBar()
        self._text_bar.blit_string("Choose a POKeMON.")
        self._cursor = 0
        self._selected_pokemon = False
        self._pokemon_selected_menu = None
    
    def _blit_active_pokemon(self):
        self._active_pokemon = ActivePokemon(self._player.get_active_pokemon(), selected=True)
        self._selectable_items.append(self._active_pokemon)
    
    def _blit_secondary_pokemon(self):
        position = (88,9)
        for pokemon in self._player.get_pokemon_team()[1:]:
            self._selectable_items.append(SecondaryPokemon(pokemon, position))
            position = (88, position[1] + 24)
    
    def draw(self, draw_surface):
        super().draw(draw_surface)
        self._cancel_button.draw(draw_surface)
        self._text_bar.draw(draw_surface)
        for item in self._selectable_items:
            item.draw(draw_surface)
        if self._pokemon_selected_menu != None:
            self._pokemon_selected_menu.draw(draw_surface)
    
    def change_cursor_pos(self, action):
        if self._selected_pokemon == False:
            old_pos = self._cursor
            if action.key == BattleActions.UP.value:
                if self._cursor > 0:
                    SoundManager.getInstance().playSound("firered_0005.wav")
                    self._cursor -= 1

            elif action.key == BattleActions.DOWN.value:
                if self._cursor <= 5:
                    SoundManager.getInstance().playSound("firered_0005.wav")
                    self._cursor += 1
            
            elif action.key == BattleActions.LEFT.value:
                if self._cursor == 1:
                    SoundManager.getInstance().playSound("firered_0005.wav")
                    self._cursor = 0
            
            elif action.key == BattleActions.RIGHT.value:
                if self._cursor == 0:
                    SoundManager.getInstance().playSound("firered_0005.wav")
                    self._cursor = 1
            if old_pos != self._cursor: self._update_selected_pos(old_pos)
        else:
            self._pokemon_selected_menu.handle_event(action)

    def _update_selected_pos(self, old_pos):
        if self._cursor == 6:
            self._cancel_button.set_selected()
        else: 
            self._selectable_items[self._cursor].set_selected()
        
        if old_pos == 6: self._cancel_button.set_unselected()
        else: self._selectable_items[old_pos].set_unselected()
    
    def handle_select_event(self, action):
        if self._cursor == 6: 
            return (BattleStates.CHOOSING_FIGHT_OR_RUN, 0)
        else:
            if not self._selected_pokemon:
                self._selected_pokemon = True
                self._pokemon_selected_menu = PokemonSelectedMenu(self._player, self._cursor, battle=True)
                self._text_bar.blit_string("Do what with this PKMN?")
            else:
                response = self._pokemon_selected_menu.handle_event(action)
                if response == "cancel":
                    self._selected_pokemon = False
                    self._pokemon_selected_menu = None
                    self._text_bar.blit_string("Choose a POKeMON.")
                elif response == BattleStates.DISPLAY_PLAYER_TOSS_TEXT:
                    return (response, 0)
                elif response == "PKMN is already in battle!":
                    self._text_bar.blit_string(response)
    
    def update(self, ticks):
        for item in self._selectable_items:
            item.update(ticks)
        
class PokemonSelectedMenu(Drawable):
    def __init__(self, player, selected_pos, battle=False):
        self._player = player
        self._battle = battle
        self._selected_pos = selected_pos
        self._cursor = 0
        super().__init__("menu.png", (177, 113))
        self.blit_text()
        self.blit_arrow()
    
    def handle_event(self, action):
        if action.key == BattleActions.UP.value:
            if self._cursor > 0:
                SoundManager.getInstance().playSound("firered_0005.wav")
                self._cursor -= 1
                self.blit_arrow()

        elif action.key == BattleActions.DOWN.value:
            if self._cursor < self._num_lines - 1:
                SoundManager.getInstance().playSound("firered_0005.wav")
                self._cursor += 1
                self.blit_arrow()
        
        elif action.key == BattleActions.SELECT.value:
            SoundManager.getInstance().playSound("firered_0005.wav")
            if self._cursor == 2:
                return "cancel" # cancel
            elif self._cursor == 1:
                pass # summary
            elif self._cursor == 0:
                if self._selected_pos != 0:
                    self._player._pokemon_team[0], self._player._pokemon_team[self._selected_pos] = \
                        self._player._pokemon_team[self._selected_pos], self._player._pokemon_team[0]
                    self._player.set_active_pokemon(0)
                    print(self._player._pokemon_team)
                    return BattleStates.DISPLAY_PLAYER_TOSS_TEXT
                else:
                    return "PKMN is already in battle!"

        
    def blit_arrow(self):
        y_pos = self._cursor * 12
        position = (5, y_pos + 5)

        self._arrow = pygame.Surface((20,60))
        self._arrow.fill((255,255,255))
        self._arrow.set_colorkey((255,255,255))
        arrow_frame = FRAMES.getFrame(join("battle", "cursor.png"))
        self._arrow.blit(arrow_frame, position)

    def blit_text(self):
        if self._battle:
            lines = ["SHIFT", "SUMMARY", "CANCEL"]
            self._txt = pygame.Surface((160, 50))
            self._txt.fill((255,255,255))
            self._txt.set_colorkey((255,255,255))
            current_pos = Vector2(15, 7)
            for line in lines:
                for char in line:
                    font_index = int(ord(char)) - 65
                    font_char = FRAMES.getFrame("party_txt_font.png", offset=(font_index, 0))
                    font_char.set_colorkey((255,255,255))
                    self._txt.blit(font_char, (current_pos.x, current_pos.y))
                    if char != "I": current_pos.x += 5
                    else: current_pos.x += 4
                current_pos.y += 12
                current_pos.x = 15
            self._num_lines = len(lines)
            
        else: #TODO: Will be implemented later
            pass
    
    def draw(self, draw_surface):
        super().draw(draw_surface)
        draw_surface.blit(self._txt, self._position)
        draw_surface.blit(self._arrow, self._position)

class PokemonMenuPokemon(Drawable):
    def __init__(self, pokemon, position, bar_name, selected=False):
        self._pokemon = pokemon
        offset = (1,0) if selected else (0,0)
        super().__init__(bar_name, position, offset=offset)
        self._bouncing_pokemon = BouncingPokemon(self._pokemon, (0, 21))
        self._blit_level()
        self._blit_hp_bar()
        self._blit_hp_remaining()
    
    def set_selected(self):
        self._image = FRAMES.getFrame(self._imageName, (1,0))
    
    def set_unselected(self):
        self._image = FRAMES.getFrame(self._imageName, (0,0))
    
    def update(self, ticks):
        self._bouncing_pokemon.update(ticks)
    
    def _blit_level(self):
        self._lvl = pygame.Surface((10, 8))
        self._lvl.fill((255, 255, 255))
        self._lvl.set_colorkey((255,255,255))
        start_pos = Vector2(0, 0)
        current_pos = start_pos
        for char in str(self._pokemon.get_lvl()):
            font_index = int(ord(char)) - 48
            font_char = FRAMES.getFrame("party_font.png", offset=(font_index, 1))
            font_char.set_colorkey((0,128,0))
            self._lvl.blit(font_char, (current_pos.x, current_pos.y))
            current_pos.x += 5
    
    def _blit_hp_bar(self):
        green = (112, 248, 168)
        yellow = (248, 224, 56)
        red = (241, 14, 14)

        current_hp = self._pokemon._stats["Current HP"]
        max_hp = self._pokemon._stats["HP"]
        percentage = (current_hp / max_hp)
        
        self._hp = pygame.Surface((int(percentage * 48), 3))
        if percentage > .50: self._hp.fill(green)
        elif percentage > .15: self._hp.fill(yellow)
        else: self._hp.fill(red)
        self._hp_darken = pygame.Surface((48, 1))
        self._hp_darken.fill((0,0,0))
        self._hp_darken.set_alpha(50)
    
    def _blit_hp_remaining(self):
        self._hp_remaining = pygame.Surface((35, 8))
        self._hp_remaining.fill((255, 255, 255))
        self._hp_remaining.set_colorkey((255, 255, 255))
        current_hp = self._pokemon._stats["Current HP"]
        start_pos = Vector2(0,0)
        current_pos = start_pos
        for char in str(str(current_hp) + " " + str(self._pokemon._stats["HP"])):
            font_index = int(ord(char)) - 48
            font_char = FRAMES.getFrame("party_font.png", offset=(font_index, 1))
            font_char.set_colorkey((0,128,0))
            if char == " ": pass 
            else: self._hp_remaining.blit(font_char, (current_pos.x, current_pos.y))
            current_pos.x += 5

class ActivePokemon(PokemonMenuPokemon):
    def __init__(self, pokemon, selected=False):
        super().__init__(pokemon, (2, 18), "party_active_poke_bar.png", selected=selected)

    def draw(self, draw_surface):
        super().draw(draw_surface)
        self._bouncing_pokemon.draw(draw_surface)
        draw_surface.blit(self._lvl, (self._position[0] + 46, self._position[1] + 30))
        draw_surface.blit(self._hp_remaining, (self._position[0] + 49, self._position[1] + 46))
        draw_surface.blit(self._hp, (self._position[0] + 30, self._position[1] + 41))
        draw_surface.blit(self._hp_darken, (self._position[0] + 30, self._position[1] + 41))
    
class SecondaryPokemon(PokemonMenuPokemon):
    def __init__(self, pokemon, position, selected=False):
        super().__init__(pokemon, position, "party_individual_poke_bar.png",selected=selected)
        self._bouncing_pokemon = BouncingPokemon(self._pokemon, (self._position[0] - 5, self._position[1]-8))

    def draw(self, draw_surface):
        super().draw(draw_surface)
        self._bouncing_pokemon.draw(draw_surface)
        draw_surface.blit(self._hp, (self._position[0] + 96, self._position[1] + 9))
        draw_surface.blit(self._hp_darken, (self._position[0] + 96, self._position[1] + 9))
        draw_surface.blit(self._hp_remaining, (self._position[0] + 115, self._position[1] + 15))
        draw_surface.blit(self._lvl, (self._position[0] + 48, self._position[1] + 15))
        

class BouncingPokemon(Animated):
    def __init__(self, pokemon, position):
        self._pokemon = pokemon

        with open(join("jsons", "pokemon_lookup_s.json"), "r") as pokemon_lookup_json:
            pokemon_lookup = json.load(pokemon_lookup_json)
            _lookup = pokemon_lookup[self._pokemon.get_name()]
        _offset = (0, _lookup)
        super().__init__(join("pokemon", "pokemon_small.png"), position, offset=_offset)
        self._nFrames = 2
        self._row = _lookup
        self._framesPerSecond = 8

class CancelButton(Drawable):
    def __init__(self, selected=False):
        _offset = (1,0) if selected else (0,0)
        super().__init__("party_cancel_bar.png", (184, 132), offset=_offset)
    
    def set_selected(self):
        self._image = FRAMES.getFrame(self._imageName, (1,0))
    
    def set_unselected(self):
        self._image = FRAMES.getFrame(self._imageName, (0,0))
    

class PartyTextBar(Drawable):
    def __init__(self):
        super().__init__("party_text_box.png", (2, 130))
        self.blit_string("")
    
    def draw(self, draw_surface):
        super().draw(draw_surface)
        draw_surface.blit(self._txt, self._position)

    def blit_string(self, string):
        self._txt = pygame.Surface((160, 22))
        self._txt.fill((255,255,255))
        self._txt.set_colorkey((255,255,255))
        current_pos = Vector2(4, 4)
        for char in string:
            if char.islower(): 
                font_index = int(ord(char)) - 97
                font_char = FRAMES.getFrame("party_txt_font.png", offset=(font_index, 1))
                font_char.set_colorkey((255,255,255))
                self._txt.blit(font_char, (current_pos.x, current_pos.y))
            elif char == " ": pass
            else:
                off = 0
                font_index = int(ord(char)) - 65
                if char in [".", ","]: font_index = [",", "."].index(char) + 25
                elif char in ["!", "?"]: 
                    font_index = ["!", "?"].index(char)
                    off = 3
                font_char = FRAMES.getFrame("party_txt_font.png", offset=(font_index, off))
                font_char.set_colorkey((255,255,255))
                self._txt.blit(font_char, (current_pos.x, current_pos.y))
            if char != "i":
                current_pos.x += 5
            else:
                current_pos.x += 3
    

    
       
    

