import pygame
from os.path import join

from .dialogue import Dialogue
from ..utils.cursor import Cursor
from ..utils.UI.resizable_menu import ResizableMenu
from ..utils.text_maker import TextMaker
from ..enumerated.battle_actions import BattleActions


class ResponseDialogue(Dialogue):
    def __init__(self, dialogue_id, player, npc, box=0, gender="male",
                 response_string="YES NO", replace=None, dy=0):
        """Creates a Dialogue instance. The dialogue tells the object which
        lines the dialogue consists off. It requires the player and npc to
        passed in so that a battle can be created if necessary. Also, the
        color of the dialogue is based on the gender of the npc. A response
        Dialogue will end with a text box question and will store said
        response."""
        self._response_string = response_string
        super().__init__(dialogue_id, player, npc, box=box, gender=gender,
                         replace=replace, dy=dy)

        self.response = None
        self.response_menu = None

        if len(self._dialogue) == 1:
            self._text_cursor.deactivate()
            self._blit_response()

    def _blit_line(self):
        if self._current_line > len(self._dialogue):
            return
        super()._blit_line()
        if self._current_line == len(self._dialogue):
            self._text_cursor.deactivate()
            self._blit_response()

    def draw(self, draw_surface):
        super().draw(draw_surface)
        if self.response_menu is not None:
            draw_surface.blit(self.response_menu, (150, 70))
            self.cursor.draw(draw_surface)

    def handle_event(self, event):
        if self.response_menu is not None:
            if event.type == pygame.KEYDOWN:
                if event.key in [BattleActions.UP.value,
                                 BattleActions.DOWN.value]:
                    self.cursor.change_cursor_pos(event)
                elif event.key == BattleActions.SELECT.value:
                    self.response = self.cursor.cursor
        else:
            super().handle_event(event)

    def _blit_response(self):
        """Blit the response box as well as the two prompts"""
        self.response_menu = ResizableMenu(2, width=5).menu_surface
        text_maker = TextMaker(join("fonts", "party_txt_font.png"), max=15,
                               line_height=12)
        self.response_menu.blit(text_maker.get_surface(self._response_string),
                                (15, 11))
        self.cursor = Cursor(2, initial_pos=(156, 79))

    def is_over(self):
        return self.response is not None
