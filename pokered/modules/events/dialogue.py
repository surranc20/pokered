import pygame
import json
import textwrap
from os.path import join
from ..enumerated.battle_actions import BattleActions
from ..utils.UI.drawable import Drawable
from ..utils.managers.soundManager import SoundManager
from ..battle.battle import Battle
from ..utils.UI.text_cursor import TextCursor


class Dialogue():
    def __init__(self, dialogue_id, player, npc, box=0, gender="male",
                 show_curs=True, turn=True, dy=0, replace=None, 
                 auto_finish=False):
        """Creates a Dialogue instance. The dialogue tells the object which
        lines the dialogue consists off. It requires the player and npc to
        passed in so that a battle can be created if necessary. Also, the
        color of the dialogue is based on the gender of the npc. Replace is a
        list and allows dynamically changing aspects of the dialogue."""
        self._dialogue_frame = Drawable("dialog_boxes.png",
                                        (0, 110 + dy),
                                        offset=(0, box),
                                        world_bound=False)
        self._line_surface = pygame.Surface(
            (self._dialogue_frame.getSize()[0] - 10,
             self._dialogue_frame.getSize()[1])
             )
        self._player = player
        self._npc = npc
        self._npc.turn(
            self._npc.determine_direction_to_tile(player.current_tile.pos)
            )
        self._color = (232, 81, 78) if npc.gender == "female" else \
            (55, 88, 193)
        self._text_cursor = TextCursor((0, 0))
        self._text_cursor.activate()

        # Get lines from json
        with open(join("jsons", "lines.json"), "r") as lines_json:
            lines = json.load(lines_json)
            self._dialogue = lines[dialogue_id][0]
            self._end_battle = (True if lines[dialogue_id][1] == "True"
                                else False)

        self._dialogue = self._dialogue.split("\n")
        self._font = pygame.font.Font(join("fonts", "pokemon_fire_red.ttf"),
                                      15)
        self._current_line = 0
        # Display the first line of the dialogue
        self.replace = replace
        self.replace_index = 0
        self._dy = dy
        self._blit_line()
        self.turned = not turn
        self._show_curs = show_curs
        self._auto_finish = auto_finish

    def _blit_line(self):
        """Blits the next line to the line surface."""
        # If all lines have been blitted then increase current_line by one so
        # that is_dead can determine that the dialogue is over.
        if self._current_line >= len(self._dialogue):
            self._current_line += 1
            return
        # Otherwise, blit the next line to the line surface
        self._line_surface.fill((255, 255, 255))
        self._line_surface.set_colorkey((255, 255, 255))
        string_lyst = textwrap.wrap(self._dialogue[self._current_line],
                                    width=41)
        height = 10
        for string in string_lyst:
            string = string.replace("<player>", self._player.name.upper())
            string = string.replace("<rival>", self._player.rival_name.upper())
            if self.replace is not None:
                try:
                    while "<replace>" in string:
                        string = string.replace("<replace>", self.replace[self.replace_index], 1)
                        self.replace_index += 1
                except IndexError as e:
                    print(e)
                    pass
            rendered = self._font.render(string, False, self._color)
            self._line_surface.blit(rendered, (10, height))
            height += 15
        self._current_line += 1

        # Make sure the cusor is bouncing up and down at the end of the
        # dialogue.
        self._text_cursor.set_pos((rendered.get_width() + 10, height))

    def draw(self, draw_surface):
        """Draw the dialogue frame, text cursor, and line surface."""
        #self._npc.draw(draw_surface)
        #self._player.draw(draw_surface)

        self._dialogue_frame.draw(draw_surface)
        draw_surface.blit(self._line_surface, (6, 111 + self._dy))
        if self._show_curs:
            self._text_cursor.draw(draw_surface)

    def update(self, ticks):
        """Updates the cursor so that it can bounce up and down."""
        self._text_cursor.update(ticks)
        if self._auto_finish:
            self._blit_line()

    def handle_event(self, event):
        """If the player hits enter then blit the next line."""
        if event.type == pygame.KEYDOWN and \
                event.key == BattleActions.SELECT.value:
            SoundManager.getInstance().playSound("firered_0005.wav")
            self._blit_line()

    def is_over(self):
        """Determines whether the dialogue is over."""
        return self._current_line == len(self._dialogue) + 1

    def get_end_event(self):
        """Returns the event that happens after the dialgoue
        (if one exists)."""
        if self._end_battle:
            return Battle(self._player, self._npc)
        else:
            return "Level"
