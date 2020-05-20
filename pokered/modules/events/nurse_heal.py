from .response_dialogue import ResponseDialogue
from .dialogue import Dialogue
from ..utils.UI.animated import Animated
from ..enumerated.cardinality import Cardinality


class NurseHeal():
    def __init__(self, nurse, player):
        self._player = player
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
        self._nurse_turned = False
        self._choice_box_cleared = False
        self.turned = True

    def update(self, ticks):
        if self._dialogue.is_over():
            if not self._nurse_turned:
                self._nurse_turned = True
                self._nurse.turn(Cardinality.WEST)
                self.turned = False
            for ball in self._balls:
                ball.update(ticks)
            self._screen.update(ticks)
        else:
            if self._response_dialogue.is_over():
                if not self._choice_box_cleared:
                    self.turned = False
                    self._choice_box_cleared = True
                self._dialogue.update(ticks)
            else:
                self._response_dialogue.update(ticks)

    def draw(self, draw_surface):
        if self._dialogue.is_over():
            self._dialogue.draw(draw_surface)
            for ball in self._balls:
                ball.draw(draw_surface)
            self._screen.draw(draw_surface)
        elif self._response_dialogue.is_over():
            self._dialogue.draw(draw_surface)
        else:
            self._response_dialogue.draw(draw_surface)

    def handle_event(self, event):
        if not self._response_dialogue.is_over():
            self._response_dialogue.handle_event(event)
        elif not self._dialogue.is_over():
            self._dialogue.handle_event(event)

    def is_over(self):
        return False

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
