from ...level import Level
from ...events.white_out import WhiteOut
from ...battle.battle import Battle
from ...events.dialogue import Dialogue
from ...events.nurse_heal import NurseHeal
from ...events.poke_mart_event import PokeMartEvent
from ...events.pc_event import PCEvent
from ...events.menu import Menu
from ...events.movie import Movie
from ..scripting_engine import ScriptingEngine


class LevelManager(object):
    def __init__(self, player,
                 level_name,
                 screen_size=(240, 160),
                 movie=None):
        """Handles switching between a levels over world and the various
        events that could be happening. NOTE: Right now these events are
        called self._active_event. I will change this name later but I don't
        want to start refactoring code the night before demo day."""
        self._player = player
        self._level_name = level_name
        self._screen_size = screen_size
        self._level = Level(level_name, player, screen_size)
        self._active_event = None
        # If the level manager was passed a movie set the active event to the
        # movie.
        if movie is not None:
            self._active_event = Movie(movie)

    def draw(self, draw_surface):
        """If an event is happeing draw the event. Otherwise, draw the over
        world."""
        if self._active_event is None:
            self._level.draw(draw_surface)
        else:
            # Need to redraw once after starting a dialogue so we can draw the
            # turned npc
            if type(self._active_event) in [Dialogue, NurseHeal, PokeMartEvent,
                                            PCEvent] and \
                    self._active_event.turned is False:
                print(f"turned!: {self._active_event}")
                self._level.draw(draw_surface)
                self._active_event.turned = True
            self._active_event.draw(draw_surface)

    def handle_event(self, event):
        """If an even is happening have the event handle the pygame event,
        otherwise have the player
        handle the event."""
        if self._active_event is None:
            self._active_event = \
                self._player.handle_event(event,
                                          self._level.get_nearby_tiles(
                                              self._player.current_tile.pos))
            if type(self._active_event) == Menu:
                self._active_event.add_level_surface(self._level)
        else:
            self._active_event.handle_event(event)

    def update(self, ticks):
        """If an event is active update the event, otherwise update the
        level."""
        if self._active_event is None:
            response = self._level.update(ticks)
            if type(response) == Dialogue:
                self._active_event = response
            # Warped will be some non None value when it is time to change
            # levels.

            elif response is not None:
                return response

        # Update the current event.
        else:
            response = self._active_event.update(ticks)
            if self._active_event.is_over():
                end_event = self._active_event.get_end_event()
                if end_event is not None:
                    # This response means it is time for the game to restart.
                    if end_event == "RESTART":
                        return "RESTART"
                    # This response means the intro video is over and it is
                    # time to load the first level.
                    elif end_event == "INTRO OVER":
                        self._active_event = None
                        self._level.play_music()
                    elif end_event == "Level":
                        self._active_event = None
                    # This response means a dialogue event has ended and it is
                    # time to start a battle.
                    elif type(end_event) == Battle:
                        self._active_event = end_event
                    # This response means the player lost a battle and it is
                    # time to start the white out event.
                    elif type(end_event) == WhiteOut:
                        self._active_event = end_event
                    # This response means it is time to play a movie.
                    elif type(end_event) == Movie:
                        self._active_event = end_event
                    # This means the response was nothing and its time to
                    # return to the over world.
                    else:
                        self._level.current_scripting_engine = \
                            ScriptingEngine(end_event,
                                            self._level)
                        self._active_event = None
                        self._level.play_music()

            if response is not None:
                return response
