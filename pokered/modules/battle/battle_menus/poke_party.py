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
        """Creates a poke party. This is what appears when you are choosing a pokemon. Shows the 
        pokemon in the players current party."""
        super().__init__("party_background.png",(0,0))
        self._player = player
        self._selectable_items = []
        self._blit_active_pokemon()
        self._blit_secondary_pokemon()
        self._cancel_button = CancelButton()
        self._text_bar = PartyTextBar()
        self._text_bar.blit_string("Choose a POKeMON.")
        self._cursor = 0
        self._selected_pokemon = False
        self._pokemon_selected_menu = None
        self._party_size = len(self._player.get_pokemon_team())
    
    def _blit_active_pokemon(self):
        """Creates the active pokemon object. This is the pokemon that appears on the left in the party screen."""
        self._active_pokemon = ActivePokemon(self._player.get_active_pokemon(), selected=True)
        self._selectable_items.append(self._active_pokemon)
    
    def _blit_secondary_pokemon(self):
        """Creates the other display objects. These are the pokemon that are not in position one."""
        position = (88,9)
        for pokemon in self._player.get_pokemon_team()[1:]:
            self._selectable_items.append(SecondaryPokemon(pokemon, position))
            position = (88, position[1] + 24)
    
    def draw(self, draw_surface):
        """Draws the active pokemon, all secondary pokemon, the cancel button, and the text box"""
        super().draw(draw_surface)
        self._cancel_button.draw(draw_surface)
        self._text_bar.draw(draw_surface)
        for item in self._selectable_items:
            item.draw(draw_surface)
        if self._pokemon_selected_menu != None:
            self._pokemon_selected_menu.draw(draw_surface)
    
    def change_cursor_pos(self, action):
        """Changes the cursor position. The cursor keeps track of which pokemon is selected.
        or where you are in the pokemon selected menu if a pokemon is selected."""
        if self._selected_pokemon == False:
            old_pos = self._cursor
            if action.key == BattleActions.UP.value:
                if self._cursor > 0:
                    if self._cursor == 6:
                        self._cursor = self._party_size - 1
                    else: self._cursor -= 1
                    SoundManager.getInstance().playSound("firered_0005.wav")

            elif action.key == BattleActions.DOWN.value:
                if self._cursor <= 5:
                    if self._cursor == self._party_size - 1:
                        self._cursor = 6
                    else: self._cursor += 1
                    SoundManager.getInstance().playSound("firered_0005.wav")
                    
            
            elif action.key == BattleActions.LEFT.value:
                if self._cursor > 0:
                    SoundManager.getInstance().playSound("firered_0005.wav")
                    self._cursor = 0
            
            elif action.key == BattleActions.RIGHT.value:
                if self._cursor == 0 and self._party_size > 1:
                    SoundManager.getInstance().playSound("firered_0005.wav")
                    self._cursor = 1
                if self._cursor == 0 and self._party_size == 1:
                    self._cursor = 6
                    SoundManager.getInstance().playSound("firered_0005.wav")

            if old_pos != self._cursor: self._update_selected_pos(old_pos)
        else:
            self._pokemon_selected_menu.handle_event(action)

    def _update_selected_pos(self, old_pos):
        """Toggles the appearance of the selectable objects (active pokmeon, secondary pokemon, and cancel button) 
        based on whether or not they are selected."""
        if self._cursor == 6:
            self._cancel_button.set_selected()
        else: 
            self._selectable_items[self._cursor].set_selected()
        
        if old_pos == 6: self._cancel_button.set_unselected()
        else: self._selectable_items[old_pos].set_unselected()
    
    def handle_back_event(self):
        """Handles a back event. If the the active pokemon is dead then a small error sound is played. If a poke menu is open,
        then the window is closed. Otherwise, the poke party closes."""
        if self._selected_pokemon:
            self._selected_pokemon = False
            self._pokemon_selected_menu = None
            self._text_bar.blit_string("Choose a POKeMON.")
        elif self._player.get_active_pokemon()._stats["Current HP"] == 0:
            SoundManager.getInstance().playSound("firered_0016.wav")
        else: return "change"

    
    def handle_select_event(self, action):
        """Handles a select event. If the user selects cancel then they return to the battle screen. Otherwise,
        a variety of checks are performed to perform the correct action."""
        if self._cursor == 6: 
            # If the pokemon is dead the screen can not be canceled
            if self._player.get_active_pokemon()._stats["Current HP"] == 0:
                SoundManager.getInstance().playSound("firered_0016.wav")
            else:return (BattleStates.CHOOSING_FIGHT_OR_RUN, 0)
        else:
            # If a pokemon has not been selected then select the pokmeon
            if not self._selected_pokemon:
                self._selected_pokemon = True
                self._pokemon_selected_menu = PokemonSelectedMenu(self._player, self._cursor, battle=True)
                self._text_bar.blit_string("Do what with this PKMN?")
            
            # Determine whether or not the pokemon can be sent into battle and act accordingly
            else:
                response = self._pokemon_selected_menu.handle_event(action)
                if response == "cancel":
                    self._selected_pokemon = False
                    self._pokemon_selected_menu = None
                    self._text_bar.blit_string("Choose a POKeMON.")
                elif response == BattleStates.PLAYER_TOSSING_POKEMON:
                    return (response, 0)
                elif response == "PKMN is already in battle!":
                    self._text_bar.blit_string(response)
                elif response == "PKMN is in no shape to battle!":
                    self._text_bar.blit_string(response)
    
    def update(self, ticks):
        """This update method allows the pokemon sprites to bounce up and down."""
        for item in self._selectable_items:
            item.update(ticks)
        
