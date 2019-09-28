from .mobile import Mobile
from .cardinality import Cardinality

class Player(Mobile):
    def __init__(self, position):
        super().__init__("trainer.png", position, Cardinality.NORTH)
        self._nFrames = 4
        self._framesPerSecond = 4
        self._running = False
        self._moving = False

    def move(self, event):
        """Updates _movement based on what is happening with wasd"""
        # If it is a keydown event flip _movement[key] to true and _movement[opposite key (ws, ad)] to false
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w: 
            self._orientation = Cardinality.NORTH
            self._moving = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_a: 
            self._orientation = Cardinality.WEST
            self._moving = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_s: 
            self._orientation = Cardinality.SOUTH
            self._moving = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_d: 
            self._orientation = Cardinality.EAST
            self._moving = T
        
        # If the key has been lifted then it is no longer being pressed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:
                self._moving = False