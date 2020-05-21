from .response_dialogue import ResponseDialogue
from .dialogue import Dialogue
from ..utils.UI.animated import Animated
from ..enumerated.cardinality import Cardinality
from ..utils.managers.soundManager import SoundManager


class NurseHeal():
    def __init__(self, nurse, player):
        self._is_dead = False
        self._player = player
        self._player.heal_all()
        self._nurse = nurse
        self._balls = []
        screen_pos = (self._nurse._position[0] + 3,
                      self._nurse._position[1] - 17)
        self._screen = Animated("poke_center_screens.png", screen_pos)
        self._screen._nFrames = 4
        self._create_balls()

        # Create dialogues that make up the nurse heal event.
        self._response_dialogue = ResponseDialogue("16", self._player,
                                                   self._nurse)
        self._dialogue = Dialogue("17", self._player, self._nurse,
                                  show_curs=False)
        self._healed_dialogue = Dialogue("18", self._player, self._nurse)
        self._no_dialogue = None

        # Control variables that allow us to tell level_manager to redraw
        # level for a frame to update changes to trainer or get rid of
        # response box.
        self._nurse_turned = False
        self._choice_box_cleared = False
        self.turned = True

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
        """Updates Nurse heal event. Last is coded first and first event is
        coded last."""
        # If the user answered no to the dialogue then update the dialogue and
        # end event once dialogue is over.
        if self._no_dialogue is not None:
            if self._no_dialogue.is_over():
                self._is_dead = True
            else:
                self._no_dialogue.update(ticks)

        # If the dialogue after healing is over then the heal event is over.
        elif self._healed_dialogue.is_over():
            self._is_dead = True

        # After done waiting then begin the heal dialgoue.
        elif self._static_finished:
            self._healed_dialogue.update(ticks)

        # After the balls and screen have finished flashing then wait .7
        # seconds. Nurse turns to face place at the end of waiting.
        elif self._flash_finished:
            self._static_timer += ticks
            if self._static_timer > .7:
                self._nurse.turn(Cardinality.SOUTH)
                self.turned = False
                self._static_finished = True

        # After the balls have been placed then the screen and balls begin
        # flashing for 2.3 seconds.
        elif self._balls_placed:
            self._flash_timer += ticks
            if self._flash_timer > 2.3:
                # After flashing set the balls and screen back to their
                # default frame.
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

        # After the nurse says she will take your pokemon she turns and begins
        # placing the balls.
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
                    SoundManager.getInstance().playSound("firered_0017.wav",
                                                         sound=2)

        # Handle the end of the response dialogue appropriately. If the user
        # wants to heal pokemon then update the healing dialogue here.
        elif self._response_dialogue.is_over():
            # User responds no so create an ending dialogue
            if self._response_dialogue.response == 1:
                self._no_dialogue = Dialogue("19", self._player, self._nurse)

            # Kinda hacky. To clear the choice box from the screen tell level
            # manager that an npc has turned so it redraws the level.
            if not self._choice_box_cleared:
                self.turned = False
                self._choice_box_cleared = True

            self._dialogue.update(ticks)

        # If the initial dialogue is not finished then update it.
        else:
            self._response_dialogue.update(ticks)

    def draw(self, draw_surface):
        """Draws the event. Follows the same flow as update so it is not
        commented."""
        if self._no_dialogue is not None:
            self._no_dialogue.draw(draw_surface)
        elif self._static_finished:
            self._healed_dialogue.draw(draw_surface)
        elif self._dialogue.is_over():
            self._dialogue.draw(draw_surface)
            for ball in self._balls[:self._num_placed]:
                ball.draw(draw_surface)
            self._screen.draw(draw_surface)
        elif self._response_dialogue.is_over():
            self._dialogue.draw(draw_surface)
        else:
            self._response_dialogue.draw(draw_surface)

    def handle_event(self, event):
        """Handles the event. Passes on event to the various dialogues that
        make up a heal event."""
        if self._no_dialogue is not None:
            self._no_dialogue.handle_event(event)
        if self._static_finished:
            self._healed_dialogue.handle_event(event)
        if not self._response_dialogue.is_over():
            self._response_dialogue.handle_event(event)
        elif not self._dialogue.is_over():
            self._dialogue.handle_event(event)

    def get_end_event(self):
        """Part of event framework. Tells level manager to return control to
        the level after nurse heal event is over."""
        return "Level"

    def is_over(self):
        """Part of event framework. Tells level manager if the event is
        over."""
        return self._is_dead

    def _create_balls(self):
        """Creates the list of pokeball objects that the nurse places in the
        machine."""
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