class PokemonSelectedMenu(Drawable):
    def __init__(self, player, selected_pos, battle=False):
        """Creates the menu that displays when a pokemon is selected."""
        self._player = player
        self._battle = battle
        self._selected_pos = selected_pos
        self._cursor = 0
        super().__init__("menu.png", (177, 113))

        # Add the text and cursor arrow to the menu
        self.blit_text()
        self.blit_arrow()
    
    def handle_event(self, action):
        """Handle wasd and select actions."""
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

            # If the select button is selected then cancel
            if self._cursor == 2:
                return "cancel"
            
            # If the summary button is selected then get summary NOTE: This is not implemented yet
            elif self._cursor == 1:
                pass # summary

            # If shift is selected then determine if the pokemon is eligible to battle
            elif self._cursor == 0:

                # Make sure the pokemon is not already battling
                if self._selected_pos != 0:

                    # Make sure the pokmeon is not dead
                    if not self._player._pokemon_team[self._selected_pos].is_alive():
                        return "PKMN is in no shape to battle!"
                    self._player._pokemon_team[0], self._player._pokemon_team[self._selected_pos] = \
                        self._player._pokemon_team[self._selected_pos], self._player._pokemon_team[0]
                    self._player.set_active_pokemon(0)
                    print(self._player._pokemon_team)
                    return BattleStates.PLAYER_TOSSING_POKEMON
                else:
                    return "PKMN is already in battle!"

        
    def blit_arrow(self):
        """Add the cursor arrow to the menu"""
        y_pos = self._cursor * 12
        position = (5, y_pos + 5)
        self._arrow = pygame.Surface((20,60))
        self._arrow.fill((255,255,255))
        self._arrow.set_colorkey((255,255,255))
        arrow_frame = FRAMES.getFrame(join("battle", "cursor.png"))
        self._arrow.blit(arrow_frame, position)

    def blit_text(self):
        """Add the text to the menu"""
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

                    # The I character is particularly small so add an extra space
                    if char != "I": current_pos.x += 5
                    else: current_pos.x += 4
                current_pos.y += 12
                current_pos.x = 15
            self._num_lines = len(lines)
            
        else: #TODO: Will need to be implemented for party system to work outside of battle
            pass
    
    def draw(self, draw_surface):
        """Draw the menu to the screen."""
        super().draw(draw_surface)
        draw_surface.blit(self._txt, self._position)
        draw_surface.blit(self._arrow, self._position)

