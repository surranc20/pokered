from enum import Enum, auto
from .animated import AnimatedGroup

class BattleStates(Enum):
    """Simple Enumeration of battle states. The value is a list of valid actions
    and the corresponding state after that action is taken"""
    NOT_STARTED = []
    OPENING_ANIMS = []
    OPPONENTS_CHOOSING_POKEMON = []
    OPPONENTS_MOVE = []
    CHOOSING_POKEMON = []
    CHOOSING_FIGHT_OR_RUN = []
    CHOOSING_MOVE = []
    PLAYER_TOSSING_POKEMON = []
    OPPONENT_TOSSING_POKEMON = []
    CHOOSING_ITEM = []
    EXECUTING_MOVE = []
    FINISHED = []

class BattleActions(Enum):
    """Simple Enumeration of battle actions"""
    SELECT = auto()
    BACK = auto()
    UP = auto()
    LEFT = auto()
    DOWN = auto()
    RIGHT = auto()

class BattleFSM:
    def __init__(self, state=BattleStates.NOT_STARTED):
        self._state = state
    
    def manage_action(self, action):
        if action in [value[0] for value in self._state.value]:
            pass

    def get_state(self):
        return self._state
    
    def update(self, ticks):
        if type(self._state.value) == tuple:
            if self._state.value[0].is_dead():
                pass
        else:
            pass
    
    def is_dead(self):
        return self._state == BattleStates.FINISHED

