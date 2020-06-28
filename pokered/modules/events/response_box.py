from os.path import join
from ..utils.UI.resizable_menu import ResizableMenu
from ..utils.text_maker import TextMaker
from ..utils.cursor import Cursor
from ..utils.misc import end_at_all
from ..enumerated.battle_actions import BattleActions


class ResponseBox():
    """Class which creates a box of varying dimensions and will display the
    options as well as a cursor."""
    def __init__(self, lines, pos, width=8, line_height=None, dx=0, dy=0,
                 end_at=False):
        self.is_dead = False  # Tracks if an option has been selected.

        # Create text maker with the desired height
        text_maker = TextMaker(join("fonts", "party_txt_font.png"),
                               line_height)

        # Create the menu
        self.menu = ResizableMenu(len(lines), width=width).menu_surface

        # Position where menu will be drawn.
        if end_at:
            self.pos = end_at_all(self.menu, pos)
        else:
            self.pos = pos

        # Display options on menu
        y_pos = 12  # Blit first option 12 pixels down
        for line in lines:
            self.menu.blit(text_maker.get_surface(line), (16, y_pos))
            y_pos += text_maker.line_height

        # Create cursor the position of the response box offset by (7, 10)
        # Dx and Dy can be used for further granularity.
        self.cursor = Cursor(len(lines), (self.pos[0] + 7 + dx,
                                          self.pos[1] + 10 + dy))

    def draw(self, draw_surface):
        """Draws the menu (with the options) and the cursor."""
        draw_surface.blit(self.menu, self.pos)
        self.cursor.draw(draw_surface)

    def handle_event(self, event):
        """Update the cursor or select an option."""
        if event.key in [BattleActions.UP.value,
                         BattleActions.DOWN.value]:
            self.cursor.change_cursor_pos(event)

        elif event.key == BattleActions.SELECT.value:
            self.response = self.cursor.cursor
            self.is_dead = True
