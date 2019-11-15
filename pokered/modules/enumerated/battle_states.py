from enum import Enum

class BattleStates(Enum):
    """Simple Enumeration of battle states. The value is a list of valid actions
    and the corresponding state after that action is taken. There are numbers in the
    tuple just so that the states are not viewed as synonyms for eachother. The actual 
    numbers have no meaning."""
    NOT_STARTED = ("auto", 1)
    OPENING_ANIMS = ("wait", 2)
    OPPONENT_TOSSING_POKEMON = ("auto", 3)
    OPPONENTS_CHOOSING_POKEMON = ("compute", 4)
    CHOOSING_POKEMON = ("wait", 5)
    CHOOSING_FIGHT_OR_RUN = ("wait", 6)
    CHOOSING_MOVE = ("wait", 7)
    POKEMON_DEAD = (8)
    PLAYER_TOSSING_POKEMON = ("auto", 9)
    CHOOSING_ITEM = ("wait", 10)
    EXECUTING_MOVE = ("auto", 11)
    FINISHED = ("finished", 12)
    PLAYER_POKEMON_MENU = ("auto", 13)
    OPPONENT_POKEMON_MENU = ("auto", 14)
    DISPLAY_OPPONENT_TOSS_TEXT = ("text", 15)
    DISPLAY_PLAYER_TOSS_TEXT = ("text", 16)
    RUNNING = ("text wait", 17)
    UPDATE_ENEMY_STATUS = ("auto", 19)
    TEST = ("auto", 18)
    OPPONENT_CHOOSING_MOVE = ("compute", 20)
    UPDATE_PLAYER_STATUS = ("auto", 21)
    OPPONENT_POKEMON_DIED = ("auto", 22)