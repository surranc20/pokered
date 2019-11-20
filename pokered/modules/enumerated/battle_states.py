from enum import Enum

class BattleStates(Enum):
    """Simple Enumeration of battle states. The value is a list of valid actions
    and the corresponding state after that action is taken. There are numbers in the
    tuple just so that the states are not viewed as synonyms for eachother. The actual 
    numbers have no meaning."""
    NOT_STARTED = ("auto", 1)
    OPENING_ANIMS = ("wait", 2)
    OPPONENT_TOSSING_POKEMON = ("auto", 3)
    OPPONENT_CHOOSING_POKEMON = ("compute", 4)
    CHOOSING_POKEMON = ("wait", 5)
    CHOOSING_FIGHT_OR_RUN = ("wait", 6)
    CHOOSING_MOVE = ("wait", 7)
    PLAYER_TOSSING_POKEMON = ("auto", 9)
    CHOOSING_ITEM = ("wait", 10)
    EXECUTING_MOVE = ("auto", 11)
    PLAYER_POKEMON_MENU = ("auto", 13)
    OPPONENT_POKEMON_MENU = ("auto", 14)
    RUNNING = ("text wait", 17)
    UPDATE_ENEMY_STATUS = ("auto", 19)
    TEST = ("auto", 18)
    OPPONENT_CHOOSING_MOVE = ("compute", 20)
    UPDATE_PLAYER_STATUS = ("auto", 21)
    OPPONENT_POKEMON_DIED = ("compute", 22)
    TEXT_WAIT = ("text wait", 23)
    CHOOSE_OPPONENT_ACTION = ("compute", 24)
    DECIDING_BATTLE_ORDER = ("compute", 25)
    EXECUTE_TURN = ("compute", 26)
    MOVE_ANIMATION = ("auto", 27)
    DISPLAY_EFFECT = ("text wait", 28)
    OPPONENT_MOVE_TEXT = ("text wait", 29)
    PLAYER_MOVE_TEXT = ("text wait", 30)
    CHECK_HEALTH = ('compute', 31)
    PLAYER_POKEMON_DIED = ("compute", 32)
    VICTORY = ("compute", 33)
    BATTLE_OVER = ("finished", 34)
    OPPONENT_FEINT = ("auto", 35)
    PLAYER_FEINT = ("auto", 36)