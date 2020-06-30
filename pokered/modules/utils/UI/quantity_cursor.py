import pygame
from os.path import join
from ..managers.frameManager import FRAMES
from ..text_maker import TextMaker


class QuantityCursor():
    def __init__(self, pos):
        """Creates a Quantity Cursor. Shows number selected and the cursor's
        going up and down."""
        # Create the two arrow cursors.
        self.down_arrow_surf = FRAMES.getFrame("shop_menu_cursor.png")
        # The up arrow needs to be flipped horizontally. Need to make a
        # separate surface because FRAMES are Singleton. Directly transforming
        # the frame will also change the down cursor.
        self.up_arrow_surf = pygame.Surface(self.down_arrow_surf.get_size())
        self.up_arrow_surf.fill((255, 245, 245))
        self.up_arrow_surf.set_colorkey((255, 245, 245))
        self.up_arrow_surf.blit(pygame.transform.flip(self.down_arrow_surf,
                                                      False, True), (0, 0))

        # Create the position's of the cursors.
        self.up_pos = pos
        self.up_anchor = self.up_pos
        self.down_pos = (pos[0], pos[1] + 25)
        self.down_anchor = self.down_pos

        # Default pixel amount the cursor changes per change.
        self.current_delta = 1

        # Timer for cursors.
        self.timer = 0

        # Create the count surface which displays the amount of items selected.
        self.text_maker = TextMaker(join("fonts", "party_txt_font.png"))
        self.count_surf = self.text_maker.get_surface("x01")
        self.count_pos = (self.up_pos[0] + 1, self.up_pos[1] + 13)

    def change_count(self, count):
        """Changes the amount displayed on the cursor."""
        self.count_surf = \
            self.text_maker.get_surface(f"x{str(count).zfill(2)}")

    def draw(self, draw_surface):
        """Draws the two cursors and the amount selected."""
        draw_surface.blit(self.up_arrow_surf, self.up_pos)
        draw_surface.blit(self.count_surf, self.count_pos)
        draw_surface.blit(self.down_arrow_surf, self.down_pos)

    def update(self, ticks):
        """Updates the two cursors and changes their positions."""
        self.timer += ticks

        # Direction that the cursors are going. Anchor points are used to
        # determine when the cursor needs to change direction.
        if self.down_pos == self.down_anchor:
            self.current_delta = 1
        elif self.down_pos[1] - self.down_anchor[1] >= 2:
            self.current_delta = -1

        # Cursor only moves 5 times a second.
        if self.timer > .2:
            self.up_pos = (self.up_pos[0], self.up_pos[1] - self.current_delta)
            self.down_pos = (self.down_pos[0],
                             self.down_pos[1] + self.current_delta)
            self.timer -= .2
