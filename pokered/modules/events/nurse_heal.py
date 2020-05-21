from .response_dialogue import ResponseDialogue
from .dialogue import Dialogue
from ..utils.UI.animated import Animated
from ..enumerated.cardinality import Cardinality
from ..utils.managers.soundManager import SoundManager


class NurseHeal():
    def __init__(self, nurse, player):
        self._player = player
        self._player.heal_all()
        self._nurse = nurse
        self._balls = []
        screen_pos = (self._nurse._position[0] + 3,
                      self._nurse._position[1] - 17)
        self._screen = Animated("poke_center_screens.png", screen_pos)
        self._screen._nFrames = 4
        self._create_balls()
        self._response_dialogue = ResponseDialogue("16", self._player,
                                                   self._nurse)
        self._dialogue = Dialogue("17", self._player, self._nurse,
                                  show_curs=False)
        self._healed_dialogue = Dialogue("18", self._player, self._nurse)
        self._nurse_turned = False
        self._choice_box_cleared = False
        self.turned = True
        self._is_dead = False

        # Ball place animation portion
        self._ballTimer = 0
        self._ballsPerSecond = 2
        self._balls_placed = False
        self._num_placed = 0

        # Flash animation portion
        self._flash_timer = 0

        # Static pokeballs animation portion
        self._flash_finished = False
        self._static_timer = 0
        self._static_finished = False

    def update(self, ticks):
        if self._healed_dialogue.is_over():
            self._is_dead = True
        if self._static_finished:
            self._healed_dialogue.update(ticks)
        elif self._flash_finished:
            self._static_timer += ticks
            if self._static_timer > .7:
                self._nurse.turn(Cardinality.SOUTH)
                self.turned = False
                self._static_finished = True
        elif self._balls_placed:
            self._flash_timer += ticks
            if self._flash_timer > 2.3:
                self._flash_finished = True
                for ball in self._balls:
                    ball._frame = 0
                    ball.get_current_frame()
                self._screen._frame = 0
                self._screen.get_current_frame()

            else:
                for ball in self._balls:
                    ball.update(ticks)
                self._screen.update(ticks)

        elif self._dialogue.is_over():
            if not self._nurse_turned:
                self._nurse_turned = True
                self._nurse.turn(Cardinality.WEST)
                self.turned = False

            self._ballTimer += ticks
            if self._ballTimer > 1 / self._ballsPerSecond:
                self._ballTimer -= 1 / self._ballsPerSecond
                self._num_placed += 1
                if self._num_placed == len(self._balls) + 1:
                    self._balls_placed = True
                    SoundManager.getInstance().playSound("pokemon_healed.wav")
                else:
                    SoundManager.getInstance().playSound("firered_0017.wav", sound=2)

        else:
            if self._response_dialogue.is_over():
                if not self._choice_box_cleared:
                    self.turned = False
                    self._choice_box_cleared = True
                self._dialogue.update(ticks)
            else:
                self._response_dialogue.update(ticks)

    def draw(self, draw_surface):
        if self._static_finished:
            self._healed_dialogue.draw(draw_surface)
        elif self._dialogue.is_over():
            self._dialogue.draw(draw_surface)
            for ball in self._balls[:self._num_placed]:
                ball.draw(draw_surface)
                print(ball._frame)
            self._screen.draw(draw_surface)
        elif self._response_dialogue.is_over():
            self._dialogue.draw(draw_surface)
        else:
            self._response_dialogue.draw(draw_surface)

    def handle_event(self, event):
        if self._static_finished:
            self._healed_dialogue.handle_event(event)
        if not self._response_dialogue.is_over():
            self._response_dialogue.handle_event(event)
        elif not self._dialogue.is_over():
            self._dialogue.handle_event(event)

    def get_end_event(self):
        return "Level"

    def is_over(self):
        return self._is_dead

    def _create_balls(self):
        x_pos = self._nurse._position[0] - 22
        y_pos = self._nurse._position[1] - 3
        for x in range(len(self._player.pokemon_team)):
            if x % 2 == 0:
                ball_pos = (x_pos, y_pos)
            else:
                ball_pos = (x_pos + 6, y_pos)
                y_pos += 4
            ball = Animated("poke_center_balls.png", ball_pos)
            ball._nFrames = 5
            self._balls.append(ball)
