from .mobile import Mobile
from .cardinality import Cardinality

class Player(Mobile):
    def __init__(self, position):
        super().__init__("trainer.png", position, Cardinality.NORTH)
        self._nFrames = 4
        self._framesPerSecond = 4