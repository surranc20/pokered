from enum import Enum, auto

class BattleStates(Enum):
    """Simple Enumeration of battle states. The value is a list of valid actions
    and the corresponding state after that action is taken"""
    NOT_STARTED = auto()
    OPENING_ANIM = auto()
    OPPONENTS_CHOOSING_POKEMON = auto()
    OPPONENTS_MOVE = auto()
    CHOOSING_POKEMON = auto()
    CHOOSING_FIGHT/RUN = auto()
    CHOOSING_MOVE = auto()
    CHOOSING_ITEM = auto()
    EXECUTING_MOVE = auto()
    FINISHED = auto()

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
        pass

    def get_state(self):
        return self._state