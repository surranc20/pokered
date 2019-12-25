import pygame
from ..utils.vector2D import Vector2
from ..utils.UI.drawable import Drawable
from ..utils.managers.soundManager import SoundManager
from ..animations.moves.scrolling_move import ScrollingMove
from .battle_fsm import BattleFSM
from ..events.white_out import WhiteOut


class Battle:
    def __init__(self, player, opponent):
        """Creates the battle event between the player and an opponent."""
        # Since nothing in the battle is world bound we can simply set
        # WINDOW_OFFSET to 0 here and it will not update again until the
        # battle is over.
        self._old_offset = (Drawable.WINDOW_OFFSET[0],
                            Drawable.WINDOW_OFFSET[1])
        Drawable.WINDOW_OFFSET = Vector2(0, 0)
        self._player = player
        self._opponent = opponent
        self._battle_fsm = BattleFSM(player, opponent)
        SoundManager.getInstance().playMusic("gym_battle_music.mp3", -1, .4)

    def handle_event(self, event):
        """Handles the event by passing it to the battle_fsm."""
        self._battle_fsm.handle_action(event)

    def draw(self, draw_surface):
        """Gets the draw list from the battle_fsm and draws each item in the
        list."""
        for obj in self._battle_fsm.get_draw_list():
            if obj is not None:
                obj.draw(draw_surface)

    def update(self, ticks):
        """Gets the update list from the battle_fsm and updates each item in
        the list."""
        self._battle_fsm.update(ticks)
        for obj in self._battle_fsm.get_update_list():
            # If the move is a scrolling move make sure to grab the background
            # and update it.
            if issubclass(type(obj), ScrollingMove):
                background = obj.update(ticks)
                self._battle_fsm._scrolling_background_surf = background

            # Otherwise simply update the object.
            else:
                obj.update(ticks)

    def is_over(self):
        """Return whether or not the battle is over. If it is over it gets the
        end event from the opponent."""
        if self._battle_fsm.is_over():
            pygame.mixer.music.pause()
            self._event = self._opponent.event
        return self._battle_fsm.is_over()

    def get_end_event(self):
        """Returns the end event that will happen after the battle is over."""
        Drawable.WINDOW_OFFSET = Vector2(self._old_offset[0],
                                         self._old_offset[1])
        if not self._battle_fsm._player_lost:
            self._opponent.defeated = True
            if self._event is not None:
                return self._event
            else:
                return "after_battle_dialog " + self._opponent.name + " " + \
                        str(self._opponent.post_battle_dialogue_id)
        if self._battle_fsm._player_lost:
            return WhiteOut(self._player)
        else:
            return self._event
