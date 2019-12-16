import pygame
from os.path import join
from .utils.managers.soundManager import SoundManager
from .enumerated.battle_actions import BattleActions

class Movie():
    def __init__(self, folder_name):
        """Creates a movie instance. I could not find a movie player that works well with pygame and won't close
        my game when playing the movie, so I decided to make my own. It takes the name of the folder where
        each of the frames of the movie is stored as a png."""
        # Create the surface where the movie will be displayed.
        self._surface = pygame.Surface((240,160))
        self._folder_name = folder_name
        # Which frame is the player currently on.
        self._counter = 0
        self._timer = 0
        self._fps = 20
        self._is_over = False
        # Load the first frame of the movie
        self._frame = pygame.image.load(join(self._folder_name, "scene00001.png"))
        self._frame.convert()
        self._surface.blit(self._frame, (0,0))

        # Play the appropriate audio for the movie
        if self._folder_name == "outro_folder":
            SoundManager.getInstance().playMusic("outro.mp3")
        else:
            SoundManager.getInstance().playMusic("intro.mp3")

    def draw(self, draw_surface):
        """Draw the movie to the screen"""
        draw_surface.blit(self._surface, (0,0))

    def update(self, ticks):
        """Update the frame of the movie. Ensures that the movie plays at the correct fps."""
        self._timer += ticks
        if self._timer > 1 / self._fps:
            self._counter += 1
            try:
                self._frame = pygame.image.load(join(self._folder_name, "scene" + self._get_num() + ".png"))
                self._frame.convert()
            # This will trigger once the movie has played all the way through. Right now the movie just restarts
            except:
                self._counter =1
                self._frame = pygame.image.load(join(self._folder_name, "scene" + self._get_num() + ".png"))
                self._frame.convert()
                if self._folder_name == "outro_folder":
                    SoundManager.getInstance().playMusic("outro.mp3")
                else:
                    SoundManager.getInstance().playMusic("intro.mp3")

            # Blit current frame to the movie surface
            self._surface.blit(self._frame, (0,0))
            self._timer -= 1 /self._fps

    def handle_event(self, event):
        """Handles the events for the movie player. Ends the video if the event is the select action."""
        if event.type == pygame.KEYDOWN and event.key == BattleActions.SELECT.value:
            SoundManager.getInstance().playSound("firered_0005.wav")
            self._is_over = True

    def is_over(self):
        """Returns whether or not the movie is over."""
        return self._is_over

    def get_end_event(self):
        """Get the event that will play after the video is over."""
        if self._folder_name == "intro_folder":
            return "INTRO OVER"
        elif self._folder_name == "outro_folder":
            return "RESTART"

    def _get_num(self):
        """Ensures that the counter object has the necessary padding of zeros."""
        return str(self._counter).zfill(5)


