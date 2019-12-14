import pygame
from os.path import join, exists

from ..utils.vector2D import Vector2
from ..utils.drawable import Drawable
from ..utils.animated import AnimatedGroup
from ..utils.soundManager import SoundManager
from ..animations.toss_pokemon import TossPokemon
from ..animations.moves.scrolling_move import ScrollingMove
from ..pokemon import Pokemon
from .battle_menus.poke_info import PokeInfo
from .battle_menus.pokemon_remaining import PokemonRemaining
from .battle_fsm import BattleFSM
from ..white_out import WhiteOut
from ..movie import Movie



class Battle:
    def __init__(self, player, opponent):
        """Creates the battle event between the player and an opponent."""
        # Since nothing in the battle is world bound we can simply set WINDOW_OFFSET to 0 here and it
        # will not update again until the battle is over.
        Drawable.WINDOW_OFFSET = Vector2(0,0)
        self._player = player
        self._opponent = opponent
        self._battle_fsm = BattleFSM(player, opponent)

        SoundManager.getInstance().playMusic("gym_battle_music.mp3", -1, .4)

    
    def handle_event(self, event):
        """Handles the event by passing it to the battle_fsm."""
        self._battle_fsm.handle_action(event)
    
    def draw(self, draw_surface):
        """Gets the draw list from the battle_fsm and draws each item in the list."""
        for obj in self._battle_fsm.get_draw_list():
            if obj != None:
                obj.draw(draw_surface)

    def update(self, ticks):
        """Gets the update list from the battle_fsm and updates each item in the list."""
        self._battle_fsm.update(ticks)
        for obj in self._battle_fsm.get_update_list():
            # If the move is a scrolling move make sure to grab the background and update it.
            if issubclass(type(obj), ScrollingMove):
                background = obj.update(ticks)
                self._battle_fsm._scrolling_background_surf = background
            
            # Otherwise simply update the object.
            else:
                new_anim = obj.update(ticks)
    
    def is_over(self):
        """Return whether or not the battle is over. If it is over it gets the end event from the opponent."""
        if self._battle_fsm.is_over():
            pygame.mixer.music.pause()
            self._event = self._opponent._event
        return self._battle_fsm.is_over()

    def get_end_event(self):
        """Returns the end event that will happen after the battle is over."""
        if not self._battle_fsm._player_lost: self._opponent.defeated = True
        if self._battle_fsm._player_lost:
            return WhiteOut(self._player)
        elif self._opponent.get_name().lower() == "lance":
            return Movie("outro_folder")
        else:
            return self._event
