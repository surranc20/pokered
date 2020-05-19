from .dialogue import Dialogue


class ResponseDialogue(Dialogue):
    def __init__(self, dialogue_id, player, npc, box=0, gender="male"):
        """Creates a Dialogue instance. The dialogue tells the object which
        lines the dialogue consists off. It requires the player and npc to
        passed in so that a battle can be created if necessary. Also, the
        color of the dialogue is based on the gender of the npc. A response
        Dialogue will end with a text box question and will store said
        response."""
        super().__init__(dialogue_id, player, npc, box=box, gender=gender)
        self.response = None
    
    def _blit_line(self):
        if self._current_line > len(self._dialogue):
            return
        super()._blit_line()
        if self._current_line == len(self._dialogue):
            self._text_cursor.deactivate()
    
    def _blit_response(self):
        """Blit the response box as well as the two prompts"""
        pass

    def is_over(self):
        return self.response is not None