class PokemonMenuPokemon(Drawable):

    def __init__(self, pokemon, position, bar_name, selected=False):
        """This is the base class for the pokemon objects in the menu. It displays the bouncing pokemon,
        the hp bar,  and the hp remaining."""
        self._pokemon = pokemon
        offset = (1,0) if selected else (0,0)
        super().__init__(bar_name, position, offset=offset)
        self._bouncing_pokemon = BouncingPokemon(self._pokemon, (0, 21))
        self._blit_level_and_gender()
        self._blit_hp_bar()
        self._blit_hp_remaining()
        self.reload()

        # If the pokemon is dead then make the box red
        if not self._pokemon.is_alive():
            if selected:
                pygame.transform.threshold(self._image, self._image.copy(), (120, 208, 232), set_color=(248, 184, 144), inverse_set=True)
                pygame.transform.threshold(self._image, self._image.copy(), (168, 232, 248), set_color=(248, 208, 216), inverse_set=True)
                pygame.transform.threshold(self._image, self._image.copy(), (72, 168, 200), set_color=(232, 160, 128), inverse_set=True)
            else:
                pygame.transform.threshold(self._image, self._image.copy(), (56, 144, 216), set_color=(192, 104, 16), inverse_set=True)
                pygame.transform.threshold(self._image, self._image.copy(), (128, 192, 216), set_color=(208, 160, 32), inverse_set=True)
                pygame.transform.threshold(self._image, self._image.copy(), (40, 120, 176), set_color=(162, 72, 0), inverse_set=True)
    
    def set_selected(self):
        """Gets the correct frame for a selected pokemon"""
        self._image = FRAMES.getFrame(self._imageName, (1,0))

        # If the pokemon is dead then make the box red
        if not self._pokemon.is_alive():
            pygame.transform.threshold(self._image, self._image.copy(), (120, 208, 232), set_color=(248, 184, 144), inverse_set=True)
            pygame.transform.threshold(self._image, self._image.copy(), (168, 232, 248), set_color=(248, 208, 216), inverse_set=True)
            pygame.transform.threshold(self._image, self._image.copy(), (72, 168, 200), set_color=(232, 160, 128), inverse_set=True)
    
    def set_unselected(self):
        """Gets the unselected frame for a pokemon"""
        self.reload()
        self._image = FRAMES.getFrame(self._imageName, (0,0))

        # If the pokemon is dead then make the box red
        if not self._pokemon.is_alive():
            pygame.transform.threshold(self._image, self._image.copy(), (56, 144, 216), set_color=(192, 104, 16), inverse_set=True)
            pygame.transform.threshold(self._image, self._image.copy(), (128, 192, 216), set_color=(208, 160, 32), inverse_set=True)
            pygame.transform.threshold(self._image, self._image.copy(), (40, 120, 176), set_color=(162, 72, 0), inverse_set=True)

    def update(self, ticks):
        """Updates the bouncing pokemon."""
        self._bouncing_pokemon.update(ticks)
    
    def _blit_level_and_gender(self):
        """Add the level and gender to the pokemon box"""
        self._lvl = pygame.Surface((40, 8))
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

        current_pos.x += 15
        font_index = 0 if self._pokemon.get_gender() == "male" else 1
        font_char = FRAMES.getFrame("gender.png", offset=(font_index,0))
        self._lvl.blit(font_char, (current_pos.x, current_pos.y))
    
    def _blit_hp_bar(self):
        """Add the hp bar to the pokemon box"""
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
        """Add the hp remaining string to the pokemon box"""
        self._hp_remaining = pygame.Surface((35, 8))
        self._hp_remaining.fill((255, 255, 255))
        self._hp_remaining.set_colorkey((255, 255, 255))
        current_hp = self._pokemon._stats["Current HP"]

        # This ensures that hp displays correctly even if it is less than three digits
        while len(str(current_hp)) < 3:
            current_hp = " " + str(current_hp)

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
        """Creates the active pokemon object. Inherits from PokemonMenuPokemon."""
        super().__init__(pokemon, (2, 18), "party_active_poke_bar.png", selected=selected)

    def draw(self, draw_surface):
        """Place the PokemonMenuPokemon's various aspects in the correct place."""
        super().draw(draw_surface)
        self._bouncing_pokemon.draw(draw_surface)
        draw_surface.blit(self._lvl, (self._position[0] + 46, self._position[1] + 30))
        draw_surface.blit(self._hp_remaining, (self._position[0] + 44, self._position[1] + 46))
        draw_surface.blit(self._hp, (self._position[0] + 30, self._position[1] + 41))
        draw_surface.blit(self._hp_darken, (self._position[0] + 30, self._position[1] + 41))
    
class SecondaryPokemon(PokemonMenuPokemon):

    def __init__(self, pokemon, position, selected=False):
        """Creates the active pokemon object. Inherits from PokemonMenuPokemon."""
        super().__init__(pokemon, position, "party_individual_poke_bar.png",selected=selected)
        self._bouncing_pokemon = BouncingPokemon(self._pokemon, (self._position[0] - 5, self._position[1]-8))

    def draw(self, draw_surface):
        """Place the PokemonMenuPokemon's various aspects in the correct place."""
        super().draw(draw_surface)
        self._bouncing_pokemon.draw(draw_surface)
        draw_surface.blit(self._hp, (self._position[0] + 96, self._position[1] + 9))
        draw_surface.blit(self._hp_darken, (self._position[0] + 96, self._position[1] + 9))
        draw_surface.blit(self._hp_remaining, (self._position[0] + 110, self._position[1] + 15))
        draw_surface.blit(self._lvl, (self._position[0] + 48, self._position[1] + 15))


class BouncingPokemon(Animated):
    def __init__(self, pokemon, position):
        """Creates a simple bouncing pokemon object. This appear on the left of the pokemon cards/objects"""
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
        """Creates a simple cancel button which is seen in the bottom right of the screen. Has
        a different appearance based on whether or not it is selected."""
        _offset = (1,0) if selected else (0,0)
        super().__init__("party_cancel_bar.png", (184, 132), offset=_offset)
    
    def set_selected(self):
        """Get the frame for when the image is selected."""
        self._image = FRAMES.getFrame(self._imageName, (1,0))
    
    def set_unselected(self):
        """Get the frame for when the image is not selected."""
        self._image = FRAMES.getFrame(self._imageName, (0,0))
    

class PartyTextBar(Drawable):
    def __init__(self):
        """"Creates the text bar which displays in the bottom right of the pokemon party menu screen."""
        super().__init__("party_text_box.png", (2, 130))
        self.blit_string("")
    
    def draw(self, draw_surface):
        """Draws the text box to the screen."""
        super().draw(draw_surface)
        draw_surface.blit(self._txt, self._position)

    def blit_string(self, string):
        """Get a surface representing the text that should be displayed."""
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

            # The lower case i char is much smaller than other characters and thus needs more space
            if char != "i":
                current_pos.x += 5
            else:
                current_pos.x += 3
    

    
       
    

