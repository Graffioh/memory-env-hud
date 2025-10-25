"""Memory Game Logic"""

import random
import numpy as np
from typing import Tuple, Optional

from enums import MoveResult


class GameMemory:
    """Text-based memory game implementation"""

    def __init__(self, size: int = 4):
        self.size = size
        self.board, self.shown = self.create_board()
        self.score = 0
        self.game_over = False
        self.moves_made = 0
        self.last_accumulated_reward = 0

    def create_board(self) -> Tuple[np.ndarray, np.ndarray]:
        """Create board with pairs and shown mask"""
        total = self.size * self.size
        if total % 2 != 0:
            raise ValueError("Board size must be even for pairs")
        nums = list(range(1, total // 2 + 1)) * 2
        random.shuffle(nums)
        board = np.array(nums).reshape(self.size, self.size)
        shown = np.zeros((self.size, self.size), dtype=bool)
        return board, shown

    def move(self, action: str) -> MoveResult:
        """Make a move by selecting two positions: 'r1 c1 r2 c2'"""

        # TODO when a move is made, the agent can't actually see the number behind the '?'

        if self.game_over:
            return MoveResult.GAME_OVER

        try:
            parts = action.split()
            if len(parts) != 4:
                return MoveResult.ERROR
            r1, c1, r2, c2 = map(int, parts)
        except ValueError:
            return MoveResult.ERROR

        if not (
            0 <= r1 < self.size
            and 0 <= c1 < self.size
            and 0 <= r2 < self.size
            and 0 <= c2 < self.size
        ):
            return MoveResult.INVALID

        if self.shown[r1, c1] or self.shown[r2, c2] or (r1, c1) == (r2, c2):
            return MoveResult.INVALID

        # Show both tiles
        self.shown[r1, c1] = True
        self.shown[r2, c2] = True

        self.moves_made += 1
        self.check_game_over()

        if self.game_over:
            return MoveResult.GAME_OVER
        elif self.board[r1, c1] == self.board[r2, c2]:
            # Match! Keep them shown
            self.score += 1
            return MoveResult.MATCHING
        else:
            return MoveResult.NO_MATCH

    def check_game_over(self):
        """Check if all tiles are matched"""
        self.game_over = np.all(self.shown)

    def get_board_ascii(self, debug) -> str:
        """Get ASCII representation of the board"""
        lines = []

        # Top border
        lines.append("+" + "-----+" * self.size)

        for i in range(self.size):
            row_str = "|"
            for j in range(self.size):
                val = self.board[i, j]

                # If closed in [...] then it's shown
                if self.shown[i, j] or debug:
                    row_str += f"[{val:2}]|"
                else:
                    row_str += "  ?  |"
            lines.append(row_str)
            lines.append("+" + "-----+" * self.size)

        # Add score and status
        lines.append(f"\nScore: {self.score}  Moves: {self.moves_made}")
        if self.game_over:
            lines.append("GAME OVER! All tiles matched.")

        return "\n".join(lines)

    def get_state(self) -> dict:
        """Get the current game state as a dictionary"""
        return {
            "board": self.board.tolist(),
            "shown": self.shown.tolist(),
            "score": int(self.score),
            "moves": int(self.moves_made),
            "game_over": bool(self.game_over),
            "last_accumulated_reward": float(self.last_accumulated_reward),
        }

    # Proxy-friendly getter methods for multiprocessing.Manager
    def get_score(self) -> int:
        """Get current score (proxy-friendly method)."""
        return self.score

    def get_moves_made(self) -> int:
        """Get number of moves made (proxy-friendly method)."""
        return self.moves_made

    def get_size(self) -> int:
        """Get board size (proxy-friendly method)."""
        return self.size

    def reset(self, size: Optional[int] = None):
        """Reset the game to initial state

        Args:
            size: Optional new board size (if not provided, keeps current size)
        """
        if size is not None:
            self.size = size
        self.board, self.shown = self.create_board()
        self.score = 0
        self.game_over = False
        self.moves_made = 0
        self.last_accumulated_reward = 0
