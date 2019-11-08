from os.path import join
import pygame
from ..drawable import Drawable
from ..animated import Animated
from ..vector2D import Vector2
from ..frameManager import FRAMES
from ..battle_actions import BattleActions
from ..battle_states import BattleStates
from ..soundManager import SoundManager


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
    
    def change_cursor_pos(self, action):
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

    def _update_selected_pos(self, old_pos):
        if self._cursor == 6:
            self._cancel_button.set_selected()
        else: 
            self._selectable_items[self._cursor].set_selected()
        
        if old_pos == 6: self._cancel_button.set_unselected()
        else: self._selectable_items[old_pos].set_unselected()
    
    def handle_select_event(self):
        if self._cursor == 6: 
            return (BattleStates.CHOOSING_FIGHT_OR_RUN, 0)
        else:
            if not self._selected_pokemon:
                self._selected_pokemon = True
                


            
        
    
    def update(self, ticks):
        for item in self._selectable_items:
            item.update(ticks)
        

class ActivePokemon(Drawable):
    def __init__(self, pokemon, selected=False):
        self._pokemon = pokemon
        offset = (1,0) if selected else (0,0)
        super().__init__("party_active_poke_bar.png", (2, 18), offset=offset)
        self._bouncing_pokemon = BouncingPokemon(self._pokemon, (0, 21))
        self._blit_level()
        self._blit_hp_bar()
        self._blit_hp_remaining()
    
    def set_selected(self):
        self._image = FRAMES.getFrame(self._imageName, (1,0))
    
    def set_unselected(self):
        self._image = FRAMES.getFrame(self._imageName, (0,0))

    def draw(self, draw_surface):
        super().draw(draw_surface)
        self._bouncing_pokemon.draw(draw_surface)
        draw_surface.blit(self._lvl, (self._position[0] + 46, self._position[1] + 30))
        draw_surface.blit(self._hp_remaining, (self._position[0] + 49, self._position[1] + 46))
        draw_surface.blit(self._hp, (self._position[0] + 30, self._position[1] + 41))
        draw_surface.blit(self._hp_darken, (self._position[0] + 30, self._position[1] + 41))
        
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
    
class SecondaryPokemon(Drawable):
    def __init__(self, pokmeon, position, selected=False):
        self._pokemon = pokmeon
        self._position = position
        offset = (1,0) if selected else (0,0)
        super().__init__("party_individual_poke_bar.png", self._position, offset=offset)
        self._bouncing_pokemon = BouncingPokemon(self._pokemon, (self._position[0] - 5, self._position[1]-8))
        self._blit_hp_bar()
        self._blit_hp_remaining()
        self._blit_level()
    
    def set_selected(self):
        self._image = FRAMES.getFrame(self._imageName, (1,0))
    
    def set_unselected(self):
        self._image = FRAMES.getFrame(self._imageName, (0,0))

    def draw(self, draw_surface):
        super().draw(draw_surface)
        self._bouncing_pokemon.draw(draw_surface)
        draw_surface.blit(self._hp, (self._position[0] + 96, self._position[1] + 9))
        draw_surface.blit(self._hp_darken, (self._position[0] + 96, self._position[1] + 9))
        draw_surface.blit(self._hp_remaining, (self._position[0] + 115, self._position[1] + 15))
        draw_surface.blit(self._lvl, (self._position[0] + 48, self._position[1] + 15))

    def update(self, ticks):
        self._bouncing_pokemon.update(ticks)
    
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
    

