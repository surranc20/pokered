from .level_manager import LevelManager


class GameManager(object):
    def __init__(self, screen_size, player):
        """Creates a simple game manager that manages which level the player
        is currently on. Right now this class really serves no purpose but if
        I ever decide to develop this project further I feel like this extra
        layer of abstraction may help."""
        self._player = player

        # Uncomment the below line to play the intro movie at startup. You will need
        # to download the into_folder seperately...
        # self._level = LevelManager(player, "elite_four_1", movie="intro_folder")
        self._level = LevelManager(player, "elite_four_1")
        self._FSM = "running"
        self.load = False

    def draw(self, surface):
        """Draws the current level."""
        if self._FSM == "running":
            self._level.draw(surface)

    def handle_event(self, event):
        """Tells the current level manager to handle the event"""
        if self._FSM == "running":
            self._level.handle_event(event)

    def update(self, ticks):
        """Tells the level to update."""
        if self._FSM == "running":
            # Warped is a response from the level manager after it has updated.
            # If it it not equal to None then it is the name of the level that
            # should be changed to. For the demo day it can also be the word
            # 'RESTART' and if this is the case the GameManager tells the game
            # to restart in the main.py file.

            if self.load:
                self.load = False
                self._level._level.reload()

            warped = self._level.update(ticks)
            if warped == "RESTART":
                return "RESTART"
            if warped == "Pickle":
                return "Pickle"
            if warped is not None:
                self._level = LevelManager(self._player, warped)
