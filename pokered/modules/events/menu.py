import pygame


class Menu():
    def __init__(self):
        """Creates the pause menu for the game."""
        self._is_over = False
        self._save_queued = False

    def draw(self, draw_surface):
        """Draws the menu."""
        pass

    def update(self, ticks):
        """Updates the menu."""
        if self._save_queued:
            print("yo")
            return "Pickle"

    def handle_event(self, event):
        """Handles the inputs and updates menu accordingly."""
        if event.type == pygame.KEYDOWN:
            self._save_queued = True
            self._is_over = True

    def is_over(self):
        """Determines whether or not the menu is closed."""
        return self._is_over

    def get_end_event(self):
        """Returns the player back to the level."""
        return "Level"
