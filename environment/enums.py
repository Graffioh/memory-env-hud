"""Game move result enumerations."""

from enum import Enum


class MoveResult(Enum):
    """Enumeration of possible results from a game move."""
    
    MATCHING = 1  # The two selected cards match.
    NO_MATCH = 2  # The two selected cards do not match.
    INVALID = 3  # The move is invalid (e.g., out of bounds or already shown).
    ERROR = 4  # An error occurred while processing the move.
    GAME_OVER = 5  # The game has ended.