class BouncingPokemon(Animated):
    POKEMON_LOOKUP = {"bulbasaur": 0, "charmander":1, "squirtle":2, "caterpie":3, "weedle":4, "golem":5, "slowpoke":6, "magneton":7, "dodrio":8, "grimer":9,
    "ivysaur":10, "charmeleon":11, "wartortle":12, "metapod":13, "kakuna":14, "ponyta":15, "slowbro":16, "farfetch'd":17, "seel":18, "muk":19,
    "venusaur":20, "charazard":21, "blastoise":22, "butterfree":23, "beedrill":24, "rapidash":25, "magnemite":26, "doduo":27, "dewgong":28, "shellder":29,
    "pidgy":30, "rattata":31, "fearow":32, "pikachu":33, "sandslash":34, "cloyster":35, "gengar":36, "hypno":37, "voltorb":38, "exeggutor":39,
    "pidgeotto":40, "raticate":41, "ekans":42, "raichu":43, "nidoran_g":44, "gastly":45, "onyx":46, "krabby":47, "electrode":48, "cubone":49,
    "pidgeot":50, "spearow":51, "arbok":52, "sandshrew":53, "nidorina":54, "haunter":55, "drowsee":56, "kingler":57, "exeggcute":58, "marowak":59,
    "nidoqueen":60, "nidoking":(2,6), "vulpix":(4,6), "wigglytuff":(6,6), "oddish":(8,6), "hitmonlee":(10,6), "koffing":(12,6), "rhydon":(14,6), "kangaskhan":(16,6), "goldeen":(18,6),
    "nidoran_b":70, "clefairy":71, "ninetails":72, "zubat":73, "gloom":74, "hitmonchan":75, "weezing":76, "chansey":77, "horsea":78, "seaking":79,
    "nidorino":80, "clefable":81, "jigglypuff":82, "golbat":83, "vileplum":84, "lickitung":85, "rhyhorn":86, "tangela":87, "seadra":88, "staryu":89,
    "paras":90, "venomoth":91, "meowth":92, "golduck":93, "growlithe":94, "starmie":95, "jynx":96, "pinser":97, "gyrados":98, "eevee":99,
    "parasect":100, "diglett":101, "persian":102, "mankey":103, "arcanine":104, "mr. mime":105, "electabuzz":106, "taurus":107, "lapras":108, "vaporeon":109,
    "venonat":110, "dugtrio":111, "pysduck":112, "primeape":113, "poliwag":114, "scyther":115, "magmar":116, "magikarp":117, "ditto":118, "jolteon":119,
    "poliwhirl":120, "kadabra":121, "machoke":122, "weepinbell":123, "tentacruel":124, "flareon":125, "omastar":126, "aerodactyl":127, "zapdos":128, "dragonair":129,
    "poliwrath":130, "alakazam":131, "machamp":132, "victreebel":133, "geodude":134, "porygon":135, "kabuto":136, "snorlax":137, "moltres":138, "dragonite":139,
    "abra":140, "machop":141, "bellsprout":142, "tentacool":143, "graveler":144, "omanyte":145, "kabutops":146, "articuno":147, "dratini":148, "mewtwo":149,
    "mew":150}
    
    def __init__(self, pokemon, position):
        self._pokemon = pokemon
        _lookup = self.POKEMON_LOOKUP[self._pokemon.get_name()]
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
        self._txt = pygame.Surface((100, 22))
        self._txt.fill((255,255,255))
        self._txt.set_colorkey((255,255,255))
        current_pos = Vector2(4, 4)
        for char in string:
            if char.islower(): 
                font_index = int(ord(char)) - 97
                print(font_index)
                font_char = FRAMES.getFrame("party_txt_font.png", offset=(font_index, 1))
                font_char.set_colorkey((255,255,255))
                self._txt.blit(font_char, (current_pos.x, current_pos.y))
            elif char == " ": pass
            else:
                font_index = int(ord(char)) - 65
                print(char, font_index)
                if char in [".", ","]: font_index = [",", "."].index(char) + 25
                font_char = FRAMES.getFrame("party_txt_font.png", offset=(font_index, 0))
                font_char.set_colorkey((255,255,255))
                self._txt.blit(font_char, (current_pos.x, current_pos.y))
            current_pos.x += 5
    

    
       
    

