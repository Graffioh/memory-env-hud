from enum import Enum

class MoveResult(Enum):
    SUCCESS = 1
    INVALID = 2
    ERROR = 3
    GAME_OVER = 4