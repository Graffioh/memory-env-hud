from enum import Enum


class MoveResult(Enum):
    MATCHING = 1
    NO_MATCH = 2
    INVALID = 3
    ERROR = 4
    GAME_OVER = 5
