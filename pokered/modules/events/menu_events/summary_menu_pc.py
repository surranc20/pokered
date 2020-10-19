from .summary_menu import SummaryMenu, PokemonSummaryMenu
from ...utils.managers.soundManager import SoundManager
from ...utils.UI.drawable import Drawable
from ...utils.vector2D import Vector2
from ...enumerated.battle_actions import BattleActions


class SummaryMenuPC(SummaryMenu):
    """The summary page from the game"""
    def __init__(self, player, cursor_pos, box):
        """Creates the summary menu. Requires a player instead of a simple
        pokemon because it is possible to jump to the summary of other pokemon
        from the summary menu in the actual game."""
        super().__init__(player, cursor_pos)
        self.box = box
        self._update_active_page()
        self.end_event = None

        # Normal summary menu is coded under the assumption that the current
        # offset is 0. Remember old offset so it can be reset when summary
        # menu is closed.
        self._old_offset = Drawable.WINDOW_OFFSET
        Drawable.WINDOW_OFFSET = Vector2(0, 0)

    @property
    def is_dead(self):
        """Alias for self._is_dead"""
        # Reset offset once summary menu is closed.
        if self._is_dead:
            Drawable.WINDOW_OFFSET = self._old_offset
        return self._is_dead

    def handle_event(self, event):
        """Overwrites default handle_event so that pokemon selected now come
        from the box instead of the party."""

        # Same as the parent method
        if self._hcursor_pos == 2 and \
                (self._active_page._active_page.mode == "detail" or
                    self._active_page._active_page.mode == "switch"):
            self._active_page.handle_event(event)

        # Change up and down so that they now select the next available
        # pokemon in the box from that direction.
        elif event.key == BattleActions.UP.value:
            next_spot = self._up_exists()
            if self._vcursor_pos >= 1 and next_spot is not False:
                SoundManager.getInstance().playSound("firered_0005.wav")
                self._vcursor_pos = next_spot
                self._update_active_page()

        elif event.key == BattleActions.DOWN.value:
            next_spot = self._down_exists()
            if self._vcursor_pos < 29 and next_spot is not False:
                SoundManager.getInstance().playSound("firered_0005.wav")
                self._vcursor_pos = next_spot
                self._update_active_page()

        # The rest of the code is the same as the parent method.
        elif event.key == BattleActions.BACK.value:
            SoundManager.getInstance().playSound("firered_0005.wav")
            self._is_dead = True

        elif event.key == BattleActions.LEFT.value:
            if self._hcursor_pos > 0:
                SoundManager.getInstance().playSound("firered_0005.wav")
                self._hcursor_pos -= 1
                self._update_active_page()

        elif event.key == BattleActions.RIGHT.value:
            if self._hcursor_pos < 2:
                SoundManager.getInstance().playSound("firered_0005.wav")
                self._hcursor_pos += 1
                self._update_active_page()

        elif event.key == BattleActions.SELECT.value:
            if self._hcursor_pos == 0:
                self._is_dead = True
                SoundManager.getInstance().playSound("firered_0005.wav")
            elif self._hcursor_pos == 2:
                self._active_page.handle_event(event)

    def _up_exists(self):
        """Find the next pokemon in the box that comes before the current
        pokemon."""
        # Traverse through previous slots in the box until next pokemon is
        # found.
        for cursor_pos in range(self._vcursor_pos - 1, -1, -1):
            x, y = cursor_pos % 6, cursor_pos // 6
            if self.box[y][x] is not None:
                return cursor_pos

        return False

    def _down_exists(self):
        """Find the next pokemon in the box that comes after the current
        pokemon."""
        # Traverse through upcoming slots in the box until next pokemon is
        # found.
        for cursor_pos in range(self._vcursor_pos + 1, 30):
            x, y = cursor_pos % 6, cursor_pos // 6
            if self.box[y][x] is not None:
                return cursor_pos

        return False

    def _update_active_page(self):
        """Overwrites parent method to take pokemon from the box instead of
        the party."""
        # Get x, y coords from vcursor
        x, y = self._vcursor_pos % 6, self._vcursor_pos // 6
        self._active_page = \
            PokemonSummaryMenu(self.box[y][x], self._hcursor_pos)
